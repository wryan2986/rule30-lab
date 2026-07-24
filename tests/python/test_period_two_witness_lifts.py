from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_witness_lifts.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_witness_lifts", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_generator_inverses_small_quotients() -> None:
    for width in range(1, 11):
        mask = (1 << width) - 1
        for state in range(1 << width):
            for letter in MODULE.LETTERS:
                image = MODULE.forward_generator(letter, state, width)
                assert MODULE.inverse_generator_mod(letter, image, width) == (state & mask)


def test_actual_survivor_pair_prefix() -> None:
    residue = MODULE.actual_survivor_residue(12)
    pairs = [(residue >> (2 * index)) & 3 for index in range(12)]
    assert pairs == [3, 1, 0, 3, 2, 1, 0, 1, 1, 0, 0, 3]


def test_known_depth_three_profiles() -> None:
    assert MODULE.phase_lift_profile(3, "p") == (7, 10, 7, 8)
    assert MODULE.phase_lift_profile(3, "u") == (2, 6, 9, 7)


def test_profile_projection_minimum() -> None:
    for depth in range(1, 7):
        assert min(MODULE.phase_lift_profile(depth, "p")) == MODULE.KAPPA_P[depth]
        assert min(MODULE.phase_lift_profile(depth, "u")) == MODULE.KAPPA_U[depth]


def test_actual_coordinate_recovers_next_complexity() -> None:
    for depth in range(1, 7):
        digit = MODULE.actual_pair(depth)
        assert MODULE.phase_lift_profile(depth, "p")[digit] == MODULE.KAPPA_P[depth + 1]
        assert MODULE.phase_lift_profile(depth, "u")[digit] == MODULE.KAPPA_U[depth + 1]


def test_deterministic_campaign_certificate() -> None:
    result = MODULE.run_campaign(6)
    assert result["certificate"] == (
        "8cbb471a6ee29272f7ba9813af2b74ce1dc85ce1e1fbacc6b047a44fc287581b"
    )
