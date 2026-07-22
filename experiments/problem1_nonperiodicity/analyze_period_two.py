#!/usr/bin/env python3
"""Test the smallest unresolved eventual period: an alternating center tail.

This campaign checks three concrete proof mechanisms:

1. whether the exact two-step five-cell cone restricts the two cells to the
   right of the center;
2. whether an alternating center alone forces a small bound on zero runs in
   the sideways-reconstructed initial-left word; and
3. whether a finite right half under a forced alternating boundary quickly
   makes its adjacent column periodic.

The finite counterexamples emitted here stop those narrow mechanisms.  They do
not construct an eventually period-two center from a finite Rule 30 seed and
do not disprove a different period-two invariant.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any

from rule30lab.two_adic import inverse_diagonal_map_mod, minus_one_third_mod


DEFAULT_RECONSTRUCTION_HORIZON = 16
DEFAULT_LIFT_WIDTH = 1_024
DEFAULT_HALF_LINE_STEPS = 4_096
MAX_RECONSTRUCTION_HORIZON = 18
MAX_LIFT_WIDTH = 4_096
MAX_HALF_LINE_STEPS = 8_192
MAX_SPATIAL_PERIOD = 128
MAX_SPATIAL_PREPERIOD = 128
MIN_SPATIAL_REPEATS = 4
HALF_LINE_SUFFIX_WINDOW = 1_024
HALF_LINE_MAX_PERIOD = 256
CANDIDATE_MAX_ZERO_RUN = 7


class PeriodTwoLimitError(RuntimeError):
    """Raised before a configured finite-work cap is crossed."""


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def local_update(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def shrinking_step(row: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        local_update(row[index], row[index + 1], row[index + 2])
        for index in range(len(row) - 2)
    )


def exact_phase_patterns(center: int) -> list[str]:
    """Return every five-cell row producing the next two alternating bits."""

    if center not in (0, 1):
        raise ValueError("center must be zero or one")
    patterns: list[str] = []
    for assignment in range(1 << 5):
        row = tuple((assignment >> index) & 1 for index in range(5))
        if row[2] != center:
            continue
        after_one = shrinking_step(row)
        after_two = shrinking_step(after_one)
        if after_one[1] == (center ^ 1) and after_two[0] == center:
            patterns.append("".join(str(bit) for bit in row))
    return patterns


def reconstruct_from_adjacent_columns(
    center: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    """Sideways-reconstruct time-zero left cells from two supplied columns."""

    if len(center) != len(right) or not center:
        raise ValueError("center and right columns must have equal positive length")
    if any(bit not in (0, 1) for bit in center + right):
        raise ValueError("columns must be binary")
    current = list(center)
    neighbor = list(right)
    initial_left: list[int] = []
    while len(current) > 1:
        new_column = [
            current[time + 1] ^ (current[time] | neighbor[time])
            for time in range(len(current) - 1)
        ]
        initial_left.append(new_column[0])
        neighbor = current[:-1]
        current = new_column
    return tuple(initial_left)


def longest_zero_run(bits: tuple[int, ...]) -> tuple[int, int]:
    """Return the longest zero-run length and its first zero-based index."""

    best_length = 0
    best_start = 0
    current_length = 0
    current_start = 0
    for index, bit in enumerate(bits):
        if bit == 0:
            if current_length == 0:
                current_start = index
            current_length += 1
            if current_length > best_length:
                best_length = current_length
                best_start = current_start
        else:
            current_length = 0
    return best_length, best_start


def first_adjacent_trace_extension_failure(
    center: tuple[int, ...], right: tuple[int, ...]
) -> int | None:
    """Find the first time no binary cell two can realize ``right[t+1]``."""

    if len(center) != len(right) or not center:
        raise ValueError("center and right columns must have equal positive length")
    for time in range(len(center) - 1):
        if not any(
            local_update(center[time], right[time], far_right)
            == right[time + 1]
            for far_right in (0, 1)
        ):
            return time
    return None


def _reconstruction_phase_summary(phase: int, horizon: int) -> dict[str, Any]:
    center = tuple((phase + time) & 1 for time in range(horizon + 1))
    maximum = -1
    witness_word = 0
    witness_left: tuple[int, ...] = ()
    witness_start = 0
    for right_word in range(1 << (horizon + 1)):
        right = tuple(
            (right_word >> time) & 1 for time in range(horizon + 1)
        )
        left = reconstruct_from_adjacent_columns(center, right)
        length, start = longest_zero_run(left)
        if length > maximum:
            maximum = length
            witness_word = right_word
            witness_left = left
            witness_start = start
    right_bits = tuple(
        (witness_word >> time) & 1 for time in range(horizon + 1)
    )
    extension_failure = first_adjacent_trace_extension_failure(
        center, right_bits
    )
    return {
        "center_phase_at_time_zero": phase,
        "right_traces_exhausted": 1 << (horizon + 1),
        "maximum_reconstructed_zero_run": maximum,
        "witness_zero_run_start_depth": witness_start + 1,
        "witness_right_trace_time_order": "".join(map(str, right_bits)),
        "witness_reconstructed_left_depth_order": "".join(
            map(str, witness_left)
        ),
        "witness_has_local_rule30_right_extension": extension_failure is None,
        "witness_first_local_extension_failure_time": extension_failure,
    }


def forced_half_line_trace_packed(
    seed: int, steps: int, *, phase: int = 0
) -> bytes:
    """Trace cell one with a forced alternating cell-zero boundary."""

    if seed < 0 or steps <= 0 or phase not in (0, 1):
        raise ValueError("invalid half-line parameters")
    width = max(2, seed.bit_length() + steps + 3)
    mask = (1 << width) - 1
    row = (seed << 1) | phase
    output = bytearray(steps)
    for time in range(steps):
        output[time] = (row >> 1) & 1
        row = ((row << 1) ^ (row | (row >> 1))) & mask
        row = (row & ~1) | ((phase + time + 1) & 1)
    return bytes(output)


def forced_half_line_trace_cell_array(
    seed: int, steps: int, *, phase: int = 0
) -> bytes:
    """Independent ordinary-cell evaluator of the same forced half-line."""

    if seed < 0 or steps <= 0 or phase not in (0, 1):
        raise ValueError("invalid half-line parameters")
    width = max(2, seed.bit_length() + steps + 3)
    row = [phase] + [
        (seed >> (position - 1)) & 1 for position in range(1, width)
    ]
    output = bytearray(steps)
    for time in range(steps):
        output[time] = row[1]
        row = [(phase + time + 1) & 1] + [
            row[position - 1] ^ (row[position] | row[position + 1])
            for position in range(1, width - 1)
        ] + [0]
    return bytes(output)


def matching_suffix_period(
    bits: bytes, *, window: int, maximum_period: int
) -> int | None:
    if (
        window <= 0
        or maximum_period <= 0
        or maximum_period >= window
        or window > len(bits)
    ):
        raise ValueError("invalid suffix-period parameters")
    start = len(bits) - window
    for period in range(1, maximum_period + 1):
        if all(
            bits[index] == bits[index - period]
            for index in range(start + period, len(bits))
        ):
            return period
    return None


def least_spatial_period(bits: bytes) -> tuple[int, int] | None:
    """Find a bounded period only when at least four repeats are compared."""

    for start in range(min(MAX_SPATIAL_PREPERIOD, len(bits)) + 1):
        for period in range(1, MAX_SPATIAL_PERIOD + 1):
            if len(bits) - start < MIN_SPATIAL_REPEATS * period:
                continue
            if all(
                bits[index] == bits[index - period]
                for index in range(start + period, len(bits))
            ):
                return start, period
    return None


def run_campaign(
    *, reconstruction_horizon: int,
    lift_width: int,
    half_line_steps: int,
) -> dict[str, Any]:
    """Run the bounded period-two mechanism audit."""

    if any(
        not isinstance(value, int)
        or isinstance(value, bool)
        or value <= 0
        for value in (reconstruction_horizon, lift_width, half_line_steps)
    ):
        raise ValueError("campaign bounds must be positive integers")
    if reconstruction_horizon > MAX_RECONSTRUCTION_HORIZON:
        raise PeriodTwoLimitError("reconstruction horizon exceeds configured cap")
    if lift_width > MAX_LIFT_WIDTH:
        raise PeriodTwoLimitError("lift width exceeds configured cap")
    if half_line_steps > MAX_HALF_LINE_STEPS:
        raise PeriodTwoLimitError("half-line steps exceed configured cap")
    if half_line_steps < HALF_LINE_SUFFIX_WINDOW:
        raise ValueError("half-line steps must cover the suffix window")

    phase_patterns = {
        str(phase): exact_phase_patterns(phase) for phase in (0, 1)
    }
    right_pair_projections = {
        phase: {
            (int(pattern[3]), int(pattern[4]))
            for pattern in phase_patterns[str(phase)]
        }
        for phase in (0, 1)
    }

    reconstruction = [
        _reconstruction_phase_summary(phase, reconstruction_horizon)
        for phase in (0, 1)
    ]

    trace_value = minus_one_third_mod(lift_width)
    lift_value = inverse_diagonal_map_mod(trace_value, lift_width)
    lift_bytes = lift_value.to_bytes((lift_width + 7) // 8, "little")
    lift_bits = bytes(
        (lift_value >> position) & 1 for position in range(lift_width)
    )

    packed_half_line = forced_half_line_trace_packed(0, half_line_steps)
    direct_half_line = forced_half_line_trace_cell_array(0, half_line_steps)
    if packed_half_line != direct_half_line:
        raise AssertionError("independent forced-half-line evaluators disagree")
    half_line_period = matching_suffix_period(
        packed_half_line,
        window=HALF_LINE_SUFFIX_WINDOW,
        maximum_period=HALF_LINE_MAX_PERIOD,
    )

    boundary_nor_verified = all(
        (
            # Start at a zero-center phase, update the first two right cells,
            # then update cell one from the next one-center phase.
            1
            ^ (
                (first | second)
                | (first ^ (second | third))
            )
        )
        == (1 ^ (first | second | third))
        for first in (0, 1)
        for second in (0, 1)
        for third in (0, 1)
    )

    zero_gap_refuted = any(
        summary["maximum_reconstructed_zero_run"]
        > CANDIDATE_MAX_ZERO_RUN
        for summary in reconstruction
    )
    cone_clause = (
        "The exact period-two cone leaves both right cells unrestricted."
    )
    if zero_gap_refuted:
        gap_clause = (
            "An arbitrary adjacent-right trace defeats the candidate "
            f"zero-run bound {CANDIDATE_MAX_ZERO_RUN}; the recorded witness "
            "is locally incompatible with a Rule 30 right-half continuation."
        )
    else:
        gap_clause = (
            "The candidate arbitrary-column zero-run bound "
            f"{CANDIDATE_MAX_ZERO_RUN} was not refuted at this horizon."
        )
    if half_line_period is None:
        half_line_clause = (
            "The zero finite right half matches no period at most "
            f"{HALF_LINE_MAX_PERIOD} throughout the tested final window."
        )
    else:
        half_line_clause = (
            "The zero finite right half matches period "
            f"{half_line_period} throughout the tested final window."
        )

    result = {
        "status": "finite-exhaustive",
        "parameters": {
            "reconstruction_horizon": reconstruction_horizon,
            "lift_width": lift_width,
            "half_line_steps": half_line_steps,
            "half_line_suffix_window": HALF_LINE_SUFFIX_WINDOW,
            "half_line_maximum_period": HALF_LINE_MAX_PERIOD,
            "spatial_preperiod_cap": MAX_SPATIAL_PREPERIOD,
            "spatial_period_cap": MAX_SPATIAL_PERIOD,
            "minimum_spatial_repeats": MIN_SPATIAL_REPEATS,
            "candidate_maximum_reconstructed_zero_run": (
                CANDIDATE_MAX_ZERO_RUN
            ),
        },
        "resource_caps": {
            "maximum_reconstruction_horizon": MAX_RECONSTRUCTION_HORIZON,
            "maximum_lift_width": MAX_LIFT_WIDTH,
            "maximum_half_line_steps": MAX_HALF_LINE_STEPS,
        },
        "coverage": {
            "five_cell_assignments_exhausted": 1 << 5,
            "arbitrary_right_traces_exhausted": (
                2 * (1 << (reconstruction_horizon + 1))
            ),
            "sideways_logical_cell_updates": (
                2
                * (1 << (reconstruction_horizon + 1))
                * reconstruction_horizon
                * (reconstruction_horizon + 1)
                // 2
            ),
            "forced_half_line_steps_per_oracle": half_line_steps,
            "forced_half_line_oracles": 2,
            "two_adic_lift_bits": lift_width,
        },
        "exact_two_phase_cones": {
            "position_order": "x_-2,x_-1,x_0,x_1,x_2",
            "patterns_by_center_phase": phase_patterns,
            "right_pair_projection_counts": {
                str(phase): len(right_pair_projections[phase])
                for phase in (0, 1)
            },
            "all_four_right_pairs_allowed_in_both_phases": all(
                len(right_pair_projections[phase]) == 4 for phase in (0, 1)
            ),
        },
        "arbitrary_adjacent_right_column": reconstruction,
        "candidate_zero_run_bound_refuted": zero_gap_refuted,
        "pure_alternating_two_adic_lift": {
            "trace_residue": trace_value,
            "lift_ones": sum(lift_bits),
            "lift_last_one_position": lift_value.bit_length() - 1,
            "bounded_spatial_period": least_spatial_period(lift_bits),
            "lift_sha256_little_endian_packed": hashlib.sha256(
                lift_bytes
            ).hexdigest(),
        },
        "forced_finite_right_half": {
            "initial_right_seed": 0,
            "two_independent_evaluators_agree": True,
            "two_step_boundary_nor_identity_verified": boundary_nor_verified,
            "matching_suffix_period": half_line_period,
            "trace_sha256_u8": hashlib.sha256(packed_half_line).hexdigest(),
        },
        "interpretation": (
            f"{cone_clause} {gap_clause} {half_line_clause} These finite "
            "checks test narrow proof mechanisms; they do not exclude a "
            "different invariant using complete finite support."
        ),
    }
    certificate_payload = json.dumps(
        result,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("ascii")
    result["certificate_sha256"] = hashlib.sha256(
        certificate_payload
    ).hexdigest()
    return result


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reconstruction-horizon",
        type=_positive_integer,
        default=DEFAULT_RECONSTRUCTION_HORIZON,
    )
    parser.add_argument(
        "--lift-width", type=_positive_integer, default=DEFAULT_LIFT_WIDTH
    )
    parser.add_argument(
        "--half-line-steps",
        type=_positive_integer,
        default=DEFAULT_HALF_LINE_STEPS,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    campaign = run_campaign(
        reconstruction_horizon=args.reconstruction_horizon,
        lift_width=args.lift_width,
        half_line_steps=args.half_line_steps,
    )
    payload = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-mechanism-audit-v1",
        "question": "problem1",
        "hypothesis": (
            "For an alternating center, the exact five-cell cone may restrict "
            "the right pair; every tested arbitrary-right reconstruction may "
            "have zero runs at most seven; or the zero finite right half may "
            "match a period at most 256 throughout the final 1024 samples."
        ),
        "backend": "python-exhaustive-and-two-oracle",
        "parameters": campaign["parameters"],
        "result_summary": campaign,
        "status": campaign["status"],
        "proof_scope": (
            "Only the exact five-cell assignments, finite right-column box, "
            "bounded 2-adic lift prefix, and bounded half-line trace listed."
        ),
        "interpretation": campaign["interpretation"],
        "limitations": [
            "an arbitrary adjacent-right trace need not come from a finite right half",
            "the forced alternating boundary need not extend to a globally compatible finite-seed spacetime",
            "absence of a short spatial period does not prove 2-adic irrationality",
            "absence of a short suffix period does not prove temporal nonperiodicity",
            "the full finite-support period-two case remains open",
            "no result proves Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
