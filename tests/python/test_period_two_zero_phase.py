from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_zero_phase.py"
)
spec = importlib.util.spec_from_file_location("zero_phase", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_terminal_head_code() -> None:
    result = mod.verify_terminal_head(7)
    assert result["all_checks_pass"]
    assert result["head_code"] == {"00": "t", "01": "p", "10": "u", "11": "p"}


def test_zero_deletion_recurrence() -> None:
    result = mod.verify_zero_deletion(8)
    assert result["all_checks_pass"]
    assert set(result["phase_counts_before_branch_duplication"]) == {"p", "u"}


def test_phase_is_bit_length_parity() -> None:
    result = mod.verify_phase_parity(8)
    assert result["all_checks_pass"]
    assert result["phase_bit_length_parity"] == {"p": "even", "u": "odd"}


def test_zero_island_phase_is_constant() -> None:
    result = mod.verify_zero_island_drivers(5, 5)
    assert result["all_checks_pass"]
    assert result["surviving_zero_prefixes"] > 0


def test_campaign_is_deterministic() -> None:
    first = mod.run_campaign(maximum_word_length=7, maximum_driver_depth=4)
    second = mod.run_campaign(maximum_word_length=7, maximum_driver_depth=4)
    assert first == second
    assert len(first["certificate_sha256"]) == 64


def test_explicit_zero_island_keeps_phase() -> None:
    word = "pttput"
    assert mod.scan(word)[1] == "00"
    _, phase, _ = mod.zero_decomposition(word)
    assert phase == "p"
    for branch in "tutu":
        word, terminal = mod.block_update(word, branch)
        assert terminal == "00"
        _, next_phase, _ = mod.zero_decomposition(word)
        assert next_phase == "p"
