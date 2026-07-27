from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments/problem1_nonperiodicity/analyze_period_two_signature_simulation_no_go.py"
)
SPEC = importlib.util.spec_from_file_location("signature_simulation_no_go", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_exact_signature_alphabet_and_graph() -> None:
    result = MODULE.run_campaign(16)
    assert result["signature_graph"] == {
        "signatures": 12,
        "phase_p_labelled_edges": 194,
        "phase_u_labelled_edges": 192,
        "union_labelled_edges": 194,
        "phase_graphs_identical": False,
    }


def test_fixed_point_prunes_in_three_rounds() -> None:
    simulation = MODULE.run_campaign(16)["simulation"]
    assert simulation["fixed_point_rounds"] == 3
    assert (
        sum(simulation["removed_by_round"])
        + simulation["greatest_fixed_point_pairs"]
        == simulation["all_candidate_pairs"]
    )


def test_universal_singleton_simulates_all_signatures() -> None:
    simulation = MODULE.run_campaign(16)["simulation"]
    assert simulation["universal_singleton"] == "0b1111/0b1111"
    assert len(simulation["universal_singleton_simulates"]) == 12


def test_concrete_same_cylinder_lift_fails() -> None:
    row = MODULE.run_campaign(16)["concrete_lift_failure"]
    assert row["current_state"] == 12
    assert row["current_signature"] == "0b0010/0b1100"
    assert row["abstract_simulation_accepts"] is True
    assert row["previous_frontier"] == [3]
    assert row["same_cylinder_previous_states"] == []


def test_transition_profiles_do_not_collapse_to_twelve_symbols() -> None:
    result = MODULE.run_campaign(16)
    assert result["phases"]["p"]["concrete_transition_profiles"] > 12
    assert result["phases"]["u"]["concrete_transition_profiles"] > 12


def test_phase_output_totals() -> None:
    result = MODULE.run_campaign(16)
    assert result["phases"]["p"]["outputs_checked"] == 52446
    assert result["phases"]["u"]["outputs_checked"] == 43970


def test_default_certificate_is_stable() -> None:
    result = MODULE.run_campaign(16)
    assert result["certificate_sha256"] == (
        "b50a4a16bf21ad6d39ce71a4658722b63efc9bca574a93a5a73ac9377153896a"
    )
