from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_return_penalty_locality.py"
)
SPEC = importlib.util.spec_from_file_location("return_penalty_locality", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CAMPAIGN = MODULE.run_campaign(9)


def test_generator_inverses_round_trip() -> None:
    for width in range(1, 11):
        for state in range(1 << width):
            for letter in MODULE.LETTERS:
                image = MODULE.forward_generator(letter, state, width)
                assert MODULE.inverse_generator_mod(letter, image, width) == state


def test_known_fringe_exclusions_are_applied() -> None:
    assert not MODULE.is_locally_admissible("uu")
    assert not MODULE.is_locally_admissible("ttttt")
    assert not MODULE.is_locally_admissible("ututtu")
    assert MODULE.is_locally_admissible("utut")


def test_gap_two_has_both_zero_and_positive_penalties() -> None:
    for phase in MODULE.PHASES:
        row = CAMPAIGN["return_gap_rows"]["2"][phase]
        assert row["zero_penalty_count"] > 0
        assert row["positive_penalty_count"] > 0
        assert row["minimum_penalty"] == 0


def test_non_two_gaps_are_positive_in_default_campaign() -> None:
    for gap in (3, 4, 5):
        for phase in MODULE.PHASES:
            row = CAMPAIGN["return_gap_rows"][str(gap)][phase]
            assert row["zero_penalty_count"] == 0
            assert row["minimum_penalty"] > 0


def test_first_six_actual_return_penalties_are_positive() -> None:
    rows = CAMPAIGN["actual_exact_returns_through_depth_21"]
    assert len(rows) == 6
    assert all(row["p_penalty"] > 0 and row["u_penalty"] > 0 for row in rows)


def test_certificate_and_scope_are_stable() -> None:
    assert CAMPAIGN["certificate_sha256"] == (
        "8e727ab4b9f74d27e3099933fd5e835bf7a5d80c1a002dfd88d18bebd99afb07"
    )
    assert "does not prove all-depth positivity" in CAMPAIGN["scope_warning"]
