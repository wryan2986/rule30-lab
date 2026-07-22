#!/usr/bin/env python3
"""Verify exact 2-adic fixed points of the period-two zero-streak map.

The renewal reduction gives a partial map on normalized preimages ``x``:

* if ``x == 7 (mod 16)``, the only zero-continuing branch is ``U(P((x-3)/4))``;
* if ``x == 11 (mod 16)``, the only zero-continuing branch is ``T(P((x-3)/4))``.

This script verifies, on exact finite quotients, the rational 2-adic fixed
points ``5/3`` and ``1/3`` and the shadowing of those points by ordinary
finite truncations.  The all-width proof is in the accompanying informal note.
It does not show that the actual period-two schedule follows either constant
branch and does not solve Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any


DEFAULT_MAXIMUM_WIDTH = 64
ABSOLUTE_MAXIMUM_WIDTH = 256


class CountermodelLimitError(RuntimeError):
    """Raised before an explicitly capped quotient campaign is exceeded."""


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def forward_generator(name: str, state: int) -> int:
    """Apply the forward ``T``, ``P``, or ``U`` map to a finite integer."""

    if state < 0:
        raise ValueError("state must be nonnegative")
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    if name == "u":
        return stepped ^ 1
    raise ValueError(f"unknown generator {name!r}")


def rational_residue(numerator: int, denominator: int, width: int) -> int:
    """Return an odd-denominator rational modulo ``2**width``."""

    if width <= 0:
        raise ValueError("width must be positive")
    if denominator & 1 == 0:
        raise ValueError("denominator must be odd")
    modulus = 1 << width
    return (numerator * pow(denominator, -1, modulus)) % modulus


def zero_branch_step_from_residue(
    x_residue: int, *, input_width: int, q_name: str
) -> int:
    """Apply one zero-branch step and return ``input_width-2`` output bits.

    Two bits are lost because the map first removes the forced low block ``11``.
    The forward generators are triangular, so the remaining input precision is
    sufficient for exactly that many output bits.
    """

    if input_width < 4:
        raise ValueError("input_width must be at least four")
    if q_name not in ("t", "u"):
        raise ValueError("q_name must be 't' or 'u'")
    modulus = 1 << input_width
    x_residue %= modulus
    if x_residue % 4 != 3:
        raise ValueError("x must be congruent to 3 modulo 4")
    tail = (x_residue - 3) >> 2
    output = forward_generator(q_name, forward_generator("p", tail))
    return output % (1 << (input_width - 2))


def forced_zero_step(x_value: int) -> tuple[str, int] | None:
    """Apply the unique ordinary-integer zero continuation when available."""

    if x_value < 0 or x_value % 4 != 3:
        raise ValueError("x must be a nonnegative integer congruent to 3 mod 4")
    residue = x_value % 16
    if residue == 7:
        q_name = "u"
    elif residue == 11:
        q_name = "t"
    else:
        return None
    tail = (x_value - 3) >> 2
    return q_name, forward_generator(
        q_name, forward_generator("p", tail)
    )


def survival_depth(x_value: int, cap: int) -> tuple[int, str]:
    """Return zero-continuation depth and the forced branch word."""

    branches: list[str] = []
    for _ in range(cap):
        step = forced_zero_step(x_value)
        if step is None:
            break
        q_name, x_value = step
        branches.append(q_name)
    return len(branches), "".join(branches)


def fixed_point_specs() -> tuple[dict[str, Any], ...]:
    return (
        {
            "name": "u-branch fixed point",
            "numerator": 5,
            "denominator": 3,
            "q_name": "u",
            "required_residue_mod_16": 7,
            "tail_numerator": -1,
            "tail_denominator": 3,
        },
        {
            "name": "t-branch fixed point",
            "numerator": 1,
            "denominator": 3,
            "q_name": "t",
            "required_residue_mod_16": 11,
            "tail_numerator": -2,
            "tail_denominator": 3,
        },
    )


def verify_fixed_points(maximum_width: int) -> list[dict[str, Any]]:
    """Verify both rational fixed points on every quotient through the cap."""

    results: list[dict[str, Any]] = []
    for spec in fixed_point_specs():
        quotient_checks = 0
        for width in range(4, maximum_width + 1):
            input_width = width + 2
            x_input = rational_residue(
                spec["numerator"], spec["denominator"], input_width
            )
            if x_input % 16 != spec["required_residue_mod_16"]:
                raise AssertionError("fixed point is in the wrong branch cylinder")
            tail = (x_input - 3) >> 2
            expected_tail = rational_residue(
                spec["tail_numerator"],
                spec["tail_denominator"],
                width,
            )
            if tail != expected_tail:
                raise AssertionError("forced low-bit division identity failed")
            stepped = zero_branch_step_from_residue(
                x_input, input_width=input_width, q_name=spec["q_name"]
            )
            expected = rational_residue(
                spec["numerator"], spec["denominator"], width
            )
            if stepped != expected:
                raise AssertionError("rational fixed-point quotient failed")
            quotient_checks += 1

        results.append(
            {
                **spec,
                "quotient_widths_checked": [4, maximum_width],
                "quotient_checks": quotient_checks,
                "all_checks_pass": True,
            }
        )
    return results


def verify_finite_truncation_shadowing(
    maximum_width: int,
) -> list[dict[str, Any]]:
    """Check the rigorous linear shadowing lower bound on finite truncations."""

    results: list[dict[str, Any]] = []
    for spec in fixed_point_specs():
        rows = []
        for width in range(4, maximum_width + 1):
            x_value = rational_residue(
                spec["numerator"], spec["denominator"], width
            )
            guaranteed_steps = (width - 4) // 2 + 1
            actual_depth, branch_word = survival_depth(
                x_value, maximum_width + 4
            )
            if actual_depth < guaranteed_steps:
                raise AssertionError("finite truncation violated shadowing bound")
            if branch_word[:guaranteed_steps] != (
                spec["q_name"] * guaranteed_steps
            ):
                raise AssertionError("truncation left the fixed branch too early")
            rows.append(
                {
                    "width": width,
                    "finite_residue": x_value,
                    "guaranteed_zero_steps": guaranteed_steps,
                    "observed_zero_steps": actual_depth,
                    "guaranteed_branch_prefix": spec["q_name"]
                    * guaranteed_steps,
                }
            )
        results.append(
            {
                "name": spec["name"],
                "width_range": [4, maximum_width],
                "rows": rows,
                "all_checks_pass": True,
            }
        )
    return results


def run_campaign(maximum_width: int = DEFAULT_MAXIMUM_WIDTH) -> dict[str, Any]:
    if maximum_width < 4:
        raise ValueError("maximum_width must be at least four")
    if maximum_width > ABSOLUTE_MAXIMUM_WIDTH:
        raise CountermodelLimitError(
            f"width exceeds absolute maximum {ABSOLUTE_MAXIMUM_WIDTH}"
        )

    payload = {
        "maximum_width": maximum_width,
        "fixed_points": verify_fixed_points(maximum_width),
        "finite_truncation_shadowing": verify_finite_truncation_shadowing(
            maximum_width
        ),
        "exact_conclusions": [
            "x=5/3 is the unique 2-adic fixed point in the constant-u branch cylinder x=7 mod 16",
            "x=1/3 is the unique 2-adic fixed point in the constant-t branch cylinder x=11 mod 16",
            "same-branch 2-adic agreement loses exactly two bits per zero step",
            "finite truncations therefore shadow either fixed point for at least floor((N-4)/2)+1 zero steps",
            "the partial integer map alone cannot support a uniform finite zero-run bound",
        ],
    }
    certificate = hashlib.sha256()
    certificate.update(b"rule30-period-two-2adic-zero-countermodels-v1\0")
    certificate.update(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    )
    payload["certificate_sha256"] = certificate.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Verify rational 2-adic zero-streak countermodels."
    )
    parser.add_argument(
        "--maximum-width",
        type=_positive_integer,
        default=DEFAULT_MAXIMUM_WIDTH,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(args.maximum_width)
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-2adic-zero-countermodels-v1",
        "question": "problem1",
        "hypothesis": (
            "The partial period-two zero-streak map admits exact rational "
            "2-adic fixed points, so low-residue dynamics alone cannot prove "
            "termination on finite-support states."
        ),
        "backend": "python-exact-2adic-quotients",
        "parameters": {
            "maximum_width": args.maximum_width,
            "absolute_maximum_width": ABSOLUTE_MAXIMUM_WIDTH,
        },
        "result_summary": result,
        "status": "finite-exhaustive",
        "proof_scope": (
            "The rational identities, branch uniqueness, and two-bit loss of "
            "2-adic agreement are proved in "
            "proofs/informal/problem1_period_two_2adic_zero_countermodels.md. "
            "Finite quotients and ordinary truncations are regression checks."
        ),
        "interpretation": (
            "Any successful period-two exclusion must use eventual-zero binary "
            "support or mismatch with the actual moving-fringe schedule. It "
            "cannot follow from the partial zero-streak map on the full 2-adic "
            "state space alone."
        ),
        "limitations": [
            "the fixed points are infinite-support 2-adic states, not finite integers",
            "finite truncations shadow but do not remain on the fixed orbit forever",
            "the actual period-two schedule is not constant t or constant u",
            "the result does not construct a Rule 30 finite-seed counterexample",
            "the result does not exclude eventual center period two",
            "the result does not prove Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
