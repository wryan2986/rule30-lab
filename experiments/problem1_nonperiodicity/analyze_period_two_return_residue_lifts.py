#!/usr/bin/env python3
"""Classify exact lifted first-return outcomes modulo 64.

At a ``u`` return write the packed fringe state as ``A=4z``.  The next
return gap and next coordinate modulo 64 are determined by ``z mod 2**16``.
The complete lift relation shows why the eight residues observed on the finite
actual orbit are not an inductive invariant when higher bits are forgotten.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any

OUTCOME_BITS = 6
DEPENDENCY_BITS = 16
BAD_RESIDUES = (28, 44, 60)
OBSERVED_ACTUAL_RESIDUES = (0, 3, 11, 24, 35, 43, 56, 63)


def advance_fringe(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    row = 1 | (state << 1)
    odd = row ^ ((row >> 1) | (row >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def branch_letter(state: int) -> str:
    return "u" if state & 3 == 0 else "t"


def return_outcome(z: int) -> tuple[int, int]:
    if z < 0:
        raise ValueError("z must be nonnegative")
    state = 4 * z
    for gap in range(1, 6):
        state = advance_fringe(state)
        if branch_letter(state) == "u":
            return gap, (state >> 2) & 63
    raise AssertionError("five-block return bound failed")


def complete_outcomes() -> list[tuple[int, int]]:
    return [return_outcome(z) for z in range(1 << DEPENDENCY_BITS)]


def precision_minimality(outcomes: list[tuple[int, int]]) -> dict[str, Any]:
    witnesses: list[dict[str, Any]] = []
    for bits in range(OUTCOME_BITS, DEPENDENCY_BITS):
        first: dict[int, tuple[int, tuple[int, int]]] = {}
        found: dict[str, Any] | None = None
        mask = (1 << bits) - 1
        for z, outcome in enumerate(outcomes):
            residue = z & mask
            previous = first.get(residue)
            if previous is None:
                first[residue] = (z, outcome)
            elif previous[1] != outcome:
                found = {
                    "bits": bits,
                    "common_residue": residue,
                    "left_z": previous[0],
                    "right_z": z,
                    "left_outcome": list(previous[1]),
                    "right_outcome": list(outcome),
                }
                break
        if found is None:
            raise AssertionError(f"precision {bits} unexpectedly sufficient")
        witnesses.append(found)

    groups: dict[int, tuple[int, int]] = {}
    mask = (1 << DEPENDENCY_BITS) - 1
    for z, outcome in enumerate(outcomes):
        residue = z & mask
        previous = groups.setdefault(residue, outcome)
        if previous != outcome:
            raise AssertionError("2^16 precision is not deterministic")

    return {
        "outcome_bits": OUTCOME_BITS,
        "sufficient_coordinate_bits": DEPENDENCY_BITS,
        "minimal": True,
        "insufficient_precision_witnesses": witnesses,
        "exact_reason": (
            "five fringe blocks have a radius-ten dependency cone; obtaining "
            "the next coordinate modulo 64 requires the next return state modulo "
            "256, hence the initial return coordinate modulo 2^16"
        ),
    }


def transition_relation(outcomes: list[tuple[int, int]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    relation: dict[int, set[tuple[int, int]]] = {r: set() for r in range(64)}
    counts: dict[int, Counter[tuple[int, int]]] = {
        r: Counter() for r in range(64)
    }
    for z, outcome in enumerate(outcomes):
        residue = z & 63
        relation[residue].add(outcome)
        counts[residue][outcome] += 1

    for residue in range(64):
        rows.append(
            {
                "z_mod_64": residue,
                "outcomes": [
                    {
                        "gap": gap,
                        "next_z_mod_64": successor,
                        "lift_count_mod_2_16": counts[residue][(gap, successor)],
                    }
                    for gap, successor in sorted(relation[residue])
                ],
            }
        )

    observed_rows = {
        str(residue): [list(outcome) for outcome in sorted(relation[residue])]
        for residue in OBSERVED_ACTUAL_RESIDUES
    }
    return {
        "states_checked": 1 << DEPENDENCY_BITS,
        "lifts_per_mod_64_class": 1 << (DEPENDENCY_BITS - OUTCOME_BITS),
        "rows": rows,
        "observed_actual_residue_rows": observed_rows,
    }


def universal_closure(outcomes: list[tuple[int, int]]) -> dict[str, Any]:
    relation: dict[int, set[int]] = {r: set() for r in range(64)}
    for z, (_, successor) in enumerate(outcomes):
        relation[z & 63].add(successor)

    seen = {0}
    frontier = {0}
    layers: list[list[int]] = [[0]]
    while frontier:
        new = set()
        for residue in frontier:
            new.update(relation[residue])
        new.difference_update(seen)
        if not new:
            break
        layers.append(sorted(new))
        seen.update(new)
        frontier = new

    bad_hits = sorted(seen.intersection(BAD_RESIDUES))
    if bad_hits != list(BAD_RESIDUES):
        raise AssertionError("universal closure did not reach every bad cylinder")
    return {
        "start_residue": 0,
        "layers": layers,
        "closure": sorted(seen),
        "closure_size": len(seen),
        "bad_residues_reached": bad_hits,
        "first_bad_layer": next(
            index for index, layer in enumerate(layers) if set(layer) & set(BAD_RESIDUES)
        ),
        "exact_no_go": (
            "no assertion depending only on z mod 64 can both contain the "
            "zero return coordinate, be closed under every compatible 2-adic "
            "lift, and exclude the consecutive-gap-two cylinders"
        ),
    }


def run_campaign() -> dict[str, Any]:
    outcomes = complete_outcomes()
    gap_counts = Counter(gap for gap, _ in outcomes)
    payload: dict[str, Any] = {
        "status": "partial-proof",
        "parameters": {
            "outcome_bits": OUTCOME_BITS,
            "dependency_bits": DEPENDENCY_BITS,
        },
        "gap_counts_over_mod_2_16": {
            str(gap): gap_counts[gap] for gap in sorted(gap_counts)
        },
        "precision": precision_minimality(outcomes),
        "transition_relation": transition_relation(outcomes),
        "universal_closure": universal_closure(outcomes),
        "scientific_boundary": (
            "the exact lift relation is a no-go theorem for residue-only "
            "induction; it does not describe the unique higher-bit actual orbit "
            "and does not exclude eventual center period two"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(run_campaign(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
