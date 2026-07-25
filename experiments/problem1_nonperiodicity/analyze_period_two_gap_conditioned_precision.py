#!/usr/bin/env python3
"""Classify exact precision loss conditioned on one first-return gap.

At a ``u`` return write the packed fringe state as ``A=4z``. For a fixed
return gap ``r`` and target width ``k``, the successor coordinate modulo
``2**k`` is determined by ``z mod 2**(k+2*r)``. This analyzer proves that the
bound is exact for every ``r in {2,3,4,5}`` and every ``k>=5`` by exhaustive
finite quotients and explicit all-width witness families.

The theorem concerns all compatible return coordinates. It does not determine
the unique actual zero-initialized orbit or exclude eventual center period two.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any

RETURN_GAPS = (2, 3, 4, 5)
MINIMUM_TARGET_BITS = 5
DEFAULT_MAXIMUM_EXHAUSTIVE_BITS = 8
ABSOLUTE_MAXIMUM_EXHAUSTIVE_BITS = 10
UNIFORM_CHECK_MAXIMUM_BITS = 40

FINITE_WITNESS_BASES: dict[int, dict[int, int]] = {
    2: {5: 100, 6: 12},
    3: {5: 25, 6: 3},
    4: {5: 6},
    5: {
        5: 407,
        6: 16191,
        7: 23,
        8: 199,
        9: 415,
        10: 11,
        11: 7,
        12: 15,
    },
}
UNIFORM_FAMILIES = {
    2: {"start_k": 7, "base_z": 4},
    3: {"start_k": 7, "base_z": 1},
    4: {"start_k": 6, "base_z": 0},
    5: {"start_k": 13, "base_z": 7},
}
STABLE_RESPONSE_SUPPORTS = {
    2: (-4, -3, 0, 4),
    3: (-6, -5, -2, 3, 6),
    4: (-8, -7, -4, 0, 1, 2, 8),
    5: (-10, -9, -6, -1, 1, 2, 3, 4, 6, 7, 10),
}


class GapConditionedPrecisionLimitError(RuntimeError):
    """Raised before a controlled exhaustive campaign exceeds its cap."""


def advance_fringe(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    row = 1 | (state << 1)
    odd = row ^ ((row >> 1) | (row >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def first_return(z: int) -> tuple[int, int]:
    if z < 0:
        raise ValueError("z must be nonnegative")
    state = 4 * z
    for gap in range(1, 6):
        state = advance_fringe(state)
        if state & 3 == 0:
            if gap not in RETURN_GAPS:
                raise AssertionError("unexpected return gap")
            return gap, state >> 2
    raise AssertionError("five-block return bound failed")


def required_source_bits(target_bits: int, gap: int) -> int:
    if target_bits < MINIMUM_TARGET_BITS:
        raise ValueError("target_bits must be at least five")
    if gap not in RETURN_GAPS:
        raise ValueError("gap must be 2, 3, 4, or 5")
    return target_bits + 2 * gap


def witness_base(gap: int, target_bits: int) -> int:
    finite = FINITE_WITNESS_BASES[gap]
    if target_bits in finite:
        return finite[target_bits]
    family = UNIFORM_FAMILIES[gap]
    if target_bits >= family["start_k"]:
        return family["base_z"]
    raise ValueError("no witness registered for this gap and target width")


def precision_witness(gap: int, target_bits: int) -> dict[str, Any]:
    source_bits = required_source_bits(target_bits, gap)
    base = witness_base(gap, target_bits)
    lifted = base + (1 << (source_bits - 1))
    left_gap, left_successor = first_return(base)
    right_gap, right_successor = first_return(lifted)
    mask = (1 << target_bits) - 1
    left_residue = left_successor & mask
    right_residue = right_successor & mask
    difference = left_residue ^ right_residue
    if left_gap != gap or right_gap != gap:
        raise AssertionError("witness left the conditioned return cylinder")
    if difference != 1 << (target_bits - 1):
        raise AssertionError("witness did not flip exactly the top target bit")
    if base % (1 << (source_bits - 1)) != lifted % (1 << (source_bits - 1)):
        raise AssertionError("witnesses are not congruent at the insufficient precision")
    return {
        "gap": gap,
        "target_bits": target_bits,
        "insufficient_source_bits": source_bits - 1,
        "required_source_bits": source_bits,
        "base_z": base,
        "lifted_z": lifted,
        "left_successor_residue": left_residue,
        "right_successor_residue": right_residue,
        "successor_xor": difference,
    }


def conditioned_level(gap: int, target_bits: int) -> dict[str, Any]:
    source_bits = required_source_bits(target_bits, gap)
    mask = (1 << target_bits) - 1
    states = 1 << source_bits
    conditioned_count = 0
    output_counts: Counter[int] = Counter()
    checksum = 0
    for z in range(states):
        observed_gap, successor = first_return(z)
        if observed_gap != gap:
            continue
        residue = successor & mask
        conditioned_count += 1
        output_counts[residue] += 1
        checksum = (checksum * 0x100000001B3 + residue) & ((1 << 64) - 1)
    witness = precision_witness(gap, target_bits)
    return {
        "gap": gap,
        "target_bits": target_bits,
        "required_source_bits": source_bits,
        "states_exhausted": states,
        "conditioned_states": conditioned_count,
        "distinct_successor_residues": len(output_counts),
        "checksum_hex": f"0x{checksum:016x}",
        "insufficiency_witness": witness,
        "exact_precision": True,
    }


def response_support(gap: int, source_index: int) -> list[int]:
    family = UNIFORM_FAMILIES[gap]
    base = family["base_z"]
    left_gap, left = first_return(base)
    right_gap, right = first_return(base + (1 << source_index))
    if left_gap != gap or right_gap != gap:
        raise AssertionError("response-support probe left its gap cylinder")
    difference = left ^ right
    return [
        index - source_index
        for index in range(difference.bit_length())
        if (difference >> index) & 1
    ]


def verify_uniform_families(maximum_target_bits: int) -> dict[str, Any]:
    rows = []
    for gap in RETURN_GAPS:
        family = UNIFORM_FAMILIES[gap]
        checked = 0
        for target_bits in range(family["start_k"], maximum_target_bits + 1):
            precision_witness(gap, target_bits)
            checked += 1
        stable_source_index = max(30, family["start_k"] + 2 * gap - 1)
        support = response_support(gap, stable_source_index)
        if tuple(support) != STABLE_RESPONSE_SUPPORTS[gap]:
            raise AssertionError("unexpected stable isolated-response support")
        if support[0] != -2 * gap:
            raise AssertionError("extreme left response displacement is missing")
        rows.append(
            {
                "gap": gap,
                "start_target_bits": family["start_k"],
                "base_z": family["base_z"],
                "target_widths_checked": checked,
                "stable_response_support": support,
            }
        )
    return {
        "maximum_target_bits_checked": maximum_target_bits,
        "families": rows,
        "all_checks_pass": True,
    }


def run_campaign(
    maximum_exhaustive_bits: int = DEFAULT_MAXIMUM_EXHAUSTIVE_BITS,
) -> dict[str, Any]:
    if not MINIMUM_TARGET_BITS <= maximum_exhaustive_bits <= ABSOLUTE_MAXIMUM_EXHAUSTIVE_BITS:
        raise GapConditionedPrecisionLimitError("exhaustive target width outside controlled range")
    levels = []
    total_states = 0
    for gap in RETURN_GAPS:
        for target_bits in range(MINIMUM_TARGET_BITS, maximum_exhaustive_bits + 1):
            row = conditioned_level(gap, target_bits)
            levels.append(row)
            total_states += row["states_exhausted"]
    payload: dict[str, Any] = {
        "status": "partial-proof",
        "parameters": {
            "minimum_target_bits": MINIMUM_TARGET_BITS,
            "maximum_exhaustive_bits": maximum_exhaustive_bits,
            "return_gaps": list(RETURN_GAPS),
        },
        "exact_theorem": (
            "for every r in {2,3,4,5} and k>=5, conditioned gap-r successor "
            "precision is exactly k+2r source bits"
        ),
        "levels": levels,
        "total_states_exhausted": total_states,
        "uniform_families": verify_uniform_families(UNIFORM_CHECK_MAXIMUM_BITS),
        "scientific_boundary": (
            "the theorem ranges over every compatible return coordinate; it does "
            "not determine the unique actual orbit or exclude eventual period two"
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
