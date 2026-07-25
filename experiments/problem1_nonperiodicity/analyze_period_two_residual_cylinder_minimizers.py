#!/usr/bin/env python3
"""Exact residual-frontier factorization for phase survivor cylinders.

For phase a, complexity k, depth L, and residue X modulo 4**L, define

    C_(a,k)(X,L) = {x in O_(a,k): x == X (mod 4**L)}.

When k>L, projection by 2L bits injects this set into O_(a,k-L), and

    C_(a,k)(X,L)
      = {X + 4**L h : h in O_(a,k-L), X + 4**L h in O_(a,k)}.

The final membership condition is decided by the exact recursive lift criterion.
Reading the fixed base-four digits of X from high to low filters the residual
frontier without constructing the full complexity-k frontier.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from functools import lru_cache
from typing import Any

PHASES = ("p", "u")
CHILD_DIGIT_MASK = {0: 0b1011, 1: 0b1100, 2: 0b1110, 3: 0b0011}
DEFAULT_MAXIMUM_DEPTH = 10
ABSOLUTE_MAXIMUM_DEPTH = 12
DEFAULT_MAXIMUM_RESIDUAL = 13
ABSOLUTE_MAXIMUM_RESIDUAL = 16
EXPECTED = {
    1: {"p": 1, "u": 2}, 2: {"p": 3, "u": 2},
    3: {"p": 7, "u": 2}, 4: {"p": 8, "u": 7},
    5: {"p": 8, "u": 12}, 6: {"p": 12, "u": 14},
    7: {"p": 13, "u": 14}, 8: {"p": 17, "u": 14},
    9: {"p": 17, "u": 18}, 10: {"p": 17, "u": 19},
    11: {"p": 21, "u": 26}, 12: {"p": 28, "u": 27},
}
COUNTER_WORDS = {
    "w12": "tutututttutu",
    "w14": "tutututttututu",
    "w16": "tutututttutututu",
}
KNOWN_COUNTEREXAMPLE = 0x1BCD3A7B3FDFB


class ResidualCylinderLimitError(RuntimeError):
    """Raised before a controlled residual-frontier campaign exceeds its cap."""


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
    return tuple(sorted({forward_generator(name, state) for name in "tup"}))


def phase_start(phase: str) -> int:
    if phase == "p":
        return 3
    if phase == "u":
        return 1
    raise ValueError("phase must be p or u")


def expected_bit_length(phase: str, complexity: int) -> int:
    if complexity <= 0:
        raise ValueError("complexity must be positive")
    return 2 * complexity if phase == "p" else 2 * complexity - 1


def inverse_t(output: int) -> int | None:
    if output < 0:
        raise ValueError("output must be nonnegative")
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
    if quotient < 0 or parent_digit not in range(4):
        raise ValueError("invalid candidate-parent argument")
    name = "t" if parent_digit == 0 else "u" if parent_digit == 1 else "p"
    residual = inverse_generator(name, quotient)
    return None if residual is None else 4 * residual + parent_digit


def build_phase_levels(phase: str, maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {phase_start(phase)}]
    for _ in range(2, maximum_complexity + 1):
        levels.append({child for state in levels[-1] for child in frontier_children(state)})
    return levels


def make_member(levels: dict[str, list[set[int]]], base_cap: int):
    @lru_cache(maxsize=None)
    def member(phase: str, complexity: int, target: int) -> bool:
        if complexity < 1 or target < 0:
            return False
        if target.bit_length() != expected_bit_length(phase, complexity):
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
    mask = (1 << width) - 1 if width else 0
    output &= mask
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
    mask = (1 << width) - 1 if width else 0
    output &= mask
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


def cylinder_filter(
    *, phase: str, depth: int, complexity: int, residue: int,
    levels: dict[str, list[set[int]]], member,
) -> tuple[list[int], list[int]]:
    if depth <= 0 or complexity <= 0:
        raise ValueError("depth and complexity must be positive")
    if not 0 <= residue < 1 << (2 * depth):
        raise ValueError("residue outside the cylinder modulus")
    member.cache_clear()
    if complexity <= depth:
        states = [residue] if member(phase, complexity, residue) else []
        return states, [len(states)]
    residual_complexity = complexity - depth
    if residual_complexity >= len(levels[phase]):
        raise ResidualCylinderLimitError("residual complexity exceeds built frontier")
    current = sorted(levels[phase][residual_complexity])
    funnel = [len(current)]
    for index in range(depth - 1, -1, -1):
        digit = (residue >> (2 * index)) & 3
        next_complexity = residual_complexity + (depth - index)
        current = [
            4 * quotient + digit
            for quotient in current
            if member(phase, next_complexity, 4 * quotient + digit)
        ]
        funnel.append(len(current))
        if not current:
            break
    return current, funnel


def cylinder_kappa(
    *, phase: str, depth: int, residue: int, maximum_complexity: int,
    levels: dict[str, list[set[int]]], member,
) -> tuple[int, list[int], list[int]]:
    for complexity in range(1, maximum_complexity + 1):
        states, funnel = cylinder_filter(
            phase=phase, depth=depth, complexity=complexity, residue=residue,
            levels=levels, member=member,
        )
        if states:
            return complexity, states, funnel
    raise AssertionError("maximum complexity did not reach the cylinder")


def exhaustive_small_check(levels: dict[str, list[set[int]]], member) -> int:
    checks = 0
    for phase in PHASES:
        for complexity in range(1, 8):
            full = levels[phase][complexity]
            for depth in range(1, min(4, complexity + 1) + 1):
                modulus = 1 << (2 * depth)
                direct: dict[int, int] = {}
                for state in full:
                    direct[state % modulus] = direct.get(state % modulus, 0) + 1
                for residue in range(modulus):
                    states, _ = cylinder_filter(
                        phase=phase, depth=depth, complexity=complexity,
                        residue=residue, levels=levels, member=member,
                    )
                    if len(states) != direct.get(residue, 0):
                        raise AssertionError("residual factorization disagreed with direct frontier")
                    checks += 1
    return checks


def run_campaign(
    maximum_depth: int = DEFAULT_MAXIMUM_DEPTH,
    maximum_residual: int = DEFAULT_MAXIMUM_RESIDUAL,
) -> dict[str, Any]:
    if not 1 <= maximum_depth <= ABSOLUTE_MAXIMUM_DEPTH:
        raise ResidualCylinderLimitError("maximum depth outside controlled range")
    if not 1 <= maximum_residual <= ABSOLUTE_MAXIMUM_RESIDUAL:
        raise ResidualCylinderLimitError("maximum residual outside controlled range")
    levels = {
        phase: build_phase_levels(phase, maximum_residual) for phase in PHASES
    }
    member = make_member(levels, maximum_residual)
    small_checks = exhaustive_small_check(levels, member)

    rows: list[dict[str, Any]] = []
    for depth in range(1, maximum_depth + 1):
        residue = survivor_for_word(actual_driver(depth))
        phase_rows: dict[str, Any] = {}
        for phase in PHASES:
            expected = EXPECTED[depth][phase]
            complexity, states, funnel = cylinder_kappa(
                phase=phase, depth=depth, residue=residue,
                maximum_complexity=expected, levels=levels, member=member,
            )
            if complexity != expected:
                raise AssertionError("actual cylinder kappa mismatch")
            phase_rows[phase] = {
                "minimum_complexity": complexity,
                "residual_complexity": max(0, complexity - depth),
                "minimum_state_count": len(states),
                "funnel": funnel,
                "example_state_hex": hex(states[0]),
            }
        rows.append({
            "depth": depth,
            "actual_word": actual_driver(depth),
            "residue": residue,
            "residue_hex": hex(residue),
            "phases": phase_rows,
        })

    counterexamples: dict[str, Any] = {}
    for label, word in COUNTER_WORDS.items():
        depth = len(word)
        residue = survivor_for_word(word)
        states, funnel = cylinder_filter(
            phase="u", depth=depth, complexity=25, residue=residue,
            levels=levels, member=member,
        )
        if states != [KNOWN_COUNTEREXAMPLE]:
            raise AssertionError("counterexample cylinder was not uniquely minimized")
        counterexamples[label] = {
            "depth": depth,
            "word": word,
            "residue_hex": hex(residue),
            "complexity": 25,
            "unique_minimizer_hex": hex(states[0]),
            "funnel": funnel,
        }

    payload: dict[str, Any] = {
        "status": "exact-residual-factorization-and-controlled-minimization",
        "maximum_depth": maximum_depth,
        "maximum_residual_complexity": maximum_residual,
        "small_exhaustive_cylinder_checks": small_checks,
        "theorem": (
            "For k>L, the map x -> x>>(2L) injects the phase-cylinder "
            "intersection into O_(a,k-L), and the intersection is exactly the "
            "high-to-low recursive lift filter over the fixed base-four digits."
        ),
        "actual_rows": rows,
        "counterexample_cylinders": counterexamples,
        "scientific_boundary": (
            "The factorization decides finite cylinders and compresses their exact "
            "search. It does not prove unbounded actual phase complexity, recurring "
            "positive return penalties, exclusion of eventual period two, or Rule 30 "
            "center nonperiodicity."
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-depth", type=int, default=DEFAULT_MAXIMUM_DEPTH)
    parser.add_argument(
        "--maximum-residual", type=int, default=DEFAULT_MAXIMUM_RESIDUAL
    )
    args = parser.parse_args()
    print(json.dumps(
        run_campaign(args.maximum_depth, args.maximum_residual),
        indent=2, sort_keys=True,
    ))


if __name__ == "__main__":
    main()
