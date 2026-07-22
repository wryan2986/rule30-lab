from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import pytest

from rule30lab.automaticity import (
    fit_berlekamp_massey_and_validate,
    two_kernel_distinct_prefixes,
    two_kernel_prefix_diagnostic,
    two_kernel_prefixes,
    validate_binary_recurrence,
    validate_fitted_predictor,
)


VECTORS = Path(__file__).resolve().parents[1] / "reference_vectors"


def test_two_kernel_prefixes_use_equal_strict_lengths() -> None:
    bits = [0, 0, 1, 0, 1, 1, 0, 1]
    prefixes = two_kernel_prefixes(bits, level=2, prefix_length=2)
    assert prefixes == (
        b"\x00\x01",
        b"\x00\x01",
        b"\x01\x00",
        b"\x00\x01",
    )
    assert two_kernel_distinct_prefixes(bits, 2, 2) == 2
    assert two_kernel_prefixes([1, 0, 1], 0, 2) == (b"\x01\x00",)


def test_two_kernel_diagnostic_reports_exact_equivalence_classes() -> None:
    bits = [0, 0, 1, 0, 1, 1, 0, 1]
    report = two_kernel_prefix_diagnostic(
        bits, 2, 2, include_prefixes=True
    )
    assert report["distinct_prefix_count"] == 2
    assert report["all_prefixes_distinct"] is False
    assert report["required_input_length"] == 8
    assert [record["residues"] for record in report["classes"]] == [
        [0, 1, 3],
        [2],
    ]
    assert [record["prefix"] for record in report["classes"]] == ["01", "10"]
    assert report["status"] == "finite_prefix_diagnostic"
    assert "does not establish nonautomaticity" in report["interpretation"]


def test_two_kernel_rejects_insufficient_or_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="insufficient data"):
        two_kernel_prefixes([0] * 7, 2, 2)
    with pytest.raises(ValueError, match="insufficient data"):
        two_kernel_prefixes([0], 1_000_000, 1)
    with pytest.raises(ValueError, match="at least 0"):
        two_kernel_prefixes([0] * 8, -1, 2)
    with pytest.raises(ValueError, match="at least 1"):
        two_kernel_prefixes([0] * 8, 2, 0)
    with pytest.raises(ValueError, match="index 3"):
        two_kernel_prefixes([0, 1, 0, 2], 1, 2)


def test_frozen_prefix_has_reported_finite_two_kernel_distinctness() -> None:
    bits = (VECTORS / "center_c00000000_c00009999.u8").read_bytes()
    for level in range(1, 8):
        assert two_kernel_distinct_prefixes(bits, level, 64) == 1 << level


def _fibonacci_mod_two(count: int) -> bytearray:
    bits = bytearray((1, 0))
    while len(bits) < count:
        bits.append(bits[-1] ^ bits[-2])
    return bits[:count]


def test_fixed_binary_recurrence_validates_train_and_held_out() -> None:
    bits = _fibonacci_mod_two(18)
    report = validate_binary_recurrence(
        bits, [1, 1], train_length=10
    )
    assert report["order"] == 2
    assert report["training"]["evaluated"] == 8
    assert report["training"]["exact_on_segment"] is True
    assert report["held_out"]["evaluated"] == 8
    assert report["held_out"]["exact_on_segment"] is True

    broken = bits.copy()
    broken[-1] ^= 1
    failed = validate_binary_recurrence(
        broken, [1, 1], train_length=10
    )
    assert failed["held_out"]["error_count"] == 1
    assert failed["held_out"]["first_error_index"] == 17
    assert failed["held_out"]["reported_error_indices"] == [17]


def test_recurrence_validation_is_strict_about_split_and_coefficients() -> None:
    with pytest.raises(ValueError, match="smaller than recurrence order"):
        validate_binary_recurrence([0, 1, 0], [1, 1], train_length=1)
    with pytest.raises(ValueError, match="leave at least one"):
        validate_binary_recurrence([0, 1, 0], [1], train_length=3)
    with pytest.raises(ValueError, match="index 0"):
        validate_binary_recurrence([0, 1, 0], [2], train_length=1)


def test_berlekamp_massey_fit_isolated_to_training_prefix() -> None:
    bits = _fibonacci_mod_two(24)
    report = fit_berlekamp_massey_and_validate(bits, train_length=12)
    assert report["fit"]["connection_polynomial"] == [1, 1, 1]
    assert report["fit"]["fit_input_stop"] == 12
    assert report["held_out"]["exact_on_segment"] is True

    zeros = fit_berlekamp_massey_and_validate([0] * 8, train_length=4)
    assert zeros["order"] == 0
    assert zeros["fit"]["connection_polynomial"] == [1]
    assert zeros["held_out"]["exact_on_segment"] is True


def test_fitted_predictor_receives_only_training_then_observed_history() -> None:
    bits = bytes([0, 1] * 6)
    seen: dict[str, Any] = {"lengths": []}

    def fit(training: bytes):
        assert training == bits[:4]

        def predict(history, index: int) -> int:
            assert len(history) == index
            seen["lengths"].append(len(history))
            return 1 - history[-1]

        return predict

    report = validate_fitted_predictor(
        bits, train_length=4, fit_predictor=fit
    )
    assert seen["lengths"] == list(range(4, len(bits)))
    assert report["held_out"]["exact_on_segment"] is True
    assert report["held_out"]["prediction_sha256_u8"] == hashlib.sha256(
        bits[4:]
    ).hexdigest()
    assert report["protocol"] == "strict_prefix_fit_teacher_forced_one_step_prediction"
    assert any("leakage" in item for item in report["limitations"])


def test_fitted_predictor_reports_errors_and_rejects_nonbits() -> None:
    report = validate_fitted_predictor(
        [0, 1, 0, 1, 0],
        train_length=2,
        fit_predictor=lambda _training: lambda _history, _index: 0,
        max_reported_errors=1,
    )
    assert report["held_out"]["error_count"] == 1
    assert report["held_out"]["reported_error_indices"] == [3]
    assert report["held_out"]["reported_errors_truncated"] is False

    with pytest.raises(ValueError, match="must be 0 or 1"):
        validate_fitted_predictor(
            [0, 1, 0],
            train_length=1,
            fit_predictor=lambda _training: lambda _history, _index: 2,
        )
    with pytest.raises(ValueError, match="return a callable"):
        validate_fitted_predictor(
            [0, 1, 0],
            train_length=1,
            fit_predictor=lambda _training: 0,  # type: ignore[return-value]
        )
