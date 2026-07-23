from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_arrangement_cocycles.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_arrangement_cocycles", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
ARRANGEMENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ARRANGEMENT)


def test_exact_transition_table_has_twelve_edges() -> None:
    edges = ARRANGEMENT.transition_edges()
    assert len(edges) == 12
    assert {edge["state"] for edge in edges} == {"00", "01", "10", "11"}
    assert {edge["input"] for edge in edges} == {"t", "p", "u"}


def test_geometric_classification_at_exceptional_lambda() -> None:
    result = ARRANGEMENT.geometric_classification(Fraction(1))
    assert result["solution_dimension"] == 2
    assert result["letter_weights"] == "a_t=a_p=a_u"
    assert result["state_potentials"] == "V_00=V_01=V_10=V_11"
    assert result["terminal_sensitivity"] is False


def test_geometric_classification_off_exceptional_lambda() -> None:
    for value in [Fraction(0), Fraction(-1), Fraction(1, 2), Fraction(2)]:
        result = ARRANGEMENT.geometric_classification(value)
        assert result["solution_dimension"] == 1
        assert result["state_potentials"] == "V_00=V_01=V_10=V_11=0"


def test_small_group_controls_find_only_trivial_family() -> None:
    s3 = ARRANGEMENT.brute_force_group_control("S3")
    d4 = ARRANGEMENT.brute_force_group_control("D4")
    assert s3["solutions"] == 18
    assert d4["solutions"] == 40
    assert s3["nontrivial_solutions"] == d4["nontrivial_solutions"] == 0


def test_campaign_is_deterministic() -> None:
    left = ARRANGEMENT.run_campaign()
    right = ARRANGEMENT.run_campaign()
    assert left == right
    assert len(left["certificate_sha256"]) == 64
    assert left["group_multiplicative"]["terminal_sensitivity"] is False
