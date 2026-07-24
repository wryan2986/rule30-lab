#!/usr/bin/env python3
"""Analyze the actual fringe cylinder for consecutive gap-two returns.

At a ``u`` return write the packed fringe state as ``A=4z``.  A complete
five-letter dependency-cone exhaustion proves that the next two return gaps are
both two exactly for three residue classes modulo 64.  The actual zero-fringe
campaign is a separate finite computation; it does not prove those classes are
avoided forever.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from typing import Any

BAD_RESIDUES_MOD_64 = (28, 44, 60)
DEFAULT_BLOCKS = 20_000
ABSOLUTE_BLOCKS = 200_000


class ActualGapTwoLimitError(RuntimeError):
    """Raised before an actual-orbit campaign exceeds its controlled cap."""


def advance_fringe(state: int) -> int:
    if state < 0:
        raise ValueError("state must be nonnegative")
    row = 1 | (state << 1)
    odd = row ^ ((row >> 1) | (row >> 2))
    return (odd << 1) ^ (odd | (odd >> 1))


def branch_letter(state: int) -> str:
    return "u" if state & 3 == 0 else "t"


def branch_word_from_return_coordinate(z: int, length: int) -> str:
    if z < 0:
        raise ValueError("z must be nonnegative")
    if length < 0:
        raise ValueError("length must be nonnegative")
    state = 4 * z
    letters: list[str] = []
    for _ in range(length):
        letters.append(branch_letter(state))
        state = advance_fringe(state)
    return "".join(letters)


def return_gap(z: int) -> int:
    if z < 0:
        raise ValueError("z must be nonnegative")
    state = 4 * z
    for gap in range(1, 7):
        state = advance_fringe(state)
        if branch_letter(state) == "u":
            return gap
    raise AssertionError("known return-gap bound failed")


def consecutive_gap_two_cylinder() -> dict[str, Any]:
    rows = []
    witnesses = []
    for residue in range(256):
        word = branch_word_from_return_coordinate(residue, 5)
        is_pair = word == "ututu"
        predicted = residue % 64 in BAD_RESIDUES_MOD_64
        if is_pair != predicted:
            raise AssertionError("mod-64 cylinder classification failed")
        if is_pair:
            witnesses.append(residue)
        rows.append({"z_mod_256": residue, "word": word, "pair_2_2": is_pair})

    if witnesses != [28, 44, 60, 92, 108, 124, 156, 172, 188, 220, 236, 252]:
        raise AssertionError("unexpected complete dependency-cone witnesses")

    return {
        "dependency_z_bits": 8,
        "states_checked": 256,
        "target_word": "ututu",
        "witnesses_mod_256": witnesses,
        "factored_residues_mod_64": list(BAD_RESIDUES_MOD_64),
        "exact_theorem": (
            "at any u return, the next two return gaps are (2,2) exactly when "
            "z mod 64 is 28, 44, or 60"
        ),
        "all_checks_pass": True,
    }


def actual_orbit_campaign(blocks: int) -> dict[str, Any]:
    if not 1 <= blocks <= ABSOLUTE_BLOCKS:
        raise ActualGapTwoLimitError("block count outside controlled range")

    state = 0
    return_count = 0
    previous_position: int | None = None
    previous_gap: int | None = None
    gap_counts: Counter[int] = Counter()
    residue_counts: Counter[int] = Counter()
    pair_22_count = 0
    bad_residue_count = 0
    last_gap_two_start: int | None = None

    for block in range(blocks):
        if branch_letter(state) == "u":
            residue = (state >> 2) & 63
            residue_counts[residue] += 1
            return_count += 1
            if residue in BAD_RESIDUES_MOD_64:
                bad_residue_count += 1
            if previous_position is not None:
                gap = block - previous_position
                gap_counts[gap] += 1
                if previous_gap == 2 and gap == 2:
                    pair_22_count += 1
                if gap == 2:
                    last_gap_two_start = previous_position
                previous_gap = gap
            previous_position = block
        state = advance_fringe(state)

    observed = sorted(residue_counts)
    return {
        "blocks": blocks,
        "return_count": return_count,
        "gap_counts": {str(key): gap_counts[key] for key in sorted(gap_counts)},
        "return_residue_counts_mod_64": {
            str(key): residue_counts[key] for key in sorted(residue_counts)
        },
        "observed_return_residues_mod_64": observed,
        "bad_cylinder_visits": bad_residue_count,
        "consecutive_gap_two_count": pair_22_count,
        "last_gap_two_start": last_gap_two_start,
        "scope": "finite actual zero-initialized fringe orbit",
    }


def run_campaign(blocks: int = DEFAULT_BLOCKS) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": "partial-proof",
        "consecutive_gap_two_cylinder": consecutive_gap_two_cylinder(),
        "actual_orbit": actual_orbit_campaign(blocks),
        "scientific_boundary": (
            "the mod-64 cylinder theorem is all-time, but the actual-orbit "
            "avoidance result is finite and does not exclude eventual period two"
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--blocks", type=int, default=DEFAULT_BLOCKS)
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.blocks), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
