#!/usr/bin/env python3
"""Directly reproduce two historical Rule 30 result payloads.

This script replaces the inline-command placeholders retained in the original
experiment records.  It emits deterministic scientific JSON to stdout and
does not write a result record or make an infinite-sequence claim.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PYTHON_SOURCE = REPOSITORY_ROOT / "src" / "python"
if str(PYTHON_SOURCE) not in sys.path:
    sys.path.insert(0, str(PYTHON_SOURCE))

from rule30_research_reference import center_column  # noqa: E402
from rule30lab.automaticity import (  # noqa: E402
    two_kernel_distinct_prefixes,
)


MILLION_COUNT = 1_000_000
MILLION_SHA256 = (
    "6fc1e4e2abfb382255b94955467f259be88c1044d09ec361c5039970985a1669"
)
MILLION_ONES = 500_768
MILLION_DISCREPANCY = 1_536
LEVEL_RECORDS_SHA256 = (
    "31041c1a58602ddd2d82b781a4af0e89b69261d4fdf7b1507b93b9085e5dbb72"
)
MAX_INPUT_BYTES = 16 * 1024 * 1024


def python_reference_summary(count: int) -> dict[str, Any]:
    """Generate ``c_0`` through ``c_(count-1)`` with the immutable source."""
    if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
        raise ValueError("count must be a positive integer")
    bits = bytes(center_column(count - 1))
    ones = sum(bits)
    return {
        "algorithm": "rule30_research_reference.center_column",
        "count": count,
        "prefix_convention": "c_0_through_c_count_minus_1",
        "ones": ones,
        "zeros": count - ones,
        "discrepancy": 2 * ones - count,
        "center_u8_sha256": hashlib.sha256(bits).hexdigest(),
        "status": "empirical",
        "interpretation": (
            "Exact output of the immutable supplied implementation for this "
            "finite prefix only; it does not establish limiting balance."
        ),
    }


def _validated_input(path: Path) -> bytes:
    path = Path(path)
    size = path.stat().st_size
    if size > MAX_INPUT_BYTES:
        raise ValueError(
            f"input has {size} bytes, exceeding the {MAX_INPUT_BYTES}-byte cap"
        )
    bits = path.read_bytes()
    invalid = next(
        ((index, value) for index, value in enumerate(bits) if value not in (0, 1)),
        None,
    )
    if invalid is not None:
        index, value = invalid
        raise ValueError(f"input byte {index} is {value}, expected numeric 0 or 1")
    return bits


def two_kernel_summary(
    bits: bytes, *, first_level: int, last_level: int, prefix_length: int
) -> dict[str, Any]:
    """Classify equal-length finite 2-kernel prefixes at explicit levels."""
    if first_level < 0 or last_level < first_level:
        raise ValueError("levels must satisfy 0 <= first_level <= last_level")
    if prefix_length <= 0:
        raise ValueError("prefix_length must be positive")
    required = prefix_length * (1 << last_level)
    if len(bits) < required:
        raise ValueError(
            f"input has {len(bits)} bits; requested levels require {required}"
        )

    records: list[dict[str, Any]] = []
    for level in range(first_level, last_level + 1):
        modulus = 1 << level
        distinct = two_kernel_distinct_prefixes(bits, level, prefix_length)
        records.append(
            {
                "all_prefixes_distinct": distinct == modulus,
                "distinct_prefix_count": distinct,
                "level": level,
                "modulus": modulus,
                "prefix_length": prefix_length,
                "required_input_length": modulus * prefix_length,
            }
        )

    canonical = json.dumps(
        records, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    return {
        "center_count_available": len(bits),
        "center_u8_sha256": hashlib.sha256(bits).hexdigest(),
        "first_level": first_level,
        "last_level": last_level,
        "prefix_length": prefix_length,
        "levels": records,
        "all_levels_fully_distinct": all(
            record["all_prefixes_distinct"] for record in records
        ),
        "canonical_level_records_sha256": hashlib.sha256(canonical).hexdigest(),
        "status": "finite-exhaustive",
        "proof_scope": (
            "Equality classification only for the explicitly listed finite "
            "prefixes and residue classes."
        ),
        "interpretation": (
            "Distinct finite 2-kernel prefixes do not establish "
            "nonautomaticity or a computational lower bound."
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "python-million",
        help="reproduce the supplied-Python million-bit counts and hash",
    )
    kernel = commands.add_parser(
        "two-kernel",
        help="reproduce the level-1-through-13 finite 2-kernel diagnostic",
    )
    kernel.add_argument("--input", type=Path, required=True)
    kernel.add_argument("--first-level", type=int, default=1)
    kernel.add_argument("--last-level", type=int, default=13)
    kernel.add_argument("--prefix-length", type=int, default=64)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "python-million":
        payload = python_reference_summary(MILLION_COUNT)
        expected = {
            "center_u8_sha256": MILLION_SHA256,
            "ones": MILLION_ONES,
            "discrepancy": MILLION_DISCREPANCY,
        }
        mismatches = {
            key: {"expected": value, "actual": payload[key]}
            for key, value in expected.items()
            if payload[key] != value
        }
        if mismatches:
            raise RuntimeError(f"million-bit reproduction mismatch: {mismatches}")
    else:
        bits = _validated_input(args.input)
        payload = two_kernel_summary(
            bits,
            first_level=args.first_level,
            last_level=args.last_level,
            prefix_length=args.prefix_length,
        )
        if (
            args.first_level == 1
            and args.last_level == 13
            and args.prefix_length == 64
            and len(bits) == MILLION_COUNT
        ):
            expected = {
                "center_u8_sha256": MILLION_SHA256,
                "canonical_level_records_sha256": LEVEL_RECORDS_SHA256,
            }
            mismatches = {
                key: {"expected": value, "actual": payload[key]}
                for key, value in expected.items()
                if payload[key] != value
            }
            if mismatches:
                raise RuntimeError(f"2-kernel reproduction mismatch: {mismatches}")

    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
