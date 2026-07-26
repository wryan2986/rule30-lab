#!/usr/bin/env python3
"""Dominant adjacent-level shadow paths for three-return survivor prefixes.

For phase a, let O_(a,k) be the exact ordinary frontier. For q in O_(a,k),
define the next-level fiber mask

    M_k(q) = {e in {0,1,2,3}: 4q+e in O_(a,k+1)}.

An adjacent pair (q,p), with q at level k and p at level k-1, is dominant when
M_k(q) is a subset of M_(k-1)(p). Then every common base-four digit available
to q is also available to p. Repeating this test along a cylinder gives an
exact finite certificate that a level-k prefix has a same-cylinder shadow at
level k-1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from itertools import product
from typing import Any

PHASES = ("p", "u")
GAPS = (2, 3, 4, 5)
FORBIDDEN = ("uu", "ttttt", "ututtu")
ALLOWED_MASKS = (0b0000, 0b0011, 0b1011, 0b1100, 0b1111)
DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 20
DEFAULT_SCHEDULE_CAP = 64


class DominantShadowLimitError(RuntimeError):
    """Raised before a controlled campaign exceeds its cap."""


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
    return tuple(sorted({forward_generator(g, state) for g in "tup"}))


def phase_start(phase: str) -> int:
    if phase == "p":
        return 3
    if phase == "u":
        return 1
    raise ValueError("phase must be p or u")


def expected_bits(phase: str, complexity: int) -> int:
    return 2 * complexity if phase == "p" else 2 * complexity - 1


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
    raise DominantShadowLimitError("forced schedule reached safety cap")


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


def build_levels(phase: str, maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {phase_start(phase)}]
    for _ in range(2, maximum_complexity + 1):
        levels.append(
            {child for state in levels[-1] for child in frontier_children(state)}
        )
    return levels


def fiber_mask(levels: list[set[int]], complexity: int, quotient: int) -> int:
    if complexity < 1 or complexity + 1 >= len(levels):
        raise ValueError("fiber level outside built frontier")
    next_level = levels[complexity + 1]
    mask = sum(
        1 << digit for digit in range(4) if 4 * quotient + digit in next_level
    )
    if mask not in ALLOWED_MASKS:
        raise AssertionError("fiber escaped five-mask alphabet")
    return mask


def dominant_path(
    levels: list[set[int]],
    complexity: int,
    current: int,
    shadow: int,
    depth: int,
) -> list[tuple[int, int, int]] | None:
    """Strip a common depth-d cylinder and certify fiber-mask dominance."""
    path: list[tuple[int, int, int]] = []
    for step in range(depth):
        digit = current & 3
        if shadow & 3 != digit:
            return None
        current_quotient = current >> 2
        shadow_quotient = shadow >> 2
        current_level = complexity - 1 - step
        if current_level < 2:
            return None
        current_mask = fiber_mask(levels, current_level, current_quotient)
        shadow_mask = fiber_mask(levels, current_level - 1, shadow_quotient)
        if current_mask & ~shadow_mask:
            return None
        path.append((current_mask, shadow_mask, digit))
        current, shadow = current_quotient, shadow_quotient
    return path


def mask_sequence(
    levels: list[set[int]], complexity: int, state: int, depth: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    masks: list[int] = []
    digits: list[int] = []
    for step in range(depth):
        digits.append(state & 3)
        quotient = state >> 2
        level = complexity - 1 - step
        if level < 1:
            raise ValueError("depth exceeds available complexity")
        masks.append(fiber_mask(levels, level, quotient))
        state = quotient
    return tuple(masks), tuple(digits)


def phase_campaign(
    phase: str, maximum_complexity: int, schedule_cap: int
) -> dict[str, Any]:
    levels = build_levels(phase, maximum_complexity)
    patterns = three_return_patterns()
    totals = Counter(
        outputs=sum(len(levels[k]) for k in range(1, maximum_complexity + 1))
    )
    totals["eligible_outputs"] = sum(
        1
        for k in range(1, maximum_complexity + 1)
        for state in levels[k]
        if state & 3 == 3
    )
    pair_counts: Counter[tuple[int, int]] = Counter()
    transition_counts: Counter[tuple[int, int, int]] = Counter()
    path_lengths: Counter[int] = Counter()
    examples: list[dict[str, Any]] = []

    for complexity in range(2, maximum_complexity + 1):
        occurrences: list[tuple[int, int, str, list[tuple[int, ...]]]] = []
        needed_depths: set[int] = set()
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
                if matches:
                    occurrences.append((current, cut, base, matches))
                    needed_depths.add(cut + 1)
        if not occurrences:
            continue

        shadow_indexes: dict[int, dict[int, dict[tuple[int, ...], int]]] = {}
        for depth in sorted(needed_depths):
            by_residue: dict[int, dict[tuple[int, ...], int]] = defaultdict(dict)
            modulus = 4**depth
            for shadow in sorted(levels[complexity - 1]):
                if shadow & 3 != 3:
                    continue
                masks, _ = mask_sequence(levels, complexity - 1, shadow, depth)
                residue = shadow % modulus
                by_residue[residue].setdefault(masks, shadow)
            shadow_indexes[depth] = by_residue

        for current, cut, base, matches in occurrences:
            depth = cut + 1
            modulus = 4**depth
            residue = current % modulus
            current_masks, current_digits = mask_sequence(
                levels, complexity, current, depth
            )
            chosen: tuple[int, tuple[int, ...]] | None = None
            for shadow_masks, shadow in shadow_indexes[depth].get(residue, {}).items():
                if all(
                    not (current_mask & ~shadow_mask)
                    for current_mask, shadow_mask in zip(
                        current_masks, shadow_masks
                    )
                ):
                    chosen = (shadow, shadow_masks)
                    break

            for gaps in matches:
                totals["occurrences"] += 1
                if cut > 0:
                    totals["positive_cut_occurrences"] += 1
                totals["maximum_cut"] = max(totals["maximum_cut"], cut)
                if chosen is None:
                    totals["violations"] += 1
                    if len(examples) < 8:
                        examples.append(
                            {
                                "kind": "violation",
                                "complexity": complexity,
                                "state_hex": hex(current),
                                "cut": cut,
                                "base": base,
                                "gaps": list(gaps),
                            }
                        )
                    continue

                shadow, shadow_masks = chosen
                totals["shadowed_occurrences"] += 1
                path_lengths[depth] += 1
                for current_mask, shadow_mask, digit in zip(
                    current_masks, shadow_masks, current_digits
                ):
                    pair_counts[(current_mask, shadow_mask)] += 1
                    transition_counts[(current_mask, shadow_mask, digit)] += 1
                if cut > 0 and len(examples) < 8:
                    examples.append(
                        {
                            "kind": "dominant-shadow",
                            "complexity": complexity,
                            "state_hex": hex(current),
                            "shadow_hex": hex(shadow),
                            "cut": cut,
                            "base": base,
                            "gaps": list(gaps),
                            "mask_path": [
                                [f"0b{a:04b}", f"0b{b:04b}", digit]
                                for a, b, digit in zip(
                                    current_masks, shadow_masks, current_digits
                                )
                            ],
                        }
                    )
        totals["levels_with_occurrences"] += 1

    return {
        "phase": phase,
        "totals": dict(totals),
        "dominant_mask_pairs": {
            f"0b{a:04b}/0b{b:04b}": count
            for (a, b), count in sorted(pair_counts.items())
        },
        "digit_transitions": {
            f"0b{a:04b}/0b{b:04b}/digit-{digit}": count
            for (a, b, digit), count in sorted(transition_counts.items())
        },
        "path_lengths": {
            str(length): count for length, count in sorted(path_lengths.items())
        },
        "examples": examples,
    }


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
    schedule_cap: int = DEFAULT_SCHEDULE_CAP,
) -> dict[str, Any]:
    if not 2 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise DominantShadowLimitError("maximum complexity outside controlled range")
    phases = {
        phase: phase_campaign(phase, maximum_complexity, schedule_cap)
        for phase in PHASES
    }
    combined: Counter[str] = Counter()
    pair_keys: set[str] = set()
    for phase in PHASES:
        combined.update(phases[phase]["totals"])
        pair_keys.update(phases[phase]["dominant_mask_pairs"])
    payload: dict[str, Any] = {
        "status": "exact-dominance-criterion-and-finite-shadow-transducer",
        "maximum_complexity": maximum_complexity,
        "schedule_cap": schedule_cap,
        "admissible_three_return_patterns": len(three_return_patterns()),
        "theorem": {
            "common_digit_simulation": (
                "If adjacent frontier states have current fiber mask contained "
                "in shadow fiber mask, every next base-four digit available to "
                "the current state is also available to the shadow state."
            ),
            "path_certificate": (
                "Repeating the mask-containment test while stripping a shared "
                "cylinder gives an exact certificate that the level-k state has "
                "a same-cylinder level-(k-1) shadow."
            ),
        },
        "phases": phases,
        "combined": dict(combined),
        "observed_pair_alphabet": sorted(pair_keys),
        "scientific_boundary": (
            "The common-digit simulation lemma is exact. Existence of a dominant "
            "shadow for every three-return occurrence is verified only through "
            "the configured complexity; it does not prove the all-depth shadow "
            "inclusion, phase-complexity divergence, exclusion of eventual period "
            "two, or Rule 30 center nonperiodicity."
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
    print(json.dumps(
        run_campaign(args.maximum_complexity, args.schedule_cap),
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
