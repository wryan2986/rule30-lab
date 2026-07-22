from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import pytest

from rule30lab.predictor_search import (
    DFAO,
    canonical_binary_digits,
    decode_canonical_gf2_recurrence,
    decode_labeled_dfao,
    evaluate_dfao,
    fit_berlekamp_massey_candidate,
    fit_two_kernel_quotient_dfao,
    labeled_dfao_model_count,
    search_boolean_window_recurrences,
    search_labeled_dfaos,
    search_short_gf2_recurrences,
)


VECTORS = Path(__file__).resolve().parents[1] / "reference_vectors"


def _thue_morse(count: int) -> bytes:
    return bytes(index.bit_count() & 1 for index in range(count))


def _fibonacci_mod_two(count: int) -> bytes:
    values = bytearray((1, 0))
    while len(values) < count:
        values.append(values[-1] ^ values[-2])
    return bytes(values[:count])


def _assert_search_contract(report: dict[str, object]) -> None:
    assert report["finite_only_status"] == "bounded_finite_search"
    assert report["output_convention"] == "one exact bit c_n in {0,1}"
    assert report["machine_model"]
    assert report["index_input_convention"]
    assert report["preprocessing_and_advice_assumptions"]
    assert report["uniformity_assumption"]
    assert set(report["complexity_measure"]) == {
        "search_time",
        "search_space",
        "single_query_time",
        "single_query_space",
        "unit",
    }
    assert report["determinism"] == {
        "randomness_used": False,
        "deterministic_seed": 0,
    }
    assert report["proof_scope"]
    assert report["limitations"]


def test_canonical_binary_digits_and_explicit_dfao_evaluation() -> None:
    assert canonical_binary_digits(0) == (0,)
    assert canonical_binary_digits(6) == (1, 1, 0)
    assert canonical_binary_digits(6, order="lsb_first") == (0, 1, 1)

    parity = DFAO(
        transitions=((0, 1), (1, 0)),
        outputs=(0, 1),
        digit_order="msb_first",
    )
    assert bytes(evaluate_dfao(parity, n) for n in range(64)) == _thue_morse(64)

    with pytest.raises(ValueError, match="order"):
        canonical_binary_digits(1, order="middle")
    with pytest.raises(ValueError, match="at least 0"):
        canonical_binary_digits(-1)


def test_labeled_dfao_decoder_matches_independent_exhaustive_oracle() -> None:
    for state_count in (1, 2):
        independent = {
            (transitions, outputs)
            for flat_transitions in itertools.product(
                range(state_count), repeat=2 * state_count
            )
            for outputs in itertools.product((0, 1), repeat=state_count)
            for transitions in (
                tuple(
                    (flat_transitions[2 * state], flat_transitions[2 * state + 1])
                    for state in range(state_count)
                ),
            )
        }
        decoded = {
            (model.transitions, model.outputs)
            for model_id in range(labeled_dfao_model_count(state_count))
            for model in (decode_labeled_dfao(state_count, model_id),)
        }
        assert decoded == independent
        assert len(decoded) == labeled_dfao_model_count(state_count)


def test_dfao_search_exhaustively_finds_thue_morse_model() -> None:
    bits = _thue_morse(32)
    report = search_labeled_dfaos(
        bits,
        train_length=16,
        min_states=2,
        max_states=2,
        max_models=64,
        stop_after_fits=None,
        max_reported_fits=64,
    )
    _assert_search_contract(report)
    enumeration = report["enumeration"]
    assert enumeration["models_examined"] == 64
    assert enumeration["completed_full_bounded_space"] is True
    by_id = {
        candidate["model_id"]: candidate
        for candidate in report["training_fit_models"]
    }
    assert 26 in by_id
    assert by_id[26]["held_out_validation"]["exact_on_segment"] is True


def test_dfao_fit_is_independent_of_held_out_bits_and_reports_first_failure() -> None:
    original = _thue_morse(24)
    changed = bytearray(original)
    changed[19] ^= 1
    kwargs = {
        "train_length": 12,
        "min_states": 2,
        "max_states": 2,
        "max_models": 64,
        "stop_after_fits": None,
        "max_reported_fits": 64,
    }
    baseline = search_labeled_dfaos(original, **kwargs)
    perturbed = search_labeled_dfaos(changed, **kwargs)
    assert [item["model_id"] for item in baseline["training_fit_models"]] == [
        item["model_id"] for item in perturbed["training_fit_models"]
    ]
    changed_model = next(
        item for item in perturbed["training_fit_models"] if item["model_id"] == 26
    )
    assert changed_model["held_out_validation"]["first_counterexample"][
        "index"
    ] == 19


def test_dfao_checkpoint_partitions_the_model_id_range_exactly() -> None:
    bits = bytes((0, 1, 1, 0, 1, 0, 0, 1, 1, 1))
    first = search_labeled_dfaos(
        bits,
        train_length=7,
        min_states=2,
        max_states=2,
        max_models=17,
        stop_after_fits=None,
        max_reported_fits=64,
    )
    checkpoint = first["enumeration"]["checkpoint"]
    assert checkpoint == {"next_state_count": 2, "next_model_id": 17}
    second = search_labeled_dfaos(
        bits,
        train_length=7,
        min_states=2,
        max_states=2,
        start_state_count=checkpoint["next_state_count"],
        start_model_id=checkpoint["next_model_id"],
        max_models=64,
        stop_after_fits=None,
        max_reported_fits=64,
    )
    assert first["enumeration"]["models_examined"] == 17
    assert second["enumeration"]["models_examined"] == 47
    assert second["enumeration"]["completed_requested_range"] is True


def test_dfao_resource_and_identifier_caps_are_strict() -> None:
    with pytest.raises(MemoryError, match="encoded inputs"):
        search_labeled_dfaos(
            [0, 1, 0], train_length=2, max_input_symbols=2
        )
    with pytest.raises(ValueError, match="start_model_id"):
        search_labeled_dfaos(
            [0, 1, 0],
            train_length=2,
            min_states=1,
            max_states=1,
            start_model_id=3,
        )
    with pytest.raises(MemoryError, match="max_state_count_cap"):
        search_labeled_dfaos(
            [0, 1, 0],
            train_length=2,
            max_states=3,
            max_state_count_cap=2,
        )


def test_two_kernel_quotient_recovers_thue_morse_without_validation_leakage() -> None:
    original = _thue_morse(64)
    report = fit_two_kernel_quotient_dfao(
        original,
        train_length=32,
        depth=2,
        fingerprint_length=4,
    )
    _assert_search_contract(report)
    assert report["construction"]["quotient_state_count"] == 2
    assert report["construction"]["closed_and_transition_consistent"] is True
    assert report["candidate_training_validation"]["exact_on_segment"] is True
    assert report["held_out_validation"]["exact_on_segment"] is True

    changed = bytearray(original)
    changed[47] ^= 1
    perturbed = fit_two_kernel_quotient_dfao(
        changed,
        train_length=32,
        depth=2,
        fingerprint_length=4,
    )
    assert perturbed["candidate_model"] == report["candidate_model"]
    assert perturbed["held_out_validation"]["first_counterexample"]["index"] == 47


def test_two_kernel_quotient_enforces_full_child_data_and_resource_caps() -> None:
    with pytest.raises(ValueError, match="at least 32"):
        fit_two_kernel_quotient_dfao(
            _thue_morse(64),
            train_length=31,
            depth=2,
            fingerprint_length=4,
        )
    with pytest.raises(MemoryError, match="nodes"):
        fit_two_kernel_quotient_dfao(
            _thue_morse(64),
            train_length=32,
            depth=2,
            fingerprint_length=4,
            max_nodes=14,
        )
    with pytest.raises(MemoryError, match="before node-tree"):
        fit_two_kernel_quotient_dfao(
            _thue_morse(64),
            train_length=32,
            depth=1_000_000,
            fingerprint_length=1,
            max_nodes=1_000,
        )


def test_gf2_decoder_and_search_match_independent_small_oracle() -> None:
    assert [decode_canonical_gf2_recurrence(i) for i in range(8)] == [
        (),
        (1,),
        (0, 1),
        (1, 1),
        (0, 0, 1),
        (1, 0, 1),
        (0, 1, 1),
        (1, 1, 1),
    ]
    bits = _fibonacci_mod_two(24)

    def training_exact(coefficients: tuple[int, ...]) -> bool:
        for index in range(len(coefficients), 12):
            prediction = 0
            for lag, coefficient in enumerate(coefficients, start=1):
                prediction ^= coefficient & bits[index - lag]
            if prediction != bits[index]:
                return False
        return True

    expected_ids = [
        candidate_id
        for candidate_id in range(8)
        if training_exact(decode_canonical_gf2_recurrence(candidate_id))
    ]
    report = search_short_gf2_recurrences(
        bits,
        train_length=12,
        max_order=3,
        max_candidates=8,
        stop_after_fits=None,
        max_reported_fits=8,
    )
    _assert_search_contract(report)
    assert [
        item["candidate_id"] for item in report["training_fit_candidates"]
    ] == expected_ids
    recurrence = next(
        item
        for item in report["training_fit_candidates"]
        if item["coefficients"] == [1, 1]
    )
    assert recurrence["held_out_validation"]["exact_on_segment"] is True


def test_gf2_fit_does_not_read_held_out_and_checkpoint_resumes() -> None:
    original = _fibonacci_mod_two(24)
    changed = bytearray(original)
    changed[18] ^= 1
    kwargs = {
        "train_length": 12,
        "max_order": 3,
        "max_candidates": 8,
        "stop_after_fits": None,
        "max_reported_fits": 8,
    }
    baseline = search_short_gf2_recurrences(original, **kwargs)
    perturbed = search_short_gf2_recurrences(changed, **kwargs)
    assert [item["candidate_id"] for item in baseline["training_fit_candidates"]] == [
        item["candidate_id"] for item in perturbed["training_fit_candidates"]
    ]
    candidate = next(
        item
        for item in perturbed["training_fit_candidates"]
        if item["coefficients"] == [1, 1]
    )
    assert candidate["held_out_validation"]["first_counterexample"]["index"] == 18

    first = search_short_gf2_recurrences(
        original,
        train_length=12,
        max_order=3,
        max_candidates=3,
        stop_after_fits=None,
    )
    assert first["enumeration"]["checkpoint"] == {"next_candidate_id": 3}
    second = search_short_gf2_recurrences(
        original,
        train_length=12,
        max_order=3,
        start_candidate_id=3,
        max_candidates=5,
        stop_after_fits=None,
    )
    assert second["enumeration"]["completed_requested_range"] is True

    with pytest.raises(MemoryError, match="max_order_cap"):
        search_short_gf2_recurrences(
            original,
            train_length=12,
            max_order=3,
            max_order_cap=2,
        )


def test_berlekamp_massey_candidate_has_active_first_counterexample() -> None:
    bits = bytearray(_fibonacci_mod_two(24))
    bits[17] ^= 1
    report = fit_berlekamp_massey_candidate(bits, train_length=12)
    _assert_search_contract(report)
    assert report["candidate"]["coefficients"] == [1, 1]
    assert report["held_out_validation"]["first_counterexample"]["index"] == 17


def _independent_boolean_training_fits(
    bits: bytes, train_length: int, window: int
) -> list[int]:
    fits: list[int] = []
    for table_code in range(1 << (1 << window)):
        exact = True
        for index in range(window, train_length):
            context = 0
            for bit in bits[index - window : index]:
                context = (context << 1) | bit
            prediction = (table_code >> context) & 1
            if prediction != bits[index]:
                exact = False
                break
        if exact:
            fits.append(table_code)
    return fits


def test_boolean_window_constraints_match_exhaustive_truth_table_oracle() -> None:
    bits = bytes((1, 0, 1, 1, 0, 0, 1, 0, 1, 1))
    expected = _independent_boolean_training_fits(bits, train_length=7, window=2)
    report = search_boolean_window_recurrences(
        bits,
        train_length=7,
        min_window=2,
        max_window=2,
        max_completions=16,
        max_unseen_contexts=4,
        max_reported_candidates=16,
    )
    _assert_search_contract(report)
    summary = report["enumeration"]["window_summaries"][0]
    if expected:
        assert summary["training_consistent"] is True
        assert summary["completion_space_size"] == len(expected)
        reported_tables = {
            sum(
                bit << context
                for context, bit in enumerate(
                    item["truth_table"]["outputs_by_unsigned_context"]
                )
            )
            for item in report["reported_training_fit_candidates"]
        }
        assert reported_tables == set(expected)
    else:
        assert summary["training_consistent"] is False
        assert summary["completion_space_size"] == 0


def test_boolean_window_training_contradiction_is_an_exact_finite_witness() -> None:
    report = search_boolean_window_recurrences(
        [0, 0, 1, 0],
        train_length=3,
        min_window=1,
        max_window=1,
    )
    summary = report["enumeration"]["window_summaries"][0]
    assert summary["training_consistent"] is False
    assert summary["first_training_counterexample"] == {
        "kind": "same_window_has_two_following_bits",
        "window_value": 0,
        "window_bits": "0",
        "first_output_index": 1,
        "first_output": 0,
        "conflicting_output_index": 2,
        "conflicting_output": 1,
    }
    assert report["enumeration"]["completed_full_bounded_space"] is True


def test_boolean_window_completion_is_autonomous_and_reports_first_failure() -> None:
    report = search_boolean_window_recurrences(
        [0, 0, 1, 1, 0],
        train_length=2,
        min_window=1,
        max_window=1,
        max_completions=2,
        max_reported_candidates=2,
        max_reported_errors=0,
    )
    assert report["enumeration"]["completions_examined"] == 2
    for candidate in report["reported_training_fit_candidates"]:
        validation = candidate["held_out_validation"]
        assert validation["validation_protocol"].startswith("autonomous")
        assert validation["first_counterexample"]["index"] == 2
        assert validation["reported_counterexamples"] == []


def test_boolean_window_caps_return_stable_checkpoint() -> None:
    bits = bytes((0, 0, 0, 0, 1, 0, 1, 0))
    unseen_capped = search_boolean_window_recurrences(
        bits,
        train_length=4,
        min_window=3,
        max_window=3,
        max_unseen_contexts=2,
    )
    assert unseen_capped["enumeration"]["termination_reason"] == (
        "max_unseen_contexts_exceeded"
    )
    assert unseen_capped["enumeration"]["checkpoint"] == {
        "next_window": 3,
        "next_completion_id": 0,
    }

    first = search_boolean_window_recurrences(
        bits,
        train_length=4,
        min_window=3,
        max_window=3,
        max_unseen_contexts=8,
        max_completions=3,
        max_reported_candidates=0,
    )
    assert first["enumeration"]["termination_reason"] == "max_completions_reached"
    assert first["enumeration"]["checkpoint"] == {
        "next_window": 3,
        "next_completion_id": 3,
    }
    resumed = search_boolean_window_recurrences(
        bits,
        train_length=4,
        min_window=3,
        max_window=3,
        start_window=3,
        start_completion_id=3,
        max_unseen_contexts=8,
        max_completions=125,
        max_reported_candidates=0,
    )
    assert resumed["enumeration"]["completions_examined"] == 125
    assert resumed["enumeration"]["completed_requested_range"] is True

    with pytest.raises(MemoryError, match="before truth-table"):
        search_boolean_window_recurrences(
            [0] * 130 + [1],
            train_length=130,
            min_window=129,
            max_window=129,
            max_table_entries=1_024,
        )


def test_trusted_rule30_prefix_produces_deterministic_bounded_search_hashes() -> None:
    bits = (VECTORS / "center_c00000000_c00009999.u8").read_bytes()[:512]
    first = search_short_gf2_recurrences(
        bits,
        train_length=256,
        max_order=8,
        max_candidates=256,
        stop_after_fits=None,
    )
    second = search_short_gf2_recurrences(
        bits,
        train_length=256,
        max_order=8,
        max_candidates=256,
        stop_after_fits=None,
    )
    assert first == second
    assert hashlib.sha256(repr(first).encode()).hexdigest() == hashlib.sha256(
        repr(second).encode()
    ).hexdigest()
    assert first["enumeration"]["completed_full_bounded_space"] is True
    assert first["status"] == "finite-exhaustive"


def test_trusted_vector_experiment_payload_is_byte_deterministic() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    command = [
        sys.executable,
        str(
            repository_root
            / "experiments"
            / "problem3_complexity"
            / "run_exact_searches.py"
        ),
        "--limit-bits",
        "512",
        "--train-length",
        "256",
        "--dfao-max-states",
        "2",
        "--kernel-depth",
        "2",
        "--kernel-fingerprint-length",
        "16",
        "--gf2-max-order",
        "8",
        "--boolean-max-window",
        "8",
    ]
    first = subprocess.check_output(command, cwd=repository_root)
    second = subprocess.check_output(command, cwd=repository_root)
    assert first == second

    payload = json.loads(first)
    trusted = (VECTORS / "center_c00000000_c00009999.u8").read_bytes()[:512]
    assert payload["input"]["sha256_used_u8"] == hashlib.sha256(trusted).hexdigest()
    assert payload["training_validation_protocol"]["training"] == {
        "start": 0,
        "stop": 256,
    }
    assert payload["result_summary"]["completion"][
        "all_requested_searches_completed"
    ] is True


def test_all_searches_reject_invalid_binary_samples() -> None:
    with pytest.raises(ValueError, match="index 2"):
        search_labeled_dfaos([0, 1, 2, 0], train_length=2)
    with pytest.raises(ValueError, match="index 2"):
        search_short_gf2_recurrences(
            [0, 1, 2, 0], train_length=2, max_order=1
        )
    with pytest.raises(ValueError, match="index 2"):
        search_boolean_window_recurrences(
            [0, 1, 2, 0], train_length=2, max_window=1
        )
