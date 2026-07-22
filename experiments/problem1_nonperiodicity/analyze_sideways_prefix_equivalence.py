#!/usr/bin/env python3
"""Test and exploit the finite sideways/prefix-mismatch equivalence.

For a proposed center trace with fixed zero initial data to its right,
left-permutive reconstruction returns the unique initial data to its left.
Relative to the zero-left reference evolution with the same center bit at
time zero, the first reconstructed one should occur at exactly the first
time the proposed trace differs from the reference center trace.

The exhaustive checks emitted here are finite tests.  The horizon-independent
statement is justified separately in the accompanying informal proof.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from collections.abc import Sequence
from typing import Any

from rule30lab.core import center_bits_cell_array
from rule30lab.sideways import (
    first_nonzero_left_depth,
    logical_reconstruction_work,
)


DEFAULT_MAX_EXHAUSTIVE_HORIZON = 16
DEFAULT_MAX_PREPERIOD = 8
DEFAULT_MAX_PERIOD = 12
DEFAULT_PERIODIC_HORIZON = 64
DEFAULT_MAX_EXHAUSTIVE_TRACES = 300_000
DEFAULT_MAX_PERIODIC_DESCRIPTIONS = 3_000_000
DEFAULT_MAX_LOGICAL_CELL_UPDATES = 200_000_000


class PrefixEquivalenceLimitError(RuntimeError):
    """Raised before an explicitly configured finite-search cap is crossed."""


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


def first_mismatch_index(left: Sequence[int], right: Sequence[int]) -> int | None:
    """Return the first zero-based mismatch, or ``None`` for equal sequences."""

    if len(left) != len(right):
        raise ValueError("sequences must have equal length")
    return next(
        (index for index, (a, b) in enumerate(zip(left, right, strict=True)) if a != b),
        None,
    )


def reference_center(c0: int, horizon: int) -> bytes:
    """Return the zero-left/zero-right center trace with initial bit ``c0``."""

    if c0 not in (0, 1):
        raise ValueError("c0 must be 0 or 1")
    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    if c0 == 0:
        return bytes(horizon + 1)
    return bytes(center_bits_cell_array(horizon + 1))


def _trace_from_code(code: int, horizon: int) -> bytes:
    return bytes((code >> time) & 1 for time in range(horizon + 1))


def _digest_case(
    digest: Any,
    *,
    horizon: int,
    c0: int,
    code: int,
    outcome: int | None,
) -> None:
    digest.update(horizon.to_bytes(2, "little"))
    digest.update(bytes((c0,)))
    digest.update(code.to_bytes(max(1, (horizon + 8) // 8), "little"))
    digest.update((0 if outcome is None else outcome + 1).to_bytes(2, "little"))


def exhaustive_equivalence(
    max_horizon: int,
    *,
    max_traces: int = DEFAULT_MAX_EXHAUSTIVE_TRACES,
    max_logical_cell_updates: int = DEFAULT_MAX_LOGICAL_CELL_UPDATES,
) -> dict[str, Any]:
    """Check every binary trace through every horizon up to ``max_horizon``."""

    if max_horizon < 0:
        raise ValueError("max_horizon must be nonnegative")
    if max_traces <= 0 or max_logical_cell_updates <= 0:
        raise ValueError("resource caps must be positive")

    trace_count = 2 * sum(1 << horizon for horizon in range(max_horizon + 1))
    logical_work = 2 * sum(
        (1 << horizon) * logical_reconstruction_work(horizon)
        for horizon in range(max_horizon + 1)
    )
    if trace_count > max_traces:
        raise PrefixEquivalenceLimitError(
            f"{trace_count} traces exceed configured maximum {max_traces}"
        )
    if logical_work > max_logical_cell_updates:
        raise PrefixEquivalenceLimitError(
            f"{logical_work} logical updates exceed configured maximum "
            f"{max_logical_cell_updates}"
        )

    digest = hashlib.sha256()
    per_horizon: list[dict[str, Any]] = []
    for horizon in range(max_horizon + 1):
        histogram: Counter[int | None] = Counter()
        cases = 0
        for c0 in (0, 1):
            reference = reference_center(c0, horizon)
            for tail_code in range(1 << horizon):
                code = c0 | (tail_code << 1)
                proposed = _trace_from_code(code, horizon)
                mismatch = first_mismatch_index(proposed, reference)
                reconstructed = first_nonzero_left_depth(proposed)
                if reconstructed != mismatch:
                    raise AssertionError(
                        "sideways/prefix equivalence failed for "
                        f"H={horizon}, c0={c0}, code={code:#x}: "
                        f"reconstructed={reconstructed}, mismatch={mismatch}"
                    )
                histogram[mismatch] += 1
                cases += 1
                _digest_case(
                    digest,
                    horizon=horizon,
                    c0=c0,
                    code=code,
                    outcome=reconstructed,
                )

        expected_histogram: dict[int | None, int] = {None: 2}
        expected_histogram.update(
            {
                depth: 2 * (1 << (horizon - depth))
                for depth in range(1, horizon + 1)
            }
        )
        if histogram != Counter(expected_histogram):
            raise AssertionError(
                f"unexpected first-mismatch distribution at horizon {horizon}"
            )
        per_horizon.append(
            {
                "horizon": horizon,
                "traces": cases,
                "equal_reference_traces": histogram[None],
                "first_mismatch_histogram": {
                    str(depth): histogram[depth]
                    for depth in range(1, horizon + 1)
                },
            }
        )

    return {
        "status": "finite-exhaustive",
        "max_horizon": max_horizon,
        "traces_checked": trace_count,
        "logical_cell_update_budget_charged": logical_work,
        "failures": 0,
        "certificate_sha256": digest.hexdigest(),
        "per_horizon": per_horizon,
        "interpretation": (
            "Every binary trace in the stated finite family satisfied the "
            "identity. The horizon-independent identity relies on the separate "
            "causal/permutivity proof, not on this enumeration."
        ),
    }


def _description_bit(
    code: int, preperiod: int, period: int, time: int
) -> int:
    index = (
        time
        if time < preperiod
        else preperiod + (time - preperiod) % period
    )
    return (code >> index) & 1


def periodic_description_prefix_search(
    max_preperiod: int,
    max_period: int,
    horizon: int,
    *,
    max_descriptions: int = DEFAULT_MAX_PERIODIC_DESCRIPTIONS,
) -> dict[str, Any]:
    """Compare each c0=1 description directly with the trusted center prefix."""

    if max_preperiod < 0 or max_period <= 0 or horizon < 0:
        raise ValueError("preperiod/horizon must be nonnegative and period positive")
    if max_preperiod + max_period > horizon:
        raise ValueError("horizon must be at least max_preperiod + max_period")
    if max_preperiod + max_period > 63:
        raise ValueError("description width is capped at 63 bits")
    if max_descriptions <= 0:
        raise ValueError("max_descriptions must be positive")

    descriptions = sum(
        1 << (preperiod + period - 1)
        for preperiod in range(max_preperiod + 1)
        for period in range(1, max_period + 1)
    )
    if descriptions > max_descriptions:
        raise PrefixEquivalenceLimitError(
            f"{descriptions} descriptions exceed configured maximum "
            f"{max_descriptions}"
        )

    trusted = bytes(center_bits_cell_array(horizon + 1))
    histogram: Counter[int] = Counter()
    survivors = 0
    digest = hashlib.sha256()
    for preperiod in range(max_preperiod + 1):
        for period in range(1, max_period + 1):
            for code in range(1, 1 << (preperiod + period), 2):
                mismatch = next(
                    (
                        time
                        for time in range(1, horizon + 1)
                        if _description_bit(code, preperiod, period, time)
                        != trusted[time]
                    ),
                    None,
                )
                digest.update(preperiod.to_bytes(2, "little"))
                digest.update(period.to_bytes(2, "little"))
                digest.update(code.to_bytes(8, "little"))
                digest.update(
                    (0 if mismatch is None else mismatch + 1).to_bytes(2, "little")
                )
                if mismatch is None:
                    survivors += 1
                else:
                    histogram[mismatch] += 1

    return {
        "status": "finite-exhaustive",
        "parameters": {
            "minimum_preperiod": 0,
            "maximum_preperiod": max_preperiod,
            "minimum_period": 1,
            "maximum_period": max_period,
            "horizon": horizon,
            "seed_condition": "c0=1",
        },
        "descriptions_checked": descriptions,
        "descriptions_matching_through_horizon": survivors,
        "descriptions_mismatching_through_horizon": descriptions - survivors,
        "first_mismatch_histogram": {
            str(depth): count for depth, count in sorted(histogram.items())
        },
        "certificate_sha256": digest.hexdigest(),
        "interpretation": (
            "By the separately proved finite equivalence, this description-level "
            "prefix-mismatch histogram equals the description-level histogram of "
            "first nonzero reconstructed-left depths. It is still a bounded prefix "
            "test and does not establish nonperiodicity."
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze the exact finite sideways/prefix equivalence."
    )
    parser.add_argument(
        "--max-exhaustive-horizon",
        type=_nonnegative_integer,
        default=DEFAULT_MAX_EXHAUSTIVE_HORIZON,
    )
    parser.add_argument(
        "--max-preperiod",
        type=_nonnegative_integer,
        default=DEFAULT_MAX_PREPERIOD,
    )
    parser.add_argument(
        "--max-period", type=_positive_integer, default=DEFAULT_MAX_PERIOD
    )
    parser.add_argument(
        "--periodic-horizon",
        type=_nonnegative_integer,
        default=DEFAULT_PERIODIC_HORIZON,
    )
    parser.add_argument(
        "--max-exhaustive-traces",
        type=_positive_integer,
        default=DEFAULT_MAX_EXHAUSTIVE_TRACES,
    )
    parser.add_argument(
        "--max-periodic-descriptions",
        type=_positive_integer,
        default=DEFAULT_MAX_PERIODIC_DESCRIPTIONS,
    )
    parser.add_argument(
        "--max-logical-cell-updates",
        type=_positive_integer,
        default=DEFAULT_MAX_LOGICAL_CELL_UPDATES,
    )
    return parser


def main() -> None:
    args = _parser().parse_args()
    exhaustive = exhaustive_equivalence(
        args.max_exhaustive_horizon,
        max_traces=args.max_exhaustive_traces,
        max_logical_cell_updates=args.max_logical_cell_updates,
    )
    periodic = periodic_description_prefix_search(
        args.max_preperiod,
        args.max_period,
        args.periodic_horizon,
        max_descriptions=args.max_periodic_descriptions,
    )
    result = {
        "schema_version": 1,
        "experiment_id": "problem1-sideways-prefix-equivalence-v1",
        "question": "problem1",
        "hypothesis": (
            "For equal-length finite center traces with the same c0 and zero "
            "initial right half, the first nonzero reconstructed-left depth "
            "equals the first mismatch from the zero-left reference trace."
        ),
        "backend": "python-packed-sideways-and-direct-prefix",
        "parameters": {
            "max_exhaustive_horizon": args.max_exhaustive_horizon,
            "maximum_preperiod": args.max_preperiod,
            "maximum_period": args.max_period,
            "periodic_horizon": args.periodic_horizon,
            "resource_limits": {
                "max_exhaustive_traces": args.max_exhaustive_traces,
                "max_periodic_descriptions": args.max_periodic_descriptions,
                "max_logical_cell_updates": args.max_logical_cell_updates,
            },
        },
        "status": "finite-exhaustive",
        "proof_scope": (
            "The computational status covers only all binary traces through "
            f"horizon {args.max_exhaustive_horizon} and the stated finite "
            "eventual-period box. The separate informal causal/permutivity "
            "proof states the finite identity for arbitrary horizon."
        ),
        "result_summary": {
            "proof_status": "informal-rigorous-finite-lemma",
            "exhaustive_cross_check": exhaustive,
            "eventually_periodic_prefix_search": periodic,
        },
        "interpretation": (
            "Finite sideways first-witness exclusions are exact certificates, "
            "but they contain the same information as direct trusted-prefix "
            "comparison. The stronger entire-tail question remains open."
        ),
        "limitations": [
            "The exhaustive cross-check has a finite horizon cap.",
            "The universal finite lemma does not imply center nonperiodicity.",
            "A first reconstructed one proves only that a proposal differs from the trusted prefix.",
            "Nothing here proves that a reconstructed left tail has infinitely many nonzero cells.",
        ],
    }
    print(json.dumps(result, sort_keys=True, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
