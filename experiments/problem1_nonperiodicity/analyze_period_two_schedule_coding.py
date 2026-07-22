#!/usr/bin/env python3
"""Check exact period-two zero-survivor schedule coding on finite quotients.

The all-width first-difference, Cantor-geometry, and eventually-periodic
schedule arguments are proved in the accompanying informal note. This script
provides bounded regression checks and does not exclude the actual period-two
schedule or solve Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from itertools import combinations, product
from pathlib import Path
from typing import Any

DEFAULT_DEPTH = 10
DEFAULT_DEGREE_LIMIT = 1 << 16
DEFAULT_SHADOW_WIDTH = 512
MAX_DEPTH = 12
MAX_DEGREE_LIMIT = 1 << 20
MAX_SHADOW_WIDTH = 2048


class ScheduleCodingLimitError(RuntimeError):
    pass


def _load_survivor_module():
    path = Path(__file__).with_name("analyze_period_two_schedule_survivor.py")
    spec = importlib.util.spec_from_file_location("schedule_survivor", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SURVIVOR = _load_survivor_module()


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def common_prefix_length(left: tuple[str, ...], right: tuple[str, ...]) -> int:
    for index, (a, b) in enumerate(zip(left, right)):
        if a != b:
            return index
    return min(len(left), len(right))


def survivor_for_prefix(prefix: tuple[str, ...], width: int) -> int:
    """Return the cylinder residue determined by ``prefix`` modulo 2**width.

    Width ``2n+2`` needs ``n+1`` finite backward branches. The final branch
    acts only at precision two and is immaterial, so a fixed ``t`` filler is
    used for an n-branch cylinder.
    """

    return SURVIVOR.schedule_survivor_residue(prefix + ("t",), width)


def verify_schedule_coding(maximum_depth: int) -> dict[str, Any]:
    levels: list[dict[str, Any]] = []
    final_words: list[tuple[str, ...]] = []
    final_residues: list[int] = []

    for depth in range(maximum_depth + 1):
        width = 2 * depth + 2
        words = list(product(("t", "u"), repeat=depth))
        residues = [survivor_for_prefix(word, width) for word in words]
        assert len(set(residues)) == 1 << depth
        assert all(value % 4 == 3 for value in residues)
        levels.append(
            {
                "depth": depth,
                "quotient_width": width,
                "distinct_cylinders": len(set(residues)),
                "expected_cylinders": 1 << depth,
                "cover_haar_measure_power_of_two": -(depth + 2),
            }
        )
        if depth == maximum_depth:
            final_words, final_residues = words, residues

    width = 2 * maximum_depth + 2
    pair_checks = 0
    for (left_word, left), (right_word, right) in combinations(
        zip(final_words, final_residues), 2
    ):
        first_difference = common_prefix_length(left_word, right_word)
        observed = SURVIVOR.valuation_mod_difference(left, right, width)
        assert observed == 2 * first_difference + 2
        pair_checks += 1

    return {
        "maximum_depth": maximum_depth,
        "levels": levels,
        "final_level_pair_checks": pair_checks,
        "exact_distance_law": "first differing branch n gives v_2=2n+2",
        "all_checks_pass": True,
    }


def forced_zero_step(x_value: int) -> tuple[str, int] | None:
    residue = x_value % 16
    if residue == 7:
        q_name = "u"
    elif residue == 11:
        q_name = "t"
    else:
        return None
    tail = (x_value - 3) >> 2
    return q_name, SURVIVOR.forward_generator(
        q_name, SURVIVOR.forward_generator("p", tail)
    )


def verify_finite_degree_law(limit: int) -> dict[str, Any]:
    checked = 0
    for x_value in range(3, limit, 4):
        step = forced_zero_step(x_value)
        if step is None:
            continue
        _, successor = step
        assert successor.bit_length() == x_value.bit_length() + 2
        checked += 1
    return {
        "exclusive_limit": limit,
        "continuing_states_checked": checked,
        "degree_increment_per_zero_step": 2,
        "all_checks_pass": True,
    }


def verify_periodic_shadow(width: int) -> dict[str, Any]:
    start_block = 2
    period = tuple("ttututt")
    required = max(width // 2 + 2, 200)
    _, actual_all = SURVIVOR.fringe_schedule(start_block + required + 4)
    actual = tuple(actual_all[start_block:])
    periodic = tuple(period[index % len(period)] for index in range(required + 4))
    first_difference = common_prefix_length(actual, periodic)
    assert first_difference == 151

    actual_state = SURVIVOR.schedule_survivor_residue(actual, width)
    periodic_state = SURVIVOR.schedule_survivor_residue(periodic, width)
    valuation = SURVIVOR.valuation_mod_difference(actual_state, periodic_state, width)
    assert valuation == 304
    return {
        "actual_schedule_start_block": start_block,
        "period_word": "".join(period),
        "common_branches": first_difference,
        "first_global_mismatch_block": start_block + first_difference,
        "survivor_2adic_agreement_bits": valuation,
        "comparison_width": width,
        "all_checks_pass": True,
    }


def run_campaign(
    *,
    maximum_coding_depth: int = DEFAULT_DEPTH,
    degree_check_limit: int = DEFAULT_DEGREE_LIMIT,
    shadow_width: int = DEFAULT_SHADOW_WIDTH,
) -> dict[str, Any]:
    if maximum_coding_depth > MAX_DEPTH:
        raise ScheduleCodingLimitError("coding depth exceeds absolute maximum")
    if degree_check_limit > MAX_DEGREE_LIMIT:
        raise ScheduleCodingLimitError("degree limit exceeds absolute maximum")
    if shadow_width > MAX_SHADOW_WIDTH:
        raise ScheduleCodingLimitError("shadow width exceeds absolute maximum")
    if shadow_width < 306 or shadow_width % 2:
        raise ValueError("shadow_width must be even and at least 306")

    payload = {
        "schedule_coding": verify_schedule_coding(maximum_coding_depth),
        "ordinary_degree_law": verify_finite_degree_law(degree_check_limit),
        "actual_periodic_shadow": verify_periodic_shadow(shadow_width),
        "exact_conclusions": {
            "similarity_coding": (
                "the first differing schedule branch n is exactly the first "
                "possible survivor disagreement at bit 2n+2"
            ),
            "cantor_geometry": (
                "the full zero-survivor set is compact, perfect, Haar-null, "
                "and has 2-adic Hausdorff dimension one half"
            ),
            "eventually_periodic_schedule_obstruction": (
                "an eventually periodic branch schedule cannot have an ordinary "
                "finite-support zero survivor because tail uniqueness conflicts "
                "with degree growth by two per step"
            ),
            "actual_shadow": (
                "the actual shift-two survivor agrees for exactly 304 low bits "
                "with the survivor of repeated branch word ttututt"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-schedule-coding-v1\0")
    digest.update(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    )
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--maximum-coding-depth", type=_positive_integer, default=DEFAULT_DEPTH)
    parser.add_argument("--degree-check-limit", type=_positive_integer, default=DEFAULT_DEGREE_LIMIT)
    parser.add_argument("--shadow-width", type=_positive_integer, default=DEFAULT_SHADOW_WIDTH)
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(
        maximum_coding_depth=args.maximum_coding_depth,
        degree_check_limit=args.degree_check_limit,
        shadow_width=args.shadow_width,
    )
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-schedule-coding-v1",
        "question": "problem1",
        "hypothesis": (
            "Zero-survivor schedules form an exact 2-adic Cantor coding, and "
            "eventually periodic schedules are incompatible with ordinary finite support."
        ),
        "backend": "python-exact-2adic-schedule-coding",
        "parameters": {
            "maximum_coding_depth": args.maximum_coding_depth,
            "degree_check_limit": args.degree_check_limit,
            "shadow_width": args.shadow_width,
        },
        "result_summary": result,
        "status": "finite-exhaustive",
        "proof_scope": (
            "All-width similarity, dimension, and periodic-schedule arguments are "
            "proved in proofs/informal/problem1_period_two_schedule_coding.md; "
            "this script checks only bounded quotients and ordinary integers."
        ),
        "interpretation": (
            "Any finite-support period-two zero survivor must be coded by a genuinely "
            "aperiodic auxiliary schedule; the actual schedule remains unresolved."
        ),
        "limitations": [
            "the actual moving-fringe branch schedule is not proved eventually periodic",
            "Haar measure zero and dimension one half do not exclude isolated ordinary integers",
            "the finite seven-block shadow does not imply an infinite periodic schedule",
            "the result does not exclude eventual center period two",
            "the result does not prove Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
