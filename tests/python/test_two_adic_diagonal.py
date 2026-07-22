from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

from rule30lab.two_adic import (
    diagonal_map_mod,
    inverse_diagonal_map_mod,
    minus_one_third_mod,
    plus_one_third_mod,
    right_edge_step_mod,
)


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_two_adic_diagonal.py"
)
SPEC = importlib.util.spec_from_file_location("two_adic_analysis", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
analysis = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = analysis
SPEC.loader.exec_module(analysis)


def _unbounded_step(state: int) -> int:
    return state ^ ((state << 1) | (state << 2))


def test_small_diagonal_map_and_validation() -> None:
    assert [diagonal_map_mod(seed, 3) for seed in range(8)] == [
        0,
        3,
        2,
        1,
        4,
        7,
        6,
        5,
    ]
    with pytest.raises(ValueError, match="positive"):
        diagonal_map_mod(0, 0)
    with pytest.raises(ValueError, match="does not fit"):
        right_edge_step_mod(8, 3)
    with pytest.raises(ValueError, match="integer residue"):
        inverse_diagonal_map_mod(True, 1)


def test_two_evaluators_and_inverse_exhaustively_through_width_eight() -> None:
    for width in range(1, 9):
        for seed in range(1 << width):
            trace = diagonal_map_mod(seed, width)
            assert analysis.diagonal_map_cell_array(seed, width) == trace
            assert inverse_diagonal_map_mod(trace, width) == seed


def test_first_differing_bit_is_preserved_exhaustively() -> None:
    width = 8
    images = [diagonal_map_mod(seed, width) for seed in range(1 << width)]
    for left in range(1 << width):
        for right in range(left + 1, 1 << width):
            input_difference = left ^ right
            output_difference = images[left] ^ images[right]
            assert (input_difference & -input_difference) == (
                output_difference & -output_difference
            )


def test_exact_rational_two_cycle_and_all_one_diagonal_modulo_2_to_64() -> None:
    for width in range(1, 65):
        mask = (1 << width) - 1
        a = minus_one_third_mod(width)
        b = plus_one_third_mod(width)
        assert right_edge_step_mod(a, width) == b
        assert right_edge_step_mod(b, width) == a
        assert diagonal_map_mod(a, width) == mask
        assert diagonal_map_mod(b, width) == 1
        assert (3 * a + 1) & mask == 0
        assert (3 * b - 1) & mask == 0


def test_finite_truncations_match_all_one_trace_without_modular_evolution() -> None:
    for horizon in range(0, 33):
        seed = minus_one_third_mod(horizon + 1)
        state = seed
        for time in range(horizon + 1):
            assert (state >> time) & 1 == 1
            state = _unbounded_step(state)


def test_campaign_is_deterministic_and_fails_closed_at_caps() -> None:
    first = analysis.run_campaign(maximum_width=6)
    second = analysis.run_campaign(maximum_width=6)
    assert first == second
    assert first["coverage"] == {
        "widths": 6,
        "quotient_points_exhausted": 126,
        "independent_diagonal_evaluators": 2,
    }
    assert first["all_finite_diagonal_maps_are_permutations"] is True
    assert first["all_finite_inverses_verified"] is True
    assert first["all_top_bit_triangular_checks_pass"] is True
    assert first["all_rational_countermodel_checks_pass"] is True
    with pytest.raises(analysis.TwoAdicLimitError, match="configured maximum"):
        analysis.run_campaign(maximum_width=17)
    with pytest.raises(analysis.TwoAdicLimitError, match="quotient points"):
        analysis.run_campaign(maximum_width=6, maximum_quotient_points=100)


def test_script_emits_finite_scope_json() -> None:
    completed = subprocess.run(
        (sys.executable, str(SCRIPT), "--maximum-width", "5"),
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    payload = json.loads(completed.stdout)
    assert payload["experiment_id"] == "problem1-two-adic-diagonal-v1"
    assert payload["status"] == "finite-exhaustive"
    assert payload["result_summary"]["coverage"][
        "quotient_points_exhausted"
    ] == 62
    assert any(
        "infinite spatial support" in limitation
        for limitation in payload["limitations"]
    )
