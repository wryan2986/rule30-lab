#!/usr/bin/env python3
"""Emit deterministic JSON for bounded Problem 1 sideways searches.

The script writes only to standard output.  It contains no timestamp, runtime,
or host-specific measurement so identical inputs and code produce identical
JSON.  Every search result is finite-exhaustive only within its explicit
parameter box and reconstruction horizon.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "python"))

from rule30lab.sideways import (  # noqa: E402
    DEFAULT_LIMITS,
    SidewaysLimits,
    SidewaysResourceLimitError,
    reconstruct_left_initial,
    search_eventually_periodic,
    search_pure_periods,
    truncated_periodic_state_graph,
    word_from_index,
)


DEFAULT_TRUSTED_CENTER = (
    REPOSITORY_ROOT
    / "tests"
    / "reference_vectors"
    / "center_c00000000_c00009999.u8"
)


def _nonnegative_integer(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected an integer") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative integer")
    return value


def _positive_integer(text: str) -> int:
    value = _nonnegative_integer(text)
    if value == 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Exhaust bounded pure and eventual-period descriptions, verify a "
            "trusted true trace, and summarize fixed-width finite state graphs."
        )
    )
    parser.add_argument("--horizon", type=_nonnegative_integer, default=500)
    parser.add_argument("--max-period", type=_positive_integer, default=10)
    parser.add_argument("--max-preperiod", type=_nonnegative_integer, default=3)
    parser.add_argument(
        "--eventual-max-period", type=_positive_integer, default=5
    )
    parser.add_argument("--graph-width", type=_positive_integer, default=4)
    parser.add_argument("--graph-max-period", type=_positive_integer, default=3)
    parser.add_argument("--trusted-center", type=Path, default=DEFAULT_TRUSTED_CENTER)
    parser.add_argument(
        "--max-horizon", type=_nonnegative_integer, default=DEFAULT_LIMITS.max_horizon
    )
    parser.add_argument(
        "--max-candidates",
        type=_nonnegative_integer,
        default=DEFAULT_LIMITS.max_candidates,
    )
    parser.add_argument(
        "--max-logical-cell-updates",
        type=_nonnegative_integer,
        default=DEFAULT_LIMITS.max_logical_cell_updates,
    )
    parser.add_argument(
        "--max-certificate-bytes",
        type=_nonnegative_integer,
        default=DEFAULT_LIMITS.max_certificate_bytes,
    )
    parser.add_argument(
        "--max-graph-states",
        type=_nonnegative_integer,
        default=DEFAULT_LIMITS.max_graph_states,
    )
    parser.add_argument(
        "--max-reported-survivors",
        type=_nonnegative_integer,
        default=DEFAULT_LIMITS.max_reported_survivors,
    )
    return parser


def _relative_or_absolute(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(REPOSITORY_ROOT))
    except ValueError:
        return str(resolved)


def _graph_summaries(
    max_period: int,
    width: int,
    limits: SidewaysLimits,
) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    description_count = 0
    for period_length in range(1, max_period + 1):
        remaining = limits.max_candidates - description_count
        if remaining < 1 or period_length >= remaining.bit_length():
            raise SidewaysResourceLimitError(
                "fixed-width graph description count exceeds configured "
                f"maximum {limits.max_candidates}"
            )
        period_count = 1 << period_length
        description_count += period_count
        for word_index in range(period_count):
            word = word_from_index(word_index, period_length)
            graph = truncated_periodic_state_graph(word, width, limits=limits)
            graph["word_index"] = word_index
            summaries.append(graph)
    return summaries


def build_summary(args: argparse.Namespace) -> dict[str, Any]:
    limits = SidewaysLimits(
        max_horizon=args.max_horizon,
        max_candidates=args.max_candidates,
        max_logical_cell_updates=args.max_logical_cell_updates,
        max_certificate_bytes=args.max_certificate_bytes,
        max_graph_states=args.max_graph_states,
        max_reported_survivors=args.max_reported_survivors,
    )
    trusted_path = args.trusted_center.resolve()
    trusted = trusted_path.read_bytes()
    if any(bit not in (0, 1) for bit in trusted):
        raise ValueError("trusted center file must use one binary byte per bit")
    if len(trusted) < args.horizon + 1:
        raise ValueError(
            f"trusted center has {len(trusted)} bits but horizon {args.horizon} "
            f"requires {args.horizon + 1}"
        )

    reconstructed = reconstruct_left_initial(
        trusted[: args.horizon + 1], limits=limits
    )
    pure = search_pure_periods(
        args.max_period,
        args.horizon,
        limits=limits,
    )
    eventual = search_eventually_periodic(
        args.max_preperiod,
        args.eventual_max_period,
        args.horizon,
        limits=limits,
    )
    graphs = _graph_summaries(
        args.graph_max_period,
        args.graph_width,
        limits,
    )

    return {
        "schema_version": 1,
        "experiment_id": "problem1-sideways-bounded-search-v1",
        "question": "problem1",
        "hypothesis": (
            "Within the explicitly bounded candidate descriptions and finite "
            "reconstruction horizon, every nonzero eventually periodic trace "
            "reconstructs at least one nonzero initial-left cell."
        ),
        "backend": "python-packed-time-columns",
        "parameters": {
            "horizon": args.horizon,
            "center_convention": f"c_0 through c_{args.horizon} inclusive",
            "reconstructed_left_convention": (
                f"x_-1(0) through x_-{args.horizon}(0)"
                if args.horizon
                else "empty horizon-zero left prefix"
            ),
            "pure_max_period": args.max_period,
            "eventual_max_preperiod": args.max_preperiod,
            "eventual_max_period": args.eventual_max_period,
            "graph_width": args.graph_width,
            "graph_max_period": args.graph_max_period,
            "resource_limits": {
                "max_horizon": limits.max_horizon,
                "max_candidates_per_search": limits.max_candidates,
                "max_logical_cell_updates_per_search": (
                    limits.max_logical_cell_updates
                ),
                "max_certificate_bytes": limits.max_certificate_bytes,
                "max_graph_states_per_graph": limits.max_graph_states,
                "max_reported_survivors": limits.max_reported_survivors,
            },
        },
        "trusted_input": {
            "path": _relative_or_absolute(trusted_path),
            "encoding": "one_byte_per_bit_c_0_first",
            "available_bit_count": len(trusted),
            "sha256_u8": hashlib.sha256(trusted).hexdigest(),
        },
        "trusted_trace_check": {
            "horizon": args.horizon,
            "reconstructed_left_bit_count": len(reconstructed),
            "nonzero_reconstructed_left_bits": sum(reconstructed),
            "reconstructed_left_sha256_u8": hashlib.sha256(reconstructed).hexdigest(),
        },
        "pure_period_search": pure,
        "preperiod_plus_period_search": eventual,
        "fixed_width_state_graphs": {
            "status": "finite-exhaustive",
            "graph_count": len(graphs),
            "graphs": graphs,
            "interpretation": (
                "Each graph is exact only for its fixed spatial width and "
                "permanently zero outer boundary. The node bound grows as "
                "period_length * 2**width."
            ),
        },
        "status": "finite-exhaustive",
        "proof_scope": (
            "Exact enumeration of the stated finite description boxes, exact "
            "Rule 30 inversion through the stated finite horizon, and exact "
            "fixed-width functional graphs only."
        ),
        "interpretation": (
            "A candidate survives only when all reconstructed initial-left bits "
            "within the finite horizon are zero; c_0=1 is checked separately for "
            "single-cell-seed compatibility."
        ),
        "limitations": [
            "no finite horizon proves eventual nonperiodicity",
            "preperiod and period lengths outside the stated boxes are untested",
            "a first nonzero depth is a finite exclusion witness only",
            "fixed-width graph cycles need not describe the semi-infinite right half",
            "the graph state bound grows exponentially when width grows with depth",
        ],
    }


def main() -> int:
    args = _parser().parse_args()
    summary = build_summary(args)
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
