#!/usr/bin/env python3
"""Analyze the fixed phase and deletion recurrence of period-two zero islands.

For the complete accumulated inverse word G, write

    U_q(G) = (G|_11) p q,  q in {t,u},
    e(G) = G(11).

The exact transducer has the stronger column property that the leftmost emitted
section letter is determined only by the final pair e(G):

    00 -> t,  01 -> p,  10 -> u,  11 -> p.

If e(G)=00 and G=t^ell a B is normalized at its first non-t letter, then
a is p or u and

    U_q(G) = t^(ell+1) U_q(B).

Moreover a=p exactly when B(11)=11, and a=u exactly when B(11)=10.
The normalized word after the zero step therefore begins with the same phase a.
Consequently every consecutive zero island has a fixed p/u phase, and a final
zero tail would remain forever in one fixed terminal fiber.

The phase also has an arithmetic interpretation.  For x=K^{-1}(0), where K is
the normalized word, phase p gives even bit length and phase u gives odd bit
length.  The bounded campaigns below validate the implementation; they do not
prove that an infinite zero tail is impossible.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter
from typing import Any

LETTERS = ("t", "p", "u")
BRANCHES = ("t", "u")
PAIR_STATES = ("00", "01", "10", "11")
DEFAULT_WORD_LENGTH = 8
DEFAULT_DRIVER_DEPTH = 5
ABSOLUTE_WORD_LENGTH = 10
ABSOLUTE_DRIVER_DEPTH = 7

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
HEAD_BY_TERMINAL = {"00": "t", "01": "p", "10": "u", "11": "p"}
TAIL_TERMINAL_BY_PHASE = {"p": "11", "u": "10"}


def scan(word: str, start_pair: str = "11") -> tuple[str, str]:
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
    section, terminal = scan(word)
    return section + "p" + branch, terminal


def leading_t_order(word: str) -> int:
    return len(word) - len(word.lstrip("t"))


def normalize(word: str) -> str:
    return word[leading_t_order(word):]


def forward_generator(name: str, state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError("unknown generator")


def preimage_zero(word: str) -> int:
    state = 0
    for letter in word:
        state = forward_generator(letter, state)
    return state


def zero_decomposition(word: str) -> tuple[int, str, str]:
    """Return ell, phase, tail for a word with terminal pair 00."""
    _, terminal = scan(word)
    if terminal != "00":
        raise ValueError("word is not in the terminal-zero domain")
    ell = leading_t_order(word)
    normalized = word[ell:]
    if not normalized or normalized[0] not in ("p", "u"):
        raise AssertionError("terminal-zero word has no p/u phase")
    return ell, normalized[0], normalized[1:]


def verify_terminal_head(maximum_word_length: int) -> dict[str, Any]:
    cases = 0
    terminal_counts: Counter[str] = Counter()
    for length in range(maximum_word_length + 1):
        for letters in itertools.product(LETTERS, repeat=length):
            word = "".join(letters)
            section, terminal = scan(word)
            terminal_counts[terminal] += 1
            for branch in BRANCHES:
                updated, observed_terminal = block_update(word, branch)
                if observed_terminal != terminal:
                    raise AssertionError("terminal changed across identical scan")
                expected_head = HEAD_BY_TERMINAL[terminal]
                if not updated or updated[0] != expected_head:
                    raise AssertionError(
                        ("terminal-head code failed", word, branch, terminal, updated)
                    )
                if word and section[0] != expected_head:
                    raise AssertionError("section head is not terminal-coded")
                cases += 1
    return {
        "maximum_word_length": maximum_word_length,
        "word_branch_cases_checked": cases,
        "terminal_counts_before_branch_duplication": dict(sorted(terminal_counts.items())),
        "head_code": HEAD_BY_TERMINAL,
        "exact_identity": "head((G|_11)pq)=h(G(11))",
        "all_checks_pass": True,
    }


def verify_zero_deletion(maximum_word_length: int) -> dict[str, Any]:
    checked = 0
    phase_counts: Counter[str] = Counter()
    continuation_counts: Counter[str] = Counter()
    for length in range(maximum_word_length + 1):
        for letters in itertools.product(LETTERS, repeat=length):
            word = "".join(letters)
            _, terminal = scan(word)
            if terminal != "00":
                continue
            ell, phase, tail = zero_decomposition(word)
            expected_tail_terminal = TAIL_TERMINAL_BY_PHASE[phase]
            if scan(tail)[1] != expected_tail_terminal:
                raise AssertionError("phase/tail-terminal classification failed")
            phase_counts[phase] += 1

            for branch in BRANCHES:
                updated, _ = block_update(word, branch)
                tail_updated, _ = block_update(tail, branch)
                expected = "t" * (ell + 1) + tail_updated
                if updated != expected:
                    raise AssertionError(
                        ("zero deletion recurrence failed", word, branch, updated, expected)
                    )
                normalized_next = normalize(updated)
                if not normalized_next or normalized_next[0] != phase:
                    raise AssertionError("zero step did not propagate phase")
                if scan(updated)[1] == "00":
                    continuation_counts[phase] += 1
                    _, next_phase, _ = zero_decomposition(updated)
                    if next_phase != phase:
                        raise AssertionError("zero-island phase changed")
                checked += 1

    return {
        "maximum_word_length": maximum_word_length,
        "zero_word_branch_cases_checked": checked,
        "phase_counts_before_branch_duplication": dict(sorted(phase_counts.items())),
        "continuing_zero_cases": dict(sorted(continuation_counts.items())),
        "tail_terminal_by_phase": TAIL_TERMINAL_BY_PHASE,
        "exact_deletion": (
            "if G=t^ell a B and G(11)=00, then "
            "U_q(G)=t^(ell+1) U_q(B)"
        ),
        "phase_propagation": (
            "the normalized word after every zero output begins with the same "
            "phase a in {p,u}"
        ),
        "all_checks_pass": True,
    }


def verify_phase_parity(maximum_word_length: int) -> dict[str, Any]:
    checked = 0
    parity_counts: Counter[str] = Counter()
    for length in range(maximum_word_length + 1):
        for letters in itertools.product(LETTERS, repeat=length):
            word = "".join(letters)
            if scan(word)[1] != "00":
                continue
            _, phase, _ = zero_decomposition(word)
            normalized = normalize(word)
            state = preimage_zero(normalized)
            if state <= 0:
                raise AssertionError("normalized zero state is not positive")
            expected_parity = 0 if phase == "p" else 1
            observed_parity = state.bit_length() & 1
            if observed_parity != expected_parity:
                raise AssertionError(
                    ("phase parity failed", word, phase, state.bit_length())
                )
            parity_counts[f"{phase}:{observed_parity}"] += 1
            checked += 1
    return {
        "maximum_word_length": maximum_word_length,
        "zero_words_checked": checked,
        "phase_bit_length_parity": {"p": "even", "u": "odd"},
        "counts": dict(sorted(parity_counts.items())),
        "exact_reason": (
            "p(0)=3 has bit length 2, u(0)=1 has bit length 1, and every "
            "subsequent forward generator raises positive bit length by 2"
        ),
        "all_checks_pass": True,
    }


def verify_zero_island_drivers(
    maximum_word_length: int, maximum_driver_depth: int
) -> dict[str, Any]:
    checked_steps = 0
    surviving_prefixes = 0
    phase_survivors: Counter[str] = Counter()
    for length in range(maximum_word_length + 1):
        for letters in itertools.product(LETTERS, repeat=length):
            initial = "".join(letters)
            if scan(initial)[1] != "00":
                continue
            _, initial_phase, _ = zero_decomposition(initial)
            for depth in range(maximum_driver_depth + 1):
                for driver in itertools.product(BRANCHES, repeat=depth):
                    word = initial
                    survived = True
                    for branch in driver:
                        if scan(word)[1] != "00":
                            survived = False
                            break
                        _, phase, _ = zero_decomposition(word)
                        if phase != initial_phase:
                            raise AssertionError("phase changed inside zero island")
                        word, _ = block_update(word, branch)
                        checked_steps += 1
                    if survived and scan(word)[1] == "00":
                        _, phase, _ = zero_decomposition(word)
                        if phase != initial_phase:
                            raise AssertionError("final zero phase changed")
                        surviving_prefixes += 1
                        phase_survivors[phase] += 1
    return {
        "maximum_initial_word_length": maximum_word_length,
        "maximum_driver_depth": maximum_driver_depth,
        "zero_driver_steps_checked": checked_steps,
        "surviving_zero_prefixes": surviving_prefixes,
        "surviving_prefixes_by_phase": dict(sorted(phase_survivors.items())),
        "exact_conclusion": (
            "every finite consecutive-zero prefix remains in its initial p/u phase"
        ),
        "all_checks_pass": True,
    }


def run_campaign(
    *,
    maximum_word_length: int = DEFAULT_WORD_LENGTH,
    maximum_driver_depth: int = DEFAULT_DRIVER_DEPTH,
) -> dict[str, Any]:
    if not 0 <= maximum_word_length <= ABSOLUTE_WORD_LENGTH:
        raise ValueError("word length outside campaign cap")
    if not 0 <= maximum_driver_depth <= ABSOLUTE_DRIVER_DEPTH:
        raise ValueError("driver depth outside campaign cap")
    payload: dict[str, Any] = {
        "terminal_head": verify_terminal_head(maximum_word_length),
        "zero_deletion": verify_zero_deletion(maximum_word_length),
        "phase_parity": verify_phase_parity(maximum_word_length),
        "zero_island_drivers": verify_zero_island_drivers(
            min(maximum_word_length, 5), maximum_driver_depth
        ),
        "exact_conclusions": {
            "terminal_head_code": (
                "the terminal pair determines the next complete-word head letter"
            ),
            "fixed_zero_phase": (
                "every consecutive terminal-zero island has one fixed p/u phase"
            ),
            "arithmetic_phase": (
                "the phase is exactly the parity of the normalized ordinary "
                "state's bit length"
            ),
            "final_tail_reduction": (
                "a final zero tail must remain forever in one of two fixed "
                "terminal fibers, with one phase letter deleted per block"
            ),
            "remaining_target": (
                "exclude infinite actual-fringe-driven orbits in both fixed "
                "terminal fibers"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-zero-phase-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--word-length", type=int, default=DEFAULT_WORD_LENGTH)
    parser.add_argument("--driver-depth", type=int, default=DEFAULT_DRIVER_DEPTH)
    args = parser.parse_args()
    print(
        json.dumps(
            run_campaign(
                maximum_word_length=args.word_length,
                maximum_driver_depth=args.driver_depth,
            ),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
