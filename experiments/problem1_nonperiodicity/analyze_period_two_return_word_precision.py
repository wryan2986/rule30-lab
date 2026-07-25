#!/usr/bin/env python3
"""Classify eventual exact precision conditioned on a finite return word.

At a ``u`` return write the packed fringe as ``A=4z``.  If a realized
return-gap word has total block span ``B``, then its final return coordinate
modulo ``2**k`` is determined by ``z mod 2**(k+2*B)``.  For every
``k >= 4*B+5`` this upper bound is exact on that return-word cylinder.

The lower witness uses the least nonnegative cylinder representative below
``2**(2*B)`` and one isolated bit at coordinate ``k+2*B-1``.  The separation
bound keeps the high perturbation disjoint from the complete low spacetime
cone, so its leftmost response flips exactly final coordinate bit ``k-1``.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any

DEFAULT_SPAN_CAP = 8
ABSOLUTE_SPAN_CAP = 10
WITNESS_WIDTH_SAMPLES = 5


class ReturnWordPrecisionLimitError(RuntimeError):
    """Raised before a controlled cylinder census exceeds its cap."""


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
            if gap not in (2, 3, 4, 5):
                raise AssertionError("unexpected return gap")
            return gap, state >> 2
    raise AssertionError("five-block return bound failed")


def follow_returns(z: int, count: int) -> tuple[tuple[int, ...], int]:
    if count < 0:
        raise ValueError("count must be nonnegative")
    word: list[int] = []
    for _ in range(count):
        gap, z = first_return(z)
        word.append(gap)
    return tuple(word), z


def enumerate_return_words(span_cap: int) -> dict[tuple[int, ...], int]:
    if not 1 <= span_cap <= ABSOLUTE_SPAN_CAP:
        raise ReturnWordPrecisionLimitError("span cap outside controlled range")
    representatives: dict[tuple[int, ...], int] = {}
    for start in range(1 << (2 * span_cap)):
        z = start
        word: list[int] = []
        span = 0
        while True:
            gap, successor = first_return(z)
            if span + gap > span_cap:
                break
            span += gap
            word.append(gap)
            key = tuple(word)
            previous = representatives.get(key)
            if previous is None or start < previous:
                representatives[key] = start
            z = successor
    return representatives


def required_source_bits(target_bits: int, total_span: int) -> int:
    if target_bits <= 0:
        raise ValueError("target_bits must be positive")
    if total_span <= 0:
        raise ValueError("total_span must be positive")
    return target_bits + 2 * total_span


def universal_threshold(total_span: int) -> int:
    if total_span <= 0:
        raise ValueError("total_span must be positive")
    return 4 * total_span + 5


def precision_witness(
    word: tuple[int, ...], representative: int, target_bits: int
) -> dict[str, Any]:
    if not word:
        raise ValueError("return word must be nonempty")
    total_span = sum(word)
    if representative < 0 or representative >= 1 << (2 * total_span):
        raise ValueError("representative must lie in the canonical low cylinder")
    threshold = universal_threshold(total_span)
    if target_bits < threshold:
        raise ValueError("target width is below the proved separation threshold")

    observed, left_successor = follow_returns(representative, len(word))
    if observed != word:
        raise AssertionError("representative does not realize the return word")

    source_bit = target_bits + 2 * total_span - 1
    lifted = representative + (1 << source_bit)
    lifted_word, right_successor = follow_returns(lifted, len(word))
    if lifted_word != word:
        raise AssertionError("high isolated bit changed the conditioned return word")

    mask = (1 << target_bits) - 1
    left_residue = left_successor & mask
    right_residue = right_successor & mask
    difference = left_residue ^ right_residue
    expected = 1 << (target_bits - 1)
    if difference != expected:
        raise AssertionError("isolated high bit did not flip exactly the top target bit")

    return {
        "return_word": list(word),
        "total_span": total_span,
        "canonical_representative": representative,
        "target_bits": target_bits,
        "required_source_bits": required_source_bits(target_bits, total_span),
        "insufficient_source_bits": target_bits + 2 * total_span - 1,
        "lifted_coordinate": lifted,
        "left_successor_mod_2k": left_residue,
        "right_successor_mod_2k": right_residue,
        "successor_xor": difference,
        "return_word_preserved": True,
    }


def analyze_span(span_cap: int) -> dict[str, Any]:
    representatives = enumerate_return_words(span_cap)
    rows: list[dict[str, Any]] = []
    span_counts: Counter[int] = Counter()
    length_counts: Counter[int] = Counter()
    checks = 0

    for word in sorted(representatives, key=lambda item: (sum(item), len(item), item)):
        representative = representatives[word]
        total_span = sum(word)
        if representative >= 1 << (2 * total_span):
            raise AssertionError("cylinder representative exceeds dependency modulus")
        observed, _ = follow_returns(representative, len(word))
        if observed != word:
            raise AssertionError("canonical representative replay failed")

        threshold = universal_threshold(total_span)
        samples = [
            precision_witness(word, representative, threshold + offset)
            for offset in range(WITNESS_WIDTH_SAMPLES)
        ]
        checks += len(samples)
        span_counts[total_span] += 1
        length_counts[len(word)] += 1
        rows.append(
            {
                "return_word": list(word),
                "return_count": len(word),
                "total_span": total_span,
                "canonical_representative": representative,
                "representative_bits": representative.bit_length(),
                "universal_threshold": threshold,
                "exact_precision": "k+2B",
                "sample_successor_xors": [sample["successor_xor"] for sample in samples],
            }
        )

    return {
        "span_cap": span_cap,
        "source_coordinates_exhausted": 1 << (2 * span_cap),
        "realized_return_words": len(rows),
        "word_counts_by_total_span": {
            str(span): span_counts[span] for span in sorted(span_counts)
        },
        "word_counts_by_return_count": {
            str(length): length_counts[length] for length in sorted(length_counts)
        },
        "witness_widths_per_word": WITNESS_WIDTH_SAMPLES,
        "witness_checks": checks,
        "rows": rows,
        "all_checks_pass": True,
    }


def run_campaign(span_cap: int = DEFAULT_SPAN_CAP) -> dict[str, Any]:
    census = analyze_span(span_cap)
    payload: dict[str, Any] = {
        "status": "partial-proof",
        "theorem": {
            "condition": "a realized finite return-gap word with total span B",
            "sufficiency": "k final coordinate bits depend on at most k+2B source bits",
            "necessity_range": "for every k >= 4B+5, k+2B source bits are necessary",
            "witness": (
                "choose the canonical representative c<2^(2B) and compare c with "
                "c+2^(k+2B-1); both realize the same return word and their final "
                "coordinates differ modulo 2^k exactly in bit k-1"
            ),
            "consequence": (
                "conditioning on the complete finite return word does not reduce "
                "the eventual exact precision loss of two bits per fringe block"
            ),
        },
        "census": census,
        "scientific_boundary": (
            "the theorem applies to every finite realized return word but does not "
            "control the unique infinite zero-initialized orbit, prove phase-witness "
            "complexity divergence, exclude eventual center period two, or solve "
            "Rule 30 center nonperiodicity"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--span-cap", type=int, default=DEFAULT_SPAN_CAP)
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.span_cap), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
