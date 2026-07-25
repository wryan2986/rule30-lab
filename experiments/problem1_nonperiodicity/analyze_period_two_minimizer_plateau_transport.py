#!/usr/bin/env python3
"""Exact fixed-complexity plateau transport for period-two phase minimizers.

For phase a, complexity k, depth L and residue X modulo 4**L, let
C_(a,k)(X,L) be the exact phase-frontier cylinder. If X' extends X by an
r-digit base-four block c, then the same-complexity cylinder is obtained by
retaining exactly those residual states whose next r digits equal c and then
shifting the consumed block away. This gives an exact return-plateau survival
criterion without searching any higher complexity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from functools import lru_cache
from itertools import product
from typing import Any

PHASES = ("p", "u")
GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
CHILD_DIGIT_MASK = {0: 0b1011, 1: 0b1100, 2: 0b1110, 3: 0b0011}
DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 20
DEFAULT_SCHEDULE_CAP = 64
KNOWN = 0x1BCD3A7B3FDFB
KNOWN_BASE = "tutututttutu"
KNOWN_MIDDLE = KNOWN_BASE + "tu"
KNOWN_FINAL = KNOWN_MIDDLE + "tu"
EXPECTED = {
    1: {"p": 1, "u": 2},
    5: {"p": 8, "u": 12},
    7: {"p": 13, "u": 14},
    12: {"p": 28, "u": 27},
    14: {"p": 33, "u": 30},
}


class CampaignLimitError(RuntimeError):
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


def inverse_t(output: int) -> int | None:
    if output == 0:
        return 0
    width = output.bit_length() - 2
    if width <= 0:
        return None
    state = 0
    for position in range(width):
        lower = 0
        if position >= 1:
            lower |= (state >> (position - 1)) & 1
        if position >= 2:
            lower |= (state >> (position - 2)) & 1
        state |= ((((output >> position) & 1) ^ lower) << position)
    return state if forward_generator("t", state) == output else None


def inverse_generator(name: str, output: int) -> int | None:
    if name == "t":
        state = inverse_t(output)
    elif name == "u":
        state = inverse_t(output ^ 1)
    elif name == "p":
        recovered_low_bit = (output & 1) ^ 1
        state = inverse_t(output ^ 1 ^ (2 if recovered_low_bit == 0 else 0))
    else:
        raise ValueError("unknown generator")
    if state is None or forward_generator(name, state) != output:
        return None
    return state


def candidate_parent(quotient: int, parent_digit: int) -> int | None:
    name = "t" if parent_digit == 0 else "u" if parent_digit == 1 else "p"
    residual = inverse_generator(name, quotient)
    return None if residual is None else 4 * residual + parent_digit


def build_levels(phase: str, maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {phase_start(phase)}]
    for _ in range(2, maximum_complexity + 1):
        levels.append(
            {child for state in levels[-1] for child in frontier_children(state)}
        )
    return levels


def make_member(levels: dict[str, list[set[int]]], base_cap: int):
    @lru_cache(maxsize=None)
    def member(phase: str, complexity: int, target: int) -> bool:
        if complexity < 1 or target < 0:
            return False
        if target.bit_length() != expected_bits(phase, complexity):
            return False
        if complexity <= base_cap:
            return target in levels[phase][complexity]
        quotient, digit = divmod(target, 4)
        for parent_digit in range(4):
            if not (CHILD_DIGIT_MASK[parent_digit] >> digit) & 1:
                continue
            parent = candidate_parent(quotient, parent_digit)
            if parent is not None and member(phase, complexity - 1, parent):
                return True
        return False

    return member


def inverse_t_mod(output: int, width: int) -> int:
    output &= (1 << width) - 1 if width else 0
    state = 0
    for position in range(width):
        lower = 0
        if position >= 1:
            lower |= (state >> (position - 1)) & 1
        if position >= 2:
            lower |= (state >> (position - 2)) & 1
        state |= ((((output >> position) & 1) ^ lower) << position)
    return state


def inverse_generator_mod(name: str, output: int, width: int) -> int:
    output &= (1 << width) - 1 if width else 0
    if name == "t":
        return inverse_t_mod(output, width)
    if name == "u":
        return inverse_t_mod(output ^ 1, width)
    if name == "p":
        recovered_low_bit = (output & 1) ^ 1
        return inverse_t_mod(
            output ^ 1 ^ (2 if recovered_low_bit == 0 else 0), width
        )
    raise ValueError("unknown generator")


def survivor_for_word(word: str) -> int:
    state = 0
    precision = 0
    for branch in reversed(word):
        precision += 2
        inner_width = precision - 2
        state = inverse_generator_mod(branch, state, inner_width)
        state = inverse_generator_mod("p", state, inner_width)
        state = ((state << 2) | 3) & ((1 << precision) - 1)
    return state


def fringe_step(state: int) -> int:
    row = 1 + 2 * state
    odd = row ^ ((row >> 1) | (row >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def actual_driver(length: int) -> str:
    state = 0
    word: list[str] = []
    for _ in range(length):
        word.append("u" if state & 3 == 0 else "t")
        state = fringe_step(state)
    return "".join(word)


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
    raise CampaignLimitError("forced zero schedule reached the safety cap")


def admissible(word: str) -> bool:
    return not any(factor in word for factor in FORBIDDEN)


def return_extension(gaps: tuple[int, ...], include_final_u: bool) -> str:
    word = "u"
    for index, gap in enumerate(gaps):
        word += "t" * (gap - 1)
        if index < len(gaps) - 1 or include_final_u:
            word += "u"
    return word


def cylinder_filter(
    phase: str,
    depth: int,
    complexity: int,
    residue: int,
    levels: dict[str, list[set[int]]],
    member,
) -> list[int]:
    member.cache_clear()
    if complexity <= depth:
        return [residue] if member(phase, complexity, residue) else []
    residual_complexity = complexity - depth
    current = sorted(levels[phase][residual_complexity])
    for index in range(depth - 1, -1, -1):
        digit = (residue >> (2 * index)) & 3
        next_complexity = residual_complexity + (depth - index)
        current = [
            4 * quotient + digit
            for quotient in current
            if member(phase, next_complexity, 4 * quotient + digit)
        ]
        if not current:
            break
    return current


def plateau_transport(
    states: list[int],
    old_depth: int,
    new_depth: int,
    old_residue: int,
    new_residue: int,
) -> dict[str, Any]:
    if new_depth <= old_depth:
        raise ValueError("new depth must be larger")
    if new_residue % (4**old_depth) != old_residue:
        raise ValueError("cylinders are not nested")
    span = new_depth - old_depth
    block = (new_residue - old_residue) // (4**old_depth)
    mask = 4**span - 1
    survivors = [
        state
        for state in states
        if ((state >> (2 * old_depth)) & mask) == block
    ]
    old_residuals = [state >> (2 * old_depth) for state in states]
    shifted = [state >> (2 * new_depth) for state in survivors]
    predicted = [
        residual >> (2 * span)
        for residual in old_residuals
        if residual & mask == block
    ]
    if shifted != predicted:
        raise AssertionError("residual transport identity failed")
    return {
        "span": span,
        "block": block,
        "block_base4_digits": [(block >> (2 * i)) & 3 for i in range(span)],
        "input_count": len(states),
        "survivor_count": len(survivors),
        "survivor_states_hex": [hex(state) for state in survivors],
        "shifted_residuals_hex": [hex(state) for state in shifted],
    }


def exhaustive_transport(levels: dict[str, list[set[int]]]) -> int:
    checks = 0
    for phase in PHASES:
        for complexity in range(1, 9):
            full = sorted(levels[phase][complexity])
            for new_depth in range(2, min(5, complexity + 1) + 1):
                for old_depth in range(1, new_depth):
                    old_modulus = 4**old_depth
                    new_modulus = 4**new_depth
                    groups: dict[int, list[int]] = {}
                    for state in full:
                        groups.setdefault(state % old_modulus, []).append(state)
                    for new_residue in {state % new_modulus for state in full}:
                        old_residue = new_residue % old_modulus
                        row = plateau_transport(
                            groups[old_residue],
                            old_depth,
                            new_depth,
                            old_residue,
                            new_residue,
                        )
                        direct = [
                            state
                            for state in groups[old_residue]
                            if state % new_modulus == new_residue
                        ]
                        if row["survivor_states_hex"] != [hex(state) for state in direct]:
                            raise AssertionError("transport disagreed with direct grouping")
                        checks += 1
    return checks


def frontier_plateau_census(
    maximum_complexity: int, schedule_cap: int
) -> dict[str, Any]:
    patterns = {
        return_count: [
            (
                gaps,
                return_extension(gaps, False),
                return_extension(gaps, True),
            )
            for gaps in product(GAPS, repeat=return_count)
            if admissible(return_extension(gaps, True))
        ]
        for return_count in (2, 3)
    }
    result: dict[str, Any] = {}
    for phase in PHASES:
        states = {phase_start(phase)}
        minimum: dict[str, int] = {}
        totals = {2: 0, 3: 0}
        examples: dict[int, list[dict[str, Any]]] = {2: [], 3: []}
        outputs = 0
        eligible = 0
        candidate_levels: list[dict[str, int]] = []
        for complexity in range(1, maximum_complexity + 1):
            rows: list[tuple[int, str]] = []
            for state in states:
                if state & 3 != 3:
                    continue
                schedule = forced_zero_schedule(state, schedule_cap)
                rows.append((state, schedule))
                eligible += 1
                for end in range(len(schedule) + 1):
                    minimum.setdefault(schedule[:end], complexity)
            level_counts = {2: 0, 3: 0}
            for state, schedule in rows:
                for cut in range(len(schedule) + 1):
                    prefix = schedule[:cut]
                    if minimum[prefix] != complexity:
                        continue
                    for return_count in (2, 3):
                        for gaps, target, complete in patterns[return_count]:
                            if not schedule[cut:].startswith(target):
                                continue
                            if not admissible(prefix + complete):
                                continue
                            totals[return_count] += 1
                            level_counts[return_count] += 1
                            if len(examples[return_count]) < 4:
                                examples[return_count].append(
                                    {
                                        "complexity": complexity,
                                        "state_hex": hex(state),
                                        "cut": cut,
                                        "base_prefix": prefix,
                                        "gaps": list(gaps),
                                        "forced_schedule": schedule,
                                    }
                                )
            if level_counts[2] or level_counts[3]:
                candidate_levels.append(
                    {
                        "complexity": complexity,
                        "two_return": level_counts[2],
                        "three_return": level_counts[3],
                    }
                )
            outputs += len(states)
            states = {
                child for state in states for child in frontier_children(state)
            }
        result[phase] = {
            "outputs_checked": outputs,
            "eligible_outputs": eligible,
            "two_return_candidates": totals[2],
            "three_return_candidates": totals[3],
            "candidate_levels": candidate_levels,
            "examples": examples,
        }
    return result


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
    schedule_cap: int = DEFAULT_SCHEDULE_CAP,
) -> dict[str, Any]:
    if not 8 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise CampaignLimitError("maximum complexity outside controlled range")
    levels = {
        phase: build_levels(phase, maximum_complexity) for phase in PHASES
    }
    member = make_member(levels, maximum_complexity)
    transport_checks = exhaustive_transport(levels)

    driver = actual_driver(20)
    return_depths = [
        index + 1
        for index, branch in enumerate(driver)
        if branch == "u" and index + 1 <= 14
    ]
    actual_rows: list[dict[str, Any]] = []
    for old_depth, new_depth in zip(return_depths, return_depths[1:]):
        old_residue = survivor_for_word(driver[:old_depth])
        new_residue = survivor_for_word(driver[:new_depth])
        phase_rows: dict[str, Any] = {}
        for phase in PHASES:
            complexity = EXPECTED[old_depth][phase]
            states = cylinder_filter(
                phase,
                old_depth,
                complexity,
                old_residue,
                levels,
                member,
            )
            phase_rows[phase] = {
                "complexity": complexity,
                "minimum_count": len(states),
                "transport": plateau_transport(
                    states,
                    old_depth,
                    new_depth,
                    old_residue,
                    new_residue,
                ),
            }
        actual_rows.append(
            {
                "old_depth": old_depth,
                "new_depth": new_depth,
                "gap": new_depth - old_depth,
                "phases": phase_rows,
            }
        )

    known_schedule = forced_zero_schedule(KNOWN)
    known_transports = []
    for old_word, new_word in (
        (KNOWN_BASE, KNOWN_MIDDLE),
        (KNOWN_MIDDLE, KNOWN_FINAL),
    ):
        known_transports.append(
            plateau_transport(
                [KNOWN],
                len(old_word),
                len(new_word),
                survivor_for_word(old_word),
                survivor_for_word(new_word),
            )
        )
    if known_schedule.startswith(KNOWN_FINAL):
        raise AssertionError("known state unexpectedly forced the final branch")

    payload: dict[str, Any] = {
        "status": "exact-plateau-transport-and-finite-census",
        "maximum_complexity": maximum_complexity,
        "transport_theorem": (
            "For nested depth-L and depth-(L+r) cylinders at fixed complexity, "
            "retain precisely residual minimizers congruent to the extension "
            "block modulo 4^r, then divide their residuals by 4^r. Zero penalty "
            "is equivalent to a nonempty filtered set."
        ),
        "exhaustive_small_transport_checks": transport_checks,
        "actual_return_transports": actual_rows,
        "known_counterexample": {
            "state_hex": hex(KNOWN),
            "forced_schedule": known_schedule,
            "two_zero_penalty_transports": known_transports,
            "third_return_possible": False,
            "reason": (
                "the required u at the next return is the depth-16 branch, which "
                "is invisible modulo 4^16; the state forces t there"
            ),
        },
        "frontier_census": frontier_plateau_census(
            maximum_complexity, schedule_cap
        ),
        "scientific_boundary": (
            "The transport theorem is all-depth exact. The absence of three-return "
            "candidates is finite through the configured complexity and does not "
            "prove the all-depth isolated-three-return lemma, phase-complexity "
            "divergence, exclusion of period two, or Rule 30 center nonperiodicity."
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
