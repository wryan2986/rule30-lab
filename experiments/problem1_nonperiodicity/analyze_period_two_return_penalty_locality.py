#!/usr/bin/env python3
"""Classify local return-gap penalties for period-two phase witnesses.

For a finite branch prefix ``w`` ending in ``u`` and a return gap ``r``, append
``t**(r-1) u``.  The exact phase penalty is the increase in positive-generator
distance from the phase start to the corresponding schedule-survivor cylinder.

The finite campaign exhausts prefixes obeying the three proved fringe-language
exclusions.  It is regression evidence for a sharper all-depth lemma; it does
not itself prove that every non-two return has positive penalty.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from array import array
from collections import Counter
from functools import lru_cache
from typing import Any, Iterator

LETTERS = ("t", "p", "u")
PHASES = ("p", "u")
RETURN_GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
DEFAULT_MAXIMUM_FINAL_DEPTH = 9
ABSOLUTE_MAXIMUM_FINAL_DEPTH = 10

KAPPA_P = (
    0, 1, 3, 7, 8, 8, 12, 13, 17, 17, 17, 21, 28, 30, 33, 34, 36, 40,
    40, 42, 47, 49, 51,
)
KAPPA_U = (
    0, 2, 2, 2, 7, 12, 14, 14, 14, 18, 19, 26, 27, 30, 30, 30, 30, 40,
    42, 42, 49, 52, 52,
)


class ReturnPenaltyLimitError(RuntimeError):
    """Raised before a controlled exhaustive campaign exceeds its limit."""


def width_mask(width: int) -> int:
    if width < 0:
        raise ValueError("width must be nonnegative")
    return (1 << width) - 1 if width else 0


def forward_generator(name: str, state: int, width: int) -> int:
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
    raise ValueError("unknown inverse generator")


def backward_zero_branch(branch: str, successor: int, width: int) -> int:
    inner_width = width - 2
    state = inverse_generator_mod(branch, successor, inner_width)
    state = inverse_generator_mod("p", state, inner_width)
    return ((state << 2) | 3) & width_mask(width)


def survivor_for_prefix(prefix: str) -> int:
    state = 0
    precision = 0
    for branch in reversed(prefix):
        precision += 2
        state = backward_zero_branch(branch, state, precision)
    return state


def is_locally_admissible(word: str) -> bool:
    return not any(factor in word for factor in FORBIDDEN)


def valid_prefixes_ending_u(length: int) -> Iterator[str]:
    if length <= 0:
        return

    def visit(prefix: str) -> Iterator[str]:
        if len(prefix) == length:
            if prefix.endswith("u"):
                yield prefix
            return
        for letter in ("t", "u"):
            candidate = prefix + letter
            if is_locally_admissible(candidate):
                yield from visit(candidate)

    yield from visit("")


@lru_cache(maxsize=None)
def phase_distances(depth: int, phase: str) -> bytes:
    if depth <= 0:
        raise ValueError("depth must be positive")
    if phase not in PHASES:
        raise ValueError("phase must be p or u")
    width = 2 * depth
    state_count = 1 << width
    start = forward_generator(phase, 0, width)
    distances = bytearray(b"\xff") * state_count
    queue = array("I", [start])
    distances[start] = 0
    head = 0
    while head < len(queue):
        state = queue[head]
        head += 1
        next_distance = distances[state] + 1
        for letter in LETTERS:
            image = forward_generator(letter, state, width)
            if distances[image] == 255:
                distances[image] = next_distance
                queue.append(image)
    return bytes(distances)


def phase_complexity(prefix: str, phase: str) -> int:
    target = survivor_for_prefix(prefix)
    return 1 + phase_distances(len(prefix), phase)[target]


def classify_gap(gap: int, phase: str, maximum_final_depth: int) -> dict[str, Any]:
    extension = "t" * (gap - 1) + "u"
    histogram: Counter[int] = Counter()
    zero_examples: list[dict[str, Any]] = []
    positive_example: dict[str, Any] | None = None
    candidates = 0

    for base_depth in range(1, maximum_final_depth - gap + 1):
        for prefix in valid_prefixes_ending_u(base_depth):
            extended = prefix + extension
            if not is_locally_admissible(extended):
                continue
            current = phase_complexity(prefix, phase)
            following = phase_complexity(extended, phase)
            penalty = following - current
            if penalty < 0:
                raise AssertionError("projection monotonicity failed")
            candidates += 1
            histogram[penalty] += 1
            row = {
                "base_depth": base_depth,
                "prefix": prefix,
                "extended_prefix": extended,
                "current_complexity": current,
                "following_complexity": following,
                "penalty": penalty,
            }
            if penalty == 0 and len(zero_examples) < 4:
                zero_examples.append(row)
            if penalty > 0 and positive_example is None:
                positive_example = row

    return {
        "candidates": candidates,
        "zero_penalty_count": histogram[0],
        "positive_penalty_count": candidates - histogram[0],
        "minimum_penalty": min(histogram),
        "maximum_penalty": max(histogram),
        "histogram": {str(key): histogram[key] for key in sorted(histogram)},
        "zero_examples": zero_examples,
        "positive_example": positive_example,
    }


def actual_return_rows() -> list[dict[str, Any]]:
    positions = (0, 4, 6, 11, 13, 18, 20)
    rows = []
    for index, (left, right) in enumerate(zip(positions, positions[1:])):
        base_depth = left + 1
        final_depth = right + 1
        rows.append(
            {
                "return_index": index,
                "gap": right - left,
                "base_depth": base_depth,
                "final_depth": final_depth,
                "p_penalty": KAPPA_P[final_depth] - KAPPA_P[base_depth],
                "u_penalty": KAPPA_U[final_depth] - KAPPA_U[base_depth],
            }
        )
    return rows


def run_campaign(
    maximum_final_depth: int = DEFAULT_MAXIMUM_FINAL_DEPTH,
) -> dict[str, Any]:
    if not 6 <= maximum_final_depth <= ABSOLUTE_MAXIMUM_FINAL_DEPTH:
        raise ReturnPenaltyLimitError("maximum final depth outside controlled range")

    rows: dict[str, Any] = {}
    for gap in RETURN_GAPS:
        rows[str(gap)] = {
            phase: classify_gap(gap, phase, maximum_final_depth)
            for phase in PHASES
        }

    payload: dict[str, Any] = {
        "status": "finite-exhaustive",
        "maximum_final_depth": maximum_final_depth,
        "known_forbidden_factors": list(FORBIDDEN),
        "return_gap_rows": rows,
        "actual_exact_returns_through_depth_21": actual_return_rows(),
        "all_depth_reduction": {
            "conditional_lemma": (
                "if every locally admissible return of gap 3, 4, or 5 has positive "
                "phase penalty, then bounded phase complexity forces all sufficiently "
                "late return gaps to equal 2"
            ),
            "periodic_consequence": (
                "eventual gap 2 makes the branch schedule eventually repeat ut; the "
                "existing schedule-coding theorem excludes an ordinary finite survivor "
                "for every eventually periodic schedule"
            ),
        },
        "scope_warning": (
            "the bounded campaign does not prove all-depth positivity for gaps 3, 4, "
            "or 5, does not exclude period two, and does not solve Rule 30 center "
            "nonperiodicity"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--maximum-final-depth",
        type=int,
        default=DEFAULT_MAXIMUM_FINAL_DEPTH,
    )
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_final_depth), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
