#!/usr/bin/env python3
"""Bounded, deterministic analysis of an explicit Rule 30 u8 prefix.

The scientific payload is deterministic for fixed input bytes and parameters.
The command-line envelope also reports measured wall time, which is deliberately
excluded from the canonical scientific-payload hash.  No timestamp is emitted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import operator
import sys
import time
from pathlib import Path
from typing import Any, Iterable, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "python"))

from rule30lab.statistics import (  # noqa: E402
    balance_checkpoints,
    block_frequencies,
    dyadic_discrepancy_summary,
    max_absolute_prefix_discrepancy,
    run_statistics,
    spin_autocorrelation,
)


HARD_MAX_INPUT_BITS = 1_000_000
HARD_MAX_SELECTED_VALUES = 16
HARD_MAX_BLOCK_WIDTH = 16
HARD_MAX_TABLE_ENTRIES = 65_536

DEFAULT_CHECKPOINTS = (10, 100, 1_000, 10_000, 100_000, 1_000_000)
DEFAULT_FIT_CHECKPOINTS = DEFAULT_CHECKPOINTS
DEFAULT_DYADIC_WIDTHS = (64, 256, 1_024, 4_096, 16_384, 65_536, 262_144)
DEFAULT_BLOCK_WIDTHS = (1, 2, 3, 4, 5, 6, 7, 8, 10, 12)
DEFAULT_LAGS = (1, 2, 3, 4, 5, 8, 16, 32, 64, 128)


def _integer(value: int, *, name: str, minimum: int) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer, not bool")
    try:
        result = operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if result < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return result


def _selection(
    values: Iterable[int],
    *,
    name: str,
    minimum: int,
    maximum: int,
) -> tuple[int, ...]:
    selected = tuple(
        sorted({_integer(value, name=name, minimum=minimum) for value in values})
    )
    if not selected:
        raise ValueError(f"at least one {name} is required")
    if len(selected) > HARD_MAX_SELECTED_VALUES:
        raise ValueError(
            f"at most {HARD_MAX_SELECTED_VALUES} distinct {name} values are allowed"
        )
    if selected[-1] > maximum:
        raise ValueError(
            f"{name} {selected[-1]} exceeds the allowed maximum {maximum}"
        )
    return selected


def _integer_csv(text: str) -> tuple[int, ...]:
    try:
        values = tuple(int(item.strip()) for item in text.split(",") if item.strip())
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected comma-separated integers") from exc
    if not values:
        raise argparse.ArgumentTypeError("at least one integer is required")
    return values


def load_u8_bits(
    input_path: Path,
    *,
    max_input_bits: int = HARD_MAX_INPUT_BITS,
    expected_count: int | None = None,
) -> tuple[Path, bytes]:
    """Load and validate an explicit one-byte-per-bit file under a hard cap."""
    limit = _integer(max_input_bits, name="max_input_bits", minimum=1)
    if limit > HARD_MAX_INPUT_BITS:
        raise ValueError(
            f"max_input_bits cannot exceed the hard cap {HARD_MAX_INPUT_BITS}"
        )
    if expected_count is not None:
        expected = _integer(expected_count, name="expected_count", minimum=1)
        if expected > limit:
            raise ValueError("expected_count cannot exceed max_input_bits")
    else:
        expected = None

    resolved = input_path.expanduser().resolve(strict=True)
    if not resolved.is_file():
        raise ValueError(f"input is not a regular file: {resolved}")

    with resolved.open("rb") as handle:
        data = handle.read(limit + 1)
    if len(data) > limit:
        raise ValueError(
            f"input exceeds max_input_bits={limit}; one byte represents one bit"
        )
    if not data:
        raise ValueError("input must contain at least one encoded bit")
    if expected is not None and len(data) != expected:
        raise ValueError(
            f"input contains {len(data)} bits; expected exactly {expected}"
        )

    invalid = next(
        ((index, value) for index, value in enumerate(data) if value not in (0, 1)),
        None,
    )
    if invalid is not None:
        index, value = invalid
        raise ValueError(
            f"input byte at index {index} is {value}; encoding permits only 0 and 1"
        )
    return resolved, data


def heuristic_loglog_fit(
    checkpoint_records: Sequence[dict[str, int | float | None]],
) -> dict[str, Any]:
    """Fit log(|D(N)|) = intercept + slope*log(N) at configured samples.

    Zero discrepancies are reported and omitted without adding a pseudocount.
    The fit is descriptive extrapolation only and supplies no asymptotic bound.
    """
    included: list[dict[str, int]] = []
    excluded_zero: list[dict[str, int]] = []
    for record in checkpoint_records:
        count = int(record["n"])
        signed = int(record["discrepancy"])
        if count <= 0:
            raise ValueError("fit checkpoints must be positive")
        sample = {
            "n": count,
            "discrepancy": signed,
            "absolute_discrepancy": abs(signed),
        }
        if signed == 0:
            excluded_zero.append(sample)
        else:
            included.append(sample)

    base: dict[str, Any] = {
        "result_kind": "heuristic_log_log_fit",
        "model": "log(abs(D(N))) = intercept + slope * log(N)",
        "logarithm": "natural",
        "sample_selection": (
            "all configured fit checkpoints, sorted and deduplicated; selection "
            "does not depend on the observed discrepancy magnitude"
        ),
        "zero_handling": (
            "D(N)=0 samples are excluded because log(0) is undefined; no "
            "pseudocount or offset is added"
        ),
        "included_samples": included,
        "excluded_zero_discrepancy_samples": excluded_zero,
        "limitations": [
            "the fitted exponent depends on the selected finite checkpoints",
            "ordinary least squares assumptions are not asserted",
            "the fit is not an asymptotic estimate or a discrepancy bound",
        ],
    }
    if len(included) < 2:
        return {
            **base,
            "status": "inconclusive",
            "reason": "fewer than two nonzero-discrepancy samples remain",
            "slope": None,
            "intercept": None,
            "coefficient": None,
            "r_squared": None,
        }

    x_values = [math.log(sample["n"]) for sample in included]
    y_values = [
        math.log(sample["absolute_discrepancy"]) for sample in included
    ]
    x_mean = math.fsum(x_values) / len(x_values)
    y_mean = math.fsum(y_values) / len(y_values)
    sum_xx = math.fsum((value - x_mean) ** 2 for value in x_values)
    if sum_xx == 0.0:
        return {
            **base,
            "status": "inconclusive",
            "reason": "fit samples do not contain two distinct checkpoint sizes",
            "slope": None,
            "intercept": None,
            "coefficient": None,
            "r_squared": None,
        }

    slope = math.fsum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x_values, y_values, strict=True)
    ) / sum_xx
    intercept = y_mean - slope * x_mean
    predictions = [intercept + slope * value for value in x_values]
    residual_sum_squares = math.fsum(
        (observed - predicted) ** 2
        for observed, predicted in zip(y_values, predictions, strict=True)
    )
    total_sum_squares = math.fsum((value - y_mean) ** 2 for value in y_values)
    r_squared = (
        None
        if total_sum_squares == 0.0
        else 1.0 - residual_sum_squares / total_sum_squares
    )
    return {
        **base,
        "status": "heuristic",
        "slope": slope,
        "intercept": intercept,
        "coefficient": math.exp(intercept),
        "r_squared": r_squared,
        "fitted_form": "abs(D(N)) approximately coefficient * N**slope",
    }


def _checkpoint_report(
    record: dict[str, int | float | None],
) -> dict[str, Any]:
    count = int(record["n"])
    signed = int(record["discrepancy"])
    return {
        "n": count,
        "ones": int(record["ones"]),
        "zeros": int(record["zeros"]),
        "discrepancy": signed,
        "normalizations": {
            "status": "empirical",
            "result_kind": "descriptive_finite_normalization",
            "discrepancy_over_sqrt_n": record["discrepancy_over_sqrt_n"],
            "discrepancy_over_n": record["discrepancy_over_n"],
            "discrepancy_over_n_exact": {
                "numerator": signed,
                "denominator": count,
            },
        },
    }


def _block_range(
    bits: bytes,
    width: int,
    *,
    max_table_entries: int,
    max_block_width: int,
) -> dict[str, Any]:
    report = block_frequencies(
        bits,
        width,
        include_zero_counts=True,
        max_table_entries=max_table_entries,
        max_width=max_block_width,
    )
    counts = tuple(report["counts"].values())
    minimum = min(counts)
    maximum = max(counts)
    return {
        "width": width,
        "window_count": report["window_count"],
        "possible_block_count": report["possible_block_count"],
        "observed_block_count": report["observed_block_count"],
        "minimum_count": minimum,
        "maximum_count": maximum,
        "count_range": maximum - minimum,
        "minimum_count_multiplicity": sum(value == minimum for value in counts),
        "maximum_count_multiplicity": sum(value == maximum for value in counts),
        "zero_count_blocks_included": True,
    }


def build_scientific_payload(
    bits: bytes,
    *,
    checkpoints: Iterable[int] = DEFAULT_CHECKPOINTS,
    fit_checkpoints: Iterable[int] = DEFAULT_FIT_CHECKPOINTS,
    dyadic_widths: Iterable[int] = DEFAULT_DYADIC_WIDTHS,
    block_widths: Iterable[int] = DEFAULT_BLOCK_WIDTHS,
    lags: Iterable[int] = DEFAULT_LAGS,
    max_table_entries: int = HARD_MAX_TABLE_ENTRIES,
    max_block_width: int = HARD_MAX_BLOCK_WIDTH,
) -> dict[str, Any]:
    """Build the deterministic, path-independent scientific result payload."""
    if not isinstance(bits, bytes):
        raise TypeError("bits must be bytes in one-byte-per-bit encoding")
    if not bits:
        raise ValueError("bits must not be empty")
    if len(bits) > HARD_MAX_INPUT_BITS:
        raise ValueError(f"input exceeds hard cap {HARD_MAX_INPUT_BITS}")
    invalid = next(
        ((index, value) for index, value in enumerate(bits) if value not in (0, 1)),
        None,
    )
    if invalid is not None:
        raise ValueError(
            f"bit at index {invalid[0]} must be 0 or 1, got {invalid[1]}"
        )

    count = len(bits)
    selected_checkpoints = _selection(
        checkpoints, name="checkpoint", minimum=1, maximum=count
    )
    selected_fit_checkpoints = _selection(
        fit_checkpoints, name="fit checkpoint", minimum=1, maximum=count
    )
    selected_dyadic_widths = _selection(
        dyadic_widths, name="dyadic width", minimum=1, maximum=count
    )
    for width in selected_dyadic_widths:
        if width & (width - 1):
            raise ValueError(f"dyadic width {width} is not a power of two")

    block_width_limit = _integer(
        max_block_width, name="max_block_width", minimum=1
    )
    if block_width_limit > HARD_MAX_BLOCK_WIDTH:
        raise ValueError(
            f"max_block_width cannot exceed hard cap {HARD_MAX_BLOCK_WIDTH}"
        )
    table_limit = _integer(
        max_table_entries, name="max_table_entries", minimum=1
    )
    if table_limit > HARD_MAX_TABLE_ENTRIES:
        raise ValueError(
            "max_table_entries cannot exceed hard cap "
            f"{HARD_MAX_TABLE_ENTRIES}"
        )
    selected_block_widths = _selection(
        block_widths,
        name="block width",
        minimum=1,
        maximum=min(count, block_width_limit),
    )
    for width in selected_block_widths:
        if 1 << width > table_limit:
            raise ValueError(
                f"dense block width {width} needs {1 << width} table entries, "
                f"exceeding max_table_entries={table_limit}"
            )

    selected_lags = _selection(
        lags, name="autocorrelation lag", minimum=0, maximum=count - 1
    )

    all_checkpoint_values = tuple(
        sorted(set(selected_checkpoints) | set(selected_fit_checkpoints))
    )
    all_checkpoint_records = balance_checkpoints(bits, all_checkpoint_values)
    checkpoint_by_n = {
        int(record["n"]): record for record in all_checkpoint_records
    }
    requested_records = [checkpoint_by_n[value] for value in selected_checkpoints]
    fit_records = [checkpoint_by_n[value] for value in selected_fit_checkpoints]

    dyadic_records = dyadic_discrepancy_summary(
        bits,
        widths=selected_dyadic_widths,
        include_partial=False,
    )
    for record in dyadic_records:
        covered = int(record["interval_count"]) * int(record["width"])
        record["covered_bit_count"] = covered
        record["omitted_suffix_bit_count"] = count - covered

    run_report = run_statistics(bits)
    run_count = int(run_report["run_count"])
    run_report["mean_run_length_exact"] = {
        "numerator": count,
        "denominator": run_count,
    }
    run_report["mean_run_length_status"] = "empirical"

    autocorrelations: list[dict[str, Any]] = []
    for lag in selected_lags:
        report = spin_autocorrelation(bits, lag)
        autocorrelations.append(
            {
                "lag": report["lag"],
                "numerator": report["numerator"],
                "denominator": report["denominator"],
                "value": report["value"],
                "normalization": report["normalization"],
                "value_status": "empirical",
                "value_result_kind": "descriptive_finite_normalization",
            }
        )

    return {
        "schema_version": 1,
        "experiment_id": "problem2-million-prefix-scaling-v1",
        "question": "problem2",
        "input": {
            "encoding": "one_byte_per_bit_c_0_first",
            "bit_count": count,
            "byte_count": count,
            "sha256": hashlib.sha256(bits).hexdigest(),
        },
        "parameters": {
            "checkpoints": list(selected_checkpoints),
            "fit_checkpoints": list(selected_fit_checkpoints),
            "dyadic_widths": list(selected_dyadic_widths),
            "dyadic_include_partial": False,
            "block_widths": list(selected_block_widths),
            "autocorrelation_lags": list(selected_lags),
            "max_input_bits": HARD_MAX_INPUT_BITS,
            "max_selected_values_per_parameter": HARD_MAX_SELECTED_VALUES,
            "max_block_width": block_width_limit,
            "max_table_entries": table_limit,
        },
        "subresults": {
            "checkpoint_discrepancy": {
                "status": "finite-exhaustive",
                "result_kind": "exact_finite_prefix_scan",
                "records": [_checkpoint_report(record) for record in requested_records],
            },
            "maximum_absolute_prefix_discrepancy": {
                "status": "finite-exhaustive",
                "result_kind": "exact_finite_prefix_scan",
                **max_absolute_prefix_discrepancy(bits),
            },
            "dyadic_interval_summaries": {
                "status": "finite-exhaustive",
                "result_kind": "exact_aligned_finite_interval_scan",
                "records": dyadic_records,
            },
            "block_frequency_ranges": {
                "status": "finite-exhaustive",
                "result_kind": "exact_overlapping_finite_window_scan",
                "records": [
                    _block_range(
                        bits,
                        width,
                        max_table_entries=table_limit,
                        max_block_width=block_width_limit,
                    )
                    for width in selected_block_widths
                ],
            },
            "spin_autocorrelation": {
                "status": "finite-exhaustive",
                "result_kind": "exact_finite_pair_scan_with_descriptive_ratio",
                "records": autocorrelations,
            },
            "runs": {
                "status": "finite-exhaustive",
                "result_kind": "exact_maximal_run_partition",
                "record": run_report,
            },
            "discrepancy_scaling_fit": heuristic_loglog_fit(fit_records),
        },
        "status": "empirical",
        "interpretation": (
            "Integer scans are exact for the identified finite payload; ratios "
            "are descriptive, and the log-log regression is heuristic."
        ),
        "proof_scope": "the identified finite prefix only",
        "limitations": [
            "a finite prefix does not establish any limiting frequency",
            "the fitted slope is neither a theorem nor a validated asymptotic law",
            "unselected lags, widths, and checkpoints were not analyzed",
        ],
    }


def canonical_payload_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_run_envelope(
    payload: dict[str, Any],
    *,
    input_path: Path,
    runtime_seconds: float,
) -> dict[str, Any]:
    if not math.isfinite(runtime_seconds) or runtime_seconds < 0.0:
        raise ValueError("runtime_seconds must be finite and nonnegative")
    return {
        "scientific_payload_sha256": canonical_payload_sha256(payload),
        "hash_scope": (
            "canonical compact sorted-key JSON of scientific_payload; input path "
            "and runtime are excluded"
        ),
        "input_path": str(input_path),
        "runtime": {
            "status": "empirical",
            "result_kind": "descriptive_wall_clock_measurement",
            "wall_seconds": runtime_seconds,
            "clock": "time.perf_counter",
            "scope": (
                "input resolution/read, validation, analysis, and canonical payload "
                "hash; excludes indented JSON serialization"
            ),
        },
        "scientific_payload": payload,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="explicit file containing exactly one byte (0 or 1) per center bit",
    )
    parser.add_argument("--expected-count", type=int, default=1_000_000)
    parser.add_argument("--max-input-bits", type=int, default=HARD_MAX_INPUT_BITS)
    parser.add_argument(
        "--checkpoints", type=_integer_csv, default=DEFAULT_CHECKPOINTS
    )
    parser.add_argument(
        "--fit-checkpoints", type=_integer_csv, default=DEFAULT_FIT_CHECKPOINTS
    )
    parser.add_argument(
        "--dyadic-widths", type=_integer_csv, default=DEFAULT_DYADIC_WIDTHS
    )
    parser.add_argument(
        "--block-widths", type=_integer_csv, default=DEFAULT_BLOCK_WIDTHS
    )
    parser.add_argument("--lags", type=_integer_csv, default=DEFAULT_LAGS)
    parser.add_argument(
        "--max-table-entries", type=int, default=HARD_MAX_TABLE_ENTRIES
    )
    parser.add_argument(
        "--max-block-width", type=int, default=HARD_MAX_BLOCK_WIDTH
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    started = time.perf_counter()
    try:
        input_path, bits = load_u8_bits(
            args.input,
            max_input_bits=args.max_input_bits,
            expected_count=args.expected_count,
        )
        payload = build_scientific_payload(
            bits,
            checkpoints=args.checkpoints,
            fit_checkpoints=args.fit_checkpoints,
            dyadic_widths=args.dyadic_widths,
            block_widths=args.block_widths,
            lags=args.lags,
            max_table_entries=args.max_table_entries,
            max_block_width=args.max_block_width,
        )
        payload_hash = canonical_payload_sha256(payload)
    except (OSError, TypeError, ValueError, MemoryError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    elapsed = time.perf_counter() - started
    envelope = build_run_envelope(
        payload,
        input_path=input_path,
        runtime_seconds=elapsed,
    )
    if envelope["scientific_payload_sha256"] != payload_hash:
        raise AssertionError("canonical payload hash changed while building envelope")
    print(json.dumps(envelope, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
