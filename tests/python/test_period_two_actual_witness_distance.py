from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_actual_witness_distance.py"
)
SPEC = importlib.util.spec_from_file_location("actual_witness_distance", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CAMPAIGN = MODULE.run_campaign(12)


def test_generator_inverses_round_trip() -> None:
    for width in range(1, 11):
        for state in range(1 << width):
            for letter in MODULE.LETTERS:
                image = MODULE.forward_generator(letter, state, width)
                assert MODULE.inverse_generator_mod(letter, image, width) == state


def test_actual_survivor_64_bit_residue() -> None:
    assert MODULE.actual_survivor_residue(32) == 0x7FE13F3088C146C7


def test_reference_phase_distances_through_ten() -> None:
    observed = {
        row["depth"]: {
            phase: row["by_phase"][phase]["minimum_length"]
            for phase in MODULE.PHASE_START
        }
        for row in CAMPAIGN["rows"][:10]
    }
    assert observed == {
        depth: MODULE.EXPECTED_PHASE_DISTANCES[depth]
        for depth in range(1, 11)
    }


def test_depth_twelve_is_exact() -> None:
    row = CAMPAIGN["rows"][-1]
    assert row["depth"] == 12
    assert row["target_hex"] == "0xc146c7"
    assert row["by_phase"]["p"]["minimum_length"] == 28
    assert row["by_phase"]["u"]["minimum_length"] == 27
    assert row["minimum_length"] == 27


def test_phase_distances_are_monotone() -> None:
    for phase in MODULE.PHASE_START:
        values = [
            row["by_phase"][phase]["minimum_length"]
            for row in CAMPAIGN["rows"]
        ]
        assert values == sorted(values)


def test_certificate_and_scope_are_stable() -> None:
    assert CAMPAIGN["certificate_sha256"] == (
        "fafe057b3a193a61af2ef4a3107b2c43029e6f2222a4fb32efb0dd71e0071f18"
    )
    assert "do not prove divergence" in CAMPAIGN["scope_warning"]
