from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_residual_profile_refinement.py"
)
SPEC = importlib.util.spec_from_file_location("residual_profile", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def test_generator_and_frontier_start() -> None:
    assert MODULE.forward_generator("t", 1) == 7
    assert MODULE.forward_generator("u", 1) == 6
    assert MODULE.forward_generator("p", 1) == 6
    levels = MODULE.build_levels(4)
    assert levels[1] == {1}
    assert levels[2] == {6, 7}


def test_local_pair_and_lift_are_concrete() -> None:
    levels = MODULE.build_levels(10)
    nodes = []
    for complexity in range(2, 8):
        for current in levels[complexity]:
            for shadow in levels[complexity - 1]:
                node = MODULE.PairNode(complexity, current, shadow)
                if MODULE.local_pair(levels, node) is not None:
                    nodes.append(node)
    assert nodes
    node = nodes[0]
    for digit in range(4):
        lifted = MODULE.lift_pair(levels, node, digit)
        if lifted is not None:
            assert lifted.current in levels[lifted.complexity]
            assert lifted.shadow in levels[lifted.complexity - 1]
            assert MODULE.local_pair(levels, lifted) is not None


def test_residual_profile_exactly_controls_short_words() -> None:
    levels = MODULE.build_levels(11)
    nodes = []
    for complexity in range(2, 7):
        for current in levels[complexity]:
            for shadow in levels[complexity - 1]:
                node = MODULE.PairNode(complexity, current, shadow)
                if MODULE.local_pair(levels, node) is not None:
                    nodes.append(node)
    groups = {}
    for node in nodes:
        groups.setdefault(MODULE.residual_profile(levels, node, 2), []).append(node)
    for group in groups.values():
        baseline = group[0]
        for node in group[1:]:
            for length in range(3):
                for word_value in range(4**length):
                    digits = tuple(
                        (word_value >> (2 * (length - 1 - index))) & 3
                        for index in range(length)
                    )
                    assert MODULE.follows_word(levels, baseline, digits) == MODULE.follows_word(
                        levels, node, digits
                    )


def test_default_campaign_totals() -> None:
    result = MODULE.run_campaign()
    assert result["outputs_built"] == 461168
    assert result["gap_222_occurrences"] == 10
    assert result["dominant_failures"] == 0
    assert result["minimum_defect_histogram"] == {"0": 10}
    assert result["source_nodes"] == 16
    assert result["profile_nodes"] == 16


def test_default_partition_stabilizes_after_radius_one() -> None:
    rows = MODULE.run_campaign()["partitions"]
    assert [row["level_classes"] for row in rows] == [9, 13, 13, 13]
    assert [row["unlevelled_classes"] for row in rows] == [3, 12, 12, 12]
    assert rows[1]["level_classes_split_next"] == 0
    assert rows[2]["level_classes_split_next"] == 0


def test_default_certificate_is_stable() -> None:
    assert (
        MODULE.run_campaign()["certificate_sha256"]
        == "93f766adf07df6f79c27ce51eb0ff857638750cf02ea7b8448e9e5eda1accb6f"
    )


def test_controlled_limits() -> None:
    with pytest.raises(MODULE.ResidualProfileLimitError):
        MODULE.run_campaign(campaign_maximum=19)
    with pytest.raises(MODULE.ResidualProfileLimitError):
        MODULE.run_campaign(radius=4)
