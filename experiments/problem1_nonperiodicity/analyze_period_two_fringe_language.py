#!/usr/bin/env python3
"""Check exact local-language constraints on the period-two moving fringe.

Under a hypothetical alternating center trace, the even-time right fringe has
an autonomous two-step map. Its branch schedule uses ``u`` exactly when the
first two fringe cells are zero. This analyzer checks complete finite
light-cones for short schedule words and the local identity tying the schedule
to the cell two places left of center.

The accompanying informal note proves why a length-n schedule word depends on
only 2n initial fringe bits and derives the all-time forbidden-word and entropy
consequences. This bounded analyzer does not exclude the actual period-two
schedule and does not solve Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from typing import Any

DEFAULT_MAXIMUM_WORD_LENGTH = 10
ABSOLUTE_MAXIMUM_WORD_LENGTH = 10


class FringeLanguageLimitError(RuntimeError):
    """Raised before an explicitly capped complete light-cone is exceeded."""


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def rule30(left: int, center: int, right: int) -> int:
    """Return the Boolean Rule 30 local map."""

    if left not in (0, 1) or center not in (0, 1) or right not in (0, 1):
        raise ValueError("Rule 30 inputs must be binary")
    return left ^ (center | right)


def advance_fringe_packed(state: int) -> int:
    """Advance the infinite even-time right fringe by one two-step block.

    Bit j of ``state`` stores the cell at distance j+1 to the right of center.
    Missing high bits are zero. The center boundary over the two steps is 1,0.
    """

    if state < 0:
        raise ValueError("state must be nonnegative")
    row = 1 | (state << 1)
    odd_row = row ^ ((row >> 1) | (row >> 2))
    return (odd_row << 1) ^ (odd_row | (odd_row >> 1))


def advance_fringe_tuple(tail: tuple[int, ...]) -> tuple[int, ...]:
    """Independent tuple implementation of the same finite dependency cone."""

    if any(bit not in (0, 1) for bit in tail):
        raise ValueError("tail must be binary")
    radius = len(tail)
    row = (1,) + tail + (0, 0)
    odd = tuple(
        rule30(row[index], row[index + 1], row[index + 2])
        for index in range(radius + 1)
    )
    return tuple(
        rule30(
            0 if distance == 1 else odd[distance - 2],
            odd[distance - 1],
            odd[distance],
        )
        for distance in range(1, radius + 1)
    )


def branch_letter(state: int) -> str:
    """Return ``u`` exactly for a zero first fringe pair, else ``t``."""

    if state < 0:
        raise ValueError("state must be nonnegative")
    return "u" if state & 0b11 == 0 else "t"


def branch_word(state: int, length: int) -> str:
    """Generate ``length`` moving-fringe branch letters."""

    if length < 0:
        raise ValueError("length must be nonnegative")
    letters: list[str] = []
    for _ in range(length):
        letters.append(branch_letter(state))
        state = advance_fringe_packed(state)
    return "".join(letters)


def verify_self_trace_identity() -> dict[str, Any]:
    """Exhaust the local alternating-center equations around positions -2..2."""

    rows: list[dict[str, Any]] = []
    for left_two in (0, 1):
        for right_one in (0, 1):
            for right_two in (0, 1):
                left_one_odd = rule30(left_two, 1, 1)
                right_one_odd = rule30(1, right_one, right_two)
                next_center = rule30(left_one_odd, 0, right_one_odd)
                if next_center != 1:
                    continue
                schedule_is_u = right_one == 0 and right_two == 0
                if left_two != int(schedule_is_u):
                    raise AssertionError("schedule/self-trace identity failed")
                rows.append(
                    {
                        "x_minus_2_even": left_two,
                        "x_minus_1_even": 1,
                        "x_plus_1_even": right_one,
                        "x_plus_2_even": right_two,
                        "x_minus_1_odd": left_one_odd,
                        "x_plus_1_odd": right_one_odd,
                        "branch": "u" if schedule_is_u else "t",
                    }
                )

    if len(rows) != 4:
        raise AssertionError("expected one valid left-two value per right pair")
    return {
        "valid_local_assignments": rows,
        "exact_identity": "1[q_m=u] = x_-2(2m)",
        "adjacent_pair_trace": (
            "[-1,0] equals (1,1) at time 2m and "
            "(1-1[q_m=u],0) at time 2m+1"
        ),
        "all_checks_pass": True,
    }


def verify_packed_map(maximum_input_bits: int = 12) -> dict[str, Any]:
    """Cross-check packed and tuple forms over a complete finite state set."""

    if maximum_input_bits <= 0:
        raise ValueError("maximum_input_bits must be positive")
    checked = 0
    mask = (1 << maximum_input_bits) - 1
    for state in range(1 << maximum_input_bits):
        tail = tuple((state >> index) & 1 for index in range(maximum_input_bits))
        tuple_next = advance_fringe_tuple(tail)
        packed_next = advance_fringe_packed(state) & mask
        rebuilt = sum(bit << index for index, bit in enumerate(tuple_next))
        if packed_next != rebuilt:
            raise AssertionError("packed and tuple fringe maps disagree")
        checked += 1
    return {
        "input_bits": maximum_input_bits,
        "states_checked": checked,
        "all_checks_pass": True,
    }


def exact_trace_languages(maximum_length: int) -> dict[int, set[str]]:
    """Enumerate every schedule word through ``maximum_length`` exactly.

    The first n outputs depend only on the first 2n initial fringe bits. A
    single enumeration at the largest width therefore contains every shorter
    cylinder as a prefix.
    """

    if maximum_length <= 0:
        raise ValueError("maximum_length must be positive")
    width = 2 * maximum_length
    languages = {length: set() for length in range(1, maximum_length + 1)}
    for state in range(1 << width):
        word = branch_word(state, maximum_length)
        for length in languages:
            languages[length].add(word[:length])
    return languages


def _all_binary_words(length: int) -> set[str]:
    return {
        format(value, f"0{length}b").translate(str.maketrans({"0": "t", "1": "u"}))
        for value in range(1 << length)
    }


def verify_trace_language(maximum_length: int) -> dict[str, Any]:
    """Return complete short languages and all-scale forbidden words."""

    languages = exact_trace_languages(maximum_length)
    expected_counts = {1: 2, 2: 3, 3: 5, 4: 8, 5: 12, 6: 17, 7: 25, 8: 36, 9: 49, 10: 65}
    for length, expected in expected_counts.items():
        if length <= maximum_length and len(languages[length]) != expected:
            raise AssertionError(f"unexpected language count at length {length}")

    required_forbidden = {2: {"uu"}, 5: {"ttttt"}, 6: {"ututtu"}}
    for length, words in required_forbidden.items():
        if length > maximum_length:
            continue
        if words & languages[length]:
            raise AssertionError("required forbidden word was observed")

    if maximum_length >= 6:
        sft_words = {
            word
            for word in _all_binary_words(6)
            if "uu" not in word and "ttttt" not in word and "ututtu" not in word
        }
        if languages[6] != sft_words:
            raise AssertionError("length-six language is not the claimed SFT language")

    summaries = []
    for length in range(1, maximum_length + 1):
        missing = sorted(_all_binary_words(length) - languages[length])
        summaries.append(
            {
                "length": length,
                "dependency_bits": 2 * length,
                "realized_words": len(languages[length]),
                "total_words": 1 << length,
                "missing_words": len(missing),
                "language": sorted(languages[length]) if length <= 6 else None,
            }
        )

    return {
        "maximum_length": maximum_length,
        "largest_dependency_bits": 2 * maximum_length,
        "initial_fringe_states_checked": 1 << (2 * maximum_length),
        "levels": summaries,
        "all_scale_forbidden_words": ["uu", "ttttt", "ututtu"],
        "gap_consequence": (
            "successive u positions are separated by 2, 3, 4, or 5 blocks"
        ),
        "all_checks_pass": True,
    }


def dominant_root_cubic(iterations: int = 100) -> float:
    """Return the positive root of lambda^3-lambda^2-1 by bisection."""

    low, high = 1.0, 2.0
    for _ in range(iterations):
        middle = (low + high) / 2
        value = middle**3 - middle**2 - 1
        if value < 0:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def verify_sft_dimension_bound() -> dict[str, Any]:
    """Compute the exact length-six SFT entropy/dimension upper bound."""

    root = dominant_root_cubic()
    if abs(root**3 - root**2 - 1) > 1e-14:
        raise AssertionError("dominant-root calculation failed")
    dimension = math.log(root) / math.log(4)
    return {
        "forbidden_words": ["uu", "ttttt", "ututtu"],
        "adjacency_characteristic_factor": "lambda^3-lambda^2-1",
        "dominant_root": root,
        "topological_entropy_nats_per_branch": math.log(root),
        "survivor_2adic_dimension_upper_bound": dimension,
        "all_checks_pass": True,
    }


def run_campaign(
    *, maximum_word_length: int = DEFAULT_MAXIMUM_WORD_LENGTH
) -> dict[str, Any]:
    if maximum_word_length > ABSOLUTE_MAXIMUM_WORD_LENGTH:
        raise FringeLanguageLimitError(
            f"word length exceeds absolute maximum {ABSOLUTE_MAXIMUM_WORD_LENGTH}"
        )
    if maximum_word_length < 6:
        raise ValueError("maximum_word_length must be at least six")

    payload = {
        "self_trace_identity": verify_self_trace_identity(),
        "packed_map_crosscheck": verify_packed_map(),
        "trace_language": verify_trace_language(maximum_word_length),
        "sft_dimension_bound": verify_sft_dimension_bound(),
        "exact_conclusions": {
            "self_trace": (
                "under an alternating center, the branch-u indicator is exactly "
                "the even-time trace of cell -2"
            ),
            "bounded_gaps": (
                "every valid moving-fringe schedule avoids uu, ttttt, and ututtu; "
                "in particular u recurs with gaps between two and five"
            ),
            "dimension_bound": (
                "the corresponding survivor subset has 2-adic Hausdorff dimension "
                "at most log(lambda)/log(4), where lambda^3=lambda^2+1"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-fringe-language-v1\0")
    digest.update(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    )
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maximum-word-length",
        type=_positive_integer,
        default=DEFAULT_MAXIMUM_WORD_LENGTH,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(maximum_word_length=args.maximum_word_length)
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-fringe-language-v1",
        "question": "problem1",
        "hypothesis": (
            "The actual period-two moving-fringe schedule obeys exact, "
            "translation-invariant local language constraints that reduce the "
            "compatible zero-survivor set below the unrestricted Cantor coding."
        ),
        "backend": "python-exact-boolean-light-cones",
        "parameters": {
            "maximum_word_length": args.maximum_word_length,
            "absolute_maximum_word_length": ABSOLUTE_MAXIMUM_WORD_LENGTH,
        },
        "result_summary": result,
        "status": "finite-exhaustive",
        "proof_scope": (
            "The dependency-cone, self-trace, forbidden-word, aperiodicity, and "
            "dimension deductions are stated in "
            "proofs/informal/problem1_period_two_fringe_language.md. The script "
            "exhausts the finite Boolean cones used by those local deductions."
        ),
        "interpretation": (
            "The actual auxiliary schedule is a bounded-gap aperiodic point of a "
            "strict subshift, and its zero survivor lies in a 2-adic subset of "
            "dimension at most about 0.276. This is a structural restriction, not "
            "a finite-support exclusion."
        ),
        "limitations": [
            "the dimension bound does not exclude isolated ordinary integers",
            "short forbidden words do not determine the complete schedule language",
            "the bounded language campaign does not prove the survivor has infinite support",
            "the result does not exclude eventual center period two",
            "the result does not prove Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
