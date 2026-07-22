from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "experiments/problem1_nonperiodicity/analyze_period_two_schedule_coding.py"
SPEC = importlib.util.spec_from_file_location("schedule_coding", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_schedule_cylinders_and_exact_first_difference_law() -> None:
    result = module.verify_schedule_coding(8)
    assert result["levels"][-1]["distinct_cylinders"] == 256
    assert result["final_level_pair_checks"] == 32_640
    assert result["all_checks_pass"] is True


def test_eventually_periodic_obstruction_degree_input() -> None:
    result = module.verify_finite_degree_law(1 << 14)
    assert result["continuing_states_checked"] > 0
    assert result["degree_increment_per_zero_step"] == 2


def test_actual_seven_block_shadow_has_exact_304_bit_agreement() -> None:
    result = module.verify_periodic_shadow(512)
    assert result["period_word"] == "ttututt"
    assert result["common_branches"] == 151
    assert result["first_global_mismatch_block"] == 153
    assert result["survivor_2adic_agreement_bits"] == 304


def test_campaign_certificate_is_stable() -> None:
    result = module.run_campaign()
    assert result["certificate_sha256"] == (
        "9bf35a8386e6f5e5f50940b174535167e276b56dec13091c19f9e8def1645093"
    )


def test_limits_fail_closed() -> None:
    with pytest.raises(module.ScheduleCodingLimitError):
        module.run_campaign(maximum_coding_depth=13)
    with pytest.raises(module.ScheduleCodingLimitError):
        module.run_campaign(degree_check_limit=(1 << 20) + 1)
    with pytest.raises(ValueError):
        module.run_campaign(shadow_width=305)


def test_cli_emits_scoped_json() -> None:
    completed = subprocess.run(
        (sys.executable, str(SCRIPT), "--maximum-coding-depth", "6"),
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == "problem1-period-two-schedule-coding-v1"
    assert payload["status"] == "finite-exhaustive"
    assert any("does not exclude eventual center period two" in item for item in payload["limitations"])
