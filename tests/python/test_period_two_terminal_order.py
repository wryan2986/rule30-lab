from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_terminal_order.py"
)
spec = importlib.util.spec_from_file_location("terminal_order", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_terminal_order_cocycle_exhaustive_small() -> None:
    result = mod.verify_terminal_order_cocycle(7)
    assert result["all_checks_pass"]
    assert result["branch_independent"]
    assert result["word_branch_cases_checked"] == 2 * sum(3**n for n in range(8))


def test_all_driver_run_counter_small() -> None:
    result = mod.verify_run_counter_on_all_branch_words(10)
    assert result["all_checks_pass"]


def test_actual_path_known_records() -> None:
    result = mod.simulate_actual_path(4096)
    assert result["all_checks_pass"]
    assert result["longest_zero_pair_run"] == {
        "length": 5,
        "start_block_zero_based": 2948,
        "end_block_zero_based": 2952,
    }
    assert [record["run_length"] for record in result["record_zero_runs"]] == [1, 2, 3, 4, 5]


def test_nonzero_terminal_resets_order() -> None:
    word = "ptttup"
    updated, terminal = mod.block_update(word, "t")
    expected = mod.leading_t_order(word) + 1 if terminal == "00" else 0
    assert mod.leading_t_order(updated) == expected


def test_campaign_certificate_is_stable_except_runtime() -> None:
    first = mod.run_campaign(maximum_word_length=5, actual_blocks=128)
    second = mod.run_campaign(maximum_word_length=5, actual_blocks=128)
    assert first["certificate_sha256"] == second["certificate_sha256"]
    first.pop("runtime_seconds")
    second.pop("runtime_seconds")
    assert first == second
