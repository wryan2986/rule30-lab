from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_concrete_shadow_beliefs.py"
)
SPEC = importlib.util.spec_from_file_location("concrete_shadow_beliefs", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_frontier_generators_match_known_first_levels() -> None:
    assert module.frontier_children(3) == (12, 13)
    assert module.frontier_children(1) == (6, 7)
    assert module.build_levels("p", 3)[3] == {50, 51, 52, 53, 55}
    assert module.build_levels("u", 3)[3] == {24, 25, 26, 27}


def test_three_return_pattern_count_is_stable() -> None:
    patterns = module.three_return_patterns()
    assert len(patterns) == 56
    assert all(module.admissible(complete) for _, _, complete in patterns)


def test_direct_and_recursive_beliefs_agree_exhaustively_small() -> None:
    for phase in module.PHASES:
        levels = module.build_levels(phase, 9)
        for complexity in range(2, 10):
            for current in levels[complexity]:
                for depth in range(1, complexity):
                    assert module.concrete_shadow_belief_direct(
                        levels, complexity, current, depth
                    ) == module.concrete_shadow_belief_recursive(
                        levels, complexity, current, depth
                    )


def test_recursive_belief_members_are_consistent_realizations() -> None:
    levels = module.build_levels("p", 10)
    current = next(state for state in levels[10] if state & 3 == 3)
    depth = 4
    belief = module.concrete_shadow_belief_recursive(levels, 10, current, depth)
    modulus = 4**depth
    assert belief
    assert all(state in levels[9] for state in belief)
    assert all(state % modulus == current % modulus for state in belief)


def test_signature_no_go_counterexample_has_empty_concrete_belief() -> None:
    levels = module.build_levels("p", 2)
    assert 12 in levels[2]
    assert module.concrete_shadow_belief_recursive(levels, 2, 12, 1) == ()


def test_known_positive_cut_belief_trace() -> None:
    levels = module.build_levels("u", 18)
    current = 0x6473D46AB
    assert current in levels[18]
    assert module.concrete_shadow_trace(levels, 18, current, 5) == (
        665,
        264,
        88,
        35,
        20,
    )


def test_default_campaign_certificate_and_totals() -> None:
    payload = module.run_campaign()
    assert payload["certificate_sha256"] == (
        "aefa388564278d291737801033e1cddc9a0902ea3982eee78050606ca2a6391d"
    )
    assert payload["combined"]["occurrences"] == 19
    assert payload["combined"]["positive_cut_occurrences"] == 5
    assert payload["combined"]["empty_beliefs"] == 0
    assert payload["combined"]["minimum_final_belief"] == 80
