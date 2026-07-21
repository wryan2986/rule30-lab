#!/usr/bin/env python3
"""
Rule 30 prize-problem research harness.

Experiments:
1. Generate the center column from a single black cell.
2. Measure balance, autocorrelation, block frequencies, and linear complexity.
3. Search finite prefixes for candidate periods.
4. Test whether the sequence resembles a 2-automatic sequence via its 2-kernel.
5. Reconstruct the initial cells to the left from a proposed center trace
   using Rule 30's sideways (left-permutive) evolution.

This is an experimental tool, not a proof of any prize problem.
"""

from __future__ import annotations

import argparse
import math
from collections import Counter
from typing import Iterable, Sequence


def center_column(steps: int) -> bytearray:
    """Return center bits c[0..steps] for Rule 30 from a single 1.

    The integer encodes a full row. After t updates, the original center
    lies at bit position t.
    """
    if steps < 0:
        raise ValueError("steps must be nonnegative")

    row = 1
    out = bytearray(steps + 1)
    out[0] = 1

    for t in range(1, steps + 1):
        row ^= (row << 1) | (row << 2)
        out[t] = (row >> t) & 1

    return out


def balance_report(bits: Sequence[int], checkpoints: Iterable[int]) -> None:
    running_ones = 0
    requested = sorted(set(n for n in checkpoints if 0 < n <= len(bits)))
    target_index = 0

    for i, bit in enumerate(bits, start=1):
        running_ones += bit
        if target_index < len(requested) and i == requested[target_index]:
            n = i
            discrepancy = 2 * running_ones - n
            print(
                f"N={n:>9}  ones={running_ones:>9}  "
                f"ones/N={running_ones / n:.9f}  "
                f"D={discrepancy:>7}  D/sqrt(N)={discrepancy / math.sqrt(n): .4f}"
            )
            target_index += 1


def autocorrelation(bits: Sequence[int], lag: int) -> float:
    """Return mean of s[t]s[t+lag], with s=2*bit-1."""
    if lag <= 0 or lag >= len(bits):
        raise ValueError("lag must be between 1 and len(bits)-1")

    total = 0
    count = len(bits) - lag
    for i in range(count):
        total += (1 if bits[i] else -1) * (1 if bits[i + lag] else -1)
    return total / count


def block_counts(bits: Sequence[int], width: int) -> Counter[int]:
    if width <= 0 or width > len(bits):
        raise ValueError("invalid block width")

    mask = (1 << width) - 1
    value = 0
    for bit in bits[:width]:
        value = (value << 1) | bit

    counts: Counter[int] = Counter({value: 1})
    for bit in bits[width:]:
        value = ((value << 1) & mask) | bit
        counts[value] += 1

    # Include absent blocks explicitly.
    for value in range(1 << width):
        counts[value] += 0

    return counts


def berlekamp_massey_binary(bits: Sequence[int]) -> int:
    """Linear complexity of a binary sequence prefix over GF(2)."""
    n = len(bits)
    c = [0] * n
    b = [0] * n
    c[0] = b[0] = 1
    length = 0
    last_update = -1

    for index in range(n):
        discrepancy = bits[index]

        for j in range(1, length + 1):
            discrepancy ^= c[j] & bits[index - j]

        if discrepancy:
            old_c = c.copy()
            shift = index - last_update

            for j in range(n - shift):
                c[j + shift] ^= b[j]

            if length <= index // 2:
                length = index + 1 - length
                last_update = index
                b = old_c

    return length


def longest_matching_suffix_for_period(
    bits: Sequence[int],
    period: int,
) -> int:
    """Length of the final suffix satisfying c[t] == c[t-period]."""
    if period <= 0 or period >= len(bits):
        raise ValueError("invalid period")

    matched = 0

    for i in range(len(bits) - 1, period - 1, -1):
        if bits[i] != bits[i - period]:
            break

        matched += 1

    return matched


def two_kernel_distinct_prefixes(
    bits: Sequence[int],
    level: int,
    prefix_length: int,
) -> int:
    """Number of distinct prefixes among c[2^level*n+r]."""
    modulus = 1 << level
    subsequences = set()

    for residue in range(modulus):
        prefix = bytes(bits[residue::modulus][:prefix_length])
        subsequences.add(prefix)

    return len(subsequences)


def reconstruct_left_initial(center: Sequence[int]) -> list[int]:
    """Reconstruct initial cells x[-1,0], x[-2,0], ... from a center trace.

    Assumptions:
      * x[0,t] is the supplied center trace.
      * x[j,0] = 0 for all j > 0.

    Rule 30 is left-permutive:
        next_center = left XOR (center OR right)

    Hence:
        left = next_center XOR (center OR right)

    A genuine center trace from the single-cell seed must reconstruct an
    all-zero initial tail on the left.
    """
    horizon = len(center) - 1

    if horizon < 0:
        return []

    # right[t][j] for t=0..horizon and j=0..horizon+1
    right = [
        bytearray(horizon + 2)
        for _ in range(horizon + 1)
    ]

    for t, bit in enumerate(center):
        right[t][0] = bit

    # Evolve the forced right half, whose initial row is all zero for j > 0.
    for t in range(horizon):
        for j in range(1, horizon + 1):
            right[t + 1][j] = (
                right[t][j - 1]
                ^ (right[t][j] | right[t][j + 1])
            )

    current = bytearray(center)
    neighbor = bytearray(
        right[t][1]
        for t in range(horizon + 1)
    )

    initial_left: list[int] = []

    for depth in range(1, horizon + 1):
        length = horizon + 1 - depth
        new_column = bytearray(length)

        for t in range(length):
            new_column[t] = (
                current[t + 1]
                ^ (current[t] | neighbor[t])
            )

        initial_left.append(new_column[0])
        neighbor = current[:length]
        current = new_column

    return initial_left


def periodic_trace(word: str, length: int) -> bytearray:
    """Repeat a binary word until the requested trace length is reached."""
    if not word or any(ch not in "01" for ch in word):
        raise ValueError("period word must be a nonempty binary string")

    values = [int(ch) for ch in word]

    return bytearray(
        values[i % len(values)]
        for i in range(length)
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run exploratory tests on the Rule 30 center column."
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=100_000,
        help="number of Rule 30 updates to generate",
    )

    parser.add_argument(
        "--linear-prefix",
        type=int,
        default=5_000,
        help="prefix length used for Berlekamp-Massey analysis",
    )

    parser.add_argument(
        "--max-period",
        type=int,
        default=1_000,
        help="largest candidate period tested against the generated prefix",
    )

    parser.add_argument(
        "--test-periodic-trace",
        metavar="WORD",
        help="sideways-reconstruct a purely periodic center trace",
    )

    args = parser.parse_args()

    bits = center_column(args.steps)

    print("First 80 center bits:")
    print("".join(str(bit) for bit in bits[:80]))
    print()

    checkpoints = [
        10,
        100,
        1_000,
        10_000,
        100_000,
        1_000_000,
    ]

    print("Balance:")
    balance_report(bits, checkpoints)
    print()

    print("Autocorrelation:")

    for lag in (
        1,
        2,
        3,
        4,
        5,
        8,
        16,
        32,
        64,
        128,
    ):
        if lag < len(bits):
            print(
                f"lag={lag:>4}: "
                f"{autocorrelation(bits, lag): .7f}"
            )

    print()

    print("Block-frequency ranges:")

    for width in range(1, 9):
        if width > len(bits):
            break

        counts = block_counts(bits, width)
        values = list(counts.values())

        print(
            f"k={width}: "
            f"min={min(values)}, "
            f"max={max(values)}, "
            f"distinct={sum(value > 0 for value in values)}/{1 << width}"
        )

    print()

    prefix_length = min(
        args.linear_prefix,
        len(bits),
    )

    complexity = berlekamp_massey_binary(
        bits[:prefix_length]
    )

    print(
        f"Berlekamp-Massey linear complexity for "
        f"N={prefix_length}: {complexity}"
    )

    print()

    max_period = min(
        args.max_period,
        len(bits) - 1,
    )

    best = sorted(
        (
            (
                longest_matching_suffix_for_period(
                    bits,
                    period,
                ),
                period,
            )
            for period in range(1, max_period + 1)
        ),
        reverse=True,
    )[:10]

    print(
        f"Longest final matches among periods "
        f"1..{max_period}:"
    )

    for length, period in best:
        print(
            f"period={period:>6}, "
            f"matching suffix={length}"
        )

    print()

    print("2-kernel distinct-prefix test:")

    for level in range(1, 10):
        modulus = 1 << level

        if modulus * 64 > len(bits):
            break

        distinct = two_kernel_distinct_prefixes(
            bits,
            level,
            64,
        )

        print(
            f"level={level}: "
            f"{distinct}/{modulus} distinct"
        )

    print()

    # Sanity check:
    # The true trace must reconstruct the all-zero left initial tail.
    horizon = min(
        500,
        len(bits) - 1,
    )

    reconstructed = reconstruct_left_initial(
        bits[:horizon + 1]
    )

    print(
        f"True trace sideways reconstruction over "
        f"{horizon} cells: "
        f"{sum(reconstructed)} nonzero initial-left bits"
    )

    if args.test_periodic_trace:
        trace = periodic_trace(
            args.test_periodic_trace,
            horizon + 1,
        )

        reconstructed = reconstruct_left_initial(trace)

        first_one = next(
            (
                index + 1
                for index, bit in enumerate(reconstructed)
                if bit
            ),
            None,
        )

        print(
            f"Periodic trace "
            f"{args.test_periodic_trace!r}: "
            f"first reconstructed nonzero left cell = "
            f"{first_one}"
        )


if __name__ == "__main__":
    main()
