from __future__ import annotations

import importlib.util
import math
import sys
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = (
    REPOSITORY_ROOT
    / "experiments"
    / "problem2_balance"
    / "run_multimillion_discrepancy.py"
)
SPEC = importlib.util.spec_from_file_location("rule30_multimillion", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
campaign = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = campaign
SPEC.loader.exec_module(campaign)


def _native(count: int, checkpoints: list[tuple[int, int]]) -> dict[str, object]:
    final_ones = checkpoints[-1][1]
    return {
        "count": count,
        "ones": final_ones,
        "zeros": count - final_ones,
        "discrepancy": 2 * final_ones - count,
        "backend": "avx2",
        "checkpoints": [
            {"count": n, "ones": ones, "discrepancy": 2 * ones - n}
            for n, ones in checkpoints
        ],
    }


def test_parse_counts_requires_unique_bounded_multimillion_horizons() -> None:
    assert campaign.parse_counts("4000000,1000000,2000000") == (
        1_000_000,
        2_000_000,
        4_000_000,
    )
    for text in ("", "999999", "1000000,1000000", "9000000", "x"):
        with pytest.raises(campaign.CampaignError):
            campaign.parse_counts(text)


def test_validate_native_payload_checks_every_identity() -> None:
    payload = _native(2_000_000, [(1_000_000, 500_768), (2_000_000, 1_000_400)])
    validated = campaign.validate_cpp_payload(
        payload,
        run_count=2_000_000,
        requested_checkpoints=(1_000_000, 2_000_000),
        backend="avx2",
    )
    assert validated["discrepancy"] == 800

    broken = dict(payload)
    broken["discrepancy"] = 802
    with pytest.raises(campaign.CampaignError, match="discrepancy"):
        campaign.validate_cpp_payload(
            broken,
            run_count=2_000_000,
            requested_checkpoints=(1_000_000, 2_000_000),
            backend="avx2",
        )


def test_overlap_consistency_and_normalizations() -> None:
    run_one = campaign.validate_cpp_payload(
        _native(1_000_000, [(1_000_000, 500_768)]),
        run_count=1_000_000,
        requested_checkpoints=(1_000_000,),
        backend="avx2",
    )
    run_two = campaign.validate_cpp_payload(
        _native(2_000_000, [(1_000_000, 500_768), (2_000_000, 1_000_400)]),
        run_count=2_000_000,
        requested_checkpoints=(1_000_000, 2_000_000),
        backend="avx2",
    )
    payload = campaign.build_scientific_payload(
        (1_000_000, 2_000_000), [run_one, run_two]
    )
    first, second = payload["finite_observations"]
    assert first["discrepancy"] == 1_536
    assert first["overlap_run_horizons"] == [1_000_000, 2_000_000]
    assert second["discrepancy"] == 800
    assert second["discrepancy_over_n"] == 0.0004
    assert second["discrepancy_over_sqrt_n"] == pytest.approx(800 / math.sqrt(2_000_000))
    assert payload["overlap_consistency"]["comparison_count"] == 1

    inconsistent = dict(run_two)
    inconsistent["checkpoints"] = [dict(item) for item in run_two["checkpoints"]]
    inconsistent["checkpoints"][0]["ones"] += 1
    inconsistent["checkpoints"][0]["discrepancy"] += 2
    with pytest.raises(campaign.CampaignError, match="overlap mismatch"):
        campaign.build_scientific_payload(
            (1_000_000, 2_000_000), [run_one, inconsistent]
        )


def test_resume_state_binds_all_scientific_configuration() -> None:
    run = {"count": 1_000_000, "checkpoints": []}
    state = {
        "schema_version": 1,
        "configuration": {
            "counts": [1_000_000, 2_000_000],
            "backend": "avx2",
            "executable_sha256": "a" * 64,
        },
        "completed_runs": [run],
    }
    assert campaign.validate_resume_state(
        state,
        counts=(1_000_000, 2_000_000),
        backend="avx2",
        executable_sha256="a" * 64,
    ) == [run]
    state["configuration"]["backend"] = "scalar"
    with pytest.raises(campaign.CampaignError, match="configuration"):
        campaign.validate_resume_state(
            state,
            counts=(1_000_000, 2_000_000),
            backend="avx2",
            executable_sha256="a" * 64,
        )


def test_fit_is_explicitly_heuristic_or_inconclusive() -> None:
    fit = campaign.discrepancy_fit(
        [
            {"n": 1_000_000, "discrepancy": 1_000},
            {"n": 4_000_000, "discrepancy": 2_000},
        ]
    )
    assert fit["status"] == "heuristic"
    assert fit["slope"] == pytest.approx(0.5)
    assert "not an upper bound" in fit["limitations"][1]
    inconclusive = campaign.discrepancy_fit(
        [{"n": 1_000_000, "discrepancy": 0}]
    )
    assert inconclusive["status"] == "inconclusive"
    assert inconclusive["slope"] is None
