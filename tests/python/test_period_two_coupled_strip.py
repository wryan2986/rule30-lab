from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_coupled_strip.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_coupled_strip", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
COUPLED = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(COUPLED)


def test_bit_reversal_is_exact_width() -> None:
    assert COUPLED.reverse_bits(0b001011, 6) == 0b110100
    assert COUPLED.reverse_bits(0, 0) == 0
    with pytest.raises(ValueError):
        COUPLED.reverse_bits(8, 3)


def test_local_coupled_transfer_matches_existing_rows() -> None:
    result = COUPLED.verify_coupled_transfer(4)
    assert result["all_checks_pass"] is True
    assert result["coupled_cases_checked"] == 16 * sum(3**n for n in range(5))


def test_moving_cut_identity_matches_independent_constructions() -> None:
    result = COUPLED.verify_moving_cut_identity(24, 128)
    assert result["all_checks_pass"] is True
    assert result["moving_cuts_checked"] == 25
    assert result["selected_rows"][0]["block"] == 0
    assert result["selected_rows"][-1]["block"] == 24


def test_fringe_head_relation_is_strongly_connected() -> None:
    adjacency = COUPLED.fringe_head_transition_relation()
    assert adjacency == {
        (0, 0): {(1, 0), (1, 1)},
        (0, 1): {(1, 1)},
        (1, 0): {(0, 1), (1, 1)},
        (1, 1): {(0, 0), (0, 1)},
    }


def test_coupled_pair_cocycle_space_is_trivial() -> None:
    result = COUPLED.verify_coupled_pair_cocycle_no_go()
    assert result["all_checks_pass"] is True
    assert result["rank"] == 18
    assert result["nullity"] == 6
    assert result["complete_solution"]["fringe_head_potential"] == (
        "P_00=P_01=P_10=P_11"
    )
    assert result["complete_solution"]["terminal_pair_potential"] == (
        "V_00=V_01=V_10=V_11"
    )


def test_invalid_limits_are_rejected() -> None:
    with pytest.raises(ValueError):
        COUPLED.verify_moving_cut_identity(20, 40)
    with pytest.raises(COUPLED.CoupledStripLimitError):
        COUPLED.run_campaign(maximum_block=257)
    with pytest.raises(COUPLED.CoupledStripLimitError):
        COUPLED.run_campaign(maximum_word_length=8)


def test_campaign_certificate_is_deterministic() -> None:
    left = COUPLED.run_campaign(
        maximum_block=16, total_width=96, maximum_word_length=3
    )
    right = COUPLED.run_campaign(
        maximum_block=16, total_width=96, maximum_word_length=3
    )
    assert left == right
    assert len(left["certificate_sha256"]) == 64
