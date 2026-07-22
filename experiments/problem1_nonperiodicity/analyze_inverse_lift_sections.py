#!/usr/bin/env python3
"""Audit exact branch recurrences for inverse Rule 30 2-adic lifts.

The experiment has two deliberately bounded purposes:

1. exhaust finite quotients to check the even/odd branch identities and a
   section-schedule implementation of ``Delta^{-1}`` against independent
   direct evaluators;
2. test whether the resulting section schedules or truncated inverse
   sections close quickly on the pure alternating period-two trace.

The first purpose supports an all-width proof written separately.  The
second is only a finite obstruction test.  Failure to see a repeated section
does not prove that the lift has infinitely many nonzero bits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from math import isqrt
from typing import Any, Callable, Iterable

from rule30lab.two_adic import (
    diagonal_map_mod,
    inverse_diagonal_map_mod,
    right_edge_inverse_mod,
    right_edge_step_mod,
)


DEFAULT_MAXIMUM_WIDTH = 10
DEFAULT_TRACE_DEPTH = 16
DEFAULT_SECTION_LOOKAHEAD = 6
DEFAULT_DYADIC_PROBE_WIDTH = 256
DEFAULT_MAXIMUM_SCHEDULE_PERIOD = 4_096
ABSOLUTE_MAXIMUM_WIDTH = 12
ABSOLUTE_TRACE_DEPTH = 20
ABSOLUTE_SECTION_LOOKAHEAD = 8
ABSOLUTE_DYADIC_PROBE_WIDTH = 1_024
DEFAULT_MAXIMUM_WORK_POINTS = 2_000_000


class InverseLiftLimitError(RuntimeError):
    """Raised before a configured finite-work limit is crossed."""


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def diagonal_map_cell_array(seed: int, width: int) -> int:
    """Independent list-of-bits evaluator for the diagonal map."""

    if width <= 0:
        raise ValueError("width must be positive")
    if seed < 0 or seed >= (1 << width):
        raise ValueError("seed does not fit width")
    state = [(seed >> position) & 1 for position in range(width)]
    output = 0
    for time in range(width):
        output |= state[time] << time
        state = [
            state[position]
            ^ (
                (state[position - 1] if position >= 1 else 0)
                | (state[position - 2] if position >= 2 else 0)
            )
            for position in range(width)
        ]
    return output


def odd_tail_step_mod(tail: int, width: int) -> int:
    """Return ``P(tail)`` from ``T(1+2*tail)=1+2*P(tail)``."""

    if width <= 0:
        raise ValueError("width must be positive")
    if tail < 0 or tail >= (1 << width):
        raise ValueError("tail does not fit width")
    correction = 1
    if width >= 2 and (tail & 1) == 0:
        correction |= 2
    return right_edge_step_mod(tail, width) ^ correction


def odd_tail_step_cell_array(tail: int, width: int) -> int:
    """Independent per-bit evaluator for ``P``."""

    if width <= 0:
        raise ValueError("width must be positive")
    if tail < 0 or tail >= (1 << width):
        raise ValueError("tail does not fit width")
    bits = [(tail >> position) & 1 for position in range(width)]
    output_bits = [1 ^ bits[0]]
    if width >= 2:
        output_bits.append(1 ^ bits[1])
    for position in range(2, width):
        output_bits.append(
            bits[position] ^ (bits[position - 1] | bits[position - 2])
        )
    return sum(bit << position for position, bit in enumerate(output_bits))


def _diagonal_for_step(
    seed: int,
    width: int,
    step: Callable[[int, int], int],
) -> int:
    state = seed
    output = 0
    for time in range(width):
        output |= ((state >> time) & 1) << time
        state = step(state, width)
    return output


def _invert_permutation(images: Iterable[int], size: int) -> list[int]:
    inverse = [-1] * size
    for source, image in enumerate(images):
        if image < 0 or image >= size or inverse[image] != -1:
            raise AssertionError("candidate map is not a permutation")
        inverse[image] = source
    if any(value < 0 for value in inverse):
        raise AssertionError("candidate map does not cover the quotient")
    return inverse


# Binary-tree sections of the three forward maps used by the recurrence.
# If F(a+2R)=pi_F(a)+2F_a(R), the tuple stores (F_0,F_1).
_ROOT_FLIP = {"T": 0, "P": 1, "U": 1, "t": 0, "p": 1, "u": 1}
_FORWARD_SECTIONS = {
    "T": ("T", "P"),
    "P": ("U", "P"),
    "U": ("T", "P"),
}
_INVERSE_SECTIONS = {
    "t": ("t", "p"),
    "p": ("p", "u"),
    "u": ("p", "t"),
}
_INVERSE_NAME = {"T": "t", "P": "p", "U": "u"}


def _primitive_period(word: tuple[str, ...]) -> tuple[str, ...]:
    length = len(word)
    divisors: set[int] = set()
    for candidate in range(1, isqrt(length) + 1):
        if length % candidate == 0:
            divisors.add(candidate)
            divisors.add(length // candidate)
    for candidate in sorted(divisors):
        if all(word[index] == word[index % candidate] for index in range(length)):
            return word[:candidate]
    raise AssertionError("a finite word must be periodic with its full length")


def advance_section_schedule(
    schedule: tuple[str, ...],
    root: int,
    *,
    maximum_period: int,
) -> tuple[str, tuple[str, ...]]:
    """Return ``B_0`` and the shifted tail schedule in the exact recurrence."""

    if not schedule or any(name not in _FORWARD_SECTIONS for name in schedule):
        raise ValueError("invalid forward schedule")
    if root not in (0, 1):
        raise ValueError("root must be binary")
    root_flip_over_period = sum(_ROOT_FLIP[name] for name in schedule) & 1
    expanded_length = len(schedule) * (2 if root_flip_over_period else 1)
    if expanded_length > maximum_period:
        raise InverseLiftLimitError(
            f"section schedule period {expanded_length} exceeds configured "
            f"maximum {maximum_period}"
        )

    current_root = root
    tail_schedule: list[str] = []
    for time in range(expanded_length):
        name = schedule[time % len(schedule)]
        tail_schedule.append(_FORWARD_SECTIONS[name][current_root])
        current_root ^= _ROOT_FLIP[name]

    first = tail_schedule[0]
    shifted = tuple(tail_schedule[1:] + tail_schedule[:1])
    return first, _primitive_period(shifted)


def _inverse_word_root(word: tuple[str, ...], root: int) -> int:
    return root ^ (sum(_ROOT_FLIP[name] for name in word) & 1)


def _inverse_word_section(
    word: tuple[str, ...], root: int
) -> tuple[str, ...]:
    """Section a composition word written outermost to innermost."""

    selected = [""] * len(word)
    current_root = root
    for index in range(len(word) - 1, -1, -1):
        name = word[index]
        selected[index] = _INVERSE_SECTIONS[name][current_root]
        current_root ^= _ROOT_FLIP[name]
    return tuple(selected)


def inverse_via_section_schedule(
    trace: int,
    width: int,
    *,
    maximum_schedule_period: int = DEFAULT_MAXIMUM_SCHEDULE_PERIOD,
) -> tuple[int, list[int]]:
    """Invert ``Delta`` bit by bit using the exact section recurrence."""

    if width <= 0:
        raise ValueError("width must be positive")
    if trace < 0 or trace >= (1 << width):
        raise ValueError("trace does not fit width")
    if maximum_schedule_period <= 0:
        raise ValueError("maximum schedule period must be positive")

    schedule = ("T",)
    postcomposition: tuple[str, ...] = ()
    seed = 0
    periods: list[int] = []
    for position in range(width):
        trace_bit = (trace >> position) & 1
        seed_bit = _inverse_word_root(postcomposition, trace_bit)
        seed |= seed_bit << position
        first, next_schedule = advance_section_schedule(
            schedule,
            trace_bit,
            maximum_period=maximum_schedule_period,
        )
        postcomposition = _inverse_word_section(
            postcomposition, trace_bit
        ) + (_INVERSE_NAME[first],)
        schedule = next_schedule
        periods.append(len(schedule))
    return seed, periods


def _table_bytes(values: list[int], width: int) -> bytes:
    bytes_per_value = (width + 7) // 8
    return b"".join(
        value.to_bytes(bytes_per_value, "little") for value in values
    )


def _analyze_width(
    width: int,
    *,
    maximum_schedule_period: int,
) -> tuple[dict[str, Any], bytes]:
    size = 1 << width
    cell_images = [diagonal_map_cell_array(seed, width) for seed in range(size)]
    cell_inverse = _invert_permutation(cell_images, size)
    packaged_images = [diagonal_map_mod(seed, width) for seed in range(size)]
    if packaged_images != cell_images:
        raise AssertionError(f"diagonal evaluators disagree at width {width}")

    maximum_observed_schedule_period = 0
    recurrence_inverse: list[int] = []
    for trace in range(size):
        recursive_seed, periods = inverse_via_section_schedule(
            trace,
            width,
            maximum_schedule_period=maximum_schedule_period,
        )
        packaged_seed = inverse_diagonal_map_mod(trace, width)
        if recursive_seed != packaged_seed or packaged_seed != cell_inverse[trace]:
            raise AssertionError(
                f"inverse oracles disagree at width={width}, trace={trace}"
            )
        recurrence_inverse.append(recursive_seed)
        maximum_observed_schedule_period = max(
            maximum_observed_schedule_period, max(periods)
        )

    for state in range(size):
        inverse = right_edge_inverse_mod(state, width)
        if (
            right_edge_step_mod(inverse, width) != state
            or right_edge_inverse_mod(right_edge_step_mod(state, width), width)
            != state
        ):
            raise AssertionError(f"right-edge inverse failed at width {width}")

    even_branch_points = 0
    odd_branch_points = 0
    if width >= 2:
        tail_width = width - 1
        tail_size = 1 << tail_width
        p_steps = [odd_tail_step_mod(tail, tail_width) for tail in range(tail_size)]
        if p_steps != [
            odd_tail_step_cell_array(tail, tail_width)
            for tail in range(tail_size)
        ]:
            raise AssertionError(f"odd-tail evaluators disagree at width {width}")
        p_step_inverse = _invert_permutation(p_steps, tail_size)
        p_diagonal = [
            _diagonal_for_step(seed, tail_width, odd_tail_step_mod)
            for seed in range(tail_size)
        ]
        p_diagonal_cell = [
            _diagonal_for_step(seed, tail_width, odd_tail_step_cell_array)
            for seed in range(tail_size)
        ]
        if p_diagonal != p_diagonal_cell:
            raise AssertionError(f"odd diagonal evaluators disagree at width {width}")
        p_diagonal_inverse = _invert_permutation(p_diagonal, tail_size)

        for tail in range(tail_size):
            if right_edge_step_mod(2 * tail, width) != 2 * right_edge_step_mod(
                tail, tail_width
            ):
                raise AssertionError("T(2S)=2T(S) failed")
            if diagonal_map_mod(2 * tail, width) != 2 * diagonal_map_mod(
                right_edge_step_mod(tail, tail_width), tail_width
            ):
                raise AssertionError("even diagonal branch identity failed")
            if right_edge_step_mod(1 + 2 * tail, width) != (
                1 + 2 * p_steps[tail]
            ):
                raise AssertionError("odd T branch identity failed")
            if diagonal_map_mod(1 + 2 * tail, width) != (
                1 + 2 * p_diagonal[p_steps[tail]]
            ):
                raise AssertionError("odd diagonal branch identity failed")
            even_branch_points += 1
            odd_branch_points += 1

        for trace_tail in range(tail_size):
            even_lift = inverse_diagonal_map_mod(2 * trace_tail, width)
            expected_even_lift = 2 * right_edge_inverse_mod(
                inverse_diagonal_map_mod(trace_tail, tail_width), tail_width
            )
            if even_lift != expected_even_lift:
                raise AssertionError("even inverse branch identity failed")

            odd_lift = inverse_diagonal_map_mod(1 + 2 * trace_tail, width)
            expected_odd_lift = 1 + 2 * p_step_inverse[
                p_diagonal_inverse[trace_tail]
            ]
            if odd_lift != expected_odd_lift:
                raise AssertionError("odd inverse branch identity failed")
            even_branch_points += 1
            odd_branch_points += 1

    table_data = _table_bytes(packaged_images, width) + _table_bytes(
        recurrence_inverse, width
    )
    summary = {
        "width": width,
        "quotient_size": size,
        "three_inverse_oracles_agree": True,
        "right_edge_inverse_verified_both_directions": True,
        "even_and_odd_branch_identities_verified": True,
        "even_branch_points_checked": even_branch_points,
        "odd_branch_points_checked": odd_branch_points,
        "maximum_observed_schedule_period": maximum_observed_schedule_period,
        "map_and_inverse_sha256": hashlib.sha256(table_data).hexdigest(),
    }
    return summary, table_data


def _control_trace(name: str, width: int) -> int:
    if width < 0:
        raise ValueError("width must be nonnegative")
    if name == "zero":
        return 0
    if name == "single_one":
        return 1 if width else 0
    if name == "constant_one":
        return (1 << width) - 1
    if name == "alternating_one_zero":
        return sum(1 << position for position in range(0, width, 2))
    raise ValueError("unknown control trace")


def _longest_zero_run(bits: str) -> int:
    longest = 0
    current = 0
    for bit in bits:
        if bit == "0":
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return longest


def _inverse_section_table(
    *,
    prefix: int,
    prefix_depth: int,
    lookahead: int,
    maximum_schedule_period: int,
) -> bytes:
    mask = (1 << lookahead) - 1
    direct_values: list[int] = []
    recursive_values: list[int] = []
    total_width = prefix_depth + lookahead
    for continuation in range(1 << lookahead):
        trace = prefix | (continuation << prefix_depth)
        direct_values.append(
            (inverse_diagonal_map_mod(trace, total_width) >> prefix_depth)
            & mask
        )
        recursive_seed, _ = inverse_via_section_schedule(
            trace,
            total_width,
            maximum_schedule_period=maximum_schedule_period,
        )
        recursive_values.append((recursive_seed >> prefix_depth) & mask)
    if direct_values != recursive_values:
        raise AssertionError("truncated inverse-section oracles disagree")
    return _table_bytes(direct_values, lookahead)


def _analyze_control(
    name: str,
    *,
    trace_depth: int,
    section_lookahead: int,
    maximum_schedule_period: int,
) -> tuple[dict[str, Any], bytes]:
    trace = _control_trace(name, trace_depth)
    seed, periods = inverse_via_section_schedule(
        trace,
        trace_depth,
        maximum_schedule_period=maximum_schedule_period,
    )
    if inverse_diagonal_map_mod(trace, trace_depth) != seed:
        raise AssertionError("control inverse implementations disagree")
    if diagonal_map_cell_array(seed, trace_depth) != trace:
        raise AssertionError("control inverse fails independent forward oracle")
    seed_bits = "".join(str((seed >> position) & 1) for position in range(trace_depth))

    prefix = 0
    section_tables: list[bytes] = []
    section_hashes: list[str] = []
    for depth in range(trace_depth + 1):
        table = _inverse_section_table(
            prefix=prefix,
            prefix_depth=depth,
            lookahead=section_lookahead,
            maximum_schedule_period=maximum_schedule_period,
        )
        section_tables.append(table)
        section_hashes.append(hashlib.sha256(table).hexdigest())
        if depth < trace_depth:
            prefix |= ((trace >> depth) & 1) << depth

    repeated_pairs = [
        [first, second]
        for second in range(len(section_tables))
        for first in range(second)
        if section_tables[first] == section_tables[second]
    ]
    dyadic_extensions = []
    block_width = 1
    while 2 * block_width <= trace_depth:
        mask = (1 << block_width) - 1
        dyadic_extensions.append(
            {
                "block_width": block_width,
                "lower_prefix": seed & mask,
                "extension_block": (seed >> block_width) & mask,
            }
        )
        block_width *= 2

    last_one = max(
        (position for position, bit in enumerate(seed_bits) if bit == "1"),
        default=None,
    )
    summary = {
        "name": name,
        "trace_residue": trace,
        "inverse_seed_residue": seed,
        "inverse_seed_bits_lsb_first": seed_bits,
        "inverse_seed_ones": seed.bit_count(),
        "inverse_seed_last_one": last_one,
        "inverse_seed_longest_zero_run": _longest_zero_run(seed_bits),
        "section_schedule_periods_after_each_bit": periods,
        "maximum_section_schedule_period": max(periods),
        "truncated_section_lookahead": section_lookahead,
        "truncated_section_hashes_by_prefix_depth": section_hashes,
        "distinct_truncated_sections": len(set(section_tables)),
        "repeated_truncated_section_depth_pairs": repeated_pairs,
        "dyadic_extension_blocks": dyadic_extensions,
    }
    certificate_data = (
        trace.to_bytes((trace_depth + 7) // 8, "little")
        + seed.to_bytes((trace_depth + 7) // 8, "little")
        + b"".join(section_tables)
        + b"".join(period.to_bytes(4, "little") for period in periods)
    )
    return summary, certificate_data


def _analyze_dyadic_probe(width: int) -> tuple[dict[str, Any], bytes]:
    trace = _control_trace("alternating_one_zero", width)
    seed = inverse_diagonal_map_mod(trace, width)
    if diagonal_map_cell_array(seed, width) != trace:
        raise AssertionError("dyadic probe failed independent forward oracle")
    samples = []
    exponent = 1
    while (1 << exponent) - 1 < width:
        position = (1 << exponent) - 1
        bit = (seed >> position) & 1
        samples.append(
            {
                "exponent": exponent,
                "position": position,
                "bit": bit,
                "equals_exponent_parity": bit == (exponent & 1),
            }
        )
        exponent += 1
    packed = seed.to_bytes((width + 7) // 8, "little")
    return (
        {
            "width": width,
            "samples": samples,
            "all_samples_equal_exponent_parity": all(
                sample["equals_exponent_parity"] for sample in samples
            ),
            "lift_ones": seed.bit_count(),
            "lift_last_one_position": seed.bit_length() - 1,
            "lift_sha256_little_endian_packed": hashlib.sha256(packed).hexdigest(),
        },
        packed,
    )


def run_campaign(
    *,
    maximum_width: int = DEFAULT_MAXIMUM_WIDTH,
    trace_depth: int = DEFAULT_TRACE_DEPTH,
    section_lookahead: int = DEFAULT_SECTION_LOOKAHEAD,
    dyadic_probe_width: int = DEFAULT_DYADIC_PROBE_WIDTH,
    maximum_schedule_period: int = DEFAULT_MAXIMUM_SCHEDULE_PERIOD,
    maximum_work_points: int = DEFAULT_MAXIMUM_WORK_POINTS,
) -> dict[str, Any]:
    """Run the bounded quotient and period-two section audit."""

    values = (
        maximum_width,
        trace_depth,
        section_lookahead,
        dyadic_probe_width,
        maximum_schedule_period,
        maximum_work_points,
    )
    if any(
        not isinstance(value, int) or isinstance(value, bool) or value <= 0
        for value in values
    ):
        raise ValueError("all widths and resource limits must be positive integers")
    if maximum_width > ABSOLUTE_MAXIMUM_WIDTH:
        raise InverseLiftLimitError(
            f"quotient width {maximum_width} exceeds absolute maximum "
            f"{ABSOLUTE_MAXIMUM_WIDTH}"
        )
    if trace_depth > ABSOLUTE_TRACE_DEPTH:
        raise InverseLiftLimitError(
            f"trace depth {trace_depth} exceeds absolute maximum "
            f"{ABSOLUTE_TRACE_DEPTH}"
        )
    if section_lookahead > ABSOLUTE_SECTION_LOOKAHEAD:
        raise InverseLiftLimitError(
            f"section lookahead {section_lookahead} exceeds absolute maximum "
            f"{ABSOLUTE_SECTION_LOOKAHEAD}"
        )
    if dyadic_probe_width > ABSOLUTE_DYADIC_PROBE_WIDTH:
        raise InverseLiftLimitError(
            f"dyadic probe width {dyadic_probe_width} exceeds absolute maximum "
            f"{ABSOLUTE_DYADIC_PROBE_WIDTH}"
        )

    quotient_points = (1 << (maximum_width + 1)) - 2
    control_names = (
        "zero",
        "single_one",
        "constant_one",
        "alternating_one_zero",
    )
    section_points = (
        len(control_names) * (trace_depth + 1) * (1 << section_lookahead)
    )
    work_points = quotient_points + section_points + dyadic_probe_width**2
    if work_points > maximum_work_points:
        raise InverseLiftLimitError(
            f"estimated {work_points} work points exceed configured maximum "
            f"{maximum_work_points}"
        )

    certificate = hashlib.sha256()
    certificate.update(b"rule30-inverse-lift-sections-certificate-v1\0")
    width_summaries = []
    for width in range(1, maximum_width + 1):
        summary, table_data = _analyze_width(
            width,
            maximum_schedule_period=maximum_schedule_period,
        )
        width_summaries.append(summary)
        certificate.update(width.to_bytes(2, "little"))
        certificate.update(table_data)

    controls = []
    for name in control_names:
        summary, control_data = _analyze_control(
            name,
            trace_depth=trace_depth,
            section_lookahead=section_lookahead,
            maximum_schedule_period=maximum_schedule_period,
        )
        controls.append(summary)
        certificate.update(name.encode("ascii") + b"\0")
        certificate.update(control_data)

    dyadic_probe, dyadic_probe_data = _analyze_dyadic_probe(dyadic_probe_width)
    certificate.update(b"dyadic-probe\0")
    certificate.update(dyadic_probe_data)

    alternating = next(
        summary for summary in controls if summary["name"] == "alternating_one_zero"
    )
    alternating_seed = alternating["inverse_seed_residue"]
    block_controls: dict[str, Any] = {}
    if trace_depth >= 4:
        prefix_two = alternating_seed & 0b11
        extension_two = (alternating_seed >> 2) & 0b11
        block_controls["independent_phase_block_at_width_two"] = {
            "prefix": prefix_two,
            "extension": extension_two,
            "extension_equals_prefix": extension_two == prefix_two,
        }
    if trace_depth >= 10:
        prefix_three = alternating_seed & 0b111
        prefix_five = alternating_seed & 0b1_1111
        extension_three = (alternating_seed >> 3) & 0b111
        extension_five = (alternating_seed >> 5) & 0b1_1111
        block_controls["same_prefix_and_phase_at_widths_three_and_five"] = {
            "prefix_width_three": prefix_three,
            "prefix_width_five": prefix_five,
            "extension_width_three": extension_three,
            "extension_width_five": extension_five,
            "extension_width_five_modulo_eight": extension_five & 0b111,
            "prefixes_equal": prefix_three == prefix_five,
            "low_three_extension_bits_disagree": (
                extension_three != (extension_five & 0b111)
            ),
        }
    if trace_depth >= 8:
        extension_two = (alternating_seed >> 2) & 0b11
        extension_four = (alternating_seed >> 4) & 0b1111
        complemented_two = extension_two ^ 0b11
        block_controls["dyadic_copy_and_complement_at_width_four"] = {
            "extension_width_two": extension_two,
            "extension_width_four": extension_four,
            "copied_width_two_prediction": extension_two | (extension_two << 2),
            "copied_complement_prediction": (
                complemented_two | (complemented_two << 2)
            ),
            "copy_prediction_matches": (
                extension_four == (extension_two | (extension_two << 2))
            ),
            "complement_prediction_matches": (
                extension_four
                == (complemented_two | (complemented_two << 2))
            ),
        }
    if trace_depth >= 12:
        bit_five = (alternating_seed >> 5) & 1
        bit_eleven = (alternating_seed >> 11) & 1
        block_controls["global_double_index_bit_rule_at_n_five"] = {
            "bit_n": bit_five,
            "bit_two_n_plus_one": bit_eleven,
            "predicted_bit_two_n_plus_one": 1 - bit_five,
            "rule_holds": bit_eleven == 1 - bit_five,
        }
    all_alternating_sections_distinct = (
        alternating["distinct_truncated_sections"] == trace_depth + 1
    )
    interpretation = (
        "The exact even/odd inverse-lift recurrence passed every listed "
        "finite quotient and independent-oracle check. For the pure "
        "alternating period-two trace, the induced forward-section schedule "
        f"reached period {alternating['maximum_section_schedule_period']} by "
        f"depth {trace_depth}; "
        + (
            "all tested truncated inverse sections were distinct. "
            if all_alternating_sections_distinct
            else "some tested truncated inverse sections repeated. "
        )
        + "The accompanying all-width argument proves that the universal "
        "diagonal map has infinitely many tree sections. Thus the recurrence "
        "is a valid structural reformulation, but a universal bounded-state "
        "closure is impossible. The dyadic-index lift-bit pattern is only a "
        f"finite induction candidate through width {dyadic_probe_width}. The "
        "next useful target is a period-specific "
        "proved quotient or invariant of the growing schedule/postcomposition "
        "state, not a larger prefix."
    )

    return {
        "status": "finite-exhaustive",
        "parameters": {
            "maximum_width": maximum_width,
            "trace_depth": trace_depth,
            "section_lookahead": section_lookahead,
            "dyadic_probe_width": dyadic_probe_width,
        },
        "resource_caps": {
            "absolute_maximum_width": ABSOLUTE_MAXIMUM_WIDTH,
            "absolute_trace_depth": ABSOLUTE_TRACE_DEPTH,
            "absolute_section_lookahead": ABSOLUTE_SECTION_LOOKAHEAD,
            "absolute_dyadic_probe_width": ABSOLUTE_DYADIC_PROBE_WIDTH,
            "maximum_schedule_period": maximum_schedule_period,
            "maximum_work_points": maximum_work_points,
        },
        "coverage": {
            "quotient_points_exhausted": quotient_points,
            "section_continuations_checked": section_points,
            "independent_diagonal_evaluators": 2,
            "inverse_oracles_compared": 3,
            "control_traces": len(control_names),
            "dyadic_probe_bits": dyadic_probe_width,
            "estimated_work_points": work_points,
        },
        "width_summaries": width_summaries,
        "control_summaries": controls,
        "period_two_block_controls": block_controls,
        "period_two_dyadic_index_probe": dyadic_probe,
        "all_finite_inverse_oracles_agree": all(
            summary["three_inverse_oracles_agree"] for summary in width_summaries
        ),
        "all_finite_branch_identities_pass": all(
            summary["even_and_odd_branch_identities_verified"]
            for summary in width_summaries
        ),
        "alternating_truncated_sections_all_distinct": (
            all_alternating_sections_distinct
        ),
        "certificate_sha256": certificate.hexdigest(),
        "interpretation": interpretation,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maximum-width", type=_positive_integer, default=DEFAULT_MAXIMUM_WIDTH
    )
    parser.add_argument(
        "--trace-depth", type=_positive_integer, default=DEFAULT_TRACE_DEPTH
    )
    parser.add_argument(
        "--section-lookahead",
        type=_positive_integer,
        default=DEFAULT_SECTION_LOOKAHEAD,
    )
    parser.add_argument(
        "--dyadic-probe-width",
        type=_positive_integer,
        default=DEFAULT_DYADIC_PROBE_WIDTH,
    )
    parser.add_argument(
        "--maximum-schedule-period",
        type=_positive_integer,
        default=DEFAULT_MAXIMUM_SCHEDULE_PERIOD,
    )
    parser.add_argument(
        "--maximum-work-points",
        type=_positive_integer,
        default=DEFAULT_MAXIMUM_WORK_POINTS,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    campaign = run_campaign(
        maximum_width=args.maximum_width,
        trace_depth=args.trace_depth,
        section_lookahead=args.section_lookahead,
        dyadic_probe_width=args.dyadic_probe_width,
        maximum_schedule_period=args.maximum_schedule_period,
        maximum_work_points=args.maximum_work_points,
    )
    payload = {
        "schema_version": 1,
        "experiment_id": "problem1-inverse-lift-sections-v1",
        "question": "problem1",
        "hypothesis": (
            "The exact inverse-lift branch recurrence is correct, and a "
            "periodic trace may induce a bounded recurring section state or "
            "a stable dyadic-index nonzero-bit invariant."
        ),
        "backend": "python-finite-exhaustive-three-oracle",
        "parameters": campaign["parameters"],
        "result_summary": campaign,
        "status": campaign["status"],
        "proof_scope": (
            "Every residue in the listed finite quotients and every listed "
            "bounded continuation table; the all-width recurrence is proved "
            "separately."
        ),
        "interpretation": campaign["interpretation"],
        "limitations": [
            "finite quotient checks do not prove the all-width recurrence",
            (
                "truncated section equality or inequality need not persist "
                "at larger lookahead"
            ),
            "schedule growth through the stated depth does not prove unbounded growth",
            "the dyadic-index pattern is checked only at the listed finite positions",
            "no bounded-state theorem for the inverse lift was established",
            "the result does not exclude eventual center period two",
            "the result does not prove Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
