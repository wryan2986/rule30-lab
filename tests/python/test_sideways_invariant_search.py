from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SEARCH_SCRIPT = (
    REPOSITORY_ROOT
    / "experiments"
    / "problem1_nonperiodicity"
    / "search_sideways_invariants.py"
)


def _load_search_module():
    specification = importlib.util.spec_from_file_location(
        "rule30_sideways_invariant_search_for_test", SEARCH_SCRIPT
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


SEARCH = _load_search_module()


def _direct_new_symbol(current: int, following: int) -> int:
    a = current & 1
    b = (current >> 1) & 1
    following_a = following & 1
    return (following_a ^ (a | b)) | (a << 1)


def _direct_cyclic_transition(state: int, period: int) -> int:
    mask = (1 << period) - 1
    a = [(state >> time) & 1 for time in range(period)]
    b = [(state >> (period + time)) & 1 for time in range(period)]
    left = [
        a[(time + 1) % period] ^ (a[time] | b[time])
        for time in range(period)
    ]
    return sum(bit << time for time, bit in enumerate(left)) | (
        (state & mask) << period
    )


def _small_arguments() -> argparse.Namespace:
    return argparse.Namespace(
        max_density_width=2,
        max_phase_period=2,
        max_affine_window=3,
        max_boolean_window=2,
        max_image_width=5,
        max_cyclic_period=4,
        max_linear_unknowns=4_096,
        max_linear_equations=16_384,
        max_summary_candidates=1_000_000,
        max_image_states=65_536,
        max_cyclic_states=65_536,
    )


def test_local_rule_and_cyclic_transition_match_independent_bit_oracles() -> None:
    for current in range(4):
        for following in range(4):
            assert SEARCH._rule30_new_symbol(current, following) == (
                _direct_new_symbol(current, following)
            )

    for period in range(1, 5):
        for state in range(1 << (2 * period)):
            assert SEARCH.cyclic_pair_transition(state, period) == (
                _direct_cyclic_transition(state, period)
            )


def test_gf2_rref_and_nullspace_are_exact() -> None:
    # x0 + x1 = 0 and x1 + x2 = 0 have nullspace span(111).
    rows = [0b011, 0b110]
    reduced, pivots = SEARCH._rref(rows, 3)
    assert pivots == [0, 1]
    assert len(reduced) == 2
    nullspace = SEARCH._nullspace(rows, 3)
    assert nullspace == [0b111]
    assert all((row & nullspace[0]).bit_count() % 2 == 0 for row in rows)


def test_local_parity_search_finds_only_trivial_rule30_densities() -> None:
    first = SEARCH.search_local_parity_conservation(2, 2)
    second = SEARCH.search_local_parity_conservation(2, 2)
    assert first == second
    assert first["equation_count"] == 128
    assert first["unknown_count"] == 64
    assert first["conserved_density_dimension"] == 8
    assert first["trivial_constant_and_coboundary_dimension"] == 8
    assert first["nontrivial_quotient_dimension"] == 0
    assert first["all_trivial_densities_verified_conserved"] is True
    assert len(first["certificate"]["equation_matrix_sha256"]) == 64

    identity = SEARCH.search_local_parity_conservation(
        1,
        1,
        local_rule=SEARCH._identity_new_symbol,
        rule_name="identity-positive-control",
    )
    assert identity["conserved_density_dimension"] == 4
    assert identity["nontrivial_quotient_dimension"] == 3

    density_a = sum((symbol & 1) << symbol for symbol in range(4))
    assert SEARCH.find_density_counterexample(density_a, 1) == {
        "cycle_length": 1,
        "old_pair_symbols": [1],
        "new_pair_symbols": [2],
        "old_total": 1,
        "new_total": 0,
    }


def test_phase_aware_search_has_expected_bounded_rank_pattern() -> None:
    for phase_period in (1, 2):
        for width in (1, 2, 3):
            result = SEARCH.search_local_parity_conservation(
                phase_period, width
            )
            expected_trivial_rank = phase_period * 4 ** (width - 1)
            assert result["conserved_density_dimension"] == expected_trivial_rank
            assert (
                result["trivial_constant_and_coboundary_dimension"]
                == expected_trivial_rank
            )
            assert result["nontrivial_quotient_dimension"] == 0


def test_window_summary_search_separates_mortal_from_persistent_predicates() -> None:
    for width in range(1, 5):
        affine = SEARCH.search_window_summaries(width, family="affine")
        assert affine["closed_summary_count"] == 2
        assert affine["closed_nonconstant_summary_count"] == 0
        assert affine["closed_persistent_nonconstant_summary_count"] == 0

    boolean_one = SEARCH.search_window_summaries(1, family="boolean")
    boolean_two = SEARCH.search_window_summaries(2, family="boolean")
    assert boolean_one["closed_summary_count"] == 2
    assert boolean_two["closed_summary_count"] == 32
    assert boolean_two["closed_nonconstant_summary_count"] == 30
    assert boolean_two["closed_persistent_nonconstant_summary_count"] == 0
    assert boolean_two["closed_transition_histogram"] == {
        "constant-0": 15,
        "constant-1": 15,
        "one-input-class-unused": 2,
    }

    identity = SEARCH.search_window_summaries(
        1,
        family="boolean",
        window_rule=SEARCH._identity_next_window,
        rule_name="identity-positive-control",
    )
    assert identity["closed_summary_count"] == 16
    assert identity["closed_nonconstant_summary_count"] == 14
    assert identity["closed_persistent_nonconstant_summary_count"] == 14


def test_image_subshift_is_exact_and_has_four_forbidden_edges() -> None:
    result = SEARCH.search_image_subshift(6)
    assert result["forbidden_edges"] == [[2, 0], [2, 1], [3, 2], [3, 3]]
    assert result["allowed_edge_count"] == 12
    assert result["each_symbol_in_degree"] == [3, 3, 3, 3]
    assert [
        item["admissible_image_windows"]
        for item in result["bounded_direct_checks"]
    ] == [4, 12, 36, 108, 324, 972]

    allowed = {tuple(edge) for edge in result["allowed_edges"]}
    for width in range(2, 5):
        direct_image = {
            SEARCH._next_window(state, width, extension)
            for state in range(1 << (2 * width))
            for extension in (0, 1)
        }
        decoded_language = set()
        for state in range(1 << (2 * width)):
            symbols = tuple(
                ((state >> time) & 1)
                | (((state >> (width + time)) & 1) << 1)
                for time in range(width)
            )
            if all(pair in allowed for pair in zip(symbols, symbols[1:])):
                decoded_language.add(state)
        assert direct_image == decoded_language


def test_lossless_window_obstruction_identifies_the_unseen_boundary_bit() -> None:
    for width in range(1, 7):
        witness = SEARCH.lossless_window_obstruction(width)
        assert witness["differing_output_bit_positions"] == [width - 1]
        assert witness["next_state_with_zero_extension"] != witness[
            "next_state_with_one_extension"
        ]


def test_cyclic_greatest_fixed_point_certificate_is_infinite_depth_in_model() -> None:
    expected_maximum_depth = [2, 2, 5, 7, 6, 7]
    for period, expected_depth in enumerate(expected_maximum_depth, start=1):
        first = SEARCH.search_cyclic_separating_certificate(period)
        second = SEARCH.search_cyclic_separating_certificate(period)
        assert first == second
        assert first["greatest_forever_safe_states"] == [0]
        assert first["greatest_forever_safe_set_size"] == 1
        assert first["center_one_starts_with_forever_safe_successor"] == 0
        assert first["maximum_first_nonzero_left_depth"] == expected_depth
        assert first["removed_per_fixed_point_round_including_final_zero"][-1] == 0
        assert sum(first["first_nonzero_left_depth_histogram"].values()) == (
            1 << (2 * period - 1)
        )


def test_all_searches_fail_closed_before_resource_caps() -> None:
    with pytest.raises(SEARCH.InvariantSearchLimitError, match="unknowns"):
        SEARCH.search_local_parity_conservation(2, 3, max_unknowns=255)
    with pytest.raises(SEARCH.InvariantSearchLimitError, match="equations"):
        SEARCH.search_local_parity_conservation(1, 3, max_equations=255)
    with pytest.raises(SEARCH.InvariantSearchLimitError, match="candidates"):
        SEARCH.search_window_summaries(2, family="boolean", max_candidates=65_535)
    with pytest.raises(SEARCH.InvariantSearchLimitError, match="output states"):
        SEARCH.search_image_subshift(4, max_states=255)
    with pytest.raises(SEARCH.InvariantSearchLimitError, match="cyclic period"):
        SEARCH.search_cyclic_separating_certificate(5, max_states=1_023)


def test_small_summary_and_cli_are_deterministic_exact_json() -> None:
    first = SEARCH.build_summary(_small_arguments())
    second = SEARCH.build_summary(_small_arguments())
    assert first == second
    assert first["status"] == "finite-exhaustive"
    assert first["local_parity_conservation_search"][
        "all_tested_solutions_trivial"
    ] is True
    assert first["bounded_window_summary_search"][
        "all_tested_closed_summaries_lose_their_distinction_after_one_step"
    ] is True
    assert first["cyclic_pair_cycle_separation"][
        "all_tested_periods_separated_at_infinite_depth_in_model"
    ] is True
    assert first["controls"]["controls_passed"] is True
    assert first["implementation"]["sha256"] == hashlib.sha256(
        SEARCH_SCRIPT.read_bytes()
    ).hexdigest()
    assert any("does not force" in limitation for limitation in first["limitations"])

    command = [
        sys.executable,
        str(SEARCH_SCRIPT),
        "--max-density-width",
        "1",
        "--max-phase-period",
        "1",
        "--max-affine-window",
        "2",
        "--max-boolean-window",
        "1",
        "--max-image-width",
        "3",
        "--max-cyclic-period",
        "3",
    ]
    run_one = subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    run_two = subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert run_one.stderr == run_two.stderr == ""
    assert run_one.stdout == run_two.stdout
    parsed = json.loads(run_one.stdout)
    assert parsed["experiment_id"] == "problem1-sideways-invariant-search-v1"
    assert parsed["parameters"]["max_cyclic_period"] == 3
