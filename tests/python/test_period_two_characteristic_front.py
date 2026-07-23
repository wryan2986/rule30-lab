from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "problem1_nonperiodicity" / "analyze_period_two_characteristic_front.py"
spec = importlib.util.spec_from_file_location("characteristic_front", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_reversal_conjugacy_small() -> None:
    result = mod.verify_reversal_conjugacy(10)
    assert result["all_checks_pass"]
    assert result["ordinary_states_checked"] == (1 << 10) - 1


def test_zero_tail_front_small() -> None:
    result = mod.verify_zero_tail_front(12)
    assert result["all_checks_pass"]
    assert abs(result["branch_counts"]["t"] - result["branch_counts"]["u"]) <= 1


def test_prefix_periods_are_dyadic() -> None:
    result = mod.verify_prefix_periods(10)
    assert result["all_checks_pass"]
    for level in result["levels"]:
        assert level["all_periods_powers_of_two"]
        assert level["maximum_cycle_period"] <= 1 << level["width"]


def test_campaign_certificate_is_stable() -> None:
    first = mod.run_campaign(12, 10)
    second = mod.run_campaign(12, 10)
    assert first == second
    assert len(first["certificate_sha256"]) == 64


def test_generator_corrections_are_low_supported() -> None:
    for state in range(256):
        t = mod.right_edge_step(state)
        assert mod.forward_generator("u", state) ^ t == 1
        correction = mod.forward_generator("p", state) ^ t
        assert correction in (1, 3)


def test_shifted_rule30_two_step_matches_direct_composition() -> None:
    front = (1, 0, 1, 1, 0, 0, 1, 0, 1)
    assert mod.shifted_rule30_two_step(front) == mod.shifted_rule30_step(
        mod.shifted_rule30_step(front)
    )
