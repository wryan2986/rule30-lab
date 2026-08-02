#!/usr/bin/env python3
"""Exact signed-slice lift recursion and scalar-recurrence obstructions."""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from typing import Any

DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 18
SCHEDULE_CAP = 64
MASK_ALPHABET = (0, 3, 11, 12, 15)

class SignedSliceLimitError(RuntimeError):
    pass

def forward_generator(name: str, state: int) -> int:
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t": return stepped
    if name == "u": return stepped ^ 1
    if name == "p": return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError(name)

def frontier_children(state: int) -> tuple[int, ...]:
    return tuple(sorted({forward_generator(g, state) for g in "tup"}))

def build_levels(maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {1}]
    for _ in range(2, maximum_complexity + 1):
        levels.append({c for s in levels[-1] for c in frontier_children(s)})
    return levels

def fiber_mask(levels: list[set[int]], complexity: int, state: int) -> int:
    mask = sum(1 << d for d in range(4) if 4 * state + d in levels[complexity + 1])
    if mask not in MASK_ALPHABET:
        raise AssertionError("fiber escaped five-mask alphabet")
    return mask

def mask_sequence(levels: list[set[int]], complexity: int, state: int, depth: int) -> tuple[int, ...]:
    out: list[int] = []
    for step in range(depth):
        state >>= 2
        out.append(fiber_mask(levels, complexity - 1 - step, state))
    return tuple(out)

def forced_zero_schedule(state: int, cap: int = SCHEDULE_CAP) -> str:
    out: list[str] = []
    for _ in range(cap):
        residue = state & 15
        if residue == 7: branch = "u"
        elif residue == 11: branch = "t"
        else: return "".join(out)
        state = forward_generator(branch, forward_generator("p", (state - 3) >> 2))
        out.append(branch)
    raise SignedSliceLimitError("forced schedule reached cap")

def admissible(word: str) -> bool:
    return all(f not in word for f in ("uu", "ttttt", "ututtu"))

def dominates(current: tuple[int, ...], shadow: tuple[int, ...]) -> bool:
    return all(not (a & ~b) for a, b in zip(current, shadow))

@dataclass(frozen=True, order=True)
class Cylinder:
    complexity: int
    state: int
    depth: int

def belief_rows(levels: list[set[int]], node: Cylinder) -> tuple[tuple[int, ...], list[tuple[int, int, tuple[int, ...]]]]:
    modulus = 4 ** node.depth
    residue = node.state % modulus
    current = mask_sequence(levels, node.complexity, node.state, node.depth)
    rows: list[tuple[int, int, tuple[int, ...]]] = []
    for shadow in levels[node.complexity - 1]:
        if shadow % modulus != residue:
            continue
        masks = mask_sequence(levels, node.complexity - 1, shadow, node.depth)
        if not dominates(current, masks):
            continue
        defects = sum(mask != 15 for mask in masks)
        rows.append((shadow, defects, masks))
    rows.sort()
    return current, rows

def signed_mass(levels: list[set[int]], node: Cylinder) -> int:
    _, rows = belief_rows(levels, node)
    return sum(-1 if defects & 1 else 1 for _, defects, _ in rows)

def parent(node: Cylinder) -> Cylinder:
    if node.depth < 2:
        raise ValueError("depth-one node has no cylinder parent")
    return Cylinder(node.complexity - 1, node.state >> 2, node.depth - 1)

def local_signed_factor(current_mask: int, shadow_mask: int) -> int:
    if current_mask & ~shadow_mask:
        return 0
    return 1 if shadow_mask == 15 else -1

def signed_slice_vector(levels: list[set[int]], child: Cylinder) -> dict[int, int]:
    """Signed parent mass split by the one new shadow fiber used by child."""
    par = parent(child)
    _, rows = belief_rows(levels, par)
    vector = {mask: 0 for mask in MASK_ALPHABET}
    for endpoint, defects, _ in rows:
        next_mask = fiber_mask(levels, child.complexity - 2, endpoint)
        vector[next_mask] += -1 if defects & 1 else 1
    return vector

def predicted_child_mass(levels: list[set[int]], child: Cylinder) -> int:
    current_mask = mask_sequence(levels, child.complexity, child.state, child.depth)[0]
    vector = signed_slice_vector(levels, child)
    return sum(local_signed_factor(current_mask, mask) * value for mask, value in vector.items())

def gap_cylinders(levels: list[set[int]], maximum_complexity: int) -> list[Cylinder]:
    out: list[Cylinder] = []
    for complexity in range(2, maximum_complexity + 1):
        for state in sorted(levels[complexity]):
            if state & 3 != 3:
                continue
            schedule = forced_zero_schedule(state)
            for cut in range(len(schedule) + 1):
                if schedule[cut:cut + 6] != "ututut":
                    continue
                if not admissible(schedule[:cut] + "utututu"):
                    continue
                out.append(Cylinder(complexity, state, cut + 1))
    return out

def ancestor_closure(nodes: list[Cylinder]) -> set[Cylinder]:
    out: set[Cylinder] = set()
    for node in nodes:
        for step in range(node.depth):
            out.add(Cylinder(node.complexity - step, node.state >> (2 * step), node.depth - step))
    return out

def node_record(levels: list[set[int]], node: Cylinder) -> dict[str, Any]:
    return {
        "complexity": node.complexity,
        "state_hex": hex(node.state),
        "depth": node.depth,
        "current_masks": [f"{m:04b}" for m in mask_sequence(levels, node.complexity, node.state, node.depth)],
        "signed_mass": signed_mass(levels, node),
    }

def run_campaign(maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY) -> dict[str, Any]:
    if not 16 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise SignedSliceLimitError("maximum complexity outside controlled range")
    levels = build_levels(maximum_complexity)
    gaps = gap_cylinders(levels, maximum_complexity)
    closure = ancestor_closure(gaps)
    masses = {node: signed_mass(levels, node) for node in closure}
    disagreements = []
    for node in closure:
        if node.depth >= 2 and predicted_child_mass(levels, node) != masses[node]:
            disagreements.append(node)

    magnitude_data: dict[str, Any] | None = None
    sign_data: dict[str, Any] | None = None
    if maximum_complexity >= 18:
        magnitude_a = Cylinder(17, 0x190B9FDFB, 2)
        magnitude_b = Cylinder(17, 0x1BCD3A7B3, 2)
        sign_a = Cylinder(18, 0x642E4D2F1, 3)
        sign_b = Cylinder(18, 0x6473D46AB, 5)
        special = [magnitude_a, magnitude_b, parent(magnitude_a), parent(magnitude_b), sign_a, sign_b, parent(sign_a), parent(sign_b)]
        if any(node.state not in levels[node.complexity] for node in special):
            raise AssertionError("explicit obstruction left the frontier")
        magnitude_data = {
            "a": node_record(levels, magnitude_a),
            "b": node_record(levels, magnitude_b),
            "parent_a": node_record(levels, parent(magnitude_a)),
            "parent_b": node_record(levels, parent(magnitude_b)),
        }
        sign_data = {
            "a": node_record(levels, sign_a),
            "b": node_record(levels, sign_b),
            "parent_a": node_record(levels, parent(sign_a)),
            "parent_b": node_record(levels, parent(sign_b)),
        }
        if not (
            magnitude_data["parent_a"]["signed_mass"] == magnitude_data["parent_b"]["signed_mass"] == 1650
            and magnitude_data["a"]["current_masks"][0] == magnitude_data["b"]["current_masks"][0] == "1011"
            and magnitude_data["a"]["signed_mass"] == 104
            and magnitude_data["b"]["signed_mass"] == 605
        ):
            raise AssertionError("scalar magnitude obstruction changed")
        if not (
            sign_data["parent_a"]["signed_mass"] > 0
            and sign_data["parent_b"]["signed_mass"] > 0
            and sign_data["a"]["current_masks"][0] == sign_data["b"]["current_masks"][0] == "1011"
            and sign_data["a"]["signed_mass"] == -83
            and sign_data["b"]["signed_mass"] == 2
        ):
            raise AssertionError("scalar sign obstruction changed")

    payload: dict[str, Any] = {
        "status": "exact-signed-slice-lift-and-scalar-recurrence-no-go",
        "maximum_complexity": maximum_complexity,
        "outputs_built": sum(len(levels[k]) for k in range(1, maximum_complexity + 1)),
        "gap_222_cylinders": len(gaps),
        "ancestor_cylinders": len(closure),
        "signed_zero_ancestor_cylinders": sum(mass == 0 for mass in masses.values()),
        "negative_ancestor_cylinders": sum(mass < 0 for mass in masses.values()),
        "minimum_absolute_ancestor_mass": min(abs(mass) for mass in masses.values()),
        "signed_slice_disagreements": len(disagreements),
        "theorem": {
            "slice_vector": "Split the signed parent belief by the exact next shadow fiber in {0000,0011,1011,1100,1111}.",
            "lift": "The child signed mass is the dot product of that five-component vector with the local signed dominance factor for the new current fiber.",
            "nonvanishing_boundary": "This identity is exact but a scalar parent mass or its sign does not determine the child mass or sign.",
        },
        "scalar_magnitude_obstruction": magnitude_data,
        "scalar_sign_obstruction": sign_data,
        "scientific_boundary": (
            "The signed-slice lift and both explicit obstructions are exact. Ancestor nonvanishing counts are finite and do not prove all-depth nonvanishing."
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-complexity", type=int, default=DEFAULT_MAXIMUM_COMPLEXITY)
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_complexity), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
