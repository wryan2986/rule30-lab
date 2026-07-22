#!/usr/bin/env python3
"""Emit deterministic JSON for bounded Problem 1 sideways searches.

The script writes its summary to standard output and, only when explicitly
requested, writes deterministic fixed-width graph artifacts.  It contains no
timestamp, runtime, or host-specific measurement so identical inputs and code
produce identical JSON and graph bytes.  Every search result is
finite-exhaustive only within its explicit parameter box and reconstruction
horizon.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "python"))

from rule30lab.sideways import (  # noqa: E402
    DEFAULT_LIMITS,
    SidewaysLimits,
    SidewaysResourceLimitError,
    logical_reconstruction_work,
    reconstruct_left_initial,
    search_eventually_periodic,
    search_pure_periods,
    truncated_periodic_state_graph,
    truncated_right_transition,
    word_from_index,
)


DEFAULT_TRUSTED_CENTER = (
    REPOSITORY_ROOT
    / "tests"
    / "reference_vectors"
    / "center_c00000000_c00009999.u8"
)

DEFAULT_TRUE_PREFIX_LENGTHS = (1, 2, 4, 8, 16, 32, 64, 128, 256)
DEFAULT_MAX_GRAPH_ARTIFACT_BYTES = 2 * 1024 * 1024
GRAPH_SCOPE_WARNING = (
    "These are exact fixed-width graphs with a permanently zero outer "
    "boundary. Their state bound grows as period_length * 2**width; they do "
    "not establish a depth-independent finite-state model for the "
    "semi-infinite Rule 30 reconstruction problem."
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


def _strictly_increasing_positive_integers(text: str) -> tuple[int, ...]:
    fields = text.split(",")
    if not fields or any(not field.strip() for field in fields):
        raise argparse.ArgumentTypeError(
            "expected a comma-separated list of positive integers"
        )
    values: list[int] = []
    for field in fields:
        try:
            value = int(field)
        except ValueError as exc:
            raise argparse.ArgumentTypeError(
                "expected a comma-separated list of positive integers"
            ) from exc
        if value <= 0:
            raise argparse.ArgumentTypeError("prefix lengths must be positive")
        values.append(value)
    if any(left >= right for left, right in zip(values, values[1:])):
        raise argparse.ArgumentTypeError(
            "prefix lengths must be unique and strictly increasing"
        )
    return tuple(values)


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
    parser.add_argument(
        "--true-prefix-lengths",
        type=_strictly_increasing_positive_integers,
        default=DEFAULT_TRUE_PREFIX_LENGTHS,
        metavar="L1,L2,...",
        help=(
            "trusted prefix lengths L to retain before setting every c_t with "
            "t >= L to zero"
        ),
    )
    parser.add_argument(
        "--export-graphs-dir",
        type=Path,
        help=(
            "optionally write one deterministic DOT edge list, README.md, and "
            "SHA256SUMS for the requested fixed-width graphs"
        ),
    )
    parser.add_argument(
        "--max-graph-artifact-bytes",
        type=_nonnegative_integer,
        default=DEFAULT_MAX_GRAPH_ARTIFACT_BYTES,
        help="maximum combined DOT, README, and checksum bytes when exporting graphs",
    )
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


def _append_unsigned_varint(output: bytearray, value: int) -> None:
    while value >= 0x80:
        output.append((value & 0x7F) | 0x80)
        value >>= 7
    output.append(value)


def _failure_certificate(
    *,
    search_kind: str,
    horizon: int,
    candidate_order: str,
    outcomes: bytes,
    candidate_count: int,
) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "search_kind": search_kind,
        "horizon": horizon,
        "candidate_order": candidate_order,
        "candidate_count": candidate_count,
        "outcome_semantics": (
            "unsigned value 0 means no reconstructed one at depths 1..H; "
            "value d>=1 is the first reconstructed nonzero depth"
        ),
        "encoding": "unsigned-varint-base64",
        "payload_bytes": len(outcomes),
        "payload_sha256": hashlib.sha256(outcomes).hexdigest(),
        "payload_base64": base64.b64encode(outcomes).decode("ascii"),
    }


def _trusted_prefix_then_zero_trace(
    trusted: bytes,
    prefix_length: int,
    horizon: int,
) -> bytearray:
    if prefix_length <= 0:
        raise ValueError("prefix_length must be positive")
    trace_length = horizon + 1
    if prefix_length > trace_length:
        raise ValueError(
            f"prefix length {prefix_length} exceeds finite trace length "
            f"{trace_length}"
        )
    if len(trusted) < prefix_length:
        raise ValueError(
            f"trusted center has {len(trusted)} bits but prefix length "
            f"{prefix_length} was requested"
        )
    trace = bytearray(trace_length)
    trace[:prefix_length] = trusted[:prefix_length]
    return trace


def search_true_prefix_then_zero(
    trusted: bytes,
    prefix_lengths: tuple[int, ...],
    horizon: int,
    *,
    limits: SidewaysLimits,
) -> dict[str, Any]:
    """Check listed true-prefix/permanent-zero traces through finite depth H."""

    if not prefix_lengths:
        raise ValueError("at least one true prefix length is required")
    if any(
        not isinstance(length, int) or isinstance(length, bool) or length <= 0
        for length in prefix_lengths
    ):
        raise ValueError("true prefix lengths must be positive integers")
    if any(
        left >= right
        for left, right in zip(prefix_lengths, prefix_lengths[1:])
    ):
        raise ValueError("true prefix lengths must be unique and strictly increasing")
    if horizon < 0:
        raise ValueError("horizon must be nonnegative")
    if horizon > limits.max_horizon:
        raise SidewaysResourceLimitError(
            f"horizon {horizon} exceeds configured maximum {limits.max_horizon}"
        )
    if len(prefix_lengths) > limits.max_candidates:
        raise SidewaysResourceLimitError(
            f"candidate count {len(prefix_lengths)} exceeds configured maximum "
            f"{limits.max_candidates}"
        )
    logical_work = len(prefix_lengths) * logical_reconstruction_work(horizon)
    if logical_work > limits.max_logical_cell_updates:
        raise SidewaysResourceLimitError(
            f"worst-case logical prefix-then-zero search work {logical_work} "
            "exceeds configured maximum "
            f"{limits.max_logical_cell_updates}"
        )
    if prefix_lengths[-1] > horizon + 1:
        raise ValueError(
            f"prefix length {prefix_lengths[-1]} exceeds finite trace length "
            f"{horizon + 1}"
        )

    encoded_outcomes = bytearray()
    per_prefix: list[dict[str, Any]] = []
    finite_exclusion_count = 0
    for prefix_length in prefix_lengths:
        center = _trusted_prefix_then_zero_trace(trusted, prefix_length, horizon)
        reconstructed = reconstruct_left_initial(center, limits=limits)
        failure_depth = next(
            (
                depth
                for depth, bit in enumerate(reconstructed, start=1)
                if bit
            ),
            None,
        )
        _append_unsigned_varint(
            encoded_outcomes, 0 if failure_depth is None else failure_depth
        )
        if len(encoded_outcomes) > limits.max_certificate_bytes:
            raise SidewaysResourceLimitError(
                "prefix-then-zero certificate exceeds configured maximum "
                f"{limits.max_certificate_bytes} bytes"
            )
        if failure_depth is not None:
            finite_exclusion_count += 1
        per_prefix.append(
            {
                "prefix_length": prefix_length,
                "trusted_times": f"0..{prefix_length - 1}",
                "zero_tail_start_time": prefix_length,
                "observed_zero_tail_bit_count": horizon + 1 - prefix_length,
                "candidate_trace_sha256_u8": hashlib.sha256(center).hexdigest(),
                "first_nonzero_reconstructed_left_depth": failure_depth,
                "nonzero_reconstructed_left_bits": sum(reconstructed),
                "reconstructed_left_sha256_u8": hashlib.sha256(
                    reconstructed
                ).hexdigest(),
            }
        )

    return {
        "status": "finite-exhaustive",
        "parameters": {
            "horizon": horizon,
            "prefix_lengths": list(prefix_lengths),
            "trace_definition": (
                "copy trusted c_t for 0 <= t < L, then set c_t=0 for every "
                "t >= L; reconstruct only c_0..c_H"
            ),
        },
        "candidate_descriptions": len(prefix_lengths),
        "finite_exclusion_witnesses": finite_exclusion_count,
        "no_witness_through_horizon": len(prefix_lengths) - finite_exclusion_count,
        "logical_cell_update_budget_charged": logical_work,
        "per_prefix": per_prefix,
        "certificate": _failure_certificate(
            search_kind="trusted-prefix-then-permanent-zero",
            horizon=horizon,
            candidate_order="prefix_length in the explicitly listed increasing order",
            outcomes=bytes(encoded_outcomes),
            candidate_count=len(prefix_lengths),
        ),
        "interpretation": (
            "A first nonzero reconstructed-left depth is an exact finite "
            "incompatibility witness for that proposed trace. A zero outcome "
            "means only that no witness occurred through depth H."
        ),
    }


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


def _canonical_graph_edges(
    period: bytes,
    width: int,
    limits: SidewaysLimits,
) -> tuple[dict[str, Any], tuple[tuple[int, int, int, int], ...], bytes]:
    summary = truncated_periodic_state_graph(period, width, limits=limits)
    states_per_phase = 1 << width
    phase_bytes = max(1, (len(period).bit_length() + 7) // 8)
    state_bytes = max(1, (width + 7) // 8)
    edges: list[tuple[int, int, int, int]] = []
    encoded = bytearray()
    for phase, boundary in enumerate(period):
        next_phase = (phase + 1) % len(period)
        for state in range(states_per_phase):
            next_state = truncated_right_transition(state, boundary, width)
            edges.append((phase, state, next_phase, next_state))
            encoded.extend(phase.to_bytes(phase_bytes, "little"))
            encoded.extend(state.to_bytes(state_bytes, "little"))
            encoded.extend(next_phase.to_bytes(phase_bytes, "little"))
            encoded.extend(next_state.to_bytes(state_bytes, "little"))
    if hashlib.sha256(encoded).hexdigest() != summary["transition_sha256"]:
        raise AssertionError("export edge encoding disagrees with graph summary")
    return summary, tuple(edges), bytes(encoded)


def _graph_artifact_payloads(
    max_period: int,
    width: int,
    limits: SidewaysLimits,
) -> dict[str, Any]:
    """Build deterministic DOT, README, and checksum payloads in memory."""

    summaries = _graph_summaries(max_period, width, limits)
    stem = f"fixed_width_periods_1_to_{max_period}_width_{width}"
    dot_name = f"{stem}.dot"
    readme_name = "README.md"
    checksums_name = "SHA256SUMS"
    dot_lines = [
        "digraph rule30_fixed_width_periodic_graphs {",
        '  graph [label="Finite fixed-width Rule 30 graphs; see README scope warning", labelloc="t"];',
        "  rankdir=LR;",
    ]
    graph_metadata: list[dict[str, Any]] = []
    graph_set_digest = hashlib.sha256()

    for graph_index, expected_summary in enumerate(summaries):
        period_length = expected_summary["period_length"]
        word_index = expected_summary["word_index"]
        period = word_from_index(word_index, period_length)
        summary, edges, encoded = _canonical_graph_edges(period, width, limits)
        if summary["transition_sha256"] != expected_summary["transition_sha256"]:
            raise AssertionError("exported graph disagrees with summary ordering")
        graph_set_digest.update(period_length.to_bytes(4, "little"))
        graph_set_digest.update(word_index.to_bytes(8, "little"))
        graph_set_digest.update(hashlib.sha256(encoded).digest())

        dot_lines.append(f"  subgraph cluster_g{graph_index:03d} {{")
        dot_lines.append(f'    label="period={summary["period"]}; width={width}";')
        for phase, state, next_phase, next_state in edges:
            source = (
                f"g{graph_index:03d}_phase{phase}_state"
                f"{state:0{width}b}"
            )
            target = (
                f"g{graph_index:03d}_phase{next_phase}_state"
                f"{next_state:0{width}b}"
            )
            dot_lines.append(f'    "{source}" -> "{target}";')
        dot_lines.append("  }")
        graph_metadata.append(
            {
                "graph_index": graph_index,
                "period_length": period_length,
                "word_index": word_index,
                "period": summary["period"],
                "width": width,
                "node_count": summary["node_count"],
                "edge_count": len(edges),
                "canonical_transition_bytes": len(encoded),
                "canonical_transition_sha256": hashlib.sha256(encoded).hexdigest(),
            }
        )

    dot_lines.append("}")
    dot_bytes = ("\n".join(dot_lines) + "\n").encode("utf-8")
    metadata = {
        "artifact_kind": "fixed-width-rule30-transition-graph-set",
        "parameters": {
            "period_lengths": f"1..{max_period}",
            "word_order": (
                "period length increasing, then unsigned word index increasing; "
                "fixed-width words are MSB-first"
            ),
            "width": width,
            "node_order": "phase increasing, then unsigned right-state increasing",
            "right_state_bits": (
                "integer bit j-1 stores site j; DOT names display integer bits "
                "from most significant to least significant"
            ),
        },
        "canonical_edge_encoding": (
            "phase, state, next_phase, next_state as fixed-width little-endian "
            "unsigned integers; phase width is ceil(bit_length(period_length)/8) "
            "and state width is ceil(width/8), each at least one byte"
        ),
        "scope_warning": GRAPH_SCOPE_WARNING,
        "dot_file": {
            "name": dot_name,
            "bytes": len(dot_bytes),
            "sha256": hashlib.sha256(dot_bytes).hexdigest(),
        },
        "graph_count": len(graph_metadata),
        "graph_set_sha256": graph_set_digest.hexdigest(),
        "graphs": graph_metadata,
    }
    readme_lines = [
        "# Fixed-width Rule 30 transition graphs",
        "",
        (
            f"This directory contains the explicit DOT edge list for all "
            f"binary period-word descriptions of lengths 1 through "
            f"{max_period} at fixed right-half width {width}."
        ),
        "",
        f"> Warning: {GRAPH_SCOPE_WARNING}",
        "",
        (
            "Edges are ordered by increasing period length, unsigned MSB-first "
            "word, phase, and unsigned right-state."
        ),
        (
            "Integer bit `j-1` stores site `j`; DOT state names display bits "
            "most-significant first."
        ),
        "",
        (
            "Canonical edge encoding: phase, state, next phase, and next state "
            "as fixed-width little-endian unsigned integers. The phase width "
            "is `ceil(bit_length(period_length)/8)` and the state width is "
            "`ceil(width/8)`, each at least one byte."
        ),
        "",
        f"- DOT: `{dot_name}` ({len(dot_bytes)} bytes)",
        f"- Graph descriptions: {len(graph_metadata)}",
        f"- Explicit nodes/edges: {sum(item['edge_count'] for item in graph_metadata)}",
        f"- Canonical graph-set SHA-256: `{graph_set_digest.hexdigest()}`",
        "- File hashes: `SHA256SUMS`",
        "",
        "| Period | Nodes | Canonical transition SHA-256 |",
        "|---:|---:|:---|",
    ]
    for graph in graph_metadata:
        readme_lines.append(
            f"| `{graph['period']}` | {graph['node_count']} | "
            f"`{graph['canonical_transition_sha256']}` |"
        )
    readme_lines.append("")
    readme_bytes = "\n".join(readme_lines).encode("utf-8")
    checksums_bytes = (
        f"{hashlib.sha256(dot_bytes).hexdigest()}  {dot_name}\n"
        f"{hashlib.sha256(readme_bytes).hexdigest()}  {readme_name}\n"
    ).encode("ascii")
    return {
        "dot_name": dot_name,
        "dot_bytes": dot_bytes,
        "readme_name": readme_name,
        "readme_bytes": readme_bytes,
        "checksums_name": checksums_name,
        "checksums_bytes": checksums_bytes,
        "metadata": metadata,
    }


def _atomic_write(path: Path, payload: bytes) -> None:
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        if temporary.exists():
            temporary.unlink()


def export_graph_artifacts(
    directory: Path,
    max_period: int,
    width: int,
    limits: SidewaysLimits,
    *,
    max_artifact_bytes: int,
) -> dict[str, Any]:
    if (
        not isinstance(max_artifact_bytes, int)
        or isinstance(max_artifact_bytes, bool)
        or max_artifact_bytes < 0
    ):
        raise ValueError("max_artifact_bytes must be a nonnegative integer")
    payloads = _graph_artifact_payloads(max_period, width, limits)
    total_bytes = (
        len(payloads["dot_bytes"])
        + len(payloads["readme_bytes"])
        + len(payloads["checksums_bytes"])
    )
    if total_bytes > max_artifact_bytes:
        raise SidewaysResourceLimitError(
            f"graph artifacts require {total_bytes} bytes, exceeding configured "
            f"maximum {max_artifact_bytes}"
        )

    resolved_directory = directory.resolve()
    resolved_directory.mkdir(parents=True, exist_ok=True)
    dot_path = resolved_directory / payloads["dot_name"]
    readme_path = resolved_directory / payloads["readme_name"]
    checksums_path = resolved_directory / payloads["checksums_name"]
    _atomic_write(dot_path, payloads["dot_bytes"])
    _atomic_write(readme_path, payloads["readme_bytes"])
    _atomic_write(checksums_path, payloads["checksums_bytes"])
    return {
        "dot_path": _relative_or_absolute(dot_path),
        "dot_bytes": len(payloads["dot_bytes"]),
        "dot_sha256": hashlib.sha256(payloads["dot_bytes"]).hexdigest(),
        "readme_path": _relative_or_absolute(readme_path),
        "readme_bytes": len(payloads["readme_bytes"]),
        "readme_sha256": hashlib.sha256(payloads["readme_bytes"]).hexdigest(),
        "checksums_path": _relative_or_absolute(checksums_path),
        "checksums_bytes": len(payloads["checksums_bytes"]),
        "checksums_sha256": hashlib.sha256(
            payloads["checksums_bytes"]
        ).hexdigest(),
        "canonical_graph_set_sha256": payloads["metadata"]["graph_set_sha256"],
        "combined_bytes": total_bytes,
        "scope_warning": GRAPH_SCOPE_WARNING,
    }


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
    prefix_then_zero = search_true_prefix_then_zero(
        trusted,
        tuple(args.true_prefix_lengths),
        args.horizon,
        limits=limits,
    )
    graphs = _graph_summaries(
        args.graph_max_period,
        args.graph_width,
        limits,
    )
    graph_artifacts = None
    if args.export_graphs_dir is not None:
        graph_artifacts = export_graph_artifacts(
            args.export_graphs_dir,
            args.graph_max_period,
            args.graph_width,
            limits,
            max_artifact_bytes=args.max_graph_artifact_bytes,
        )

    return {
        "schema_version": 1,
        "experiment_id": "problem1-sideways-bounded-search-v1",
        "question": "problem1",
        "hypothesis": (
            "Within the explicitly bounded candidate descriptions and finite "
            "reconstruction horizon, the tested nonzero eventually periodic "
            "traces and listed true-prefix/permanent-zero traces reconstruct "
            "at least one nonzero initial-left cell."
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
            "true_prefix_then_zero_lengths": list(args.true_prefix_lengths),
            "graph_width": args.graph_width,
            "graph_max_period": args.graph_max_period,
            "graph_artifact_export_directory": (
                _relative_or_absolute(args.export_graphs_dir)
                if args.export_graphs_dir is not None
                else None
            ),
            "resource_limits": {
                "max_horizon": limits.max_horizon,
                "max_candidates_per_search": limits.max_candidates,
                "max_logical_cell_updates_per_search": (
                    limits.max_logical_cell_updates
                ),
                "max_certificate_bytes": limits.max_certificate_bytes,
                "max_graph_states_per_graph": limits.max_graph_states,
                "max_reported_survivors": limits.max_reported_survivors,
                "max_graph_artifact_bytes": args.max_graph_artifact_bytes,
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
        "true_prefix_then_permanent_zero_search": prefix_then_zero,
        "fixed_width_state_graphs": {
            "status": "finite-exhaustive",
            "graph_count": len(graphs),
            "graphs": graphs,
            "explicit_artifacts": graph_artifacts,
            "interpretation": GRAPH_SCOPE_WARNING,
        },
        "status": "finite-exhaustive",
        "proof_scope": (
            "Exact enumeration of the stated finite description boxes, exact "
            "Rule 30 inversion for the listed prefix-then-zero traces through "
            "the stated finite horizon, and exact fixed-width functional "
            "graphs only."
        ),
        "interpretation": (
            "A candidate survives only when all reconstructed initial-left bits "
            "within the finite horizon are zero; c_0=1 is checked separately for "
            "single-cell-seed compatibility."
        ),
        "limitations": [
            "no finite horizon proves eventual nonperiodicity",
            "preperiod and period lengths outside the stated boxes are untested",
            "true-prefix lengths outside the explicit list are untested",
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
