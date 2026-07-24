#!/usr/bin/env python3
"""Compute exact actual period-two witness distances on finite 2-adic quotients.

For depth L, let X_L be the actual schedule survivor modulo 4**L.  A normalized
phase-p witness begins with p and therefore reaches arithmetic state 3 after its
first letter; a phase-u witness reaches state 1.  The remaining witness length
is the directed positive-generator distance from 3 or 1 to X_L modulo 4**L.

A complete reverse ball around X_L together with a complete forward BFS from a
phase start gives an exact bidirectional certificate.  The Python campaign is
capped at depth 12.  The companion C++ analyzer extends the same proof through
depth 20 without enumerating the full quotient.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any

LETTERS = ("t", "p", "u")
PHASE_START = {"p": 3, "u": 1}
DEFAULT_MAXIMUM_DEPTH = 12
ABSOLUTE_MAXIMUM_DEPTH = 12
EXPECTED_PHASE_DISTANCES = {
    1: {"p": 1, "u": 2},
    2: {"p": 3, "u": 2},
    3: {"p": 7, "u": 2},
    4: {"p": 8, "u": 7},
    5: {"p": 8, "u": 12},
    6: {"p": 12, "u": 14},
    7: {"p": 13, "u": 14},
    8: {"p": 17, "u": 14},
    9: {"p": 17, "u": 18},
    10: {"p": 17, "u": 19},
    11: {"p": 21, "u": 26},
    12: {"p": 28, "u": 27},
}


def width_mask(width: int) -> int:
    if width < 0:
        raise ValueError("width must be nonnegative")
    return (1 << width) - 1 if width else 0


def forward_t(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    return state ^ ((state << 1) | (state << 2))


def forward_generator(name: str, state: int, width: int | None = None) -> int:
    stepped = forward_t(state)
    if name == "t":
        result = stepped
    elif name == "u":
        result = stepped ^ 1
    elif name == "p":
        result = stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    else:
        raise ValueError("unknown generator")
    return result if width is None else result & width_mask(width)


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


def actual_driver(length: int) -> tuple[str, ...]:
    if length < 0:
        raise ValueError("length must be nonnegative")
    state = 0
    result: list[str] = []
    for _ in range(length):
        result.append("u" if state & 3 == 0 else "t")
        state = fringe_step(state)
    return tuple(result)


def backward_zero_branch(branch: str, successor: int, width: int) -> int:
    if width < 2:
        raise ValueError("zero branch needs at least two bits")
    inner_width = width - 2
    state = inverse_generator_mod(branch, successor, inner_width)
    state = inverse_generator_mod("p", state, inner_width)
    return ((state << 2) | 3) & width_mask(width)


def actual_survivor_residue(depth: int) -> int:
    if depth <= 0:
        raise ValueError("depth must be positive")
    state = 0
    precision = 0
    for branch in reversed(actual_driver(depth)):
        precision += 2
        state = backward_zero_branch(branch, state, precision)
    return state


def reverse_ball(target: int, width: int, maximum_distance: int) -> dict[int, int]:
    distances = {target: 0}
    frontier = [target]
    for distance in range(maximum_distance):
        next_frontier: list[int] = []
        for image in frontier:
            for letter in LETTERS:
                source = inverse_generator_mod(letter, image, width)
                if source not in distances:
                    distances[source] = distance + 1
                    next_frontier.append(source)
        frontier = next_frontier
    return distances


def phase_distance(
    *, depth: int, phase: str, reverse_distances: dict[int, int], reverse_depth: int
) -> tuple[int, dict[str, int]]:
    if phase not in PHASE_START:
        raise ValueError("phase must be p or u")
    width = 2 * depth
    start = PHASE_START[phase]
    distances = {start: 0}
    frontier = [start]
    best: int | None = None
    forward_depth = 0
    while frontier:
        for state in frontier:
            reverse_distance = reverse_distances.get(state)
            if reverse_distance is not None:
                candidate = 1 + forward_depth + reverse_distance
                best = candidate if best is None else min(best, candidate)
        if best is not None and forward_depth >= best - 1 - reverse_depth:
            break
        next_frontier: list[int] = []
        for state in frontier:
            for letter in LETTERS:
                image = forward_generator(letter, state, width)
                if image not in distances:
                    distances[image] = forward_depth + 1
                    next_frontier.append(image)
        frontier = next_frontier
        forward_depth += 1
    if best is None:
        raise AssertionError("configured reverse depth did not meet the forward search")
    return best, {
        "reverse_states": len(reverse_distances),
        "forward_states": len(distances),
        "last_forward_depth": forward_depth,
    }


def depth_row(depth: int) -> dict[str, Any]:
    reverse_depth = depth + 2
    width = 2 * depth
    target = actual_survivor_residue(depth)
    reverse_distances = reverse_ball(target, width, reverse_depth)
    by_phase: dict[str, Any] = {}
    for phase in PHASE_START:
        distance, diagnostics = phase_distance(
            depth=depth,
            phase=phase,
            reverse_distances=reverse_distances,
            reverse_depth=reverse_depth,
        )
        by_phase[phase] = {"minimum_length": distance, **diagnostics}
    expected = EXPECTED_PHASE_DISTANCES[depth]
    observed = {phase: by_phase[phase]["minimum_length"] for phase in by_phase}
    if observed != expected:
        raise AssertionError((depth, observed, expected))
    return {
        "depth": depth,
        "width_bits": width,
        "target_residue": target,
        "target_hex": hex(target),
        "reverse_depth": reverse_depth,
        "by_phase": by_phase,
        "minimum_length": min(observed.values()),
    }


def run_campaign(maximum_depth: int = DEFAULT_MAXIMUM_DEPTH) -> dict[str, Any]:
    if not 1 <= maximum_depth <= ABSOLUTE_MAXIMUM_DEPTH:
        raise ValueError("depth outside Python campaign cap")
    rows = [depth_row(depth) for depth in range(1, maximum_depth + 1)]
    for phase in PHASE_START:
        values = [row["by_phase"][phase]["minimum_length"] for row in rows]
        if values != sorted(values):
            raise AssertionError("phase witness distance decreased")
    payload: dict[str, Any] = {
        "maximum_depth": maximum_depth,
        "rows": rows,
        "exact_identity": (
            "kappa_p(L)=1+d_L(3,X_L) and kappa_u(L)=1+d_L(1,X_L), "
            "where d_L is positive-generator distance modulo 4^L"
        ),
        "cpp_extension": "exact sparse bidirectional distances through depth 20",
        "scope_warning": (
            "finite quotient distances do not prove divergence on the infinite actual schedule"
        ),
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-actual-witness-distance-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-depth", type=int, default=DEFAULT_MAXIMUM_DEPTH)
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_depth), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
