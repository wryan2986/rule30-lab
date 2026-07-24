#!/usr/bin/env python3
"""Analyze the exact past/future dual-cut criterion for period-two zero runs.

For an accumulated inverse word G and a future branch driver q_0,q_1,...,
let C_0 be empty and update fresh boundary words by

    C_(j+1) = (C_j|_11) p q_j.

Write s_j=C_j(11).  Starting from G_0=G under the same driver, write

    G_(j+1) = (G_j|_11) p q_j,
    e_j = G_j(11).

The exact factorization is

    G_j = (G|_(s_0...s_(j-1))) C_j,

so the output word e_0...e_(L-1) is the dual action of G on
s_0...s_(L-1).  Since the dual action is invertible at every depth,
L consecutive terminal 00 pairs occur exactly when the fresh future
state prefix equals the unique past-determined preimage of 00^L.

This is an all-depth identity.  Bounded campaigns validate the implementation
and record actual-orbit reset depths; they do not prove infinitely many resets.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from typing import Any, Iterable

LETTERS = ("t", "p", "u")
BRANCHES = ("t", "u")
PAIR_STATES = ("00", "01", "10", "11")
DEFAULT_WORD_LENGTH = 5
DEFAULT_DRIVER_DEPTH = 6
DEFAULT_ACTUAL_BLOCKS = 10000
DEFAULT_ACTUAL_CUT_DEPTH = 12
ABSOLUTE_WORD_LENGTH = 7
ABSOLUTE_DRIVER_DEPTH = 8
ABSOLUTE_ACTUAL_BLOCKS = 30000
ABSOLUTE_ACTUAL_CUT_DEPTH = 20

# (incoming pair, input letter) -> (section/output letter, successor pair)
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


def scan(word: str, start_pair: str = "11") -> tuple[str, str]:
    """Return (word|_start_pair, word(start_pair)) by exact right-to-left scan."""
    if start_pair not in PAIR_STATES:
        raise ValueError("unknown pair state")
    if any(letter not in LETTERS for letter in word):
        raise ValueError("word contains an unknown generator")
    output = [""] * len(word)
    state = start_pair
    for index in range(len(word) - 1, -1, -1):
        output[index], state = TRANSITIONS[(state, word[index])]
    return "".join(output), state


def block_update(word: str, branch: str) -> tuple[str, str]:
    if branch not in BRANCHES:
        raise ValueError("branch must be t or u")
    section, terminal = scan(word, "11")
    return section + "p" + branch, terminal


def section_along_state_word(word: str, states: Iterable[str]) -> str:
    current = word
    for state in states:
        current, _ = scan(current, state)
    return current


def dual_action(word: str, state_word: Iterable[str]) -> tuple[tuple[str, ...], str]:
    """Apply the dual tree action of word to a word over the four pair states."""
    current = word
    output: list[str] = []
    for state in state_word:
        current, image = scan(current, state)
        output.append(image)
    return tuple(output), current


def dual_preimage(word: str, target_word: Iterable[str]) -> tuple[str, ...]:
    """Unique state word mapped to target_word by the invertible dual action."""
    current = word
    result: list[str] = []
    for target in target_word:
        if target not in PAIR_STATES:
            raise ValueError("target contains an unknown pair state")
        matches: list[tuple[str, str]] = []
        for state in PAIR_STATES:
            section, image = scan(current, state)
            if image == target:
                matches.append((state, section))
        if len(matches) != 1:
            raise AssertionError("dual action is not uniquely invertible")
        state, current = matches[0]
        result.append(state)
    return tuple(result)


def fresh_boundary_states(branches: Iterable[str]) -> tuple[tuple[str, ...], str]:
    """Return s_0...s_L and C_(L+1) for a length-L driver.

    The returned state word has one more symbol than the branch word:
    s_j=C_j(11), with C_0 empty.
    """
    current = ""
    states: list[str] = []
    for branch in tuple(branches) + (None,):
        _, terminal = scan(current, "11")
        states.append(terminal)
        if branch is not None:
            current, _ = block_update(current, branch)
    return tuple(states), current


def coupled_outputs(word: str, branches: Iterable[str]) -> tuple[tuple[str, ...], str]:
    """Return e_0...e_L and G_(L+1) for a length-L driver."""
    current = word
    outputs: list[str] = []
    for branch in tuple(branches) + (None,):
        _, terminal = scan(current, "11")
        outputs.append(terminal)
        if branch is not None:
            current, _ = block_update(current, branch)
    return tuple(outputs), current


def verify_factorization(maximum_word_length: int, maximum_driver_depth: int) -> dict[str, Any]:
    cases = 0
    level_counts: Counter[int] = Counter()
    for word_length in range(maximum_word_length + 1):
        for letters in itertools.product(LETTERS, repeat=word_length):
            word = "".join(letters)
            for depth in range(maximum_driver_depth + 1):
                for driver in itertools.product(BRANCHES, repeat=depth):
                    states, fresh_final = fresh_boundary_states(driver)
                    outputs, coupled_final = coupled_outputs(word, driver)
                    observed, _ = dual_action(word, states)
                    if observed != outputs:
                        raise AssertionError(("dual output mismatch", word, driver))
                    final_section = section_along_state_word(word, states[:-1])
                    expected_final = final_section + fresh_final
                    if coupled_final != expected_final:
                        raise AssertionError(
                            ("final factorization mismatch", word, driver, coupled_final, expected_final)
                        )
                    cases += 1
                    level_counts[depth] += 1
    return {
        "maximum_initial_word_length": maximum_word_length,
        "maximum_driver_depth": maximum_driver_depth,
        "word_driver_cases_checked": cases,
        "cases_by_driver_depth": {str(k): v for k, v in sorted(level_counts.items())},
        "exact_factorization": (
            "G_j=(G|_(s_0...s_(j-1))) C_j and "
            "(e_0,...,e_(L-1))=tau_G(s_0,...,s_(L-1))"
        ),
        "all_checks_pass": True,
    }


def verify_unique_zero_target(maximum_word_length: int, maximum_depth: int) -> dict[str, Any]:
    cases = 0
    for word_length in range(maximum_word_length + 1):
        for letters in itertools.product(LETTERS, repeat=word_length):
            word = "".join(letters)
            for depth in range(maximum_depth + 1):
                target = ("00",) * depth
                preimage = dual_preimage(word, target)
                observed, _ = dual_action(word, preimage)
                if observed != target:
                    raise AssertionError("zero-target inverse failed")
                if depth <= 4:
                    witnesses = []
                    for candidate in itertools.product(PAIR_STATES, repeat=depth):
                        image, _ = dual_action(word, candidate)
                        if image == target:
                            witnesses.append(candidate)
                    if witnesses != [preimage]:
                        raise AssertionError("zero target is not unique")
                cases += 1
    return {
        "maximum_initial_word_length": maximum_word_length,
        "maximum_target_depth": maximum_depth,
        "word_depth_cases_checked": cases,
        "exact_criterion": (
            "L terminal-zero outputs occur iff the fresh future state prefix "
            "equals tau_G^(-1)(00^L)"
        ),
        "all_checks_pass": True,
    }


def fringe_step(state: int) -> int:
    if state < 0:
        raise ValueError("fringe state must be nonnegative")
    packed = 1 + 2 * state
    odd = packed ^ ((packed >> 1) | (packed >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def fringe_branch(state: int) -> str:
    return "u" if state & 3 == 0 else "t"


def actual_driver(blocks: int) -> str:
    state = 0
    out: list[str] = []
    for _ in range(blocks):
        out.append(fringe_branch(state))
        state = fringe_step(state)
    return "".join(out)


def actual_words_and_pairs(
    driver: str, selected_cuts: set[int]
) -> tuple[dict[int, str], list[str]]:
    word = ""
    words: dict[int, str] = {}
    pairs: list[str] = []
    for block, branch in enumerate(driver):
        if block in selected_cuts:
            words[block] = word
        word, terminal = block_update(word, branch)
        pairs.append(terminal)
    return words, pairs


def _zero_run_from(pairs: list[str], start: int, cap: int) -> int:
    length = 0
    while start + length < len(pairs) and length < cap and pairs[start + length] == "00":
        length += 1
    return length


def verify_actual_cut(blocks: int, cut_depth: int) -> dict[str, Any]:
    driver = actual_driver(blocks + cut_depth)
    sampled_cuts = list(range(0, blocks, 997))
    if blocks - 1 not in sampled_cuts:
        sampled_cuts.append(blocks - 1)
    words, pairs = actual_words_and_pairs(driver, set(sampled_cuts))

    mismatch_histogram: Counter[int] = Counter()
    checked = 0
    for cut in sampled_cuts:
        future = driver[cut : cut + cut_depth - 1]
        future_states, _ = fresh_boundary_states(future)
        future_prefix = future_states[:cut_depth]
        past_target = dual_preimage(words[cut], ("00",) * cut_depth)
        common = 0
        for actual, target in zip(future_prefix, past_target):
            if actual != target:
                break
            common += 1
        observed_run = _zero_run_from(pairs, cut, cut_depth)
        if common != observed_run:
            raise AssertionError(
                ("actual cut mismatch", cut, common, observed_run, future_prefix, past_target)
            )
        mismatch_histogram[common] += 1
        checked += 1

    runs: list[tuple[int, int, int]] = []
    start: int | None = None
    for index, pair in enumerate(pairs[:blocks] + ["END"]):
        if pair == "00" and start is None:
            start = index
        elif pair != "00" and start is not None:
            runs.append((start, index - 1, index - start))
            start = None
    longest = max(runs, key=lambda row: row[2], default=(-1, -1, 0))
    records: list[dict[str, int]] = []
    best = 0
    for start, end, length in runs:
        if length > best:
            best = length
            records.append(
                {
                    "length": length,
                    "start_block_zero_based": start,
                    "end_block_zero_based": end,
                }
            )

    return {
        "blocks": blocks,
        "cut_depth": cut_depth,
        "sampled_cuts_checked": checked,
        "truncated_match_length_histogram": {
            str(k): v for k, v in sorted(mismatch_histogram.items())
        },
        "longest_terminal_zero_run": {
            "length": longest[2],
            "start_block_zero_based": longest[0],
            "end_block_zero_based": longest[1],
        },
        "record_terminal_zero_runs": records,
        "exact_interpretation": (
            "at each checked cut, the forward terminal-zero run length equals "
            "the common-prefix length between the future boundary state word "
            "and the past dual zero target, truncated at cut_depth"
        ),
        "scope_warning": (
            "bounded cut checks do not prove that mismatches recur infinitely often"
        ),
        "all_checks_pass": True,
    }


def run_campaign(
    *,
    maximum_word_length: int = DEFAULT_WORD_LENGTH,
    maximum_driver_depth: int = DEFAULT_DRIVER_DEPTH,
    actual_blocks: int = DEFAULT_ACTUAL_BLOCKS,
    actual_cut_depth: int = DEFAULT_ACTUAL_CUT_DEPTH,
) -> dict[str, Any]:
    if not 0 <= maximum_word_length <= ABSOLUTE_WORD_LENGTH:
        raise ValueError("word length outside campaign cap")
    if not 0 <= maximum_driver_depth <= ABSOLUTE_DRIVER_DEPTH:
        raise ValueError("driver depth outside campaign cap")
    if not 1 <= actual_blocks <= ABSOLUTE_ACTUAL_BLOCKS:
        raise ValueError("actual block count outside campaign cap")
    if not 1 <= actual_cut_depth <= ABSOLUTE_ACTUAL_CUT_DEPTH:
        raise ValueError("actual cut depth outside campaign cap")

    payload: dict[str, Any] = {
        "factorization": verify_factorization(maximum_word_length, maximum_driver_depth),
        "unique_zero_target": verify_unique_zero_target(
            maximum_word_length, maximum_driver_depth + 1
        ),
        "actual_cut": verify_actual_cut(actual_blocks, actual_cut_depth),
        "exact_conclusions": {
            "past_future_cut": (
                "the future terminal-pair word is the dual action of the past "
                "accumulated word on a fresh state word generated solely by the "
                "future branch schedule"
            ),
            "zero_run_prefix_match": (
                "a zero run of length L is exactly a depth-L match between the "
                "future state word and the unique past preimage of 00^L"
            ),
            "remaining_target": (
                "prove that the two infinite boundary words mismatch at finite "
                "depth for infinitely many actual cuts"
            ),
        },
        "scientific_boundary": (
            "This campaign proves an exact all-depth factorization and cut criterion. "
            "It does not prove infinitely many resets, exclude period two, or solve "
            "Rule 30 center nonperiodicity."
        ),
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-dual-cut-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--word-length", type=int, default=DEFAULT_WORD_LENGTH)
    parser.add_argument("--driver-depth", type=int, default=DEFAULT_DRIVER_DEPTH)
    parser.add_argument("--actual-blocks", type=int, default=DEFAULT_ACTUAL_BLOCKS)
    parser.add_argument("--cut-depth", type=int, default=DEFAULT_ACTUAL_CUT_DEPTH)
    args = parser.parse_args()
    print(
        json.dumps(
            run_campaign(
                maximum_word_length=args.word_length,
                maximum_driver_depth=args.driver_depth,
                actual_blocks=args.actual_blocks,
                actual_cut_depth=args.cut_depth,
            ),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
