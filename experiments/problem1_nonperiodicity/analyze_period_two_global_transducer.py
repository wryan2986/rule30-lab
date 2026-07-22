#!/usr/bin/env python3
"""Analyze the whole-word transducer behind the period-two inverse lift.

The accumulated inverse word ``G`` updates by taking its section along the
literal input pair ``11`` and appending ``p q``. Although that operation acts
on the complete growing word, it is computed by a four-state right-to-left
Mealy transducer. This analyzer verifies the exact table, proves the complete
single-letter additive-cocycle space, and records a counterexample showing
that the currently known short forbidden branch words do not by themselves
bound zero-pair runs.

These are structural and no-go results. They do not exclude period two and do
not solve Rule 30 center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable

DEFAULT_WORD_EXHAUSTION_LENGTH = 7
ABSOLUTE_WORD_EXHAUSTION_LENGTH = 9
LETTERS = ("t", "p", "u")
PAIR_STATES = ((0, 0), (0, 1), (1, 0), (1, 1))
KNOWN_BRANCH_FORBIDDEN_WORDS = ("uu", "ttttt", "ututtu")
SHORT_LANGUAGE_COUNTEREXAMPLE = "ttttututtttuttttututtttutututttuttuttutu"


class GlobalTransducerLimitError(RuntimeError):
    """Raised before an explicitly capped finite campaign is exceeded."""


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


SURVIVOR = _load_sibling(
    "analyze_period_two_schedule_survivor.py", "schedule_survivor"
)


def word_action_on_pair(
    word: tuple[str, ...], pair: tuple[int, int]
) -> tuple[int, int]:
    """Apply an inverse-generator word to a two-bit input word."""

    if pair not in PAIR_STATES:
        raise ValueError("pair must be binary")
    current = word
    outputs: list[int] = []
    for bit in pair:
        outputs.append(SURVIVOR.inverse_word_root(current, bit))
        current = SURVIVOR.inverse_word_section(current, bit)
    return outputs[0], outputs[1]


def letter_transition(
    letter: str, incoming_pair: tuple[int, int]
) -> tuple[str, tuple[int, int]]:
    """Return the double-section letter and transformed scan pair."""

    if letter not in LETTERS:
        raise ValueError("unknown inverse-generator letter")
    if incoming_pair not in PAIR_STATES:
        raise ValueError("incoming_pair must be binary")
    one_letter = (letter,)
    section = SURVIVOR.section_along(one_letter, incoming_pair)
    if len(section) != 1:
        raise AssertionError("a generator section must remain one generator")
    return section[0], word_action_on_pair(one_letter, incoming_pair)


def double_section_transduce(
    word: tuple[str, ...], start_pair: tuple[int, int] = (1, 1)
) -> tuple[tuple[str, ...], tuple[int, int]]:
    """Compute ``word|_start_pair`` and ``word(start_pair)`` in one scan."""

    if start_pair not in PAIR_STATES:
        raise ValueError("start_pair must be binary")
    output = [""] * len(word)
    state = start_pair
    for index in range(len(word) - 1, -1, -1):
        output[index], state = letter_transition(word[index], state)
    return tuple(output), state


def transition_table() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for state in PAIR_STATES:
        for letter in LETTERS:
            output, successor = letter_transition(letter, state)
            rows.append(
                {
                    "incoming_pair": "".join(map(str, state)),
                    "input_letter": letter,
                    "output_letter": output,
                    "successor_pair": "".join(map(str, successor)),
                }
            )
    return rows


def verify_transducer_table(maximum_word_length: int) -> dict[str, Any]:
    """Exhaust complete short words against independent section operations."""

    checked = 0
    for length in range(maximum_word_length + 1):
        for word in itertools.product(LETTERS, repeat=length):
            for pair in PAIR_STATES:
                output, terminal = double_section_transduce(word, pair)
                direct_section = SURVIVOR.section_along(word, pair)
                direct_terminal = word_action_on_pair(word, pair)
                if output != direct_section:
                    raise AssertionError("whole-word transducer section mismatch")
                if terminal != direct_terminal:
                    raise AssertionError("whole-word transducer terminal mismatch")
                checked += 1
    return {
        "maximum_word_length": maximum_word_length,
        "word_pair_cases_checked": checked,
        "transition_table": transition_table(),
        "exact_identity": (
            "right-to-left scan returns (G|_v, G(v)) for every binary pair v"
        ),
        "all_checks_pass": True,
    }


def verify_block_recurrence(maximum_word_length: int) -> dict[str, Any]:
    """Cross-check ``G^+=G|_11 p q`` and its boundary output pair."""

    checked = 0
    for length in range(maximum_word_length + 1):
        for word in itertools.product(LETTERS, repeat=length):
            section, output_pair = double_section_transduce(word)
            if output_pair != word_action_on_pair(word, (1, 1)):
                raise AssertionError("terminal pair is not G(11)")
            for q_name in ("t", "u"):
                expected = section + ("p", q_name)
                observed = SURVIVOR.block_update(word, q_name)
                if observed != expected:
                    raise AssertionError("global block recurrence mismatch")
                checked += 1
    return {
        "word_branch_cases_checked": checked,
        "exact_recurrence": "G_(m+1)=(G_m)|_11 p q_m",
        "output_pair": "terminal scan state equals G_m(11)",
        "finite_support_target": "terminal scan state is eventually 00",
        "all_checks_pass": True,
    }


def _rational_rref(
    rows: list[list[Fraction]], column_count: int
) -> tuple[list[list[Fraction]], list[int]]:
    matrix = [row[:] for row in rows]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row
                for row in range(pivot_row, len(matrix))
                if matrix[row][column] != 0
            ),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = (
            matrix[selected],
            matrix[pivot_row],
        )
        divisor = matrix[pivot_row][column]
        matrix[pivot_row] = [value / divisor for value in matrix[pivot_row]]
        for row in range(len(matrix)):
            if row == pivot_row or matrix[row][column] == 0:
                continue
            multiplier = matrix[row][column]
            matrix[row] = [
                matrix[row][index] - multiplier * matrix[pivot_row][index]
                for index in range(column_count)
            ]
        pivot_columns.append(column)
        pivot_row += 1
    return matrix, pivot_columns


def verify_additive_cocycle_no_go() -> dict[str, Any]:
    """Solve every single-letter additive cocycle over the rationals."""

    variable_names = [
        "a_t",
        "a_p",
        "a_u",
        "V_00",
        "V_01",
        "V_10",
        "V_11",
    ]
    rows: list[list[Fraction]] = []
    for state in PAIR_STATES:
        for input_letter in LETTERS:
            output_letter, successor = letter_transition(input_letter, state)
            row = [Fraction(0) for _ in variable_names]
            row[LETTERS.index(input_letter)] += 1
            row[LETTERS.index(output_letter)] -= 1
            row[3 + PAIR_STATES.index(successor)] -= 1
            row[3 + PAIR_STATES.index(state)] += 1
            rows.append(row)

    reduced, pivots = _rational_rref(rows, len(variable_names))
    expected_pivots = [0, 1, 3, 4, 5]
    if pivots != expected_pivots:
        raise AssertionError("unexpected additive-cocycle rank")

    nonzero_rows = [row for row in reduced if any(value != 0 for value in row)]
    expected_rows = [
        [Fraction(1), Fraction(0), Fraction(-1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(1), Fraction(-1), Fraction(0), Fraction(0), Fraction(0), Fraction(0)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(0), Fraction(-1)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(0), Fraction(-1)],
        [Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(1), Fraction(-1)],
    ]
    if nonzero_rows != expected_rows:
        raise AssertionError("additive-cocycle solution space changed")

    return {
        "variables": variable_names,
        "edge_equations": len(rows),
        "rank": len(pivots),
        "nullity": len(variable_names) - len(pivots),
        "complete_solution": {
            "letter_weights": "a_t=a_p=a_u",
            "state_potentials": "V_00=V_01=V_10=V_11",
        },
        "interpretation": (
            "the only additive word statistic is a multiple of word length; "
            "the only state potential is constant"
        ),
        "all_checks_pass": True,
    }


def _longest_zero_pair_run(
    pairs: Iterable[tuple[int, int]]
) -> tuple[int, int, int]:
    best_length = 0
    best_start = -1
    current_start = -1
    current_length = 0
    for index, pair in enumerate(pairs):
        if pair == (0, 0):
            if current_length == 0:
                current_start = index
            current_length += 1
            if current_length > best_length:
                best_length = current_length
                best_start = current_start
        else:
            current_length = 0
            current_start = -1
    return best_length, best_start, best_start + best_length - 1


def verify_short_language_counterexample() -> dict[str, Any]:
    """Refute use of the three short branch exclusions as a complete driver."""

    q_word = SHORT_LANGUAGE_COUNTEREXAMPLE
    violated = [word for word in KNOWN_BRANCH_FORBIDDEN_WORDS if word in q_word]
    if violated:
        raise AssertionError("counterexample violates a claimed forbidden word")

    word: tuple[str, ...] = ()
    pairs: list[tuple[int, int]] = []
    leading_t_runs: list[int] = []
    for q_name in q_word:
        word = SURVIVOR.block_update(word, q_name)
        pairs.append(word_action_on_pair(word, (1, 1)))
        leading_t_runs.append(len(word) - len(SURVIVOR.normalize_word(word)))

    run_length, start, end = _longest_zero_pair_run(pairs)
    if (run_length, start, end) != (10, 30, 39):
        raise AssertionError("short-language counterexample changed")
    if leading_t_runs[start : end + 1] != list(range(10)):
        raise AssertionError("zero-pair run did not grow the leading t run exactly")

    return {
        "branch_word": q_word,
        "branch_word_length": len(q_word),
        "avoids": list(KNOWN_BRANCH_FORBIDDEN_WORDS),
        "longest_zero_pair_run": run_length,
        "zero_pair_run_start_zero_based": start,
        "zero_pair_run_end_zero_based": end,
        "zero_run_branch_suffix": q_word[start : end + 1],
        "leading_t_runs_during_zero_pairs": leading_t_runs[start : end + 1],
        "exact_conclusion": (
            "the three known forbidden branch words alone do not bound "
            "survivor zero-pair runs"
        ),
        "scope_warning": (
            "this finite branch word is not claimed to occur in the exact "
            "autonomous fringe orbit"
        ),
        "all_checks_pass": True,
    }


def run_campaign(
    *, maximum_word_length: int = DEFAULT_WORD_EXHAUSTION_LENGTH
) -> dict[str, Any]:
    if maximum_word_length > ABSOLUTE_WORD_EXHAUSTION_LENGTH:
        raise GlobalTransducerLimitError(
            "word exhaustion exceeds absolute maximum "
            f"{ABSOLUTE_WORD_EXHAUSTION_LENGTH}"
        )
    payload = {
        "whole_word_transducer": verify_transducer_table(maximum_word_length),
        "block_recurrence": verify_block_recurrence(maximum_word_length),
        "additive_cocycle_no_go": verify_additive_cocycle_no_go(),
        "short_language_counterexample": verify_short_language_counterexample(),
        "exact_conclusions": {
            "global_reformulation": (
                "the complete growing word is scanned by a four-state "
                "right-to-left transducer and finite support means its terminal "
                "state is eventually 00"
            ),
            "additive_no_go": (
                "no nontrivial single-letter additive cocycle telescopes the "
                "growing middle"
            ),
            "short_language_no_go": (
                "the forbidden words uu, ttttt, and ututtu are insufficient "
                "without the exact autonomous fringe orbit"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-global-transducer-v1\0")
    digest.update(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maximum-word-length",
        type=_positive_integer,
        default=DEFAULT_WORD_EXHAUSTION_LENGTH,
    )
    return parser


def main() -> int:
    args = _parser().parse_args()
    result = run_campaign(maximum_word_length=args.maximum_word_length)
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-global-transducer-v1",
        "question": "problem1",
        "hypothesis": (
            "A whole-word transducer can bridge the growing middle and expose "
            "which global cocycle strategies remain viable."
        ),
        "backend": "python-exact-finite-transducer",
        "parameters": {
            "maximum_word_length": args.maximum_word_length,
            "absolute_maximum_word_length": ABSOLUTE_WORD_EXHAUSTION_LENGTH,
        },
        "result_summary": result,
        "status": "partial-proof-and-finite-exhaustive",
        "proof_scope": (
            "The four-state table and additive-cocycle classification are "
            "all-word statements. Short-word exhaustion cross-checks the table. "
            "The branch-language counterexample is one exact finite word."
        ),
        "limitations": [
            "the additive theorem does not exclude nonlinear or growing-memory cocycles",
            "the finite branch counterexample is not claimed to be an exact fringe trace",
            "the result does not prove the alternating survivor has infinite support",
            "the result does not exclude eventual center period two",
            "the result does not solve Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
