#!/usr/bin/env python3
"""Emit a deterministic JSON summary of finite-prefix Problem 2 measurements.

The script writes only to standard output.  It does not create a result file;
the experiment orchestrator may capture stdout atomically when appropriate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "python"))

from rule30lab.statistics import (  # noqa: E402
    approximate_entropy,
    balance_checkpoints,
    berlekamp_massey_binary,
    block_frequencies,
    dyadic_discrepancy_summary,
    max_absolute_prefix_discrepancy,
    power_spectral_summary,
    run_statistics,
    spin_autocorrelation,
)


DEFAULT_INPUT = (
    REPOSITORY_ROOT
    / "tests"
    / "reference_vectors"
    / "center_c00000000_c00009999.u8"
)


def _integer_csv(text: str) -> list[int]:
    try:
        values = [int(value.strip()) for value in text.split(",") if value.strip()]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected comma-separated integers") from exc
    if not values:
        raise argparse.ArgumentTypeError("at least one integer is required")
    return values


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Print exact and descriptive finite-prefix Rule 30 balance "
            "measurements as JSON; no result file is written."
        )
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument(
        "--checkpoints", type=_integer_csv, default=_integer_csv("10,100,1000,10000")
    )
    parser.add_argument(
        "--block-widths", type=_integer_csv, default=_integer_csv("1,2,3,4,5,6,7,8")
    )
    parser.add_argument(
        "--lags", type=_integer_csv, default=_integer_csv("1,2,3,4,5,8,16,32,64,128")
    )
    parser.add_argument(
        "--linear-prefixes", type=_integer_csv, default=_integer_csv("1000,2000,5000")
    )
    parser.add_argument(
        "--apen-patterns", type=_integer_csv, default=_integer_csv("1,2,3,4,5,6")
    )
    parser.add_argument(
        "--dyadic-widths",
        type=_integer_csv,
        help="comma-separated powers of two; default is every full dyadic width",
    )
    parser.add_argument("--max-table-entries", type=int, default=1_048_576)
    parser.add_argument("--max-block-width", type=int, default=64)
    parser.add_argument(
        "--spectral",
        action="store_true",
        help="include the optional NumPy centered-spin periodogram summary",
    )
    parser.add_argument("--spectral-top-k", type=int, default=8)
    return parser


def _block_reports(
    bits: bytes,
    widths: list[int],
    *,
    max_table_entries: int,
    max_width: int,
) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for width in sorted(set(widths)):
        report = block_frequencies(
            bits,
            width,
            include_zero_counts=True,
            max_table_entries=max_table_entries,
            max_width=max_width,
        )
        counts = list(report["counts"].values())
        report["minimum_count"] = min(counts)
        report["maximum_count"] = max(counts)
        reports.append(report)
    return reports


def build_summary(args: argparse.Namespace) -> dict[str, Any]:
    input_path = args.input.resolve()
    bits = input_path.read_bytes()
    # Every analysis function validates bytes as binary.  Validate the entire
    # input immediately as well, including when a selected report uses a prefix.
    balance_checkpoints(bits, [0])

    for prefix in args.linear_prefixes:
        if prefix < 0 or prefix > len(bits):
            raise ValueError(
                f"linear prefix {prefix} must be between 0 and {len(bits)}"
            )
    for lag in args.lags:
        if lag < 0 or lag >= len(bits):
            raise ValueError(f"lag {lag} must be between 0 and {len(bits) - 1}")

    result_summary: dict[str, Any] = {
        "balance_checkpoints": balance_checkpoints(bits, args.checkpoints),
        "maximum_absolute_prefix_discrepancy": max_absolute_prefix_discrepancy(bits),
        "dyadic_interval_discrepancy": dyadic_discrepancy_summary(
            bits,
            widths=args.dyadic_widths,
        ),
        "block_frequencies": _block_reports(
            bits,
            args.block_widths,
            max_table_entries=args.max_table_entries,
            max_width=args.max_block_width,
        ),
        "spin_autocorrelation": [
            spin_autocorrelation(bits, lag) for lag in sorted(set(args.lags))
        ],
        "runs": run_statistics(bits),
        "approximate_entropy": [
            approximate_entropy(
                bits,
                pattern_length,
                max_table_entries=args.max_table_entries,
                max_width=args.max_block_width,
            )
            for pattern_length in sorted(set(args.apen_patterns))
        ],
        "gf2_linear_complexity": [
            {
                "prefix_length": prefix,
                "linear_complexity": berlekamp_massey_binary(bits[:prefix]),
            }
            for prefix in sorted(set(args.linear_prefixes))
        ],
    }
    if args.spectral:
        result_summary["power_spectral_summary"] = power_spectral_summary(
            bits, top_k=args.spectral_top_k
        )

    return {
        "schema_version": 1,
        "experiment_id": "problem2-finite-prefix-summary-v1",
        "question": "problem2",
        "hypothesis": (
            "Measure discrepancy and selected descriptive statistics on one "
            "explicit finite center-sequence prefix."
        ),
        "backend": "python",
        "parameters": {
            "checkpoints": sorted(set(args.checkpoints)),
            "block_widths": sorted(set(args.block_widths)),
            "lags": sorted(set(args.lags)),
            "linear_prefixes": sorted(set(args.linear_prefixes)),
            "approximate_entropy_pattern_lengths": sorted(set(args.apen_patterns)),
            "dyadic_widths": (
                None if args.dyadic_widths is None else sorted(set(args.dyadic_widths))
            ),
            "max_table_entries": args.max_table_entries,
            "max_block_width": args.max_block_width,
            "spectral": args.spectral,
            "spectral_top_k": args.spectral_top_k,
        },
        "input": {
            "path": str(input_path),
            "encoding": "one_byte_per_bit_c_0_first",
            "count": len(bits),
            "sha256_u8": hashlib.sha256(bits).hexdigest(),
        },
        "result_summary": result_summary,
        "interpretation": (
            "All integer counts are exact for the identified finite input. "
            "Floating-point normalizations are descriptive only."
        ),
        "status": "empirical",
        "proof_scope": "exact arithmetic on the identified finite prefix only",
        "limitations": [
            "no finite measurement proves limiting balance",
            "no statistical measurement establishes randomness or normality",
            "approximate entropy and spectral summaries are descriptive",
            "this experiment makes no claim about an infinite Rule 30 sequence",
        ],
    }


def main() -> int:
    args = _parser().parse_args()
    summary = build_summary(args)
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
