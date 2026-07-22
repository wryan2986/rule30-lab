from __future__ import annotations

import importlib.util
import math
import sys
from collections import Counter
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPOSITORY_ROOT
    / "experiments"
    / "problem2_balance"
    / "run_scaling_analysis.py"
)
SPEC = importlib.util.spec_from_file_location("rule30_scaling_analysis", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
scaling = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = scaling
SPEC.loader.exec_module(scaling)


def _records_by_n(payload: dict[str, object]) -> dict[int, dict[str, object]]:
    subresults = payload["subresults"]
    assert isinstance(subresults, dict)
    section = subresults["checkpoint_discrepancy"]
    assert isinstance(section, dict)
    records = section["records"]
    assert isinstance(records, list)
    return {int(record["n"]): record for record in records}


def test_hand_prefix_has_exact_scans_and_explicit_statuses() -> None:
    bits = bytes((1, 1, 0, 0, 1, 0, 1, 0))
    payload = scaling.build_scientific_payload(
        bits,
        checkpoints=(1, 2, 4, 8),
        fit_checkpoints=(1, 2, 4, 8),
        dyadic_widths=(2, 4, 8),
        block_widths=(1, 2),
        lags=(1, 2),
    )

    records = _records_by_n(payload)
    assert {n: record["discrepancy"] for n, record in records.items()} == {
        1: 1,
        2: 2,
        4: 0,
        8: 0,
    }
    normalizations = records[2]["normalizations"]
    assert normalizations["status"] == "empirical"
    assert normalizations["result_kind"] == "descriptive_finite_normalization"
    assert normalizations["discrepancy_over_sqrt_n"] == pytest.approx(math.sqrt(2))
    assert normalizations["discrepancy_over_n"] == 1.0
    assert normalizations["discrepancy_over_n_exact"] == {
        "numerator": 2,
        "denominator": 2,
    }

    subresults = payload["subresults"]
    assert subresults["checkpoint_discrepancy"]["status"] == "finite-exhaustive"
    assert subresults["maximum_absolute_prefix_discrepancy"] == {
        "status": "finite-exhaustive",
        "result_kind": "exact_finite_prefix_scan",
        "n": 2,
        "discrepancy": 2,
        "absolute_discrepancy": 2,
    }

    block_records = {
        record["width"]: record
        for record in subresults["block_frequency_ranges"]["records"]
    }
    assert block_records[1]["minimum_count"] == 4
    assert block_records[1]["maximum_count"] == 4
    assert block_records[2]["minimum_count"] == 1
    assert block_records[2]["maximum_count"] == 3

    correlations = {
        record["lag"]: record
        for record in subresults["spin_autocorrelation"]["records"]
    }
    assert (correlations[1]["numerator"], correlations[1]["denominator"]) == (
        -3,
        7,
    )
    assert (correlations[2]["numerator"], correlations[2]["denominator"]) == (
        0,
        6,
    )

    runs = subresults["runs"]["record"]
    assert runs["run_count"] == 6
    assert runs["length_histogram"] == {1: 4, 2: 2}
    assert runs["mean_run_length_exact"] == {"numerator": 8, "denominator": 6}

    fit = subresults["discrepancy_scaling_fit"]
    assert fit["status"] == "heuristic"
    assert fit["slope"] == pytest.approx(1.0)
    assert fit["coefficient"] == pytest.approx(1.0)
    assert fit["r_squared"] == pytest.approx(1.0)
    assert [sample["n"] for sample in fit["excluded_zero_discrepancy_samples"]] == [
        4,
        8,
    ]
    assert "no pseudocount" in fit["zero_handling"]


def test_fit_with_too_few_nonzero_samples_is_inconclusive() -> None:
    fit = scaling.heuristic_loglog_fit(
        [
            {"n": 2, "discrepancy": 0},
            {"n": 4, "discrepancy": 2},
            {"n": 8, "discrepancy": 0},
        ]
    )
    assert fit["status"] == "inconclusive"
    assert fit["slope"] is None
    assert [item["n"] for item in fit["excluded_zero_discrepancy_samples"]] == [
        2,
        8,
    ]


def test_input_loader_enforces_count_cap_and_binary_encoding(tmp_path: Path) -> None:
    valid = tmp_path / "valid.u8"
    valid.write_bytes(bytes((1, 0, 1, 0)))
    resolved, bits = scaling.load_u8_bits(
        valid, max_input_bits=4, expected_count=4
    )
    assert resolved == valid.resolve()
    assert bits == bytes((1, 0, 1, 0))

    invalid = tmp_path / "invalid.u8"
    invalid.write_bytes(bytes((0, 1, 2, 0)))
    with pytest.raises(ValueError, match="index 2 is 2"):
        scaling.load_u8_bits(invalid, max_input_bits=4)

    oversized = tmp_path / "oversized.u8"
    oversized.write_bytes(bytes((0,)) * 5)
    with pytest.raises(ValueError, match="exceeds max_input_bits=4"):
        scaling.load_u8_bits(oversized, max_input_bits=4)
    with pytest.raises(ValueError, match="expected exactly 3"):
        scaling.load_u8_bits(valid, max_input_bits=4, expected_count=3)
    with pytest.raises(ValueError, match="hard cap"):
        scaling.load_u8_bits(
            valid, max_input_bits=scaling.HARD_MAX_INPUT_BITS + 1
        )


def test_trusted_10000_vector_matches_checkpoints_and_independent_oracles() -> None:
    vector = (
        REPOSITORY_ROOT
        / "tests"
        / "reference_vectors"
        / "center_c00000000_c00009999.u8"
    ).read_bytes()
    payload = scaling.build_scientific_payload(
        vector,
        checkpoints=(10, 100, 1_000, 10_000),
        fit_checkpoints=(10, 100, 1_000, 10_000),
        dyadic_widths=(64, 256, 1_024, 4_096),
        block_widths=(1, 2, 4, 8),
        lags=(1, 2, 8, 64),
    )
    assert payload["input"] == {
        "encoding": "one_byte_per_bit_c_0_first",
        "bit_count": 10_000,
        "byte_count": 10_000,
        "sha256": "61de1c97dc3f80cb24d3a02207920bd442d6f530304497eee70189a039a47860",
    }
    assert {
        n: record["discrepancy"] for n, record in _records_by_n(payload).items()
    } == {10: 4, 100: 4, 1_000: -38, 10_000: 64}

    running = 0
    best = (0, 0, 0)
    for n, bit in enumerate(vector, start=1):
        running += 1 if bit else -1
        if abs(running) > best[0]:
            best = (abs(running), n, running)
    maximum = payload["subresults"]["maximum_absolute_prefix_discrepancy"]
    assert (
        maximum["absolute_discrepancy"],
        maximum["n"],
        maximum["discrepancy"],
    ) == best

    expected_width_two = Counter(
        (vector[index] << 1) | vector[index + 1]
        for index in range(len(vector) - 1)
    )
    width_two = next(
        record
        for record in payload["subresults"]["block_frequency_ranges"]["records"]
        if record["width"] == 2
    )
    assert width_two["minimum_count"] == min(expected_width_two.values())
    assert width_two["maximum_count"] == max(expected_width_two.values())


def test_payload_hash_is_path_and_runtime_independent(tmp_path: Path) -> None:
    bits = bytes((1, 0, 1, 1, 0, 0, 1, 0))
    kwargs = {
        "checkpoints": (2, 4, 8),
        "fit_checkpoints": (2, 4, 8),
        "dyadic_widths": (2, 4, 8),
        "block_widths": (1, 2),
        "lags": (1, 2),
    }
    first = scaling.build_scientific_payload(bits, **kwargs)
    second = scaling.build_scientific_payload(bits, **kwargs)
    assert first == second
    digest = scaling.canonical_payload_sha256(first)
    first_envelope = scaling.build_run_envelope(
        first, input_path=tmp_path / "first.u8", runtime_seconds=1.0
    )
    second_envelope = scaling.build_run_envelope(
        second, input_path=tmp_path / "second.u8", runtime_seconds=9.0
    )
    assert first_envelope["scientific_payload_sha256"] == digest
    assert second_envelope["scientific_payload_sha256"] == digest
    assert "timestamp" not in repr(first_envelope).lower()


def test_resource_caps_reject_unbounded_parameter_sets() -> None:
    bits = bytes((0, 1)) * 16
    base = {
        "checkpoints": (32,),
        "fit_checkpoints": (16, 32),
        "dyadic_widths": (2, 4),
        "block_widths": (1, 2),
        "lags": (1, 2),
    }
    with pytest.raises(ValueError, match="at most 16"):
        scaling.build_scientific_payload(
            bits,
            **{**base, "lags": tuple(range(17))},
        )
    with pytest.raises(ValueError, match="hard cap 16"):
        scaling.build_scientific_payload(
            bits,
            **base,
            max_block_width=17,
        )
    with pytest.raises(ValueError, match="dense block width"):
        scaling.build_scientific_payload(
            bits,
            **{**base, "block_widths": (9,)},
            max_table_entries=256,
        )
