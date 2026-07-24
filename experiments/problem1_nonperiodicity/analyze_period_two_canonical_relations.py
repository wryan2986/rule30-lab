#!/usr/bin/env python3
"""Analyze canonical arithmetic relations for period-two witnesses.

For a normalized inverse word, different words can represent the same ordinary
state x=G^{-1}(0).  Three exact state-conditioned relations give a finite
canonical-language quotient:

    odd x:       p(x)=u(x)
    x == 1 mod4: up(x)=tt(x)
    x == 2 mod4: ut(x)=tp(x)

With alphabet order t<u<p, each relation strictly lowers the word while
preserving its length and arithmetic state.  Every word therefore reduces to a
representative accepted by a six-state automaton.  Its dominant growth root is
the largest root of lambda^3-2 lambda^2-lambda+1, approximately 2.24698.  This
improves the previous Pell arithmetic-image bound 1+sqrt(2).

The bounded campaigns validate the implementation and compare exact arithmetic
state counts to the canonical automaton.  They do not prove divergence on the
actual zero-initialized fringe schedule.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from typing import Any

LETTERS = ("t", "u", "p")
PHASE_START = {"p": 3, "u": 1}
DEFAULT_REWRITE_LENGTH = 9
DEFAULT_STATE_LENGTH = 18
ABSOLUTE_REWRITE_LENGTH = 11
ABSOLUTE_STATE_LENGTH = 22
ORDER = {"t": 0, "u": 1, "p": 2}

# (current arithmetic residue mod 4, one-step pending prohibition)
# pending 0: none; 1: forbid p; 2: forbid t.
AUTOMATON_STATES = ((0, 0), (1, 0), (2, 0), (2, 1), (3, 0), (3, 2))
STATE_INDEX = {state: index for index, state in enumerate(AUTOMATON_STATES)}
ADJACENCY_MATRIX = (
    (1, 1, 0, 0, 1, 0),
    (0, 0, 0, 1, 1, 0),
    (0, 1, 1, 0, 0, 1),
    (0, 0, 1, 0, 0, 1),
    (1, 1, 0, 0, 0, 0),
    (1, 0, 0, 0, 0, 0),
)


def forward_t(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    return state ^ ((state << 1) | (state << 2))


def forward_generator(name: str, state: int) -> int:
    stepped = forward_t(state)
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError("unknown generator")


def apply_word(state: int, word: str) -> int:
    for letter in word:
        state = forward_generator(letter, state)
    return state


def residue_transition(residue: int, letter: str) -> int:
    return forward_generator(letter, residue) & 3


def lex_key(word: str) -> tuple[int, ...]:
    return tuple(ORDER[letter] for letter in word)


def first_rewrite(start: int, word: str) -> tuple[str, tuple[int, str]] | None:
    state = start
    for index, letter in enumerate(word):
        if state & 1 and letter == "p":
            return (
                word[:index] + "u" + word[index + 1 :],
                (index, "odd-p-to-u"),
            )
        if index + 1 < len(word) and state & 3 == 1 and word[index : index + 2] == "up":
            return (
                word[:index] + "tt" + word[index + 2 :],
                (index, "one-up-to-tt"),
            )
        if index + 1 < len(word) and state & 3 == 2 and word[index : index + 2] == "ut":
            return (
                word[:index] + "tp" + word[index + 2 :],
                (index, "two-ut-to-tp"),
            )
        state = forward_generator(letter, state)
    return None


def reduce_word(start: int, word: str) -> tuple[str, int]:
    steps = 0
    while True:
        rewrite = first_rewrite(start, word)
        if rewrite is None:
            return word, steps
        updated, _ = rewrite
        if len(updated) != len(word) or not lex_key(updated) < lex_key(word):
            raise AssertionError("rewrite did not strictly lower the word")
        if apply_word(start, updated) != apply_word(start, word):
            raise AssertionError("rewrite changed the arithmetic state")
        word = updated
        steps += 1


def automaton_step(
    state: tuple[int, int], letter: str
) -> tuple[int, int] | None:
    residue, pending = state
    if residue & 1 and letter == "p":
        return None
    if pending == 1 and letter == "p":
        return None
    if pending == 2 and letter == "t":
        return None

    next_residue = residue_transition(residue, letter)
    next_pending = (
        1
        if residue == 1 and letter == "u"
        else 2
        if residue == 2 and letter == "u"
        else 0
    )
    result = (next_residue, next_pending)
    if result not in STATE_INDEX:
        raise AssertionError("unexpected canonical automaton state")
    return result


def is_canonical(start: int, word: str) -> bool:
    state = (start & 3, 0)
    for letter in word:
        next_state = automaton_step(state, letter)
        if next_state is None:
            return False
        state = next_state
    return True


def matrix_count(start: int, continuation_length: int) -> int:
    vector = [0] * len(AUTOMATON_STATES)
    vector[STATE_INDEX[(start & 3, 0)]] = 1
    for _ in range(continuation_length):
        updated = [0] * len(AUTOMATON_STATES)
        for source, count in enumerate(vector):
            for target, multiplicity in enumerate(ADJACENCY_MATRIX[source]):
                updated[target] += count * multiplicity
        vector = updated
    return sum(vector)


def verify_conditional_relations(limit: int = 1 << 16) -> dict[str, Any]:
    checks = 0
    for state in range(limit):
        if state & 1:
            if forward_generator("p", state) != forward_generator("u", state):
                raise AssertionError("odd p/u collision failed")
            checks += 1
        if state & 3 == 1:
            if apply_word(state, "up") != apply_word(state, "tt"):
                raise AssertionError("mod-four up/tt relation failed")
            checks += 1
        if state & 3 == 2:
            if apply_word(state, "ut") != apply_word(state, "tp"):
                raise AssertionError("mod-four ut/tp relation failed")
            checks += 1
    return {
        "states_checked": limit,
        "conditional_identity_checks": checks,
        "all_checks_pass": True,
    }


def verify_reduction(maximum_length: int) -> dict[str, Any]:
    words_checked = 0
    words_changed = 0
    maximum_steps = 0
    for phase, phase_state in PHASE_START.items():
        for length in range(1, maximum_length + 1):
            for suffix in itertools.product(LETTERS, repeat=length - 1):
                word = phase + "".join(suffix)
                reduced, steps = reduce_word(0, word)
                if apply_word(0, reduced) != apply_word(0, word):
                    raise AssertionError("reduction changed the full normalized state")
                if not is_canonical(phase_state, reduced[1:]):
                    raise AssertionError("reduction did not reach the automaton language")
                words_checked += 1
                words_changed += int(steps > 0)
                maximum_steps = max(maximum_steps, steps)
    return {
        "maximum_normalized_length": maximum_length,
        "words_checked": words_checked,
        "words_changed": words_changed,
        "maximum_rewrite_steps": maximum_steps,
        "all_checks_pass": True,
    }


def verify_arithmetic_state_counts(maximum_length: int) -> dict[str, Any]:
    current = {phase: {start} for phase, start in PHASE_START.items()}
    rows: list[dict[str, Any]] = []
    for length in range(1, maximum_length + 1):
        if length > 1:
            for phase in current:
                successors: set[int] = set()
                for state in current[phase]:
                    successors.update(
                        forward_generator(letter, state) for letter in LETTERS
                    )
                current[phase] = successors

        row: dict[str, Any] = {"length": length}
        for phase, start in PHASE_START.items():
            actual = len(current[phase])
            bound = matrix_count(start, length - 1)
            if actual > bound:
                raise AssertionError("canonical automaton bound failed")
            row[phase] = {
                "distinct_arithmetic_states": actual,
                "canonical_automaton_bound": bound,
            }
        rows.append(row)
    return {"rows": rows, "all_checks_pass": True}


def dominant_root() -> float:
    low, high = 2.0, 2.5
    for _ in range(100):
        middle = (low + high) / 2
        value = middle**3 - 2 * middle**2 - middle + 1
        if value < 0:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def run_campaign(
    rewrite_length: int = DEFAULT_REWRITE_LENGTH,
    state_length: int = DEFAULT_STATE_LENGTH,
) -> dict[str, Any]:
    if not 1 <= rewrite_length <= ABSOLUTE_REWRITE_LENGTH:
        raise ValueError("rewrite length outside campaign cap")
    if not 1 <= state_length <= ABSOLUTE_STATE_LENGTH:
        raise ValueError("state length outside campaign cap")

    root = dominant_root()
    rate = math.log(2) / math.log(root)
    payload: dict[str, Any] = {
        "conditional_relations": verify_conditional_relations(),
        "canonical_reduction": verify_reduction(rewrite_length),
        "canonical_automaton": {
            "states": [list(state) for state in AUTOMATON_STATES],
            "adjacency_matrix": [list(row) for row in ADJACENCY_MATRIX],
            "characteristic_polynomial": (
                "lambda^3 (lambda^3-2 lambda^2-lambda+1)"
            ),
            "dominant_root": root,
            "almost_sure_rate_log_root_2": rate,
        },
        "arithmetic_state_counts": verify_arithmetic_state_counts(state_length),
        "exact_conclusions": {
            "canonical_representatives": (
                "every normalized arithmetic witness has a same-length "
                "representative accepted by the six-state automaton"
            ),
            "growth_bound": (
                "phase arithmetic-image growth is O(lambda^N), where lambda is "
                "the largest root of lambda^3-2 lambda^2-lambda+1"
            ),
            "improved_generic_rate": (
                "Bernoulli-almost surely liminf kappa_a(q,L)/L is at least "
                "log(2)/log(lambda)"
            ),
            "remaining_target": (
                "prove divergence for the one deterministic zero-initialized "
                "fringe schedule"
            ),
        },
        "scope_warning": (
            "this is a generic arithmetic quotient and does not prove "
            "actual-orbit divergence"
        ),
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-canonical-relations-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--rewrite-length", type=int, default=DEFAULT_REWRITE_LENGTH
    )
    parser.add_argument("--state-length", type=int, default=DEFAULT_STATE_LENGTH)
    args = parser.parse_args()
    print(
        json.dumps(
            run_campaign(args.rewrite_length, args.state_length), sort_keys=True
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
