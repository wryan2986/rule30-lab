#!/usr/bin/env python3
"""Exact recursive base-four lift criterion for ordinary phase frontiers.

For phase a in {p,u}, let O_(a,k) be the distinct ordinary outputs at
complexity k. If a target at level k+1 is y=4h+e, then its possible level-k
parents are determined by the low digit d of the parent and the partial inverse
of t, u, or p applied to h. This gives an exact recursive membership test that
does not enumerate the complete frontier.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from typing import Any

PHASES = ("p", "u")
DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 20
KNOWN_COUNTEREXAMPLE = 0x1BCD3A7B3FDFB
CHILD_DIGIT_MASK = {
    0: 0b1011,
    1: 0b1100,
    2: 0b1110,
    3: 0b0011,
}
ALLOWED_FIBER_MASKS = (0b0000, 0b0011, 0b1011, 0b1100, 0b1111)


class LiftRecursionLimitError(RuntimeError):
    """Raised before a controlled exhaustive campaign exceeds its cap."""


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
    """Return the unique exact nonnegative t-preimage, or None."""
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
        bit = ((output >> position) & 1) ^ lower
        state |= bit << position
    return state if forward_generator("t", state) == output else None


def inverse_generator(name: str, output: int) -> int | None:
    if output < 0:
        raise ValueError("output must be nonnegative")
    if name == "t":
        return inverse_t(output)
    if name == "u":
        state = inverse_t(output ^ 1)
    elif name == "p":
        recovered_low_bit = (output & 1) ^ 1
        adjusted = output ^ 1 ^ (2 if recovered_low_bit == 0 else 0)
        state = inverse_t(adjusted)
    else:
        raise ValueError("unknown generator")
    if state is None or forward_generator(name, state) != output:
        return None
    return state


def candidate_parent(quotient: int, parent_digit: int) -> int | None:
    if quotient < 0 or parent_digit not in range(4):
        raise ValueError("invalid candidate-parent argument")
    generator = "t" if parent_digit == 0 else "u" if parent_digit == 1 else "p"
    residual = inverse_generator(generator, quotient)
    return None if residual is None else 4 * residual + parent_digit


def predicted_fiber_mask(current: set[int], quotient: int) -> tuple[int, int]:
    predecessor_mask = 0
    fiber_mask = 0
    for digit in range(4):
        parent = candidate_parent(quotient, digit)
        if parent is not None and parent in current:
            predecessor_mask |= 1 << digit
            fiber_mask |= CHILD_DIGIT_MASK[digit]
    if predecessor_mask & 0b0100 and not predecessor_mask & 0b1000:
        raise AssertionError("residue-two predecessor lacked its residue-three mate")
    if fiber_mask not in ALLOWED_FIBER_MASKS:
        raise AssertionError("fiber escaped the five-mask alphabet")
    return predecessor_mask, fiber_mask


def actual_fiber_mask(next_level: set[int], quotient: int) -> int:
    return sum(1 << digit for digit in range(4) if 4 * quotient + digit in next_level)


def enumerate_phase(phase: str, maximum_complexity: int) -> dict[str, Any]:
    current = {phase_start(phase)}
    levels: list[dict[str, Any]] = []
    total_outputs = 0
    total_quotients = 0
    total_candidate_checks = 0
    total_mask_counts: Counter[int] = Counter()
    total_predecessor_counts: Counter[int] = Counter()

    for complexity in range(1, maximum_complexity + 1):
        expected = expected_bit_length(phase, complexity)
        if any(state.bit_length() != expected for state in current):
            raise AssertionError("frontier bit-length law failed")
        total_outputs += len(current)
        if complexity == maximum_complexity:
            levels.append({"complexity": complexity, "outputs": len(current)})
            break

        next_level = {child for state in current for child in frontier_children(state)}
        mask_counts: Counter[int] = Counter()
        predecessor_counts: Counter[int] = Counter()
        uncovered = 0
        for quotient in current:
            predecessor_mask, predicted = predicted_fiber_mask(current, quotient)
            actual = actual_fiber_mask(next_level, quotient)
            if predicted != actual:
                raise AssertionError("exact lift recursion failed")
            mask_counts[actual] += 1
            predecessor_counts[predecessor_mask] += 1
            uncovered += actual == 0
            total_quotients += 1
            total_candidate_checks += 4
        total_mask_counts.update(mask_counts)
        total_predecessor_counts.update(predecessor_counts)
        levels.append(
            {
                "complexity": complexity,
                "outputs": len(current),
                "next_outputs": len(next_level),
                "uncovered_quotients": uncovered,
                "fiber_masks": {
                    f"0b{mask:04b}": count for mask, count in sorted(mask_counts.items())
                },
            }
        )
        current = next_level

    return {
        "phase": phase,
        "levels": levels,
        "outputs_checked": total_outputs,
        "quotients_checked": total_quotients,
        "candidate_parent_checks": total_candidate_checks,
        "fiber_mask_totals": {
            f"0b{mask:04b}": count for mask, count in sorted(total_mask_counts.items())
        },
        "predecessor_mask_totals": {
            f"0b{mask:04b}": count
            for mask, count in sorted(total_predecessor_counts.items())
        },
    }


@lru_cache(maxsize=None)
def frontier_member(phase: str, complexity: int, target: int) -> bool:
    """Decide exact frontier membership by recursive lift inversion."""
    if complexity < 1 or target < 0:
        return False
    if target.bit_length() != expected_bit_length(phase, complexity):
        return False
    if complexity == 1:
        return target == phase_start(phase)

    quotient, digit = divmod(target, 4)
    for parent_digit in range(4):
        if not (CHILD_DIGIT_MASK[parent_digit] >> digit) & 1:
            continue
        parent = candidate_parent(quotient, parent_digit)
        if parent is not None and frontier_member(phase, complexity - 1, parent):
            return True
    return False


@lru_cache(maxsize=None)
def frontier_witness(phase: str, complexity: int, target: int) -> str | None:
    if not frontier_member(phase, complexity, target):
        return None
    if complexity == 1:
        return phase

    quotient, digit = divmod(target, 4)
    for parent_digit in range(4):
        if not (CHILD_DIGIT_MASK[parent_digit] >> digit) & 1:
            continue
        parent = candidate_parent(quotient, parent_digit)
        if parent is None or not frontier_member(phase, complexity - 1, parent):
            continue
        prefix = frontier_witness(phase, complexity - 1, parent)
        if prefix is None:
            continue
        for generator in "tup":
            if forward_generator(generator, parent) == target:
                return prefix + generator
    raise AssertionError("membership had no generator witness")


def apply_word(word: str) -> int:
    if not word or word[0] not in "pu":
        raise ValueError("word must begin with phase p or u")
    state = phase_start(word[0])
    for generator in word[1:]:
        state = forward_generator(generator, state)
    return state


def strict_examples() -> dict[str, Any]:
    examples = {
        "phase_p": {"phase": "p", "complexity": 2, "quotient": 12},
        "phase_u": {"phase": "u", "complexity": 3, "quotient": 26},
    }
    for row in examples.values():
        phase = row["phase"]
        complexity = row["complexity"]
        current = {phase_start(phase)}
        for _ in range(1, complexity):
            current = {child for state in current for child in frontier_children(state)}
        next_level = {child for state in current for child in frontier_children(state)}
        predecessor, predicted = predicted_fiber_mask(current, row["quotient"])
        actual = actual_fiber_mask(next_level, row["quotient"])
        if predicted != actual:
            raise AssertionError("strict example recursion mismatch")
        row["predecessor_mask"] = f"0b{predecessor:04b}"
        row["fiber_mask"] = f"0b{actual:04b}"
        row["lifts"] = [
            4 * row["quotient"] + digit
            for digit in range(4)
            if (actual >> digit) & 1
        ]
    return examples


def run_campaign(maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY) -> dict[str, Any]:
    if not 2 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise LiftRecursionLimitError("maximum complexity outside controlled range")

    phase_rows = {
        phase: enumerate_phase(phase, maximum_complexity) for phase in PHASES
    }
    frontier_member.cache_clear()
    frontier_witness.cache_clear()
    if not frontier_member("u", 25, KNOWN_COUNTEREXAMPLE):
        raise AssertionError("recursive criterion missed known counterexample")
    witness = frontier_witness("u", 25, KNOWN_COUNTEREXAMPLE)
    if witness is None or len(witness) != 25 or apply_word(witness) != KNOWN_COUNTEREXAMPLE:
        raise AssertionError("recursive counterexample witness failed")

    payload: dict[str, Any] = {
        "status": "exact-recursive-membership-and-finite-exhaustion",
        "maximum_complexity": maximum_complexity,
        "theorem": {
            "membership": (
                "4h+e lies in O_(a,k+1) iff at least one exact candidate parent "
                "selected by the partial inverses of t,u,p lies in O_(a,k) and "
                "its parent-digit contribution contains e"
            ),
            "child_digit_masks": {
                str(digit): f"0b{mask:04b}"
                for digit, mask in CHILD_DIGIT_MASK.items()
            },
            "fiber_alphabet": [f"0b{mask:04b}" for mask in ALLOWED_FIBER_MASKS],
        },
        "phases": phase_rows,
        "strict_examples": strict_examples(),
        "known_counterexample": {
            "phase": "u",
            "complexity": 25,
            "state": KNOWN_COUNTEREXAMPLE,
            "state_hex": hex(KNOWN_COUNTEREXAMPLE),
            "recursive_membership": True,
            "recovered_generator_word": witness,
            "recursive_cache_entries": frontier_member.cache_info().currsize,
        },
        "scientific_boundary": (
            "The recursion decides ordinary phase-frontier membership exactly. It "
            "does not prove that actual return penalties recur positively, prove "
            "phase-complexity divergence, exclude eventual center period two, or "
            "solve Rule 30 center nonperiodicity."
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
