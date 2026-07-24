from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_return_lift_profiles.py"
)
SPEC = importlib.util.spec_from_file_location("return_lift_profiles", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CAMPAIGN = MODULE.run_campaign(2)


def test_generator_inverses_small_quotients() -> None:
    for width in range(1, 10):
        for state in range(1 << width):
            for letter in MODULE.LETTERS:
                image = MODULE.forward_generator(letter, state, width)
                assert MODULE.inverse_generator_mod(letter, image, width) == state


def test_first_three_actual_return_intervals() -> None:
    assert MODULE.actual_u_return_intervals(3) == ((0, 4), (4, 6), (6, 11))


def test_actual_return_block_codes() -> None:
    assert MODULE.actual_block_code(1, 4) == 177
    assert MODULE.actual_block_code(5, 2) == 1
    assert MODULE.actual_block_code(7, 5) == 773


def test_first_two_return_penalties() -> None:
    observed = [
        (
            row["gap"],
            row["by_phase"]["p"]["penalty"],
            row["by_phase"]["u"]["penalty"],
        )
        for row in CAMPAIGN["rows"]
    ]
    assert observed == [(4, 7, 10), (2, 5, 2)]


def test_projection_and_telescoping_checks() -> None:
    assert CAMPAIGN["cumulative_penalties"] == {"p": 12, "u": 12}
    for row in CAMPAIGN["rows"]:
        for phase in MODULE.PHASES:
            summary = row["by_phase"][phase]
            assert summary["actual_length"] - summary["minimum"] == summary["penalty"]
            assert summary["penalty"] > 0


def test_default_certificate_and_scope() -> None:
    assert CAMPAIGN["certificate_sha256"] == (
        "52dcb40543f16d4eef6784919156683e15ba4938f87a4425e234dcc6fb193bbf"
    )
    assert "do not prove positive penalties" in CAMPAIGN["scope_warning"]
