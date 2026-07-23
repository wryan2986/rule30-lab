#!/usr/bin/env python3
"""Analyze the exact multi-time bulk map in the period-two zero recurrence.

During a hypothetical final zero tail, the normalized ordinary state obeys

    x_(m+1) = q_m(p(x_m >> 2)),    q_m in {t,u},

where t,p,u are the forward maps inverse to the three inverse-tree letters.
This module proves and checks the next two-seam obstruction:

* above the four-bit boundary layer, every branch has the same radius-two
  Boolean bulk rule;
* after k blocks, every safe interior bit has a radius-2k dependency cone and
  is independent of the complete intervening t/u schedule;
* the bulk rule is right permutive, so an arbitrary later interior word can be
  realized by uniquely selecting one earlier middle bit per output position.

Consequently, a fixed-lag multi-time comparison cannot bridge the arbitrary
middle between low schedule cylinders and a finite high frontier.  This is a
no-go theorem for bounded-lag local seam strategies.  It does not exclude a
lag growing with the seam width, does not exclude period two, and does not
solve Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import platform
import resource
import time
from typing import Any

DEFAULT_MAXIMUM_LAG = 3
DEFAULT_MAXIMUM_TARGET_WIDTH = 5
ABSOLUTE_MAXIMUM_LAG = 4
ABSOLUTE_MAXIMUM_TARGET_WIDTH = 8


class MultiTimeBulkLimitError(RuntimeError):
    """Raised before an explicitly capped exact campaign is exceeded."""


def right_edge_step(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    return state ^ ((state << 1) | (state << 2))


def forward_generator(name: str, state: int) -> int:
    """Apply the forward map inverse to one letter t, p, or u."""

    if state < 0:
        raise ValueError("state must be nonnegative")
    stepped = right_edge_step(state)
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError(f"unknown generator {name!r}")


def normalized_zero_step(q_name: str, state: int) -> int:
    """Apply one scheduled normalized zero step, extended to all integers."""

    if q_name not in ("t", "u"):
        raise ValueError("q_name must be 't' or 'u'")
    return forward_generator(q_name, forward_generator("p", state >> 2))


def state_bit(state: int, index: int) -> int:
    if index < 0:
        return 0
    return (state >> index) & 1


def bulk_rule(window: tuple[int, int, int, int, int]) -> int:
    """Return the branch-independent interior bit after one normalized step.

    ``window`` is ``(x_(i-2), ..., x_(i+2))``.  For every branch and every
    ``i >= 4``, output bit ``i`` is this value.
    """

    a, b, c, d, e = window
    first_i = e ^ (d | c)
    first_im1 = d ^ (c | b)
    first_im2 = c ^ (b | a)
    return first_i ^ (first_im1 | first_im2)


def bulk_rule_anf() -> str:
    """Return a compact algebraic-normal-form description over GF(2)."""

    return (
        "a + b + a*b + a*c + b*c + a*b*c + "
        "a*d + b*d + a*b*d + e"
    )


def bulk_iterate(
    initial_bits: dict[int, int], lag: int, output_low: int, output_high: int
) -> dict[int, int]:
    """Iterate the bi-infinite bulk rule with zero outside supplied context."""

    if lag < 0 or output_low > output_high:
        raise ValueError("invalid lag or output interval")
    current = dict(initial_bits)
    current_low = output_low - 2 * lag
    current_high = output_high + 2 * lag
    for _ in range(lag):
        next_low = current_low + 2
        next_high = current_high - 2
        current = {
            index: bulk_rule(
                tuple(current.get(source, 0) for source in range(index - 2, index + 3))
            )
            for index in range(next_low, next_high + 1)
        }
        current_low, current_high = next_low, next_high
    return {index: current[index] for index in range(output_low, output_high + 1)}


def scheduled_iterate(schedule: tuple[str, ...], state: int) -> int:
    for q_name in schedule:
        state = normalized_zero_step(q_name, state)
    return state


def verify_one_step_bulk(input_width: int = 14) -> dict[str, Any]:
    """Exhaust complete residues and verify the exact one-step bulk identity."""

    if input_width < 12:
        raise ValueError("input_width must be at least twelve")
    checks = 0
    for q_name in ("t", "u"):
        for state in range(1 << input_width):
            successor = normalized_zero_step(q_name, state)
            for index in range(4, input_width - 2):
                window = tuple(state_bit(state, source) for source in range(index - 2, index + 3))
                if state_bit(successor, index) != bulk_rule(window):
                    raise AssertionError("branch-independent one-step bulk rule failed")
                checks += 1

    permutive_checks = 0
    for left_context in itertools.product((0, 1), repeat=4):
        if bulk_rule(left_context + (0,)) == bulk_rule(left_context + (1,)):
            raise AssertionError("bulk rule is not right permutive")
        permutive_checks += 1

    truth_table = 0
    for index, window in enumerate(itertools.product((0, 1), repeat=5)):
        truth_table |= bulk_rule(window) << index

    return {
        "input_width": input_width,
        "bulk_bit_checks": checks,
        "right_permutivity_checks": permutive_checks,
        "bulk_truth_table_hex": f"0x{truth_table:08x}",
        "bulk_rule_anf": bulk_rule_anf(),
        "exact_boundary_statement": (
            "for every q in {t,u} and every i>=4, "
            "R_q(x)_i=Phi(x_(i-2),...,x_(i+2))"
        ),
        "all_checks_pass": True,
    }


def verify_multitime_cones(maximum_lag: int) -> dict[str, Any]:
    """Exhaust every local cone and every branch word through ``maximum_lag``."""

    if maximum_lag <= 0:
        raise ValueError("maximum_lag must be positive")
    if maximum_lag > ABSOLUTE_MAXIMUM_LAG:
        raise MultiTimeBulkLimitError(
            f"maximum_lag exceeds absolute cap {ABSOLUTE_MAXIMUM_LAG}"
        )

    lag_rows = []
    total_checks = 0
    for lag in range(1, maximum_lag + 1):
        safe_index = 2 * lag + 2
        cone_width = 4 * lag + 1
        checks = 0
        for values in itertools.product((0, 1), repeat=cone_width):
            first_index = safe_index - 2 * lag
            state = sum(
                value << (first_index + offset)
                for offset, value in enumerate(values)
            )
            context = {
                first_index + offset: value
                for offset, value in enumerate(values)
            }
            expected = bulk_iterate(context, lag, safe_index, safe_index)[safe_index]
            for schedule in itertools.product(("t", "u"), repeat=lag):
                obtained = state_bit(scheduled_iterate(schedule, state), safe_index)
                if obtained != expected:
                    raise AssertionError("multi-time branch-independent cone failed")
                checks += 1
        lag_rows.append(
            {
                "lag": lag,
                "safe_output_index": safe_index,
                "input_cone_width": cone_width,
                "branch_words": 2**lag,
                "checks": checks,
            }
        )
        total_checks += checks

    return {
        "maximum_lag": maximum_lag,
        "lag_rows": lag_rows,
        "total_cone_checks": total_checks,
        "exact_conclusion": (
            "after k scheduled zero steps, every output bit i>=2k+2 is "
            "independent of the intervening branch word and depends only on "
            "initial bits i-2k through i+2k via Phi^k"
        ),
        "all_checks_pass": True,
    }


def solve_bulk_target(
    lag: int, target: tuple[int, ...], fixed_context: dict[int, int]
) -> dict[int, int]:
    """Solve uniquely for one extreme-right input bit per target output bit."""

    if lag <= 0 or not target:
        raise ValueError("lag and target width must be positive")
    bits = dict(fixed_context)
    for output_index, desired in enumerate(target):
        variable_index = output_index + 2 * lag
        bits[variable_index] = 0
        output_zero = bulk_iterate(bits, lag, output_index, output_index)[output_index]
        bits[variable_index] = 1
        output_one = bulk_iterate(bits, lag, output_index, output_index)[output_index]
        if output_zero == output_one:
            raise AssertionError("iterated bulk rule lost right permutivity")
        bits[variable_index] = 0 if output_zero == desired else 1

    produced = bulk_iterate(bits, lag, 0, len(target) - 1)
    if tuple(produced[index] for index in range(len(target))) != target:
        raise AssertionError("right-permutive target solver failed")
    return bits


def verify_block_surjectivity(
    maximum_lag: int, maximum_target_width: int
) -> dict[str, Any]:
    """Check constructive realization of every target block in fixed contexts."""

    if maximum_lag <= 0 or maximum_target_width <= 0:
        raise ValueError("campaign bounds must be positive")
    if maximum_lag > ABSOLUTE_MAXIMUM_LAG:
        raise MultiTimeBulkLimitError("maximum_lag exceeds absolute cap")
    if maximum_target_width > ABSOLUTE_MAXIMUM_TARGET_WIDTH:
        raise MultiTimeBulkLimitError("maximum_target_width exceeds absolute cap")

    checks = 0
    rows = []
    for lag in range(1, maximum_lag + 1):
        for width in range(1, maximum_target_width + 1):
            variable_positions = {index + 2 * lag for index in range(width)}
            all_positions = range(-2 * lag, width + 2 * lag)
            fixed_positions = [
                position for position in all_positions if position not in variable_positions
            ]
            contexts = (
                {position: 0 for position in fixed_positions},
                {position: 1 for position in fixed_positions},
                {
                    position: (position * position + 3 * position + 1) & 1
                    for position in fixed_positions
                },
            )
            local_checks = 0
            for context in contexts:
                for target in itertools.product((0, 1), repeat=width):
                    solve_bulk_target(lag, target, context)
                    checks += 1
                    local_checks += 1
            rows.append(
                {
                    "lag": lag,
                    "target_width": width,
                    "contexts": len(contexts),
                    "targets_per_context": 2**width,
                    "checks": local_checks,
                }
            )

    return {
        "maximum_lag": maximum_lag,
        "maximum_target_width": maximum_target_width,
        "rows": rows,
        "constructive_checks": checks,
        "exact_conclusion": (
            "Phi^k is right permutive in the extreme input bit i+2k; "
            "therefore every finite later interior word is realizable after "
            "fixing all other bits in its dependency rectangle"
        ),
        "all_checks_pass": True,
    }


def run_campaign(
    maximum_lag: int = DEFAULT_MAXIMUM_LAG,
    maximum_target_width: int = DEFAULT_MAXIMUM_TARGET_WIDTH,
) -> dict[str, Any]:
    if maximum_lag > ABSOLUTE_MAXIMUM_LAG:
        raise MultiTimeBulkLimitError("maximum_lag exceeds absolute cap")
    if maximum_target_width > ABSOLUTE_MAXIMUM_TARGET_WIDTH:
        raise MultiTimeBulkLimitError("maximum_target_width exceeds absolute cap")

    one_step = verify_one_step_bulk()
    cones = verify_multitime_cones(maximum_lag)
    surjectivity = verify_block_surjectivity(maximum_lag, maximum_target_width)
    payload = {
        "one_step_bulk": one_step,
        "multitime_cones": cones,
        "block_surjectivity": surjectivity,
        "exact_conclusions": {
            "bulk_ca": (
                "the normalized zero recurrence has one branch-independent "
                "radius-two bulk cellular rule outside its four-bit boundary layer"
            ),
            "bounded_lag_no_go": (
                "a fixed k-block seam comparison leaves a constructively free "
                "interior; no bounded-lag local identity can bridge arbitrary "
                "low and high boundary data"
            ),
            "next_target": (
                "use lags growing with the seam width, a nonlocal spacetime "
                "quantity, or a theorem special to the actual fringe orbit"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-multitime-bulk-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-lag", type=int, default=DEFAULT_MAXIMUM_LAG)
    parser.add_argument(
        "--maximum-target-width", type=int, default=DEFAULT_MAXIMUM_TARGET_WIDTH
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    started = time.perf_counter()
    result = run_campaign(args.maximum_lag, args.maximum_target_width)
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-multitime-bulk-v1",
        "question": "problem1",
        "hypothesis": (
            "A fixed-lag comparison of two moving seams might bridge the free "
            "middle and distinguish an eventually finite survivor."
        ),
        "status": "partial-proof",
        "parameters": {
            "maximum_lag": args.maximum_lag,
            "maximum_target_width": args.maximum_target_width,
        },
        "result_summary": result,
        "interpretation": (
            "The opposite occurs: the schedule affects only a boundary cone, "
            "while the common interior is a right-permutive radius-two CA. "
            "Every finite later middle word remains realizable at fixed lag."
        ),
        "limitations": [
            "does not address lags that grow with the seam or state width",
            "does not classify nonlocal or actual-orbit-specific quantities",
            "does not prove the alternating inverse lift has infinite support",
            "does not exclude eventual center period two",
            "does not solve Rule 30 center nonperiodicity",
        ],
        "backend": "python-exact-boolean-exhaustion",
        "runtime_seconds": round(time.perf_counter() - started, 6),
        "hardware": {
            "environment": "isolated Linux CPU sandbox",
            "cpu_threads_used": 1,
            "gpu_used": False,
            "maximum_resident_set_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        },
        "software": {
            "implementation": "CPython",
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
    }
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
