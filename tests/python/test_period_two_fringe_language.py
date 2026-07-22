from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "experiments" / "problem1_nonperiodicity" / "analyze_period_two_fringe_language.py"
SPEC = importlib.util.spec_from_file_location("period_two_fringe_language", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_packed_map_matches_tuple_map() -> None:
    result = module.verify_packed_map(10)
    assert result == {"input_bits": 10, "states_checked": 1024, "all_checks_pass": True}


def test_alternating_center_self_trace_identity() -> None:
    result = module.verify_self_trace_identity()
    assert result["exact_identity"] == "1[q_m=u] = x_-2(2m)"
    assert len(result["valid_local_assignments"]) == 4
    assert {row["branch"] for row in result["valid_local_assignments"]} == {"t", "u"}


def test_complete_short_trace_languages() -> None:
    result = module.verify_trace_language(10)
    assert [level["realized_words"] for level in result["levels"]] == [
        2,
        3,
        5,
        8,
        12,
        17,
        25,
        36,
        49,
        65,
    ]
    assert result["all_scale_forbidden_words"] == ["uu", "ttttt", "ututtu"]
    assert result["levels"][5]["language"] == [
        "ttttut",
        "tttutt",
        "tttutu",
        "ttuttt",
        "ttuttu",
        "ttutut",
        "tutttt",
        "tutttu",
        "tuttut",
        "tututt",
        "tututu",
        "uttttu",
        "utttut",
        "uttutt",
        "uttutu",
        "ututtt",
        "ututut",
    ]


def test_sft_dimension_bound() -> None:
    result = module.verify_sft_dimension_bound()
    assert result["adjacency_characteristic_factor"] == "lambda^3-lambda^2-1"
    assert 1.4655 < result["dominant_root"] < 1.4656
    assert 0.2757 < result["survivor_2adic_dimension_upper_bound"] < 0.2758


def test_campaign_limits_fail_closed() -> None:
    with pytest.raises(module.FringeLanguageLimitError):
        module.run_campaign(maximum_word_length=11)
    with pytest.raises(ValueError):
        module.run_campaign(maximum_word_length=5)


def test_script_emits_scoped_deterministic_json() -> None:
    completed = subprocess.run(
        (sys.executable, str(SCRIPT), "--maximum-word-length", "6"),
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == "problem1-period-two-fringe-language-v1"
    assert payload["status"] == "finite-exhaustive"
    assert len(payload["result_summary"]["certificate_sha256"]) == 64
    assert any(
        "does not exclude eventual center period two" in limitation
        for limitation in payload["limitations"]
    )
