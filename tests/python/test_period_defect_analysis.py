from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_defect.py"
)
SPEC = importlib.util.spec_from_file_location("period_defect_analysis", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def test_two_p_step_evaluators_match_hand_values_and_validate() -> None:
    # p=1: F(x)_0 = left XOR (center OR right).
    for assignment in range(8):
        left = assignment & 1
        center = (assignment >> 1) & 1
        right = (assignment >> 2) & 1
        expected = left ^ (center | right)
        assert module.iterated_center_cell_array(1, assignment) == expected
        assert module.iterated_center_packed(1, assignment) == expected
    with pytest.raises(ValueError, match="positive"):
        module.iterated_center_cell_array(0, 0)
    with pytest.raises(ValueError, match="does not fit"):
        module.iterated_center_packed(1, 8)


def test_mobius_transform_known_or_function() -> None:
    # x OR y = x XOR y XOR xy over GF(2).
    assert module.mobius_anf(bytes((0, 1, 1, 1)), 2) == bytearray(
        (0, 1, 1, 1)
    )
    with pytest.raises(ValueError, match=r"2\*\*variables"):
        module.mobius_anf(bytes((0, 1)), 2)


def test_period_one_defect_and_solved_left_constraint() -> None:
    result = module.run_campaign(minimum_period=1, maximum_period=1)
    summary = result["period_summaries"][0]
    assert summary["period_constraint_solutions"] == 4
    assert summary["left_permutive"] is True
    assert summary["solved_left_constraint_verified"] is True
    assert summary["essential_spatial_positions"] == [-1, 0, 1]
    assert summary["algebraic_degree"] == 2
    assert summary["highest_degree_monomials"] == [[0, 1]]
    assert summary["matches_reference_top_pattern"] is True


def test_small_campaign_exact_patterns_and_determinism() -> None:
    first = module.run_campaign(minimum_period=1, maximum_period=4)
    second = module.run_campaign(minimum_period=1, maximum_period=4)
    assert first == second
    assert first["coverage"]["assignments_exhausted"] == 680
    assert first["coverage"]["independent_oracles"] == 2
    assert first["all_periods_use_full_causal_cone"] is True
    assert first["all_periods_match_linear_degree_pattern"] is True
    assert first["all_periods_match_reference_top_pattern"] is True
    assert first["structural_collapse_periods"] == []
    assert [
        summary["algebraic_degree"]
        for summary in first["period_summaries"]
    ] == [2, 3, 5, 7]
    assert [
        summary["highest_degree_monomials"]
        for summary in first["period_summaries"]
    ] == [
        [[0, 1]],
        [[-1, 1, 2], [0, 1, 2]],
        [[-1, 0, 1, 2, 3]],
        [[-2, -1, 0, 1, 2, 3, 4]],
    ]


def test_work_and_resource_caps_fail_closed() -> None:
    work = module.estimate_work(1, 2)
    assert work.assignments == 40
    assert work.mobius_updates == 92
    with pytest.raises(ValueError, match="1 <= minimum"):
        module.estimate_work(2, 1)
    with pytest.raises(module.PeriodDefectLimitError, match="assignments"):
        module.run_campaign(
            minimum_period=1,
            maximum_period=4,
            max_total_assignments=100,
        )
    with pytest.raises(module.PeriodDefectLimitError, match="Mobius"):
        module.run_campaign(
            minimum_period=1,
            maximum_period=4,
            max_mobius_updates=100,
        )
    with pytest.raises(module.PeriodDefectLimitError, match="period"):
        module.run_campaign(
            minimum_period=1,
            maximum_period=3,
            max_period=2,
        )


def test_script_emits_strict_finite_scope_payload() -> None:
    completed = subprocess.run(
        (
            sys.executable,
            str(SCRIPT),
            "--maximum-period",
            "3",
        ),
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == "problem1-period-defect-anf-v1"
    assert payload["question"] == "problem1"
    assert payload["status"] == "finite-exhaustive"
    assert payload["result_summary"]["coverage"]["assignments_exhausted"] == 168
    assert any(
        "does not imply behavior of one fixed seed" in limitation
        for limitation in payload["limitations"]
    )
