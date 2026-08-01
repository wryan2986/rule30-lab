from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_weighted_shadow_recursion.py"
)
SPEC = importlib.util.spec_from_file_location("weighted_shadow_recursion", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_frontier_generators_and_first_levels() -> None:
    assert module.frontier_children(3) == (12, 13)
    assert module.frontier_children(1) == (6, 7)
    assert module.build_levels("p", 3)[3] == {50, 51, 52, 53, 55}
    assert module.build_levels("u", 3)[3] == {24, 25, 26, 27}


def test_three_return_pattern_count() -> None:
    patterns = module.three_return_patterns()
    assert len(patterns) == 56
    assert all(module.admissible(complete) for _, _, complete in patterns)


def test_direct_and_recursive_weighted_beliefs_agree_small() -> None:
    for phase in module.PHASES:
        levels = module.build_levels(phase, 8)
        for complexity in range(2, 9):
            for current in levels[complexity]:
                for depth in range(1, complexity):
                    assert module.weighted_shadow_belief_direct(
                        levels, complexity, current, depth
                    ) == module.weighted_shadow_belief_recursive(
                        levels, complexity, current, depth
                    )


def test_signature_counterexample_is_rejected_by_weighted_belief() -> None:
    levels = module.build_levels("p", 2)
    assert 12 in levels[2]
    assert module.weighted_shadow_belief_recursive(levels, 2, 12, 1) == {}


def test_known_positive_cut_has_zero_defect_certificate() -> None:
    levels = module.build_levels("u", 18)
    current = 0x6473D46AB
    certificate = module.minimum_defect_certificate(levels, 18, current, 5)
    assert certificate is not None
    assert certificate["minimum_defects"] == 0
    assert certificate["synchronized_defects"]
    assert certificate["seed_current_complexity"] == 14
    assert certificate["lift_digits"] == (2, 2, 2, 3)


def test_defect_cost_matches_selected_shadow_masks() -> None:
    levels = module.build_levels("p", 12)
    current = next(state for state in sorted(levels[12]) if state & 3 == 3)
    certificate = module.minimum_defect_certificate(levels, 12, current, 2)
    assert certificate is not None
    assert certificate["minimum_defects"] == module.defect_count(
        certificate["shadow_masks"]
    )
    assert module.dominates(
        certificate["current_masks"], certificate["shadow_masks"]
    )


def test_default_campaign_certificate_and_totals() -> None:
    payload = module.run_campaign()
    assert payload["certificate_sha256"] == (
        "cd52b20688d0c57c84e82d7b42da01d281a347464c6265d80f70ddf9dc62fed6"
    )
    assert payload["combined"]["occurrences"] == 19
    assert payload["combined"]["dominant_failures"] == 0
    assert payload["combined"]["weighted_cylinders_checked"] == 17
    assert payload["combined"]["maximum_minimum_defects"] == 0
