#!/usr/bin/env python3
"""Classify exact phase penalties across two consecutive ``u`` returns.

For a locally admissible schedule prefix ending in ``u``, append two return
blocks with gaps r,s in {2,3,4,5}.  The two-return penalty is the increase in
minimum phase-witness complexity between the initial and final survivor
cylinders.  Projection makes it the sum of the two nonnegative single-return
penalties.

The bounded campaign is regression evidence for the accompanying all-depth
reduction.  It does not prove that every actual two-return penalty is positive.
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


class TwoReturnPenaltyLimitError(RuntimeError):
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
        state |= ((((output >> position) & 1) ^ previous) << position)
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
    def visit(prefix: str) -> Iterator[str]:
        if len(prefix) == length:
            if prefix.endswith("u"):
                yield prefix
            return
        for letter in ("t", "u"):
            candidate = prefix + letter
            if is_locally_admissible(candidate):
                yield from visit(candidate)

    if length > 0:
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
    return 1 + phase_distances(len(prefix), phase)[survivor_for_prefix(prefix)]


def return_extension(gap: int) -> str:
    if gap not in RETURN_GAPS:
        raise ValueError("gap must lie in 2..5")
    return "t" * (gap - 1) + "u"


def classify_gap_pair(
    first_gap: int,
    second_gap: int,
    phase: str,
    maximum_final_depth: int,
) -> dict[str, Any]:
    extension = return_extension(first_gap) + return_extension(second_gap)
    histogram: Counter[int] = Counter()
    candidates = 0
    zero_examples: list[dict[str, Any]] = []
    minimum_example: dict[str, Any] | None = None

    for base_depth in range(
        1, maximum_final_depth - first_gap - second_gap + 1
    ):
        for prefix in valid_prefixes_ending_u(base_depth):
            final_prefix = prefix + extension
            if not is_locally_admissible(final_prefix):
                continue
            middle_prefix = prefix + return_extension(first_gap)
            initial = phase_complexity(prefix, phase)
            middle = phase_complexity(middle_prefix, phase)
            final = phase_complexity(final_prefix, phase)
            first_penalty = middle - initial
            second_penalty = final - middle
            total_penalty = final - initial
            if first_penalty < 0 or second_penalty < 0:
                raise AssertionError("projection monotonicity failed")
            if total_penalty != first_penalty + second_penalty:
                raise AssertionError("two-return penalty failed to telescope")
            candidates += 1
            histogram[total_penalty] += 1
            row = {
                "base_depth": base_depth,
                "prefix": prefix,
                "middle_prefix": middle_prefix,
                "final_prefix": final_prefix,
                "first_penalty": first_penalty,
                "second_penalty": second_penalty,
                "total_penalty": total_penalty,
            }
            if total_penalty == 0 and len(zero_examples) < 4:
                zero_examples.append(row)
            if (
                minimum_example is None
                or total_penalty < minimum_example["total_penalty"]
            ):
                minimum_example = row

    if not candidates:
        return {
            "candidates": 0,
            "zero_penalty_count": 0,
            "minimum_penalty": None,
            "maximum_penalty": None,
            "histogram": {},
            "zero_examples": [],
            "minimum_example": None,
        }
    return {
        "candidates": candidates,
        "zero_penalty_count": histogram[0],
        "positive_penalty_count": candidates - histogram[0],
        "minimum_penalty": min(histogram),
        "maximum_penalty": max(histogram),
        "histogram": {str(key): histogram[key] for key in sorted(histogram)},
        "zero_examples": zero_examples,
        "minimum_example": minimum_example,
    }


def run_campaign(
    maximum_final_depth: int = DEFAULT_MAXIMUM_FINAL_DEPTH,
) -> dict[str, Any]:
    if not 6 <= maximum_final_depth <= ABSOLUTE_MAXIMUM_FINAL_DEPTH:
        raise TwoReturnPenaltyLimitError(
            "maximum final depth outside controlled range"
        )

    rows: dict[str, Any] = {}
    total_phase_cases = 0
    total_zero_cases = 0
    for first_gap in RETURN_GAPS:
        for second_gap in RETURN_GAPS:
            pair_key = f"{first_gap},{second_gap}"
            rows[pair_key] = {}
            for phase in PHASES:
                summary = classify_gap_pair(
                    first_gap, second_gap, phase, maximum_final_depth
                )
                rows[pair_key][phase] = summary
                total_phase_cases += summary["candidates"]
                total_zero_cases += summary["zero_penalty_count"]

    payload: dict[str, Any] = {
        "status": "finite-exhaustive",
        "maximum_final_depth": maximum_final_depth,
        "known_forbidden_factors": list(FORBIDDEN),
        "gap_pair_rows": rows,
        "totals": {
            "phase_gap_pair_cases": total_phase_cases,
            "zero_two_return_penalties": total_zero_cases,
        },
        "all_depth_reduction": {
            "identity": (
                "Delta_(a,j)=kappa_a(L_(j+2))-kappa_a(L_j)="
                "delta_(a,j)+delta_(a,j+1)"
            ),
            "criterion": (
                "if every sufficiently late two-return penalty is positive, "
                "then kappa_a(L_J) grows by at least floor((J-J0)/2)"
            ),
            "equivalent_form": (
                "it suffices to prove that zero single-return penalties cannot "
                "occur on two consecutive returns"
            ),
        },
        "scope_warning": (
            "the bounded campaign does not prove all-depth two-return positivity, "
            "does not exclude period two, and does not solve Rule 30 center "
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
