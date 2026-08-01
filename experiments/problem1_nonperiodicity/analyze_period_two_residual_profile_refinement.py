#!/usr/bin/env python3
"""Refine synchronized/full endpoint pairs by their legal residual languages."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any

DEFAULT_CAMPAIGN_MAXIMUM = 16
DEFAULT_RADIUS = 3
ABSOLUTE_CAMPAIGN_MAXIMUM = 18
ABSOLUTE_RADIUS = 3
SCHEDULE_CAP = 64


class ResidualProfileLimitError(RuntimeError):
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
        levels.append({c for s in levels[-1] for c in frontier_children(s)})
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
        state = forward_generator(
            branch, forward_generator("p", (state - 3) >> 2)
        )
        word.append(branch)
    raise ResidualProfileLimitError("forced schedule reached safety cap")


def admissible(word: str) -> bool:
    return all(factor not in word for factor in ("uu", "ttttt", "ututtu"))


def mask_sequence(
    levels: list[set[int]], complexity: int, state: int, depth: int
) -> tuple[int, ...]:
    result: list[int] = []
    for step in range(depth):
        state >>= 2
        result.append(fiber_mask(levels, complexity - 1 - step, state))
    return tuple(result)


def dominates(current: tuple[int, ...], shadow: tuple[int, ...]) -> bool:
    return all(not (a & ~b) for a, b in zip(current, shadow))


def synchronized_or_full(
    current: tuple[int, ...], shadow: tuple[int, ...]
) -> bool:
    return all(b == 0b1111 or b == a for a, b in zip(current, shadow))


@dataclass(frozen=True, order=True)
class PairNode:
    complexity: int
    current: int
    shadow: int


def local_pair(
    levels: list[set[int]], node: PairNode
) -> tuple[int, int] | None:
    if node.current not in levels[node.complexity]:
        return None
    if node.shadow not in levels[node.complexity - 1]:
        return None
    current_mask = fiber_mask(levels, node.complexity, node.current)
    shadow_mask = fiber_mask(levels, node.complexity - 1, node.shadow)
    if shadow_mask != 0b1111 and shadow_mask != current_mask:
        return None
    return current_mask, shadow_mask


def lift_pair(
    levels: list[set[int]], node: PairNode, digit: int
) -> PairNode | None:
    child = PairNode(
        node.complexity + 1,
        4 * node.current + digit,
        4 * node.shadow + digit,
    )
    return child if local_pair(levels, child) is not None else None


def residual_profile(
    levels: list[set[int]],
    node: PairNode,
    radius: int,
    memo: dict[tuple[PairNode, int], tuple[Any, ...]] | None = None,
) -> tuple[Any, ...]:
    """Return the exact typed legal-continuation tree through ``radius`` lifts."""
    if radius < 0:
        raise ValueError("radius must be nonnegative")
    if memo is None:
        memo = {}
    key = (node, radius)
    if key in memo:
        return memo[key]
    masks = local_pair(levels, node)
    if masks is None:
        raise ValueError("residual profile requires a synchronized/full pair")
    children: tuple[Any, ...]
    if radius == 0:
        children = ()
    else:
        children = tuple(
            None
            if (child := lift_pair(levels, node, digit)) is None
            else residual_profile(levels, child, radius - 1, memo)
            for digit in range(4)
        )
    result: tuple[Any, ...] = (masks[0], masks[1], children)
    memo[key] = result
    return result


def follows_word(
    levels: list[set[int]], node: PairNode, word: tuple[int, ...]
) -> bool:
    if local_pair(levels, node) is None:
        return False
    for digit in word:
        lifted = lift_pair(levels, node, digit)
        if lifted is None:
            return False
        node = lifted
    return True


def selected_certificates(
    levels: list[set[int]], campaign_maximum: int
) -> tuple[list[dict[str, Any]], set[PairNode]]:
    rows: list[dict[str, Any]] = []
    source_nodes: set[PairNode] = set()
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
                residue = current % modulus
                current_masks = mask_sequence(levels, complexity, current, depth)
                candidates: list[tuple[int, int, tuple[int, ...]]] = []
                for shadow in levels[complexity - 1]:
                    if shadow % modulus != residue:
                        continue
                    shadow_masks = mask_sequence(
                        levels, complexity - 1, shadow, depth
                    )
                    if not dominates(current_masks, shadow_masks):
                        continue
                    if not synchronized_or_full(current_masks, shadow_masks):
                        continue
                    defects = sum(mask != 0b1111 for mask in shadow_masks)
                    candidates.append((defects, shadow, shadow_masks))
                if not candidates:
                    rows.append(
                        {
                            "complexity": complexity,
                            "current": current,
                            "cut": cut,
                            "depth": depth,
                            "failure": True,
                        }
                    )
                    continue
                defects, shadow, shadow_masks = min(candidates)
                rows.append(
                    {
                        "complexity": complexity,
                        "current": current,
                        "cut": cut,
                        "depth": depth,
                        "shadow": shadow,
                        "defects": defects,
                        "shadow_masks": shadow_masks,
                        "failure": False,
                    }
                )
                for step in range(1, depth + 1):
                    source_nodes.add(
                        PairNode(
                            complexity - step,
                            current >> (2 * step),
                            shadow >> (2 * step),
                        )
                    )
    return rows, source_nodes


def partition_metrics(
    levels: list[set[int]], nodes: set[PairNode], maximum_radius: int
) -> list[dict[str, int]]:
    memo: dict[tuple[PairNode, int], tuple[Any, ...]] = {}
    profiles = {
        radius: {
            node: residual_profile(levels, node, radius, memo)
            for node in nodes
        }
        for radius in range(maximum_radius + 1)
    }
    result: list[dict[str, int]] = []
    for radius in range(maximum_radius + 1):
        level_groups: dict[tuple[int, tuple[Any, ...]], list[PairNode]] = defaultdict(list)
        unlevelled: dict[tuple[Any, ...], list[PairNode]] = defaultdict(list)
        for node, profile in profiles[radius].items():
            level_groups[(node.complexity, profile)].append(node)
            unlevelled[profile].append(node)
        row = {
            "radius": radius,
            "level_classes": len(level_groups),
            "unlevelled_classes": len(unlevelled),
            "level_collision_classes": sum(len(v) > 1 for v in level_groups.values()),
            "unlevelled_collision_classes": sum(len(v) > 1 for v in unlevelled.values()),
            "maximum_level_class_size": max(map(len, level_groups.values()), default=0),
        }
        if radius < maximum_radius:
            row["level_classes_split_next"] = sum(
                len({profiles[radius + 1][node] for node in group}) > 1
                for group in level_groups.values()
            )
            row["unlevelled_classes_split_next"] = sum(
                len({profiles[radius + 1][node] for node in group}) > 1
                for group in unlevelled.values()
            )
        result.append(row)
    return result


def run_campaign(
    campaign_maximum: int = DEFAULT_CAMPAIGN_MAXIMUM,
    radius: int = DEFAULT_RADIUS,
) -> dict[str, Any]:
    if not 4 <= campaign_maximum <= ABSOLUTE_CAMPAIGN_MAXIMUM:
        raise ResidualProfileLimitError("campaign maximum outside controlled range")
    if not 1 <= radius <= ABSOLUTE_RADIUS:
        raise ResidualProfileLimitError("radius outside controlled range")
    frontier_maximum = campaign_maximum + radius + 1
    levels = build_levels(frontier_maximum)
    rows, source_nodes = selected_certificates(levels, campaign_maximum)
    failures = sum(row["failure"] for row in rows)
    defect_histogram = Counter(
        row["defects"] for row in rows if not row["failure"]
    )
    profile_nodes = {
        node
        for node in source_nodes
        if node.complexity <= frontier_maximum - radius - 1
    }
    partitions = partition_metrics(levels, profile_nodes, radius)
    payload: dict[str, Any] = {
        "status": "exact-residual-profile-recursion-and-finite-refinement-census",
        "phase": "u",
        "campaign_maximum_complexity": campaign_maximum,
        "frontier_maximum_complexity": frontier_maximum,
        "maximum_radius": radius,
        "outputs_built": sum(len(levels[k]) for k in range(1, frontier_maximum + 1)),
        "gap_222_occurrences": len(rows),
        "dominant_failures": failures,
        "minimum_defect_histogram": {
            str(key): value for key, value in sorted(defect_histogram.items())
        },
        "source_nodes": len(source_nodes),
        "profile_nodes": len(profile_nodes),
        "partitions": partitions,
        "theorem": {
            "residual_profile": (
                "R_0 records the current and shadow fibers. R_(r+1) records R_0 "
                "and, for each digit, either a dead marker or R_r of the exact "
                "synchronized/full common-digit lift."
            ),
            "exact_language": (
                "Equality of radius-r residual profiles is exactly equality of the "
                "typed synchronized/full continuation trees through r lifts."
            ),
        },
        "scientific_boundary": (
            "The recursion theorem is exact. Partition counts are finite and do not "
            "show that the residual alphabet closes at arbitrary complexity."
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
