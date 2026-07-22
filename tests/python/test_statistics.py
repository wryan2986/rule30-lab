from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path

import pytest

from rule30lab.statistics import (
    approximate_entropy,
    balance_checkpoints,
    berlekamp_massey_binary,
    berlekamp_massey_connection_polynomial,
    block_frequencies,
    discrepancy,
    dyadic_discrepancy_summary,
    dyadic_interval_discrepancies,
    max_absolute_prefix_discrepancy,
    power_spectral_summary,
    run_lengths,
    run_statistics,
    spin_autocorrelation,
)


VECTORS = Path(__file__).resolve().parents[1] / "reference_vectors"


def test_balance_checkpoints_have_exact_count_convention() -> None:
    records = balance_checkpoints([1, 0, 1, 1], [4, 0, 2, 1, 2])
    assert [record["n"] for record in records] == [0, 1, 2, 4]
    assert records[0] == {
        "n": 0,
        "ones": 0,
        "zeros": 0,
        "discrepancy": 0,
        "ones_fraction": None,
        "discrepancy_over_sqrt_n": None,
        "discrepancy_over_n": None,
    }
    assert records[2]["ones"] == 1
    assert records[2]["zeros"] == 1
    assert records[2]["discrepancy"] == 0
    assert records[3]["ones_fraction"] == 0.75
    assert records[3]["discrepancy"] == 2
    assert discrepancy([1, 0, 1, 1]) == 2


def test_balance_rejects_bad_bits_and_out_of_range_checkpoints() -> None:
    with pytest.raises(ValueError, match="index 1"):
        balance_checkpoints([0, 2], [1])
    with pytest.raises(ValueError, match="exceeds prefix length"):
        balance_checkpoints([0, 1], [3])
    with pytest.raises(ValueError, match="at least 0"):
        balance_checkpoints([0, 1], [-1])
    with pytest.raises(ValueError, match="not bool"):
        balance_checkpoints([0, 1], [True])


def test_frozen_10000_vector_reproduces_balance_checkpoints() -> None:
    bits = (VECTORS / "center_c00000000_c00009999.u8").read_bytes()
    manifest = json.loads((VECTORS / "manifest.json").read_text(encoding="utf-8"))
    expected = manifest["balance_checkpoints"]
    records = balance_checkpoints(bits, (10, 100, 1_000, 10_000))

    for record in records:
        checkpoint = expected[str(record["n"])]
        assert record["ones"] == checkpoint["ones"]
        assert record["zeros"] == checkpoint["zeros"]
        assert record["discrepancy"] == checkpoint["discrepancy"]
        assert record["ones_fraction"] == checkpoint["ones_fraction"]


def test_max_absolute_prefix_discrepancy_uses_first_tie() -> None:
    assert max_absolute_prefix_discrepancy([]) == {
        "n": 0,
        "discrepancy": 0,
        "absolute_discrepancy": 0,
    }
    assert max_absolute_prefix_discrepancy([0, 0, 1, 0, 1, 1]) == {
        "n": 2,
        "discrepancy": -2,
        "absolute_discrepancy": 2,
    }


def test_dyadic_interval_discrepancies_match_hand_oracle() -> None:
    bits = [1, 1, 0, 0, 1, 0, 1, 0]
    records = dyadic_interval_discrepancies(bits)
    by_width = {
        width: [
            record["discrepancy"]
            for record in records
            if record["width"] == width
        ]
        for width in (1, 2, 4, 8)
    }
    assert by_width == {
        1: [1, 1, -1, -1, 1, -1, 1, -1],
        2: [2, -2, 0, 0],
        4: [0, 0],
        8: [0],
    }
    assert all(record["partial"] is False for record in records)


def test_dyadic_partial_intervals_summary_and_resource_cap() -> None:
    bits = [1, 1, 0, 0, 1]
    assert [
        record["discrepancy"]
        for record in dyadic_interval_discrepancies(
            bits, widths=[4], include_partial=True
        )
    ] == [0, 1]

    summary = dyadic_discrepancy_summary(
        [1, 1, 0, 0, 1, 0, 1, 0], widths=[2]
    )[0]
    assert summary == {
        "width": 2,
        "interval_count": 4,
        "include_partial": False,
        "minimum_discrepancy": -2,
        "maximum_discrepancy": 2,
        "maximum_absolute_discrepancy": 2,
        "first_maximum_start": 0,
        "first_maximum_stop": 2,
        "first_maximum_discrepancy": 2,
        "sum_of_interval_discrepancies": 0,
    }

    with pytest.raises(ValueError, match="not a power of two"):
        dyadic_interval_discrepancies(bits, widths=[3])
    with pytest.raises(ValueError, match="exceeds prefix length"):
        dyadic_interval_discrepancies(bits, widths=[8])
    with pytest.raises(MemoryError, match="records"):
        dyadic_interval_discrepancies([0] * 8, max_intervals=10)


def _brute_block_counts(bits: tuple[int, ...], width: int) -> Counter[int]:
    counts: Counter[int] = Counter()
    for start in range(len(bits) - width + 1):
        value = 0
        for bit in bits[start : start + width]:
            value = (value << 1) | bit
        counts[value] += 1
    return counts


def test_block_frequencies_match_exhaustive_small_oracle() -> None:
    for length in range(1, 7):
        for bits in itertools.product((0, 1), repeat=length):
            for width in range(1, length + 1):
                result = block_frequencies(bits, width)
                assert result["counts"] == dict(
                    sorted(_brute_block_counts(bits, width).items())
                )
                assert sum(result["counts"].values()) == length - width + 1


def test_block_frequencies_dense_mode_and_memory_limits() -> None:
    sparse = block_frequencies([0, 0, 1, 0, 0], 2)
    assert sparse["counts"] == {0: 2, 1: 1, 2: 1}
    dense = block_frequencies(
        [0, 0, 1, 0, 0], 2, include_zero_counts=True
    )
    assert dense["counts"] == {0: 2, 1: 1, 2: 1, 3: 0}
    with pytest.raises(MemoryError, match="max_table_entries"):
        block_frequencies([0] * 10, 3, include_zero_counts=True, max_table_entries=7)
    with pytest.raises(MemoryError, match="max_width"):
        block_frequencies([0] * 10, 5, max_width=4)
    with pytest.raises(ValueError, match="exceeds prefix length"):
        block_frequencies([0, 1], 3)


def test_spin_autocorrelation_returns_exact_fraction_parts() -> None:
    assert spin_autocorrelation([1, 0, 1, 1], 1) == {
        "lag": 1,
        "numerator": -1,
        "denominator": 3,
        "value": -1 / 3,
        "normalization": "uncentered_mean_spin_product",
    }
    lag_zero = spin_autocorrelation([1, 0, 1, 1], 0)
    assert lag_zero["numerator"] == 4
    assert lag_zero["denominator"] == 4
    assert lag_zero["value"] == 1.0
    with pytest.raises(ValueError, match="smaller than prefix length"):
        spin_autocorrelation([], 0)
    with pytest.raises(ValueError, match="at least 0"):
        spin_autocorrelation([0, 1], -1)


def test_runs_have_explicit_empty_and_maximal_run_conventions() -> None:
    bits = [0, 0, 0, 1, 1, 0, 1, 1, 1]
    assert run_lengths(bits) == ((0, 3), (1, 2), (0, 1), (1, 3))
    summary = run_statistics(bits)
    assert summary["run_count"] == 4
    assert summary["zero_run_count"] == 2
    assert summary["one_run_count"] == 2
    assert summary["longest_zero_run"] == 3
    assert summary["longest_one_run"] == 3
    assert summary["mean_run_length"] == 9 / 4
    assert summary["length_histogram"] == {1: 1, 2: 1, 3: 2}
    assert run_lengths([]) == ()
    assert run_statistics([])["mean_run_length"] is None


def _symbolic_phi(bits: tuple[int, ...], width: int, base: float) -> float:
    blocks = Counter(bits[index : index + width] for index in range(len(bits) - width + 1))
    total = sum(blocks.values())
    return sum(
        (count / total) * math.log(count / total, base)
        for count in blocks.values()
    )


def test_approximate_entropy_matches_independent_block_oracle() -> None:
    bits = (0, 0, 1, 0, 1, 1, 0, 1)
    report = approximate_entropy(bits, 2)
    expected = _symbolic_phi(bits, 2, 2.0) - _symbolic_phi(bits, 3, 2.0)
    assert report["approximate_entropy"] == pytest.approx(expected)
    assert report["status"] == "descriptive_finite_prefix"
    assert "not a randomness test" in report["limitations"]
    assert approximate_entropy([1] * 8, 2)["approximate_entropy"] == 0.0
    with pytest.raises(ValueError, match=r"pattern_length \+ 1"):
        approximate_entropy([0, 1], 2)
    with pytest.raises(ValueError, match="base"):
        approximate_entropy([0, 1, 0], 1, base=1.0)


def _brute_linear_complexity(bits: tuple[int, ...]) -> int:
    for order in range(len(bits) + 1):
        for coefficients in itertools.product((0, 1), repeat=order):
            if all(
                bits[index]
                == sum(
                    coefficients[offset - 1] * bits[index - offset]
                    for offset in range(1, order + 1)
                )
                % 2
                for index in range(order, len(bits))
            ):
                return order
    raise AssertionError("an order equal to sequence length is always valid")


def test_berlekamp_massey_matches_exhaustive_small_oracle() -> None:
    assert berlekamp_massey_binary([]) == 0
    assert berlekamp_massey_connection_polynomial([]) == (1,)
    for length in range(8):
        for bits in itertools.product((0, 1), repeat=length):
            complexity = berlekamp_massey_binary(bits)
            polynomial = berlekamp_massey_connection_polynomial(bits)
            assert complexity == _brute_linear_complexity(bits)
            assert len(polynomial) == complexity + 1
            assert polynomial[0] == 1
            assert all(
                bits[index]
                == sum(
                    polynomial[offset] * bits[index - offset]
                    for offset in range(1, complexity + 1)
                )
                % 2
                for index in range(complexity, length)
            )


def test_frozen_vector_reproduces_reported_linear_complexity() -> None:
    bits = (VECTORS / "center_c00000000_c00009999.u8").read_bytes()
    assert berlekamp_massey_binary(bits[:1_000]) == 500
    assert berlekamp_massey_binary(bits[:2_000]) == 1_000
    assert berlekamp_massey_binary(bits[:5_000]) == 2_500


def test_optional_numpy_spectrum_finds_alternating_nyquist_peak() -> None:
    pytest.importorskip("numpy")
    report = power_spectral_summary([0, 1] * 4, top_k=2)
    assert report["spin_mean"] == 0.0
    assert report["spin_variance"] == 1.0
    assert report["one_sided_power_sum"] == pytest.approx(1.0)
    assert report["top_bins"][0]["bin"] == 4
    assert report["top_bins"][0]["cycles_per_sample"] == 0.5
    assert report["top_bins"][0]["power"] == pytest.approx(1.0)
