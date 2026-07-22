from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from rule30lab.two_adic import right_edge_inverse_mod, right_edge_step_mod


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_inverse_lift_sections.py"
)
SPEC = importlib.util.spec_from_file_location("inverse_lift_sections", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


def test_right_edge_inverse_is_exact_and_validated() -> None:
    for width in range(1, 9):
        for state in range(1 << width):
            image = right_edge_step_mod(state, width)
            assert right_edge_inverse_mod(image, width) == state
            assert right_edge_step_mod(
                right_edge_inverse_mod(state, width), width
            ) == state
    with pytest.raises(ValueError, match="positive"):
        right_edge_inverse_mod(0, 0)
    with pytest.raises(ValueError, match="does not fit"):
        right_edge_inverse_mod(8, 3)


def test_odd_tail_oracles_and_known_section_path() -> None:
    assert [module.odd_tail_step_mod(tail, 3) for tail in range(8)] == [
        3,
        6,
        5,
        4,
        7,
        2,
        1,
        0,
    ]
    for width in range(1, 7):
        for tail in range(1 << width):
            assert module.odd_tail_step_mod(
                tail, width
            ) == module.odd_tail_step_cell_array(tail, width)

    seed, periods = module.inverse_via_section_schedule(0b010101, 6)
    assert seed == 0b000111
    assert periods == [1, 2, 2, 4, 8, 8]

    alternating_ten = sum(1 << position for position in range(0, 10, 2))
    seed_ten, _ = module.inverse_via_section_schedule(alternating_ten, 10)
    assert (seed_ten & 0b111) == 7
    assert (seed_ten & 0b1_1111) == 7
    assert (seed_ten >> 3) & 0b111 == 0
    assert ((seed_ten >> 5) & 0b1_1111) == 22
    assert ((seed_ten >> 4) & 0b1111) == 12

    alternating_twelve = sum(1 << position for position in range(0, 12, 2))
    seed_twelve, _ = module.inverse_via_section_schedule(alternating_twelve, 12)
    assert ((seed_twelve >> 5) & 1) == 0
    assert ((seed_twelve >> 11) & 1) == 0


def test_section_recurrence_matches_independent_inverse_exhaustively() -> None:
    for width in range(1, 9):
        for trace in range(1 << width):
            recursive, _ = module.inverse_via_section_schedule(trace, width)
            assert module.diagonal_map_cell_array(recursive, width) == trace


def test_small_campaign_is_deterministic_and_fails_closed() -> None:
    arguments = {
        "maximum_width": 5,
        "trace_depth": 8,
        "section_lookahead": 4,
        "dyadic_probe_width": 32,
    }
    first = module.run_campaign(**arguments)
    second = module.run_campaign(**arguments)
    assert first == second
    assert first["coverage"] == {
        "quotient_points_exhausted": 62,
        "section_continuations_checked": 576,
        "independent_diagonal_evaluators": 2,
        "inverse_oracles_compared": 3,
        "control_traces": 4,
        "dyadic_probe_bits": 32,
        "estimated_work_points": 1_662,
    }
    assert first["all_finite_inverse_oracles_agree"] is True
    assert first["all_finite_branch_identities_pass"] is True
    alternating = first["control_summaries"][-1]
    assert alternating["name"] == "alternating_one_zero"
    assert alternating["inverse_seed_bits_lsb_first"] == "11100011"
    assert alternating["section_schedule_periods_after_each_bit"] == [
        1,
        2,
        2,
        4,
        8,
        8,
        16,
        32,
    ]
    assert alternating["distinct_truncated_sections"] == 9
    assert first["period_two_block_controls"] == {
        "independent_phase_block_at_width_two": {
            "prefix": 3,
            "extension": 1,
            "extension_equals_prefix": False,
        },
        "dyadic_copy_and_complement_at_width_four": {
            "extension_width_two": 1,
            "extension_width_four": 12,
            "copied_width_two_prediction": 5,
            "copied_complement_prediction": 10,
            "copy_prediction_matches": False,
            "complement_prediction_matches": False,
        },
    }
    assert first["period_two_dyadic_index_probe"]["samples"] == [
        {
            "exponent": exponent,
            "position": (1 << exponent) - 1,
            "bit": exponent & 1,
            "equals_exponent_parity": True,
        }
        for exponent in range(1, 6)
    ]
    assert len(first["certificate_sha256"]) == 64

    with pytest.raises(module.InverseLiftLimitError, match="quotient width"):
        module.run_campaign(maximum_width=13)
    with pytest.raises(module.InverseLiftLimitError, match="trace depth"):
        module.run_campaign(trace_depth=21)
    with pytest.raises(module.InverseLiftLimitError, match="lookahead"):
        module.run_campaign(section_lookahead=9)
    with pytest.raises(module.InverseLiftLimitError, match="dyadic probe"):
        module.run_campaign(dyadic_probe_width=1_025)
    with pytest.raises(module.InverseLiftLimitError, match="work points"):
        module.run_campaign(maximum_work_points=10)
    with pytest.raises(module.InverseLiftLimitError, match="schedule period"):
        module.run_campaign(
            maximum_width=5,
            trace_depth=8,
            section_lookahead=4,
            maximum_schedule_period=4,
        )


def test_script_emits_strict_finite_scope_json() -> None:
    completed = subprocess.run(
        (
            sys.executable,
            str(SCRIPT),
            "--maximum-width",
            "5",
            "--trace-depth",
            "8",
            "--section-lookahead",
            "4",
            "--dyadic-probe-width",
            "32",
        ),
        check=True,
        capture_output=True,
        text=True,
        timeout=15,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == "problem1-inverse-lift-sections-v1"
    assert payload["status"] == "finite-exhaustive"
    assert any(
        "does not exclude eventual center period two" in limitation
        for limitation in payload["limitations"]
    )
