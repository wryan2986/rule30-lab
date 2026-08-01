from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_shadow_defect_classification.py"
)
SPEC = importlib.util.spec_from_file_location("shadow_defects", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_frontier_generators_match_known_levels() -> None:
    assert module.frontier_children(3) == (12, 13)
    assert module.frontier_children(1) == (6, 7)
    assert module.build_levels("p", 3)[3] == {50, 51, 52, 53, 55}
    assert module.build_levels("u", 3)[3] == {24, 25, 26, 27}


def test_three_return_pattern_count_is_stable() -> None:
    patterns = module.three_return_patterns()
    assert len(patterns) == 56
    assert all(module.admissible(complete) for _, _, complete in patterns)


def test_mask_sequences_match_small_exact_examples() -> None:
    levels = module.build_levels("p", 4)
    assert module.mask_sequence(levels, 3, 50, 2) == (0b1100, 0b0011)
    assert module.mask_sequence(levels, 3, 52, 2) == (0b1011, 0b0011)


def test_saturated_sequence_is_universally_dominant() -> None:
    current = (0b0011, 0b1011, 0b1100, 0b1111)
    saturated = (0b1111,) * len(current)
    assert module.dominates(current, saturated)
    assert module.defect_count(saturated) == 0


def test_defect_measure_counts_only_nonfull_masks() -> None:
    sequence = (0b1111, 0b1011, 0b1100, 0b1111, 0b1011)
    assert module.defect_count(sequence) == 3
    assert module.dominates((0b1011, 0b1011, 0b1100, 0b0011, 0b1011), sequence)


def test_campaign_limit_is_enforced() -> None:
    try:
        module.run_campaign(module.ABSOLUTE_MAXIMUM_COMPLEXITY + 1)
    except module.ShadowDefectLimitError:
        pass
    else:
        raise AssertionError("campaign limit was not enforced")


def test_default_campaign_certificate_and_totals() -> None:
    payload = module.run_campaign()
    assert payload["certificate_sha256"] == (
        "87fb98033cf66048cf7f44ea11c09fcd40879bf6fe8d05e1214016f65ce0b080"
    )
    assert payload["combined"]["occurrences"] == 19
    assert payload["combined"]["dominant_failures"] == 0
    assert payload["combined"]["saturated_failures"] == 0
    assert payload["combined"]["maximum_minimum_defects"] == 0
