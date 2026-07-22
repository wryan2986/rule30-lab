#!/usr/bin/env python3
"""Audit finite quotients behind the Rule 30 2-adic diagonal map.

The exact infinite argument is in
``proofs/informal/problem1_two_adic_diagonal_map.md``.  This script checks all
residues at every explicitly bounded width with two independent evaluators.
It also checks the finite residues of the exact 2-adic countermodel

    A = -1/3,  B = 1/3,  T(A) = B,  T(B) = A,  Delta(A) = -1.

If any finite check fails, the proposed reformulation or an implementation is
wrong.  Passing every finite check is regression evidence for the proof, not
a proof over all widths and not a proof of Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any

from rule30lab.two_adic import (
    diagonal_map_mod,
    inverse_diagonal_map_mod,
    minus_one_third_mod,
    plus_one_third_mod,
    right_edge_step_mod,
)


DEFAULT_MAXIMUM_WIDTH = 12
DEFAULT_MAXIMUM_QUOTIENT_POINTS = 200_000
ABSOLUTE_MAXIMUM_WIDTH = 16


class TwoAdicLimitError(RuntimeError):
    """Raised before a configured finite-work limit is crossed."""


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def quotient_points(maximum_width: int) -> int:
    if maximum_width <= 0:
        raise ValueError("maximum width must be positive")
    return (1 << (maximum_width + 1)) - 2


def diagonal_map_cell_array(seed: int, width: int) -> int:
    """Independent per-bit evaluator of the finite diagonal map."""

    if width <= 0:
        raise ValueError("width must be positive")
    if seed < 0 or seed >= (1 << width):
        raise ValueError("seed does not fit the requested width")
    state = [(seed >> position) & 1 for position in range(width)]
    output = 0
    for time in range(width):
        output |= state[time] << time
        state = [
            state[position]
            ^ (
                (state[position - 1] if position >= 1 else 0)
                | (state[position - 2] if position >= 2 else 0)
            )
            for position in range(width)
        ]
    return output


def _table_bytes(values: list[int], width: int) -> bytes:
    bytes_per_value = (width + 7) // 8
    return b"".join(
        value.to_bytes(bytes_per_value, "little") for value in values
    )


def _analyze_width(width: int) -> tuple[dict[str, Any], bytes, bytes]:
    size = 1 << width
    packed_images: list[int] = []
    for seed in range(size):
        packed = diagonal_map_mod(seed, width)
        direct = diagonal_map_cell_array(seed, width)
        if packed != direct:
            raise AssertionError(
                f"diagonal evaluators disagree at width={width}, seed={seed}"
            )
        packed_images.append(packed)

    permutation = len(set(packed_images)) == size
    if not permutation:
        raise AssertionError(f"finite diagonal map is not bijective at width {width}")

    inverses = [inverse_diagonal_map_mod(trace, width) for trace in range(size)]
    inverse_verified = all(
        packed_images[inverses[trace]] == trace
        and inverses[packed_images[trace]] == trace
        for trace in range(size)
    )
    if not inverse_verified:
        raise AssertionError(f"finite diagonal inverse failed at width {width}")

    highest_bit = 1 << (width - 1)
    top_bit_unit_triangular = all(
        packed_images[lower] ^ packed_images[lower | highest_bit]
        == highest_bit
        for lower in range(highest_bit)
    )
    if not top_bit_unit_triangular:
        raise AssertionError(f"unit triangular property failed at width {width}")

    a = minus_one_third_mod(width)
    b = plus_one_third_mod(width)
    mask = size - 1
    rational_cycle_verified = (
        right_edge_step_mod(a, width) == b
        and right_edge_step_mod(b, width) == a
    )
    all_one_diagonal_verified = diagonal_map_mod(a, width) == mask
    single_one_diagonal_verified = diagonal_map_mod(b, width) == 1
    expected_a = sum(1 << position for position in range(0, width, 2))
    expected_b = 1 + sum(1 << position for position in range(1, width, 2))
    rational_digit_patterns_verified = a == expected_a and b == expected_b
    if not (
        rational_cycle_verified
        and all_one_diagonal_verified
        and single_one_diagonal_verified
        and rational_digit_patterns_verified
    ):
        raise AssertionError(f"rational 2-adic countermodel failed at width {width}")

    image_bytes = _table_bytes(packed_images, width)
    inverse_bytes = _table_bytes(inverses, width)
    summary = {
        "width": width,
        "quotient_size": size,
        "two_independent_evaluators_agree": True,
        "diagonal_map_is_permutation": permutation,
        "inverse_verified_both_directions": inverse_verified,
        "top_bit_unit_triangular": top_bit_unit_triangular,
        "minus_one_third_residue": a,
        "plus_one_third_residue": b,
        "rational_two_cycle_verified": rational_cycle_verified,
        "rational_digit_patterns_verified": rational_digit_patterns_verified,
        "minus_one_third_has_all_one_diagonal": all_one_diagonal_verified,
        "plus_one_third_has_single_one_diagonal": (
            single_one_diagonal_verified
        ),
        "map_table_sha256": hashlib.sha256(image_bytes).hexdigest(),
        "inverse_table_sha256": hashlib.sha256(inverse_bytes).hexdigest(),
    }
    return summary, image_bytes, inverse_bytes


def run_campaign(
    *,
    maximum_width: int,
    maximum_quotient_points: int = DEFAULT_MAXIMUM_QUOTIENT_POINTS,
    absolute_maximum_width: int = ABSOLUTE_MAXIMUM_WIDTH,
) -> dict[str, Any]:
    """Exhaust every residue at widths one through ``maximum_width``."""

    if any(
        not isinstance(value, int)
        or isinstance(value, bool)
        or value <= 0
        for value in (
            maximum_width,
            maximum_quotient_points,
            absolute_maximum_width,
        )
    ):
        raise ValueError("widths and work limits must be positive integers")
    if maximum_width > absolute_maximum_width:
        raise TwoAdicLimitError(
            f"width {maximum_width} exceeds configured maximum "
            f"{absolute_maximum_width}"
        )
    points = quotient_points(maximum_width)
    if points > maximum_quotient_points:
        raise TwoAdicLimitError(
            f"{points} quotient points exceed configured maximum "
            f"{maximum_quotient_points}"
        )

    certificate = hashlib.sha256()
    certificate.update(b"rule30-two-adic-diagonal-certificate-v1\0")
    certificate.update(maximum_width.to_bytes(2, "little"))
    summaries: list[dict[str, Any]] = []
    for width in range(1, maximum_width + 1):
        summary, image_bytes, inverse_bytes = _analyze_width(width)
        summaries.append(summary)
        certificate.update(width.to_bytes(2, "little"))
        certificate.update(image_bytes)
        certificate.update(inverse_bytes)

    return {
        "status": "finite-exhaustive",
        "parameters": {"maximum_width": maximum_width},
        "resource_caps": {
            "absolute_maximum_width": absolute_maximum_width,
            "maximum_quotient_points": maximum_quotient_points,
        },
        "coverage": {
            "widths": maximum_width,
            "quotient_points_exhausted": points,
            "independent_diagonal_evaluators": 2,
        },
        "width_summaries": summaries,
        "all_finite_diagonal_maps_are_permutations": all(
            summary["diagonal_map_is_permutation"] for summary in summaries
        ),
        "all_finite_inverses_verified": all(
            summary["inverse_verified_both_directions"] for summary in summaries
        ),
        "all_top_bit_triangular_checks_pass": all(
            summary["top_bit_unit_triangular"] for summary in summaries
        ),
        "all_rational_countermodel_checks_pass": all(
            summary["rational_two_cycle_verified"]
            and summary["rational_digit_patterns_verified"]
            and summary["minus_one_third_has_all_one_diagonal"]
            and summary["plus_one_third_has_single_one_diagonal"]
            for summary in summaries
        ),
        "certificate_sha256": certificate.hexdigest(),
        "interpretation": (
            "The tested finite quotients support the unit-triangular diagonal "
            "bijection and the exact -1/3, 1/3 two-cycle. The accompanying "
            "all-width proof shows that periodicity alone is consistent with "
            "the growing diagonal; a Problem 1 proof must use finite spatial "
            "support or another property absent from this countermodel."
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maximum-width",
        type=_positive_integer,
        default=DEFAULT_MAXIMUM_WIDTH,
    )
    parser.add_argument(
        "--maximum-quotient-points",
        type=_positive_integer,
        default=DEFAULT_MAXIMUM_QUOTIENT_POINTS,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    campaign = run_campaign(
        maximum_width=args.maximum_width,
        maximum_quotient_points=args.maximum_quotient_points,
    )
    payload = {
        "schema_version": 1,
        "experiment_id": "problem1-two-adic-diagonal-v1",
        "question": "problem1",
        "hypothesis": (
            "The Rule 30 growing-diagonal map is unit triangular on finite "
            "2-adic quotients, while a spatially infinite rational 2-adic "
            "state can have an exactly periodic diagonal."
        ),
        "backend": "python-exhaustive-two-oracle",
        "parameters": campaign["parameters"],
        "result_summary": campaign,
        "status": campaign["status"],
        "proof_scope": (
            "Every residue modulo 2^m for each explicitly tested width m; "
            "the separate informal proof supplies the all-width statement."
        ),
        "interpretation": campaign["interpretation"],
        "limitations": [
            "the executable campaign alone covers only the listed finite widths",
            "both rational countermodel states have infinite spatial support",
            "finite truncations matching longer prefixes may change with the horizon",
            "the result does not prove any finite seed has a periodic diagonal",
            "the result does not prove Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
