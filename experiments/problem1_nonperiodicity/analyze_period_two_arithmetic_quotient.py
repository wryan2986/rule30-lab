#!/usr/bin/env python3
"""Analyze the arithmetic quotient of normalized period-two witnesses.

For a normalized inverse word G=a_1...a_n beginning in phase p or u, let

    x(G)=G^{-1}(0)

be its ordinary preimage of zero. Different words can have the same x(G), and
on odd arithmetic states the forward letters p and u coincide. Tracking only
state parity gives a Pell-growth upper bound on the number of distinct
arithmetic witnesses:

    E_(n+1) <= E_n + O_n,
    O_(n+1) <= 2 E_n + O_n.

For one fixed phase, the number of exact-length-n states is at most the Pell
number P_n. This sharpens the finite-witness counting theorem and improves the
Bernoulli-almost-sure lower rate from log(2)/log(3) to
log(2)/log(1+sqrt(2)).

The bounded campaign also compares every reachable arithmetic state through a
configured word length with the exact actual schedule-survivor residue. It is
finite regression evidence and does not prove divergence on the actual orbit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from typing import Any

LETTERS = ("t", "p", "u")
PHASE_START = {"p": 3, "u": 1}
PHASES = tuple(PHASE_START)
DEFAULT_MAXIMUM_LENGTH = 16
ABSOLUTE_MAXIMUM_LENGTH = 22
DEFAULT_SURVIVOR_BITS = 64


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


def next_arithmetic_states(state: int) -> set[int]:
    return {forward_generator(letter, state) for letter in LETTERS}


def pell_numbers(maximum_index: int) -> list[int]:
    if maximum_index < 0:
        raise ValueError("maximum index must be nonnegative")
    values = [0] * (maximum_index + 1)
    if maximum_index >= 1:
        values[1] = 1
    for index in range(2, maximum_index + 1):
        values[index] = 2 * values[index - 1] + values[index - 2]
    return values


def pell_cumulative_bound(maximum_length: int) -> int:
    """Return sum(P_1,...,P_N)."""
    if maximum_length <= 0:
        return 0
    pell = pell_numbers(maximum_length + 1)
    return (pell[maximum_length + 1] + pell[maximum_length] - 1) // 2


def verify_parity_transition(sample_limit: int = 4096) -> dict[str, Any]:
    checked = 0
    for state in range(1, sample_limit + 1):
        t_value = forward_generator("t", state)
        p_value = forward_generator("p", state)
        u_value = forward_generator("u", state)
        if (t_value & 1) != (state & 1):
            raise AssertionError("t did not preserve parity")
        if (p_value & 1) == (state & 1) or (u_value & 1) == (state & 1):
            raise AssertionError("p/u did not flip parity")
        if state & 1:
            if p_value != u_value:
                raise AssertionError("p and u must coincide on odd states")
            if len({t_value, p_value, u_value}) != 2:
                raise AssertionError("odd state must have two distinct children")
        else:
            if len({t_value, p_value, u_value}) != 3:
                raise AssertionError("even state must have three distinct children")
        checked += 1
    return {
        "positive_states_checked": checked,
        "odd_state_children": {"odd": 1, "even": 1, "identity": "p(x)=u(x)"},
        "even_state_children": {"odd": 2, "even": 1},
        "parity_matrix": [[1, 1], [2, 1]],
        "spectral_radius": 1 + math.sqrt(2),
        "all_checks_pass": True,
    }


def reachable_rows(maximum_length: int) -> tuple[dict[str, list[dict[str, int]]], dict[str, set[int]]]:
    pell = pell_numbers(maximum_length)
    rows: dict[str, list[dict[str, int]]] = {}
    cumulative_sets: dict[str, set[int]] = {}
    for phase, initial in PHASE_START.items():
        current = {initial}
        cumulative: set[int] = set()
        phase_rows: list[dict[str, int]] = []
        for length in range(1, maximum_length + 1):
            if length > 1:
                current = {
                    successor
                    for state in current
                    for successor in next_arithmetic_states(state)
                }
            cumulative.update(current)
            even = sum(state & 1 == 0 for state in current)
            odd = len(current) - even
            if len(current) > pell[length]:
                raise AssertionError("exact arithmetic image exceeded Pell bound")
            if len(cumulative) > pell_cumulative_bound(length):
                raise AssertionError("cumulative arithmetic image exceeded Pell sum")
            phase_rows.append(
                {
                    "length": length,
                    "distinct_exact_length_states": len(current),
                    "distinct_cumulative_states": len(cumulative),
                    "even_states": even,
                    "odd_states": odd,
                    "pell_exact_bound": pell[length],
                    "pell_cumulative_bound": pell_cumulative_bound(length),
                }
            )
        rows[phase] = phase_rows
        cumulative_sets[phase] = cumulative
    return rows, cumulative_sets


def fringe_step(state: int) -> int:
    if state < 0:
        raise ValueError("fringe state must be nonnegative")
    packed = 1 + 2 * state
    odd = packed ^ ((packed >> 1) | (packed >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def actual_driver(length: int) -> tuple[str, ...]:
    state = 0
    output: list[str] = []
    for _ in range(length):
        output.append("u" if state & 3 == 0 else "t")
        state = fringe_step(state)
    return tuple(output)


def _inverse_t_mod(output: int, width: int) -> int:
    if width < 0:
        raise ValueError("width must be nonnegative")
    if width == 0:
        return 0
    output &= (1 << width) - 1
    state = 0
    for position in range(width):
        previous_one = (state >> (position - 1)) & 1 if position >= 1 else 0
        previous_two = (state >> (position - 2)) & 1 if position >= 2 else 0
        bit = ((output >> position) & 1) ^ (previous_one | previous_two)
        state |= bit << position
    return state


def inverse_generator_mod(name: str, output: int, width: int) -> int:
    if width == 0:
        return 0
    mask = (1 << width) - 1
    output &= mask
    if name == "t":
        return _inverse_t_mod(output, width)
    if name == "u":
        return _inverse_t_mod(output ^ 1, width)
    if name == "p":
        recovered_low_bit = (output & 1) ^ 1
        adjusted = output ^ 1 ^ (2 if recovered_low_bit == 0 else 0)
        return _inverse_t_mod(adjusted, width)
    raise ValueError("unknown generator")


def backward_zero_branch(q_name: str, successor: int, width: int) -> int:
    if q_name not in ("t", "u"):
        raise ValueError("branch must be t or u")
    if width < 2:
        raise ValueError("width must be at least two")
    inner_width = width - 2
    state = inverse_generator_mod(q_name, successor, inner_width)
    state = inverse_generator_mod("p", state, inner_width)
    return ((state << 2) | 3) & ((1 << width) - 1)


def schedule_survivor_residue(q_names: tuple[str, ...], width: int) -> int:
    if width < 2 or width % 2:
        raise ValueError("width must be a positive even integer")
    required = width // 2
    if len(q_names) < required:
        raise ValueError("not enough branch letters")
    state = 0
    precision = 0
    for q_name in reversed(q_names[:required]):
        precision += 2
        state = backward_zero_branch(q_name, state, precision)
    return state


def valuation_difference(left: int, right: int, width: int) -> int:
    difference = (left - right) & ((1 << width) - 1)
    if difference == 0:
        return width
    return (difference & -difference).bit_length() - 1


def actual_agreement_rows(maximum_length: int, survivor_bits: int) -> dict[str, Any]:
    if survivor_bits < 2 * maximum_length + 2:
        raise ValueError("survivor width is too small for the requested word length")
    driver = actual_driver(survivor_bits // 2)
    survivor = schedule_survivor_residue(driver, survivor_bits)
    phase_rows: dict[str, list[dict[str, int]]] = {}
    for phase, initial in PHASE_START.items():
        current = {initial}
        cumulative: set[int] = set()
        rows: list[dict[str, int]] = []
        best_valuation = -1
        best_state = 0
        for length in range(1, maximum_length + 1):
            if length > 1:
                current = {
                    successor
                    for state in current
                    for successor in next_arithmetic_states(state)
                }
            cumulative.update(current)
            for state in cumulative:
                valuation = valuation_difference(state, survivor, survivor_bits)
                if valuation > best_valuation:
                    best_valuation = valuation
                    best_state = state
            rows.append(
                {
                    "maximum_length": length,
                    "distinct_exact_length_states": len(current),
                    "distinct_cumulative_states": len(cumulative),
                    "best_matching_bits": best_valuation,
                    "best_complete_pair_depth": best_valuation // 2,
                    "best_state": best_state,
                }
            )
        phase_rows[phase] = rows
    return {
        "survivor_bits": survivor_bits,
        "actual_driver_prefix": "".join(driver),
        "actual_survivor_residue": survivor,
        "actual_survivor_residue_hex": hex(survivor),
        "by_phase": phase_rows,
        "interpretation": (
            "a phase word of length at most N can sustain exactly floor(v2(x-X)/2) "
            "complete zero blocks, where x is its arithmetic quotient state"
        ),
        "all_checks_pass": True,
    }


def run_campaign(
    maximum_length: int = DEFAULT_MAXIMUM_LENGTH,
    survivor_bits: int = DEFAULT_SURVIVOR_BITS,
) -> dict[str, Any]:
    if not 1 <= maximum_length <= ABSOLUTE_MAXIMUM_LENGTH:
        raise ValueError("maximum length outside campaign cap")
    if survivor_bits % 2 or survivor_bits < 2 * maximum_length + 2:
        raise ValueError("survivor bits must be even and sufficiently large")
    reachable, _ = reachable_rows(maximum_length)
    rate = math.log(2) / math.log(1 + math.sqrt(2))
    payload: dict[str, Any] = {
        "parity_transition": verify_parity_transition(),
        "reachable_arithmetic_states": reachable,
        "actual_agreement": actual_agreement_rows(maximum_length, survivor_bits),
        "exact_conclusions": {
            "pell_bound": (
                "for a fixed phase, exact-length-n arithmetic witness states are at most P_n"
            ),
            "cumulative_pell_bound": (
                "phase-a witness states of length at most N are at most "
                "(P_(N+1)+P_N-1)/2"
            ),
            "improved_counting": (
                "the same bound applies to distinct driver prefixes with kappa_a(q,L)<=N"
            ),
            "almost_sure_rate": (
                "Bernoulli-almost surely liminf kappa_a(q,L)/L is at least "
                "log(2)/log(1+sqrt(2))"
            ),
        },
        "almost_sure_linear_rate": rate,
        "scope_warning": (
            "bounded arithmetic enumeration does not prove divergence on the actual schedule"
        ),
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-arithmetic-quotient-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-length", type=int, default=DEFAULT_MAXIMUM_LENGTH)
    parser.add_argument("--survivor-bits", type=int, default=DEFAULT_SURVIVOR_BITS)
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_length, args.survivor_bits), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
