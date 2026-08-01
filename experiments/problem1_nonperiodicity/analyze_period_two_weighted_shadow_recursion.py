#!/usr/bin/env python3
"""Exact defect-weighted recursion for concrete dominant shadow beliefs."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import product
from typing import Any

PHASES = ("p", "u")
GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
ALLOWED_MASKS = (0b0000, 0b0011, 0b1011, 0b1100, 0b1111)
DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 18
DEFAULT_SCHEDULE_CAP = 64


class WeightedShadowLimitError(RuntimeError):
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
    return tuple(sorted({forward_generator(g, state) for g in "tup"}))


def phase_start(phase: str) -> int:
    if phase == "p":
        return 3
    if phase == "u":
        return 1
    raise ValueError(phase)


def expected_bits(phase: str, complexity: int) -> int:
    return 2 * complexity if phase == "p" else 2 * complexity - 1


def build_levels(phase: str, maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {phase_start(phase)}]
    for _ in range(2, maximum_complexity + 1):
        levels.append(
            {child for state in levels[-1] for child in frontier_children(state)}
        )
    return levels


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
    raise WeightedShadowLimitError("forced schedule reached safety cap")


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


def fiber_mask(levels: list[set[int]], complexity: int, quotient: int) -> int:
    mask = sum(
        1 << digit
        for digit in range(4)
        if 4 * quotient + digit in levels[complexity + 1]
    )
    if mask not in ALLOWED_MASKS:
        raise AssertionError("fiber escaped five-mask alphabet")
    return mask


def mask_sequence(
    levels: list[set[int]], complexity: int, state: int, depth: int
) -> tuple[int, ...]:
    masks: list[int] = []
    for step in range(depth):
        quotient = state >> 2
        level = complexity - 1 - step
        if level < 1:
            raise ValueError("depth exceeds complexity")
        masks.append(fiber_mask(levels, level, quotient))
        state = quotient
    return tuple(masks)


def dominates(current: tuple[int, ...], shadow: tuple[int, ...]) -> bool:
    return len(current) == len(shadow) and all(
        not (current_mask & ~shadow_mask)
        for current_mask, shadow_mask in zip(current, shadow)
    )


def defect_count(shadow: tuple[int, ...]) -> int:
    return sum(mask != 0b1111 for mask in shadow)


def weighted_shadow_belief_direct(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> dict[int, int]:
    if not 2 <= complexity < len(levels):
        raise ValueError("complexity outside built levels")
    if not 1 <= depth < complexity:
        raise ValueError("depth must satisfy 1 <= depth < complexity")
    modulus = 4**depth
    residue = current % modulus
    current_masks = mask_sequence(levels, complexity, current, depth)
    result: dict[int, int] = {}
    for shadow in levels[complexity - 1]:
        if shadow % modulus != residue:
            continue
        shadow_masks = mask_sequence(levels, complexity - 1, shadow, depth)
        if dominates(current_masks, shadow_masks):
            result[shadow] = defect_count(shadow_masks)
    return result


def weighted_shadow_belief_recursive(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> dict[int, int]:
    """Return every dominant concrete shadow endpoint with its exact defect cost."""
    if not 2 <= complexity < len(levels):
        raise ValueError("complexity outside built levels")
    if not 1 <= depth < complexity:
        raise ValueError("depth must satisfy 1 <= depth < complexity")
    digit = current & 3
    quotient = current >> 2
    current_mask = fiber_mask(levels, complexity - 1, quotient)
    if depth == 1:
        result: dict[int, int] = {}
        for shadow in levels[complexity - 1]:
            if shadow & 3 != digit:
                continue
            shadow_quotient = shadow >> 2
            shadow_mask = fiber_mask(levels, complexity - 2, shadow_quotient)
            if not (current_mask & ~shadow_mask):
                result[shadow] = int(shadow_mask != 0b1111)
        return result

    lower = weighted_shadow_belief_recursive(
        levels, complexity - 1, quotient, depth - 1
    )
    target_level = levels[complexity - 1]
    result: dict[int, int] = {}
    for shadow_quotient, lower_cost in lower.items():
        shadow = 4 * shadow_quotient + digit
        if shadow not in target_level:
            continue
        shadow_mask = fiber_mask(levels, complexity - 2, shadow_quotient)
        if current_mask & ~shadow_mask:
            continue
        result[shadow] = lower_cost + int(shadow_mask != 0b1111)
    return result


def minimum_defect_certificate(
    levels: list[set[int]], complexity: int, current: int, depth: int
) -> dict[str, Any] | None:
    belief = weighted_shadow_belief_recursive(levels, complexity, current, depth)
    if not belief:
        return None
    shadow, defects = min(belief.items(), key=lambda item: (item[1], item[0]))
    current_masks = mask_sequence(levels, complexity, current, depth)
    shadow_masks = mask_sequence(levels, complexity - 1, shadow, depth)
    digits_low_to_high = tuple((current >> (2 * index)) & 3 for index in range(depth))
    return {
        "shadow": shadow,
        "minimum_defects": defects,
        "current_masks": current_masks,
        "shadow_masks": shadow_masks,
        "seed_current": current >> (2 * (depth - 1)),
        "seed_shadow": shadow >> (2 * (depth - 1)),
        "seed_current_complexity": complexity - depth + 1,
        "lift_digits": tuple(reversed(digits_low_to_high[:-1])),
        "synchronized_defects": all(
            shadow_mask == 0b1111 or shadow_mask == current_mask
            for current_mask, shadow_mask in zip(current_masks, shadow_masks)
        ),
    }


def phase_campaign(
    phase: str, maximum_complexity: int, schedule_cap: int
) -> dict[str, Any]:
    levels = build_levels(phase, maximum_complexity)
    patterns = three_return_patterns()
    totals = Counter(
        outputs=sum(len(levels[k]) for k in range(1, maximum_complexity + 1))
    )
    minimum_defects = Counter()
    checked = 0
    examples: list[dict[str, Any]] = []
    for complexity in range(2, maximum_complexity + 1):
        for current in sorted(levels[complexity]):
            if current.bit_length() != expected_bits(phase, complexity):
                raise AssertionError("frontier bit-length law failed")
            if current & 3 != 3:
                continue
            schedule = forced_zero_schedule(current, schedule_cap)
            for cut in range(len(schedule) + 1):
                base = schedule[:cut]
                matches = [
                    gaps
                    for gaps, target, complete in patterns
                    if schedule[cut:].startswith(target)
                    and admissible(base + complete)
                ]
                if not matches:
                    continue
                depth = cut + 1
                direct = weighted_shadow_belief_direct(
                    levels, complexity, current, depth
                )
                recursive = weighted_shadow_belief_recursive(
                    levels, complexity, current, depth
                )
                if direct != recursive:
                    raise AssertionError("direct and recursive weighted beliefs disagree")
                checked += 1
                weight = len(matches)
                totals["occurrences"] += weight
                if not recursive:
                    totals["dominant_failures"] += weight
                    continue
                certificate = minimum_defect_certificate(
                    levels, complexity, current, depth
                )
                assert certificate is not None
                defects = certificate["minimum_defects"]
                minimum_defects[defects] += weight
                totals["dominant_occurrences"] += weight
                totals["maximum_minimum_defects"] = max(
                    totals["maximum_minimum_defects"], defects
                )
                if cut:
                    totals["positive_cut_occurrences"] += weight
                if len(examples) < 6 and cut:
                    examples.append(
                        {
                            "complexity": complexity,
                            "state_hex": hex(current),
                            "cut": cut,
                            "depth": depth,
                            "gaps": [list(gaps) for gaps in matches],
                            "shadow_hex": hex(certificate["shadow"]),
                            "minimum_defects": defects,
                            "seed_current_hex": hex(certificate["seed_current"]),
                            "seed_shadow_hex": hex(certificate["seed_shadow"]),
                            "lift_digits": list(certificate["lift_digits"]),
                            "synchronized_defects": certificate[
                                "synchronized_defects"
                            ],
                        }
                    )
    totals["weighted_cylinders_checked"] = checked
    return {
        "phase": phase,
        "totals": dict(totals),
        "minimum_defect_histogram": {
            str(defects): count
            for defects, count in sorted(minimum_defects.items())
        },
        "examples": examples,
    }


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
    schedule_cap: int = DEFAULT_SCHEDULE_CAP,
) -> dict[str, Any]:
    if not 2 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise WeightedShadowLimitError("maximum complexity outside controlled range")
    phases = {
        phase: phase_campaign(phase, maximum_complexity, schedule_cap)
        for phase in PHASES
    }
    fields = (
        "outputs",
        "occurrences",
        "positive_cut_occurrences",
        "dominant_occurrences",
        "dominant_failures",
        "weighted_cylinders_checked",
    )
    combined = {
        field: sum(phases[phase]["totals"].get(field, 0) for phase in PHASES)
        for field in fields
    }
    combined["maximum_minimum_defects"] = max(
        phases[phase]["totals"].get("maximum_minimum_defects", 0)
        for phase in PHASES
    )
    payload: dict[str, Any] = {
        "status": "exact-defect-weighted-concrete-shadow-recursion",
        "maximum_complexity": maximum_complexity,
        "schedule_cap": schedule_cap,
        "admissible_three_return_patterns": len(three_return_patterns()),
        "theorem": {
            "weighted_belief": (
                "A weighted belief retains each concrete dominant shadow endpoint "
                "together with the number of non-1111 shadow fibers on its path."
            ),
            "exact_recursion": (
                "For x=4q+d, recursively lift each weighted shadow p of q to "
                "4p+d exactly when that lift exists and the new current fiber is "
                "contained in the new shadow fiber; add one precisely when the "
                "new shadow fiber is not 1111."
            ),
            "seed_lift_decomposition": (
                "Every depth-L certificate is a depth-one seed pair followed by "
                "L-1 exact common-digit lifts, and its defect count is the sum of "
                "the local non-full shadow-fiber indicators."
            ),
        },
        "phases": phases,
        "combined": combined,
        "scientific_boundary": (
            "The weighted recursion and seed/lift decomposition are exact at every "
            "depth. Campaign nonemptiness and defect bounds remain finite and do "
            "not prove that three defects suffice at arbitrary complexity."
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
