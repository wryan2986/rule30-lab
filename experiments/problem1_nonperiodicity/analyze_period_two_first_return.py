#!/usr/bin/env python3
"""Analyze exact first returns between ``u`` events in the period-two system.

The period-two moving-fringe schedule has ``u`` exactly when the first two
fringe bits vanish.  The earlier trace-language theorem confines the next
``u`` return to two through five blocks.  This module sharpens that statement:

* after writing a ``u``-state as ``A=4z``, the return time is determined only
  by ``z mod 16``;
* the survivor-side state at a ``u`` return has one exact residue cylinder for
  each return time;
* both ordinary finite return systems have the same degree increment ``2r``.

The shared degree cocycle is structural progress, not a contradiction.  It
does not prove that the actual schedule survivor has infinite support and does
not solve Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

DEFAULT_SELECTOR_BITS = 10
DEFAULT_FORWARD_SAMPLES_PER_BRANCH = 1_024
ABSOLUTE_SELECTOR_BITS = 16
ABSOLUTE_FORWARD_SAMPLES_PER_BRANCH = 16_384
RETURN_TIMES = (2, 3, 4, 5)
EXPECTED_SELECTOR = {
    0: 4,
    1: 3,
    2: 4,
    3: 3,
    4: 2,
    5: 3,
    6: 4,
    7: 5,
    8: 2,
    9: 3,
    10: 4,
    11: 5,
    12: 2,
    13: 3,
    14: 4,
    15: 5,
}
EXPECTED_SURVIVOR_RESIDUES = {2: 8, 3: 60, 4: 108, 5: 940}
PAIR_WITNESSES = {
    (2, 2): 28,
    (2, 4): 4,
    (2, 5): 8,
    (3, 2): 17,
    (3, 3): 1,
    (3, 4): 57,
    (3, 5): 29,
    (4, 2): 0,
    (4, 3): 34,
    (4, 4): 14,
    (4, 5): 2,
    (5, 2): 15,
    (5, 3): 39,
    (5, 4): 31,
    (5, 5): 7,
}


class FirstReturnLimitError(RuntimeError):
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


FRINGE = _load_sibling("analyze_period_two_fringe_language.py", "fringe_language")
RENEWAL = _load_sibling("analyze_period_two_renewal.py", "period_two_renewal")
SURVIVOR = _load_sibling(
    "analyze_period_two_schedule_survivor.py", "schedule_survivor"
)


def iterate_fringe(state: int, steps: int) -> int:
    if state < 0 or steps < 0:
        raise ValueError("state and steps must be nonnegative")
    for _ in range(steps):
        state = FRINGE.advance_fringe_packed(state)
    return state


def first_return_gap_from_u_state(z_value: int) -> int:
    """Return the next ``u`` gap when the current fringe is ``A=4z``."""

    if z_value < 0:
        raise ValueError("z must be nonnegative")
    state = 4 * z_value
    if FRINGE.branch_letter(state) != "u":
        raise AssertionError("A=4z must begin in the u cylinder")
    for gap in range(1, max(RETURN_TIMES) + 1):
        state = FRINGE.advance_fringe_packed(state)
        if FRINGE.branch_letter(state) == "u":
            if gap not in RETURN_TIMES:
                raise AssertionError("unexpected u return outside 2..5")
            return gap
    raise AssertionError("the exact trace-language theorem bounds returns by five")


def fringe_return_step(z_value: int) -> tuple[int, int]:
    gap = first_return_gap_from_u_state(z_value)
    returned = iterate_fringe(4 * z_value, gap)
    if returned & 0b11:
        raise AssertionError("first return did not land in the u cylinder")
    return gap, returned >> 2


def verify_return_selector(selector_bits: int) -> dict[str, Any]:
    """Exhaust the finite dependency cone proving the four-bit selector."""

    if selector_bits < 10:
        raise ValueError("selector_bits must be at least ten")
    counts = {gap: 0 for gap in RETURN_TIMES}
    residue_rows = []
    for residue in range(16):
        residue_rows.append(
            {"z_mod_16": residue, "first_return_gap": EXPECTED_SELECTOR[residue]}
        )

    for z_value in range(1 << selector_bits):
        observed = first_return_gap_from_u_state(z_value)
        expected = EXPECTED_SELECTOR[z_value & 15]
        if observed != expected:
            raise AssertionError("return selector depends on more than z mod 16")
        counts[observed] += 1

    return {
        "selector_bits_exhausted": selector_bits,
        "normalized_states_checked": 1 << selector_bits,
        "selector_table": residue_rows,
        "return_time_counts": {str(gap): counts[gap] for gap in RETURN_TIMES},
        "exact_statement": "rho(z) depends only on z mod 16",
        "all_checks_pass": True,
    }


def return_gaps(z_value: int, count: int) -> tuple[int, ...]:
    if count < 0:
        raise ValueError("count must be nonnegative")
    gaps = []
    for _ in range(count):
        gap, z_value = fringe_return_step(z_value)
        gaps.append(gap)
    return tuple(gaps)


def verify_gap_pair_language() -> dict[str, Any]:
    """Check the exact two-return language and explicit realization witnesses."""

    allowed = set(PAIR_WITNESSES)
    expected = {
        (left, right)
        for left in RETURN_TIMES
        for right in RETURN_TIMES
        if (left, right) != (2, 3)
    }
    if allowed != expected:
        raise AssertionError("witness table does not cover the exact pair language")
    for pair, witness in PAIR_WITNESSES.items():
        if return_gaps(witness, 2) != pair:
            raise AssertionError("gap-pair witness failed")
    return {
        "allowed_gap_pairs": [list(pair) for pair in sorted(allowed)],
        "forbidden_gap_pair": [2, 3],
        "realization_witnesses": {
            f"{left},{right}": witness
            for (left, right), witness in sorted(PAIR_WITNESSES.items())
        },
        "all_checks_pass": True,
    }


def verify_fringe_degree_cocycle(sample_limit: int) -> dict[str, Any]:
    """Check the all-width degree law on a bounded ordinary sample."""

    checks = 0
    for z_value in range(1, sample_limit + 1):
        gap, successor = fringe_return_step(z_value)
        if successor.bit_length() != z_value.bit_length() + 2 * gap:
            raise AssertionError("fringe return degree cocycle failed")
        checks += 1
    initial_gap, initial_successor = fringe_return_step(0)
    if (initial_gap, initial_successor) != (4, 56):
        raise AssertionError("unexpected exceptional first return from zero")
    return {
        "positive_states_checked": checks,
        "ordinary_degree_increment": "bit_length(z')=bit_length(z)+2*r",
        "exceptional_zero_return": {
            "gap": initial_gap,
            "successor": initial_successor,
        },
        "all_checks_pass": True,
    }


def survivor_return_residue(gap: int) -> int:
    """Return the unique normalized y residue modulo 4**gap."""

    if gap not in RETURN_TIMES:
        raise ValueError("gap must be one of 2,3,4,5")
    width = 2 * gap + 4
    state = 7
    word = ("u",) + ("t",) * (gap - 1)
    for q_name in reversed(word):
        state = SURVIVOR.backward_zero_branch(q_name, state, width)
    return ((state - 7) >> 4) & ((1 << (2 * gap)) - 1)


def forced_survivor_return(y_value: int) -> tuple[int, int] | None:
    """Advance an ordinary ``u``-state to its next ``u`` return, if it survives."""

    if y_value < 0:
        raise ValueError("y must be nonnegative")
    state = 16 * y_value + 7
    first = RENEWAL.forced_zero_step(state)
    if first is None or first[0] != "u":
        raise AssertionError("x=16y+7 must use the u branch")
    state = first[1]
    for gap in range(1, max(RETURN_TIMES) + 1):
        current = state
        step = RENEWAL.forced_zero_step(current)
        if step is None:
            return None
        q_name, successor = step
        if q_name == "u":
            if gap not in RETURN_TIMES:
                raise AssertionError("unexpected survivor u return outside 2..5")
            if (current - 7) % 16:
                raise AssertionError("returned survivor state is not 7 mod 16")
            return gap, (current - 7) // 16
        state = successor
    raise AssertionError("surviving actual return words have gaps at most five")


def verify_survivor_return_cylinders(samples_per_branch: int) -> dict[str, Any]:
    """Verify exact survivor return cylinders and their degree cocycle."""

    rows = []
    checks = 0
    for gap in RETURN_TIMES:
        modulus = 1 << (2 * gap)
        residue = survivor_return_residue(gap)
        if residue != EXPECTED_SURVIVOR_RESIDUES[gap]:
            raise AssertionError("unexpected survivor return residue")
        for quotient in range(samples_per_branch):
            y_value = residue + modulus * quotient
            returned = forced_survivor_return(y_value)
            if returned is None or returned[0] != gap:
                raise AssertionError("survivor return cylinder failed")
            successor = returned[1]
            if successor.bit_length() != y_value.bit_length() + 2 * gap:
                raise AssertionError("survivor return degree cocycle failed")
            checks += 1
        rows.append(
            {
                "gap": gap,
                "y_modulus": modulus,
                "required_y_residue": residue,
                "schedule_word": "u" + "t" * (gap - 1) + "u",
            }
        )
    return {
        "return_cylinders": rows,
        "ordinary_states_checked": checks,
        "ordinary_degree_increment": "bit_length(y')=bit_length(y)+2*r",
        "all_checks_pass": True,
    }


def verify_shared_degree_cocycle() -> dict[str, Any]:
    """State the exact coupled consequence under a finite-survivor hypothesis."""

    return {
        "hypothetical_u_return_states": {
            "fringe": "A_n=4*z_n",
            "survivor": "X_n=16*y_n+7",
        },
        "shared_return_time": "r_n in {2,3,4,5}",
        "degree_updates": {
            "fringe": "deg(z_(n+1))=deg(z_n)+2*r_n",
            "survivor": "deg(y_(n+1))=deg(y_n)+2*r_n",
        },
        "cocycle": (
            "after the exceptional initial z_0=0 return, "
            "deg(y_n)-deg(z_n) is constant along u returns"
        ),
        "scientific_boundary": (
            "the constant degree offset does not force a contradiction; a future "
            "argument must distinguish the two high-front shapes or couple them "
            "to survivor output pairs"
        ),
    }


def run_campaign(
    *,
    selector_bits: int = DEFAULT_SELECTOR_BITS,
    forward_samples_per_branch: int = DEFAULT_FORWARD_SAMPLES_PER_BRANCH,
) -> dict[str, Any]:
    if selector_bits > ABSOLUTE_SELECTOR_BITS:
        raise FirstReturnLimitError("selector bit count exceeds absolute maximum")
    if forward_samples_per_branch > ABSOLUTE_FORWARD_SAMPLES_PER_BRANCH:
        raise FirstReturnLimitError("forward sample count exceeds absolute maximum")
    payload = {
        "fringe_return_selector": verify_return_selector(selector_bits),
        "gap_pair_language": verify_gap_pair_language(),
        "fringe_degree_cocycle": verify_fringe_degree_cocycle(
            forward_samples_per_branch
        ),
        "survivor_return_cylinders": verify_survivor_return_cylinders(
            forward_samples_per_branch
        ),
        "shared_degree_cocycle": verify_shared_degree_cocycle(),
        "exact_conclusions": {
            "four_bit_selector": (
                "at a u event A=4z, the next u return time is determined exactly "
                "by z mod 16"
            ),
            "variable_length_survivor_coding": (
                "each return gap r fixes one survivor residue y mod 4^r"
            ),
            "shared_degree_increment": (
                "both ordinary finite return systems increase normalized degree "
                "by exactly 2r"
            ),
            "remaining_obstruction": (
                "return time and degree alone cannot exclude finite support; the "
                "next invariant must compare high-front shape or survivor output"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-first-return-v1\0")
    digest.update(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    )
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--selector-bits", type=_positive_integer, default=DEFAULT_SELECTOR_BITS
    )
    parser.add_argument(
        "--forward-samples-per-branch",
        type=_positive_integer,
        default=DEFAULT_FORWARD_SAMPLES_PER_BRANCH,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(
        selector_bits=args.selector_bits,
        forward_samples_per_branch=args.forward_samples_per_branch,
    )
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-first-return-v1",
        "question": "problem1",
        "hypothesis": (
            "The bounded-gap moving fringe and the zero-survivor dynamics admit "
            "an exact common first-return description at u events."
        ),
        "backend": "python-exact-integer-first-return",
        "parameters": {
            "selector_bits": args.selector_bits,
            "forward_samples_per_branch": args.forward_samples_per_branch,
        },
        "result_summary": result,
        "status": "finite-exhaustive",
        "proof_scope": (
            "The all-width selector, return-cylinder, and degree arguments are "
            "stated in proofs/informal/problem1_period_two_first_return.md. The "
            "analyzer exhausts the finite dependency cone and bounded ordinary "
            "regression samples used by those arguments."
        ),
        "interpretation": (
            "The period-two system has an exact variable-length return coding. "
            "The shared degree cocycle is neutral rather than contradictory, so "
            "the next proof must control high-front shape or output-pair support."
        ),
        "limitations": [
            "the shared degree offset is compatible with an infinite coupled orbit",
            "the return selector does not determine the complete fringe state",
            "the bounded regression samples do not prove infinite support",
            "the result does not exclude eventual center period two",
            "the result does not solve Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
