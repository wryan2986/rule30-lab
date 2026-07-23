#!/usr/bin/env python3
"""Analyze the characteristic high frontier of a hypothetical period-two zero tail.

If an ordinary normalized state emits zero forever, one block has the form

    x' = q(p(x >> 2)),  q in {t,u}.

The branch-dependent corrections live at the low end.  Reading a finite integer
from its highest set bit downward, the high frontier evolves exactly by two
steps of a shifted Rule 30 map, except for a bounded low-end boundary layer.
This module verifies that conjugacy exhaustively, proves/validates dyadic
period bounds for every fixed high-front column, and records the scientific
boundary: the aperiodic low schedule and dyadically recurrent high frontier
remain separated by a growing right-permutive interior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any

DEFAULT_INTEGER_WIDTH = 16
DEFAULT_PREFIX_WIDTH = 12
ABSOLUTE_INTEGER_WIDTH = 20
ABSOLUTE_PREFIX_WIDTH = 16


def right_edge_step(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    return state ^ ((state << 1) | (state << 2))


def forward_generator(name: str, state: int) -> int:
    stepped = right_edge_step(state)
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError("unknown generator")


def zero_step(state: int) -> tuple[str, int] | None:
    residue = state & 15
    if residue == 7:
        branch = "u"
    elif residue == 11:
        branch = "t"
    else:
        return None
    shifted = state >> 2
    return branch, forward_generator(branch, forward_generator("p", shifted))


def high_front(state: int, width: int | None = None) -> tuple[int, ...]:
    """Read from the highest set bit downward and pad by zeros on the right."""
    if state <= 0:
        raise ValueError("state must be positive")
    natural = state.bit_length()
    if width is None:
        width = natural
    if width < 0:
        raise ValueError("width must be nonnegative")
    top = natural - 1
    return tuple((state >> (top - j)) & 1 if j < natural else 0 for j in range(width))


def shifted_rule30_step(front: tuple[int, ...]) -> tuple[int, ...]:
    """The exact top-oriented Rule 30 step.

    Missing cells to the left of the highest bit are zero.  The output at j is
    f(front[j-2], front[j-1], front[j]) for f(a,b,c)=a XOR (b OR c).
    """
    out = []
    for j, current in enumerate(front):
        left2 = front[j - 2] if j >= 2 else 0
        left1 = front[j - 1] if j >= 1 else 0
        out.append(left2 ^ (left1 | current))
    return tuple(out)


def shifted_rule30_two_step(front: tuple[int, ...]) -> tuple[int, ...]:
    return shifted_rule30_step(shifted_rule30_step(front))


def verify_reversal_conjugacy(maximum_width: int) -> dict[str, Any]:
    cases = 0
    for width in range(1, maximum_width + 1):
        for state in range(1 << (width - 1), 1 << width):
            padded = high_front(state, width + 2)
            expected = shifted_rule30_step(padded)
            actual = high_front(right_edge_step(state), width + 2)
            if actual != expected:
                raise AssertionError((width, state, actual, expected))
            cases += 1
    return {
        "maximum_integer_width": maximum_width,
        "ordinary_states_checked": cases,
        "identity": "front(T(x)) = E(front(x))",
        "all_checks_pass": True,
    }


def verify_zero_tail_front(maximum_width: int) -> dict[str, Any]:
    cases = 0
    branch_counts: Counter[str] = Counter()
    compared_bits = 0
    for width in range(4, maximum_width + 1):
        for state in range(1 << (width - 1), 1 << width):
            result = zero_step(state)
            if result is None:
                continue
            branch, successor = result
            if successor.bit_length() != state.bit_length() + 2:
                raise AssertionError("continuing degree law failed")
            before = high_front(state, width)
            after = high_front(successor, width + 2)
            expected = shifted_rule30_two_step(before + (0, 0))
            safe = width - 2
            if after[:safe] != expected[:safe]:
                raise AssertionError((state, branch, after[:safe], expected[:safe]))
            cases += 1
            branch_counts[branch] += 1
            compared_bits += safe
    return {
        "maximum_integer_width": maximum_width,
        "zero_branch_states_checked": cases,
        "branch_counts": dict(sorted(branch_counts.items())),
        "high_front_bits_compared": compared_bits,
        "exact_safe_prefix": "all front positions j <= degree(x)-2",
        "boundary_layer": "only the final four low-end positions can depend on q",
        "all_checks_pass": True,
    }


def _prefix_map(state: int, width: int) -> int:
    bits = tuple((state >> j) & 1 for j in range(width))
    out = shifted_rule30_step(bits)
    return sum(bit << j for j, bit in enumerate(out))


def _functional_graph_statistics(width: int) -> dict[str, Any]:
    size = 1 << width
    successor = [_prefix_map(state, width) for state in range(size)]
    status = [0] * size
    cycle_periods: Counter[int] = Counter()
    maximum_preperiod = 0

    for start in range(size):
        if status[start] == 2:
            continue
        path: list[int] = []
        local: dict[int, int] = {}
        node = start
        while status[node] == 0 and node not in local:
            local[node] = len(path)
            path.append(node)
            status[node] = 1
            node = successor[node]
        if node in local:
            cycle_start = local[node]
            period = len(path) - cycle_start
            cycle_periods[period] += 1
            maximum_preperiod = max(maximum_preperiod, cycle_start)
        for item in path:
            status[item] = 2

    if any(period & (period - 1) for period in cycle_periods):
        raise AssertionError("non-dyadic prefix cycle found")
    if any(period > (1 << width) for period in cycle_periods):
        raise AssertionError("period bound failed")
    return {
        "width": width,
        "states": size,
        "cycle_period_counts": {str(k): v for k, v in sorted(cycle_periods.items())},
        "maximum_cycle_period": max(cycle_periods, default=0),
        "maximum_preperiod_seen": maximum_preperiod,
        "all_periods_powers_of_two": True,
    }


def verify_prefix_periods(maximum_width: int) -> dict[str, Any]:
    levels = [_functional_graph_statistics(width) for width in range(1, maximum_width + 1)]
    return {
        "maximum_prefix_width": maximum_width,
        "levels": levels,
        "exact_inductive_bound": (
            "column j is eventually periodic with period dividing 2^(j+1); "
            "a width-r prefix therefore has dyadic eventual period dividing 2^r"
        ),
        "all_checks_pass": True,
    }


def run_campaign(integer_width: int, prefix_width: int) -> dict[str, Any]:
    if not 1 <= integer_width <= ABSOLUTE_INTEGER_WIDTH:
        raise ValueError("integer width outside campaign cap")
    if not 1 <= prefix_width <= ABSOLUTE_PREFIX_WIDTH:
        raise ValueError("prefix width outside campaign cap")
    payload = {
        "reversal_conjugacy": verify_reversal_conjugacy(integer_width),
        "zero_tail_front": verify_zero_tail_front(integer_width),
        "prefix_periods": verify_prefix_periods(prefix_width),
        "exact_conclusions": {
            "characteristic_self_embedding": (
                "the schedule-independent high frontier of every ordinary zero-tail state is an exact shifted Rule 30 orbit"
            ),
            "dyadic_front_recurrence": (
                "every fixed high-front window is eventually periodic with a power-of-two period"
            ),
            "two_boundary_strip": (
                "under the finite-support period-two hypothesis, a dyadically recurrent high boundary must coexist with the already-proved aperiodic low fringe schedule across a growing right-permutive interior"
            ),
            "remaining_target": (
                "a cross-characteristic quantity spanning both boundaries; neither boundary alone can exclude finite support"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-characteristic-front-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--integer-width", type=int, default=DEFAULT_INTEGER_WIDTH)
    parser.add_argument("--prefix-width", type=int, default=DEFAULT_PREFIX_WIDTH)
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.integer_width, args.prefix_width), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
