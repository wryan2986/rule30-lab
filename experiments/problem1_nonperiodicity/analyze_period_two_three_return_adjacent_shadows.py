#!/usr/bin/env python3
"""Adjacent-level shadow reduction for three-return phase plateaus.

For phase a and exact complexity k, let P_(a,k) be the set of forced-zero
schedule prefixes realized by ordinary phase outputs. Let T_(a,k) be the set of
prefixes that occur immediately before an admissible three-return continuation.
A three-return zero-penalty plateau can begin at complexity k only if its base
prefix lies in T_(a,k) but not in P_(a,k-1). Therefore the all-depth inclusion
T_(a,k) subset P_(a,k-1) is a sufficient obstruction to every such plateau.

The controlled campaign exhausts all ordinary phase outputs through a configured
complexity and checks the inclusion for every state, cut, and admissible gap
triple. It is finite evidence, not an all-depth proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from typing import Any

PHASES = ("p", "u")
GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 20
DEFAULT_SCHEDULE_CAP = 64


class ShadowCampaignLimitError(RuntimeError):
    """Raised before a controlled campaign exceeds its cap."""


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


def expected_bits(phase: str, complexity: int) -> int:
    return 2 * complexity if phase == "p" else 2 * complexity - 1


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
    raise ShadowCampaignLimitError("forced schedule reached the safety cap")


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


def prefix_keys(states: set[int], schedule_cap: int) -> set[str]:
    keys: set[str] = set()
    for state in states:
        if state & 3 != 3:
            continue
        schedule = forced_zero_schedule(state, schedule_cap)
        keys.update(schedule[:end] for end in range(len(schedule) + 1))
    return keys


def state_occurrences(
    state: int,
    previous_prefixes: set[str],
    complexity: int,
    schedule_cap: int = DEFAULT_SCHEDULE_CAP,
) -> list[dict[str, Any]]:
    if state & 3 != 3:
        return []
    schedule = forced_zero_schedule(state, schedule_cap)
    rows: list[dict[str, Any]] = []
    for cut in range(len(schedule) + 1):
        base = schedule[:cut]
        for gaps, target, complete in three_return_patterns():
            if not schedule[cut:].startswith(target):
                continue
            if not admissible(base + complete):
                continue
            rows.append(
                {
                    "cut": cut,
                    "base_prefix": base,
                    "gaps": list(gaps),
                    "forced_schedule": schedule,
                    "shadowed_one_level_down": (
                        complexity > 1 and base in previous_prefixes
                    ),
                }
            )
    return rows


def phase_campaign(
    phase: str,
    maximum_complexity: int,
    schedule_cap: int,
) -> dict[str, Any]:
    states = {phase_start(phase)}
    previous_states: set[int] = set()
    totals = {
        "outputs": 0,
        "eligible_outputs": 0,
        "occurrences": 0,
        "shadowed_occurrences": 0,
        "violations": 0,
        "positive_cut_occurrences": 0,
        "states_with_occurrence": 0,
        "maximum_cut": 0,
    }
    levels: list[dict[str, int]] = []
    examples: list[dict[str, Any]] = []

    for complexity in range(1, maximum_complexity + 1):
        previous_prefixes = (
            prefix_keys(previous_states, schedule_cap) if complexity > 1 else set()
        )
        level_occurrences = 0
        level_violations = 0
        level_states_with = 0
        eligible = 0

        for state in states:
            if state.bit_length() != expected_bits(phase, complexity):
                raise AssertionError("phase frontier bit-length law failed")
            if state & 3 != 3:
                continue
            eligible += 1
            occurrences = state_occurrences(
                state, previous_prefixes, complexity, schedule_cap
            )
            if occurrences:
                level_states_with += 1
                totals["states_with_occurrence"] += 1
            for row in occurrences:
                level_occurrences += 1
                totals["occurrences"] += 1
                if row["cut"] > 0:
                    totals["positive_cut_occurrences"] += 1
                totals["maximum_cut"] = max(totals["maximum_cut"], row["cut"])
                if row["shadowed_one_level_down"]:
                    totals["shadowed_occurrences"] += 1
                else:
                    level_violations += 1
                    totals["violations"] += 1
                if len(examples) < 12 and (
                    row["cut"] > 0 or not row["shadowed_one_level_down"]
                ):
                    examples.append({"complexity": complexity, "state_hex": hex(state), **row})

        totals["outputs"] += len(states)
        totals["eligible_outputs"] += eligible
        if level_occurrences or level_violations:
            levels.append(
                {
                    "complexity": complexity,
                    "distinct_outputs": len(states),
                    "previous_prefixes": len(previous_prefixes),
                    "three_return_occurrences": level_occurrences,
                    "states_with_occurrence": level_states_with,
                    "shadow_violations": level_violations,
                }
            )

        if complexity < maximum_complexity:
            previous_states = states
            states = {
                child for state in states for child in frontier_children(state)
            }

    if totals["shadowed_occurrences"] + totals["violations"] != totals["occurrences"]:
        raise AssertionError("occurrence accounting failed")
    return {
        "phase": phase,
        "totals": totals,
        "levels_with_occurrences": levels,
        "examples": examples,
    }


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
    schedule_cap: int = DEFAULT_SCHEDULE_CAP,
) -> dict[str, Any]:
    if not 2 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise ShadowCampaignLimitError("maximum complexity outside controlled range")
    phases = {
        phase: phase_campaign(phase, maximum_complexity, schedule_cap)
        for phase in PHASES
    }
    combined = {
        key: sum(phases[phase]["totals"][key] for phase in PHASES)
        for key in phases["p"]["totals"]
        if key != "maximum_cut"
    }
    combined["maximum_cut"] = max(
        phases[phase]["totals"]["maximum_cut"] for phase in PHASES
    )
    payload: dict[str, Any] = {
        "status": "exact-reduction-and-finite-adjacent-shadow-census",
        "maximum_complexity": maximum_complexity,
        "schedule_cap": schedule_cap,
        "admissible_three_return_patterns": len(three_return_patterns()),
        "theorem": {
            "prefix_language_reduction": (
                "A three-return zero-penalty plateau at exact complexity k exists "
                "only if a three-return-bearing base prefix realized at level k is "
                "absent from the level-(k-1) prefix language."
            ),
            "all_depth_target": (
                "For every phase and k>=2, T_(a,k) subset P_(a,k-1), where "
                "T contains prefixes immediately preceding an admissible three-return "
                "continuation."
            ),
        },
        "phases": phases,
        "combined": combined,
        "scientific_boundary": (
            "The adjacent-level reduction is exact at all depths. The verified shadow "
            "inclusion is finite through the configured complexity and does not yet "
            "prove the all-depth inclusion, phase-complexity divergence, exclusion of "
            "eventual period two, or Rule 30 center nonperiodicity."
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
    print(json.dumps(
        run_campaign(args.maximum_complexity, args.schedule_cap),
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
