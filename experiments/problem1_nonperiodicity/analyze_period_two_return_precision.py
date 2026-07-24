#!/usr/bin/env python3
"""Classify exact 2-adic precision loss in the period-two first-return map.

At a ``u`` return write the packed fringe as ``A=4z`` and let
``(rho(z), R(z))`` be the next return gap and return coordinate. A gap-r
return is determined by ``k+2r`` low bits of z. Since r is at most five,
the complete lifted outcome ``(rho(z), R(z) mod 2**k)`` has exact worst-case
precision ``k+10`` for every ``k>=4``.

The all-width upper bound is a dependency-cone theorem. The analyzer checks
finite exhaustive levels and validates explicit lower-bound witnesses. It does
not determine the unique infinite actual orbit or exclude eventual period two.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any

MINIMUM_TARGET_BITS = 4
DEFAULT_MAXIMUM_EXHAUSTIVE_BITS = 8
ABSOLUTE_MAXIMUM_EXHAUSTIVE_BITS = 10
UNIFORM_WITNESS_START = 13
UNIFORM_WITNESS_BASE = 7
FINITE_WITNESS_BASES = {
    4: 203,
    5: 407,
    6: 16191,
    7: 23,
    8: 199,
    9: 415,
    10: 11,
    11: 7,
    12: 15,
}


class ReturnPrecisionLimitError(RuntimeError):
    """Raised before a controlled exhaustive campaign is exceeded."""


def advance_fringe(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    row = 1 | (state << 1)
    odd = row ^ ((row >> 1) | (row >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def rule30(left: int, center: int, right: int) -> int:
    return left ^ (center | right)


def interior_two_step_rule(window: tuple[int, int, int, int, int]) -> int:
    """Return one interior fringe bit after a two-step block."""
    a, b, c, d, e = window
    odd_left = rule30(a, b, c)
    odd_center = rule30(b, c, d)
    odd_right = rule30(c, d, e)
    return rule30(odd_left, odd_center, odd_right)


def isolated_impulse_support(steps: int) -> list[int]:
    """Evolve one isolated interior bit in an otherwise zero background."""
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    current = {0: 1}
    for _ in range(steps):
        low = min(current) - 2
        high = max(current) + 2
        current = {
            index: interior_two_step_rule(
                tuple(current.get(source, 0) for source in range(index - 2, index + 3))
            )
            for index in range(low, high + 1)
        }
    return sorted(index for index, value in current.items() if value)


def first_return(z: int) -> tuple[int, int]:
    if z < 0:
        raise ValueError("z must be nonnegative")
    state = 4 * z
    for gap in range(1, 6):
        state = advance_fringe(state)
        if state & 3 == 0:
            if gap < 2:
                raise AssertionError("the exact return language forbids gap one")
            return gap, state >> 2
    raise AssertionError("the exact return language bounds gaps by five")


def lifted_outcome(z: int, target_bits: int) -> tuple[int, int]:
    if target_bits <= 0:
        raise ValueError("target_bits must be positive")
    gap, successor = first_return(z)
    return gap, successor & ((1 << target_bits) - 1)


def source_bits_for_gap(target_bits: int, gap: int) -> int:
    if target_bits <= 0:
        raise ValueError("target_bits must be positive")
    if gap not in (2, 3, 4, 5):
        raise ValueError("gap must be 2, 3, 4, or 5")
    return target_bits + 2 * gap


def worst_case_source_bits(target_bits: int) -> int:
    if target_bits < MINIMUM_TARGET_BITS:
        raise ValueError("target_bits must be at least four")
    return target_bits + 10


def witness_base(target_bits: int) -> int:
    if target_bits in FINITE_WITNESS_BASES:
        return FINITE_WITNESS_BASES[target_bits]
    if target_bits >= UNIFORM_WITNESS_START:
        return UNIFORM_WITNESS_BASE
    raise ValueError("no witness is registered below four target bits")


def precision_witness(target_bits: int) -> dict[str, Any]:
    if target_bits < MINIMUM_TARGET_BITS:
        raise ValueError("target_bits must be at least four")
    base = witness_base(target_bits)
    insufficient_bits = target_bits + 9
    lifted = base + (1 << insufficient_bits)
    left = lifted_outcome(base, target_bits)
    right = lifted_outcome(lifted, target_bits)
    if left[0] != 5 or right[0] != 5:
        raise AssertionError("precision witnesses must stay in the gap-five cylinder")
    if left[1] ^ right[1] != 1 << (target_bits - 1):
        raise AssertionError("witness must flip exactly the top target bit")
    if base % (1 << insufficient_bits) != lifted % (1 << insufficient_bits):
        raise AssertionError("witness pair is not congruent at the claimed precision")
    return {
        "target_bits": target_bits,
        "insufficient_source_bits": insufficient_bits,
        "required_source_bits": target_bits + 10,
        "base_z": base,
        "lifted_z": lifted,
        "left_outcome": list(left),
        "right_outcome": list(right),
        "successor_xor": left[1] ^ right[1],
        "exact_difference": "the two successors differ first at target bit k-1",
    }


def exhaustive_level(target_bits: int) -> dict[str, Any]:
    required = worst_case_source_bits(target_bits)
    states = 1 << required
    gap_counts: Counter[int] = Counter()
    checksum = 0
    mask = (1 << target_bits) - 1
    for z in range(states):
        gap, successor = first_return(z)
        residue = successor & mask
        gap_counts[gap] += 1
        checksum = (
            checksum * 0x100000001B3 + gap * (1 << target_bits) + residue
        ) & ((1 << 64) - 1)
    witness = precision_witness(target_bits)
    return {
        "target_bits": target_bits,
        "required_source_bits": required,
        "states_exhausted": states,
        "gap_counts": {str(gap): gap_counts[gap] for gap in sorted(gap_counts)},
        "fnv_style_checksum_64": f"{checksum:016x}",
        "lower_bound_witness": witness,
    }


def verify_uniform_family(maximum_target_bits: int = 32) -> dict[str, Any]:
    if maximum_target_bits < UNIFORM_WITNESS_START:
        raise ValueError("uniform-family maximum must be at least thirteen")
    rows = [
        precision_witness(bits)
        for bits in range(UNIFORM_WITNESS_START, maximum_target_bits + 1)
    ]
    support = isolated_impulse_support(5)
    expected = [-10, -9, -6, -1, 1, 2, 3, 4, 6, 7, 10]
    if support != expected:
        raise AssertionError("unexpected five-block isolated-impulse support")
    return {
        "first_target_bits": UNIFORM_WITNESS_START,
        "last_target_bits_checked": maximum_target_bits,
        "base_z": UNIFORM_WITNESS_BASE,
        "lift_rule": "z'=7+2^(k+9)",
        "five_block_impulse_support": support,
        "lowest_impulse_displacement": -10,
        "checked_rows": len(rows),
        "all_checks_pass": True,
    }


def run_campaign(
    maximum_exhaustive_bits: int = DEFAULT_MAXIMUM_EXHAUSTIVE_BITS,
) -> dict[str, Any]:
    if maximum_exhaustive_bits > ABSOLUTE_MAXIMUM_EXHAUSTIVE_BITS:
        raise ReturnPrecisionLimitError(
            f"maximum exhaustive target bits exceeds {ABSOLUTE_MAXIMUM_EXHAUSTIVE_BITS}"
        )
    if maximum_exhaustive_bits < MINIMUM_TARGET_BITS:
        raise ValueError("maximum exhaustive target bits must be at least four")
    payload: dict[str, Any] = {
        "status": "partial-proof",
        "exact_theorem": (
            "for every k>=4, the lifted outcome (rho(z),R(z) mod 2^k) is "
            "determined by z mod 2^(k+10), and no modulus 2^(k+9) suffices"
        ),
        "gap_conditioned_precision": (
            "a gap-r return is determined by k+2r source bits"
        ),
        "levels": [
            exhaustive_level(bits)
            for bits in range(MINIMUM_TARGET_BITS, maximum_exhaustive_bits + 1)
        ],
        "finite_witnesses": [precision_witness(bits) for bits in range(4, 13)],
        "uniform_witness_family": verify_uniform_family(),
        "iterated_consequence": (
            "along fixed gaps r_0,...,r_(j-1), k output bits are determined by "
            "k+2*sum(r_i) initial coordinate bits; worst-case fresh precision is 10 per return"
        ),
        "scientific_boundary": (
            "the theorem rules out a deterministic fixed-width suffix automaton for the full "
            "return map but does not determine or exclude the unique zero-initialized orbit"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maximum-exhaustive-bits",
        type=int,
        default=DEFAULT_MAXIMUM_EXHAUSTIVE_BITS,
    )
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_exhaustive_bits), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
