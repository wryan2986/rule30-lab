#!/usr/bin/env python3
"""Analyze the lossless renormalized high-front map for period-two returns.

For the packed two-step fringe map F, define H(x)=F(x)//4. Exact truncation
commutation gives

    F**B(s) >> (m+2B) = H**B(s >> m).

At a u-return A=4z followed by a return word of total span B, the final return
coordinate R therefore satisfies R >> (2B) = H**B(z). The map H is triangular
from high bits to low bits with diagonal one, so it is a permutation on every
fixed bit-length shell and has an explicit high-to-low inverse.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any

DEFAULT_MAX_BITS = 14
ABSOLUTE_MAX_BITS = 18
DEFAULT_SEMICONJUGACY_BITS = 11
DEFAULT_MAX_BLOCKS = 8
DEFAULT_RETURN_COUNT = 4


class RenormalizedFrontLimitError(RuntimeError):
    """Raised before a controlled exhaustive campaign exceeds its cap."""


def advance_fringe(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    row = 1 | (state << 1)
    odd = row ^ ((row >> 1) | (row >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def renormalized_front(value: int) -> int:
    if value < 0:
        raise ValueError("value must be nonnegative")
    return advance_fringe(value) >> 2


def renormalized_front_formula(value: int) -> int:
    if value < 0:
        raise ValueError("value must be nonnegative")
    result = 0
    for index in range(value.bit_length()):
        bit = lambda offset: (value >> (index + offset)) & 1
        odd0 = bit(0) ^ (bit(1) | bit(2))
        odd1 = bit(1) ^ (bit(2) | bit(3))
        odd2 = bit(2) ^ (bit(3) | bit(4))
        output = odd0 ^ (odd1 | odd2)
        result |= output << index
    return result


def inverse_renormalized_front(value: int) -> int:
    if value < 0:
        raise ValueError("value must be nonnegative")
    result = 0
    for index in range(value.bit_length() - 1, -1, -1):
        bit1 = (result >> (index + 1)) & 1
        bit2 = (result >> (index + 2)) & 1
        bit3 = (result >> (index + 3)) & 1
        bit4 = (result >> (index + 4)) & 1
        odd0_without_current = bit1 | bit2
        odd1 = bit1 ^ (bit2 | bit3)
        odd2 = bit2 ^ (bit3 | bit4)
        correction = odd0_without_current ^ (odd1 | odd2)
        source_bit = ((value >> index) & 1) ^ correction
        result |= source_bit << index
    return result


def iterate_front(value: int, blocks: int) -> int:
    if blocks < 0:
        raise ValueError("blocks must be nonnegative")
    for _ in range(blocks):
        value = renormalized_front(value)
    return value


def iterate_fringe(state: int, blocks: int) -> int:
    if blocks < 0:
        raise ValueError("blocks must be nonnegative")
    for _ in range(blocks):
        state = advance_fringe(state)
    return state


def first_return(z: int) -> tuple[int, int]:
    if z < 0:
        raise ValueError("z must be nonnegative")
    state = 4 * z
    for gap in range(1, 6):
        state = advance_fringe(state)
        if state & 3 == 0:
            if gap not in (2, 3, 4, 5):
                raise AssertionError("unexpected return gap")
            return gap, state >> 2
    raise AssertionError("five-block return bound failed")


def follow_returns(z: int, count: int) -> tuple[tuple[int, ...], int, int]:
    if count < 0:
        raise ValueError("count must be nonnegative")
    word: list[int] = []
    span = 0
    for _ in range(count):
        gap, z = first_return(z)
        word.append(gap)
        span += gap
    return tuple(word), span, z


def cycle_census(max_bits: int) -> tuple[list[dict[str, Any]], int]:
    if not 1 <= max_bits <= ABSOLUTE_MAX_BITS:
        raise RenormalizedFrontLimitError("max_bits outside controlled range")
    rows: list[dict[str, Any]] = []
    total_states = 0
    for bits in range(1, max_bits + 1):
        lower = 1 << (bits - 1)
        upper = 1 << bits
        seen = bytearray(upper - lower)
        counts: Counter[int] = Counter()
        for start in range(lower, upper):
            if seen[start - lower]:
                continue
            current = start
            length = 0
            while not seen[current - lower]:
                seen[current - lower] = 1
                current = renormalized_front(current)
                length += 1
            if current != start:
                raise AssertionError("shell permutation traversal merged cycles")
            counts[length] += 1
        if any(length & (length - 1) for length in counts):
            raise AssertionError("triangular permutation produced non-dyadic cycle")
        states = upper - lower
        total_states += states
        rows.append(
            {
                "bits": bits,
                "states": states,
                "cycle_counts": {str(k): counts[k] for k in sorted(counts)},
                "maximum_cycle_length": max(counts),
            }
        )
    return rows, total_states


def run_campaign(
    max_bits: int = DEFAULT_MAX_BITS,
    semiconjugacy_bits: int = DEFAULT_SEMICONJUGACY_BITS,
    max_blocks: int = DEFAULT_MAX_BLOCKS,
    return_count: int = DEFAULT_RETURN_COUNT,
) -> dict[str, Any]:
    if not 1 <= semiconjugacy_bits <= 16:
        raise RenormalizedFrontLimitError("semiconjugacy_bits outside controlled range")
    if not 0 <= max_blocks <= 16:
        raise RenormalizedFrontLimitError("max_blocks outside controlled range")
    if not 0 <= return_count <= 8:
        raise RenormalizedFrontLimitError("return_count outside controlled range")

    formula_checks = 0
    inverse_checks = 0
    shell_states = (1 << max_bits) - 1
    for value in range(1, 1 << max_bits):
        front = renormalized_front(value)
        if front != renormalized_front_formula(value):
            raise AssertionError("explicit bit formula mismatch")
        if front.bit_length() != value.bit_length():
            raise AssertionError("renormalized front changed bit length")
        if inverse_renormalized_front(front) != value:
            raise AssertionError("left inverse failed")
        if renormalized_front(inverse_renormalized_front(value)) != value:
            raise AssertionError("right inverse failed")
        formula_checks += 1
        inverse_checks += 2

    truncation_checks = 0
    semiconjugacy_checks = 0
    return_bridge_checks = 0
    for value in range(1, 1 << semiconjugacy_bits):
        for shift in range(0, semiconjugacy_bits + 1):
            left = advance_fringe(value) >> (shift + 2)
            right = renormalized_front(value >> shift)
            if left != right:
                raise AssertionError("one-block truncation commutation failed")
            truncation_checks += 1
        for blocks in range(max_blocks + 1):
            left = iterate_fringe(4 * value, blocks) >> (2 * blocks + 2)
            right = iterate_front(value, blocks)
            if left != right:
                raise AssertionError("iterated semiconjugacy failed")
            semiconjugacy_checks += 1
        word, span, final = follow_returns(value, return_count)
        if final >> (2 * span) != iterate_front(value, span):
            raise AssertionError("return-coordinate bridge failed")
        recovered = final >> (2 * span)
        for _ in range(span):
            recovered = inverse_renormalized_front(recovered)
        if recovered != value:
            raise AssertionError("return high front did not recover initial coordinate")
        replay_word, replay_span, replay_final = follow_returns(recovered, return_count)
        if (replay_word, replay_span, replay_final) != (word, span, final):
            raise AssertionError("recovered coordinate did not recover return history")
        return_bridge_checks += 1

    cycles, cycle_states = cycle_census(max_bits)
    payload: dict[str, Any] = {
        "status": "partial-proof",
        "theorem": {
            "renormalized_map": "H(x)=F(x)>>2",
            "bit_formula": (
                "H(x)_j=x_j xor ((x_(j+1) or x_(j+2)) xor "
                "((x_(j+1) xor (x_(j+2) or x_(j+3))) or "
                "(x_(j+2) xor (x_(j+3) or x_(j+4)))))"
            ),
            "triangularity": "output bit j is input bit j xor a function of higher bits only",
            "semiconjugacy": "F^B(s)>>(m+2B)=H^B(s>>m)",
            "return_bridge": "for a return word of span B, final R satisfies R>>2B=H^B(z)",
            "lossless_consequence": (
                "H is a shell permutation, so the aligned high front of the final "
                "return coordinate recovers the complete initial coordinate and return history"
            ),
            "cycle_consequence": "every finite-shell cycle length is a power of two",
        },
        "parameters": {
            "max_bits": max_bits,
            "semiconjugacy_bits": semiconjugacy_bits,
            "max_blocks": max_blocks,
            "return_count": return_count,
        },
        "validation": {
            "shell_states": shell_states,
            "formula_checks": formula_checks,
            "inverse_checks": inverse_checks,
            "truncation_checks": truncation_checks,
            "semiconjugacy_checks": semiconjugacy_checks,
            "return_bridge_checks": return_bridge_checks,
            "cycle_states": cycle_states,
        },
        "cycle_census": cycles,
        "scientific_boundary": (
            "The lossless high-front theorem identifies where finite-coordinate information "
            "moves. It does not constrain the unique infinite actual front enough to prove "
            "phase-witness divergence, exclude eventual center period two, or solve Rule 30 "
            "center nonperiodicity."
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-bits", type=int, default=DEFAULT_MAX_BITS)
    parser.add_argument("--semiconjugacy-bits", type=int, default=DEFAULT_SEMICONJUGACY_BITS)
    parser.add_argument("--max-blocks", type=int, default=DEFAULT_MAX_BLOCKS)
    parser.add_argument("--return-count", type=int, default=DEFAULT_RETURN_COUNT)
    args = parser.parse_args()
    print(
        json.dumps(
            run_campaign(
                max_bits=args.max_bits,
                semiconjugacy_bits=args.semiconjugacy_bits,
                max_blocks=args.max_blocks,
                return_count=args.return_count,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
