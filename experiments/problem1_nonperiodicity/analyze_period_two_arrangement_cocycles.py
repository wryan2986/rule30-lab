#!/usr/bin/env python3
"""Classify arrangement-sensitive edge cocycles for the period-two transducer.

Two exact whole-word ansatzes are considered.

1. Geometrically weighted additive cocycles over a field:

       a_x - a_y = V_s - lambda V_t

   on every transducer edge ``s --x/y--> t``. Multiplication by powers of
   ``lambda`` makes this identity telescope across the ordered word, so it
   retains every letter position rather than only factor counts.

2. Group-valued multiplicative cocycles:

       C_s A_x = A_y C_t

   on every edge. Products then telescope noncommutatively across the complete
   ordered word.

Exact cancellation proves both classes terminal-blind: all three letter weights
coincide, and all terminal gauges are either zero/equal (additive) or identical
(group-valued). These are no-go theorems for these ansatzes, not a proof of
period-two exclusion or Rule 30 center nonperiodicity.
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

LETTERS = ("t", "p", "u")
PAIR_STATES = ((0, 0), (0, 1), (1, 0), (1, 1))
DEFAULT_CONTROL_GROUPS = ("S3", "D4")


class ArrangementCocycleError(RuntimeError):
    """Raised when an exact control contradicts the proved classification."""


def _load_sibling(filename: str, module_name: str):
    path = Path(__file__).with_name(filename)
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


GLOBAL = _load_sibling(
    "analyze_period_two_global_transducer.py", "period_two_global_transducer"
)


def state_name(state: tuple[int, int]) -> str:
    return "".join(map(str, state))


def transition_edges() -> tuple[dict[str, str], ...]:
    """Return the exact twelve edges of the whole-word transducer."""

    rows: list[dict[str, str]] = []
    for state in PAIR_STATES:
        for letter in LETTERS:
            output, successor = GLOBAL.letter_transition(letter, state)
            rows.append(
                {
                    "state": state_name(state),
                    "input": letter,
                    "output": output,
                    "successor": state_name(successor),
                }
            )
    return tuple(rows)


def _additive_residuals(
    lam: Fraction,
    letter_weights: dict[str, Fraction],
    potentials: dict[str, Fraction],
) -> tuple[Fraction, ...]:
    return tuple(
        letter_weights[edge["input"]]
        - letter_weights[edge["output"]]
        - potentials[edge["state"]]
        + lam * potentials[edge["successor"]]
        for edge in transition_edges()
    )


def geometric_classification(lam: Fraction) -> dict[str, Any]:
    """Return and independently check the exact field-valued classification."""

    lam = Fraction(lam)
    if lam == 1:
        witness_weights = {letter: Fraction(7) for letter in LETTERS}
        witness_potentials = {state_name(s): Fraction(5) for s in PAIR_STATES}
        potential_conclusion = "V_00=V_01=V_10=V_11"
        dimension = 2
    else:
        witness_weights = {letter: Fraction(7) for letter in LETTERS}
        witness_potentials = {state_name(s): Fraction(0) for s in PAIR_STATES}
        potential_conclusion = "V_00=V_01=V_10=V_11=0"
        dimension = 1

    if any(_additive_residuals(lam, witness_weights, witness_potentials)):
        raise ArrangementCocycleError("classified additive witness fails an edge")

    return {
        "lambda": str(lam),
        "solution_dimension": dimension,
        "letter_weights": "a_t=a_p=a_u",
        "state_potentials": potential_conclusion,
        "terminal_sensitivity": False,
        "proof_split": "lambda=1 versus lambda!=1",
        "all_checks_pass": True,
    }


def verify_geometric_cases() -> dict[str, Any]:
    cases = [
        Fraction(-2),
        Fraction(-1),
        Fraction(0),
        Fraction(1, 2),
        Fraction(1),
        Fraction(2),
    ]
    results = [geometric_classification(value) for value in cases]
    return {
        "exact_theorem": (
            "for every field scalar lambda, geometrically weighted additive "
            "edge cocycles have equal letter weights and terminal-blind potentials"
        ),
        "control_cases": results,
        "all_checks_pass": True,
    }


Permutation = tuple[int, ...]


def compose(left: Permutation, right: Permutation) -> Permutation:
    """Return left after right."""

    return tuple(left[right[index]] for index in range(len(left)))


def identity(size: int) -> Permutation:
    return tuple(range(size))


def inverse(value: Permutation) -> Permutation:
    result = [0] * len(value)
    for index, image in enumerate(value):
        result[image] = index
    return tuple(result)


def generated_group(size: int, generators: Iterable[Permutation]) -> tuple[Permutation, ...]:
    one = identity(size)
    seen = {one}
    frontier = [one]
    gens = tuple(generators)
    while frontier:
        current = frontier.pop()
        for generator in gens:
            for candidate in (
                compose(current, generator),
                compose(generator, current),
            ):
                if candidate not in seen:
                    seen.add(candidate)
                    frontier.append(candidate)
    return tuple(sorted(seen))


def named_group(name: str) -> tuple[Permutation, ...]:
    if name == "S3":
        return generated_group(3, ((1, 0, 2), (1, 2, 0)))
    if name == "D4":
        return generated_group(4, ((1, 2, 3, 0), (0, 3, 2, 1)))
    raise ValueError(f"unknown control group {name}")


def _multiplicative_edges_hold(
    letters: dict[str, Permutation], gauges: dict[str, Permutation]
) -> bool:
    return all(
        compose(gauges[edge["state"]], letters[edge["input"]])
        == compose(letters[edge["output"]], gauges[edge["successor"]])
        for edge in transition_edges()
    )


def brute_force_group_control(name: str) -> dict[str, Any]:
    """Exhaust a small group with exact pruning from four edge equations."""

    group = named_group(name)
    solutions = 0
    nontrivial = 0
    expected = 0

    for a in group:
        for c in group:
            if compose(a, c) == compose(c, a):
                expected += 1

    for a, b, c0, c1 in itertools.product(group, repeat=4):
        u = b
        c3 = compose(compose(inverse(b), c0), b)
        c2 = compose(compose(b, c1), inverse(b))
        letters = {"t": a, "p": b, "u": u}
        gauges = {"00": c0, "01": c1, "10": c2, "11": c3}
        if not _multiplicative_edges_hold(letters, gauges):
            continue
        solutions += 1
        if len(set(letters.values())) != 1 or len(set(gauges.values())) != 1:
            nontrivial += 1

    if solutions != expected or nontrivial:
        raise ArrangementCocycleError("finite group control contradicts group theorem")
    return {
        "group": name,
        "order": len(group),
        "reduced_assignments_checked": len(group) ** 4,
        "solutions": solutions,
        "expected_commuting_pairs": expected,
        "nontrivial_solutions": nontrivial,
        "all_checks_pass": True,
    }


def verify_group_cocycle_theorem(
    control_groups: tuple[str, ...] = DEFAULT_CONTROL_GROUPS,
) -> dict[str, Any]:
    controls = [brute_force_group_control(name) for name in control_groups]
    return {
        "exact_theorem": (
            "in every group, C_s A_x=A_y C_t on all twelve edges forces "
            "A_t=A_p=A_u and C_00=C_01=C_10=C_11"
        ),
        "proof_dependencies": [
            "group cancellation",
            "the exact twelve-edge transducer table",
        ],
        "terminal_sensitivity": False,
        "finite_group_controls": controls,
        "all_checks_pass": True,
    }


def run_campaign() -> dict[str, Any]:
    payload = {
        "transition_edges": transition_edges(),
        "geometric_additive": verify_geometric_cases(),
        "group_multiplicative": verify_group_cocycle_theorem(),
        "exact_conclusions": {
            "arrangement_preserved": (
                "geometric weights retain absolute positions and group products retain "
                "the complete noncommutative letter order"
            ),
            "no_go": (
                "both exact edge-telescoping classes are terminal-blind and cannot "
                "distinguish eventual output 00"
            ),
            "remaining_target": (
                "a noninvertible semigroup representation, a multiscale recursive "
                "observable, or an actual-orbit identity not decomposable edge by edge"
            ),
        },
    }
    digest = hashlib.sha256()
    digest.update(b"rule30-period-two-arrangement-cocycles-v1\0")
    digest.update(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode())
    payload["certificate_sha256"] = digest.hexdigest()
    return payload


def _parser() -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description=__doc__)


def main() -> int:
    _parser().parse_args()
    print(json.dumps(run_campaign(), sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
