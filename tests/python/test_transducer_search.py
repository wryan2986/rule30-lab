from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import pytest

from rule30lab.transducer_search import (
    AffineDigitModel,
    affine_encoding_bits,
    affine_model_count,
    decode_affine_model,
    evaluate_affine_model,
    finite_two_kernel_refinement,
    locate_first_counterexample,
    search_affine_digit_models,
)


ROOT = Path(__file__).resolve().parents[2]
VECTORS = ROOT / "tests" / "reference_vectors"
CAMPAIGN = (
    ROOT
    / "experiments"
    / "problem3_complexity"
    / "run_extended_model_searches.py"
)


def _thue_morse(count: int) -> bytes:
    return bytes(index.bit_count() & 1 for index in range(count))


def _parity_model() -> AffineDigitModel:
    return AffineDigitModel(
        dimension=1,
        initial_state=0,
        matrices=((1,), (1,)),
        translations=(0, 1),
        output_mask=1,
        output_bias=0,
    )


def _campaign_module():
    specification = importlib.util.spec_from_file_location(
        "run_extended_model_searches", CAMPAIGN
    )
    assert specification is not None and specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def _assert_contract(report: dict[str, object]) -> None:
    assert report["finite_only_status"] == "bounded_finite_search"
    assert report["determinism"] == {
        "randomness_used": False,
        "deterministic_seed": 0,
    }
    assert report["machine_model"]
    assert report["proof_scope"]
    assert report["limitations"]
    assert report["complexity_measure"]


def test_affine_model_encodes_binary_digit_parity_exactly() -> None:
    model = _parity_model()
    assert bytes(evaluate_affine_model(model, n) for n in range(128)) == (
        _thue_morse(128)
    )
    assert affine_encoding_bits(1) == 7
    assert affine_model_count(1) == 128


def test_affine_decoder_is_a_bijection_in_dimension_one() -> None:
    decoded = {
        (
            model.initial_state,
            model.matrices,
            model.translations,
            model.output_mask,
            model.output_bias,
        )
        for model_id in range(affine_model_count(1))
        for model in (decode_affine_model(1, model_id),)
    }
    assert len(decoded) == affine_model_count(1)
    with pytest.raises(ValueError, match="smaller"):
        decode_affine_model(1, affine_model_count(1))


def test_affine_search_finds_parity_and_is_finite_exhaustive() -> None:
    report = search_affine_digit_models(
        _thue_morse(64),
        train_length=32,
        min_dimension=1,
        max_dimension=1,
        max_models=128,
        max_selected_training_fits=128,
    )
    _assert_contract(report)
    assert report["enumeration"]["models_examined"] == 128
    assert report["enumeration"]["completed_requested_range"] is True
    assert report["enumeration"]["training_fit_count"] > 0
    assert any(
        candidate["held_out_validation"]["exact_on_segment"]
        for candidate in report["selected_candidates"]
    )


def test_affine_candidate_selection_cannot_read_held_out_bits() -> None:
    original = _thue_morse(48)
    changed = bytearray(original)
    changed[37] ^= 1
    arguments = {
        "train_length": 24,
        "min_dimension": 1,
        "max_dimension": 1,
        "max_models": 128,
        "max_selected_training_fits": 128,
    }
    baseline = search_affine_digit_models(original, **arguments)
    perturbed = search_affine_digit_models(changed, **arguments)
    baseline_ids = [
        (item["dimension"], item["model_id"])
        for item in baseline["selected_candidates"]
    ]
    perturbed_ids = [
        (item["dimension"], item["model_id"])
        for item in perturbed["selected_candidates"]
    ]
    assert baseline_ids == perturbed_ids
    assert baseline["enumeration"] == perturbed["enumeration"]
    changed_failures = [
        item["held_out_validation"]["first_counterexample"]
        for item in perturbed["selected_candidates"]
        if item["held_out_validation"]["first_counterexample"] is not None
    ]
    assert any(failure["index"] == 37 for failure in changed_failures)


def test_active_counterexample_locator_reports_exact_binary_index() -> None:
    bits = bytearray(_thue_morse(32))
    bits[19] ^= 1
    assert locate_first_counterexample(
        _parity_model(), bits, start=8, stop=32
    ) == {
        "index": 19,
        "index_binary": "10011",
        "predicted": _thue_morse(20)[19],
        "observed": bits[19],
    }


def test_affine_search_caps_and_checkpoint_are_exact() -> None:
    report = search_affine_digit_models(
        _thue_morse(32),
        train_length=16,
        min_dimension=1,
        max_dimension=2,
        max_models=17,
    )
    assert report["enumeration"]["models_examined"] == 17
    assert report["enumeration"]["completed_requested_range"] is False
    assert report["enumeration"]["checkpoint"] == {
        "next_dimension": 1,
        "next_model_id": 17,
    }
    assert report["status"] == "inconclusive"
    with pytest.raises(MemoryError, match="max_dimension_cap"):
        search_affine_digit_models(
            [0, 1], train_length=1, max_dimension=3, max_dimension_cap=2
        )


def test_affine_validation_cap_cannot_claim_full_completion() -> None:
    report = search_affine_digit_models(
        bytes(32),
        train_length=16,
        min_dimension=1,
        max_dimension=1,
        max_models=128,
        max_selected_training_fits=1,
    )
    assert report["enumeration"]["completed_requested_range"] is True
    assert report["enumeration"]["training_fit_count"] > 1
    assert report["completion"]["all_training_fits_validated"] is False
    assert report["completion"]["all_requested_searches_completed"] is False
    assert report["status"] == "inconclusive"


def test_kernel_refinement_recovers_thue_morse_classes() -> None:
    report = finite_two_kernel_refinement(
        _thue_morse(256),
        train_length=128,
        max_level=3,
        refinement_rounds=3,
    )
    _assert_contract(report)
    construction = report["construction"]
    assert construction["distinct_class_count_across_levels"] == 2
    assert construction["closed_and_transition_congruent"] is True
    assert report["candidate_model"]["training_validation"][
        "exact_on_segment"
    ]
    assert report["candidate_model"]["held_out_validation"][
        "exact_on_segment"
    ]
    assert report["completion"]["all_requested_searches_completed"] is True


def test_kernel_construction_is_independent_of_held_out_mutation() -> None:
    original = _thue_morse(256)
    changed = bytearray(original)
    changed[211] ^= 1
    arguments = {
        "train_length": 128,
        "max_level": 3,
        "refinement_rounds": 3,
    }
    baseline = finite_two_kernel_refinement(original, **arguments)
    perturbed = finite_two_kernel_refinement(changed, **arguments)
    assert baseline["construction"] == perturbed["construction"]
    assert (
        perturbed["candidate_model"]["held_out_validation"][
            "first_counterexample"
        ]["index"]
        == 211
    )


def test_kernel_refinement_enforces_training_and_resource_caps() -> None:
    with pytest.raises(ValueError, match="at least 128"):
        finite_two_kernel_refinement(
            _thue_morse(128),
            train_length=64,
            max_level=3,
            refinement_rounds=3,
        )
    with pytest.raises(MemoryError, match="max_nodes"):
        finite_two_kernel_refinement(
            _thue_morse(256),
            train_length=128,
            max_level=3,
            refinement_rounds=3,
            max_nodes=10,
        )


def test_campaign_payload_has_exact_completion_flags_and_is_deterministic() -> None:
    module = _campaign_module()
    arguments = argparse.Namespace(
        input=VECTORS / "center_c00000000_c00009999.u8",
        limit_bits=128,
        affine_train_length=24,
        pilot_train_length=8,
        affine_min_dimension=1,
        affine_max_dimension=1,
        affine_max_models=128,
        affine_selected_fits=8,
        kernel_train_length=96,
        kernel_max_level=2,
        kernel_refinement_rounds=3,
        kernel_max_nodes=10_000,
        kernel_max_work_entries=100_000,
    )
    first = module.build_payload(arguments)
    second = module.build_payload(arguments)
    assert json.dumps(first, sort_keys=True, allow_nan=False) == json.dumps(
        second, sort_keys=True, allow_nan=False
    )
    completion = first["result_summary"]["completion"]
    assert completion == {
        "affine_primary_completed": True,
        "affine_short_training_counterexample_probe_completed": True,
        "multiscale_two_kernel_completed": True,
        "all_requested_searches_completed": True,
    }
    assert first["status"] == "finite-exhaustive"
    assert "nonautomaticity" in " ".join(first["limitations"])
