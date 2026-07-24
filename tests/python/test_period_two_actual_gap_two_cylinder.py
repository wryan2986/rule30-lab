from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[2] / "experiments" / "problem1_nonperiodicity" / "analyze_period_two_actual_gap_two_cylinder.py"
spec = importlib.util.spec_from_file_location("actual_gap_two", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_initial_fringe_steps() -> None:
    state = 0
    observed = []
    for _ in range(5):
        observed.append(state)
        state = module.advance_fringe(state)
    assert observed == [0, 3, 14, 63, 224]


def test_return_selector_examples() -> None:
    assert module.return_gap(4) == 2
    assert module.return_gap(8) == 2
    assert module.return_gap(12) == 2
    assert module.return_gap(15) == 5


def test_complete_consecutive_gap_two_cylinder() -> None:
    result = module.consecutive_gap_two_cylinder()
    assert result["states_checked"] == 256
    assert result["factored_residues_mod_64"] == [28, 44, 60]
    assert len(result["witnesses_mod_256"]) == 12


def test_bad_classes_generate_ututu() -> None:
    for residue in module.BAD_RESIDUES_MOD_64:
        assert module.branch_word_from_return_coordinate(residue, 5) == "ututu"
    assert module.branch_word_from_return_coordinate(24, 5) != "ututu"


def test_actual_5000_block_campaign() -> None:
    row = module.actual_orbit_campaign(5000)
    assert row["return_count"] == 1081
    assert row["consecutive_gap_two_count"] == 0
    assert row["bad_cylinder_visits"] == 0
    assert row["last_gap_two_start"] == 144


def test_small_campaign_certificate() -> None:
    result = module.run_campaign(5000)
    assert result["certificate_sha256"] == (
        "5bd0b5af84355bf8773fb2099a67a72e37157d9b2458fac876d4489144bb2e78"
    )
