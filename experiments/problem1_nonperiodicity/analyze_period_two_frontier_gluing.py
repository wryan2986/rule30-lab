#!/usr/bin/env python3
"""Analyze exact low/high frontier gluing for period-two return prefixes.

A finite prefix of u-to-u return gaps fixes a unique low 2-adic cylinder for
the hypothetical survivor.  This module proves and checks that the cylinder can
be combined with any prescribed finite leading-bit word, with an arbitrary
middle region between them.  Thus fixed return-prefix and fixed high-front
checks cannot by themselves exclude ordinary finite support.

The result is a no-go theorem for bounded separated-front tests, not a proof of
period-two exclusion or Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any, Iterable

DEFAULT_RETURN_COUNT = 8
DEFAULT_FRONT_WIDTH = 8
DEFAULT_FREE_BITS = 10
ABSOLUTE_RETURN_COUNT = 32
ABSOLUTE_FRONT_WIDTH = 32
ABSOLUTE_FREE_BITS = 20
RETURN_TIMES = (2, 3, 4, 5)


class FrontierGluingLimitError(RuntimeError):
    """Raised before an explicitly capped finite campaign is exceeded."""


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def _load_sibling(filename: str, module_name: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FIRST_RETURN = _load_sibling(
    "analyze_period_two_first_return.py", "period_two_first_return"
)
SURVIVOR = _load_sibling(
    "analyze_period_two_schedule_survivor.py", "schedule_survivor"
)


def branch_word_for_return_gaps(gaps: Iterable[int]) -> tuple[str, ...]:
    """Return the branch word from one u event up to the next final u event."""

    word: list[str] = []
    for gap in gaps:
        if gap not in RETURN_TIMES:
            raise ValueError("every return gap must be one of 2,3,4,5")
        word.append("u")
        word.extend("t" for _ in range(gap - 1))
    return tuple(word)


def survivor_y_prefix_residue(gaps: Iterable[int]) -> tuple[int, int]:
    """Return the unique y residue and modulus for a finite return-gap prefix.

    At the initial u event write X=16y+7.  If the listed gaps have total branch
    length B, survival through the prefix fixes y modulo 2**(2B).  The terminal
    state is constrained only to the next u cylinder X=7 mod 16.
    """

    gap_tuple = tuple(gaps)
    word = branch_word_for_return_gaps(gap_tuple)
    branch_count = len(word)
    if branch_count == 0:
        return 0, 1
    width = 2 * branch_count + 4
    state = 7
    for q_name in reversed(word):
        state = SURVIVOR.backward_zero_branch(q_name, state, width)
    if (state - 7) % 16:
        raise AssertionError("backward return cylinder is not normalized")
    modulus = 1 << (2 * branch_count)
    residue = ((state - 7) >> 4) & (modulus - 1)
    return residue, modulus


def follow_survivor_return_prefix(
    y_value: int, gaps: Iterable[int]
) -> tuple[int, tuple[int, ...]]:
    """Advance an ordinary y state through the requested return prefix."""

    if y_value < 0:
        raise ValueError("y must be nonnegative")
    observed: list[int] = []
    for expected_gap in gaps:
        returned = FIRST_RETURN.forced_survivor_return(y_value)
        if returned is None:
            raise AssertionError("state stopped before the prescribed return prefix")
        gap, y_value = returned
        if gap != expected_gap:
            raise AssertionError("state followed a different return gap")
        observed.append(gap)
    return y_value, tuple(observed)


def glue_finite_state(
    *,
    low_residue: int,
    low_modulus: int,
    front_word: int,
    front_width: int,
    free_middle: int,
    free_bits: int,
) -> int:
    """Glue a low cylinder, free middle, and prescribed leading word."""

    if low_modulus <= 0 or low_modulus & (low_modulus - 1):
        raise ValueError("low_modulus must be a positive power of two")
    low_bits = low_modulus.bit_length() - 1
    if not 0 <= low_residue < low_modulus:
        raise ValueError("low_residue must fit low_modulus")
    if front_width <= 0:
        raise ValueError("front_width must be positive")
    if not (1 << (front_width - 1)) <= front_word < (1 << front_width):
        raise ValueError("front_word must have exactly front_width bits")
    if free_bits < 0 or not 0 <= free_middle < (1 << free_bits):
        raise ValueError("free_middle must fit free_bits")
    return (
        (front_word << (free_bits + low_bits))
        | (free_middle << low_bits)
        | low_residue
    )


def actual_return_gaps(count: int) -> tuple[int, ...]:
    """Return the first ``count`` exact u-to-u gaps from the zero right fringe."""

    if count < 0:
        raise ValueError("count must be nonnegative")
    z_value = 0
    gaps: list[int] = []
    for _ in range(count):
        gap, z_value = FIRST_RETURN.fringe_return_step(z_value)
        gaps.append(gap)
    return tuple(gaps)


def verify_single_gap_residues() -> dict[str, Any]:
    rows = []
    for gap in RETURN_TIMES:
        residue, modulus = survivor_y_prefix_residue((gap,))
        expected = FIRST_RETURN.EXPECTED_SURVIVOR_RESIDUES[gap]
        if modulus != 1 << (2 * gap) or residue != expected:
            raise AssertionError("grouped prefix cylinder disagrees with first-return result")
        rows.append({"gap": gap, "residue": residue, "modulus": modulus})
    return {"rows": rows, "all_checks_pass": True}


def verify_gluing_campaign(
    *, return_count: int, front_width: int, free_bits: int
) -> dict[str, Any]:
    gaps = actual_return_gaps(return_count)
    low_residue, low_modulus = survivor_y_prefix_residue(gaps)
    low_bits = low_modulus.bit_length() - 1
    front_words = tuple(range(1 << (front_width - 1), 1 << front_width))
    middle_count = 1 << free_bits
    checks = 0
    final_bit_lengths: set[int] = set()

    for front_word in front_words:
        for middle in range(middle_count):
            y_value = glue_finite_state(
                low_residue=low_residue,
                low_modulus=low_modulus,
                front_word=front_word,
                front_width=front_width,
                free_middle=middle,
                free_bits=free_bits,
            )
            expected_length = low_bits + free_bits + front_width
            if y_value.bit_length() != expected_length:
                raise AssertionError("glued state has the wrong leading position")
            if y_value & (low_modulus - 1) != low_residue:
                raise AssertionError("glued state left the prescribed low cylinder")
            if y_value >> (low_bits + free_bits) != front_word:
                raise AssertionError("glued state lost the prescribed high front")
            successor, observed = follow_survivor_return_prefix(y_value, gaps)
            if observed != gaps:
                raise AssertionError("glued state failed the exact return prefix")
            final_bit_lengths.add(successor.bit_length())
            checks += 1

    expected_checks = len(front_words) * middle_count
    if checks != expected_checks:
        raise AssertionError("unexpected gluing count")
    total_branches = sum(gaps)
    expected_initial_bits = low_bits + free_bits + front_width
    expected_final_bits = expected_initial_bits + 2 * total_branches
    if final_bit_lengths != {expected_final_bits}:
        raise AssertionError("degree cocycle did not preserve the glued front length")

    return {
        "actual_return_gaps": list(gaps),
        "total_zero_branches": total_branches,
        "fixed_low_bits": low_bits,
        "low_residue": low_residue,
        "front_width": front_width,
        "leading_front_words_checked": len(front_words),
        "free_middle_bits": free_bits,
        "free_middle_assignments_per_front": middle_count,
        "ordinary_finite_states_checked": checks,
        "exact_family_size": f"2^({front_width - 1}+{free_bits})",
        "initial_bit_length": expected_initial_bits,
        "final_bit_length_after_prefix": expected_final_bits,
        "all_checks_pass": True,
    }


def run_campaign(
    *,
    return_count: int = DEFAULT_RETURN_COUNT,
    front_width: int = DEFAULT_FRONT_WIDTH,
    free_bits: int = DEFAULT_FREE_BITS,
) -> dict[str, Any]:
    if return_count > ABSOLUTE_RETURN_COUNT:
        raise FrontierGluingLimitError("return count exceeds absolute maximum")
    if front_width > ABSOLUTE_FRONT_WIDTH:
        raise FrontierGluingLimitError("front width exceeds absolute maximum")
    if free_bits > ABSOLUTE_FREE_BITS:
        raise FrontierGluingLimitError("free-middle width exceeds absolute maximum")

    payload = {
        "single_gap_consistency": verify_single_gap_residues(),
        "actual_prefix_gluing": verify_gluing_campaign(
            return_count=return_count,
            front_width=front_width,
            free_bits=free_bits,
        ),
        "exact_conclusions": {
            "unique_low_cylinder": (
                "a return-gap prefix of total branch length B fixes exactly one "
                "survivor residue y modulo 2^(2B)"
            ),
            "arbitrary_front_gluing": (
                "any finite leading word and any finite free middle can be glued "
                "above that low cylinder without changing the return prefix"
            ),
            "bounded_frontier_obstruction": (
                "fixed low-prefix and fixed high-front tests cannot exclude finite "
                "support; a successful invariant must bridge the growing interior"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-frontier-gluing-v1\0")
    digest.update(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    )
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--return-count", type=_positive_integer, default=DEFAULT_RETURN_COUNT)
    parser.add_argument("--front-width", type=_positive_integer, default=DEFAULT_FRONT_WIDTH)
    parser.add_argument("--free-bits", type=_positive_integer, default=DEFAULT_FREE_BITS)
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(
        return_count=args.return_count,
        front_width=args.front_width,
        free_bits=args.free_bits,
    )
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-frontier-gluing-v1",
        "question": "problem1",
        "hypothesis": (
            "Finite return-prefix constraints and finite high-front constraints "
            "remain exactly separable by an arbitrary middle region."
        ),
        "backend": "python-exact-2adic-cylinder-gluing",
        "parameters": {
            "return_count": args.return_count,
            "front_width": args.front_width,
            "free_bits": args.free_bits,
        },
        "result_summary": result,
        "status": "finite-exhaustive",
        "proof_scope": (
            "The all-width cylinder and gluing arguments are stated in "
            "proofs/informal/problem1_period_two_frontier_gluing.md. The analyzer "
            "checks a bounded actual return prefix and every selected finite gluing."
        ),
        "interpretation": (
            "A fixed-width high-front refinement cannot close the period-two proof: "
            "finite shadows can satisfy the exact low schedule cylinder while carrying "
            "any prescribed finite edge shape."
        ),
        "limitations": [
            "the construction changes the finite state as the tested prefix grows",
            "it does not construct one ordinary state surviving the infinite schedule",
            "it does not exclude a growing-width or genuinely global invariant",
            "it does not exclude eventual center period two",
            "it does not solve Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
