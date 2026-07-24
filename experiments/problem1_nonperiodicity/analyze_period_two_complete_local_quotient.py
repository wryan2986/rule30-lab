#!/usr/bin/env python3
"""Build complete bounded-span canonical quotients for period-two witnesses.

For a common block length m, two generator words can differ only in the lowest
2m output bits, and those bits depend only on the lowest 2m input bits. Thus
all same-length arithmetic identities are decided by one finite table modulo
4**m.

For a configured span s, this analyzer replaces every block of length at most s
by the lexicographically least equal block at its exact starting residue. The
resulting irreducible words form a finite-state language. Its growth bounds the
number of distinct arithmetic witnesses.

The Python implementation is capped at span four. The companion C++ analyzer
constructs the span-five graph and emits the exact below-binary path-count
certificate. These generic quotients do not prove divergence on the one
zero-initialized Rule 30 fringe schedule.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any, Iterable

LETTERS = ("t", "u", "p")
LETTER_INDEX = {letter: index for index, letter in enumerate(LETTERS)}
PHASE_START = {"p": 3, "u": 1}
DEFAULT_SPAN = 3
ABSOLUTE_SPAN = 4
DEFAULT_COUNT_LENGTH = 14
ABSOLUTE_COUNT_LENGTH = 18


def forward_t(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    return state ^ ((state << 1) | (state << 2))


def forward_generator(letter: str, state: int) -> int:
    stepped = forward_t(state)
    if letter == "t":
        return stepped
    if letter == "u":
        return stepped ^ 1
    if letter == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError("unknown generator")


def apply_word(state: int, word: Iterable[str]) -> int:
    for letter in word:
        state = forward_generator(letter, state)
    return state


def word_index(word: str) -> int:
    value = 0
    for letter in word:
        value = 3 * value + LETTER_INDEX[letter]
    return value


def words_of_length(length: int) -> tuple[str, ...]:
    return tuple("".join(word) for word in itertools.product(LETTERS, repeat=length))


def complete_local_minima(span: int) -> dict[tuple[int, int, str], str]:
    """Return every lex-min same-length representative through ``span``."""
    if not 1 <= span <= ABSOLUTE_SPAN:
        raise ValueError("span outside Python campaign cap")
    full_modulus = 1 << (2 * span)
    table: dict[tuple[int, int, str], str] = {}
    for length in range(1, span + 1):
        modulus = 1 << (2 * length)
        words = words_of_length(length)
        residue_minima: list[dict[int, str]] = []
        for residue in range(modulus):
            minima: dict[int, str] = {}
            for word in words:
                output = apply_word(residue, word) & (modulus - 1)
                minima.setdefault(output, word)
            residue_minima.append(minima)
        for lifted_residue in range(full_modulus):
            residue = lifted_residue & (modulus - 1)
            minima = residue_minima[residue]
            for word in words:
                output = apply_word(residue, word) & (modulus - 1)
                table[(lifted_residue, length, word)] = minima[output]
    return table


def inverse_tables(modulus: int) -> dict[str, tuple[int, ...]]:
    result: dict[str, tuple[int, ...]] = {}
    for letter in LETTERS:
        inverse = [-1] * modulus
        for state in range(modulus):
            image = forward_generator(letter, state) & (modulus - 1)
            if inverse[image] != -1:
                raise AssertionError("generator is not invertible modulo power of two")
            inverse[image] = state
        if any(value < 0 for value in inverse):
            raise AssertionError("generator permutation is incomplete")
        result[letter] = tuple(inverse)
    return result


def invert_word(residue: int, word: str, inverse: dict[str, tuple[int, ...]]) -> int:
    for letter in reversed(word):
        residue = inverse[letter][residue]
    return residue


@dataclass(frozen=True, order=True)
class AutomatonState:
    residue: int
    history: str


class CompleteLocalAutomaton:
    def __init__(self, span: int):
        if not 1 <= span <= ABSOLUTE_SPAN:
            raise ValueError("span outside Python campaign cap")
        self.span = span
        self.modulus = 1 << (2 * span)
        self.mask = self.modulus - 1
        self.minima = complete_local_minima(span)
        self.inverse = inverse_tables(self.modulus)
        self.phase_starts = {
            phase: AutomatonState(state & self.mask, phase)
            for phase, state in PHASE_START.items()
        }
        self.states, self.transitions = self._build_reachable_graph()
        self.index = {state: index for index, state in enumerate(self.states)}

    def step(self, state: AutomatonState, letter: str) -> AutomatonState | None:
        if letter not in LETTER_INDEX:
            raise ValueError("unknown generator")
        new_residue = forward_generator(letter, state.residue) & self.mask
        full_history = state.history + letter
        for length in range(1, min(self.span, len(full_history)) + 1):
            block = full_history[-length:]
            start = invert_word(new_residue, block, self.inverse)
            if self.minima[(start, length, block)] != block:
                return None
        history_width = max(0, self.span - 1)
        new_history = full_history[-history_width:] if history_width else ""
        return AutomatonState(new_residue, new_history)

    def _build_reachable_graph(
        self,
    ) -> tuple[tuple[AutomatonState, ...], dict[AutomatonState, tuple[AutomatonState | None, ...]]]:
        reached = set(self.phase_starts.values())
        queue: deque[AutomatonState] = deque(reached)
        transitions: dict[AutomatonState, tuple[AutomatonState | None, ...]] = {}
        while queue:
            state = queue.popleft()
            images = tuple(self.step(state, letter) for letter in LETTERS)
            transitions[state] = images
            for image in images:
                if image is not None and image not in reached:
                    reached.add(image)
                    queue.append(image)
        states = tuple(sorted(reached))
        for state in states:
            transitions.setdefault(state, tuple(self.step(state, letter) for letter in LETTERS))
        return states, transitions

    def accepted(self, phase: str, suffix: str) -> bool:
        state = self.phase_starts[phase]
        for letter in suffix:
            image = self.step(state, letter)
            if image is None:
                return False
            state = image
        return True

    def count_by_phase(self, maximum_length: int) -> list[dict[str, int]]:
        if maximum_length < 1:
            raise ValueError("maximum length must be positive")
        current = {phase: {start: 1} for phase, start in self.phase_starts.items()}
        rows: list[dict[str, int]] = []
        for length in range(1, maximum_length + 1):
            if length > 1:
                for phase in current:
                    updated: defaultdict[AutomatonState, int] = defaultdict(int)
                    for state, count in current[phase].items():
                        for image in self.transitions[state]:
                            if image is not None:
                                updated[image] += count
                    current[phase] = dict(updated)
            rows.append({
                "length": length,
                **{phase: sum(row.values()) for phase, row in current.items()},
            })
        return rows

    def spectral_radius(self, iterations: int = 300) -> float:
        vector = [1.0] * len(self.states)
        for _ in range(iterations):
            updated = [0.0] * len(self.states)
            for source, state in enumerate(self.states):
                updated[source] = sum(
                    vector[self.index[image]]
                    for image in self.transitions[state]
                    if image is not None
                )
            scale = max(updated)
            if scale == 0:
                return 0.0
            vector = [value / scale for value in updated]
        ratios = []
        for source, state in enumerate(self.states):
            numerator = sum(
                vector[self.index[image]]
                for image in self.transitions[state]
                if image is not None
            )
            if vector[source] > 1e-15:
                ratios.append(numerator / vector[source])
        return (min(ratios) + max(ratios)) / 2


def reduce_word(word: str, span: int, minima: dict[tuple[int, int, str], str]) -> tuple[str, int]:
    """Reduce one normalized word by the first available local replacement."""
    if not word or word[0] not in PHASE_START:
        raise ValueError("word must be normalized and begin with p or u")
    full_mask = (1 << (2 * span)) - 1
    steps = 0
    while True:
        state = 0
        changed = False
        for index in range(len(word)):
            for length in range(1, min(span, len(word) - index) + 1):
                block = word[index : index + length]
                minimum = minima[(state & full_mask, length, block)]
                if minimum != block:
                    candidate = word[:index] + minimum + word[index + length :]
                    if word_index(candidate) >= word_index(word):
                        raise AssertionError("local replacement did not lower the word")
                    if apply_word(0, candidate) != apply_word(0, word):
                        raise AssertionError("local replacement changed arithmetic state")
                    word = candidate
                    steps += 1
                    changed = True
                    break
            if changed:
                break
            state = forward_generator(word[index], state)
        if not changed:
            return word, steps


def verify_locality_tables(span: int) -> dict[str, Any]:
    minima = complete_local_minima(span)
    checks = 0
    nontrivial = 0
    for length in range(1, span + 1):
        modulus = 1 << (2 * length)
        words = words_of_length(length)
        for residue in range(modulus):
            for word in words:
                minimum = minima[(residue, length, word)]
                if apply_word(residue, word) & (modulus - 1) != apply_word(
                    residue, minimum
                ) & (modulus - 1):
                    raise AssertionError("local minimum table is not output preserving")
                checks += 1
                nontrivial += int(minimum != word)
    return {
        "span": span,
        "finite_table_checks": checks,
        "nonminimal_entries": nontrivial,
        "locality_lemma": (
            "equal-length-m word differences are confined below bit 2m, so the "
            "table modulo 4^m is an all-width identity table"
        ),
        "all_checks_pass": True,
    }


def verify_reduction(span: int, maximum_length: int) -> dict[str, Any]:
    minima = complete_local_minima(span)
    automaton = CompleteLocalAutomaton(span)
    checked = changed = maximum_steps = 0
    for length in range(1, maximum_length + 1):
        for phase in PHASE_START:
            for suffix in itertools.product(LETTERS, repeat=length - 1):
                word = phase + "".join(suffix)
                reduced, steps = reduce_word(word, span, minima)
                if not automaton.accepted(reduced[0], reduced[1:]):
                    raise AssertionError("reduced word is not accepted")
                checked += 1
                changed += int(steps > 0)
                maximum_steps = max(maximum_steps, steps)
    return {
        "maximum_normalized_length": maximum_length,
        "words_checked": checked,
        "words_changed": changed,
        "maximum_rewrite_steps": maximum_steps,
        "all_checks_pass": True,
    }


def exact_arithmetic_counts(maximum_length: int) -> list[dict[str, int]]:
    current = {phase: {state} for phase, state in PHASE_START.items()}
    rows: list[dict[str, int]] = []
    for length in range(1, maximum_length + 1):
        if length > 1:
            for phase in current:
                current[phase] = {
                    forward_generator(letter, state)
                    for state in current[phase]
                    for letter in LETTERS
                }
        rows.append({
            "length": length,
            **{phase: len(states) for phase, states in current.items()},
        })
    return rows


def run_campaign(*, span: int = DEFAULT_SPAN, count_length: int = DEFAULT_COUNT_LENGTH) -> dict[str, Any]:
    if not 1 <= span <= ABSOLUTE_SPAN:
        raise ValueError("span outside Python campaign cap")
    if not 1 <= count_length <= ABSOLUTE_COUNT_LENGTH:
        raise ValueError("count length outside campaign cap")
    automaton = CompleteLocalAutomaton(span)
    canonical_counts = automaton.count_by_phase(count_length)
    arithmetic_counts = exact_arithmetic_counts(count_length)
    for canonical, arithmetic in zip(canonical_counts, arithmetic_counts, strict=True):
        for phase in PHASE_START:
            if arithmetic[phase] > canonical[phase]:
                raise AssertionError("canonical language does not bound arithmetic image")
    radius = automaton.spectral_radius()
    payload: dict[str, Any] = {
        "span": span,
        "modulus": automaton.modulus,
        "reachable_automaton_states": len(automaton.states),
        "spectral_radius_approx": radius,
        "generic_complexity_rate_approx": math.log(2) / math.log(radius),
        "locality_tables": verify_locality_tables(span),
        "reduction_checks": verify_reduction(span, min(8, count_length)),
        "canonical_counts": canonical_counts,
        "arithmetic_counts": arithmetic_counts,
        "exact_conclusions": {
            "complete_local_reduction": (
                "every normalized word has a same-length representative whose every "
                "block through the configured span is lex-minimal at its exact residue"
            ),
            "regular_language_bound": (
                "the fixed-span irreducible language is finite-state and bounds the "
                "fixed-phase arithmetic image"
            ),
            "remaining_target": (
                "the quotient is generic and does not exclude the deterministic "
                "zero-initialized fringe survivor"
            ),
        },
        "scope_warning": (
            "the Python campaign is capped at span four; the companion C++ campaign "
            "provides the span-five below-binary certificate"
        ),
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-complete-local-quotient-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--span", type=int, default=DEFAULT_SPAN)
    parser.add_argument("--count-length", type=int, default=DEFAULT_COUNT_LENGTH)
    args = parser.parse_args()
    print(json.dumps(run_campaign(span=args.span, count_length=args.count_length), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
