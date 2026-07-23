#!/usr/bin/env python3
"""Classify quadratic parity cocycles for the period-two whole-word strip.

The coupled-strip result closed rational nearest-neighbor additive functionals.
This module tests the next nonlinear class exactly: quadratic polynomials over
GF(2) in the parities of all word factors of length at most three.

For either fixed boundary branch q in {t,u}, assume an identity of the form

    Q(N(q p tau_11(J))) + Q(N(J)) = V(e(J)) + C

holds for every inverse word J.  Here N records factor-count parities, Q has
algebraic degree at most two, and e(J) is the terminal whole-word transducer
state.  Exact GF(2) elimination proves that V must be constant for factor
ranges one, two, and three.  Therefore this nonlinear finite-memory class
cannot distinguish terminal 00 from a nonzero reconstructed pair, even if C
is allowed to depend arbitrarily on the exact current fringe state.

This is a no-go theorem for a specific nonlinear class.  It does not exclude
higher algebraic degree, factor range four or greater, growing memory, period
two, or Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
from typing import Any

DEFAULT_MAXIMUM_FACTOR_RANGE = 3
ABSOLUTE_MAXIMUM_FACTOR_RANGE = 3
LETTERS = ("t", "p", "u")
PAIR_STATES = ((0, 0), (0, 1), (1, 0), (1, 1))
EXPECTED = {
    1: {
        "maximum_word_length": 5,
        "fixed_rows": {"t": 44, "u": 43},
        "fixed_variables": 11,
        "fixed_rank": 9,
        "fixed_nullity": 2,
        "combined_rows": 87,
        "combined_variables": 12,
        "combined_rank": 10,
        "combined_nullity": 2,
    },
    2: {
        "maximum_word_length": 6,
        "fixed_rows": {"t": 920, "u": 923},
        "fixed_variables": 83,
        "fixed_rank": 68,
        "fixed_nullity": 15,
        "combined_rows": 1843,
        "combined_variables": 84,
        "combined_rank": 69,
        "combined_nullity": 15,
    },
    3: {
        "maximum_word_length": 7,
        "fixed_rows": {"t": 3211, "u": 3211},
        "fixed_variables": 785,
        "fixed_rank": 581,
        "fixed_nullity": 204,
        "combined_rows": 6422,
        "combined_variables": 786,
        "combined_rank": 582,
        "combined_nullity": 204,
    },
}


class QuadraticParityLimitError(RuntimeError):
    """Raised before an explicitly capped exact campaign is exceeded."""


def _load_sibling(filename: str, module_name: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


COUPLED = _load_sibling(
    "analyze_period_two_coupled_strip.py", "period_two_coupled_strip"
)


def factor_patterns(maximum_range: int) -> tuple[tuple[str, ...], ...]:
    if not 1 <= maximum_range <= ABSOLUTE_MAXIMUM_FACTOR_RANGE:
        raise ValueError("factor range must be between one and three")
    return tuple(
        pattern
        for width in range(1, maximum_range + 1)
        for pattern in itertools.product(LETTERS, repeat=width)
    )


def factor_parities_direct(
    word: tuple[str, ...], patterns: tuple[tuple[str, ...], ...]
) -> tuple[int, ...]:
    values = []
    for pattern in patterns:
        width = len(pattern)
        count = sum(
            tuple(word[index : index + width]) == pattern
            for index in range(len(word) - width + 1)
        )
        values.append(count & 1)
    return tuple(values)


def factor_parities_streaming(
    word: tuple[str, ...], patterns: tuple[tuple[str, ...], ...]
) -> tuple[int, ...]:
    index = {pattern: offset for offset, pattern in enumerate(patterns)}
    values = [0] * len(patterns)
    maximum_range = max((len(pattern) for pattern in patterns), default=0)
    for right in range(len(word)):
        for width in range(1, min(maximum_range, right + 1) + 1):
            pattern = tuple(word[right - width + 1 : right + 1])
            values[index[pattern]] ^= 1
    return tuple(values)


def quadratic_monomials(feature_count: int) -> tuple[tuple[int, ...], ...]:
    return tuple((index,) for index in range(feature_count)) + tuple(
        (left, right)
        for left in range(feature_count)
        for right in range(left + 1, feature_count)
    )


def quadratic_feature_mask(
    parities: tuple[int, ...], monomials: tuple[tuple[int, ...], ...]
) -> int:
    mask = 0
    for index, monomial in enumerate(monomials):
        if all(parities[feature] for feature in monomial):
            mask |= 1 << index
    return mask


def _gf2_rank(rows: list[int]) -> int:
    basis: dict[int, int] = {}
    for original in rows:
        row = original
        while row:
            pivot = (row & -row).bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return len(basis)


def _terminal_difference_mask(
    variable_names: tuple[str, ...], state: tuple[int, int]
) -> int:
    left = variable_names.index(f"V_{state[0]}{state[1]}")
    right = variable_names.index("V_11")
    return (1 << left) ^ (1 << right)


def _equation_system(
    maximum_range: int,
    maximum_word_length: int,
    branches: tuple[str, ...],
) -> tuple[list[int], tuple[str, ...]]:
    patterns = factor_patterns(maximum_range)
    monomials = quadratic_monomials(len(patterns))
    monomial_names = tuple(
        "M_" + "_".join(str(index) for index in monomial)
        for monomial in monomials
    )
    variable_names = (
        monomial_names
        + tuple(f"V_{state[0]}{state[1]}" for state in PAIR_STATES)
        + tuple(f"K_{branch}" for branch in branches)
    )
    variable_index = {name: index for index, name in enumerate(variable_names)}
    rows: list[int] = []
    seen: set[int] = set()

    for length in range(maximum_word_length + 1):
        for word in itertools.product(LETTERS, repeat=length):
            scanned, terminal = COUPLED.scan_reversed_word(word)
            before_direct = factor_parities_direct(word, patterns)
            before_streaming = factor_parities_streaming(word, patterns)
            if before_direct != before_streaming:
                raise AssertionError("independent factor-parity implementations disagree")
            before_mask = quadratic_feature_mask(before_direct, monomials)

            for branch in branches:
                after_word = (branch, "p") + scanned
                after_direct = factor_parities_direct(after_word, patterns)
                after_streaming = factor_parities_streaming(after_word, patterns)
                if after_direct != after_streaming:
                    raise AssertionError(
                        "independent transformed factor-parity implementations disagree"
                    )
                row = before_mask ^ quadratic_feature_mask(after_direct, monomials)
                row ^= 1 << variable_index[f"V_{terminal[0]}{terminal[1]}"]
                row ^= 1 << variable_index[f"K_{branch}"]
                if row not in seen:
                    seen.add(row)
                    rows.append(row)
    return rows, variable_names


def _verify_terminal_potential_is_constant(
    rows: list[int], variable_names: tuple[str, ...]
) -> dict[str, Any]:
    rank = _gf2_rank(rows)
    forced: dict[str, bool] = {}
    for state in ((0, 0), (0, 1), (1, 0)):
        difference = _terminal_difference_mask(variable_names, state)
        forced["".join(map(str, state))] = _gf2_rank(rows + [difference]) == rank
    if not all(forced.values()):
        raise AssertionError("quadratic parity class can distinguish terminal states")
    return {
        "rank": rank,
        "nullity": len(variable_names) - rank,
        "terminal_equalities_forced": forced,
        "terminal_potential": "V_00=V_01=V_10=V_11",
    }


def verify_range(maximum_range: int) -> dict[str, Any]:
    expected = EXPECTED[maximum_range]
    maximum_word_length = expected["maximum_word_length"]
    fixed_results: dict[str, Any] = {}

    for branch in ("t", "u"):
        rows, names = _equation_system(
            maximum_range, maximum_word_length, (branch,)
        )
        result = _verify_terminal_potential_is_constant(rows, names)
        if len(rows) != expected["fixed_rows"][branch]:
            raise AssertionError("unexpected fixed-branch equation count")
        if len(names) != expected["fixed_variables"]:
            raise AssertionError("unexpected fixed-branch variable count")
        if result["rank"] != expected["fixed_rank"]:
            raise AssertionError("unexpected fixed-branch rank")
        if result["nullity"] != expected["fixed_nullity"]:
            raise AssertionError("unexpected fixed-branch nullity")
        result.update({"equations": len(rows), "variables": len(names)})
        fixed_results[branch] = result

    combined_rows, combined_names = _equation_system(
        maximum_range, maximum_word_length, ("t", "u")
    )
    combined = _verify_terminal_potential_is_constant(
        combined_rows, combined_names
    )
    if len(combined_rows) != expected["combined_rows"]:
        raise AssertionError("unexpected combined equation count")
    if len(combined_names) != expected["combined_variables"]:
        raise AssertionError("unexpected combined variable count")
    if combined["rank"] != expected["combined_rank"]:
        raise AssertionError("unexpected combined rank")
    if combined["nullity"] != expected["combined_nullity"]:
        raise AssertionError("unexpected combined nullity")
    combined.update({"equations": len(combined_rows), "variables": len(combined_names)})

    return {
        "maximum_factor_range": maximum_range,
        "maximum_word_length_needed": maximum_word_length,
        "factor_parity_features": sum(3**width for width in range(1, maximum_range + 1)),
        "quadratic_monomials": len(
            quadratic_monomials(
                sum(3**width for width in range(1, maximum_range + 1))
            )
        ),
        "fixed_branch_systems": fixed_results,
        "combined_branch_system": combined,
        "exact_conclusion": (
            "every degree-at-most-two GF(2) polynomial in factor-count parities "
            "of this range has terminal-pair potential constant in any all-word "
            "one-step cocycle identity"
        ),
        "all_checks_pass": True,
    }


def run_campaign(
    maximum_factor_range: int = DEFAULT_MAXIMUM_FACTOR_RANGE,
) -> dict[str, Any]:
    if maximum_factor_range > ABSOLUTE_MAXIMUM_FACTOR_RANGE:
        raise QuadraticParityLimitError(
            f"factor range exceeds absolute maximum {ABSOLUTE_MAXIMUM_FACTOR_RANGE}"
        )
    if maximum_factor_range <= 0:
        raise ValueError("maximum_factor_range must be positive")

    payload = {
        "ranges": [verify_range(value) for value in range(1, maximum_factor_range + 1)],
        "exact_conclusions": {
            "nonlinear_no_go": (
                "quadratic parity functionals of factor counts through range three cannot distinguish terminal 00 from a nonzero output pair"
            ),
            "actual_orbit_scope": (
                "allowing an arbitrary potential on the exact current fringe state only changes the branch equation by a scalar and therefore does not evade the fixed-branch theorem"
            ),
            "remaining_target": (
                "higher algebraic degree, factor range at least four, genuinely growing memory, or a non-factor-based nonlinear observable"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-quadratic-parity-v1\0")
    digest.update(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maximum-factor-range",
        type=int,
        default=DEFAULT_MAXIMUM_FACTOR_RANGE,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(args.maximum_factor_range)
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-quadratic-parity-v1",
        "question": "problem1",
        "hypothesis": (
            "A quadratic parity cocycle using complete factor-count parities might distinguish terminal zero output after rational additive cocycles fail."
        ),
        "backend": "python-exact-gf2-bitset-elimination",
        "parameters": {"maximum_factor_range": args.maximum_factor_range},
        "result_summary": result,
        "status": "partial-proof",
        "proof_scope": (
            "The finite GF(2) systems are coefficient proofs: any proposed all-word identity belongs to the finite subsystem, whose exact row space forces the terminal potential constant."
        ),
        "limitations": [
            "covers algebraic degree at most two only",
            "covers factor-count parities of factors of length at most three only",
            "does not cover nonlinear observables depending on factor order beyond counts",
            "does not cover growing memory",
            "does not exclude eventual center period two",
            "does not solve Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
