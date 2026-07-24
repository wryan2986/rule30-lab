from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "problem1_nonperiodicity" / "analyze_period_two_prebranch_minimizers.py"
spec = importlib.util.spec_from_file_location("prebranch", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_frontier_children_are_distinct_generator_images() -> None:
    for state in range(1, 128):
        expected = {
            module.forward_generator(letter, state)
            for letter in ("t", "p", "u")
        }
        assert set(module.frontier_children(state)) == expected


def test_phase_frontier_bit_length_law() -> None:
    for phase in module.PHASES:
        states = {module.phase_start(phase)}
        for complexity in range(1, 9):
            expected = 2 * complexity if phase == "p" else 2 * complexity - 1
            assert {state.bit_length() for state in states} == {expected}
            states = {
                child
                for state in states
                for child in module.frontier_children(state)
            }


def test_final_branch_is_invisible_at_its_depth() -> None:
    prefix = "tutututttututut"
    left = prefix + "t"
    right = prefix + "u"
    assert len(left) == len(right)
    assert module.survivor_for_word(left) == module.survivor_for_word(right)


def test_known_counterexample_schedule_and_admissibility() -> None:
    row = module.verify_known_counterexample()
    assert row["forced_zero_schedule"] == "tutututttutututt"
    assert row["return_gaps"] == [2, 2]
    assert module.locally_admissible(module.KNOWN_FINAL_WORD)


def test_known_counterexample_matches_all_three_cylinders() -> None:
    state = module.KNOWN_COUNTEREXAMPLE
    for word in (
        module.KNOWN_BASE_WORD,
        module.KNOWN_MIDDLE_WORD,
        module.KNOWN_FINAL_WORD,
    ):
        assert state % (4 ** len(word)) == module.survivor_for_word(word)


def test_small_campaign_is_deterministic_and_pre_counterexample() -> None:
    result = module.run_campaign(12, 48)
    assert result["certificate_sha256"] == (
        "def883f8e5ebf9e80280826db499112f89603705fe172a3b35e742c090fa5fea"
    )
    assert all(
        not row["two_return_zero_candidates"]
        for row in result["phases"].values()
    )
