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
    / "analyze_period_two.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_analysis", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def test_exact_five_cell_phase_patterns() -> None:
    assert module.exact_phase_patterns(0) == [
        "01000",
        "10010",
        "01001",
        "10011",
    ]
    assert module.exact_phase_patterns(1) == [
        "11100",
        "01110",
        "01101",
        "01111",
    ]
    with pytest.raises(ValueError, match="center"):
        module.exact_phase_patterns(2)


def test_explicit_arbitrary_right_trace_refutes_zero_gap_seven() -> None:
    horizon = 16
    center = tuple(time & 1 for time in range(horizon + 1))
    right_word = 1_092
    right = tuple((right_word >> time) & 1 for time in range(horizon + 1))
    left = module.reconstruct_from_adjacent_columns(center, right)
    assert "".join(map(str, left)) == "1000000100000000"
    assert module.longest_zero_run(left) == (8, 8)
    assert module.first_adjacent_trace_extension_failure(center, right) == 2


def test_forced_half_line_implementations_match_and_validate() -> None:
    for phase in (0, 1):
        for seed in range(16):
            assert module.forced_half_line_trace_packed(
                seed, 64, phase=phase
            ) == module.forced_half_line_trace_cell_array(
                seed, 64, phase=phase
            )
    with pytest.raises(ValueError, match="invalid"):
        module.forced_half_line_trace_packed(-1, 8)


def test_small_campaign_is_deterministic_and_fails_closed() -> None:
    first = module.run_campaign(
        reconstruction_horizon=8,
        lift_width=128,
        half_line_steps=1_024,
    )
    second = module.run_campaign(
        reconstruction_horizon=8,
        lift_width=128,
        half_line_steps=1_024,
    )
    assert first == second
    cones = first["exact_two_phase_cones"]
    assert cones["all_four_right_pairs_allowed_in_both_phases"] is True
    assert [
        summary["maximum_reconstructed_zero_run"]
        for summary in first["arbitrary_adjacent_right_column"]
    ] == [6, 4]
    assert first["candidate_zero_run_bound_refuted"] is False
    assert "was not refuted at this horizon" in first["interpretation"]
    assert len(first["certificate_sha256"]) == 64
    assert first["coverage"]["arbitrary_right_traces_exhausted"] == 1_024
    assert first["forced_finite_right_half"][
        "two_independent_evaluators_agree"
    ] is True
    assert first["forced_finite_right_half"][
        "two_step_boundary_nor_identity_verified"
    ] is True
    with pytest.raises(module.PeriodTwoLimitError, match="horizon"):
        module.run_campaign(
            reconstruction_horizon=19,
            lift_width=128,
            half_line_steps=1_024,
        )
    with pytest.raises(module.PeriodTwoLimitError, match="lift width"):
        module.run_campaign(
            reconstruction_horizon=8,
            lift_width=4_097,
            half_line_steps=1_024,
        )
    with pytest.raises(module.PeriodTwoLimitError, match="half-line"):
        module.run_campaign(
            reconstruction_horizon=8,
            lift_width=128,
            half_line_steps=8_193,
        )
    with pytest.raises(ValueError, match="suffix-period"):
        module.matching_suffix_period(
            bytes(16), window=8, maximum_period=8
        )


def test_cli_emits_strict_finite_scope_json() -> None:
    completed = subprocess.run(
        (
            sys.executable,
            str(SCRIPT),
            "--reconstruction-horizon",
            "8",
            "--lift-width",
            "128",
            "--half-line-steps",
            "1024",
        ),
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == "problem1-period-two-mechanism-audit-v1"
    assert payload["status"] == "finite-exhaustive"
    assert any(
        "full finite-support period-two case remains open" in limitation
        for limitation in payload["limitations"]
    )
