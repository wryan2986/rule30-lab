#!/usr/bin/env python3
"""Couple the period-two zero orbit to its exact future schedule.

For a future branch schedule q_m,q_(m+1),... with q in {t,u}, the inverse
zero-branch contractions determine a unique 2-adic normalized state X_m that
would emit zero forever while following exactly that schedule.  This analyzer
checks:

* the contraction and unique-survivor construction on finite quotients;
* an exact output-pair transducer for the binary digits of X_m;
* the mismatch law saying that a finite normalized state x_m has exactly
  floor(v_2(x_m-X_m)/2) consecutive zero blocks.

The finite campaign is regression evidence for the accompanying all-width
proof.  It does not prove that any X_m has infinite ordinary support and does
not solve Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any, Iterable

from rule30lab.two_adic import (
    inverse_diagonal_map_mod,
    minus_one_third_mod,
    right_edge_step_mod,
)


DEFAULT_ACTUAL_BLOCKS = 512
DEFAULT_SURVIVOR_WIDTH = 128
DEFAULT_PAIR_COUNT = 128
ABSOLUTE_ACTUAL_BLOCKS = 4_096
ABSOLUTE_SURVIVOR_WIDTH = 1_024
ABSOLUTE_PAIR_COUNT = 512
LETTERS = ("t", "p", "u")
_ROOT_FLIP = {"t": 0, "p": 1, "u": 1}
_SECTIONS = {
    "t": ("t", "p"),
    "p": ("p", "u"),
    "u": ("p", "t"),
}


class ScheduleSurvivorLimitError(RuntimeError):
    """Raised before an explicitly capped finite campaign is exceeded."""


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def forward_generator(name: str, state: int) -> int:
    """Apply the forward T, P, or U generator to a finite integer."""

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


def _inverse_t_mod(output: int, width: int) -> int:
    """Invert T exactly modulo 2**width by triangular low-to-high recovery."""

    if width < 0:
        raise ValueError("width must be nonnegative")
    if width == 0:
        return 0
    output &= (1 << width) - 1
    state = 0
    for position in range(width):
        previous_one = (state >> (position - 1)) & 1 if position >= 1 else 0
        previous_two = (state >> (position - 2)) & 1 if position >= 2 else 0
        bit = ((output >> position) & 1) ^ (previous_one | previous_two)
        state |= bit << position
    return state


def inverse_generator_mod(name: str, output: int, width: int) -> int:
    """Apply inverse letter t, p, or u exactly modulo 2**width."""

    if width < 0:
        raise ValueError("width must be nonnegative")
    if width == 0:
        return 0
    mask = (1 << width) - 1
    output &= mask
    if name == "t":
        return _inverse_t_mod(output, width)
    if name == "u":
        return _inverse_t_mod(output ^ 1, width)
    if name == "p":
        recovered_low_bit = (output & 1) ^ 1
        adjusted = output ^ 1 ^ (2 if recovered_low_bit == 0 else 0)
        return _inverse_t_mod(adjusted, width)
    raise ValueError(f"unknown inverse generator {name!r}")


def backward_zero_branch(q_name: str, successor: int, width: int) -> int:
    """Return B_q(successor) modulo 2**width.

    B_q(y) = 4 * p(q(y)) + 3, where lowercase letters are inverse tree maps.
    The map contracts 2-adic distance by exactly two valuation units.
    """

    if q_name not in ("t", "u"):
        raise ValueError("q_name must be 't' or 'u'")
    if width < 2:
        raise ValueError("width must be at least two")
    inner_width = width - 2
    state = inverse_generator_mod(q_name, successor, inner_width)
    state = inverse_generator_mod("p", state, inner_width)
    return ((state << 2) | 3) & ((1 << width) - 1)


def schedule_survivor_residue(q_names: Iterable[str], width: int) -> int:
    """Construct the unique schedule-survivor residue modulo 2**width."""

    if width < 2 or width % 2:
        raise ValueError("width must be a positive even integer")
    required = width // 2
    names = tuple(q_names)
    if len(names) < required:
        raise ValueError(f"at least {required} schedule branches are required")
    state = 0
    precision = 0
    for q_name in reversed(names[:required]):
        precision += 2
        state = backward_zero_branch(q_name, state, precision)
    return state


def valuation_mod_difference(left: int, right: int, width: int) -> int:
    """Return v_2(left-right), capped at width for equal residues."""

    difference = (left - right) & ((1 << width) - 1)
    if difference == 0:
        return width
    return (difference & -difference).bit_length() - 1


def inverse_word_root(word: tuple[str, ...], root: int) -> int:
    if root not in (0, 1):
        raise ValueError("root must be binary")
    return root ^ (sum(_ROOT_FLIP[name] for name in word) & 1)


def inverse_word_section(word: tuple[str, ...], root: int) -> tuple[str, ...]:
    if root not in (0, 1):
        raise ValueError("root must be binary")
    selected = [""] * len(word)
    current = root
    for index in range(len(word) - 1, -1, -1):
        name = word[index]
        selected[index] = _SECTIONS[name][current]
        current ^= _ROOT_FLIP[name]
    return tuple(selected)


def section_along(word: tuple[str, ...], path: tuple[int, ...]) -> tuple[str, ...]:
    for root in path:
        word = inverse_word_section(word, root)
    return word


def inverse_word_preimage_zero(word: tuple[str, ...]) -> int:
    state = 0
    for name in word:
        state = forward_generator(name, state)
    return state


def normalize_word(word: tuple[str, ...]) -> tuple[str, ...]:
    offset = next(
        (index for index, name in enumerate(word) if name != "t"),
        len(word),
    )
    return word[offset:]


def emitted_block(word: tuple[str, ...]) -> int:
    return (1 ^ inverse_word_root(word, 0)) + 2 * (
        1 ^ inverse_word_root(inverse_word_section(word, 1), 0)
    )


def block_update(word: tuple[str, ...], q_name: str) -> tuple[str, ...]:
    if q_name not in ("t", "u"):
        raise ValueError("q_name must be 't' or 'u'")
    return section_along(word, (1, 1)) + ("p", q_name)


def section_head_for_pair(pair: tuple[int, int]) -> str:
    if pair == (0, 0):
        return "T"
    if pair == (1, 0):
        return "U"
    if pair in ((0, 1), (1, 1)):
        return "P"
    raise ValueError("pair must be binary")


def advance_fringe(tail: tuple[int, ...]) -> tuple[int, ...]:
    if not tail or any(value not in (0, 1) for value in tail):
        raise ValueError("tail must be a nonempty binary tuple")
    radius = len(tail)
    row = (1,) + tail + (0, 0)
    first = tuple(
        row[index] ^ (row[index + 1] | row[index + 2])
        for index in range(radius + 1)
    )
    return tuple(
        (0 if distance == 1 else first[distance - 2])
        ^ (first[distance - 1] | first[distance])
        for distance in range(1, radius + 1)
    )


def fringe_schedule(maximum_block: int) -> tuple[list[str], list[str]]:
    """Return exact schedule heads and q letters through maximum_block."""

    if maximum_block < 0:
        raise ValueError("maximum_block must be nonnegative")
    tail = (0,) * (2 * maximum_block + 8)
    heads: list[str] = []
    q_names: list[str] = []
    for block in range(maximum_block + 1):
        head = section_head_for_pair((tail[1], tail[0]))
        heads.append(head)
        q_names.append("u" if head == "T" else "t")
        if block < maximum_block:
            tail = advance_fringe(tail)
    return heads, q_names


def word_action_on_11(word: tuple[str, ...]) -> tuple[tuple[int, int], tuple[str, ...]]:
    """Return word(11) and the section after the input prefix 11."""

    outputs: list[int] = []
    current = word
    for input_bit in (1, 1):
        outputs.append(inverse_word_root(current, input_bit))
        current = inverse_word_section(current, input_bit)
    return (outputs[0], outputs[1]), current


def survivor_output_pairs(
    q_names: Iterable[str], pair_count: int
) -> tuple[list[tuple[int, int]], list[int]]:
    """Generate low-to-high binary pairs of the schedule-survivor state.

    The first pair is literal 11. Thereafter a word state G outputs G(11),
    takes section G|_11, and appends the next inverse branch word p q.
    """

    if pair_count <= 0:
        raise ValueError("pair_count must be positive")
    names = tuple(q_names)
    if pair_count == 1:
        return [(1, 1)], [0]
    if len(names) < pair_count - 1:
        raise ValueError("not enough q names for requested output pairs")

    pairs = [(1, 1)]
    state = ("p", names[0])
    state_lengths = [0, len(state)]
    for pair_index in range(1, pair_count):
        output, section = word_action_on_11(state)
        pairs.append(output)
        if pair_index < pair_count - 1:
            state = section + ("p", names[pair_index])
            state_lengths.append(len(state))
    return pairs, state_lengths


def pairs_to_integer(pairs: Iterable[tuple[int, int]]) -> int:
    value = 0
    for pair_index, pair in enumerate(pairs):
        if pair[0] not in (0, 1) or pair[1] not in (0, 1):
            raise ValueError("pairs must be binary")
        value |= pair[0] << (2 * pair_index)
        value |= pair[1] << (2 * pair_index + 1)
    return value


def _consecutive_zero_blocks(blocks: list[int], start: int) -> int:
    length = 0
    while start + length < len(blocks) and blocks[start + length] == 0:
        length += 1
    return length


def verify_actual_mismatch_law(actual_blocks: int, survivor_width: int) -> dict[str, Any]:
    """Verify the exact streak/valuation law on the actual alternating path."""

    future_blocks = survivor_width // 2 + 2
    heads, q_names = fringe_schedule(actual_blocks + future_blocks)
    word: tuple[str, ...] = ()
    words: list[tuple[str, ...]] = []
    blocks: list[int] = []
    for block in range(actual_blocks + future_blocks + 1):
        words.append(word)
        blocks.append(emitted_block(word))
        if block < actual_blocks + future_blocks:
            word = block_update(word, q_names[block])

    valuation_counts: Counter[int] = Counter()
    streak_counts: Counter[int] = Counter()
    rows: list[dict[str, Any]] = []
    maximum_streak = 0
    maximum_valuation = 0
    for block in range(actual_blocks + 1):
        normalized = normalize_word(words[block])
        x_value = inverse_word_preimage_zero(normalized)
        survivor = schedule_survivor_residue(q_names[block:], survivor_width)
        valuation = valuation_mod_difference(x_value, survivor, survivor_width)
        streak = _consecutive_zero_blocks(blocks, block)
        if valuation == survivor_width:
            raise AssertionError(
                "finite campaign cannot certify equality to the 2-adic survivor"
            )
        if streak != valuation // 2:
            raise AssertionError("zero-streak valuation law failed")
        maximum_streak = max(maximum_streak, streak)
        maximum_valuation = max(maximum_valuation, valuation)
        valuation_counts[valuation] += 1
        streak_counts[streak] += 1
        if streak >= 2 or block in (0, 1, actual_blocks):
            rows.append(
                {
                    "block": block,
                    "emitted_block": blocks[block],
                    "schedule_head": heads[block],
                    "q_name": q_names[block],
                    "normalized_x_mod_16": x_value % 16,
                    "survivor_x_mod_16": survivor % 16,
                    "mismatch_valuation": valuation,
                    "consecutive_zero_blocks": streak,
                }
            )

    return {
        "actual_blocks_checked_inclusive": actual_blocks + 1,
        "survivor_width": survivor_width,
        "all_streak_valuation_checks_pass": True,
        "maximum_consecutive_zero_blocks": maximum_streak,
        "maximum_mismatch_valuation": maximum_valuation,
        "valuation_counts": {
            str(key): valuation_counts[key] for key in sorted(valuation_counts)
        },
        "streak_counts": {
            str(key): streak_counts[key] for key in sorted(streak_counts)
        },
        "selected_rows": rows,
    }


def verify_pair_transducer(pair_count: int) -> dict[str, Any]:
    """Cross-check the pair transducer against direct backward contraction."""

    _, q_names = fringe_schedule(pair_count + 4)
    pairs, state_lengths = survivor_output_pairs(q_names, pair_count)
    pair_value = pairs_to_integer(pairs)
    direct_value = schedule_survivor_residue(q_names, 2 * pair_count)
    if pair_value != direct_value:
        raise AssertionError("pair transducer and direct survivor disagree")

    longest_zero_pair_run = 0
    current_zero_pair_run = 0
    nonzero_pair_count = 0
    for pair in pairs:
        if pair == (0, 0):
            current_zero_pair_run += 1
            longest_zero_pair_run = max(longest_zero_pair_run, current_zero_pair_run)
        else:
            current_zero_pair_run = 0
            nonzero_pair_count += 1

    pair_bytes = "".join(f"{a}{b}" for a, b in pairs).encode("ascii")
    return {
        "pair_count": pair_count,
        "direct_backward_contraction_matches": True,
        "literal_first_pair": list(pairs[0]),
        "nonzero_pairs_observed": nonzero_pair_count,
        "longest_zero_pair_run_observed": longest_zero_pair_run,
        "first_32_pairs": [list(pair) for pair in pairs[:32]],
        "maximum_word_state_length": max(state_lengths),
        "pair_stream_sha256": hashlib.sha256(pair_bytes).hexdigest(),
        "finite_scope_warning": (
            "Observed nonzero high pairs do not prove that the survivor has "
            "infinite ordinary support."
        ),
    }


def verify_inverse_lift_identity(
    survivor_width: int, maximum_block: int = 32
) -> dict[str, Any]:
    """Identify schedule survivors with moving tails of the alternating lift."""

    if maximum_block < 0:
        raise ValueError("maximum_block must be nonnegative")
    total_width = survivor_width + 2 * maximum_block
    trace = minus_one_third_mod(total_width)
    seed = inverse_diagonal_map_mod(trace, total_width)
    _, q_names = fringe_schedule(maximum_block + survivor_width // 2 + 2)
    selected = sorted(
        value
        for value in {0, 1, 2, 3, 4, 8, 16, 32, maximum_block}
        if value <= maximum_block
    )
    selected_set = set(selected)
    mask = (1 << survivor_width) - 1
    row = seed
    checks: list[dict[str, Any]] = []
    for step in range(2 * maximum_block + 1):
        if step % 2 == 0:
            block = step // 2
            if block in selected_set:
                moving_tail = (row >> (2 * block)) & mask
                survivor = schedule_survivor_residue(q_names[block:], survivor_width)
                if moving_tail != survivor:
                    raise AssertionError(
                        "moving inverse-lift tail and schedule survivor disagree"
                    )
                checks.append(
                    {
                        "block": block,
                        "moving_tail_low_32": moving_tail & 0xFFFFFFFF,
                        "identity_holds": True,
                    }
                )
        if step < 2 * maximum_block:
            row = right_edge_step_mod(row, total_width)

    shift_zero = schedule_survivor_residue(q_names, survivor_width)
    if shift_zero != (seed & mask):
        raise AssertionError("shift-zero survivor is not the alternating inverse lift")
    return {
        "survivor_width": survivor_width,
        "maximum_block": maximum_block,
        "selected_moving_tail_checks": checks,
        "shift_zero_equals_inverse_diagonal_lift": True,
        "all_selected_moving_tail_identities_pass": True,
        "inverse_lift_residue_sha256": hashlib.sha256(
            (seed & mask).to_bytes((survivor_width + 7) // 8, "little")
        ).hexdigest(),
    }


def run_campaign(
    *,
    actual_blocks: int = DEFAULT_ACTUAL_BLOCKS,
    survivor_width: int = DEFAULT_SURVIVOR_WIDTH,
    pair_count: int = DEFAULT_PAIR_COUNT,
) -> dict[str, Any]:
    if actual_blocks > ABSOLUTE_ACTUAL_BLOCKS:
        raise ScheduleSurvivorLimitError(
            f"actual blocks exceed absolute maximum {ABSOLUTE_ACTUAL_BLOCKS}"
        )
    if survivor_width > ABSOLUTE_SURVIVOR_WIDTH:
        raise ScheduleSurvivorLimitError(
            "survivor width exceeds absolute maximum "
            f"{ABSOLUTE_SURVIVOR_WIDTH}"
        )
    if pair_count > ABSOLUTE_PAIR_COUNT:
        raise ScheduleSurvivorLimitError(
            f"pair count exceeds absolute maximum {ABSOLUTE_PAIR_COUNT}"
        )
    if survivor_width < 16 or survivor_width % 2:
        raise ValueError("survivor_width must be an even integer at least 16")

    mismatch = verify_actual_mismatch_law(actual_blocks, survivor_width)
    transducer = verify_pair_transducer(pair_count)
    inverse_lift = verify_inverse_lift_identity(survivor_width)
    payload = {
        "actual_mismatch_law": mismatch,
        "schedule_survivor_pair_transducer": transducer,
        "alternating_inverse_lift_identity": inverse_lift,
        "exact_reductions": {
            "unique_schedule_survivor": (
                "For every infinite q schedule there is a unique X_m in Z_2 "
                "with X_m=B_qm(X_m+1) that emits zero forever under that schedule."
            ),
            "mismatch_cocycle": (
                "Along every matched zero step, v_2(x_m-X_m) drops by exactly "
                "two; the current zero-streak length is floor(v_2/2)."
            ),
            "support_transducer": (
                "The low-to-high bit pairs of X_m are generated by G(11), "
                "G <- G|_11 p q; X_m is an ordinary integer iff those pairs "
                "are eventually 00."
            ),
            "inverse_lift_identity": (
                "For the actual moving-fringe schedule, X_0 is exactly the "
                "2-adic inverse diagonal lift of the alternating trace, and "
                "X_m is its time-2m moving tail above position 2m."
            ),
        },
    }
    certificate = hashlib.sha256()
    certificate.update(b"rule30-period-two-schedule-survivor-v1\0")
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
        description="Verify the period-two schedule-survivor mismatch cocycle."
    )
    parser.add_argument(
        "--actual-blocks", type=_positive_integer, default=DEFAULT_ACTUAL_BLOCKS
    )
    parser.add_argument(
        "--survivor-width",
        type=_positive_integer,
        default=DEFAULT_SURVIVOR_WIDTH,
    )
    parser.add_argument(
        "--pair-count", type=_positive_integer, default=DEFAULT_PAIR_COUNT
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(
        actual_blocks=args.actual_blocks,
        survivor_width=args.survivor_width,
        pair_count=args.pair_count,
    )
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-schedule-survivor-v1",
        "question": "problem1",
        "hypothesis": (
            "A unique future-schedule survivor and its 2-adic mismatch valuation "
            "give an exact support/schedule cocycle for period-two zero streaks."
        ),
        "backend": "python-exact-word-transducer-and-2adic-quotient",
        "parameters": {
            "actual_blocks": args.actual_blocks,
            "survivor_width": args.survivor_width,
            "pair_count": args.pair_count,
        },
        "result_summary": result,
        "status": "finite-exhaustive",
        "proof_scope": (
            "The all-width contraction, uniqueness, valuation, and pair-transducer "
            "identities are proved in the accompanying informal proof. The script "
            "checks only the stated finite quotients and actual path prefix."
        ),
        "interpretation": (
            "A hypothetical final zero tail at block m is equivalent to equality "
            "of the ordinary normalized state x_m with the unique 2-adic survivor "
            "X_m generated by the future moving-fringe schedule."
        ),
        "limitations": [
            "finite quotient agreement does not prove x_m differs from X_m in Z_2",
            "the observed pair stream does not prove infinitely many nonzero pairs",
            "the result does not exclude eventual center period two",
            "the result does not prove Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
