#!/usr/bin/env python3
"""Audit two concrete period-two inverse-lift quotient candidates.

The pure alternating temporal trace has low-first bits ``1010...``.  This
experiment tests two proposed simplifications of its exact inverse lift:

* a seven-block cycle in the first state of the induced section schedule;
* parity of the inverse-lift bit at positions ``2**k - 1``.

It also identifies the schedule head with an exact two-cell spacetime fringe
and exhausts the four-state local transition relation for that fringe.  The
counterexamples emitted here refute only the named candidate quotients.  They
do not prove that every period-two quotient is impossible and do not resolve
Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import product
from math import isqrt
from typing import Any

from rule30lab.two_adic import (
    diagonal_map_mod,
    inverse_diagonal_map_mod,
    minus_one_third_mod,
    right_edge_step_mod,
)


DEFAULT_WIDTH = 2_048
DEFAULT_DRIVER_MAX_BLOCK = 160
DEFAULT_SCHEDULE_CROSSCHECK_BLOCKS = 12
DEFAULT_MAXIMUM_SCHEDULE_PERIOD = 8_192
DEFAULT_MAXIMUM_WORK_POINTS = 20_000_000
ABSOLUTE_WIDTH = 4_096
ABSOLUTE_DRIVER_MAX_BLOCK = 512
ABSOLUTE_SCHEDULE_CROSSCHECK_BLOCKS = 16
PERIOD_SEVEN_START_BLOCK = 2
PERIOD_SEVEN_WORD = ("U", "P", "T", "P", "T", "P", "P")


class PeriodTwoQuotientLimitError(RuntimeError):
    """Raised before a configured finite-work limit is crossed."""


_ROOT_FLIP = {"T": 0, "P": 1, "U": 1}
_FORWARD_SECTIONS = {
    "T": ("T", "P"),
    "P": ("U", "P"),
    "U": ("T", "P"),
}
_INVERSE_ROOT_FLIP = {"t": 0, "p": 1, "u": 1}
_INVERSE_SECTIONS = {
    "t": ("t", "p"),
    "p": ("p", "u"),
    "u": ("p", "t"),
}
_PORTRAIT_WORDS = ((), (0,), (1,), (0, 0), (0, 1), (1, 0), (1, 1))


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def diagonal_map_cell_array(seed: int, width: int) -> int:
    """Independent ordinary-bit evaluator of the finite diagonal map."""

    if width <= 0 or seed < 0 or seed >= (1 << width):
        raise ValueError("invalid finite diagonal arguments")
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


def section_head_for_pair(pair: tuple[int, int]) -> str:
    """Return the section of ``T`` after the low-prefix terminal pair.

    The pair is ``(r_2, r_1)``, where ``r_j`` is the bit at distance ``j``
    behind the sampled diagonal.  It is therefore the pair in increasing
    input-bit order.
    """

    if pair == (0, 0):
        return "T"
    if pair == (1, 0):
        return "U"
    if pair in ((0, 1), (1, 1)):
        return "P"
    raise ValueError("pair must contain exactly two binary values")


def fringe_pair_transition(
    pair: tuple[int, int], context: tuple[int, int]
) -> tuple[int, int]:
    """Advance the two-cell inward fringe by one temporal ``10`` block.

    ``pair=(r_2,r_1)`` and ``context=(r_3,r_4)``.  The even-phase diagonal
    bit is ``r_0=1``.  Two direct Rule 30 updates give the returned
    ``(r'_2,r'_1)``.
    """

    values = pair + context
    if any(value not in (0, 1) for value in values):
        raise ValueError("fringe values must be binary")
    r2, r1 = pair
    r3, r4 = context
    g0 = 1 ^ (r1 | r2)
    g1 = r1 ^ (r2 | r3)
    g2 = r2 ^ (r3 | r4)
    return g0 ^ (g1 | g2), g0 | g1


def fringe_pair_graph() -> dict[str, Any]:
    """Exhaust the four-state local fringe transition relation."""

    pairs = tuple(product((0, 1), repeat=2))
    adjacency: dict[tuple[int, int], set[tuple[int, int]]] = {
        pair: set() for pair in pairs
    }
    witnesses: dict[tuple[tuple[int, int], tuple[int, int]], tuple[int, int]] = {}
    assignments = 0
    for pair in pairs:
        for context in pairs:
            target = fringe_pair_transition(pair, context)
            adjacency[pair].add(target)
            witnesses.setdefault((pair, target), context)
            assignments += 1

    def reachable(start: tuple[int, int]) -> set[tuple[int, int]]:
        seen = {start}
        frontier = [start]
        while frontier:
            current = frontier.pop()
            for target in adjacency[current]:
                if target not in seen:
                    seen.add(target)
                    frontier.append(target)
        return seen

    strongly_connected = all(len(reachable(pair)) == len(pairs) for pair in pairs)
    cycle = ((0, 0), (0, 1), (1, 0), (1, 1), (0, 0))
    cycle_witnesses = []
    for source, target in zip(cycle[:-1], cycle[1:], strict=True):
        cycle_witnesses.append(
            {
                "source_pair": list(source),
                "context_r3_r4": list(witnesses[(source, target)]),
                "target_pair": list(target),
            }
        )

    return {
        "assignments_exhausted": assignments,
        "adjacency": {
            "".join(map(str, pair)): [
                "".join(map(str, target)) for target in sorted(adjacency[pair])
            ]
            for pair in pairs
        },
        "strongly_connected": strongly_connected,
        "explicit_directed_cycle": cycle_witnesses,
        "pair_only_monotone_observable_consequence": (
            "Every real-valued observable nondecreasing or nonincreasing on "
            "all allowed pair transitions is constant."
        ),
    }


def advance_fringe(tail: tuple[int, ...]) -> tuple[int, ...]:
    """Apply the exact two-step moving-fringe map with a zero far tail."""

    if not tail or any(value not in (0, 1) for value in tail):
        raise ValueError("tail must be a nonempty binary tuple")
    radius = len(tail)
    row = (1,) + tail + (0, 0)
    first_step = tuple(
        row[index] ^ (row[index + 1] | row[index + 2])
        for index in range(radius + 1)
    )
    return tuple(
        (0 if distance == 1 else first_step[distance - 2])
        ^ (first_step[distance - 1] | first_step[distance])
        for distance in range(1, radius + 1)
    )


def fringe_driver(maximum_block: int) -> tuple[list[str], list[tuple[int, int]]]:
    """Generate exact schedule heads from the autonomous zero-tail fringe."""

    if maximum_block < 0:
        raise ValueError("maximum block must be nonnegative")
    # Each block imports two farther cells.  This padding keeps the dependency
    # cone of r_1 and r_2 away from the artificial far boundary.
    tail_width = 2 * maximum_block + 8
    tail = (0,) * tail_width
    heads: list[str] = []
    pairs: list[tuple[int, int]] = []
    for block in range(maximum_block + 1):
        pair = (tail[1], tail[0])
        pairs.append(pair)
        heads.append(section_head_for_pair(pair))
        if block < maximum_block:
            tail = advance_fringe(tail)

    # A differently placed zero boundary is an independent finite-cone check.
    wider_tail = (0,) * (tail_width + 17)
    wider_heads: list[str] = []
    for block in range(maximum_block + 1):
        wider_heads.append(section_head_for_pair((wider_tail[1], wider_tail[0])))
        if block < maximum_block:
            wider_tail = advance_fringe(wider_tail)
    if wider_heads != heads:
        raise AssertionError("fringe driver depends on the artificial far boundary")
    return heads, pairs


def spacetime_driver(
    seed: int, width: int, maximum_block: int
) -> tuple[list[str], list[tuple[int, int]]]:
    """Generate schedule heads from rows ``T**(2m)(seed)`` independently."""

    row = seed
    heads: list[str] = []
    pairs: list[tuple[int, int]] = []
    for depth in range(2 * maximum_block + 1):
        if depth % 2 == 0:
            if depth == 0:
                pair = (0, 0)
            else:
                pair = (
                    (row >> (depth - 2)) & 1,
                    (row >> (depth - 1)) & 1,
                )
            pairs.append(pair)
            heads.append(section_head_for_pair(pair))
        if depth < 2 * maximum_block:
            row = right_edge_step_mod(row, width)
    return heads, pairs


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
    raise AssertionError("every finite word has its full length as a period")


def advance_section_schedule(
    schedule: tuple[str, ...], root: int, *, maximum_period: int
) -> tuple[str, ...]:
    """Apply one exact inverse-recursion schedule transition."""

    if not schedule or root not in (0, 1):
        raise ValueError("invalid schedule transition")
    flip = sum(_ROOT_FLIP[name] for name in schedule) & 1
    expanded_length = len(schedule) * (2 if flip else 1)
    if expanded_length > maximum_period:
        raise PeriodTwoQuotientLimitError(
            f"schedule period {expanded_length} exceeds maximum {maximum_period}"
        )
    current = root
    tails = []
    for time in range(expanded_length):
        name = schedule[time % len(schedule)]
        tails.append(_FORWARD_SECTIONS[name][current])
        current ^= _ROOT_FLIP[name]
    shifted = tuple(tails[1:] + tails[:1])
    return _primitive_period(shifted)


def exact_schedule_heads(
    maximum_block: int, *, maximum_period: int
) -> tuple[list[str], list[int]]:
    """Generate full schedules for a capped independent cross-check."""

    schedule = ("T",)
    heads: list[str] = []
    periods: list[int] = []
    for block in range(maximum_block + 1):
        heads.append(schedule[0])
        periods.append(len(schedule))
        if block < maximum_block:
            schedule = advance_section_schedule(
                schedule, 1, maximum_period=maximum_period
            )
            schedule = advance_section_schedule(
                schedule, 0, maximum_period=maximum_period
            )
    return heads, periods


def _inverse_word_root(word: tuple[str, ...], root: int) -> int:
    if root not in (0, 1):
        raise ValueError("root must be binary")
    return root ^ (sum(_INVERSE_ROOT_FLIP[name] for name in word) & 1)


def _inverse_word_section(
    word: tuple[str, ...], root: int
) -> tuple[str, ...]:
    """Section a composition word written outermost to innermost."""

    if root not in (0, 1):
        raise ValueError("root must be binary")
    selected = [""] * len(word)
    current = root
    for index in range(len(word) - 1, -1, -1):
        name = word[index]
        selected[index] = _INVERSE_SECTIONS[name][current]
        current ^= _INVERSE_ROOT_FLIP[name]
    return tuple(selected)


def _section_along(
    word: tuple[str, ...], path: tuple[int, ...]
) -> tuple[str, ...]:
    for root in path:
        word = _inverse_word_section(word, root)
    return word


def _depth_two_portrait(word: tuple[str, ...]) -> tuple[int, ...]:
    return tuple(
        _inverse_word_root(_section_along(word, path), 0)
        for path in _PORTRAIT_WORDS
    )


def _emitted_block(word: tuple[str, ...]) -> int:
    """Return the two seed bits emitted by the repeated temporal block 10."""

    return (1 ^ _inverse_word_root(word, 0)) + 2 * (
        1 ^ _inverse_word_root(_inverse_word_section(word, 1), 0)
    )


def depth_two_portrait_conflict(heads: list[str]) -> dict[str, Any] | None:
    """Find an actual-path failure of the depth-two portrait quotient."""

    if len(heads) < 2:
        return None
    words: list[tuple[str, ...]] = [()]
    for head in heads[:-1]:
        current = words[-1]
        section_11 = _section_along(current, (1, 1))
        words.append(
            section_11 + ("p", "u" if head == "T" else "t")
        )

    portraits = [_depth_two_portrait(word) for word in words]
    blocks = [_emitted_block(word) for word in words]
    first: dict[tuple[str, tuple[int, ...]], int] = {}
    for block in range(len(heads) - 1):
        key = (heads[block], portraits[block])
        previous = first.get(key)
        if previous is not None and (
            (blocks[previous + 1] == 0) != (blocks[block + 1] == 0)
        ):
            return {
                "portrait_word_order": [
                    "epsilon", "0", "1", "00", "01", "10", "11"
                ],
                "head": heads[block],
                "portrait": list(portraits[block]),
                "first_block": previous,
                "first_current_emitted_block": blocks[previous],
                "first_next_emitted_block": blocks[previous + 1],
                "conflicting_block": block,
                "conflicting_current_emitted_block": blocks[block],
                "conflicting_next_emitted_block": blocks[block + 1],
                "next_zero_status_differs": (
                    (blocks[previous + 1] == 0) != (blocks[block + 1] == 0)
                ),
            }
        first.setdefault(key, block)
    return None


def _first_period_mismatch(heads: list[str]) -> dict[str, Any] | None:
    for block in range(PERIOD_SEVEN_START_BLOCK, len(heads)):
        expected = PERIOD_SEVEN_WORD[
            (block - PERIOD_SEVEN_START_BLOCK) % len(PERIOD_SEVEN_WORD)
        ]
        if heads[block] != expected:
            return {
                "block": block,
                "expected_head": expected,
                "actual_head": heads[block],
                "matched_blocks_before_mismatch": block - PERIOD_SEVEN_START_BLOCK,
            }
    return None


def _first_head_only_transition_conflict(heads: list[str]) -> dict[str, Any] | None:
    first: dict[str, tuple[int, str]] = {}
    for block, (source, target) in enumerate(zip(heads, heads[1:], strict=False)):
        previous = first.get(source)
        if previous is not None and previous[1] != target:
            return {
                "head": source,
                "first_block": previous[0],
                "first_successor": previous[1],
                "conflicting_block": block,
                "conflicting_successor": target,
            }
        first.setdefault(source, (block, target))
    return None


def run_campaign(
    *,
    width: int = DEFAULT_WIDTH,
    driver_max_block: int = DEFAULT_DRIVER_MAX_BLOCK,
    schedule_crosscheck_blocks: int = DEFAULT_SCHEDULE_CROSSCHECK_BLOCKS,
    maximum_schedule_period: int = DEFAULT_MAXIMUM_SCHEDULE_PERIOD,
    maximum_work_points: int = DEFAULT_MAXIMUM_WORK_POINTS,
) -> dict[str, Any]:
    """Run the bounded period-two quotient-obstruction campaign."""

    values = (
        width,
        driver_max_block,
        schedule_crosscheck_blocks,
        maximum_schedule_period,
        maximum_work_points,
    )
    if any(value <= 0 for value in values):
        raise ValueError("all campaign limits must be positive")
    if width > ABSOLUTE_WIDTH:
        raise PeriodTwoQuotientLimitError(
            f"width {width} exceeds absolute maximum {ABSOLUTE_WIDTH}"
        )
    if driver_max_block > ABSOLUTE_DRIVER_MAX_BLOCK:
        raise PeriodTwoQuotientLimitError(
            "driver maximum block exceeds absolute maximum "
            f"{ABSOLUTE_DRIVER_MAX_BLOCK}"
        )
    if schedule_crosscheck_blocks > ABSOLUTE_SCHEDULE_CROSSCHECK_BLOCKS:
        raise PeriodTwoQuotientLimitError(
            "schedule cross-check exceeds absolute maximum "
            f"{ABSOLUTE_SCHEDULE_CROSSCHECK_BLOCKS}"
        )
    if schedule_crosscheck_blocks > driver_max_block:
        raise ValueError("schedule cross-check cannot exceed driver maximum block")
    if 2 * driver_max_block >= width:
        raise ValueError("width must exceed twice the driver maximum block")

    inverse_row_updates = width * (width + 1) // 2
    cell_updates = width * width
    fringe_cell_updates = (driver_max_block + 1) * (
        4 * driver_max_block + 33
    )
    estimated_work_points = (
        inverse_row_updates
        + cell_updates
        + width
        + 2 * driver_max_block
        + fringe_cell_updates
        + 16
    )
    if estimated_work_points > maximum_work_points:
        raise PeriodTwoQuotientLimitError(
            f"estimated work {estimated_work_points} exceeds maximum "
            f"{maximum_work_points}"
        )

    trace = minus_one_third_mod(width)
    seed = inverse_diagonal_map_mod(trace, width)
    if diagonal_map_mod(seed, width) != trace:
        raise AssertionError("packed inverse/forward diagonal check failed")
    if diagonal_map_cell_array(seed, width) != trace:
        raise AssertionError("cell-array forward diagonal check failed")

    fringe_heads, fringe_pairs = fringe_driver(driver_max_block)
    row_heads, row_pairs = spacetime_driver(seed, width, driver_max_block)
    if fringe_heads != row_heads or fringe_pairs != row_pairs:
        raise AssertionError("fringe and direct-spacetime schedule heads disagree")

    schedule_heads, schedule_periods = exact_schedule_heads(
        schedule_crosscheck_blocks,
        maximum_period=maximum_schedule_period,
    )
    if schedule_heads != fringe_heads[: schedule_crosscheck_blocks + 1]:
        raise AssertionError("full schedules and fringe schedule heads disagree")

    endpoint_samples = []
    exponent = 1
    while (1 << exponent) - 1 < width:
        position = (1 << exponent) - 1
        bit = (seed >> position) & 1
        endpoint_samples.append(
            {
                "exponent": exponent,
                "position": position,
                "bit": bit,
                "expected_exponent_parity": exponent & 1,
                "matches_candidate": bit == (exponent & 1),
            }
        )
        exponent += 1
    endpoint_mismatch = next(
        (sample for sample in endpoint_samples if not sample["matches_candidate"]),
        None,
    )

    period_mismatch = _first_period_mismatch(fringe_heads)
    graph = fringe_pair_graph()
    head_only_conflict = _first_head_only_transition_conflict(fringe_heads)
    portrait_conflict = depth_two_portrait_conflict(fringe_heads)
    packed_seed = seed.to_bytes((width + 7) // 8, "little")
    certificate_payload = {
        "endpoint_samples": endpoint_samples,
        "fringe_heads": fringe_heads,
        "fringe_pairs": fringe_pairs,
        "graph": graph,
        "portrait_conflict": portrait_conflict,
        "period_mismatch": period_mismatch,
        "schedule_heads": schedule_heads,
        "schedule_periods": schedule_periods,
    }
    certificate = hashlib.sha256()
    certificate.update(b"rule30-period-two-quotient-obstruction-v1\0")
    certificate.update(packed_seed)
    certificate.update(
        json.dumps(
            certificate_payload,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    )

    if period_mismatch is None:
        period_interpretation = (
            "The seven-block schedule-head candidate survived only through "
            f"the finite tested block {driver_max_block}."
        )
    else:
        period_interpretation = (
            "The proposed seven-block schedule-head cycle is exactly refuted "
            f"at block {period_mismatch['block']}."
        )
    if endpoint_mismatch is None:
        endpoint_interpretation = (
            "The dyadic endpoint parity candidate survived only at the listed "
            "finite positions."
        )
    else:
        endpoint_interpretation = (
            "The dyadic endpoint parity candidate is exactly refuted at "
            f"exponent {endpoint_mismatch['exponent']}."
        )

    return {
        "parameters": {
            "width": width,
            "driver_max_block": driver_max_block,
            "schedule_crosscheck_blocks": schedule_crosscheck_blocks,
            "maximum_schedule_period": maximum_schedule_period,
            "maximum_work_points": maximum_work_points,
            "absolute_width": ABSOLUTE_WIDTH,
            "absolute_driver_max_block": ABSOLUTE_DRIVER_MAX_BLOCK,
        },
        "coverage": {
            "finite_diagonal_bits": width,
            "driver_blocks_inclusive": driver_max_block + 1,
            "full_schedule_states_crosschecked": schedule_crosscheck_blocks + 1,
            "local_fringe_assignments_exhausted": 16,
            "independent_forward_diagonal_evaluators": 2,
            "estimated_work_points": estimated_work_points,
        },
        "all_finite_oracles_agree": True,
        "fringe_schedule_identity": {
            "verified_blocks_inclusive": driver_max_block + 1,
            "schedule_heads_prefix": "".join(fringe_heads[:32]),
            "full_schedule_periods": schedule_periods,
            "pair_transition_graph": graph,
            "head_only_transition_conflict": head_only_conflict,
            "depth_two_portrait_transition_conflict": portrait_conflict,
        },
        "seven_block_schedule_head_candidate": {
            "start_block": PERIOD_SEVEN_START_BLOCK,
            "candidate_word": "".join(PERIOD_SEVEN_WORD),
            "first_mismatch": period_mismatch,
            "pair_at_first_mismatch": (
                list(fringe_pairs[period_mismatch["block"]])
                if period_mismatch is not None
                else None
            ),
        },
        "dyadic_endpoint_parity_candidate": {
            "samples": endpoint_samples,
            "first_mismatch": endpoint_mismatch,
        },
        "alternating_lift": {
            "trace_residue": trace,
            "inverse_seed_ones": seed.bit_count(),
            "inverse_seed_last_one_position": seed.bit_length() - 1,
            "inverse_seed_sha256_little_endian_packed": hashlib.sha256(
                packed_seed
            ).hexdigest(),
        },
        "certificate_sha256": certificate.hexdigest(),
        "status": "finite-exhaustive",
        "interpretation": (
            f"{period_interpretation} {endpoint_interpretation} The exact "
            "depth-two root-activity portrait fails to preserve even the "
            "zero status of the next emitted block. The exact fringe "
            "transition graph is strongly connected, so no "
            "nonconstant monotone observable depending only on its two-bit "
            "state can hold for all local tails. Any surviving period-two "
            "argument must retain nonlocal tail information or use a "
            "different arithmetic invariant."
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit period-two inverse-lift quotient candidates."
    )
    parser.add_argument("--width", type=_positive_integer, default=DEFAULT_WIDTH)
    parser.add_argument(
        "--driver-max-block",
        type=_positive_integer,
        default=DEFAULT_DRIVER_MAX_BLOCK,
    )
    parser.add_argument(
        "--schedule-crosscheck-blocks",
        type=_positive_integer,
        default=DEFAULT_SCHEDULE_CROSSCHECK_BLOCKS,
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
        width=args.width,
        driver_max_block=args.driver_max_block,
        schedule_crosscheck_blocks=args.schedule_crosscheck_blocks,
        maximum_schedule_period=args.maximum_schedule_period,
        maximum_work_points=args.maximum_work_points,
    )
    payload = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-quotient-obstruction-v1",
        "question": "problem1",
        "hypothesis": (
            "For the pure alternating trace, either a seven-block schedule-head "
            "cycle or dyadic endpoint parity supplies a closed induction state."
        ),
        "backend": "python-exact-packed-and-cell-array",
        "parameters": campaign["parameters"],
        "result_summary": campaign,
        "status": campaign["status"],
        "proof_scope": (
            "Every listed finite lift bit, schedule state, fringe block, and "
            "all 16 assignments in the two-cell local transition relation. "
            "The all-width fringe identities are proved separately."
        ),
        "interpretation": campaign["interpretation"],
        "limitations": [
            "the candidate counterexamples do not exclude every period-two quotient",
            "finite lift bits do not prove any later bit pattern",
            "the pair transition graph does not encode the complete inward tail",
            "local strong connectivity does not imply mixing of the unique true orbit",
            "the result does not exclude eventual center period two",
            "the result does not prove Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
