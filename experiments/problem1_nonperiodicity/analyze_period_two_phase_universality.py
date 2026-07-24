#!/usr/bin/env python3
"""Prove finite-depth driver universality in both period-two zero phases."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, deque
from typing import Any, Iterable

LETTERS = ("t", "p", "u")
BRANCHES = ("t", "u")
PAIR_STATES = ("00", "01", "10", "11")
PHASES = ("p", "u")
DEFAULT_DEPTH = 7
ABSOLUTE_DEPTH = 7

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
    current = ""
    states: list[str] = []
    for branch in driver + (None,):
        _, terminal = scan(current)
        states.append(terminal)
        if branch is not None:
            current, _ = block_update(current, branch)
    return tuple(states)


def coupled_outputs(word: str, branches: Iterable[str]) -> tuple[str, ...]:
    driver = tuple(branches)
    current = word
    outputs: list[str] = []
    for branch in driver + (None,):
        _, terminal = scan(current)
        outputs.append(terminal)
        if branch is not None:
            current, _ = block_update(current, branch)
    return tuple(outputs)


def normalized_phase(word: str) -> str:
    normalized = word.lstrip("t")
    if not normalized or normalized[0] not in PHASES:
        raise ValueError("word has no p/u normalized phase")
    return normalized[0]


def generator_permutation(
    letter: str, depth: int
) -> tuple[list[tuple[str, ...]], list[int]]:
    states = list(itertools.product(PAIR_STATES, repeat=depth))
    index = {state: position for position, state in enumerate(states)}
    permutation = [index[dual_image(letter, state)] for state in states]
    if sorted(permutation) != list(range(len(states))):
        raise AssertionError("dual generator is not a permutation")
    return states, permutation


def permutation_order(permutation: list[int]) -> int:
    seen = [False] * len(permutation)
    order = 1
    for start in range(len(permutation)):
        if seen[start]:
            continue
        current = start
        length = 0
        while not seen[current]:
            seen[current] = True
            length += 1
            current = permutation[current]
        order = math.lcm(order, length)
    return order


def positive_witnesses_to_zero(
    depth: int,
) -> tuple[list[tuple[str, ...]], dict[tuple[str, ...], str]]:
    states = list(itertools.product(PAIR_STATES, repeat=depth))
    index = {state: position for position, state in enumerate(states)}
    inverse_maps: dict[str, list[int]] = {}
    for letter in LETTERS:
        _, permutation = generator_permutation(letter, depth)
        inverse = [0] * len(permutation)
        for source, target in enumerate(permutation):
            inverse[target] = source
        inverse_maps[letter] = inverse

    zero = ("00",) * depth
    witnesses: dict[tuple[str, ...], str] = {zero: ""}
    queue: deque[tuple[str, ...]] = deque([zero])
    while queue:
        target = queue.popleft()
        target_index = index[target]
        suffix = witnesses[target]
        for letter in LETTERS:
            predecessor = states[inverse_maps[letter][target_index]]
            if predecessor in witnesses:
                continue
            witnesses[predecessor] = suffix + letter
            queue.append(predecessor)
    return states, witnesses


def verify_level_positive_transitivity(maximum_depth: int) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for depth in range(1, maximum_depth + 1):
        states, witnesses = positive_witnesses_to_zero(depth)
        if len(witnesses) != len(states):
            raise AssertionError("positive dual monoid is not level transitive")
        lengths = [len(word) for word in witnesses.values()]
        for state, word in witnesses.items():
            if dual_image(word, state) != ("00",) * depth:
                raise AssertionError("positive witness does not reach zero target")
        rows.append(
            {
                "depth": depth,
                "level_size": len(states),
                "states_reaching_zero": len(witnesses),
                "maximum_witness_length": max(lengths),
                "mean_witness_length": sum(lengths) / len(lengths),
            }
        )
    return {
        "levels": rows,
        "exact_reason": (
            "the existing self-replication theorem gives level transitivity; "
            "on each finite level generator inverses are positive powers, so the "
            "positive monoid has the same orbit"
        ),
        "all_checks_pass": True,
    }


def verify_phase_padded_driver_universality(
    maximum_depth: int,
) -> dict[str, Any]:
    depth_rows: list[dict[str, Any]] = []
    total_witnesses = 0
    for depth in range(1, maximum_depth + 1):
        _, witnesses = positive_witnesses_to_zero(depth)
        phase_orders: dict[str, int] = {}
        for phase in PHASES:
            _, permutation = generator_permutation(phase, depth)
            phase_orders[phase] = permutation_order(permutation)

        driver_count = 0
        max_total_length = {phase: 0 for phase in PHASES}
        phase_counts: Counter[str] = Counter()
        for driver in itertools.product(BRANCHES, repeat=depth - 1):
            future = fresh_boundary_prefix(driver)
            if len(future) != depth:
                raise AssertionError("future boundary depth mismatch")
            base = witnesses[future]
            for phase in PHASES:
                word = phase * phase_orders[phase] + base
                if normalized_phase(word) != phase:
                    raise AssertionError("phase padding did not set requested phase")
                if dual_image(word, future) != ("00",) * depth:
                    raise AssertionError("phase padding changed dual zero target")
                outputs = coupled_outputs(word, driver)
                if outputs != ("00",) * depth:
                    raise AssertionError(
                        (
                            "phase-padded witness did not sustain zeros",
                            depth,
                            driver,
                            phase,
                        )
                    )
                current = word
                for branch in driver:
                    if scan(current)[1] != "00":
                        raise AssertionError("witness left zero island early")
                    if normalized_phase(current) != phase:
                        raise AssertionError("zero-island phase changed")
                    current, _ = block_update(current, branch)
                if scan(current)[1] != "00" or normalized_phase(current) != phase:
                    raise AssertionError("final witness state lost phase or zero terminal")
                max_total_length[phase] = max(max_total_length[phase], len(word))
                phase_counts[phase] += 1
                total_witnesses += 1
            driver_count += 1

        depth_rows.append(
            {
                "depth": depth,
                "driver_prefix_length": depth - 1,
                "driver_words_checked": driver_count,
                "phase_orders": phase_orders,
                "witnesses_by_phase": dict(sorted(phase_counts.items())),
                "maximum_phase_padded_witness_length": max_total_length,
            }
        )
    return {
        "depths": depth_rows,
        "total_phase_padded_witnesses": total_witnesses,
        "exact_conclusion": (
            "for every finite future driver and each phase p/u, a finite "
            "accumulated word of that phase realizes the complete terminal-zero prefix"
        ),
        "all_checks_pass": True,
    }


def run_campaign(maximum_depth: int = DEFAULT_DEPTH) -> dict[str, Any]:
    if not 1 <= maximum_depth <= ABSOLUTE_DEPTH:
        raise ValueError("depth outside campaign cap")
    payload: dict[str, Any] = {
        "positive_level_transitivity": verify_level_positive_transitivity(
            maximum_depth
        ),
        "phase_padded_driver_universality": (
            verify_phase_padded_driver_universality(maximum_depth)
        ),
        "exact_conclusions": {
            "finite_phase_universality": (
                "both fixed phases realize every finite future driver prefix"
            ),
            "no_finite_language_obstruction": (
                "no forbidden finite branch word, finite dual-depth mismatch, or "
                "finite phase cylinder can exclude a final zero tail"
            ),
            "remaining_target": (
                "an infinite actual-orbit argument must prevent one compatible "
                "sequence of finite phase witnesses from converging to an ordinary finite state"
            ),
        },
        "scope_warning": (
            "the witness depends on the requested depth; finite-depth universality "
            "does not construct one ordinary word surviving an infinite driver"
        ),
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-phase-universality-v1\0")
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
