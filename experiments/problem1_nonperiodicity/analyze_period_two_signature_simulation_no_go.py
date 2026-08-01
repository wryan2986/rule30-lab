#!/usr/bin/env python3
"""Greatest set-valued simulation on the period-two signature graph.

The twelve parent/fiber signatures form a finite nondeterministic labelled graph
when concrete frontier states are quotiented by signature. This analyzer
computes the greatest same-digit simulation between one current signature and a
nonempty set of shadow signatures. It then exhibits why that abstraction is
too coarse for survivor-cylinder shadows: the greatest simulation has a
universal singleton shadow, while a small exact frontier cylinder has no
adjacent concrete shadow at all.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from typing import Any

PHASES = ("p", "u")
CHILD_MASK = {0: 0b1011, 1: 0b1100, 2: 0b1110, 3: 0b0011}
DEFAULT_MAXIMUM_COMPLEXITY = 16
ABSOLUTE_MAXIMUM_COMPLEXITY = 20
TOP_SIGNATURE = (0b1111, 0b1111)


class SimulationCampaignLimitError(RuntimeError):
    """Raised before a controlled campaign exceeds its configured cap."""


def forward_generator(name: str, state: int) -> int:
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError("unknown generator")


def frontier_children(state: int) -> tuple[int, ...]:
    return tuple(sorted({forward_generator(name, state) for name in "tup"}))


def phase_start(phase: str) -> int:
    if phase == "p":
        return 3
    if phase == "u":
        return 1
    raise ValueError("phase must be p or u")


def build_levels(phase: str, maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {phase_start(phase)}]
    for _ in range(2, maximum_complexity + 1):
        levels.append(
            {child for state in levels[-1] for child in frontier_children(state)}
        )
    return levels


def fiber_from_predecessor(mask: int) -> int:
    fiber = 0
    for digit in range(4):
        if (mask >> digit) & 1:
            fiber |= CHILD_MASK[digit]
    return fiber


def signature_map(level: set[int]) -> dict[int, tuple[int, int]]:
    """Compute all signatures by the exact direct predecessor contribution."""
    predecessor: dict[int, int] = {}
    for parent in level:
        digit = parent & 3
        residual = parent >> 2
        generator = "t" if digit == 0 else "u" if digit == 1 else "p"
        quotient = forward_generator(generator, residual)
        predecessor[quotient] = predecessor.get(quotient, 0) | (1 << digit)
    result: dict[int, tuple[int, int]] = {}
    for state in level:
        mask = predecessor.get(state, 0)
        if mask & 0b0100 and not mask & 0b1000:
            raise AssertionError("digit-2 predecessor lacked digit-3 mate")
        result[state] = (mask, fiber_from_predecessor(mask))
    return result


def format_signature(signature: tuple[int, int]) -> str:
    return f"0b{signature[0]:04b}/0b{signature[1]:04b}"


def phase_graph(phase: str, maximum_complexity: int) -> dict[str, Any]:
    levels = build_levels(phase, maximum_complexity)
    maps = [dict() for _ in range(maximum_complexity + 1)]
    for complexity in range(1, maximum_complexity + 1):
        maps[complexity] = signature_map(levels[complexity])

    signatures: set[tuple[int, int]] = set()
    edges: set[tuple[tuple[int, int], int, tuple[int, int]]] = set()
    profiles: set[
        tuple[tuple[int, int], tuple[tuple[int, int] | None, ...]]
    ] = set()
    profiles_by_level: dict[str, int] = {}

    for complexity in range(1, maximum_complexity):
        current = maps[complexity]
        next_map = maps[complexity + 1]
        level_profiles = set()
        signatures.update(current.values())
        signatures.update(next_map.values())
        for state, source in current.items():
            targets: list[tuple[int, int] | None] = []
            for digit in range(4):
                target = next_map.get(4 * state + digit)
                targets.append(target)
                if target is not None:
                    edges.add((source, digit, target))
            profile = (source, tuple(targets))
            profiles.add(profile)
            level_profiles.add(profile)
        profiles_by_level[str(complexity)] = len(level_profiles)

    return {
        "phase": phase,
        "outputs_checked": sum(
            len(levels[complexity])
            for complexity in range(1, maximum_complexity + 1)
        ),
        "signatures": signatures,
        "edges": edges,
        "concrete_transition_profiles": len(profiles),
        "profiles_by_level": profiles_by_level,
        "levels": levels,
        "maps": maps,
    }


def greatest_set_simulation(
    signatures: set[tuple[int, int]],
    edges: set[tuple[tuple[int, int], int, tuple[int, int]]],
) -> dict[str, Any]:
    ordered = sorted(signatures)
    index = {signature: position for position, signature in enumerate(ordered)}
    state_count = len(ordered)
    subset_count = 1 << state_count

    post = [[0] * 4 for _ in ordered]
    for source, digit, target in edges:
        post[index[source]][digit] |= 1 << index[target]

    subset_post = [[0] * 4 for _ in range(subset_count)]
    for subset in range(1, subset_count):
        low = subset & -subset
        position = low.bit_length() - 1
        previous = subset ^ low
        for digit in range(4):
            subset_post[subset][digit] = (
                subset_post[previous][digit] | post[position][digit]
            )

    good = {
        (current, shadow_set)
        for current in range(state_count)
        for shadow_set in range(1, subset_count)
    }
    removed_rounds: list[int] = []
    while True:
        removed: list[tuple[int, int]] = []
        for current, shadow_set in good:
            valid = True
            for digit in range(4):
                current_targets = post[current][digit]
                if not current_targets:
                    continue
                shadow_targets = subset_post[shadow_set][digit]
                if not shadow_targets:
                    valid = False
                    break
                remaining = current_targets
                while remaining:
                    low = remaining & -remaining
                    target = low.bit_length() - 1
                    remaining ^= low
                    if (target, shadow_targets) not in good:
                        valid = False
                        break
                if not valid:
                    break
            if not valid:
                removed.append((current, shadow_set))
        if not removed:
            break
        for pair in removed:
            good.remove(pair)
        removed_rounds.append(len(removed))

    singleton_rows: dict[str, list[str]] = {}
    singleton_count = 0
    for current, signature in enumerate(ordered):
        simulators = []
        for shadow, shadow_signature in enumerate(ordered):
            if (current, 1 << shadow) in good:
                simulators.append(format_signature(shadow_signature))
                singleton_count += 1
        singleton_rows[format_signature(signature)] = simulators

    top_index = index[TOP_SIGNATURE]
    top_simulated = [
        format_signature(ordered[current])
        for current in range(state_count)
        if (current, 1 << top_index) in good
    ]
    return {
        "signature_count": state_count,
        "nonempty_shadow_subsets": subset_count - 1,
        "all_candidate_pairs": state_count * (subset_count - 1),
        "greatest_fixed_point_pairs": len(good),
        "removed_by_round": removed_rounds,
        "fixed_point_rounds": len(removed_rounds),
        "singleton_simulations": singleton_count,
        "singleton_simulators": singleton_rows,
        "universal_singleton": format_signature(TOP_SIGNATURE),
        "universal_singleton_simulates": top_simulated,
        "ordered_signatures": [format_signature(row) for row in ordered],
        "good": good,
        "index": index,
    }


def concrete_lift_failure(
    phase_row: dict[str, Any], simulation: dict[str, Any]
) -> dict[str, Any]:
    levels = phase_row["levels"]
    maps = phase_row["maps"]
    current = 12
    current_complexity = 2
    depth = 1
    residue = current % (4**depth)
    source_signature = maps[current_complexity][current]
    shadows = sorted(
        state
        for state in levels[current_complexity - 1]
        if state % (4**depth) == residue
    )
    source_index = simulation["index"][source_signature]
    top_index = simulation["index"][TOP_SIGNATURE]
    abstract_good = (source_index, 1 << top_index) in simulation["good"]
    if source_signature != (0b0010, 0b1100):
        raise AssertionError("small source signature changed")
    if not abstract_good or shadows:
        raise AssertionError("concrete abstraction counterexample failed")
    return {
        "phase": "p",
        "current_complexity": current_complexity,
        "current_state": current,
        "current_state_hex": hex(current),
        "current_signature": format_signature(source_signature),
        "cylinder_depth": depth,
        "cylinder_residue": residue,
        "previous_frontier": sorted(levels[current_complexity - 1]),
        "same_cylinder_previous_states": shadows,
        "abstract_universal_shadow": format_signature(TOP_SIGNATURE),
        "abstract_simulation_accepts": abstract_good,
        "consequence": (
            "Signature simulation does not imply a same-cylinder adjacent frontier "
            "shadow because the quotient forgets residue and concrete realization."
        ),
    }


def strip_internal(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in row.items()
        if key not in {"signatures", "edges", "levels", "maps"}
    }


def run_campaign(
    maximum_complexity: int = DEFAULT_MAXIMUM_COMPLEXITY,
) -> dict[str, Any]:
    if not 8 <= maximum_complexity <= ABSOLUTE_MAXIMUM_COMPLEXITY:
        raise SimulationCampaignLimitError("maximum complexity outside controlled range")

    phases = {
        phase: phase_graph(phase, maximum_complexity) for phase in PHASES
    }
    signatures = phases["p"]["signatures"] | phases["u"]["signatures"]
    edges = phases["p"]["edges"] | phases["u"]["edges"]
    if len(signatures) != 12:
        raise AssertionError("signature alphabet did not close at twelve symbols")

    simulation = greatest_set_simulation(signatures, edges)
    concrete = concrete_lift_failure(phases["p"], simulation)
    simulation_public = {
        key: value
        for key, value in simulation.items()
        if key not in {"good", "index"}
    }
    payload: dict[str, Any] = {
        "status": "finite-greatest-signature-simulation-and-concrete-no-go",
        "maximum_complexity": maximum_complexity,
        "signature_graph": {
            "signatures": len(signatures),
            "phase_p_labelled_edges": len(phases["p"]["edges"]),
            "phase_u_labelled_edges": len(phases["u"]["edges"]),
            "union_labelled_edges": len(edges),
            "phase_graphs_identical": phases["p"]["edges"] == phases["u"]["edges"],
        },
        "theorem": {
            "greatest_set_simulation": (
                "For a finite digit-labelled signature graph, (s,B) survives the "
                "greatest fixed point exactly when every labelled successor of s is "
                "again simulated by the deterministic shadow update Post_d(B)."
            ),
            "abstraction_no_go": (
                "A surviving signature-level simulation does not imply an adjacent "
                "same-cylinder frontier shadow; residue and realization consistency "
                "were discarded by the signature quotient."
            ),
        },
        "simulation": simulation_public,
        "concrete_lift_failure": concrete,
        "phases": {phase: strip_internal(row) for phase, row in phases.items()},
        "scientific_boundary": (
            "The fixed point is exact for the configured finite signature graph, and "
            "the concrete lifting failure is exact. The 194-edge stabilization and "
            "transition-profile growth are finite evidence. This result does not prove "
            "an all-depth concrete simulation, the adjacent-shadow inclusion, phase-"
            "complexity divergence, exclusion of eventual period two, or Rule 30 "
            "center nonperiodicity."
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--maximum-complexity", type=int, default=DEFAULT_MAXIMUM_COMPLEXITY
    )
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.maximum_complexity), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
