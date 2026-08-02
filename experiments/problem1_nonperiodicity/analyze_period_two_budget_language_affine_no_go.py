#!/usr/bin/env python3
"""Defect-budget continuation languages and affine-separation quotient tests."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

DEFAULT_CAMPAIGN_MAXIMUM = 16
ABSOLUTE_CAMPAIGN_MAXIMUM = 18
DEFAULT_RADIUS = 5
ABSOLUTE_RADIUS = 5
INITIAL_BUDGET = 3
SCHEDULE_CAP = 64


class BudgetLanguageLimitError(RuntimeError):
    pass


def forward_generator(name: str, state: int) -> int:
    stepped = state ^ ((state << 1) | (state << 2))
    if name == "t":
        return stepped
    if name == "u":
        return stepped ^ 1
    if name == "p":
        return stepped ^ 1 ^ (2 if state & 1 == 0 else 0)
    raise ValueError(name)


def frontier_children(state: int) -> tuple[int, ...]:
    return tuple(sorted({forward_generator(g, state) for g in "tup"}))


def build_levels(maximum_complexity: int) -> list[set[int]]:
    levels: list[set[int]] = [set(), {1}]
    for _ in range(2, maximum_complexity + 1):
        levels.append({child for state in levels[-1] for child in frontier_children(state)})
    return levels


def fiber_mask(levels: list[set[int]], complexity: int, state: int) -> int:
    return sum(
        1 << digit
        for digit in range(4)
        if 4 * state + digit in levels[complexity + 1]
    )


def forced_zero_schedule(state: int, cap: int = SCHEDULE_CAP) -> str:
    word: list[str] = []
    for _ in range(cap):
        residue = state & 15
        if residue == 7:
            branch = "u"
        elif residue == 11:
            branch = "t"
        else:
            return "".join(word)
        state = forward_generator(branch, forward_generator("p", (state - 3) >> 2))
        word.append(branch)
    raise BudgetLanguageLimitError("forced schedule reached safety cap")


def admissible(word: str) -> bool:
    return all(factor not in word for factor in ("uu", "ttttt", "ututtu"))


def mask_sequence(
    levels: list[set[int]], complexity: int, state: int, depth: int
) -> tuple[int, ...]:
    masks: list[int] = []
    for step in range(depth):
        state >>= 2
        masks.append(fiber_mask(levels, complexity - 1 - step, state))
    return tuple(masks)


@dataclass(frozen=True, order=True)
class PairNode:
    complexity: int
    current: int
    shadow: int


@dataclass(frozen=True, order=True)
class BudgetState:
    node: PairNode
    budget: int


def local_masks(levels: list[set[int]], node: PairNode) -> tuple[int, int] | None:
    if node.current not in levels[node.complexity]:
        return None
    if node.shadow not in levels[node.complexity - 1]:
        return None
    current = fiber_mask(levels, node.complexity, node.current)
    shadow = fiber_mask(levels, node.complexity - 1, node.shadow)
    if shadow != 0b1111 and shadow != current:
        return None
    return current, shadow


def local_cost(levels: list[set[int]], node: PairNode) -> int:
    masks = local_masks(levels, node)
    if masks is None:
        raise ValueError("local cost requires a synchronized/full pair")
    return int(masks[1] != 0b1111)


def affine_separation(node: PairNode) -> int:
    return node.current - 4 * node.shadow


def lift_pair(
    levels: list[set[int]], node: PairNode, digit: int
) -> PairNode | None:
    child = PairNode(
        node.complexity + 1,
        4 * node.current + digit,
        4 * node.shadow + digit,
    )
    return child if local_masks(levels, child) is not None else None


def lift_budget_state(
    levels: list[set[int]], state: BudgetState, digit: int
) -> BudgetState | None:
    cost = local_cost(levels, state.node)
    if cost > state.budget:
        return None
    child = lift_pair(levels, state.node, digit)
    if child is None:
        return None
    result = BudgetState(child, state.budget - cost)
    return result if local_cost(levels, child) <= result.budget else None


def budget_language_profile(
    levels: list[set[int]],
    state: BudgetState,
    radius: int,
    memo: dict[tuple[BudgetState, int], tuple[Any, ...]] | None = None,
) -> tuple[Any, ...] | None:
    """Return the exact common-digit language feasible within the defect budget."""
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    if local_cost(levels, state.node) > state.budget:
        return None
    if memo is None:
        memo = {}
    key = (state, radius)
    if key in memo:
        return memo[key]
    if radius == 0:
        result: tuple[Any, ...] = ()
    else:
        result = tuple(
            None
            if (child := lift_budget_state(levels, state, digit)) is None
            else budget_language_profile(levels, child, radius - 1, memo)
            for digit in range(4)
        )
    memo[key] = result
    return result


def feasible_words(
    levels: list[set[int]], state: BudgetState, maximum_length: int
) -> set[tuple[int, ...]]:
    if local_cost(levels, state.node) > state.budget:
        return set()
    result: set[tuple[int, ...]] = {()}
    frontier = {(): state}
    for _ in range(maximum_length):
        following: dict[tuple[int, ...], BudgetState] = {}
        for word, current in frontier.items():
            for digit in range(4):
                child = lift_budget_state(levels, current, digit)
                if child is not None:
                    following[word + (digit,)] = child
        result.update(following)
        frontier = following
    return result


def selected_certificates(
    levels: list[set[int]], campaign_maximum: int
) -> tuple[list[dict[str, Any]], set[PairNode]]:
    rows: list[dict[str, Any]] = []
    nodes: set[PairNode] = set()
    for complexity in range(2, campaign_maximum + 1):
        for current in sorted(levels[complexity]):
            if current & 3 != 3:
                continue
            schedule = forced_zero_schedule(current)
            for cut in range(len(schedule) + 1):
                if schedule[cut : cut + 6] != "ututut":
                    continue
                if not admissible(schedule[:cut] + "utututu"):
                    continue
                depth = cut + 1
                modulus = 4**depth
                current_masks = mask_sequence(levels, complexity, current, depth)
                candidates: list[tuple[int, int]] = []
                for shadow in levels[complexity - 1]:
                    if shadow % modulus != current % modulus:
                        continue
                    shadow_masks = mask_sequence(levels, complexity - 1, shadow, depth)
                    if any(a & ~b for a, b in zip(current_masks, shadow_masks)):
                        continue
                    if any(b != 0b1111 and b != a for a, b in zip(current_masks, shadow_masks)):
                        continue
                    candidates.append((sum(mask != 0b1111 for mask in shadow_masks), shadow))
                if not candidates:
                    rows.append({"complexity": complexity, "current": current, "cut": cut, "failure": True})
                    continue
                defects, shadow = min(candidates)
                rows.append(
                    {
                        "complexity": complexity,
                        "current": current,
                        "cut": cut,
                        "depth": depth,
                        "shadow": shadow,
                        "defects": defects,
                        "failure": False,
                    }
                )
                for step in range(1, depth + 1):
                    nodes.add(
                        PairNode(
                            complexity - step,
                            current >> (2 * step),
                            shadow >> (2 * step),
                        )
                    )
    return rows, nodes


def close_budget_states(
    levels: list[set[int]], states: set[BudgetState], maximum_complexity: int
) -> set[BudgetState]:
    result = set(states)
    frontier = set(states)
    while frontier:
        following: set[BudgetState] = set()
        for state in frontier:
            if state.node.complexity >= maximum_complexity:
                continue
            for digit in range(4):
                child = lift_budget_state(levels, state, digit)
                if child is not None and child not in result:
                    following.add(child)
        result.update(following)
        frontier = following
    return result


def partition_metrics(
    levels: list[set[int]], states: set[BudgetState], maximum_radius: int
) -> list[dict[str, int]]:
    memo: dict[tuple[BudgetState, int], tuple[Any, ...]] = {}
    profiles = {
        radius: {
            state: budget_language_profile(levels, state, radius, memo)
            for state in states
        }
        for radius in range(maximum_radius + 1)
    }
    rows: list[dict[str, int]] = []
    for radius in range(maximum_radius + 1):
        groups: dict[tuple[Any, ...] | None, list[BudgetState]] = defaultdict(list)
        for state, profile in profiles[radius].items():
            groups[profile].append(state)
        row = {"radius": radius, "classes": len(groups)}
        if radius < maximum_radius:
            row["classes_split_next"] = sum(
                len({profiles[radius + 1][state] for state in group}) > 1
                for group in groups.values()
            )
        rows.append(row)
    return rows


def affine_quotient_metrics(
    levels: list[set[int]], states: set[BudgetState], bit_counts: tuple[int, ...]
) -> list[dict[str, int]]:
    rows: list[dict[str, int]] = []
    for bits in bit_counts:
        modulus = 1 << bits

        def feature(state: BudgetState) -> tuple[int, int, int, int]:
            current_mask, shadow_mask = local_masks(levels, state.node) or (0, 0)
            return (
                state.budget,
                current_mask,
                shadow_mask,
                affine_separation(state.node) % modulus,
            )

        transitions: dict[tuple[tuple[int, int, int, int], int], set[Any]] = defaultdict(set)
        for state in states:
            for digit in range(4):
                child = lift_budget_state(levels, state, digit)
                transitions[(feature(state), digit)].add(None if child is None else feature(child))
        rows.append(
            {
                "bits": bits,
                "classes": len({feature(state) for state in states}),
                "nondeterministic_class_digits": sum(len(targets) > 1 for targets in transitions.values()),
            }
        )
    return rows


def run_campaign(
    campaign_maximum: int = DEFAULT_CAMPAIGN_MAXIMUM,
    radius: int = DEFAULT_RADIUS,
) -> dict[str, Any]:
    if not 8 <= campaign_maximum <= ABSOLUTE_CAMPAIGN_MAXIMUM:
        raise BudgetLanguageLimitError("campaign maximum outside controlled range")
    if not 1 <= radius <= ABSOLUTE_RADIUS:
        raise BudgetLanguageLimitError("radius outside controlled range")
    frontier_maximum = campaign_maximum + radius + 1
    levels = build_levels(frontier_maximum)
    rows, source_nodes = selected_certificates(levels, campaign_maximum)
    source_states = {BudgetState(node, INITIAL_BUDGET) for node in source_nodes}
    closure_seeds = {
        state for state in source_states if state.node.complexity <= campaign_maximum - 3
    }
    closure = close_budget_states(levels, closure_seeds, campaign_maximum)
    partitions = partition_metrics(levels, closure, radius)
    affine = affine_quotient_metrics(levels, closure, (4, 6, 8, 10, 12))
    defects = Counter(row["defects"] for row in rows if not row["failure"])
    payload: dict[str, Any] = {
        "status": "exact-defect-budget-language-and-affine-modular-no-go",
        "phase": "u",
        "campaign_maximum_complexity": campaign_maximum,
        "frontier_maximum_complexity": frontier_maximum,
        "initial_defect_budget": INITIAL_BUDGET,
        "maximum_radius": radius,
        "outputs_built": sum(len(levels[k]) for k in range(1, frontier_maximum + 1)),
        "gap_222_occurrences": len(rows),
        "dominant_failures": sum(row["failure"] for row in rows),
        "minimum_defect_histogram": {str(k): v for k, v in sorted(defects.items())},
        "source_pairs": len(source_nodes),
        "closure_states": len(closure),
        "partitions": partitions,
        "affine_quotients": affine,
        "theorem": {
            "budget_language": (
                "A state is a synchronized/full endpoint pair with remaining defect budget b. "
                "The exact transition subtracts the current shadow defect and follows the same "
                "base-four digit when the concrete lifted pair exists and remains within budget."
            ),
            "profile_language": (
                "Equality of radius-r budget profiles is exactly equality of all common-digit "
                "words of length at most r realizable without exceeding the remaining budget."
            ),
            "affine_separation": (
                "For H(q,p)=q-4p, a common digit lift d sends H to 4H-3d exactly."
            ),
        },
        "scientific_boundary": (
            "The recursions are exact. Stabilization and modular-quotient counts are finite. "
            "They do not prove that every fixed algebraic quotient fails or establish an "
            "all-depth three-defect certificate."
        ),
    }
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["certificate_sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--campaign-maximum", type=int, default=DEFAULT_CAMPAIGN_MAXIMUM)
    parser.add_argument("--radius", type=int, default=DEFAULT_RADIUS)
    args = parser.parse_args()
    print(json.dumps(run_campaign(args.campaign_maximum, args.radius), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
