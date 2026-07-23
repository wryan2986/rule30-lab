#!/usr/bin/env python3
"""Analyze the exact coupled moving strip for the period-two inverse lift.

The alternating inverse lift, its autonomous right fringe, and its survivor
state are three descriptions of one moving Rule 30 row.  This module verifies
that exact moving-cut identity, gives a local width-growing transfer system for
the reversed inverse word and fringe, and classifies the first coupled
nearest-neighbor additive cocycle ansatz over the rationals.

The cocycle classification is a no-go theorem for a specific linear finite-
memory strategy.  It does not exclude nonlinear or growing-memory invariants,
does not exclude period two, and does not solve Rule 30 center
nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from rule30lab.two_adic import (
    inverse_diagonal_map_mod,
    minus_one_third_mod,
    right_edge_step_mod,
)

DEFAULT_MAXIMUM_BLOCK = 64
DEFAULT_TOTAL_WIDTH = 256
DEFAULT_WORD_EXHAUSTION_LENGTH = 5
ABSOLUTE_MAXIMUM_BLOCK = 256
ABSOLUTE_TOTAL_WIDTH = 1_024
ABSOLUTE_WORD_EXHAUSTION_LENGTH = 7
LETTERS = ("t", "p", "u")
PAIR_STATES = ((0, 0), (0, 1), (1, 0), (1, 1))


class CoupledStripLimitError(RuntimeError):
    """Raised before an explicitly capped exact campaign is exceeded."""


def _positive_integer(text: str) -> int:
    value = int(text)
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def _load_sibling(filename: str, module_name: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


FRINGE = _load_sibling(
    "analyze_period_two_fringe_language.py", "period_two_fringe_language"
)
SURVIVOR = _load_sibling(
    "analyze_period_two_schedule_survivor.py", "period_two_schedule_survivor"
)
GLOBAL = _load_sibling(
    "analyze_period_two_global_transducer.py", "period_two_global_transducer"
)


def reverse_bits(value: int, width: int) -> int:
    """Reverse exactly ``width`` low bits of a nonnegative integer."""

    if value < 0 or width < 0 or value >= (1 << width):
        raise ValueError("value must fit the requested nonnegative width")
    result = 0
    for index in range(width):
        result |= ((value >> index) & 1) << (width - 1 - index)
    return result


def right_edge_step_unbounded(state: int) -> int:
    """Apply the exact ordinary-integer right-edge map."""

    if state < 0:
        raise ValueError("state must be nonnegative")
    return state ^ ((state << 1) | (state << 2))


def iterate_right_edge_unbounded(state: int, steps: int) -> int:
    if state < 0 or steps < 0:
        raise ValueError("state and steps must be nonnegative")
    for _ in range(steps):
        state = right_edge_step_unbounded(state)
    return state


def scan_reversed_word(
    reversed_word: tuple[str, ...],
    start_pair: tuple[int, int] = (1, 1),
) -> tuple[tuple[str, ...], tuple[int, int]]:
    """Scan the inverse word in low-to-high order.

    ``reversed_word`` is the reversal of the established outer-to-inner word.
    The whole-word transducer therefore scans it from left to right.
    """

    if start_pair not in PAIR_STATES:
        raise ValueError("start_pair must be binary")
    output: list[str] = []
    state = start_pair
    for letter in reversed_word:
        emitted, state = GLOBAL.letter_transition(letter, state)
        output.append(emitted)
    return tuple(output), state


def coupled_strip_step(
    fringe_state: int, reversed_word: tuple[str, ...]
) -> tuple[int, tuple[str, ...], tuple[int, int], str]:
    """Advance one exact width-growing coupled strip row.

    The fringe grows by two outer cells.  The reversed inverse word grows by
    inserting ``q,p`` at its inner boundary and transducing its complete old
    row.  The terminal scan pair is the next reconstructed spatial pair.
    """

    if fringe_state < 0:
        raise ValueError("fringe_state must be nonnegative")
    q_name = FRINGE.branch_letter(fringe_state)
    output, terminal = scan_reversed_word(reversed_word)
    next_word = (q_name, "p") + output
    next_fringe = FRINGE.advance_fringe_packed(fringe_state)
    return next_fringe, next_word, terminal, q_name


def verify_coupled_transfer(maximum_word_length: int) -> dict[str, Any]:
    """Cross-check the local coupled strip against both existing rows."""

    cases = 0
    for length in range(maximum_word_length + 1):
        for reversed_word in itertools.product(LETTERS, repeat=length):
            original_word = tuple(reversed(reversed_word))
            for low_four_bits in range(16):
                next_fringe, next_reversed, terminal, q_name = coupled_strip_step(
                    low_four_bits, reversed_word
                )
                direct_word = SURVIVOR.block_update(original_word, q_name)
                if next_reversed != tuple(reversed(direct_word)):
                    raise AssertionError("reversed-word transfer mismatch")
                if terminal != GLOBAL.word_action_on_pair(original_word, (1, 1)):
                    raise AssertionError("terminal output-pair mismatch")
                direct_fringe = FRINGE.advance_fringe_tuple(
                    tuple((low_four_bits >> bit) & 1 for bit in range(4))
                )
                packed_low_four = tuple(
                    (next_fringe >> bit) & 1 for bit in range(4)
                )
                if packed_low_four != direct_fringe:
                    raise AssertionError("packed/tuple fringe transfer mismatch")
                cases += 1
    return {
        "maximum_word_length": maximum_word_length,
        "coupled_cases_checked": cases,
        "exact_word_update": "reverse(G_(m+1)) = q_m p scan_11(reverse(G_m))",
        "exact_fringe_update": "A_(m+1) is the autonomous two-step Rule 30 fringe map",
        "right_boundary_output": "terminal scan state equals G_m(11)",
        "all_checks_pass": True,
    }


def _schedule(maximum_block: int) -> tuple[list[int], list[str]]:
    fringe_states: list[int] = []
    q_names: list[str] = []
    state = 0
    for block in range(maximum_block + 1):
        fringe_states.append(state)
        q_names.append(FRINGE.branch_letter(state))
        if block < maximum_block:
            state = FRINGE.advance_fringe_packed(state)
    return fringe_states, q_names


def verify_moving_cut_identity(
    maximum_block: int, total_width: int
) -> dict[str, Any]:
    """Verify the exact low-fringe/high-survivor cut by independent routes."""

    if total_width <= 2 * maximum_block + 8:
        raise ValueError("total_width must leave at least eight survivor bits")
    if total_width % 2:
        raise ValueError("total_width must be even")

    future_needed = total_width // 2 + maximum_block + 2
    fringe_states, q_names = _schedule(future_needed)
    trace = minus_one_third_mod(total_width)
    seed = inverse_diagonal_map_mod(trace, total_width)
    row = seed
    word: tuple[str, ...] = ()
    selected_blocks = sorted(
        value
        for value in {0, 1, 2, 3, 4, 8, 16, 32, 64, maximum_block}
        if value <= maximum_block
    )
    selected_set = set(selected_blocks)
    rows: list[dict[str, Any]] = []
    checks = 0

    for block in range(maximum_block + 1):
        seam = 2 * block
        low_mask = (1 << seam) - 1 if seam else 0
        fringe_state = fringe_states[block]
        reversed_fringe = reverse_bits(fringe_state, seam) if seam else 0
        if row & low_mask != reversed_fringe:
            raise AssertionError("moving row low half is not the reversed fringe")

        high_width = total_width - seam
        survivor_from_row = row >> seam
        survivor_from_schedule = SURVIVOR.schedule_survivor_residue(
            q_names[block:], high_width
        )
        if survivor_from_row != survivor_from_schedule:
            raise AssertionError("moving row high half is not the schedule survivor")

        truncated_seed = seed & low_mask
        truncated_row = iterate_right_edge_unbounded(truncated_seed, seam)
        if truncated_row & low_mask != reversed_fringe:
            raise AssertionError("truncated row does not preserve the exact fringe")
        ordinary_tail = truncated_row >> seam
        word_tail = SURVIVOR.inverse_word_preimage_zero(
            SURVIVOR.normalize_word(word)
        )
        if ordinary_tail != word_tail:
            raise AssertionError("truncated moving tail is not H_m^(-1)(0)")

        _, output_pair = GLOBAL.double_section_transduce(word, (1, 1))
        seed_pair = ((seed >> seam) & 1, (seed >> (seam + 1)) & 1)
        if output_pair != seed_pair:
            raise AssertionError("terminal transducer pair is not the next seed pair")

        if block in selected_set:
            rows.append(
                {
                    "block": block,
                    "seam_bits": seam,
                    "fringe_width": fringe_state.bit_length(),
                    "reversed_fringe_low_32": reversed_fringe & 0xFFFFFFFF,
                    "survivor_low_32": survivor_from_row & 0xFFFFFFFF,
                    "ordinary_shadow_bit_length": ordinary_tail.bit_length(),
                    "seed_pair": list(seed_pair),
                    "q_name": q_names[block],
                }
            )
        checks += 1

        if block < maximum_block:
            row = right_edge_step_mod(row, total_width)
            row = right_edge_step_mod(row, total_width)
            word = SURVIVOR.block_update(word, q_names[block])

    seed_bytes = seed.to_bytes((total_width + 7) // 8, "little")
    return {
        "maximum_block_inclusive": maximum_block,
        "total_width": total_width,
        "moving_cuts_checked": checks,
        "exact_full_cut": (
            "T^(2m)(S) = reverse_(2m)(A_m) + 2^(2m) X_m modulo 2^W"
        ),
        "exact_truncated_cut": (
            "T^(2m)(S mod 2^(2m)) = reverse_(2m)(A_m) + 2^(2m) H_m^(-1)(0)"
        ),
        "terminal_pair_identity": "G_m(11) equals seed bits (2m,2m+1)",
        "selected_rows": rows,
        "inverse_lift_sha256": hashlib.sha256(seed_bytes).hexdigest(),
        "all_checks_pass": True,
    }


def fringe_head_transition_relation() -> dict[tuple[int, int], set[tuple[int, int]]]:
    """Return every exact low-pair transition over the two imported bits."""

    adjacency = {head: set() for head in PAIR_STATES}
    for head in PAIR_STATES:
        for context in PAIR_STATES:
            state = (
                head[0]
                | (head[1] << 1)
                | (context[0] << 2)
                | (context[1] << 3)
            )
            next_state = FRINGE.advance_fringe_packed(state)
            target = (next_state & 1, (next_state >> 1) & 1)
            adjacency[head].add(target)
    return adjacency


def _word_statistic_row(
    word: tuple[str, ...], variable_names: list[str], indices: dict[str, int]
) -> list[Fraction]:
    row = [Fraction(0) for _ in variable_names]
    if not word:
        return row
    row[indices[f"L_{word[0]}"]] += 1
    row[indices[f"R_{word[-1]}"]] += 1
    for left, right in zip(word, word[1:]):
        row[indices[f"W_{left}{right}"]] += 1
    return row


def verify_coupled_pair_cocycle_no_go(
    maximum_word_length: int = 3,
) -> dict[str, Any]:
    """Classify the universal nearest-neighbor coupled additive ansatz.

    Seek a nearest-neighbor word functional ``F``, a potential ``P`` on the
    current fringe head, a potential ``V`` on the terminal output pair, and a
    constant ``K`` such that every locally allowed coupled tile satisfies

        F(H^+) - F(H) + P(h^+) - P(h) = V(e) + K.

    Here ``H^+=q(h) p scan_11(H)``.  Exact rational elimination shows that
    ``F`` is only a multiple of word length (up to a zero coboundary), while
    both potentials are constant.  Thus this range-two linear ansatz cannot
    distinguish the branch or terminal output pair.
    """

    pair_words = tuple(itertools.product(LETTERS, repeat=2))
    variable_names = (
        [f"W_{left}{right}" for left, right in pair_words]
        + [f"L_{letter}" for letter in LETTERS]
        + [f"R_{letter}" for letter in LETTERS]
        + [f"P_{head[0]}{head[1]}" for head in PAIR_STATES]
        + [f"V_{state[0]}{state[1]}" for state in PAIR_STATES]
        + ["K"]
    )
    indices = {name: index for index, name in enumerate(variable_names)}
    adjacency = fringe_head_transition_relation()
    equations: list[list[Fraction]] = []

    for length in range(maximum_word_length + 1):
        for word in itertools.product(LETTERS, repeat=length):
            scanned, terminal = scan_reversed_word(word)
            before = _word_statistic_row(word, variable_names, indices)
            for head in PAIR_STATES:
                q_name = "u" if head == (0, 0) else "t"
                after_word = (q_name, "p") + scanned
                after = _word_statistic_row(after_word, variable_names, indices)
                for target in sorted(adjacency[head]):
                    equation = [
                        after[index] - before[index]
                        for index in range(len(variable_names))
                    ]
                    equation[indices[f"P_{target[0]}{target[1]}"]] += 1
                    equation[indices[f"P_{head[0]}{head[1]}"]] -= 1
                    equation[indices[f"V_{terminal[0]}{terminal[1]}"]] -= 1
                    equation[indices["K"]] -= 1
                    equations.append(equation)

    reduced, pivots = GLOBAL._rational_rref(equations, len(variable_names))
    expected_pivots = [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        15,
        16,
        17,
        19,
        20,
        21,
    ]
    if pivots != expected_pivots:
        raise AssertionError("unexpected coupled pair-cocycle rank")

    nonzero_rows = [row for row in reduced if any(value != 0 for value in row)]
    if len(nonzero_rows) != 18:
        raise AssertionError("unexpected coupled pair-cocycle reduced system")

    relation_map: dict[str, dict[str, Fraction]] = {}
    for row in nonzero_rows:
        pivot = next(index for index, value in enumerate(row) if value != 0)
        if row[pivot] != 1:
            raise AssertionError("RREF pivot is not normalized")
        relation_map[variable_names[pivot]] = {
            variable_names[index]: value
            for index, value in enumerate(row)
            if value != 0
        }

    for head in ("00", "01", "10"):
        if relation_map[f"P_{head}"] != {
            f"P_{head}": Fraction(1),
            "P_11": Fraction(-1),
        }:
            raise AssertionError("fringe-head potential is not forced constant")
    for state in ("00", "01", "10"):
        if relation_map[f"V_{state}"] != {
            f"V_{state}": Fraction(1),
            "V_11": Fraction(-1),
        }:
            raise AssertionError("terminal-state potential is not forced constant")

    half_terms = {"V_11": Fraction(-1, 2), "K": Fraction(-1, 2)}
    for letter in LETTERS:
        expected = {
            f"L_{letter}": Fraction(1),
            f"R_{letter}": Fraction(1),
            **half_terms,
        }
        if relation_map[f"L_{letter}"] != expected:
            raise AssertionError("left boundary relation changed")
    for left, right in pair_words:
        expected = {
            f"W_{left}{right}": Fraction(1),
            f"R_{left}": Fraction(-1),
            f"R_{right}": Fraction(1),
            **half_terms,
        }
        if left == right:
            expected.pop(f"R_{left}")
            expected.pop(f"R_{right}", None)
        if relation_map[f"W_{left}{right}"] != expected:
            raise AssertionError("nearest-neighbor relation changed")

    return {
        "maximum_word_length_needed": maximum_word_length,
        "variables": variable_names,
        "equations": len(equations),
        "rank": len(pivots),
        "nullity": len(variable_names) - len(pivots),
        "fringe_head_adjacency": {
            "".join(map(str, head)): [
                "".join(map(str, target)) for target in sorted(adjacency[head])
            ]
            for head in PAIR_STATES
        },
        "complete_solution": {
            "word_functional": (
                "F(H)=c*len(H), up to an identically-zero nearest-neighbor coboundary"
            ),
            "fringe_head_potential": "P_00=P_01=P_10=P_11",
            "terminal_pair_potential": "V_00=V_01=V_10=V_11",
            "boundary_sensitivity": (
                "the increment cannot distinguish q=t from q=u or any terminal pair"
            ),
        },
        "all_checks_pass": True,
    }


def run_campaign(
    *,
    maximum_block: int = DEFAULT_MAXIMUM_BLOCK,
    total_width: int = DEFAULT_TOTAL_WIDTH,
    maximum_word_length: int = DEFAULT_WORD_EXHAUSTION_LENGTH,
) -> dict[str, Any]:
    if maximum_block > ABSOLUTE_MAXIMUM_BLOCK:
        raise CoupledStripLimitError(
            f"maximum block exceeds absolute maximum {ABSOLUTE_MAXIMUM_BLOCK}"
        )
    if total_width > ABSOLUTE_TOTAL_WIDTH:
        raise CoupledStripLimitError(
            f"total width exceeds absolute maximum {ABSOLUTE_TOTAL_WIDTH}"
        )
    if maximum_word_length > ABSOLUTE_WORD_EXHAUSTION_LENGTH:
        raise CoupledStripLimitError(
            "word exhaustion exceeds absolute maximum "
            f"{ABSOLUTE_WORD_EXHAUSTION_LENGTH}"
        )

    payload = {
        "coupled_transfer": verify_coupled_transfer(maximum_word_length),
        "moving_cut_identity": verify_moving_cut_identity(maximum_block, total_width),
        "coupled_pair_cocycle_no_go": verify_coupled_pair_cocycle_no_go(),
        "exact_conclusions": {
            "moving_cut": (
                "the reversed right fringe and future survivor are the exact low/high halves of one moving right-edge row"
            ),
            "finite_shadow_cut": (
                "the truncated seed evolves to the same fringe low half and the ordinary inverse-word state as its high half"
            ),
            "range_two_no_go": (
                "no universal nearest-neighbor additive cocycle on the coupled head/word tiles distinguishes the fringe branch or reconstructed pair"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-coupled-strip-v1\0")
    digest.update(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maximum-block", type=_positive_integer, default=DEFAULT_MAXIMUM_BLOCK
    )
    parser.add_argument(
        "--total-width", type=_positive_integer, default=DEFAULT_TOTAL_WIDTH
    )
    parser.add_argument(
        "--maximum-word-length",
        type=_positive_integer,
        default=DEFAULT_WORD_EXHAUSTION_LENGTH,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(
        maximum_block=args.maximum_block,
        total_width=args.total_width,
        maximum_word_length=args.maximum_word_length,
    )
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-coupled-strip-v1",
        "question": "problem1",
        "hypothesis": (
            "The autonomous fringe and whole-word transducer form one exact moving strip, and the first coupled nearest-neighbor additive cocycle class can be decided completely."
        ),
        "backend": "python-exact-coupled-transfer",
        "parameters": {
            "maximum_block": args.maximum_block,
            "total_width": args.total_width,
            "maximum_word_length": args.maximum_word_length,
        },
        "result_summary": result,
        "status": "partial-proof-and-finite-exhaustive",
        "proof_scope": (
            "The moving-cut, local transfer, and rational cocycle classification are all-width/all-word statements. Finite campaigns independently cross-check their implementations."
        ),
        "limitations": [
            "the cocycle theorem covers only universal rational nearest-neighbor additive functionals",
            "an invariant restricted to the unique actual fringe orbit may evade the local-head classification",
            "nonlinear and growing-memory coupled invariants remain open",
            "the result does not exclude eventual center period two",
            "the result does not solve Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
