#!/usr/bin/env python3
"""Analyze minimum finite-word complexity for period-two zero targets.

For a future branch prefix of length L-1, let V_L be its fresh boundary state
word.  For phase a in {p,u}, kappa_a(L) is the minimum length of a normalized
inverse word beginning with a whose dual action sends V_L to 00^L.

The all-scale theorem is:

* kappa_a(L) is nondecreasing;
* one finite phase-a word works at every depth iff kappa_a(L) is bounded;
* at most (3^N-1)/2 schedule prefixes have kappa_a(L) <= N;
* consequently almost every schedule satisfies
      liminf kappa_a(L)/L >= log(2)/log(3).

Finite Schreier-graph campaigns validate shortest witnesses for the actual
zero-initialized fringe schedule.  They do not prove divergence on that one
exceptional schedule.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import deque
from typing import Any, Iterable

LETTERS = ("t", "p", "u")
BRANCHES = ("t", "u")
PHASES = ("p", "u")
PAIR_STATES = ("00", "01", "10", "11")
DEFAULT_DEPTH = 9
ABSOLUTE_DEPTH = 10

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
    if start_pair not in PAIR_STATES:
        raise ValueError("unknown pair state")
    if any(letter not in LETTERS for letter in word):
        raise ValueError("word contains an unknown generator")
    output = [""] * len(word)
    state = start_pair
    for index in range(len(word) - 1, -1, -1):
        output[index], state = TRANSITIONS[(state, word[index])]
    return "".join(output), state


def dual_image(word: str, state_word: Iterable[str]) -> tuple[str, ...]:
    current = word
    output: list[str] = []
    for state in state_word:
        current, image = scan(current, state)
        output.append(image)
    return tuple(output)


def block_update(word: str, branch: str) -> tuple[str, str]:
    if branch not in BRANCHES:
        raise ValueError("branch must be t or u")
    section, terminal = scan(word)
    return section + "p" + branch, terminal


def fresh_boundary_prefix(branches: Iterable[str]) -> tuple[str, ...]:
    driver = tuple(branches)
    word = ""
    states: list[str] = []
    for branch in driver + (None,):
        _, terminal = scan(word)
        states.append(terminal)
        if branch is not None:
            word, _ = block_update(word, branch)
    return tuple(states)


def fringe_step(state: int) -> int:
    if state < 0:
        raise ValueError("fringe state must be nonnegative")
    packed = 1 + 2 * state
    odd = packed ^ ((packed >> 1) | (packed >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def actual_driver(length: int) -> tuple[str, ...]:
    state = 0
    output: list[str] = []
    for _ in range(length):
        output.append("u" if state & 3 == 0 else "t")
        state = fringe_step(state)
    return tuple(output)


def level_states(depth: int) -> list[tuple[str, ...]]:
    return list(itertools.product(PAIR_STATES, repeat=depth))


def generator_permutation(
    letter: str, states: list[tuple[str, ...]]
) -> list[int]:
    index = {state: position for position, state in enumerate(states)}
    permutation = [index[dual_image(letter, state)] for state in states]
    if sorted(permutation) != list(range(len(states))):
        raise AssertionError("dual generator is not a permutation")
    return permutation


def reverse_shortest_witnesses(
    depth: int, target: tuple[str, ...]
) -> dict[tuple[str, ...], str]:
    """Shortest positive words sending each depth state to target.

    If source --letter--> current and suffix sends current to target, then
    suffix+letter sends source to target because the rightmost letter acts first.
    """
    states = level_states(depth)
    index = {state: position for position, state in enumerate(states)}
    inverse_maps: dict[str, list[int]] = {}
    for letter in LETTERS:
        permutation = generator_permutation(letter, states)
        inverse = [0] * len(permutation)
        for source, image in enumerate(permutation):
            inverse[image] = source
        inverse_maps[letter] = inverse

    witnesses: dict[tuple[str, ...], str] = {target: ""}
    queue: deque[tuple[str, ...]] = deque([target])
    while queue:
        current = queue.popleft()
        suffix = witnesses[current]
        current_index = index[current]
        for letter in LETTERS:
            predecessor = states[inverse_maps[letter][current_index]]
            if predecessor in witnesses:
                continue
            witnesses[predecessor] = suffix + letter
            queue.append(predecessor)
    if len(witnesses) != len(states):
        raise AssertionError("positive dual graph is not connected to target")
    return witnesses


def phase_input_target(phase: str, depth: int) -> tuple[str, ...]:
    if phase not in PHASES:
        raise ValueError("phase must be p or u")
    zero = ("00",) * depth
    matches = [
        state
        for state in level_states(depth)
        if dual_image(phase, state) == zero
    ]
    if len(matches) != 1:
        raise AssertionError("phase generator has no unique zero preimage")
    return matches[0]


def forward_shortest_targets(
    source: tuple[str, ...], targets: dict[str, tuple[str, ...]]
) -> dict[str, str]:
    """Return shortest positive words sending source to each named target."""
    target_names: dict[tuple[str, ...], list[str]] = {}
    for name, target in targets.items():
        target_names.setdefault(target, []).append(name)
    found: dict[str, str] = {}
    queue: deque[tuple[str, ...]] = deque([source])
    parent: dict[tuple[str, ...], tuple[tuple[str, ...], str]] = {}
    visited = {source}

    def reconstruct(state: tuple[str, ...]) -> str:
        letters: list[str] = []
        while state != source:
            previous, letter = parent[state]
            letters.append(letter)
            state = previous
        return "".join(letters)

    if source in target_names:
        for name in target_names[source]:
            found[name] = ""
    while queue and len(found) < len(targets):
        current = queue.popleft()
        for letter in LETTERS:
            image = dual_image(letter, current)
            if image in visited:
                continue
            visited.add(image)
            parent[image] = (current, letter)
            queue.append(image)
            if image in target_names:
                word = reconstruct(image)
                for name in target_names[image]:
                    found[name] = word
    if len(found) != len(targets):
        raise AssertionError("not every target was reached")
    return found


def witness_row(
    depth: int, boundary: tuple[str, ...]
) -> dict[str, Any]:
    if len(boundary) != depth:
        raise ValueError("boundary depth mismatch")
    zero = ("00",) * depth
    targets = {"zero": zero}
    targets.update({phase: phase_input_target(phase, depth) for phase in PHASES})
    suffixes = forward_shortest_targets(boundary, targets)

    unrestricted = suffixes["zero"]
    if not unrestricted or unrestricted[0] not in PHASES:
        raise AssertionError("shortest nonempty zero witness is not normalized")
    if dual_image(unrestricted, boundary) != zero:
        raise AssertionError("unrestricted witness failed")

    phase_rows: dict[str, Any] = {}
    for phase in PHASES:
        word = phase + suffixes[phase]
        if dual_image(word, boundary) != zero:
            raise AssertionError("phase witness failed")
        phase_rows[phase] = {
            "minimum_normalized_length": len(word),
            "witness": word,
            "witness_sha256": hashlib.sha256(word.encode()).hexdigest(),
        }

    if len(unrestricted) != min(
        row["minimum_normalized_length"] for row in phase_rows.values()
    ):
        raise AssertionError("unrestricted and phase minima disagree")
    return {
        "depth": depth,
        "boundary_prefix": list(boundary),
        "minimum_normalized_length": len(unrestricted),
        "witness": unrestricted,
        "witness_sha256": hashlib.sha256(unrestricted.encode()).hexdigest(),
        "by_phase": phase_rows,
    }


def verify_monotonicity(rows: list[dict[str, Any]]) -> None:
    for key in (None,) + PHASES:
        values = [
            row["minimum_normalized_length"]
            if key is None
            else row["by_phase"][key]["minimum_normalized_length"]
            for row in rows
        ]
        if values != sorted(values):
            raise AssertionError(("witness complexity decreased", key, values))


def verify_counting_bound(maximum_depth: int) -> dict[str, Any]:
    checked_rows: list[dict[str, Any]] = []
    for depth in range(1, min(maximum_depth, 6) + 1):
        phase_maps = {
            phase: reverse_shortest_witnesses(
                depth, phase_input_target(phase, depth)
            )
            for phase in PHASES
        }
        boundaries = [
            fresh_boundary_prefix(driver)
            for driver in itertools.product(BRANCHES, repeat=depth - 1)
        ]
        if len(set(boundaries)) != len(boundaries):
            raise AssertionError("future boundary coding is not injective")
        for limit in range(1, 2 * depth + 2):
            phase_counts = {
                phase: sum(
                    1
                    for boundary in boundaries
                    if 1 + len(phase_maps[phase][boundary]) <= limit
                )
                for phase in PHASES
            }
            phase_bound = (3**limit - 1) // 2
            if any(count > phase_bound for count in phase_counts.values()):
                raise AssertionError("phase counting bound failed")
            either_count = sum(
                1
                for boundary in boundaries
                if min(
                    1 + len(phase_maps[phase][boundary])
                    for phase in PHASES
                )
                <= limit
            )
            if either_count > 3**limit - 1:
                raise AssertionError("two-phase counting bound failed")
        checked_rows.append(
            {
                "depth": depth,
                "driver_prefixes": len(boundaries),
                "largest_limit_checked": 2 * depth + 1,
            }
        )
    return {
        "checked_rows": checked_rows,
        "phase_bound": "# {drivers: kappa_a(L)<=N} <= (3^N-1)/2",
        "either_phase_bound": "# {drivers: kappa(L)<=N} <= 3^N-1",
        "all_checks_pass": True,
    }


def run_campaign(maximum_depth: int = DEFAULT_DEPTH) -> dict[str, Any]:
    if not 1 <= maximum_depth <= ABSOLUTE_DEPTH:
        raise ValueError("depth outside campaign cap")
    driver = actual_driver(maximum_depth - 1)
    full_boundary = fresh_boundary_prefix(driver)
    rows = [
        witness_row(depth, full_boundary[:depth])
        for depth in range(1, maximum_depth + 1)
    ]
    verify_monotonicity(rows)

    payload: dict[str, Any] = {
        "maximum_depth": maximum_depth,
        "actual_driver_prefix": "".join(driver),
        "actual_boundary_rows": rows,
        "counting_checks": verify_counting_bound(maximum_depth),
        "exact_conclusions": {
            "monotonicity": "kappa_a(q,L+1) >= kappa_a(q,L)",
            "boundedness_criterion": (
                "a finite normalized phase-a word kills the full infinite boundary "
                "iff sup_L kappa_a(q,L) is finite"
            ),
            "counting_bound": (
                "at depth L, at most (3^N-1)/2 schedule prefixes have "
                "phase-a witness complexity at most N"
            ),
            "almost_sure_linear_bound": (
                "for Bernoulli-almost every schedule and each phase a, "
                "liminf kappa_a(q,L)/L >= log(2)/log(3)"
            ),
            "remaining_target": (
                "prove kappa_p or kappa_u diverges on the one exact "
                "zero-initialized fringe schedule"
            ),
        },
        "linear_rate_log3_2": math.log(2) / math.log(3),
        "scope_warning": (
            "the depth campaign is finite and does not prove divergence for the actual schedule"
        ),
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-witness-complexity-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--depth", type=int, default=DEFAULT_DEPTH)
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.depth), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
