#!/usr/bin/env python3
"""Analyze phase-minimal ordinary outputs at pre-branch survivor cylinders.

A schedule word of length L determines its zero-survivor residue modulo 4**L,
but its final branch is invisible at that precision: schedules first differing at
branch n agree through bit 2n+1 and first differ at bit 2n+2. Therefore an
ordinary output y matches the depth-L cylinder for q_0...q_(L-1) exactly when

* y == 3 (mod 4), and
* y's forced zero schedule begins with q_0...q_(L-2).

This off-by-one cylinder rule is essential when translating return penalties to
ordinary frontier outputs. The bounded campaign enumerates exact phase
frontiers and searches for locally admissible two-return zero penalties. It
does not prove or disprove the actual moving-fringe period-two survivor.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any

PHASES = ("p", "u")
FORBIDDEN = ("uu", "ttttt", "ututtu")
RETURN_GAPS = (2, 3, 4, 5)
DEFAULT_MAXIMUM_COMPLEXITY = 18
ABSOLUTE_MAXIMUM_COMPLEXITY = 20
DEFAULT_SCHEDULE_CAP = 48
KNOWN_COUNTEREXAMPLE = 0x1BCD3A7B3FDFB
KNOWN_BASE_WORD = "tutututttutu"
KNOWN_MIDDLE_WORD = KNOWN_BASE_WORD + "tu"
KNOWN_FINAL_WORD = KNOWN_MIDDLE_WORD + "tu"


class FrontierLimitError(RuntimeError):
    pass


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


def forced_zero_step(state: int) -> tuple[str, int] | None:
    residue = state & 15
    if residue == 7:
        branch = "u"
    elif residue == 11:
        branch = "t"
    else:
        return None
    tail = (state - 3) >> 2
    return branch, forward_generator(branch, forward_generator("p", tail))


def forced_zero_schedule(state: int, cap: int = DEFAULT_SCHEDULE_CAP) -> str:
    letters: list[str] = []
    for _ in range(cap):
        step = forced_zero_step(state)
        if step is None:
            return "".join(letters)
        branch, state = step
        letters.append(branch)
    raise FrontierLimitError("forced zero schedule reached the safety cap")


def inverse_t_mod(output: int, width: int) -> int:
    output &= (1 << width) - 1
    state = 0
    for position in range(width):
        previous = 0
        if position >= 1:
            previous |= (state >> (position - 1)) & 1
        if position >= 2:
            previous |= (state >> (position - 2)) & 1
        state |= ((((output >> position) & 1) ^ previous) << position)
    return state


def inverse_generator_mod(name: str, output: int, width: int) -> int:
    output &= (1 << width) - 1
    if name == "t":
        return inverse_t_mod(output, width)
    if name == "u":
        return inverse_t_mod(output ^ 1, width)
    if name == "p":
        recovered_low_bit = (output & 1) ^ 1
        return inverse_t_mod(
            output ^ 1 ^ (2 if recovered_low_bit == 0 else 0), width
        )
    raise ValueError("unknown inverse generator")


def backward_zero_branch(branch: str, successor: int, width: int) -> int:
    inner_width = width - 2
    state = inverse_generator_mod(branch, successor, inner_width)
    state = inverse_generator_mod("p", state, inner_width)
    return ((state << 2) | 3) & ((1 << width) - 1)


def survivor_for_word(word: str) -> int:
    state = 0
    precision = 0
    for branch in reversed(word):
        precision += 2
        state = backward_zero_branch(branch, state, precision)
    return state


def locally_admissible(word: str) -> bool:
    return not any(factor in word for factor in FORBIDDEN)


def return_extension(first_gap: int, second_gap: int, include_final_u: bool) -> str:
    if first_gap not in RETURN_GAPS or second_gap not in RETURN_GAPS:
        raise ValueError("return gaps must be in 2..5")
    result = "u" + "t" * (first_gap - 1) + "u" + "t" * (second_gap - 1)
    return result + ("u" if include_final_u else "")


def phase_campaign(
    phase: str,
    maximum_complexity: int,
    schedule_cap: int,
) -> dict[str, Any]:
    states = {phase_start(phase)}
    minimum_complexity: dict[str, int] = {}
    outputs_checked = 0
    eligible_outputs = 0
    maximum_schedule_length = 0
    candidates: list[dict[str, Any]] = []
    level_rows: list[dict[str, int]] = []

    for complexity in range(1, maximum_complexity + 1):
        rows: list[tuple[int, str]] = []
        for state in states:
            expected = 2 * complexity if phase == "p" else 2 * complexity - 1
            if state.bit_length() != expected:
                raise AssertionError("frontier bit-length law failed")
            if state & 3 != 3:
                continue
            schedule = forced_zero_schedule(state, schedule_cap)
            rows.append((state, schedule))
            maximum_schedule_length = max(maximum_schedule_length, len(schedule))
            for end in range(len(schedule) + 1):
                minimum_complexity.setdefault(schedule[:end], complexity)

        level_candidates = 0
        for state, schedule in rows:
            for cut in range(len(schedule) + 1):
                base_prefix = schedule[:cut]
                if minimum_complexity[base_prefix] != complexity:
                    continue
                for first_gap in RETURN_GAPS:
                    for second_gap in RETURN_GAPS:
                        target_extension = return_extension(
                            first_gap, second_gap, include_final_u=False
                        )
                        complete_extension = return_extension(
                            first_gap, second_gap, include_final_u=True
                        )
                        complete_word = base_prefix + complete_extension
                        if not locally_admissible(complete_word):
                            continue
                        if schedule[cut : cut + len(target_extension)] != target_extension:
                            continue
                        level_candidates += 1
                        if len(candidates) < 16:
                            candidates.append(
                                {
                                    "complexity": complexity,
                                    "state": state,
                                    "state_hex": hex(state),
                                    "cut": cut,
                                    "base_prefix_before_return": base_prefix,
                                    "first_gap": first_gap,
                                    "second_gap": second_gap,
                                    "target_extension_excluding_final_branch": target_extension,
                                    "complete_return_word": complete_word,
                                }
                            )

        outputs_checked += len(states)
        eligible_outputs += len(rows)
        level_rows.append(
            {
                "complexity": complexity,
                "distinct_outputs": len(states),
                "eligible_outputs_mod_4_eq_3": len(rows),
                "two_return_zero_candidates": level_candidates,
            }
        )
        states = {
            child
            for state in states
            for child in frontier_children(state)
        }

    return {
        "phase": phase,
        "outputs_checked": outputs_checked,
        "eligible_outputs_mod_4_eq_3": eligible_outputs,
        "maximum_complete_zero_schedule_length": maximum_schedule_length,
        "two_return_zero_candidates": candidates,
        "levels": level_rows,
    }


def verify_known_counterexample() -> dict[str, Any]:
    state = KNOWN_COUNTEREXAMPLE
    schedule = forced_zero_schedule(state)
    words = (KNOWN_BASE_WORD, KNOWN_MIDDLE_WORD, KNOWN_FINAL_WORD)
    residues = []
    for word in words:
        modulus = 4 ** len(word)
        target = survivor_for_word(word)
        residue = state % modulus
        if target != residue:
            raise AssertionError("known counterexample failed survivor congruence")
        residues.append(
            {
                "word": word,
                "depth": len(word),
                "residue_hex": hex(residue),
            }
        )
    if state.bit_length() != 49:
        raise AssertionError("known counterexample has wrong phase-u complexity")
    if not schedule.startswith(KNOWN_FINAL_WORD[:-1]):
        raise AssertionError("known counterexample has wrong forced schedule")
    if not locally_admissible(KNOWN_FINAL_WORD):
        raise AssertionError("known counterexample word is not locally admissible")
    return {
        "phase": "u",
        "complexity": 25,
        "state": state,
        "state_hex": hex(state),
        "bit_length": state.bit_length(),
        "forced_zero_schedule": schedule,
        "return_gaps": [2, 2],
        "residues": residues,
        "consequence": "kappa_u(12)=kappa_u(14)=kappa_u(16)=25 for this schedule",
    }


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
    schedule_cap: int = DEFAULT_SCHEDULE_CAP,
) -> dict[str, Any]:
    if not 1 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise FrontierLimitError("maximum complexity outside controlled range")
    phases = {
        phase: phase_campaign(phase, maximum_complexity, schedule_cap)
        for phase in PHASES
    }
    payload: dict[str, Any] = {
        "status": "finite-exhaustive-and-explicit-counterexample",
        "maximum_complexity": maximum_complexity,
        "schedule_cap": schedule_cap,
        "phases": phases,
        "known_complexity_25_counterexample": verify_known_counterexample(),
        "exact_theorems": {
            "prebranch_cylinder": (
                "depth-L survivor congruence fixes the first L-1 forced branches; "
                "the branch at index L-1 is invisible modulo 4^L"
            ),
            "frontier_characterization": (
                "kappa_a at a survivor cylinder is the first phase complexity "
                "containing an output congruent to that cylinder"
            ),
        },
        "research_consequence": (
            "known local schedule exclusions do not imply that zero return "
            "penalties are isolated; an actual-orbit-specific invariant is required"
        ),
        "scope_warning": (
            "the counterexample is a locally admissible auxiliary schedule, not the "
            "actual zero-initialized moving-fringe schedule, and does not construct "
            "a finite actual period-two survivor"
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
    print(json.dumps(run_campaign(args.maximum_complexity, args.schedule_cap), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
