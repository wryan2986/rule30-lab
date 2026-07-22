from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = (
    ROOT
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_first_return.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_first_return", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_exact_four_bit_return_selector() -> None:
    result = MODULE.verify_return_selector(10)
    assert result["all_checks_pass"] is True
    assert result["return_time_counts"] == {
        "2": 192,
        "3": 320,
        "4": 320,
        "5": 192,
    }


def test_selector_partition() -> None:
    assert {k for k, v in MODULE.EXPECTED_SELECTOR.items() if v == 2} == {4, 8, 12}
    assert {k for k, v in MODULE.EXPECTED_SELECTOR.items() if v == 3} == {1, 3, 5, 9, 13}
    assert {k for k, v in MODULE.EXPECTED_SELECTOR.items() if v == 4} == {0, 2, 6, 10, 14}
    assert {k for k, v in MODULE.EXPECTED_SELECTOR.items() if v == 5} == {7, 11, 15}


def test_gap_pair_language() -> None:
    result = MODULE.verify_gap_pair_language()
    assert result["forbidden_gap_pair"] == [2, 3]
    assert len(result["allowed_gap_pairs"]) == 15


def test_fringe_return_degree_cocycle() -> None:
    result = MODULE.verify_fringe_degree_cocycle(512)
    assert result["exceptional_zero_return"] == {"gap": 4, "successor": 56}


def test_survivor_return_residues() -> None:
    assert {
        gap: MODULE.survivor_return_residue(gap) for gap in MODULE.RETURN_TIMES
    } == {2: 8, 3: 60, 4: 108, 5: 940}


def test_survivor_return_cylinders() -> None:
    result = MODULE.verify_survivor_return_cylinders(128)
    assert result["all_checks_pass"] is True
    assert result["ordinary_states_checked"] == 512


def test_campaign_is_deterministic() -> None:
    first = MODULE.run_campaign(selector_bits=10, forward_samples_per_branch=64)
    second = MODULE.run_campaign(selector_bits=10, forward_samples_per_branch=64)
    assert first == second
    assert len(first["certificate_sha256"]) == 64


def test_cli_emits_scoped_json() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            str(MODULE_PATH),
            "--selector-bits",
            "10",
            "--forward-samples-per-branch",
            "32",
        ],
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src" / "python")},
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["status"] == "finite-exhaustive"
    assert payload["question"] == "problem1"
    assert "does not solve Rule 30" in " ".join(payload["limitations"])
