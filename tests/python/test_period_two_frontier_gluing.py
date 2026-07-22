from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_frontier_gluing.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_frontier_gluing", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
GLUING = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GLUING)


def test_single_gap_residues_match_first_return_theorem() -> None:
    result = GLUING.verify_single_gap_residues()
    assert result["all_checks_pass"] is True
    assert {row["gap"]: row["residue"] for row in result["rows"]} == {
        2: 8,
        3: 60,
        4: 108,
        5: 940,
    }


def test_multi_return_prefix_residue_is_exact() -> None:
    gaps = (4, 2, 5, 2)
    residue, modulus = GLUING.survivor_y_prefix_residue(gaps)
    assert modulus == 1 << (2 * sum(gaps))
    for quotient in range(16):
        _, observed = GLUING.follow_survivor_return_prefix(
            residue + modulus * quotient, gaps
        )
        assert observed == gaps


def test_arbitrary_front_and_middle_glue_independently() -> None:
    result = GLUING.verify_gluing_campaign(
        return_count=4, front_width=5, free_bits=4
    )
    assert result["all_checks_pass"] is True
    assert result["ordinary_finite_states_checked"] == 16 * 16
    assert result["leading_front_words_checked"] == 16


def test_glue_validation() -> None:
    with pytest.raises(ValueError):
        GLUING.glue_finite_state(
            low_residue=0,
            low_modulus=3,
            front_word=1,
            front_width=1,
            free_middle=0,
            free_bits=0,
        )
    with pytest.raises(ValueError):
        GLUING.survivor_y_prefix_residue((1,))


def test_campaign_certificate_is_deterministic() -> None:
    left = GLUING.run_campaign(return_count=4, front_width=4, free_bits=3)
    right = GLUING.run_campaign(return_count=4, front_width=4, free_bits=3)
    assert left == right
    assert len(left["certificate_sha256"]) == 64
