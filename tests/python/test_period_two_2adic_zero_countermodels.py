from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    ROOT
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_2adic_zero_countermodels.py"
)
SPEC = importlib.util.spec_from_file_location(
    "period_two_2adic_zero_countermodels", SCRIPT
)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


@pytest.mark.parametrize(
    ("numerator", "residue"),
    ((5, 7), (1, 11)),
)
def test_rational_fixed_points_have_required_branch_residues(
    numerator: int, residue: int
) -> None:
    for width in range(4, 65):
        assert module.rational_residue(numerator, 3, width) % 16 == residue


def test_both_fixed_points_hold_through_width_64() -> None:
    results = module.verify_fixed_points(64)
    assert [result["q_name"] for result in results] == ["u", "t"]
    assert all(result["quotient_checks"] == 61 for result in results)
    assert all(result["all_checks_pass"] is True for result in results)


def test_same_branch_step_loses_exactly_two_bits_of_agreement() -> None:
    for spec in module.fixed_point_specs():
        for width in range(8, 25):
            fixed = module.rational_residue(
                spec["numerator"], spec["denominator"], width + 2
            )
            perturbed = fixed ^ (1 << width)
            fixed_out = module.zero_branch_step_from_residue(
                fixed, input_width=width + 2, q_name=spec["q_name"]
            )
            perturbed_out = module.zero_branch_step_from_residue(
                perturbed,
                input_width=width + 2,
                q_name=spec["q_name"],
            )
            difference = fixed_out ^ perturbed_out
            assert difference & -difference == 1 << (width - 2)


def test_finite_truncations_meet_linear_shadowing_bound() -> None:
    results = module.verify_finite_truncation_shadowing(64)
    for result in results:
        for row in result["rows"]:
            assert row["observed_zero_steps"] >= row["guaranteed_zero_steps"]
            assert len(row["guaranteed_branch_prefix"]) == row[
                "guaranteed_zero_steps"
            ]


def test_campaign_certificate_is_deterministic() -> None:
    first = module.run_campaign(32)
    second = module.run_campaign(32)
    assert first == second
    assert len(first["certificate_sha256"]) == 64


def test_campaign_limits_fail_closed() -> None:
    with pytest.raises(module.CountermodelLimitError, match="width"):
        module.run_campaign(257)


def test_script_emits_scoped_json() -> None:
    completed = subprocess.run(
        (sys.executable, str(SCRIPT), "--maximum-width", "32"),
        check=True,
        capture_output=True,
        text=True,
        timeout=20,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == (
        "problem1-period-two-2adic-zero-countermodels-v1"
    )
    assert payload["status"] == "finite-exhaustive"
    assert any(
        "actual period-two schedule is not constant" in limitation
        for limitation in payload["limitations"]
    )
