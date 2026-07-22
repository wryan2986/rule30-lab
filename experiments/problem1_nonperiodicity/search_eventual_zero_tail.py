#!/usr/bin/env python3
"""Search finite whole-tail evidence for the focused Problem 1 conjecture.

The experiment enumerates an explicit finite box of eventually periodic
center-trace descriptions with c_0=1, reconstructs their initial-left prefixes,
and asks whether any reconstructed prefix develops a terminal zero region that
persists across increasing horizons.  It intentionally does not report only
the first reconstructed one: that statistic is already known to equal the
first trusted-prefix mismatch.

No finite absence of a long zero suffix proves that an infinite reconstructed
tail is not eventually zero.  A candidate with no new ones across a large
extension interval would be a counterexample lead, not a counterexample.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "python"))

from rule30lab.sideways import (  # noqa: E402
    eventually_periodic_trace,
    logical_reconstruction_work,
    reconstruct_left_initial,
)


DEFAULT_MAX_PREPERIOD = 4
DEFAULT_MAX_PERIOD = 8
DEFAULT_HORIZONS = (64, 128, 256, 512, 1_024, 2_048)
DEFAULT_MAX_DESCRIPTIONS = 200_000
DEFAULT_MAX_UNIQUE_TRACES = 200_000
DEFAULT_MAX_HORIZON = 4_096
DEFAULT_MAX_LOGICAL_CELL_UPDATES = 80_000_000_000
DEFAULT_MAX_REPORTED_CANDIDATES = 32


class EventualZeroTailLimitError(RuntimeError):
    """Raised before a configured finite campaign cap is crossed."""


@dataclass
class TraceClass:
    multiplicity: int
    canonical_preperiod: int
    canonical_period: int
    canonical_code: int


def _nonnegative_integer(text: str) -> int:
    value = int(text)
    if value < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative integer")
    return value


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def _horizons(text: str) -> tuple[int, ...]:
    try:
        values = tuple(int(part) for part in text.split(","))
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "horizons must be comma-separated integers"
        ) from exc
    if not values or any(value <= 0 for value in values):
        raise argparse.ArgumentTypeError("horizons must be positive")
    if tuple(sorted(set(values))) != values:
        raise argparse.ArgumentTypeError(
            "horizons must be strictly increasing without duplicates"
        )
    return values


def trailing_zero_run(bits: bytes | bytearray) -> int:
    """Return the number of zero bits after the final one."""

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("bits must contain only zero and one")
    for index in range(len(bits) - 1, -1, -1):
        if bits[index] == 1:
            return len(bits) - index - 1
    return len(bits)


def longest_zero_run_after_first_one(bits: bytes | bytearray) -> int:
    """Return the longest zero run strictly after the first observed one."""

    if any(bit not in (0, 1) for bit in bits):
        raise ValueError("bits must contain only zero and one")
    first_one = next((index for index, bit in enumerate(bits) if bit == 1), None)
    if first_one is None:
        return len(bits)
    longest = 0
    current = 0
    for bit in bits[first_one + 1 :]:
        if bit == 0:
            current += 1
            longest = max(longest, current)
        elif bit == 1:
            current = 0
    return longest


def _description_parts(
    preperiod: int, period: int, code: int
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    before = tuple((code >> index) & 1 for index in range(preperiod))
    cycle = tuple(
        (code >> (preperiod + index)) & 1 for index in range(period)
    )
    return before, cycle


def _description_count(max_preperiod: int, max_period: int) -> int:
    return sum(
        1 << (preperiod + period - 1)
        for preperiod in range(max_preperiod + 1)
        for period in range(1, max_period + 1)
    )


def _enumerate_trace_classes(
    max_preperiod: int,
    max_period: int,
    horizon: int,
    *,
    max_descriptions: int,
    max_unique_traces: int,
) -> tuple[dict[bytes, TraceClass], int]:
    descriptions = _description_count(max_preperiod, max_period)
    if descriptions > max_descriptions:
        raise EventualZeroTailLimitError(
            f"{descriptions} descriptions exceed configured maximum "
            f"{max_descriptions}"
        )

    classes: dict[bytes, TraceClass] = {}
    for preperiod in range(max_preperiod + 1):
        for period in range(1, max_period + 1):
            for code in range(1, 1 << (preperiod + period), 2):
                before, cycle = _description_parts(preperiod, period, code)
                trace = bytes(eventually_periodic_trace(before, cycle, horizon))
                existing = classes.get(trace)
                if existing is None:
                    if len(classes) >= max_unique_traces:
                        raise EventualZeroTailLimitError(
                            "unique finite traces exceed configured maximum "
                            f"{max_unique_traces}"
                        )
                    classes[trace] = TraceClass(1, preperiod, period, code)
                else:
                    existing.multiplicity += 1
    if sum(item.multiplicity for item in classes.values()) != descriptions:
        raise AssertionError("description multiplicity accounting failed")
    return classes, descriptions


def _candidate_payload(
    trace_class: TraceClass,
    *,
    terminal_zero_run: int,
    longest_zero_run: int,
    ones: int,
) -> dict[str, Any]:
    return {
        "canonical_description": {
            "preperiod": trace_class.canonical_preperiod,
            "period": trace_class.canonical_period,
            "code_hex": hex(trace_class.canonical_code),
        },
        "represented_descriptions": trace_class.multiplicity,
        "ones_in_reconstructed_prefix": ones,
        "terminal_zero_run": terminal_zero_run,
        "longest_zero_run_after_first_one": longest_zero_run,
    }


def run_campaign(
    *,
    max_preperiod: int,
    max_period: int,
    horizons: tuple[int, ...],
    max_descriptions: int = DEFAULT_MAX_DESCRIPTIONS,
    max_unique_traces: int = DEFAULT_MAX_UNIQUE_TRACES,
    max_horizon: int = DEFAULT_MAX_HORIZON,
    max_logical_cell_updates: int = DEFAULT_MAX_LOGICAL_CELL_UPDATES,
    max_reported_candidates: int = DEFAULT_MAX_REPORTED_CANDIDATES,
) -> dict[str, Any]:
    """Run one deterministic finite whole-tail campaign."""

    if max_preperiod < 0 or max_period <= 0:
        raise ValueError("preperiod must be nonnegative and period positive")
    if not horizons or tuple(sorted(set(horizons))) != horizons:
        raise ValueError("horizons must be strictly increasing")
    if horizons[0] <= 0 or horizons[-1] > max_horizon:
        raise EventualZeroTailLimitError(
            f"horizon {horizons[-1]} exceeds configured maximum {max_horizon}"
        )
    if max_preperiod + max_period > 63:
        raise ValueError("description width is capped at 63 bits")
    if max_preperiod + max_period > horizons[0]:
        raise ValueError(
            "the first horizon must expose every bit of every description"
        )
    if any(
        cap <= 0
        for cap in (
            max_descriptions,
            max_unique_traces,
            max_horizon,
            max_logical_cell_updates,
            max_reported_candidates,
        )
    ):
        raise ValueError("resource and report caps must be positive")

    classes, description_count = _enumerate_trace_classes(
        max_preperiod,
        max_period,
        horizons[-1],
        max_descriptions=max_descriptions,
        max_unique_traces=max_unique_traces,
    )
    logical_work = len(classes) * sum(
        logical_reconstruction_work(horizon) for horizon in horizons
    )
    if logical_work > max_logical_cell_updates:
        raise EventualZeroTailLimitError(
            f"{logical_work} logical updates exceed configured maximum "
            f"{max_logical_cell_updates}"
        )

    checkpoint_accumulators: dict[int, dict[str, Any]] = {
        horizon: {
            "trailing_histogram": Counter(),
            "maximum_terminal_zero_run": -1,
            "maximum_candidate": None,
            "maximum_zero_run_after_first_one": -1,
            "maximum_zero_run_candidate": None,
            "all_zero_trace_classes": 0,
            "total_ones": 0,
        }
        for horizon in horizons
    }
    empty_extension_classes = {horizon: 0 for horizon in horizons[1:]}
    empty_extension_descriptions = {horizon: 0 for horizon in horizons[1:]}
    ranked: list[tuple[int, int, int, int, int, int, TraceClass]] = []
    certificate = hashlib.sha256()
    certificate.update(
        json.dumps(
            {
                "max_preperiod": max_preperiod,
                "max_period": max_period,
                "horizons": horizons,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("ascii")
    )

    for trace, trace_class in sorted(classes.items()):
        full_left = bytes(reconstruct_left_initial(trace))
        certificate.update(len(trace).to_bytes(4, "little"))
        certificate.update(trace_class.multiplicity.to_bytes(8, "little"))
        certificate.update(trace_class.canonical_preperiod.to_bytes(2, "little"))
        certificate.update(trace_class.canonical_period.to_bytes(2, "little"))
        certificate.update(trace_class.canonical_code.to_bytes(8, "little"))
        certificate.update(trace)
        certificate.update(full_left)

        for horizon in horizons:
            independently_reconstructed = (
                full_left
                if horizon == horizons[-1]
                else bytes(reconstruct_left_initial(trace[: horizon + 1]))
            )
            expected = full_left[:horizon]
            if independently_reconstructed != expected:
                raise AssertionError(
                    "cross-horizon reconstructed prefixes disagree"
                )
            terminal = trailing_zero_run(expected)
            longest = longest_zero_run_after_first_one(expected)
            ones = sum(expected)
            accumulator = checkpoint_accumulators[horizon]
            accumulator["trailing_histogram"][terminal] += 1
            accumulator["total_ones"] += ones
            if ones == 0:
                accumulator["all_zero_trace_classes"] += 1
            if terminal > accumulator["maximum_terminal_zero_run"]:
                accumulator["maximum_terminal_zero_run"] = terminal
                accumulator["maximum_candidate"] = _candidate_payload(
                    trace_class,
                    terminal_zero_run=terminal,
                    longest_zero_run=longest,
                    ones=ones,
                )
            if longest > accumulator["maximum_zero_run_after_first_one"]:
                accumulator["maximum_zero_run_after_first_one"] = longest
                accumulator["maximum_zero_run_candidate"] = _candidate_payload(
                    trace_class,
                    terminal_zero_run=terminal,
                    longest_zero_run=longest,
                    ones=ones,
                )

        for lower, upper in zip(horizons[:-1], horizons[1:], strict=True):
            if not any(full_left[lower:upper]):
                empty_extension_classes[upper] += 1
                empty_extension_descriptions[upper] += trace_class.multiplicity

        terminal = trailing_zero_run(full_left)
        longest = longest_zero_run_after_first_one(full_left)
        ranked.append(
            (
                terminal,
                longest,
                -trace_class.canonical_preperiod,
                -trace_class.canonical_period,
                -trace_class.canonical_code,
                sum(full_left),
                trace_class,
            )
        )

    checkpoint_summaries = []
    for index, horizon in enumerate(horizons):
        accumulator = checkpoint_accumulators[horizon]
        histogram: Counter[int] = accumulator["trailing_histogram"]
        checkpoint_summaries.append(
            {
                "horizon": horizon,
                "trace_classes": len(classes),
                "all_zero_reconstructed_trace_classes": accumulator[
                    "all_zero_trace_classes"
                ],
                "total_ones_across_trace_classes": accumulator["total_ones"],
                "maximum_terminal_zero_run": accumulator[
                    "maximum_terminal_zero_run"
                ],
                "maximum_candidate": accumulator["maximum_candidate"],
                "maximum_zero_run_after_first_one": accumulator[
                    "maximum_zero_run_after_first_one"
                ],
                "maximum_zero_run_candidate": accumulator[
                    "maximum_zero_run_candidate"
                ],
                "terminal_zero_run_histogram": {
                    str(run): count for run, count in sorted(histogram.items())
                },
                "classes_with_no_one_since_previous_checkpoint": (
                    None if index == 0 else empty_extension_classes[horizon]
                ),
                "descriptions_with_no_one_since_previous_checkpoint": (
                    None if index == 0 else empty_extension_descriptions[horizon]
                ),
            }
        )

    ranked.sort(reverse=True, key=lambda item: item[:5])
    reported = [
        _candidate_payload(
            item[-1],
            terminal_zero_run=item[0],
            longest_zero_run=item[1],
            ones=item[5],
        )
        for item in ranked[:max_reported_candidates]
    ]

    final_extension_leads = empty_extension_classes[horizons[-1]]
    return {
        "status": "finite-exhaustive",
        "parameters": {
            "minimum_preperiod": 0,
            "maximum_preperiod": max_preperiod,
            "minimum_period": 1,
            "maximum_period": max_period,
            "horizons": list(horizons),
            "seed_condition": "c0=1",
        },
        "coverage": {
            "descriptions": description_count,
            "distinct_finite_trace_classes": len(classes),
            "duplicate_descriptions": description_count - len(classes),
            "reconstructions_completed": len(classes) * len(horizons),
            "cross_horizon_prefix_equalities_checked": len(classes)
            * (len(horizons) - 1),
            "logical_cell_update_budget_charged": logical_work,
        },
        "checkpoints": checkpoint_summaries,
        "counterexample_lead_rule": (
            "a trace class with no reconstructed one between the final two "
            "checkpoints"
        ),
        "counterexample_lead_trace_classes": final_extension_leads,
        "counterexample_lead_descriptions": empty_extension_descriptions[
            horizons[-1]
        ],
        "ranked_terminal_zero_candidates": reported,
        "certificate_sha256": certificate.hexdigest(),
        "interpretation": (
            "The campaign measures complete reconstructed prefixes and new-one "
            "occupancy across explicit extension intervals. A zero lead count is "
            "finite evidence only and cannot exclude an eventually-zero infinite "
            "tail outside this description box or beyond the final horizon."
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-preperiod",
        type=_nonnegative_integer,
        default=DEFAULT_MAX_PREPERIOD,
    )
    parser.add_argument(
        "--max-period", type=_positive_integer, default=DEFAULT_MAX_PERIOD
    )
    parser.add_argument(
        "--horizons",
        type=_horizons,
        default=DEFAULT_HORIZONS,
        help="strictly increasing comma-separated reconstruction horizons",
    )
    parser.add_argument(
        "--max-descriptions",
        type=_positive_integer,
        default=DEFAULT_MAX_DESCRIPTIONS,
    )
    parser.add_argument(
        "--max-unique-traces",
        type=_positive_integer,
        default=DEFAULT_MAX_UNIQUE_TRACES,
    )
    parser.add_argument(
        "--max-horizon", type=_positive_integer, default=DEFAULT_MAX_HORIZON
    )
    parser.add_argument(
        "--max-logical-cell-updates",
        type=_positive_integer,
        default=DEFAULT_MAX_LOGICAL_CELL_UPDATES,
    )
    parser.add_argument(
        "--max-reported-candidates",
        type=_positive_integer,
        default=DEFAULT_MAX_REPORTED_CANDIDATES,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    campaign = run_campaign(
        max_preperiod=args.max_preperiod,
        max_period=args.max_period,
        horizons=args.horizons,
        max_descriptions=args.max_descriptions,
        max_unique_traces=args.max_unique_traces,
        max_horizon=args.max_horizon,
        max_logical_cell_updates=args.max_logical_cell_updates,
        max_reported_candidates=args.max_reported_candidates,
    )
    payload = {
        "schema_version": 1,
        "experiment_id": "problem1-eventual-zero-tail-search-v1",
        "question": "problem1",
        "hypothesis": (
            "An eventually periodic center trace with c0=1 cannot reconstruct "
            "an eventually-zero initial left half."
        ),
        "backend": "python-packed-sideways",
        "parameters": campaign["parameters"],
        "result_summary": campaign,
        "status": campaign["status"],
        "proof_scope": (
            "Only every description in the explicit finite preperiod/period "
            "box and every reconstructed depth through the final horizon."
        ),
        "interpretation": campaign["interpretation"],
        "limitations": [
            "finite zero-run bounds do not prove infinitely many reconstructed ones",
            "descriptions outside the finite preperiod/period box remain untreated",
            "a later all-zero tail can begin after the final reconstruction horizon",
            "a finite counterexample lead would require exact infinite verification",
            "the experiment does not prove Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
