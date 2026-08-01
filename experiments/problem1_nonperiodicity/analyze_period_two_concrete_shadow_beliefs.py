#!/usr/bin/env python3
"""Exact residue-aware concrete shadow beliefs for period-two frontiers.

For phase a, current state x in O_(a,k), and cylinder depth L, define

    B_(a,k,L)(x) = {y in O_(a,k-1): y == x (mod 4^L)}.

This is the complete set of adjacent-complexity frontier realizations in the
same survivor cylinder.  Unlike a signature powerset, every member is one
actual concrete state, so digit updates cannot splice edges from unrelated
realizations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import product
from typing import Any

PHASES = ("p", "u")
GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 20
DEFAULT_SCHEDULE_CAP = 64


class ConcreteShadowLimitError(RuntimeError):
    """Raised before a controlled campaign exceeds its configured cap."""


def forward_generator(name: str, state: int) -> int:
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError("unknown generator")


def frontier_children(state: int) -> tuple[int, ...]:
    return tuple(sorted({forward_generator(g, state) for g in "tup"}))


def phase_start(phase: str) -> int:
    if phase == "p":
        return 3
    if phase == "u":
        return 1
    raise ValueError("phase must be p or u")


def expected_bits(phase: str, complexity: int) -> int:
    return 2 * complexity if phase == "p" else 2 * complexity - 1


def build_levels(phase: str, maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {phase_start(phase)}]
    for _ in range(2, maximum_complexity + 1):
        levels.append(
            {child for state in levels[-1] for child in frontier_children(state)}
        )
    return levels


def forced_zero_schedule(state: int, cap: int = DEFAULT_SCHEDULE_CAP) -> str:
    word: list[str] = []
    for _ in range(cap):
        residue = state & 15
        if residue == 7:
            branch = "u"
        elif residue == 11:
            branch = "t"
        else:
            return "".join(word)
        state = forward_generator(
            branch, forward_generator("p", (state - 3) >> 2)
        )
        word.append(branch)
    raise ConcreteShadowLimitError("forced schedule reached safety cap")


def admissible(word: str) -> bool:
    return not any(factor in word for factor in FORBIDDEN)


def return_extension(gaps: tuple[int, ...], include_final_u: bool) -> str:
    word = "u"
    for index, gap in enumerate(gaps):
        word += "t" * (gap - 1)
        if index < len(gaps) - 1 or include_final_u:
            word += "u"
    return word


def three_return_patterns() -> tuple[tuple[tuple[int, ...], str, str], ...]:
    rows = []
    for gaps in product(GAPS, repeat=3):
        target = return_extension(gaps, False)
        complete = return_extension(gaps, True)
        if admissible(complete):
            rows.append((gaps, target, complete))
    return tuple(rows)


def concrete_shadow_belief_direct(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> tuple[int, ...]:
    """Return every level-(k-1) state in the current depth-L cylinder."""
    if not 2 <= complexity < len(levels):
        raise ValueError("complexity outside built levels")
    if not 1 <= depth < complexity:
        raise ValueError("depth must satisfy 1 <= depth < complexity")
    if current not in levels[complexity]:
        raise ValueError("current state is not in the requested frontier")
    modulus = 4**depth
    residue = current % modulus
    return tuple(sorted(state for state in levels[complexity - 1] if state % modulus == residue))


def lift_belief_one_digit(
    levels: list[set[int]], target_level: int, belief: tuple[int, ...], digit: int
) -> tuple[int, ...]:
    """Append one common low base-four digit to one concrete belief."""
    if digit not in range(4):
        raise ValueError("digit must be in {0,1,2,3}")
    target = levels[target_level]
    return tuple(4 * state + digit for state in belief if 4 * state + digit in target)


def concrete_shadow_belief_recursive(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> tuple[int, ...]:
    """Compute the exact belief by recursive common-digit lifting.

    The base case selects the complete previous frontier with the required low
    digit.  For greater depth, strip the common digit from the current state,
    recurse one level lower, then append that exact digit to every surviving
    concrete shadow realization.
    """
    if not 2 <= complexity < len(levels):
        raise ValueError("complexity outside built levels")
    if not 1 <= depth < complexity:
        raise ValueError("depth must satisfy 1 <= depth < complexity")
    if current not in levels[complexity]:
        raise ValueError("current state is not in the requested frontier")
    digit = current & 3
    if depth == 1:
        return tuple(sorted(state for state in levels[complexity - 1] if state & 3 == digit))
    parent = current >> 2
    belief = concrete_shadow_belief_recursive(
        levels, complexity - 1, parent, depth - 1
    )
    return lift_belief_one_digit(levels, complexity - 1, belief, digit)


def concrete_shadow_trace(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> tuple[int, ...]:
    """Return belief cardinalities from the first common digit to full depth."""
    if depth == 1:
        return (len(concrete_shadow_belief_recursive(levels, complexity, current, 1)),)
    parent_trace = concrete_shadow_trace(levels, complexity - 1, current >> 2, depth - 1)
    full = concrete_shadow_belief_recursive(levels, complexity, current, depth)
    return parent_trace + (len(full),)


def phase_campaign(
    phase: str, maximum_complexity: int, schedule_cap: int
) -> dict[str, Any]:
    levels = build_levels(phase, maximum_complexity)
    patterns = three_return_patterns()
    totals = Counter(
        outputs=sum(len(levels[k]) for k in range(1, maximum_complexity + 1))
    )
    totals["eligible_outputs"] = sum(
        1
        for k in range(1, maximum_complexity + 1)
        for state in levels[k]
        if state & 3 == 3
    )
    belief_sizes: Counter[int] = Counter()
    belief_sizes_by_depth: Counter[tuple[int, int]] = Counter()
    distinct_cylinders: set[tuple[int, int, int]] = set()
    examples: list[dict[str, Any]] = []
    smallest: tuple[int, dict[str, Any]] | None = None

    for complexity in range(2, maximum_complexity + 1):
        level_had_occurrence = False
        for current in sorted(levels[complexity]):
            if current.bit_length() != expected_bits(phase, complexity):
                raise AssertionError("frontier bit-length law failed")
            if current & 3 != 3:
                continue
            schedule = forced_zero_schedule(current, schedule_cap)
            for cut in range(len(schedule) + 1):
                base = schedule[:cut]
                matches = [
                    gaps
                    for gaps, target, complete in patterns
                    if schedule[cut:].startswith(target)
                    and admissible(base + complete)
                ]
                if not matches:
                    continue
                level_had_occurrence = True
                depth = cut + 1
                if depth >= complexity:
                    raise AssertionError("occurrence cylinder consumed entire frontier")
                direct = concrete_shadow_belief_direct(
                    levels, complexity, current, depth
                )
                recursive = concrete_shadow_belief_recursive(
                    levels, complexity, current, depth
                )
                if direct != recursive:
                    raise AssertionError("direct and recursive beliefs disagree")
                trace = concrete_shadow_trace(levels, complexity, current, depth)
                residue = current % (4**depth)
                distinct_cylinders.add((complexity, depth, residue))
                weight = len(matches)
                totals["occurrences"] += weight
                totals["maximum_cut"] = max(totals["maximum_cut"], cut)
                totals["maximum_depth"] = max(totals["maximum_depth"], depth)
                if cut:
                    totals["positive_cut_occurrences"] += weight
                if direct:
                    totals["shadowed_occurrences"] += weight
                else:
                    totals["empty_beliefs"] += weight
                totals["total_shadow_realizations"] += weight * len(direct)
                belief_sizes[len(direct)] += weight
                belief_sizes_by_depth[(depth, len(direct))] += weight
                row = {
                    "complexity": complexity,
                    "state_hex": hex(current),
                    "cut": cut,
                    "depth": depth,
                    "residue_hex": hex(residue),
                    "gaps": [list(gaps) for gaps in matches],
                    "belief_size": len(direct),
                    "belief_trace": list(trace),
                    "first_shadow_hex": hex(direct[0]) if direct else None,
                }
                if smallest is None or len(direct) < smallest[0]:
                    smallest = (len(direct), row)
                if cut > 0 and len(examples) < 8:
                    examples.append(row)
        if level_had_occurrence:
            totals["levels_with_occurrences"] += 1

    if totals["occurrences"]:
        totals["distinct_occurrence_cylinders"] = len(distinct_cylinders)
        totals["minimum_final_belief"] = min(belief_sizes)
        totals["maximum_final_belief"] = max(belief_sizes)

    return {
        "phase": phase,
        "totals": dict(totals),
        "belief_size_histogram": {
            str(size): count for size, count in sorted(belief_sizes.items())
        },
        "belief_sizes_by_depth": {
            f"depth-{depth}/size-{size}": count
            for (depth, size), count in sorted(belief_sizes_by_depth.items())
        },
        "smallest_belief_example": smallest[1] if smallest else None,
        "positive_cut_examples": examples,
    }


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
    schedule_cap: int = DEFAULT_SCHEDULE_CAP,
) -> dict[str, Any]:
    if not 2 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise ConcreteShadowLimitError("maximum complexity outside controlled range")
    phases = {
        phase: phase_campaign(phase, maximum_complexity, schedule_cap)
        for phase in PHASES
    }
    additive_fields = (
        "outputs",
        "eligible_outputs",
        "occurrences",
        "positive_cut_occurrences",
        "shadowed_occurrences",
        "empty_beliefs",
        "total_shadow_realizations",
        "levels_with_occurrences",
        "distinct_occurrence_cylinders",
    )
    combined: dict[str, int] = {
        field: sum(phases[phase]["totals"].get(field, 0) for phase in PHASES)
        for field in additive_fields
    }
    combined["maximum_cut"] = max(
        phases[phase]["totals"].get("maximum_cut", 0) for phase in PHASES
    )
    combined["maximum_depth"] = max(
        phases[phase]["totals"].get("maximum_depth", 0) for phase in PHASES
    )
    combined["minimum_final_belief"] = min(
        phases[phase]["totals"]["minimum_final_belief"] for phase in PHASES
    )
    combined["maximum_final_belief"] = max(
        phases[phase]["totals"]["maximum_final_belief"] for phase in PHASES
    )
    payload: dict[str, Any] = {
        "status": "exact-residue-aware-concrete-shadow-belief-recursion",
        "maximum_complexity": maximum_complexity,
        "schedule_cap": schedule_cap,
        "admissible_three_return_patterns": len(three_return_patterns()),
        "theorem": {
            "belief_definition": (
                "B_(a,k,L)(x) is the complete set of O_(a,k-1) states congruent "
                "to x modulo 4^L. It is nonempty exactly when the cylinder has "
                "an adjacent-complexity concrete shadow."
            ),
            "recursive_update": (
                "For x=4q+d and L>=2, B_(a,k,L)(x) is obtained from "
                "B_(a,k-1,L-1)(q) by retaining exactly the concrete lifts "
                "4p+d that belong to O_(a,k-1)."
            ),
            "realization_consistency": (
                "Every recursive belief member is one actual frontier state; "
                "the update never combines transitions from unrelated states."
            ),
        },
        "phases": phases,
        "combined": combined,
        "scientific_boundary": (
            "The concrete belief recursion is exact at every depth. Nonemptiness "
            "for three-return occurrence cylinders is verified only through the "
            "configured complexity; this does not prove the all-depth adjacent-"
            "shadow inclusion, phase-complexity divergence, exclusion of eventual "
            "center period two, or Rule 30 center nonperiodicity."
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--maximum-complexity", type=int, default=DEFAULT_MAXIMUM_COMPLEXITY
    )
    parser.add_argument("--schedule-cap", type=int, default=DEFAULT_SCHEDULE_CAP)
    args = parser.parse_args()
    print(
        json.dumps(
            run_campaign(args.maximum_complexity, args.schedule_cap),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
