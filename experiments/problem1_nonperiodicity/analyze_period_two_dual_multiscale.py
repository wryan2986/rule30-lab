#!/usr/bin/env python3
"""Analyze the dual multiscale action of the period-two whole-word transducer.

The exact whole-word transducer has four scan states and input/output alphabet
{t,p,u}. Reversibility in the scan-state coordinate makes the dual machine an
invertible self-similar action on the rooted 4-ary tree of scan-state words.

This module verifies explicit self-replication witnesses, proves the hypotheses
of the all-depth level-transitivity lemma, exhausts finite levels, and measures
section growth on the unique actual period-two word orbit.

The exact theorem is structural: the dual group is self-replicating and acts
transitively on every finite level, so every boundary orbit has all 4**d depth-d
prefixes. The actual-orbit section counts are finite diagnostics only. This
does not prove infinite support, exclude period two, or solve Rule 30 center
nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import deque
from typing import Any, Iterable

LETTERS = ("t", "p", "u")
INVERSES = {"t": "T", "p": "P", "u": "U", "T": "t", "P": "p", "U": "u"}
STATE_NAMES = ("00", "01", "10", "11")

# (emitted letter, next scan state)
TRANSITIONS: dict[int, dict[str, tuple[str, int]]] = {
    0: {"t": ("t", 0), "p": ("p", 3), "u": ("p", 3)},
    1: {"t": ("p", 1), "p": ("u", 2), "u": ("u", 2)},
    2: {"t": ("p", 3), "p": ("p", 1), "u": ("t", 0)},
    3: {"t": ("u", 2), "p": ("t", 0), "u": ("p", 1)},
}

EXPECTED_PAIR_ORBIT_COUNTS = {1: 2, 2: 4, 3: 6, 4: 8}
EXPECTED_PAIR_ORBIT_SIZES = {
    1: [4, 8],
    2: [16, 32, 64, 128],
    3: [64, 128, 256, 512, 1024, 2048],
    4: [256, 512, 1024, 2048, 4096, 8192, 16384, 32768],
}
EXPECTED_ACTUAL_SECTIONS = {
    4: [4, 16, 62, 200, 394, 491, 514, 517],
    8: [4, 16, 64, 256, 1003, 3695, 11426, 26043],
    16: [4, 16, 64, 256, 1024, 4096, 16378, 65413],
    32: [4, 16, 64, 256, 1024, 4096, 16384, 65536],
}


def scan(word: tuple[str, ...], start_state: int) -> tuple[tuple[str, ...], int]:
    output: list[str] = []
    state = start_state
    for letter in word:
        emitted, state = TRANSITIONS[state][letter]
        output.append(emitted)
    return tuple(output), state


def dual_action(letter: str, state_word: tuple[int, ...]) -> tuple[int, ...]:
    """Apply one dual generator to a word of scan states."""

    if letter not in LETTERS:
        raise ValueError("dual generator must be t, p, or u")
    output: list[int] = []
    current = letter
    for state in state_word:
        emitted, next_state = TRANSITIONS[state][current]
        output.append(next_state)
        current = emitted
    return tuple(output)


def root_permutation(letter: str) -> tuple[int, ...]:
    return tuple(TRANSITIONS[state][letter][1] for state in range(4))


def generator_sections(letter: str) -> tuple[str, ...]:
    return tuple(TRANSITIONS[state][letter][0] for state in range(4))


def inverse_permutation(permutation: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * len(permutation)
    for source, target in enumerate(permutation):
        result[target] = source
    return tuple(result)


def compose_permutations(
    left: tuple[int, ...], right: tuple[int, ...]
) -> tuple[int, ...]:
    """Return left after right."""

    return tuple(left[right[index]] for index in range(len(right)))


def reduce_group_word(word: Iterable[str]) -> tuple[str, ...]:
    stack: list[str] = []
    for symbol in word:
        if symbol not in INVERSES:
            raise ValueError("unknown group symbol")
        if stack and stack[-1] == INVERSES[symbol]:
            stack.pop()
        else:
            stack.append(symbol)
    return tuple(stack)


def symbol_recursions() -> dict[str, tuple[tuple[int, ...], tuple[tuple[str, ...], ...]]]:
    recursions: dict[
        str, tuple[tuple[int, ...], tuple[tuple[str, ...], ...]]
    ] = {}
    for letter in LETTERS:
        recursions[letter] = (
            root_permutation(letter),
            tuple((section,) for section in generator_sections(letter)),
        )
    for letter in LETTERS:
        inverse = letter.upper()
        permutation, sections = recursions[letter]
        inverse_root = inverse_permutation(permutation)
        inverse_sections: list[tuple[str, ...]] = []
        for vertex in range(4):
            source = inverse_root[vertex]
            inverse_sections.append(
                reduce_group_word(INVERSES[symbol] for symbol in reversed(sections[source]))
            )
        recursions[inverse] = (inverse_root, tuple(inverse_sections))
    return recursions


RECURSIONS = symbol_recursions()
IDENTITY_RECURSION = (tuple(range(4)), tuple(() for _ in range(4)))


def compose_recursions(
    left: tuple[tuple[int, ...], tuple[tuple[str, ...], ...]],
    right: tuple[tuple[int, ...], tuple[tuple[str, ...], ...]],
) -> tuple[tuple[int, ...], tuple[tuple[str, ...], ...]]:
    """Return the wreath recursion of left after right."""

    left_root, left_sections = left
    right_root, right_sections = right
    root = compose_permutations(left_root, right_root)
    sections = tuple(
        reduce_group_word(right_sections[vertex] + left_sections[right_root[vertex]])
        for vertex in range(4)
    )
    return root, sections


def group_word_recursion(
    word: tuple[str, ...],
) -> tuple[tuple[int, ...], tuple[tuple[str, ...], ...]]:
    recursion = IDENTITY_RECURSION
    for symbol in word:
        recursion = compose_recursions(RECURSIONS[symbol], recursion)
    return recursion


def verify_self_replication_witnesses() -> dict[str, Any]:
    witnesses = {
        "t": ("t",),
        "p": ("p", "p", "T"),
        "u": ("t", "P", "t", "t", "P"),
    }
    details: dict[str, Any] = {}
    expected_root = root_permutation("t")
    if expected_root != (0, 1, 3, 2):
        raise AssertionError("unexpected t root permutation")
    if root_permutation("u") != (3, 2, 0, 1):
        raise AssertionError("u is not the expected four-cycle")

    for target, word in witnesses.items():
        root, sections = group_word_recursion(word)
        if root != expected_root:
            raise AssertionError("witness does not have the required root action")
        if root[0] != 0:
            raise AssertionError("witness does not fix vertex 00")
        if sections[0] != (target,):
            raise AssertionError("witness section is not the requested generator")
        details[target] = {
            "word": "".join(word),
            "root_permutation": list(root),
            "section_at_00": "".join(sections[0]),
            "all_sections": ["".join(section) for section in sections],
        }

    return {
        "root_four_cycle": {"generator": "u", "permutation": [3, 2, 0, 1]},
        "stabilizer_section_witnesses": details,
        "exact_conclusion": (
            "the dual action is self-replicating and level-transitive on Q^d "
            "for every d>=1"
        ),
        "boundary_conclusion": (
            "every dual boundary orbit has all 4^d possible depth-d prefixes"
        ),
        "all_checks_pass": True,
    }


def enumerate_level_orbit(depth: int) -> int:
    start = (0,) * depth
    queue: deque[tuple[int, ...]] = deque([start])
    seen = {start}
    while queue:
        word = queue.popleft()
        for letter in LETTERS:
            target = dual_action(letter, word)
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return len(seen)


def verify_level_orbits(maximum_depth: int = 8) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for depth in range(1, maximum_depth + 1):
        count = enumerate_level_orbit(depth)
        expected = 4**depth
        if count != expected:
            raise AssertionError("dual level orbit is not full")
        counts[str(depth)] = count
    return {
        "maximum_depth": maximum_depth,
        "orbit_sizes": counts,
        "all_levels_full": True,
    }


def root_output_signature(state_word: tuple[int, ...]) -> tuple[str, ...]:
    signature: list[str] = []
    for letter in LETTERS:
        current = letter
        for state in state_word:
            current = TRANSITIONS[state][current][0]
        signature.append(current)
    return tuple(signature)


def verify_pair_orbits(maximum_depth: int = 4) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for depth in range(1, maximum_depth + 1):
        words = list(itertools.product(range(4), repeat=depth))
        index = {word: offset for offset, word in enumerate(words)}
        transitions = {
            letter: [index[dual_action(letter, word)] for word in words]
            for letter in LETTERS
        }
        signatures = [root_output_signature(word) for word in words]
        size = len(words)
        unseen = bytearray(b"\x01") * (size * size)
        for position in range(size):
            unseen[position * size + position] = 0
        orbit_sizes: list[int] = []
        nonseparating_orbits = 0

        for code in range(size * size):
            if not unseen[code]:
                continue
            unseen[code] = 0
            left, right = divmod(code, size)
            queue: deque[tuple[int, int]] = deque([(left, right)])
            orbit_size = 0
            separates = False
            while queue:
                first, second = queue.popleft()
                orbit_size += 1
                if signatures[first] != signatures[second]:
                    separates = True
                for letter in LETTERS:
                    target_first = transitions[letter][first]
                    target_second = transitions[letter][second]
                    target_code = target_first * size + target_second
                    if unseen[target_code]:
                        unseen[target_code] = 0
                        queue.append((target_first, target_second))
            orbit_sizes.append(orbit_size)
            if not separates:
                nonseparating_orbits += 1

        orbit_sizes.sort()
        if len(orbit_sizes) != EXPECTED_PAIR_ORBIT_COUNTS[depth]:
            raise AssertionError("unexpected pair-orbit count")
        if orbit_sizes != EXPECTED_PAIR_ORBIT_SIZES[depth]:
            raise AssertionError("unexpected pair-orbit sizes")
        if nonseparating_orbits:
            raise AssertionError("a finite pair orbit failed to separate root outputs")
        results[str(depth)] = {
            "ordered_pair_orbits": len(orbit_sizes),
            "orbit_sizes": orbit_sizes,
            "all_orbits_root_separating": True,
        }
    return {
        "maximum_depth": maximum_depth,
        "levels": results,
        "finite_pattern": "2d ordered-pair orbits at depth d through the checked range",
        "scientific_boundary": "the 2d pair-orbit law is finite evidence, not an all-depth theorem here",
    }


def fringe_step(state: int) -> int:
    right_row = 1 + 2 * state
    first = right_row ^ ((right_row >> 1) | (right_row >> 2))
    return (first << 1) ^ (first | (first >> 1))


def branch_letter(state: int) -> str:
    return "u" if state % 4 == 0 else "t"


def actual_words(maximum_block: int) -> dict[int, tuple[str, ...]]:
    fringe = 0
    word: tuple[str, ...] = ()
    words = {0: word}
    for block in range(maximum_block):
        scanned, _ = scan(word, 3)
        word = (branch_letter(fringe), "p") + scanned
        fringe = fringe_step(fringe)
        words[block + 1] = word
    return words


def section_level_sizes(word: tuple[str, ...], maximum_depth: int) -> list[int]:
    level = {word}
    sizes: list[int] = []
    for _ in range(maximum_depth):
        level = {scan(candidate, state)[0] for candidate in level for state in range(4)}
        sizes.append(len(level))
    return sizes


def verify_actual_section_growth(maximum_depth: int = 8) -> dict[str, Any]:
    words = actual_words(max(EXPECTED_ACTUAL_SECTIONS))
    results: dict[str, Any] = {}
    for block, expected in EXPECTED_ACTUAL_SECTIONS.items():
        sizes = section_level_sizes(words[block], maximum_depth)
        if sizes != expected:
            raise AssertionError("unexpected actual-orbit section growth")
        results[str(block)] = {
            "word_length": len(words[block]),
            "section_orbit_sizes": sizes,
            "maximum_possible": [4**depth for depth in range(1, maximum_depth + 1)],
            "full_through_depth": max(
                depth
                for depth, (observed, maximum) in enumerate(
                    zip(sizes, (4**value for value in range(1, maximum_depth + 1))),
                    start=1,
                )
                if observed == maximum
            ),
        }
    return {
        "maximum_depth": maximum_depth,
        "blocks": results,
        "finite_conclusion": (
            "the actual block-32 word realizes all 4^d iterated sections through d=8"
        ),
        "scientific_boundary": "finite section growth does not prove all-depth freeness or infinite support",
    }


def run_campaign(maximum_level_depth: int = 8) -> dict[str, Any]:
    payload = {
        "self_replication": verify_self_replication_witnesses(),
        "level_orbits": verify_level_orbits(maximum_level_depth),
        "pair_orbits": verify_pair_orbits(4),
        "actual_section_growth": verify_actual_section_growth(8),
        "exact_conclusions": {
            "dual_level_transitivity": (
                "the invertible dual acts transitively on every finite level Q^d"
            ),
            "boundary_orbits": (
                "every infinite scan-state word has a dual orbit with all 4^d prefixes at every depth d"
            ),
            "multiscale_no_closure": (
                "the natural exact section hierarchy does not collapse to a small universal level orbit"
            ),
            "next_target": (
                "use a quotient special to the unique actual fringe orbit or a multi-time seam identity, not the full universal section tower"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-dual-multiscale-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--maximum-level-depth", type=int, default=8)
    return result


def main() -> int:
    args = parser().parse_args()
    if not 1 <= args.maximum_level_depth <= 8:
        raise SystemExit("maximum level depth must be between 1 and 8")
    campaign = run_campaign(args.maximum_level_depth)
    output = {
        "schema_version": 1,
        "experiment_id": "problem1-period-two-dual-multiscale-v1",
        "question": "problem1",
        "hypothesis": (
            "A recursively composed section state might close at bounded size and distinguish eventual terminal 00."
        ),
        "status": "partial-proof",
        "result_summary": campaign,
        "interpretation": (
            "The dual is exactly self-replicating and level-transitive, while the actual word already realizes maximal iterated-section growth through depth eight. The universal section tower expands rather than closing; a useful recursive observable must quotient it using actual-orbit or multi-time structure."
        ),
        "limitations": [
            "does not prove the scan-state semigroup is free",
            "the ordered-pair orbit law is checked only through depth four",
            "the actual section-growth campaign is finite through depth eight",
            "does not prove the alternating inverse lift has infinite support",
            "does not exclude eventual center period two",
            "does not solve Rule 30 center nonperiodicity",
        ],
    }
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
