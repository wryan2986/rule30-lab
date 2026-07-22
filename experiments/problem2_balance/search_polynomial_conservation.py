#!/usr/bin/env python3
"""Run a deterministic exact campaign over polynomial conservation ansatzes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "python"))

from rule30lab.polynomial_conservation import (  # noqa: E402
    MAX_INPUT_WIDTH,
    search_polynomial_conservation,
    verify_search_certificate,
)


def _sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rule", type=int, default=30)
    parser.add_argument("--minimum-width", type=int, default=6)
    parser.add_argument("--maximum-width", type=int, default=8)
    parser.add_argument("--density-degree", type=int, default=2)
    parser.add_argument("--flux-degree", type=int, default=2)
    parser.add_argument(
        "--time-steps",
        action="append",
        type=int,
        dest="time_steps",
        help="time displacement to search; repeat for multiple values (default: 1)",
    )
    parser.add_argument(
        "--field",
        action="append",
        choices=("rational", "gf2"),
        dest="fields",
        help="coefficient field; repeat as needed (default: both)",
    )
    parser.add_argument("--control-width", type=int, default=2)
    parser.add_argument(
        "--rule204-control",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="run matching Rule 204 positive controls",
    )
    parser.add_argument(
        "--compact", action="store_true", help="emit compact rather than indented JSON"
    )
    return parser


def main() -> int:
    parser = _parser()
    args = parser.parse_args()
    steps = sorted(set(args.time_steps or [1]))
    fields = list(dict.fromkeys(args.fields or ["rational", "gf2"]))
    if args.rule < 0 or args.rule > 255:
        parser.error("rule must be between 0 and 255")
    if args.minimum_width < 1 or args.maximum_width < args.minimum_width:
        parser.error("widths must satisfy 1 <= minimum <= maximum")
    if args.density_degree < 0 or args.flux_degree < 0:
        parser.error("polynomial degrees must be nonnegative")
    if args.rule204_control and args.density_degree < 1:
        parser.error("Rule 204 positive control requires density degree at least one")
    if args.control_width < 1:
        parser.error("control width must be positive")
    if any(step < 1 for step in steps):
        parser.error("time steps must be positive")
    if any(args.maximum_width + 2 * step > MAX_INPUT_WIDTH for step in steps):
        parser.error(
            f"requested width/time combination exceeds input-width cap "
            f"{MAX_INPUT_WIDTH}"
        )
    if args.rule204_control and any(
        args.control_width + 2 * step > MAX_INPUT_WIDTH for step in steps
    ):
        parser.error("Rule 204 control exceeds the input-width cap")

    results = [
        search_polynomial_conservation(
            width,
            args.density_degree,
            args.flux_degree,
            rule=args.rule,
            time_steps=step,
            field=field,
        )
        for field in fields
        for step in steps
        for width in range(args.minimum_width, args.maximum_width + 1)
    ]
    controls = (
        [
            search_polynomial_conservation(
                args.control_width,
                args.density_degree,
                args.flux_degree,
                rule=204,
                time_steps=step,
                field=field,
            )
            for field in fields
            for step in steps
        ]
        if args.rule204_control
        else []
    )
    if not all(verify_search_certificate(result) for result in [*results, *controls]):
        raise AssertionError("a campaign certificate did not verify")
    if controls and not all(
        result["nontrivial_excess_nullity"] > 0 for result in controls
    ):
        raise AssertionError("Rule 204 positive control did not produce excess")

    configuration = {
        "rule": args.rule,
        "minimum_density_width": args.minimum_width,
        "maximum_density_width": args.maximum_width,
        "density_degree": args.density_degree,
        "flux_degree": args.flux_degree,
        "time_steps": steps,
        "fields": fields,
        "rule204_positive_control": args.rule204_control,
        "control_width": args.control_width if args.rule204_control else None,
    }
    payload = {
        "schema_version": 1,
        "question": "problem2",
        "hypothesis": (
            "A bounded-degree multilinear local density and flux may satisfy an "
            "exact one-step or multi-step telescoping identity for Rule 30."
        ),
        "parameters": configuration,
        "results": results,
        "positive_controls": controls,
        "summary": {
            "finite_system_count": len(results),
            "positive_control_count": len(controls),
            "systems_with_excess": sum(
                result["nontrivial_excess_nullity"] > 0 for result in results
            ),
            "positive_controls_with_excess": sum(
                result["nontrivial_excess_nullity"] > 0 for result in controls
            ),
            "result_set_sha256": _sha256(results),
            "positive_control_set_sha256": _sha256(controls),
        },
        "status": "finite-exhaustive",
        "interpretation": (
            "Every reported finite linear system and quotient was solved exactly. "
            "A zero excess count is limited to this enumerated campaign."
        ),
        "limitations": [
            "the campaign has explicit width, degree, time-step, and field bounds",
            "bounded-degree bases are a subset of all block functions at wider widths",
            "the search excludes nonlocal and non-telescoping proof mechanisms",
            "a discovered identity would require a separate link to center discrepancy",
            "no finite campaign proves nonexistence of a global conservation law",
        ],
    }
    print(
        json.dumps(
            payload,
            indent=None if args.compact else 2,
            sort_keys=True,
            allow_nan=False,
            separators=(",", ":") if args.compact else None,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
