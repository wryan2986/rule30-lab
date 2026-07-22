#!/usr/bin/env python3
"""Emit deterministic finite-only extended Problem 3 model searches as JSON."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "python"))

from rule30lab.transducer_search import (  # noqa: E402
    finite_two_kernel_refinement,
    search_affine_digit_models,
)


DEFAULT_INPUT = (
    REPOSITORY_ROOT
    / "tests"
    / "reference_vectors"
    / "center_c00000000_c00009999.u8"
)
MAX_INPUT_BYTES = 64 * 1024 * 1024


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Print deterministic bounded affine-transducer and multiscale "
            "2-kernel searches. No result file is written."
        )
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--limit-bits", type=int, default=10_000)
    parser.add_argument("--affine-train-length", type=int, default=64)
    parser.add_argument("--pilot-train-length", type=int, default=8)
    parser.add_argument("--affine-min-dimension", type=int, default=1)
    parser.add_argument("--affine-max-dimension", type=int, default=2)
    parser.add_argument("--affine-max-models", type=int, default=200_000)
    parser.add_argument("--affine-selected-fits", type=int, default=256)
    parser.add_argument("--kernel-train-length", type=int, default=5_000)
    parser.add_argument("--kernel-max-level", type=int, default=4)
    parser.add_argument("--kernel-refinement-rounds", type=int, default=7)
    parser.add_argument("--kernel-max-nodes", type=int, default=1_000_000)
    parser.add_argument("--kernel-max-work-entries", type=int, default=8_000_000)
    return parser


def _read_input(path: Path, limit_bits: int) -> tuple[Path, bytes, str]:
    if limit_bits < 2:
        raise ValueError("limit_bits must be at least 2")
    resolved = path.resolve(strict=True)
    size = resolved.stat().st_size
    if size > MAX_INPUT_BYTES:
        raise MemoryError(
            f"input has {size} bytes, exceeding cap {MAX_INPUT_BYTES}"
        )
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
    for name, split in (
        ("affine_train_length", args.affine_train_length),
        ("pilot_train_length", args.pilot_train_length),
        ("kernel_train_length", args.kernel_train_length),
    ):
        if split < 1 or split >= len(bits):
            raise ValueError(f"{name} must be between 1 and {len(bits) - 1}")

    affine_arguments = {
        "min_dimension": args.affine_min_dimension,
        "max_dimension": args.affine_max_dimension,
        "max_models": args.affine_max_models,
        "max_selected_training_fits": args.affine_selected_fits,
    }
    affine_primary = search_affine_digit_models(
        bits, train_length=args.affine_train_length, **affine_arguments
    )
    affine_pilot = search_affine_digit_models(
        bits, train_length=args.pilot_train_length, **affine_arguments
    )
    kernel = finite_two_kernel_refinement(
        bits,
        train_length=args.kernel_train_length,
        max_level=args.kernel_max_level,
        refinement_rounds=args.kernel_refinement_rounds,
        max_nodes=args.kernel_max_nodes,
        max_work_entries=args.kernel_max_work_entries,
    )

    completion = {
        "affine_primary_completed": affine_primary["completion"][
            "all_requested_searches_completed"
        ],
        "affine_short_training_counterexample_probe_completed": affine_pilot[
            "completion"
        ]["all_requested_searches_completed"],
        "multiscale_two_kernel_completed": kernel["completion"][
            "all_requested_searches_completed"
        ],
    }
    completion["all_requested_searches_completed"] = all(completion.values())

    return {
        "schema_version": 1,
        "experiment_id": "problem3-extended-exact-model-searches-v1",
        "question": "problem3",
        "hypothesis": (
            "Determine whether any explicitly bounded affine GF(2) binary-digit "
            "matrix product fits the Rule 30 center prefix, and whether a deeper "
            "multiscale finite 2-kernel partition closes under child transitions."
        ),
        "backend": "python",
        "parameters": {
            "limit_bits": args.limit_bits,
            "affine_primary_train_length": args.affine_train_length,
            "affine_pilot_train_length": args.pilot_train_length,
            "affine_min_dimension": args.affine_min_dimension,
            "affine_max_dimension": args.affine_max_dimension,
            "affine_max_models": args.affine_max_models,
            "affine_selected_fits": args.affine_selected_fits,
            "kernel_train_length": args.kernel_train_length,
            "kernel_max_level": args.kernel_max_level,
            "kernel_refinement_rounds": args.kernel_refinement_rounds,
            "kernel_max_nodes": args.kernel_max_nodes,
            "kernel_max_work_entries": args.kernel_max_work_entries,
        },
        "input": {
            "path": str(input_path),
            "encoding": "one_byte_per_bit_c_0_first",
            "available_input_bytes": input_path.stat().st_size,
            "used_bit_count": len(bits),
            "sha256_used_u8": input_hash,
        },
        "training_validation_protocol": {
            "affine_primary": {
                "training": {"start": 0, "stop": args.affine_train_length},
                "held_out": {
                    "start": args.affine_train_length,
                    "stop": len(bits),
                },
            },
            "affine_short_training_counterexample_probe": {
                "training": {"start": 0, "stop": args.pilot_train_length},
                "held_out": {
                    "start": args.pilot_train_length,
                    "stop": len(bits),
                },
                "purpose": (
                    "exercise active first-counterexample localization on models "
                    "selected by a deliberately short but disjoint training prefix"
                ),
            },
            "multiscale_two_kernel": {
                "training": {"start": 0, "stop": args.kernel_train_length},
                "held_out": {
                    "start": args.kernel_train_length,
                    "stop": len(bits),
                },
            },
            "leakage_control": (
                "candidate enumeration, ordering, selection, kernel signatures, "
                "and quotient construction use training bits only and are frozen "
                "before held-out bits are inspected"
            ),
            "deterministic_seed": 0,
            "randomness_used": False,
        },
        "result_summary": {
            "affine_primary": affine_primary,
            "affine_short_training_counterexample_probe": affine_pilot,
            "multiscale_two_kernel": kernel,
            "completion": completion,
        },
        "status": (
            "finite-exhaustive"
            if completion["all_requested_searches_completed"]
            else "inconclusive"
        ),
        "proof_scope": (
            "only the exact reported finite model-ID ranges, finite prefix "
            "comparisons, and finite 2-kernel partition/closure checks"
        ),
        "interpretation": (
            "The pilot is a counterexample-localization control, while the longer "
            "split is the substantive bounded affine search. No outcome proves "
            "or refutes automaticity or a complexity lower bound."
        ),
        "limitations": [
            "no finite search proves nonautomaticity",
            "no failed model search proves another exact representation absent",
            "finite held-out agreement does not establish an identity for all n",
            "finite 2-kernel classes need not persist at greater depth",
            "no result establishes an o(n) algorithm or an Omega(n) lower bound",
        ],
    }


def main() -> int:
    payload = build_payload(_parser().parse_args())
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
