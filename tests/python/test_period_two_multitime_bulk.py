from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_multitime_bulk.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_multitime_bulk", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_one_step_bulk_and_truth_table() -> None:
    result = MODULE.verify_one_step_bulk(12)
    assert result["all_checks_pass"]
    assert result["bulk_truth_table_hex"] == "0x696969aa"
    assert result["right_permutivity_checks"] == 16


def test_multitime_cones() -> None:
    result = MODULE.verify_multitime_cones(3)
    assert result["all_checks_pass"]
    assert result["total_cone_checks"] == 67648
    assert [row["input_cone_width"] for row in result["lag_rows"]] == [5, 9, 13]


def test_constructive_block_surjectivity() -> None:
    result = MODULE.verify_block_surjectivity(3, 5)
    assert result["all_checks_pass"]
    assert result["constructive_checks"] == 558


def test_solver_preserves_fixed_context() -> None:
    lag = 2
    target = (1, 0, 1, 1)
    variable_positions = {index + 2 * lag for index in range(len(target))}
    fixed = {
        position: (position + 1) & 1
        for position in range(-2 * lag, len(target) + 2 * lag)
        if position not in variable_positions
    }
    solved = MODULE.solve_bulk_target(lag, target, fixed)
    assert all(solved[position] == value for position, value in fixed.items())
    produced = MODULE.bulk_iterate(solved, lag, 0, len(target) - 1)
    assert tuple(produced[index] for index in range(len(target))) == target


def test_campaign_certificate_is_deterministic() -> None:
    first = MODULE.run_campaign(2, 3)
    second = MODULE.run_campaign(2, 3)
    assert first == second
    assert len(first["certificate_sha256"]) == 64


def test_resource_caps() -> None:
    with pytest.raises(MODULE.MultiTimeBulkLimitError):
        MODULE.run_campaign(MODULE.ABSOLUTE_MAXIMUM_LAG + 1, 1)
    with pytest.raises(MODULE.MultiTimeBulkLimitError):
        MODULE.run_campaign(1, MODULE.ABSOLUTE_MAXIMUM_TARGET_WIDTH + 1)
