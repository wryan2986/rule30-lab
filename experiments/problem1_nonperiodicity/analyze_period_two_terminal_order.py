#!/usr/bin/env python3
"""Analyze the terminal-zero/leading-order cocycle in the period-two word system.

The accumulated inverse word G updates by

    G^+ = (G|_11) p q,  q in {t,u},

where the section and terminal pair are obtained by the exact four-state
right-to-left transducer.  Let ord_t(G) be the length of the maximal leading
run of ``t`` letters.  This analyzer verifies the all-word identity

    ord_t(G^+) = ord_t(G)+1  if G(11)=00,
                  0          otherwise.

Thus ord_t is an exact nonlinear cross-word counter: it is the current run
length of consecutive zero output pairs.  The finite campaign also audits the
actual zero-initialized fringe orbit and records growing zero-run examples.
It does not prove that zero runs are bounded or unbounded, and it does not
solve Rule 30 center nonperiodicity.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter
from typing import Any, Iterable

LETTERS = ("t", "p", "u")
BRANCHES = ("t", "u")
PAIR_STATES = ("00", "01", "10", "11")
DEFAULT_WORD_EXHAUSTION_LENGTH = 8
DEFAULT_ACTUAL_BLOCKS = 4096
ABSOLUTE_WORD_EXHAUSTION_LENGTH = 10
ABSOLUTE_ACTUAL_BLOCKS = 20000

# entry = (emitted letter, successor scan state)
TRANSITIONS: dict[tuple[str, str], tuple[str, str]] = {
    ("00", "t"): ("t", "00"),
    ("00", "p"): ("p", "11"),
    ("00", "u"): ("p", "11"),
    ("01", "t"): ("p", "01"),
    ("01", "p"): ("u", "10"),
    ("01", "u"): ("u", "10"),
    ("10", "t"): ("p", "11"),
    ("10", "p"): ("p", "01"),
    ("10", "u"): ("t", "00"),
    ("11", "t"): ("u", "10"),
    ("11", "p"): ("t", "00"),
    ("11", "u"): ("p", "01"),
}


def transduce(word: str, start_pair: str = "11") -> tuple[str, str]:
    """Return ``(word|_start_pair, word(start_pair))`` by one exact scan."""
    if start_pair not in PAIR_STATES:
        raise ValueError("start_pair must be a two-bit state")
    if any(letter not in LETTERS for letter in word):
        raise ValueError("word contains an unknown letter")
    output = [""] * len(word)
    state = start_pair
    for index in range(len(word) - 1, -1, -1):
        output[index], state = TRANSITIONS[(state, word[index])]
    return "".join(output), state


def block_update(word: str, branch: str) -> tuple[str, str]:
    """Return the updated word and the current terminal output pair."""
    if branch not in BRANCHES:
        raise ValueError("branch must be t or u")
    section, terminal = transduce(word)
    return section + "p" + branch, terminal


def leading_t_order(word: str) -> int:
    """Length of the maximal leading run of ``t`` letters."""
    return len(word) - len(word.lstrip("t"))


def expected_next_order(word: str) -> tuple[int, str]:
    """The exact order predicted from the current terminal pair."""
    _, terminal = transduce(word)
    current = leading_t_order(word)
    return (current + 1 if terminal == "00" else 0), terminal


def verify_terminal_order_cocycle(maximum_word_length: int) -> dict[str, Any]:
    """Exhaust every word through the configured length and both branches."""
    checked = 0
    terminal_counts: Counter[str] = Counter()
    for length in range(maximum_word_length + 1):
        for letters in itertools.product(LETTERS, repeat=length):
            word = "".join(letters)
            predicted, terminal = expected_next_order(word)
            terminal_counts[terminal] += 1
            for branch in BRANCHES:
                updated, observed_terminal = block_update(word, branch)
                if observed_terminal != terminal:
                    raise AssertionError("terminal changed across identical scan")
                observed = leading_t_order(updated)
                if observed != predicted:
                    raise AssertionError(
                        (word, branch, terminal, predicted, observed, updated)
                    )
                checked += 1
    return {
        "maximum_word_length": maximum_word_length,
        "word_branch_cases_checked": checked,
        "terminal_counts_before_branch_duplication": dict(sorted(terminal_counts.items())),
        "exact_identity": (
            "ord_t((G|_11)pq)=ord_t(G)+1 when G(11)=00, and 0 otherwise"
        ),
        "branch_independent": True,
        "all_checks_pass": True,
    }


def fringe_step(state: int) -> int:
    """Exact autonomous two-step map for the zero-initialized right fringe."""
    if state < 0:
        raise ValueError("fringe state must be nonnegative")
    packed = 1 + 2 * state
    odd = packed ^ ((packed >> 1) | (packed >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def fringe_branch(state: int) -> str:
    return "u" if state & 3 == 0 else "t"


def _zero_runs(values: Iterable[str]) -> list[tuple[int, int, int]]:
    runs: list[tuple[int, int, int]] = []
    start: int | None = None
    sequence = list(values)
    for index, value in enumerate(sequence + ["END"]):
        if value == "00" and start is None:
            start = index
        elif value != "00" and start is not None:
            runs.append((start, index - 1, index - start))
            start = None
    return runs


def simulate_actual_path(blocks: int) -> dict[str, Any]:
    """Run the exact coupled fringe/word recurrence for a bounded prefix."""
    fringe = 0
    word = ""
    pairs: list[str] = []
    branches: list[str] = []
    orders: list[int] = []
    records: list[dict[str, Any]] = []
    best = 0

    for block in range(blocks):
        branch = fringe_branch(fringe)
        current_order = leading_t_order(word)
        updated, terminal = block_update(word, branch)
        next_order = leading_t_order(updated)
        expected = current_order + 1 if terminal == "00" else 0
        if next_order != expected:
            raise AssertionError("actual path violated terminal-order cocycle")

        branches.append(branch)
        pairs.append(terminal)
        orders.append(current_order)
        word = updated
        fringe = fringe_step(fringe)

    for start, end, length in _zero_runs(pairs):
        observed_orders = orders[start : end + 1]
        if observed_orders != list(
            range(observed_orders[0], observed_orders[0] + length)
        ):
            raise AssertionError("zero run did not increment order exactly")
        if length > best:
            best = length
            left = max(0, start - 10)
            right = min(blocks, end + 11)
            records.append(
                {
                    "run_length": length,
                    "start_block_zero_based": start,
                    "end_block_zero_based": end,
                    "branch_context": "".join(branches[left:right]),
                    "context_start_block": left,
                    "context_end_block_exclusive": right,
                }
            )

    pair_counts = Counter(pairs)
    longest = max(_zero_runs(pairs), key=lambda item: item[2], default=(-1, -1, 0))
    return {
        "blocks": blocks,
        "pair_counts": dict(sorted(pair_counts.items())),
        "longest_zero_pair_run": {
            "length": longest[2],
            "start_block_zero_based": longest[0],
            "end_block_zero_based": longest[1],
        },
        "record_zero_runs": records,
        "final_word_length": len(word),
        "final_leading_t_order": leading_t_order(word),
        "exact_interpretation": (
            "leading-t order equals the length of the immediately preceding "
            "consecutive terminal-00 run"
        ),
        "scope_warning": (
            "bounded actual-path data neither bounds zero runs nor proves "
            "that nonzero terminal pairs occur infinitely often"
        ),
        "all_checks_pass": True,
    }


def verify_run_counter_on_all_branch_words(maximum_length: int) -> dict[str, Any]:
    """Check the run-counter corollary on every t/u driver through a small depth."""
    checked_prefixes = 0
    for length in range(maximum_length + 1):
        for branches in itertools.product(BRANCHES, repeat=length):
            word = ""
            preceding_zero_run = 0
            for branch in branches:
                if leading_t_order(word) != preceding_zero_run:
                    raise AssertionError("leading order is not the zero-run counter")
                word, terminal = block_update(word, branch)
                preceding_zero_run = preceding_zero_run + 1 if terminal == "00" else 0
                checked_prefixes += 1
            if leading_t_order(word) != preceding_zero_run:
                raise AssertionError("final leading order is not the zero-run counter")
    return {
        "maximum_branch_word_length": maximum_length,
        "driver_prefix_steps_checked": checked_prefixes,
        "all_checks_pass": True,
    }


def run_campaign(
    *,
    maximum_word_length: int = DEFAULT_WORD_EXHAUSTION_LENGTH,
    actual_blocks: int = DEFAULT_ACTUAL_BLOCKS,
) -> dict[str, Any]:
    if not 0 <= maximum_word_length <= ABSOLUTE_WORD_EXHAUSTION_LENGTH:
        raise ValueError("word exhaustion outside campaign cap")
    if not 1 <= actual_blocks <= ABSOLUTE_ACTUAL_BLOCKS:
        raise ValueError("actual block count outside campaign cap")

    started = time.perf_counter()
    payload: dict[str, Any] = {
        "terminal_order_cocycle": verify_terminal_order_cocycle(maximum_word_length),
        "all_driver_run_counter": verify_run_counter_on_all_branch_words(12),
        "actual_path": simulate_actual_path(actual_blocks),
        "exact_conclusions": {
            "nonlinear_cross_word_bridge": (
                "the terminal pair at one boundary exactly increments or resets "
                "the leading-t order at the opposite word boundary"
            ),
            "finite_support_reformulation": (
                "eventual terminal 00 is equivalent to eventual unit-slope "
                "divergence of the leading-t order"
            ),
            "remaining_target": (
                "prove that the zero-initialized coupled fringe orbit resets "
                "the leading-t order infinitely often"
            ),
        },
    }
    payload["runtime_seconds"] = round(time.perf_counter() - started, 6)
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-terminal-order-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--word-length", type=int, default=DEFAULT_WORD_EXHAUSTION_LENGTH
    )
    parser.add_argument("--actual-blocks", type=int, default=DEFAULT_ACTUAL_BLOCKS)
    args = parser.parse_args()
    print(
        json.dumps(
            run_campaign(
                maximum_word_length=args.word_length,
                actual_blocks=args.actual_blocks,
            ),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
