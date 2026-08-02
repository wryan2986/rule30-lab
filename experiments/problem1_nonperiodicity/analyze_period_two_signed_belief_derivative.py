#!/usr/bin/env python3
"""Signed defect mass and branching derivatives for concrete shadow beliefs."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any

DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 18
SCHEDULE_CAP = 64
MASK_ALPHABET = (0b0000, 0b0011, 0b1011, 0b1100, 0b1111)
RELEVANT_CURRENT_MASKS = (0b0011, 0b1011, 0b1100, 0b1111)


class SignedBeliefLimitError(RuntimeError):
    pass


def forward_generator(name: str, state: int) -> int:
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError(name)


def frontier_children(state: int) -> tuple[int, ...]:
    return tuple(sorted({forward_generator(name, state) for name in "tup"}))


def build_levels(maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {1}]
    for _ in range(2, maximum_complexity + 1):
        levels.append(
            {child for state in levels[-1] for child in frontier_children(state)}
        )
    return levels


def fiber_mask(levels: list[set[int]], complexity: int, quotient: int) -> int:
    mask = sum(
        1 << digit
        for digit in range(4)
        if 4 * quotient + digit in levels[complexity + 1]
    )
    if mask not in MASK_ALPHABET:
        raise AssertionError("fiber escaped the five-mask alphabet")
    return mask


def mask_sequence(
    levels: list[set[int]], complexity: int, state: int, depth: int
) -> tuple[int, ...]:
    result: list[int] = []
    for step in range(depth):
        state >>= 2
        result.append(fiber_mask(levels, complexity - 1 - step, state))
    return tuple(result)


def forced_zero_schedule(state: int, cap: int = SCHEDULE_CAP) -> str:
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
    raise SignedBeliefLimitError("forced schedule reached safety cap")


def admissible(word: str) -> bool:
    return all(factor not in word for factor in ("uu", "ttttt", "ututtu"))


def dominates(current: tuple[int, ...], shadow: tuple[int, ...]) -> bool:
    return all(
        not (current_mask & ~shadow_mask)
        for current_mask, shadow_mask in zip(current, shadow)
    )


def synchronized_or_full(
    current: tuple[int, ...], shadow: tuple[int, ...]
) -> bool:
    return all(
        shadow_mask == 0b1111 or shadow_mask == current_mask
        for current_mask, shadow_mask in zip(current, shadow)
    )


def defect_count(shadow: tuple[int, ...]) -> int:
    return sum(mask != 0b1111 for mask in shadow)


def local_signed_factor(current_mask: int, shadow_mask: int) -> int:
    """Return the local contribution to P(-1), including dominance rejection."""
    if current_mask & ~shadow_mask:
        return 0
    return 1 if shadow_mask == 0b1111 else -1


def local_branching_derivative(current_mask: int, shadow_mask: int) -> int:
    """Express the signed factor through one missing sibling indicator."""
    if current_mask & ~shadow_mask:
        return 0
    if current_mask == 0b1111:
        return int(shadow_mask == 0b1111)
    if current_mask in (0b0011, 0b1011):
        return 2 * ((shadow_mask >> 2) & 1) - 1
    if current_mask == 0b1100:
        return 2 * (shadow_mask & 1) - 1
    raise ValueError("branching derivative excludes current mask 0000")


def branching_path_weight(
    current: tuple[int, ...], shadow: tuple[int, ...]
) -> int:
    result = 1
    for current_mask, shadow_mask in zip(current, shadow):
        result *= local_branching_derivative(current_mask, shadow_mask)
    return result


def concrete_belief(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> tuple[tuple[int, ...], list[tuple[int, int, tuple[int, ...]]], int]:
    modulus = 4**depth
    residue = current % modulus
    current_masks = mask_sequence(levels, complexity, current, depth)
    rows: list[tuple[int, int, tuple[int, ...]]] = []
    same_cylinder = 0
    for shadow in levels[complexity - 1]:
        if shadow % modulus != residue:
            continue
        same_cylinder += 1
        shadow_masks = mask_sequence(levels, complexity - 1, shadow, depth)
        if not dominates(current_masks, shadow_masks):
            continue
        rows.append((shadow, defect_count(shadow_masks), shadow_masks))
    rows.sort()
    return current_masks, rows, same_cylinder


def signed_mass(rows: list[tuple[int, int, tuple[int, ...]]]) -> int:
    return sum(-1 if defects & 1 else 1 for _, defects, _ in rows)


def gap_222_occurrences(
    levels: list[set[int]], maximum_complexity: int
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for complexity in range(2, maximum_complexity + 1):
        for current in sorted(levels[complexity]):
            if current & 3 != 3:
                continue
            schedule = forced_zero_schedule(current)
            for cut in range(len(schedule) + 1):
                if schedule[cut : cut + 6] != "ututut":
                    continue
                if not admissible(schedule[:cut] + "utututu"):
                    continue
                depth = cut + 1
                current_masks, belief, same_cylinder = concrete_belief(
                    levels, complexity, current, depth
                )
                if any(mask not in RELEVANT_CURRENT_MASKS for mask in current_masks):
                    raise AssertionError("relevant path acquired current mask 0000")
                synchronized_failures = sum(
                    not synchronized_or_full(current_masks, shadow_masks)
                    for _, _, shadow_masks in belief
                )
                derivative_disagreements = sum(
                    branching_path_weight(current_masks, shadow_masks)
                    != (-1 if defects & 1 else 1)
                    for _, defects, shadow_masks in belief
                )
                histogram = Counter(defects for _, defects, _ in belief)
                mass = signed_mass(belief)
                result.append(
                    {
                        "complexity": complexity,
                        "state_hex": hex(current),
                        "cut": cut,
                        "depth": depth,
                        "same_cylinder": same_cylinder,
                        "dominant_shadows": len(belief),
                        "budget_three_shadows": sum(
                            defects <= 3 for _, defects, _ in belief
                        ),
                        "minimum_defect": min(
                            (defects for _, defects, _ in belief), default=None
                        ),
                        "signed_mass": mass,
                        "current_masks": [f"{mask:04b}" for mask in current_masks],
                        "defect_histogram": {
                            str(key): value for key, value in sorted(histogram.items())
                        },
                        "synchronized_failures": synchronized_failures,
                        "derivative_disagreements": derivative_disagreements,
                    }
                )
    return result


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
) -> dict[str, Any]:
    if not 5 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise SignedBeliefLimitError("maximum complexity outside controlled range")

    for current_mask in RELEVANT_CURRENT_MASKS:
        for shadow_mask in MASK_ALPHABET:
            if local_signed_factor(current_mask, shadow_mask) != (
                local_branching_derivative(current_mask, shadow_mask)
            ):
                raise AssertionError("local branching derivative identity failed")

    levels = build_levels(maximum_complexity)
    rows = gap_222_occurrences(levels, maximum_complexity)
    if not rows:
        raise AssertionError("controlled campaign found no gap-222 occurrences")

    cancellation_masks, cancellation_belief, _ = concrete_belief(
        levels, 5, 0x198, 1
    )
    cancellation_histogram = Counter(
        defects for _, defects, _ in cancellation_belief
    )
    cancellation_mass = signed_mass(cancellation_belief)

    minimum_defects = Counter(row["minimum_defect"] for row in rows)
    payload: dict[str, Any] = {
        "status": "exact-signed-belief-branching-derivative-and-finite-nonvanishing",
        "phase": "u",
        "maximum_complexity": maximum_complexity,
        "outputs_built": sum(
            len(levels[complexity])
            for complexity in range(1, maximum_complexity + 1)
        ),
        "gap_222_occurrences": len(rows),
        "dominant_failures": sum(row["dominant_shadows"] == 0 for row in rows),
        "synchronized_failures": sum(
            row["synchronized_failures"] for row in rows
        ),
        "derivative_disagreements": sum(
            row["derivative_disagreements"] for row in rows
        ),
        "signed_zero_cylinders": sum(row["signed_mass"] == 0 for row in rows),
        "negative_signed_cylinders": sum(row["signed_mass"] < 0 for row in rows),
        "majority_failures": sum(
            2 * row["dominant_shadows"] < row["same_cylinder"] for row in rows
        ),
        "minimum_absolute_signed_mass": min(
            abs(row["signed_mass"]) for row in rows
        ),
        "minimum_budget_three_count": min(
            row["budget_three_shadows"] for row in rows
        ),
        "minimum_defect_histogram": {
            str(key): value for key, value in sorted(minimum_defects.items())
        },
        "theorem": {
            "defect_polynomial": (
                "For a concrete dominant shadow belief, P(z) is the sum of "
                "z raised to the number of non-full shadow fibers."
            ),
            "signed_mass": (
                "P(-1) is the sum over same-cylinder shadow endpoints of the "
                "product of local signed dominance factors. Nonzero P(-1) "
                "therefore certifies a nonempty concrete belief."
            ),
            "branching_derivative": (
                "On every relevant nonzero current mask, the local signed factor "
                "is exactly a Rademacher difference determined by one missing "
                "sibling child: digit 2 for masks 0011/1011 and digit 0 for "
                "mask 1100."
            ),
        },
        "nongap_cancellation": {
            "complexity": 5,
            "state_hex": "0x198",
            "depth": 1,
            "current_masks": [f"{mask:04b}" for mask in cancellation_masks],
            "defect_histogram": {
                str(key): value
                for key, value in sorted(cancellation_histogram.items())
            },
            "signed_mass": cancellation_mass,
            "conclusion": (
                "Signed nonvanishing is not universal; a proof must use the "
                "gap-return schedule rather than only the five-mask alphabet."
            ),
        },
        "examples": sorted(
            rows,
            key=lambda row: (
                abs(row["signed_mass"]),
                row["complexity"],
                row["state_hex"],
            ),
        )[:6],
        "scientific_boundary": (
            "The polynomial identity, branching-derivative identity, and "
            "nonzero-implies-nonempty implication are exact. Nonvanishing and "
            "the defect bounds are finite observations through the configured "
            "complexity and do not prove the all-depth adjacent-shadow inclusion."
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
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_complexity), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
