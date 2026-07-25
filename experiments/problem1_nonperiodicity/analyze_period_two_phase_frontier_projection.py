#!/usr/bin/env python3
"""Analyze the exact base-four projection tower of ordinary phase frontiers.

For phase a in {p,u}, let O_(a,k) be the distinct ordinary outputs at
complexity k.  The projection pi(x)=x>>2 sends every O_(a,k) state into
O_(a,k-1).  Iterating this theorem couples every phase-minimizer witness to an
exact residual-complexity high ancestor.

This is a structural theorem about ordinary phase frontiers.  It does not prove
that the actual moving-fringe orbit has positive return penalties.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any

PHASES = ("p", "u")
DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 20
KNOWN_COUNTEREXAMPLE = 0x1BCD3A7B3FDFB
KNOWN_GENERATOR_WORD = "uuuttttutuptttututututuu"
KNOWN_DEPTHS = (12, 14, 16)


class ProjectionLimitError(RuntimeError):
    """Raised before a controlled frontier campaign exceeds its cap."""


def forward_generator(name: str, state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError("unknown generator")


def frontier_children(state: int) -> tuple[int, ...]:
    stepped = forward_generator("t", state)
    if state & 1:
        return stepped, stepped ^ 1
    return stepped, stepped ^ 1, stepped ^ 3


def phase_start(phase: str) -> int:
    if phase == "p":
        return 3
    if phase == "u":
        return 1
    raise ValueError("phase must be p or u")


def projected_child_name(parent_residue_mod_4: int) -> str:
    if parent_residue_mod_4 == 0:
        return "t"
    if parent_residue_mod_4 == 1:
        return "u"
    if parent_residue_mod_4 in (2, 3):
        return "p"
    raise ValueError("residue must be in 0..3")


def projected_child_formula(parent: int) -> int:
    if parent < 0:
        raise ValueError("parent must be nonnegative")
    quotient, residue = divmod(parent, 4)
    return forward_generator(projected_child_name(residue), quotient)


def verify_projection_identity(parent: int) -> None:
    expected = projected_child_formula(parent)
    for name in ("t", "u", "p"):
        observed = forward_generator(name, parent) >> 2
        if observed != expected:
            raise AssertionError("generator projection identity failed")


def generate_levels(phase: str, maximum_complexity: int) -> list[set[int]]:
    if maximum_complexity < 1:
        raise ValueError("maximum_complexity must be positive")
    states = {phase_start(phase)}
    levels: list[set[int]] = []
    for _ in range(maximum_complexity):
        levels.append(states)
        states = {child for state in states for child in frontier_children(state)}
    return levels


def level_projection_row(
    previous: set[int], current: set[int], complexity: int
) -> dict[str, Any]:
    fibers = Counter(value >> 2 for value in current)
    violations = sorted(parent for parent in fibers if parent not in previous)
    if violations:
        raise AssertionError("phase frontier projection left the preceding level")
    fiber_histogram = Counter(fibers.values())
    if any(size < 2 or size > 4 for size in fibers.values()):
        raise AssertionError("nonempty projection fiber must contain two to four lifts")
    return {
        "complexity": complexity,
        "distinct_outputs": len(current),
        "preceding_outputs": len(previous),
        "projected_parents": len(fibers),
        "uncovered_preceding_outputs": len(previous) - len(fibers),
        "fiber_histogram": {
            str(size): fiber_histogram.get(size, 0) for size in (2, 3, 4)
        },
        "projection_violations": 0,
    }


def verify_iterated_projection(levels: list[set[int]]) -> int:
    checks = 0
    for complexity, states in enumerate(levels, start=1):
        for value in states:
            projected = value
            for depth in range(1, complexity):
                projected >>= 2
                if projected not in levels[complexity - depth - 1]:
                    raise AssertionError("iterated projection theorem failed")
                checks += 1
    return checks


def apply_generator_word(start: int, word: str) -> int:
    state = start
    for name in word:
        state = forward_generator(name, state)
    return state


def known_counterexample_ancestry(u_levels: list[set[int]]) -> list[dict[str, Any]]:
    state = apply_generator_word(phase_start("u"), KNOWN_GENERATOR_WORD)
    if state != KNOWN_COUNTEREXAMPLE:
        raise AssertionError("known generator word did not reproduce counterexample")
    if len(KNOWN_GENERATOR_WORD) + 1 != 25:
        raise AssertionError("known counterexample complexity mismatch")
    rows = []
    for depth in KNOWN_DEPTHS:
        ancestor = state >> (2 * depth)
        residual_complexity = 25 - depth
        if residual_complexity > len(u_levels):
            raise AssertionError("campaign too shallow for known ancestor")
        if ancestor not in u_levels[residual_complexity - 1]:
            raise AssertionError("known projected ancestor left phase-u frontier")
        expected_bits = 2 * residual_complexity - 1
        if ancestor.bit_length() != expected_bits:
            raise AssertionError("known ancestor bit-length law failed")
        rows.append(
            {
                "depth": depth,
                "residual_complexity": residual_complexity,
                "ancestor": ancestor,
                "ancestor_hex": hex(ancestor),
                "bit_length": ancestor.bit_length(),
            }
        )
    return rows


def verify_strict_nonconverse(levels: dict[str, list[set[int]]]) -> list[dict[str, Any]]:
    examples = [
        {
            "phase": "p",
            "parent_complexity": 2,
            "parent": 12,
            "present_lifts": [50, 51],
            "absent_lifts": [48, 49],
        },
        {
            "phase": "u",
            "parent_complexity": 3,
            "parent": 26,
            "present_lifts": [104, 105, 107],
            "absent_lifts": [106],
        },
    ]
    for row in examples:
        phase_levels = levels[row["phase"]]
        parent_level = phase_levels[row["parent_complexity"] - 1]
        child_level = phase_levels[row["parent_complexity"]]
        if row["parent"] not in parent_level:
            raise AssertionError("nonconverse parent missing")
        for value in row["present_lifts"]:
            if value not in child_level or value >> 2 != row["parent"]:
                raise AssertionError("present nonconverse lift failed")
        for value in row["absent_lifts"]:
            if value in child_level or value >> 2 != row["parent"]:
                raise AssertionError("absent nonconverse lift failed")
    return examples


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
) -> dict[str, Any]:
    if not 13 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise ProjectionLimitError(
            "maximum complexity must be between 13 and the controlled cap"
        )
    levels = {
        phase: generate_levels(phase, maximum_complexity) for phase in PHASES
    }
    formula_checks = 0
    phases: dict[str, Any] = {}
    iterated_checks = 0
    for phase in PHASES:
        phase_levels = levels[phase]
        rows = []
        for complexity, states in enumerate(phase_levels, start=1):
            expected_bits = 2 * complexity if phase == "p" else 2 * complexity - 1
            for state in states:
                if state.bit_length() != expected_bits:
                    raise AssertionError("phase frontier bit-length law failed")
                verify_projection_identity(state)
                formula_checks += 3
            if complexity >= 2:
                rows.append(
                    level_projection_row(
                        phase_levels[complexity - 2], states, complexity
                    )
                )
        iterated_checks += verify_iterated_projection(phase_levels)
        phases[phase] = {
            "levels": rows,
            "final_complexity": maximum_complexity,
            "final_distinct_outputs": len(phase_levels[-1]),
        }

    payload: dict[str, Any] = {
        "status": "exact-theorem-and-controlled-exhaustion",
        "maximum_complexity": maximum_complexity,
        "exact_theorems": {
            "one_level_projection": (
                "for every phase a and k>=2, x in O_(a,k) implies "
                "x>>2 in O_(a,k-1)"
            ),
            "iterated_projection": (
                "x in O_(a,k) implies x>>(2L) in O_(a,k-L) "
                "for every 0<=L<k"
            ),
            "fiber_bound": (
                "every nonempty one-level projection fiber contains "
                "between two and four ordinary outputs"
            ),
            "minimizer_coupling": (
                "a complexity-k phase minimizer in a depth-L survivor cylinder "
                "has a residual phase ancestor of complexity k-L in its aligned "
                "high quotient"
            ),
        },
        "projection_identity": {
            "parent_residue_0": "G_g(4r)>>2=t(r)",
            "parent_residue_1": "G_g(4r+1)>>2=u(r)",
            "parent_residue_2": "G_g(4r+2)>>2=p(r)",
            "parent_residue_3": "G_g(4r+3)>>2=p(r)",
            "independent_of_child_generator": True,
        },
        "formula_checks": formula_checks,
        "iterated_membership_checks": iterated_checks,
        "phases": phases,
        "known_counterexample_ancestry": known_counterexample_ancestry(
            levels["u"]
        ),
        "strict_nonconverse_examples": verify_strict_nonconverse(levels),
        "research_consequence": (
            "the aligned high quotient supplies an exact necessary "
            "phase-frontier ancestor for every minimizer witness, but the "
            "ancestor alone is not sufficient to reconstruct a valid low lift"
        ),
        "scientific_boundary": (
            "This theorem couples ordinary phase minimizers to exact high "
            "ancestors. It does not prove recurring positive return penalties, "
            "phase-complexity divergence, exclusion of eventual period two, or "
            "Rule 30 center nonperiodicity."
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--maximum-complexity",
        type=int,
        default=DEFAULT_MAXIMUM_COMPLEXITY,
    )
    args = parser.parse_args()
    print(
        json.dumps(
            run_campaign(args.maximum_complexity),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
