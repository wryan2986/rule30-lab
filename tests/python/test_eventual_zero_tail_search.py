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
    / "search_eventual_zero_tail.py"
)
SPEC = importlib.util.spec_from_file_location("eventual_zero_tail_search", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def test_zero_run_helpers() -> None:
    assert module.trailing_zero_run(b"") == 0
    assert module.trailing_zero_run(bytes((0, 0))) == 2
    assert module.trailing_zero_run(bytes((1, 0, 0))) == 2
    assert module.longest_zero_run_after_first_one(bytes((0, 1, 0, 0, 1, 0))) == 2
    assert module.longest_zero_run_after_first_one(bytes((0, 0))) == 2
    with pytest.raises(ValueError, match="zero and one"):
        module.trailing_zero_run(bytes((2,)))


def test_small_campaign_has_exact_coverage_and_cross_horizon_checks() -> None:
    result = module.run_campaign(
        max_preperiod=2,
        max_period=3,
        horizons=(8, 16, 32),
        max_reported_candidates=4,
    )
    assert result["coverage"]["descriptions"] == 49
    assert result["coverage"]["distinct_finite_trace_classes"] < 49
    assert result["coverage"]["reconstructions_completed"] == (
        3 * result["coverage"]["distinct_finite_trace_classes"]
    )
    assert result["coverage"]["cross_horizon_prefix_equalities_checked"] == (
        2 * result["coverage"]["distinct_finite_trace_classes"]
    )
    assert result["checkpoints"][-1]["horizon"] == 32
    assert result["checkpoints"][-1]["maximum_zero_run_after_first_one"] >= 0
    assert result["counterexample_lead_rule"].startswith("a trace class")


def test_campaign_is_deterministic() -> None:
    arguments = {
        "max_preperiod": 1,
        "max_period": 3,
        "horizons": (8, 16),
        "max_reported_candidates": 3,
    }
    first = module.run_campaign(**arguments)
    second = module.run_campaign(**arguments)
    assert first == second


def test_independent_horizon_prefixes_are_reported() -> None:
    result = module.run_campaign(
        max_preperiod=1,
        max_period=2,
        horizons=(4, 8, 16),
        max_reported_candidates=2,
    )
    for checkpoint in result["checkpoints"][1:]:
        assert checkpoint["classes_with_no_one_since_previous_checkpoint"] is not None
        assert (
            checkpoint["descriptions_with_no_one_since_previous_checkpoint"]
            is not None
        )


def test_resource_and_shape_validation() -> None:
    with pytest.raises(ValueError, match="strictly increasing"):
        module.run_campaign(
            max_preperiod=1, max_period=2, horizons=(8, 4)
        )
    with pytest.raises(ValueError, match="expose every bit"):
        module.run_campaign(
            max_preperiod=4, max_period=8, horizons=(8, 16)
        )
    with pytest.raises(module.EventualZeroTailLimitError, match="descriptions"):
        module.run_campaign(
            max_preperiod=2,
            max_period=3,
            horizons=(8, 16),
            max_descriptions=10,
        )
    with pytest.raises(module.EventualZeroTailLimitError, match="logical"):
        module.run_campaign(
            max_preperiod=2,
            max_period=3,
            horizons=(8, 16),
            max_logical_cell_updates=10,
        )


def test_script_emits_strict_bounded_record_payload() -> None:
    completed = subprocess.run(
        (
            sys.executable,
            str(SCRIPT),
            "--max-preperiod",
            "1",
            "--max-period",
            "2",
            "--horizons",
            "4,8,16",
            "--max-reported-candidates",
            "2",
        ),
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == "problem1-eventual-zero-tail-search-v1"
    assert payload["question"] == "problem1"
    assert payload["status"] == "finite-exhaustive"
    assert payload["result_summary"]["coverage"]["descriptions"] == 9
    assert payload["result_summary"]["counterexample_lead_trace_classes"] >= 0
    assert any(
        "does not prove Rule 30 center nonperiodicity" in limitation
        for limitation in payload["limitations"]
    )
