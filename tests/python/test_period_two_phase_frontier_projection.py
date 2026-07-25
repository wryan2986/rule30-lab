from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_phase_frontier_projection.py"
)
SPEC = importlib.util.spec_from_file_location("phase_frontier_projection", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_projection_identity_is_generator_blind() -> None:
    for parent in range(4096):
        expected = MODULE.projected_child_formula(parent)
        observed = {
            MODULE.forward_generator(name, parent) >> 2
            for name in ("t", "u", "p")
        }
        assert observed == {expected}


def test_one_level_projection_theorem() -> None:
    for phase in MODULE.PHASES:
        levels = MODULE.generate_levels(phase, 10)
        for complexity in range(2, 11):
            assert {
                value >> 2 for value in levels[complexity - 1]
            } <= levels[complexity - 2]


def test_nonempty_projection_fibers_have_size_two_to_four() -> None:
    for phase in MODULE.PHASES:
        levels = MODULE.generate_levels(phase, 10)
        for complexity in range(2, 11):
            row = MODULE.level_projection_row(
                levels[complexity - 2],
                levels[complexity - 1],
                complexity,
            )
            assert row["projection_violations"] == 0
            assert sum(row["fiber_histogram"].values()) == row["projected_parents"]


def test_iterated_projection_theorem() -> None:
    for phase in MODULE.PHASES:
        levels = MODULE.generate_levels(phase, 9)
        assert MODULE.verify_iterated_projection(levels) > 0


def test_known_counterexample_has_residual_phase_ancestors() -> None:
    u_levels = MODULE.generate_levels("u", 13)
    rows = MODULE.known_counterexample_ancestry(u_levels)
    assert [row["ancestor_hex"] for row in rows] == [
        "0x1bcd3a7",
        "0x1bcd3a",
        "0x1bcd3",
    ]
    assert [row["residual_complexity"] for row in rows] == [13, 11, 9]


def test_projection_inclusion_has_no_converse() -> None:
    levels = {
        phase: MODULE.generate_levels(phase, 4)
        for phase in MODULE.PHASES
    }
    rows = MODULE.verify_strict_nonconverse(levels)
    assert len(rows) == 2


def test_campaign_certificate_and_limit_guard() -> None:
    payload = MODULE.run_campaign(13)
    assert payload["certificate_sha256"] == (
        "c9f77e5de3d8b34df9ba7748543667ce876d843233fd3a4fcac331c8d93d03c4"
    )
    with pytest.raises(MODULE.ProjectionLimitError):
        MODULE.run_campaign(12)
    with pytest.raises(MODULE.ProjectionLimitError):
        MODULE.run_campaign(MODULE.ABSOLUTE_MAXIMUM_COMPLEXITY + 1)
