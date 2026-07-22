"""Strict finite-prefix diagnostics for automaticity and exact predictors.

These routines describe bounded data only.  Distinct finite 2-kernel prefixes
do not establish nonautomaticity, and failed held-out predictors do not imply a
lower bound or the nonexistence of another exact representation.
"""

from __future__ import annotations

import hashlib
import operator
from collections.abc import Callable, Iterable, Sequence
from typing import Any, overload

from .statistics import berlekamp_massey_connection_polynomial


def _integer(value: int, *, name: str, minimum: int | None = None) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer, not bool")
    try:
        result = operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if minimum is not None and result < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return result


def _validated_bits(bits: Iterable[int]) -> bytes:
    output = bytearray()
    for position, value in enumerate(bits):
        try:
            bit = operator.index(value)
        except TypeError as exc:
            raise ValueError(f"bit at index {position} is not an integer") from exc
        if bit not in (0, 1):
            raise ValueError(f"bit at index {position} must be 0 or 1, got {value!r}")
        output.append(bit)
    return bytes(output)


def two_kernel_prefixes(
    bits: Iterable[int], level: int, prefix_length: int
) -> tuple[bytes, ...]:
    """Return all exact prefixes of ``c[2**level*n + r]``.

    The input must contain at least ``2**level * prefix_length`` bits, enough
    to give every residue class the same requested prefix length.  Insufficient
    data is rejected rather than comparing shorter, unequal subsequences.
    """
    data = _validated_bits(bits)
    checked_level = _integer(level, name="level", minimum=0)
    checked_prefix = _integer(
        prefix_length, name="prefix_length", minimum=1
    )

    # Right-shifting the finite input length is safe even for an enormous level
    # and avoids constructing an enormous ``1 << level`` merely to reject it.
    if checked_prefix > (len(data) >> checked_level):
        raise ValueError(
            "insufficient data: every residue class requires prefix_length "
            "elements, so len(bits) must be at least prefix_length * 2**level"
        )

    modulus = 1 << checked_level
    required_length = checked_prefix * modulus
    return tuple(
        bytes(data[residue:required_length:modulus])
        for residue in range(modulus)
    )


def two_kernel_distinct_prefixes(
    bits: Iterable[int], level: int, prefix_length: int
) -> int:
    """Count distinct, equally long finite 2-kernel prefixes."""
    return len(set(two_kernel_prefixes(bits, level, prefix_length)))


def two_kernel_prefix_diagnostic(
    bits: Iterable[int],
    level: int,
    prefix_length: int,
    *,
    include_prefixes: bool = False,
) -> dict[str, Any]:
    """Return a JSON-compatible finite 2-kernel equivalence diagnostic."""
    prefixes = two_kernel_prefixes(bits, level, prefix_length)
    classes: dict[bytes, list[int]] = {}
    for residue, prefix in enumerate(prefixes):
        classes.setdefault(prefix, []).append(residue)

    class_records: list[dict[str, Any]] = []
    for prefix, residues in classes.items():
        record: dict[str, Any] = {
            "representative_residue": residues[0],
            "residues": residues,
            "prefix_sha256": hashlib.sha256(prefix).hexdigest(),
        }
        if include_prefixes:
            record["prefix"] = prefix.decode("latin1").translate(
                {0: "0", 1: "1"}
            )
        class_records.append(record)

    checked_level = _integer(level, name="level", minimum=0)
    checked_prefix = _integer(
        prefix_length, name="prefix_length", minimum=1
    )
    modulus = 1 << checked_level
    return {
        "level": checked_level,
        "modulus": modulus,
        "prefix_length": checked_prefix,
        "required_input_length": modulus * checked_prefix,
        "distinct_prefix_count": len(classes),
        "all_prefixes_distinct": len(classes) == modulus,
        "classes": class_records,
        "status": "finite_prefix_diagnostic",
        "interpretation": (
            "Exact equality classes for this level and prefix length only; "
            "distinctness does not establish nonautomaticity."
        ),
    }


def _checked_coefficients(coefficients: Iterable[int]) -> tuple[int, ...]:
    return tuple(_validated_bits(coefficients))


def _recurrence_prediction(
    data: Sequence[int], index: int, coefficients: Sequence[int]
) -> int:
    prediction = 0
    for offset, coefficient in enumerate(coefficients, start=1):
        prediction ^= coefficient & data[index - offset]
    return prediction


def _validation_segment(
    data: Sequence[int],
    coefficients: Sequence[int],
    start: int,
    stop: int,
    max_reported_errors: int,
) -> dict[str, Any]:
    error_count = 0
    first_error: int | None = None
    reported: list[int] = []
    for index in range(start, stop):
        prediction = _recurrence_prediction(data, index, coefficients)
        if prediction != data[index]:
            error_count += 1
            if first_error is None:
                first_error = index
            if len(reported) < max_reported_errors:
                reported.append(index)
    return {
        "start": start,
        "stop": stop,
        "evaluated": stop - start,
        "error_count": error_count,
        "first_error_index": first_error,
        "reported_error_indices": reported,
        "reported_errors_truncated": error_count > len(reported),
        "exact_on_segment": error_count == 0,
    }


def validate_binary_recurrence(
    bits: Iterable[int],
    coefficients: Iterable[int],
    *,
    train_length: int,
    max_reported_errors: int = 32,
) -> dict[str, Any]:
    """Validate one fixed GF(2) recurrence on training and held-out segments.

    Coefficients are ``(a_1, ..., a_L)`` with prediction
    ``s[n] = XOR(a_j & s[n-j])``.  An empty coefficient list is the order-zero
    predictor that emits zero.  At least one held-out bit is required.
    """
    data = _validated_bits(bits)
    recurrence = _checked_coefficients(coefficients)
    checked_train = _integer(train_length, name="train_length", minimum=0)
    error_limit = _integer(
        max_reported_errors, name="max_reported_errors", minimum=0
    )
    order = len(recurrence)
    if checked_train < order:
        raise ValueError(
            f"train_length {checked_train} is smaller than recurrence order {order}"
        )
    if checked_train >= len(data):
        raise ValueError("train_length must leave at least one held-out bit")

    training = _validation_segment(
        data, recurrence, order, checked_train, error_limit
    )
    held_out = _validation_segment(
        data, recurrence, checked_train, len(data), error_limit
    )
    return {
        "sample_count": len(data),
        "train_length": checked_train,
        "order": order,
        "coefficients": list(recurrence),
        "coefficient_convention": "a_j multiplies s[n-j] over GF(2)",
        "training": training,
        "held_out": held_out,
        "status": "finite_exact_validation",
        "limitations": [
            "exact held-out agreement is limited to the supplied finite segment",
            "failure does not imply that no other exact recurrence exists",
            "agreement does not establish an infinite recurrence",
        ],
    }


def fit_berlekamp_massey_and_validate(
    bits: Iterable[int],
    *,
    train_length: int,
    max_reported_errors: int = 32,
) -> dict[str, Any]:
    """Fit GF(2) Berlekamp--Massey on training data, then validate held out."""
    data = _validated_bits(bits)
    checked_train = _integer(train_length, name="train_length", minimum=1)
    if checked_train >= len(data):
        raise ValueError("train_length must leave at least one held-out bit")
    polynomial = berlekamp_massey_connection_polynomial(data[:checked_train])
    result = validate_binary_recurrence(
        data,
        polynomial[1:],
        train_length=checked_train,
        max_reported_errors=max_reported_errors,
    )
    result["fit"] = {
        "method": "berlekamp_massey_gf2",
        "connection_polynomial": list(polynomial),
        "fit_input_start": 0,
        "fit_input_stop": checked_train,
    }
    return result


class _ReadOnlyHistory(Sequence[int]):
    """A live read-only view used to avoid copying history for every prediction."""

    def __init__(self, initial: bytes) -> None:
        self._data = bytearray(initial)

    def __len__(self) -> int:
        return len(self._data)

    @overload
    def __getitem__(self, index: int) -> int: ...

    @overload
    def __getitem__(self, index: slice) -> bytes: ...

    def __getitem__(self, index: int | slice) -> int | bytes:
        value = self._data[index]
        return bytes(value) if isinstance(index, slice) else value

    def _append_observation(self, bit: int) -> None:
        self._data.append(bit)


Predictor = Callable[[Sequence[int], int], int]
PredictorFitter = Callable[[bytes], Predictor]


def validate_fitted_predictor(
    bits: Iterable[int],
    *,
    train_length: int,
    fit_predictor: PredictorFitter,
    max_reported_errors: int = 32,
) -> dict[str, Any]:
    """Fit on a strict prefix and perform teacher-forced held-out validation.

    ``fit_predictor`` receives only an immutable copy of the training prefix and
    returns ``predictor(history, index)``.  At each held-out index the predictor
    sees the training data and earlier *observed* held-out bits, never the
    current or future held-out bits through this helper.  The helper cannot
    prevent a user callback from obtaining data through an external closure, so
    callers must still audit predictor construction for leakage.
    """
    data = _validated_bits(bits)
    checked_train = _integer(train_length, name="train_length", minimum=1)
    error_limit = _integer(
        max_reported_errors, name="max_reported_errors", minimum=0
    )
    if checked_train >= len(data):
        raise ValueError("train_length must leave at least one held-out bit")
    if not callable(fit_predictor):
        raise ValueError("fit_predictor must be callable")

    predictor = fit_predictor(bytes(data[:checked_train]))
    if not callable(predictor):
        raise ValueError("fit_predictor must return a callable predictor")

    history = _ReadOnlyHistory(data[:checked_train])
    predictions = bytearray()
    error_count = 0
    first_error: int | None = None
    reported: list[int] = []
    for index in range(checked_train, len(data)):
        raw_prediction = predictor(history, index)
        try:
            prediction = operator.index(raw_prediction)
        except TypeError as exc:
            raise ValueError(
                f"prediction at index {index} is not an integer"
            ) from exc
        if prediction not in (0, 1):
            raise ValueError(
                f"prediction at index {index} must be 0 or 1, got {raw_prediction!r}"
            )
        predictions.append(prediction)
        if prediction != data[index]:
            error_count += 1
            if first_error is None:
                first_error = index
            if len(reported) < error_limit:
                reported.append(index)
        history._append_observation(data[index])

    return {
        "sample_count": len(data),
        "train_length": checked_train,
        "held_out": {
            "start": checked_train,
            "stop": len(data),
            "evaluated": len(data) - checked_train,
            "error_count": error_count,
            "first_error_index": first_error,
            "reported_error_indices": reported,
            "reported_errors_truncated": error_count > len(reported),
            "exact_on_segment": error_count == 0,
            "prediction_sha256_u8": hashlib.sha256(predictions).hexdigest(),
        },
        "protocol": "strict_prefix_fit_teacher_forced_one_step_prediction",
        "status": "finite_exact_validation",
        "limitations": [
            "the callback must be audited for out-of-band held-out data leakage",
            "held-out history uses earlier observed bits rather than recursive predictions",
            "finite agreement does not establish an exact predictor for all indices",
            "failure does not imply a computational lower bound",
        ],
    }
