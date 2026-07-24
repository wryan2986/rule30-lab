from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_two_return_penalties.py"
)
SPEC = importlib.util.spec_from_file_location("two_return_penalties", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
CAMPAIGN = MODULE.run_campaign(8)


def test_generator_inverses_small_quotients() -> None:
    for width in range(1, 11):
        for state in range(1 << width):
            for letter in MODULE.LETTERS:
                image = MODULE.forward_generator(letter, state, width)
                assert MODULE.inverse_generator_mod(letter, image, width) == state


def test_gap_pair_23_is_forbidden() -> None:
    for phase in MODULE.PHASES:
        assert CAMPAIGN["gap_pair_rows"]["2,3"][phase]["candidates"] == 0


def test_no_two_return_zero_penalty_through_depth_eight() -> None:
    assert CAMPAIGN["totals"]["zero_two_return_penalties"] == 0


def test_double_gap_two_has_positive_total_penalty() -> None:
    p_row = CAMPAIGN["gap_pair_rows"]["2,2"]["p"]
    u_row = CAMPAIGN["gap_pair_rows"]["2,2"]["u"]
    assert p_row["minimum_penalty"] > 0
    assert u_row["minimum_penalty"] > 0


def test_two_return_penalty_telescopes() -> None:
    for pair in CAMPAIGN["gap_pair_rows"].values():
        for phase in MODULE.PHASES:
            example = pair[phase]["minimum_example"]
            if example is None:
                continue
            assert example["total_penalty"] == (
                example["first_penalty"] + example["second_penalty"]
            )


def test_deterministic_certificate() -> None:
    assert CAMPAIGN["certificate_sha256"] == (
        "acf4eef630117b9fd955cafeeaf4f217f090a139993554e5ee85427b348e6d88"
    )
