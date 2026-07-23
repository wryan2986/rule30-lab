from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path

ROOT = Path(__file__).parents[2]
MODULE_PATH = (
    ROOT
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_dual_cut.py"
)
TERMINAL_PATH = (
    ROOT
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_terminal_order.py"
)


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


mod = _load(MODULE_PATH, "dual_cut")
terminal = _load(TERMINAL_PATH, "terminal_order_crosscheck")


def test_factorization_small() -> None:
    result = mod.verify_factorization(3, 4)
    assert result["all_checks_pass"]


def test_unique_zero_target_small() -> None:
    result = mod.verify_unique_zero_target(3, 5)
    assert result["all_checks_pass"]


def test_direct_example() -> None:
    word = "tputp"
    driver = "utttu"
    states, fresh_final = mod.fresh_boundary_states(driver)
    outputs, coupled_final = mod.coupled_outputs(word, driver)
    observed, _ = mod.dual_action(word, states)
    final_section = mod.section_along_state_word(word, states[:-1])
    assert observed == outputs
    assert coupled_final == final_section + fresh_final


def test_transition_table_matches_terminal_order_analyzer() -> None:
    for length in range(5):
        for letters in itertools.product(mod.LETTERS, repeat=length):
            word = "".join(letters)
            for state in mod.PAIR_STATES:
                section, image = mod.scan(word, state)
                expected_section, expected_image = terminal.transduce(word, state)
                assert (section, image) == (expected_section, expected_image)


def test_actual_cut_small() -> None:
    result = mod.verify_actual_cut(600, 8)
    assert result["all_checks_pass"]


def test_campaign_certificate_stable() -> None:
    first = mod.run_campaign(
        maximum_word_length=3,
        maximum_driver_depth=4,
        actual_blocks=600,
        actual_cut_depth=8,
    )
    second = mod.run_campaign(
        maximum_word_length=3,
        maximum_driver_depth=4,
        actual_blocks=600,
        actual_cut_depth=8,
    )
    assert first == second
    assert len(first["certificate_sha256"]) == 64
