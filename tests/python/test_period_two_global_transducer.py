from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_global_transducer.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_global_transducer", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
GLOBAL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GLOBAL)


def test_single_letter_table_has_twelve_edges() -> None:
    rows = GLOBAL.transition_table()
    assert len(rows) == 12
    assert {
        (
            row["incoming_pair"],
            row["input_letter"],
            row["output_letter"],
            row["successor_pair"],
        )
        for row in rows
    } == {
        ("00", "t", "t", "00"),
        ("00", "p", "p", "11"),
        ("00", "u", "p", "11"),
        ("01", "t", "p", "01"),
        ("01", "p", "u", "10"),
        ("01", "u", "u", "10"),
        ("10", "t", "p", "11"),
        ("10", "p", "p", "01"),
        ("10", "u", "t", "00"),
        ("11", "t", "u", "10"),
        ("11", "p", "t", "00"),
        ("11", "u", "p", "01"),
    }


def test_whole_word_scan_matches_independent_sections() -> None:
    result = GLOBAL.verify_transducer_table(5)
    assert result["all_checks_pass"] is True
    assert result["word_pair_cases_checked"] == 4 * sum(3**n for n in range(6))


def test_block_recurrence_matches_existing_implementation() -> None:
    result = GLOBAL.verify_block_recurrence(5)
    assert result["all_checks_pass"] is True
    assert result["word_branch_cases_checked"] == 2 * sum(3**n for n in range(6))


def test_additive_cocycle_space_is_trivial() -> None:
    result = GLOBAL.verify_additive_cocycle_no_go()
    assert result["all_checks_pass"] is True
    assert result["rank"] == 5
    assert result["nullity"] == 2
    assert result["complete_solution"] == {
        "letter_weights": "a_t=a_p=a_u",
        "state_potentials": "V_00=V_01=V_10=V_11",
    }


def test_short_language_counterexample_has_ten_zero_pairs() -> None:
    result = GLOBAL.verify_short_language_counterexample()
    assert result["all_checks_pass"] is True
    assert result["branch_word_length"] == 40
    assert result["longest_zero_pair_run"] == 10
    assert result["zero_pair_run_start_zero_based"] == 30
    assert result["leading_t_runs_during_zero_pairs"] == list(range(10))


def test_invalid_inputs_are_rejected() -> None:
    with pytest.raises(ValueError):
        GLOBAL.letter_transition("x", (1, 1))
    with pytest.raises(ValueError):
        GLOBAL.double_section_transduce(("t",), (2, 0))
    with pytest.raises(GLOBAL.GlobalTransducerLimitError):
        GLOBAL.run_campaign(maximum_word_length=10)


def test_campaign_certificate_is_deterministic() -> None:
    left = GLOBAL.run_campaign(maximum_word_length=5)
    right = GLOBAL.run_campaign(maximum_word_length=5)
    assert left == right
    assert len(left["certificate_sha256"]) == 64
