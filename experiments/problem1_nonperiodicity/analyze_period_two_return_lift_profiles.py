#!/usr/bin/env python3
"""Analyze witness-complexity penalties across actual ``u`` return blocks.

At successive ``u`` positions n_j of the actual period-two fringe schedule, set
L_j=n_j+1.  For phase a and a base-4 block code c of length r_j=n_(j+1)-n_j,
this module computes the shortest phase-a witness reaching

    X_(L_j) + c * 4**L_j  (mod 4**L_(j+1)).

The minimum over c is kappa_a(L_j), while the actual block coordinate is
kappa_a(L_(j+1)).  Their difference is the exact return-block penalty.  These
penalties telescope along the return sequence.

The finite campaign does not prove that return penalties are positive
infinitely often and does not solve Rule 30 center nonperiodicity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from array import array
from collections import Counter
from typing import Any

LETTERS = ("t", "p", "u")
PHASES = ("p", "u")
DEFAULT_MAXIMUM_RETURNS = 2
ABSOLUTE_MAXIMUM_RETURNS = 3
ABSOLUTE_MAXIMUM_FINAL_DEPTH = 12

KAPPA_P = (
    0, 1, 3, 7, 8, 8, 12, 13, 17, 17, 17, 21, 28, 30, 33, 34, 36, 40,
    40, 42, 47, 49, 51,
)
KAPPA_U = (
    0, 2, 2, 2, 7, 12, 14, 14, 14, 18, 19, 26, 27, 30, 30, 30, 30, 40,
    42, 42, 49, 52, 52,
)


class ReturnLiftLimitError(RuntimeError):
    """Raised before an explicitly capped exhaustive campaign is exceeded."""


def width_mask(width: int) -> int:
    if width < 0:
        raise ValueError("width must be nonnegative")
    return (1 << width) - 1 if width else 0


def forward_generator(name: str, state: int, width: int) -> int:
    if state < 0 or width < 0:
        raise ValueError("state and width must be nonnegative")
    stepped = (state ^ ((state << 1) | (state << 2))) & width_mask(width)
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
    if length < 0:
        raise ValueError("length must be nonnegative")
    state = 0
    result: list[str] = []
    for _ in range(length):
        result.append("u" if state & 3 == 0 else "t")
        state = fringe_step(state)
    return result


def backward_zero_branch(branch: str, successor: int, width: int) -> int:
    if branch not in ("t", "u"):
        raise ValueError("branch must be t or u")
    if width < 2:
        raise ValueError("width must be at least two")
    inner_width = width - 2
    state = inverse_generator_mod(branch, successor, inner_width)
    state = inverse_generator_mod("p", state, inner_width)
    return ((state << 2) | 3) & width_mask(width)


def actual_survivor_residue(depth: int) -> int:
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    state = 0
    precision = 0
    for branch in reversed(actual_driver(depth)):
        precision += 2
        state = backward_zero_branch(branch, state, precision)
    return state


def actual_u_return_intervals(count: int) -> tuple[tuple[int, int], ...]:
    if count < 0:
        raise ValueError("count must be nonnegative")
    positions: list[int] = []
    state = 0
    position = 0
    while len(positions) < count + 1:
        if state & 3 == 0:
            positions.append(position)
        state = fringe_step(state)
        position += 1
    intervals = tuple(zip(positions, positions[1:]))
    for left, right in intervals:
        if right - left not in (2, 3, 4, 5):
            raise AssertionError("actual u return gap escaped the exact 2..5 bound")
    return intervals


def actual_block_code(base_depth: int, span: int) -> int:
    if base_depth < 0 or span <= 0:
        raise ValueError("base depth must be nonnegative and span positive")
    lower = actual_survivor_residue(base_depth)
    upper = actual_survivor_residue(base_depth + span)
    if upper & width_mask(2 * base_depth) != lower:
        raise AssertionError("survivor residues failed to project")
    return (upper - lower) >> (2 * base_depth)


def return_lift_profile(base_depth: int, span: int, phase: str) -> tuple[int, ...]:
    if phase not in PHASES:
        raise ValueError("phase must be p or u")
    final_depth = base_depth + span
    if final_depth > ABSOLUTE_MAXIMUM_FINAL_DEPTH:
        raise ReturnLiftLimitError("final profile depth exceeds controlled maximum")

    width = 2 * final_depth
    state_count = 1 << width
    block_count = 1 << (2 * span)
    base = actual_survivor_residue(base_depth)
    targets = tuple(base + (code << (2 * base_depth)) for code in range(block_count))
    target_lookup = {target: code for code, target in enumerate(targets)}

    start = forward_generator(phase, 0, width)
    distances = bytearray(b"\xff") * state_count
    queue = array("I", [start])
    distances[start] = 0
    answers: list[int | None] = [None] * block_count
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
            code = target_lookup.get(image)
            if code is not None and answers[code] is None:
                answers[code] = next_distance + 1
                remaining -= 1

    if remaining:
        raise AssertionError("positive generator graph failed to reach a block lift")
    return tuple(int(value) for value in answers)  # type: ignore[arg-type]


def summarize_profile(profile: tuple[int, ...], actual_code: int) -> dict[str, Any]:
    minimum = min(profile)
    histogram = Counter(profile)
    return {
        "minimum": minimum,
        "actual_length": profile[actual_code],
        "penalty": profile[actual_code] - minimum,
        "minimizer_count": sum(value == minimum for value in profile),
        "maximum": max(profile),
        "profile_sha256": hashlib.sha256(bytes(profile)).hexdigest(),
        "histogram": {str(key): histogram[key] for key in sorted(histogram)},
    }


def run_campaign(maximum_returns: int = DEFAULT_MAXIMUM_RETURNS) -> dict[str, Any]:
    if not 1 <= maximum_returns <= ABSOLUTE_MAXIMUM_RETURNS:
        raise ReturnLiftLimitError("return count outside controlled range")

    rows: list[dict[str, Any]] = []
    intervals = actual_u_return_intervals(maximum_returns)
    previous_final_depth: int | None = None
    cumulative = {phase: 0 for phase in PHASES}

    for return_index, (left, right) in enumerate(intervals):
        gap = right - left
        base_depth = left + 1
        final_depth = right + 1
        if previous_final_depth is not None and base_depth != previous_final_depth:
            raise AssertionError("return depth intervals failed to concatenate")
        previous_final_depth = final_depth

        actual_code = actual_block_code(base_depth, gap)
        actual_digits = [
            (actual_code >> (2 * index)) & 3 for index in range(gap)
        ]
        phase_rows: dict[str, Any] = {}
        for phase in PHASES:
            profile = return_lift_profile(base_depth, gap, phase)
            summary = summarize_profile(profile, actual_code)
            current = (KAPPA_P if phase == "p" else KAPPA_U)[base_depth]
            following = (KAPPA_P if phase == "p" else KAPPA_U)[final_depth]
            if summary["minimum"] != current:
                raise AssertionError("profile projection did not recover base complexity")
            if summary["actual_length"] != following:
                raise AssertionError("actual return coordinate did not recover final complexity")
            if summary["penalty"] != following - current:
                raise AssertionError("return penalty failed to equal complexity increment")
            cumulative[phase] += summary["penalty"]
            phase_rows[phase] = summary

        rows.append(
            {
                "return_index": return_index,
                "driver_start": left,
                "driver_end": right,
                "gap": gap,
                "base_depth": base_depth,
                "final_depth": final_depth,
                "actual_block_code": actual_code,
                "actual_block_digits_low_to_high": actual_digits,
                "by_phase": phase_rows,
            }
        )

    first_base_depth = rows[0]["base_depth"]
    last_final_depth = rows[-1]["final_depth"]
    for phase, sequence in (("p", KAPPA_P), ("u", KAPPA_U)):
        if cumulative[phase] != sequence[last_final_depth] - sequence[first_base_depth]:
            raise AssertionError("return penalties failed to telescope")

    payload: dict[str, Any] = {
        "status": "finite-exhaustive",
        "maximum_returns": maximum_returns,
        "rows": rows,
        "theorem_checks": {
            "return_depths": "L_j=n_j+1",
            "profile_minimum": "min_c Gamma_a(j,c)=kappa_a(L_j)",
            "actual_coordinate": "Gamma_a(j,c_j)=kappa_a(L_(j+1))",
            "penalty": "delta_(a,j)=kappa_a(L_(j+1))-kappa_a(L_j)",
            "telescoping": "kappa_a(L_J)=kappa_a(L_0)+sum_(j<J) delta_(a,j)",
            "boundedness": "kappa_a bounded iff all sufficiently late return penalties vanish",
        },
        "cumulative_penalties": cumulative,
        "scope_warning": (
            "finite return profiles do not prove positive penalties recur infinitely often, "
            "do not exclude period two, and do not solve Rule 30 center nonperiodicity"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--maximum-returns",
        type=int,
        default=DEFAULT_MAXIMUM_RETURNS,
    )
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_returns), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
