#!/usr/bin/env python3
"""Emit deterministic exact bounded local-conservation search results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "python"))

from rule30lab.conservation import search_local_conservation  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rule", type=int, default=30)
    parser.add_argument("--minimum-width", type=int, default=1)
    parser.add_argument("--maximum-width", type=int, default=5)
    args = parser.parse_args()
    if args.minimum_width < 1 or args.maximum_width < args.minimum_width:
        parser.error("widths must satisfy 1 <= minimum <= maximum")
    if args.maximum_width > 6:
        parser.error("maximum width is capped at 6 for conservative exact search")

    results = [
        search_local_conservation(width, rule=args.rule, field=field)
        for field in ("rational", "gf2")
        for width in range(args.minimum_width, args.maximum_width + 1)
    ]
    payload = {
        "schema_version": 1,
        "question": "problem2",
        "hypothesis": (
            "Search for exact telescoping local density/flux identities within "
            "the explicitly bounded ansatz."
        ),
        "parameters": {
            "rule": args.rule,
            "minimum_density_width": args.minimum_width,
            "maximum_density_width": args.maximum_width,
            "fields": ["rational", "gf2"],
        },
        "results": results,
        "status": "finite-exhaustive",
        "interpretation": (
            "Each listed finite linear system is solved exactly. Absence of excess "
            "nullity at tested widths is not a proof of global nonexistence."
        ),
        "limitations": [
            "only scalar block densities and one-step nearest-boundary fluxes are searched",
            "the density width is explicitly bounded",
            "failure does not exclude other rings, nonlocal identities, or other proof tools",
            "a global conservation law would not by itself prove center-column balance",
        ],
    }
    print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
