#!/usr/bin/env python3
"""Emit deterministic JSON for bounded exact Problem 3 model searches.

The script reads a trusted one-byte-per-bit prefix and writes JSON only to
standard output.  It deliberately omits timestamps and runtimes so identical
inputs and parameters have byte-identical payloads.  An experiment orchestrator
may add machine/run metadata and atomically capture stdout separately.
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

from rule30lab.predictor_search import (  # noqa: E402
    fit_berlekamp_massey_candidate,
    fit_two_kernel_quotient_dfao,
    search_boolean_window_recurrences,
    search_labeled_dfaos,
    search_short_gf2_recurrences,
)


DEFAULT_INPUT = (
    REPOSITORY_ROOT
    / "tests"
    / "reference_vectors"
    / "center_c00000000_c00009999.u8"
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Print deterministic finite-only DFAO, 2-kernel, and recurrence "
            "search results; no result file is written."
        )
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--limit-bits", type=int, default=10_000)
    parser.add_argument("--train-length", type=int, default=5_000)
    parser.add_argument("--max-reported-errors", type=int, default=8)

    parser.add_argument("--dfao-min-states", type=int, default=1)
    parser.add_argument("--dfao-max-states", type=int, default=3)
    parser.add_argument("--dfao-start-state", type=int)
    parser.add_argument("--dfao-start-model-id", type=int, default=0)
    parser.add_argument("--dfao-max-models", type=int, default=100_000)
    parser.add_argument("--dfao-max-state-count-cap", type=int, default=16)

    parser.add_argument("--kernel-depth", type=int, default=5)
    parser.add_argument("--kernel-fingerprint-length", type=int, default=64)
    parser.add_argument("--kernel-max-nodes", type=int, default=131_071)
    parser.add_argument(
        "--kernel-max-fingerprint-bytes", type=int, default=64 * 1024 * 1024
    )

    parser.add_argument("--gf2-max-order", type=int, default=12)
    parser.add_argument("--gf2-start-candidate-id", type=int, default=0)
    parser.add_argument("--gf2-max-candidates", type=int, default=1_000_000)
    parser.add_argument("--gf2-max-order-cap", type=int, default=64)

    parser.add_argument("--boolean-min-window", type=int, default=1)
    parser.add_argument("--boolean-max-window", type=int, default=12)
    parser.add_argument("--boolean-start-window", type=int)
    parser.add_argument("--boolean-start-completion-id", type=int, default=0)
    parser.add_argument("--boolean-max-completions", type=int, default=1_000_000)
    parser.add_argument("--boolean-max-unseen-contexts", type=int, default=20)
    parser.add_argument("--boolean-max-table-entries", type=int, default=1_048_576)
    return parser


def _read_input(path: Path, limit_bits: int) -> tuple[Path, bytes, str]:
    if limit_bits < 2:
        raise ValueError("limit_bits must be at least 2")
    resolved = path.resolve()
    complete = resolved.read_bytes()
    if limit_bits > len(complete):
        raise ValueError(
            f"limit_bits={limit_bits} exceeds input length {len(complete)}"
        )
    bits = complete[:limit_bits]
    for index, bit in enumerate(bits):
        if bit not in (0, 1):
            raise ValueError(f"input byte at index {index} is not 0 or 1")
    return resolved, bits, hashlib.sha256(bits).hexdigest()


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    input_path, bits, input_hash = _read_input(args.input, args.limit_bits)
    if args.train_length < 1 or args.train_length >= len(bits):
        raise ValueError(
            f"train_length must be between 1 and {len(bits) - 1}"
        )

    common_errors = args.max_reported_errors
    dfao = search_labeled_dfaos(
        bits,
        train_length=args.train_length,
        min_states=args.dfao_min_states,
        max_states=args.dfao_max_states,
        start_state_count=args.dfao_start_state,
        start_model_id=args.dfao_start_model_id,
        max_models=args.dfao_max_models,
        stop_after_fits=1,
        max_reported_fits=1,
        max_reported_errors=common_errors,
        max_state_count_cap=args.dfao_max_state_count_cap,
    )
    kernel = fit_two_kernel_quotient_dfao(
        bits,
        train_length=args.train_length,
        depth=args.kernel_depth,
        fingerprint_length=args.kernel_fingerprint_length,
        max_nodes=args.kernel_max_nodes,
        max_fingerprint_bytes=args.kernel_max_fingerprint_bytes,
        max_reported_errors=common_errors,
    )
    gf2 = search_short_gf2_recurrences(
        bits,
        train_length=args.train_length,
        max_order=args.gf2_max_order,
        start_candidate_id=args.gf2_start_candidate_id,
        max_candidates=args.gf2_max_candidates,
        stop_after_fits=1,
        max_reported_fits=1,
        max_reported_errors=common_errors,
        max_order_cap=args.gf2_max_order_cap,
    )
    berlekamp_massey = fit_berlekamp_massey_candidate(
        bits,
        train_length=args.train_length,
        max_reported_errors=common_errors,
    )
    nonlinear = search_boolean_window_recurrences(
        bits,
        train_length=args.train_length,
        min_window=args.boolean_min_window,
        max_window=args.boolean_max_window,
        start_window=args.boolean_start_window,
        start_completion_id=args.boolean_start_completion_id,
        max_completions=args.boolean_max_completions,
        max_unseen_contexts=args.boolean_max_unseen_contexts,
        max_table_entries=args.boolean_max_table_entries,
        max_reported_candidates=8,
        max_reported_table_entries=256,
        max_reported_errors=common_errors,
    )

    bounded_completion = {
        "dfao_completed": dfao["enumeration"]["completed_requested_range"],
        "gf2_completed": gf2["enumeration"]["completed_requested_range"],
        "boolean_completed": nonlinear["enumeration"][
            "completed_requested_range"
        ],
        "kernel_construction_checked": True,
        "berlekamp_massey_candidate_checked": True,
    }
    bounded_completion["all_requested_searches_completed"] = all(
        bounded_completion.values()
    )
    overall_status = (
        "finite-exhaustive"
        if bounded_completion["all_requested_searches_completed"]
        else "inconclusive"
    )

    return {
        "schema_version": 1,
        "experiment_id": "problem3-trusted-prefix-exact-searches-v1",
        "question": "problem3",
        "hypothesis": (
            "Determine whether any model in several explicitly bounded exact "
            "DFAO and recurrence classes fits a strict training prefix and then "
            "survives a disjoint held-out prefix."
        ),
        "backend": "python",
        "parameters": {
            "limit_bits": args.limit_bits,
            "train_length": args.train_length,
            "max_reported_errors": args.max_reported_errors,
            "dfao": {
                "min_states": args.dfao_min_states,
                "max_states": args.dfao_max_states,
                "start_state": args.dfao_start_state,
                "start_model_id": args.dfao_start_model_id,
                "max_models": args.dfao_max_models,
                "max_state_count_cap": args.dfao_max_state_count_cap,
            },
            "two_kernel": {
                "depth": args.kernel_depth,
                "fingerprint_length": args.kernel_fingerprint_length,
                "max_nodes": args.kernel_max_nodes,
                "max_fingerprint_bytes": args.kernel_max_fingerprint_bytes,
            },
            "gf2": {
                "max_order": args.gf2_max_order,
                "start_candidate_id": args.gf2_start_candidate_id,
                "max_candidates": args.gf2_max_candidates,
                "max_order_cap": args.gf2_max_order_cap,
            },
            "boolean_recurrence": {
                "min_window": args.boolean_min_window,
                "max_window": args.boolean_max_window,
                "start_window": args.boolean_start_window,
                "start_completion_id": args.boolean_start_completion_id,
                "max_completions": args.boolean_max_completions,
                "max_unseen_contexts": args.boolean_max_unseen_contexts,
                "max_table_entries": args.boolean_max_table_entries,
            },
        },
        "input": {
            "path": str(input_path),
            "encoding": "one_byte_per_bit_c_0_first",
            "available_input_bytes": input_path.stat().st_size,
            "used_bit_count": len(bits),
            "sha256_used_u8": input_hash,
        },
        "training_validation_protocol": {
            "training": {"start": 0, "stop": args.train_length},
            "held_out": {"start": args.train_length, "stop": len(bits)},
            "leakage_control": (
                "all models and deterministic enumeration choices are fixed from "
                "training bits before held-out bits are inspected"
            ),
            "deterministic_seed": 0,
            "randomness_used": False,
        },
        "result_summary": {
            "labeled_dfaos": dfao,
            "finite_two_kernel_quotient": kernel,
            "short_gf2_recurrences": gf2,
            "berlekamp_massey_candidate": berlekamp_massey,
            "boolean_window_recurrences": nonlinear,
            "completion": bounded_completion,
        },
        "interpretation": (
            "Every count and counterexample is exact for the identified finite "
            "input and bounded model class. Search failure has no asymptotic or "
            "universal interpretation."
        ),
        "status": overall_status,
        "proof_scope": (
            "only the exact bounded enumerations, quotient consistency checks, "
            "and finite training/validation comparisons embedded in this payload"
        ),
        "limitations": [
            "no finite result proves or refutes automaticity of the infinite sequence",
            "no failed search proves that another exact representation does not exist",
            "no result establishes an o(n) algorithm or an Omega(n) lower bound",
            (
                "training-derived tables constitute finite-prefix advice until "
                "independently proved uniform"
            ),
            "the three published interpretations of Problem 3 remain separate",
        ],
    }


def main() -> int:
    args = _parser().parse_args()
    payload = build_payload(args)
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
