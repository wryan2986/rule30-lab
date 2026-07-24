#!/usr/bin/env python3
"""Analyze exact one-pair lifts of period-two arithmetic witnesses.

For base depth L and phase a in {p,u}, the lift profile records the minimum
normalized word length needed to reach each of the four residues

    X_L + r * 4**L,  r in {0,1,2,3},

modulo 4**(L+1), where X_L is the actual zero-survivor residue.  Projection
shows that the minimum profile entry is kappa_a(L), while the coordinate
selected by the actual next survivor pair is kappa_a(L+1).

The default Python campaign is deliberately bounded.  The accompanying C++
analyzer provides the compact exact search through depth 22.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from array import array
from typing import Any

LETTERS = ("t", "p", "u")
PHASES = ("p", "u")
DEFAULT_MAXIMUM_BASE_DEPTH = 10
ABSOLUTE_MAXIMUM_BASE_DEPTH = 12

# Exact phase complexities already established by the directed-distance theorem.
KAPPA_P = (0, 1, 3, 7, 8, 8, 12, 13, 17, 17, 17, 21, 28, 30)
KAPPA_U = (0, 2, 2, 2, 7, 12, 14, 14, 14, 18, 19, 26, 27, 30)


def width_mask(width: int) -> int:
    if width < 0:
        raise ValueError("width must be nonnegative")
    return (1 << width) - 1 if width else 0


def forward_generator(name: str, state: int, width: int | None = None) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    stepped = state ^ ((state << 1) | (state << 2))
    if width is not None:
        stepped &= width_mask(width)
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError("unknown generator")


def inverse_t_mod(output: int, width: int) -> int:
    output &= width_mask(width)
    state = 0
    for position in range(width):
        previous = 0
        if position >= 1:
            previous |= (state >> (position - 1)) & 1
        if position >= 2:
            previous |= (state >> (position - 2)) & 1
        bit = ((output >> position) & 1) ^ previous
        state |= bit << position
    return state


def inverse_generator_mod(name: str, output: int, width: int) -> int:
    output &= width_mask(width)
    if name == "t":
        return inverse_t_mod(output, width)
    if name == "u":
        return inverse_t_mod(output ^ 1, width)
    if name == "p":
        recovered_low_bit = (output & 1) ^ 1
        adjusted = output ^ 1 ^ (2 if recovered_low_bit == 0 else 0)
        return inverse_t_mod(adjusted, width)
    raise ValueError("unknown generator")


def fringe_step(state: int) -> int:
    packed = 1 + 2 * state
    odd = packed ^ ((packed >> 1) | (packed >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def actual_driver(length: int) -> list[str]:
    state = 0
    result: list[str] = []
    for _ in range(length):
        result.append("u" if state & 3 == 0 else "t")
        state = fringe_step(state)
    return result


def backward_zero_branch(branch: str, successor: int, width: int) -> int:
    if branch not in ("t", "u"):
        raise ValueError("branch must be t or u")
    inner_width = width - 2
    state = inverse_generator_mod(branch, successor, inner_width)
    state = inverse_generator_mod("p", state, inner_width)
    return ((state << 2) | 3) & width_mask(width)


def actual_survivor_residue(depth: int) -> int:
    state = 0
    precision = 0
    for branch in reversed(actual_driver(depth)):
        precision += 2
        state = backward_zero_branch(branch, state, precision)
    return state


def actual_pair(depth_index: int) -> int:
    """Return pair digit at zero-based pair position depth_index."""
    return (actual_survivor_residue(depth_index + 1) >> (2 * depth_index)) & 3


def phase_lift_profile(base_depth: int, phase: str) -> tuple[int, int, int, int]:
    if not 1 <= base_depth <= ABSOLUTE_MAXIMUM_BASE_DEPTH:
        raise ValueError("base depth outside controlled range")
    if phase not in PHASES:
        raise ValueError("phase must be p or u")

    width = 2 * (base_depth + 1)
    state_count = 1 << width
    base = actual_survivor_residue(base_depth)
    targets = tuple(base + (digit << (2 * base_depth)) for digit in range(4))
    target_lookup = {target: digit for digit, target in enumerate(targets)}

    start = forward_generator(phase, 0, width)
    distances = bytearray(b"\xff") * state_count
    queue = array("I", [start])
    distances[start] = 0
    answers: list[int | None] = [None, None, None, None]
    if start in target_lookup:
        answers[target_lookup[start]] = 1
    remaining = sum(value is None for value in answers)

    head = 0
    while head < len(queue) and remaining:
        state = queue[head]
        head += 1
        next_distance = distances[state] + 1
        for letter in LETTERS:
            image = forward_generator(letter, state, width)
            if distances[image] != 255:
                continue
            distances[image] = next_distance
            queue.append(image)
            digit = target_lookup.get(image)
            if digit is not None and answers[digit] is None:
                answers[digit] = next_distance + 1
                remaining -= 1

    if remaining:
        raise AssertionError("positive generator graph failed to reach a lift")
    return tuple(int(value) for value in answers)  # type: ignore[arg-type]


def run_campaign(maximum_base_depth: int = DEFAULT_MAXIMUM_BASE_DEPTH) -> dict[str, Any]:
    if not 1 <= maximum_base_depth <= ABSOLUTE_MAXIMUM_BASE_DEPTH:
        raise ValueError("maximum base depth outside controlled range")

    rows: list[dict[str, Any]] = []
    for base_depth in range(1, maximum_base_depth + 1):
        digit = actual_pair(base_depth)
        profiles = {phase: phase_lift_profile(base_depth, phase) for phase in PHASES}
        for phase, profile in profiles.items():
            expected_current = (KAPPA_P if phase == "p" else KAPPA_U)[base_depth]
            expected_next = (KAPPA_P if phase == "p" else KAPPA_U)[base_depth + 1]
            if min(profile) != expected_current:
                raise AssertionError("projection minimum did not recover current complexity")
            if profile[digit] != expected_next:
                raise AssertionError("actual lift coordinate did not recover next complexity")
        rows.append(
            {
                "base_depth": base_depth,
                "actual_next_pair": digit,
                "p_profile": list(profiles["p"]),
                "u_profile": list(profiles["u"]),
                "p_jump_penalty": profiles["p"][digit] - min(profiles["p"]),
                "u_jump_penalty": profiles["u"][digit] - min(profiles["u"]),
            }
        )

    payload: dict[str, Any] = {
        "status": "finite-exhaustive",
        "maximum_base_depth": maximum_base_depth,
        "rows": rows,
        "theorem_checks": {
            "profile_minimum_equals_current_complexity": True,
            "actual_coordinate_equals_next_complexity": True,
            "plateau_iff_actual_digit_is_profile_minimizer": True,
        },
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--maximum-base-depth",
        type=int,
        default=DEFAULT_MAXIMUM_BASE_DEPTH,
    )
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_base_depth), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
