#!/usr/bin/env python3
"""Audit exact finite Boolean constraints for hypothetical center periods.

For a period p, the condition c_(t+p) = c_t is equivalent at time t to

    Delta_p(x[-p..p]) = F^p(x)_0 XOR x_0 = 0.

Rule 30 is left-permutive, so Delta_p is affine in the leftmost variable
x[-p] and the equation uniquely solves that variable from the other 2p
cells.  This experiment exhaustively constructs the truth table and algebraic
normal form (ANF) for explicitly bounded p.  It asks whether the constraint
loses an essential variable, radius, or algebraic degree in a way that could
support a depth-independent phase argument.

Finite saturation of a causal cone does not prove that an eventually periodic
center is impossible.  Algebraic degree of a function over arbitrary rows also
does not prove nonperiodicity for the fixed single-cell seed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from typing import Any


DEFAULT_MINIMUM_PERIOD = 1
DEFAULT_MAXIMUM_PERIOD = 8
DEFAULT_MAX_TOTAL_ASSIGNMENTS = 1_000_000
DEFAULT_MAX_MOBIUS_UPDATES = 30_000_000
DEFAULT_MAX_PERIOD = 10
DEFAULT_MAX_REPORTED_TOP_MONOMIALS = 16


class PeriodDefectLimitError(RuntimeError):
    """Raised before an exact finite resource cap is crossed."""


@dataclass(frozen=True)
class WorkEstimate:
    assignments: int
    mobius_updates: int
    direct_cell_updates: int


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def estimate_work(minimum_period: int, maximum_period: int) -> WorkEstimate:
    """Return exact logical loop counts for one requested period interval."""

    if minimum_period <= 0 or maximum_period < minimum_period:
        raise ValueError("period interval must satisfy 1 <= minimum <= maximum")
    assignments = 0
    mobius_updates = 0
    direct_cell_updates = 0
    for period in range(minimum_period, maximum_period + 1):
        variables = 2 * period + 1
        table_entries = 1 << variables
        assignments += table_entries
        mobius_updates += variables * (table_entries // 2)
        direct_cell_updates += table_entries * period * period
    return WorkEstimate(assignments, mobius_updates, direct_cell_updates)


def _checked_period(period: int) -> int:
    if not isinstance(period, int) or isinstance(period, bool) or period <= 0:
        raise ValueError("period must be a positive integer")
    return period


def iterated_center_cell_array(period: int, assignment: int) -> int:
    """Evaluate F^p(x)_0 with an ordinary shrinking cell array.

    Bit i of ``assignment`` is spatial position ``-p+i``.  Only the complete
    radius-p causal cone is represented.
    """

    period = _checked_period(period)
    variables = 2 * period + 1
    if assignment < 0 or assignment >= (1 << variables):
        raise ValueError("assignment does not fit the period causal cone")
    row = [(assignment >> index) & 1 for index in range(variables)]
    for _ in range(period):
        row = [
            row[index] ^ (row[index + 1] | row[index + 2])
            for index in range(len(row) - 2)
        ]
    if len(row) != 1:
        raise AssertionError("shrinking causal cone did not reach one cell")
    return row[0]


def iterated_center_packed(period: int, assignment: int) -> int:
    """Independent packed evaluation of F^p(x)_0."""

    period = _checked_period(period)
    variables = 2 * period + 1
    if assignment < 0 or assignment >= (1 << variables):
        raise ValueError("assignment does not fit the period causal cone")
    row = assignment
    width = variables
    for _ in range(period):
        width -= 2
        row = (row ^ ((row >> 1) | (row >> 2))) & ((1 << width) - 1)
    return row & 1


def period_defect_truth_table(period: int) -> bytearray:
    """Return Delta_p for every causal-cone assignment in integer order."""

    period = _checked_period(period)
    variables = 2 * period + 1
    table = bytearray(1 << variables)
    for assignment in range(len(table)):
        direct = iterated_center_cell_array(period, assignment)
        packed = iterated_center_packed(period, assignment)
        if direct != packed:
            raise AssertionError(
                f"independent p-step evaluators disagree for p={period}, "
                f"assignment={assignment}"
            )
        table[assignment] = direct ^ ((assignment >> period) & 1)
    return table


def mobius_anf(truth_table: bytes | bytearray, variables: int) -> bytearray:
    """Convert a Boolean truth table to ANF coefficients in place order."""

    if variables <= 0 or len(truth_table) != (1 << variables):
        raise ValueError("truth table length must equal 2**variables")
    if any(value not in (0, 1) for value in truth_table):
        raise ValueError("truth table must contain only zero and one")
    coefficients = bytearray(truth_table)
    for variable in range(variables):
        half_block = 1 << variable
        block = half_block << 1
        for base in range(0, len(coefficients), block):
            for mask in range(base + half_block, base + block):
                coefficients[mask] ^= coefficients[mask - half_block]
    return coefficients


def essential_variable_indices(
    truth_table: bytes | bytearray, variables: int
) -> tuple[int, ...]:
    """Return variables whose Boolean derivative is nonzero somewhere."""

    if variables <= 0 or len(truth_table) != (1 << variables):
        raise ValueError("truth table length must equal 2**variables")
    essential: list[int] = []
    for variable in range(variables):
        bit = 1 << variable
        found = False
        for base in range(0, len(truth_table), bit << 1):
            for mask in range(base, base + bit):
                if truth_table[mask] != truth_table[mask | bit]:
                    found = True
                    break
            if found:
                break
        if found:
            essential.append(variable)
    return tuple(essential)


def _positions(mask: int, period: int) -> list[int]:
    return [
        index - period
        for index in range(2 * period + 1)
        if mask & (1 << index)
    ]


def _analyze_period(
    period: int,
    *,
    max_reported_top_monomials: int,
) -> tuple[dict[str, Any], bytes, bytes]:
    variables = 2 * period + 1
    truth_table = period_defect_truth_table(period)
    coefficients = mobius_anf(truth_table, variables)
    essential = essential_variable_indices(truth_table, variables)

    left_permutive = all(
        truth_table[assignment] ^ truth_table[assignment | 1] == 1
        for assignment in range(0, len(truth_table), 2)
    )
    if not left_permutive:
        raise AssertionError("p-step defect lost Rule 30 left-permutivity")

    solved_left_verified = True
    solved_left_truth = bytearray(1 << (variables - 1))
    for remaining in range(len(solved_left_truth)):
        with_left_zero = remaining << 1
        required_left = truth_table[with_left_zero]
        solved_left_truth[remaining] = required_left
        satisfying = with_left_zero | required_left
        rejected = with_left_zero | (required_left ^ 1)
        if truth_table[satisfying] != 0 or truth_table[rejected] != 1:
            solved_left_verified = False
            break
    if not solved_left_verified:
        raise AssertionError("solved-left constraint verification failed")

    monomial_masks = [
        mask for mask, coefficient in enumerate(coefficients) if coefficient
    ]
    degree_histogram = Counter(mask.bit_count() for mask in monomial_masks)
    algebraic_degree = max(degree_histogram)
    top_masks = [
        mask
        for mask in monomial_masks
        if mask.bit_count() == algebraic_degree
    ]
    expected_degree = 2 if period == 1 else 2 * period - 1

    # These exact small-period patterns are reported descriptively.  The
    # p=1 and p=2 bases are genuinely exceptional; from p=3 onward the
    # observed top term is the contiguous interval [-p+2, p].  Nothing here
    # asserts that the latter pattern continues beyond the exhausted range.
    if period == 1:
        reference_top_positions = [[0, 1]]
    elif period == 2:
        reference_top_positions = [[-1, 1, 2], [0, 1, 2]]
    else:
        reference_top_positions = [list(range(-period + 2, period + 1))]
    actual_top_positions = [_positions(mask, period) for mask in top_masks]

    summary = {
        "period": period,
        "variables": variables,
        "spatial_interval": [-period, period],
        "assignments_exhausted": len(truth_table),
        "period_constraint_solutions": truth_table.count(0),
        "left_permutive": left_permutive,
        "solved_left_constraint_verified": solved_left_verified,
        "essential_spatial_positions": [
            index - period for index in essential
        ],
        "full_causal_cone_essential": len(essential) == variables,
        "algebraic_degree": algebraic_degree,
        "expected_linear_degree_pattern": expected_degree,
        "matches_linear_degree_pattern": algebraic_degree == expected_degree,
        "anf_monomials": len(monomial_masks),
        "anf_density": len(monomial_masks) / len(coefficients),
        "degree_histogram": {
            str(degree): count
            for degree, count in sorted(degree_histogram.items())
        },
        "highest_degree_monomial_count": len(top_masks),
        "highest_degree_monomials": actual_top_positions[
            :max_reported_top_monomials
        ],
        "reference_highest_degree_monomials": reference_top_positions,
        "matches_reference_top_pattern": (
            actual_top_positions == reference_top_positions
        ),
        "truth_table_sha256": hashlib.sha256(truth_table).hexdigest(),
        "solved_left_truth_table_sha256": hashlib.sha256(
            solved_left_truth
        ).hexdigest(),
        "anf_coefficients_sha256": hashlib.sha256(coefficients).hexdigest(),
    }
    return summary, bytes(truth_table), bytes(coefficients)


def run_campaign(
    *,
    minimum_period: int,
    maximum_period: int,
    max_total_assignments: int = DEFAULT_MAX_TOTAL_ASSIGNMENTS,
    max_mobius_updates: int = DEFAULT_MAX_MOBIUS_UPDATES,
    max_period: int = DEFAULT_MAX_PERIOD,
    max_reported_top_monomials: int = DEFAULT_MAX_REPORTED_TOP_MONOMIALS,
) -> dict[str, Any]:
    """Run one deterministic finite p-step defect campaign."""

    if minimum_period <= 0 or maximum_period < minimum_period:
        raise ValueError("period interval must satisfy 1 <= minimum <= maximum")
    if maximum_period > max_period:
        raise PeriodDefectLimitError(
            f"period {maximum_period} exceeds configured maximum {max_period}"
        )
    if any(
        not isinstance(value, int)
        or isinstance(value, bool)
        or value <= 0
        for value in (
            max_total_assignments,
            max_mobius_updates,
            max_period,
            max_reported_top_monomials,
        )
    ):
        raise ValueError("resource and report caps must be positive integers")

    work = estimate_work(minimum_period, maximum_period)
    if work.assignments > max_total_assignments:
        raise PeriodDefectLimitError(
            f"{work.assignments} assignments exceed configured maximum "
            f"{max_total_assignments}"
        )
    if work.mobius_updates > max_mobius_updates:
        raise PeriodDefectLimitError(
            f"{work.mobius_updates} Mobius updates exceed configured maximum "
            f"{max_mobius_updates}"
        )

    certificate = hashlib.sha256()
    certificate.update(b"rule30-period-defect-certificate-v1\0")
    certificate.update(
        json.dumps(
            {
                "minimum_period": minimum_period,
                "maximum_period": maximum_period,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
    )
    certificate.update(b"\0")
    summaries: list[dict[str, Any]] = []
    for period in range(minimum_period, maximum_period + 1):
        summary, truth_table, coefficients = _analyze_period(
            period,
            max_reported_top_monomials=max_reported_top_monomials,
        )
        summaries.append(summary)
        certificate.update(period.to_bytes(2, "little"))
        certificate.update(len(truth_table).to_bytes(8, "little"))
        certificate.update(truth_table)
        certificate.update(coefficients)

    all_full_cones = all(
        summary["full_causal_cone_essential"] for summary in summaries
    )
    all_degree_pattern = all(
        summary["matches_linear_degree_pattern"] for summary in summaries
    )
    all_reference_top = all(
        summary["matches_reference_top_pattern"] for summary in summaries
    )
    collapse_periods = [
        summary["period"]
        for summary in summaries
        if not (
            summary["full_causal_cone_essential"]
            and summary["matches_linear_degree_pattern"]
        )
    ]

    return {
        "status": "finite-exhaustive",
        "parameters": {
            "minimum_period": minimum_period,
            "maximum_period": maximum_period,
        },
        "resource_caps": {
            "maximum_period": max_period,
            "maximum_total_assignments": max_total_assignments,
            "maximum_mobius_updates": max_mobius_updates,
            "maximum_reported_top_monomials": max_reported_top_monomials,
        },
        "coverage": {
            "periods": maximum_period - minimum_period + 1,
            "assignments_exhausted": work.assignments,
            "mobius_updates": work.mobius_updates,
            "cell_array_logical_cell_updates": work.direct_cell_updates,
            "independent_oracles": 2,
        },
        "period_summaries": summaries,
        "all_periods_use_full_causal_cone": all_full_cones,
        "all_periods_match_linear_degree_pattern": all_degree_pattern,
        "all_periods_match_reference_top_pattern": all_reference_top,
        "structural_collapse_periods": collapse_periods,
        "certificate_sha256": certificate.hexdigest(),
        "interpretation": (
            "For each tested p, the exact condition c_(t+p)=c_t uses every "
            "cell in x[-p..p], uniquely solves x[-p], and has the reported "
            "linearly growing ANF degree. This is a finite obstruction to a narrower "
            "local phase constraint, not a proof against an eventually "
            "periodic center or against a nonlocal simplification."
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--minimum-period",
        type=_positive_integer,
        default=DEFAULT_MINIMUM_PERIOD,
    )
    parser.add_argument(
        "--maximum-period",
        type=_positive_integer,
        default=DEFAULT_MAXIMUM_PERIOD,
    )
    parser.add_argument(
        "--max-total-assignments",
        type=_positive_integer,
        default=DEFAULT_MAX_TOTAL_ASSIGNMENTS,
    )
    parser.add_argument(
        "--max-mobius-updates",
        type=_positive_integer,
        default=DEFAULT_MAX_MOBIUS_UPDATES,
    )
    parser.add_argument(
        "--max-period", type=_positive_integer, default=DEFAULT_MAX_PERIOD
    )
    parser.add_argument(
        "--max-reported-top-monomials",
        type=_positive_integer,
        default=DEFAULT_MAX_REPORTED_TOP_MONOMIALS,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    campaign = run_campaign(
        minimum_period=args.minimum_period,
        maximum_period=args.maximum_period,
        max_total_assignments=args.max_total_assignments,
        max_mobius_updates=args.max_mobius_updates,
        max_period=args.max_period,
        max_reported_top_monomials=args.max_reported_top_monomials,
    )
    payload = {
        "schema_version": 1,
        "experiment_id": "problem1-period-defect-anf-v1",
        "question": "problem1",
        "hypothesis": (
            "A hypothetical center period may induce a lower-radius or "
            "lower-degree exact phase constraint compatible with fixed "
            "moving-frame periods."
        ),
        "backend": "python-exhaustive-boolean",
        "parameters": campaign["parameters"],
        "result_summary": campaign,
        "status": campaign["status"],
        "proof_scope": (
            "Every Boolean assignment in each p-step causal cone for the "
            "explicit finite period interval."
        ),
        "interpretation": campaign["interpretation"],
        "limitations": [
            "finite period bounds do not cover arbitrary eventual periods",
            "full finite-cone dependence does not exclude nonlocal identities",
            "ANF degree over arbitrary rows does not imply behavior of one fixed seed",
            "the constraints are imposed at one spatial site, not at every translate",
            "no result proves Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
