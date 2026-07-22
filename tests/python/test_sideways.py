from __future__ import annotations

import itertools
import json
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

import pytest

import rule30_research_reference as supplied
from rule30lab.sideways import (
    SidewaysLimits,
    SidewaysResourceLimitError,
    decode_certificate_outcomes,
    eventually_periodic_trace,
    first_nonzero_left_depth,
    logical_reconstruction_work,
    periodic_trace,
    reconstruct_left_initial,
    right_neighbor_trace,
    search_eventually_periodic,
    search_pure_periods,
    truncated_periodic_state_graph,
    truncated_right_transition,
    word_from_index,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TRUSTED_CENTER = (
    REPOSITORY_ROOT
    / "tests"
    / "reference_vectors"
    / "center_c00000000_c00009999.u8"
)
EXPERIMENT_SCRIPT = (
    REPOSITORY_ROOT
    / "experiments"
    / "problem1_nonperiodicity"
    / "run_sideways_search.py"
)


def _direct_sideways_oracle(center: Sequence[int]) -> tuple[bytearray, bytearray]:
    """Cell-by-cell oracle with no packed operations from the maintained code."""

    horizon = len(center) - 1
    right = [bytearray(horizon + 2) for _ in range(horizon + 1)]
    for time, bit in enumerate(center):
        right[time][0] = bit
    for time in range(horizon):
        for position in range(1, horizon + 1):
            right[time + 1][position] = right[time][position - 1] ^ (
                right[time][position] | right[time][position + 1]
            )

    current = bytearray(center)
    neighbor = bytearray(right[time][1] for time in range(horizon + 1))
    initial_left = bytearray()
    for depth in range(1, horizon + 1):
        new_length = horizon + 1 - depth
        new_column = bytearray(
            current[time + 1] ^ (current[time] | neighbor[time])
            for time in range(new_length)
        )
        initial_left.append(new_column[0])
        neighbor = current[:new_length]
        current = new_column
    return bytearray(row[1] for row in right), initial_left


def _center_trace_from_initial_left(c0: int, initial_left: Sequence[int]) -> bytearray:
    """Independent full-row evolution used as an exhaustive round-trip oracle."""

    horizon = len(initial_left)
    minimum = -horizon
    maximum = horizon
    row = {position: 0 for position in range(minimum, maximum + 1)}
    row[0] = c0
    for depth, bit in enumerate(initial_left, start=1):
        row[-depth] = bit

    center = bytearray((c0,))
    for _ in range(horizon):
        row = {
            position: row.get(position - 1, 0)
            ^ (row.get(position, 0) | row.get(position + 1, 0))
            for position in range(minimum, maximum + 1)
        }
        center.append(row[0])
    return center


def test_explicit_center_horizon_convention_and_edge_cases() -> None:
    assert reconstruct_left_initial((0,)) == bytearray()
    assert reconstruct_left_initial((1,)) == bytearray()
    assert right_neighbor_trace((1,)) == bytearray((0,))
    assert logical_reconstruction_work(0) == 0
    assert logical_reconstruction_work(3) == 15

    with pytest.raises(ValueError, match="nonempty"):
        reconstruct_left_initial(())
    with pytest.raises(ValueError, match=r"center\[1\]"):
        reconstruct_left_initial((1, 2))
    with pytest.raises(ValueError, match="nonnegative"):
        logical_reconstruction_work(-1)


def test_packed_engine_matches_cell_by_cell_oracle_for_every_small_trace() -> None:
    for horizon in range(8):
        for center in itertools.product((0, 1), repeat=horizon + 1):
            expected_right, expected_left = _direct_sideways_oracle(center)
            assert right_neighbor_trace(center) == expected_right
            assert reconstruct_left_initial(center) == expected_left
            expected_first = next(
                (depth for depth, bit in enumerate(expected_left, start=1) if bit),
                None,
            )
            assert first_nonzero_left_depth(center) == expected_first


def test_exhaustive_small_initial_left_round_trips() -> None:
    for horizon in range(7):
        for c0 in (0, 1):
            for initial_left in itertools.product((0, 1), repeat=horizon):
                center = _center_trace_from_initial_left(c0, initial_left)
                assert reconstruct_left_initial(center) == bytearray(initial_left)


def test_maintained_engine_audits_immutable_reference_exhaustively() -> None:
    for horizon in range(7):
        for center in itertools.product((0, 1), repeat=horizon + 1):
            assert list(reconstruct_left_initial(center)) == supplied.reconstruct_left_initial(
                center
            )


def test_true_trusted_trace_reconstructs_zero_left_tail() -> None:
    trusted = TRUSTED_CENTER.read_bytes()
    horizon = 500
    reconstructed = reconstruct_left_initial(trusted[: horizon + 1])
    assert len(reconstructed) == horizon
    assert reconstructed == bytearray(horizon)


def test_periodic_and_eventually_periodic_generators_use_c0_first() -> None:
    assert periodic_trace((1, 0), 6) == bytearray((1, 0, 1, 0, 1, 0, 1))
    assert eventually_periodic_trace((1, 1, 0), (0, 1), 8) == bytearray(
        (1, 1, 0, 0, 1, 0, 1, 0, 1)
    )
    assert eventually_periodic_trace((), (1,), 2) == bytearray((1, 1, 1))
    assert word_from_index(0, 0) == b""
    assert word_from_index(5, 4) == bytes((0, 1, 0, 1))

    with pytest.raises(ValueError, match="nonempty"):
        periodic_trace((), 3)
    with pytest.raises(ValueError, match="does not fit"):
        word_from_index(4, 2)


@pytest.mark.slow
def test_reported_pure_periods_one_through_ten_observation_at_horizon_500() -> None:
    result = search_pure_periods(max_period=10, horizon=500)
    assert result["status"] == "finite-exhaustive"
    assert result["candidate_descriptions"] == sum(1 << width for width in range(1, 11))
    assert result["zero_left_survivor_descriptions"] == 10
    assert result["distinct_survivor_periodic_sequences"] == 1
    assert result["survivor_primitive_roots"] == ["0"]
    assert result["single_seed_survivor_descriptions"] == 0
    assert result["nonzero_trace_survivor_descriptions"] == 0
    assert result["only_constant_zero_trace_survives"] is True
    assert max(
        report["maximum_first_nonzero_depth"] or 0
        for report in result["per_period"]
    ) == 11

    outcomes = decode_certificate_outcomes(result["certificate"])
    assert len(outcomes) == 2046
    assert outcomes.count(0) == 10


def test_bounded_preperiod_plus_period_search_is_exhaustive() -> None:
    result = search_eventually_periodic(
        max_preperiod=2,
        max_period=3,
        horizon=32,
    )
    expected = sum(
        1 << (preperiod + period)
        for preperiod in range(3)
        for period in range(1, 4)
    )
    assert expected == 98
    assert result["candidate_descriptions"] == expected
    assert result["zero_left_survivor_descriptions"] == 9
    assert result["all_zero_trace_survivor_descriptions"] == 9
    assert result["single_seed_survivor_descriptions"] == 0
    assert result["only_all_zero_descriptions_survive"] is True
    assert decode_certificate_outcomes(result["certificate"]).count(0) == 9


def test_small_horizon_reports_a_counterexample_instead_of_overclaiming() -> None:
    result = search_pure_periods(max_period=1, horizon=0)
    assert result["candidate_descriptions"] == 2
    assert result["zero_left_survivor_descriptions"] == 2
    assert result["only_constant_zero_trace_survives"] is False
    assert result["first_counterexample_to_only_constant_zero"]["word"] == "1"
    assert decode_certificate_outcomes(result["certificate"]) == (0, 0)


def test_certificate_integrity_failure_is_detected() -> None:
    result = search_pure_periods(max_period=2, horizon=4)
    certificate = dict(result["certificate"])
    certificate["payload_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="hash mismatch"):
        decode_certificate_outcomes(certificate)


def test_search_and_reconstruction_resource_bounds_fail_closed() -> None:
    tiny_horizon = SidewaysLimits(max_horizon=2)
    with pytest.raises(SidewaysResourceLimitError, match="horizon"):
        reconstruct_left_initial((1, 1, 0, 1), limits=tiny_horizon)

    tiny_candidates = SidewaysLimits(max_candidates=3)
    with pytest.raises(SidewaysResourceLimitError, match="candidate"):
        search_pure_periods(2, 3, limits=tiny_candidates)

    tiny_work = SidewaysLimits(max_logical_cell_updates=10)
    with pytest.raises(SidewaysResourceLimitError, match="logical search work"):
        search_pure_periods(1, 3, limits=tiny_work)

    tiny_certificate = SidewaysLimits(max_certificate_bytes=1)
    with pytest.raises(SidewaysResourceLimitError, match="certificate"):
        search_pure_periods(1, 1, limits=tiny_certificate)


def test_fixed_width_transition_matches_direct_cells() -> None:
    width = 5
    for state in range(1 << width):
        cells = [(state >> position) & 1 for position in range(width)]
        for boundary in (0, 1):
            expected = 0
            for position in range(width):
                left = boundary if position == 0 else cells[position - 1]
                center = cells[position]
                right = cells[position + 1] if position + 1 < width else 0
                expected |= (left ^ (center | right)) << position
            assert truncated_right_transition(state, boundary, width) == expected


def test_fixed_width_graph_has_proved_finite_bound_and_deterministic_hash() -> None:
    first = truncated_periodic_state_graph((1, 0, 1), width=4)
    second = truncated_periodic_state_graph((1, 0, 1), width=4)
    assert first == second
    assert first["node_count"] == 3 * (1 << 4)
    assert first["edge_count"] == first["node_count"]
    assert sum(
        int(degree) * count for degree, count in first["indegree_histogram"].items()
    ) == first["edge_count"]
    assert first["zero_initial_orbit"]["visited_nodes_before_repeat"] <= first[
        "node_count"
    ]

    limits = SidewaysLimits(max_graph_states=31)
    with pytest.raises(SidewaysResourceLimitError, match="state bound"):
        truncated_periodic_state_graph((1,), width=5, limits=limits)


def test_json_experiment_is_deterministic_for_small_parameters() -> None:
    command = (
        sys.executable,
        str(EXPERIMENT_SCRIPT),
        "--horizon",
        "24",
        "--max-period",
        "4",
        "--max-preperiod",
        "1",
        "--eventual-max-period",
        "2",
        "--graph-width",
        "3",
        "--graph-max-period",
        "2",
    )
    first = subprocess.run(command, check=True, capture_output=True, text=True).stdout
    second = subprocess.run(command, check=True, capture_output=True, text=True).stdout
    assert first == second
    record = json.loads(first)
    assert record["status"] == "finite-exhaustive"
    assert record["question"] == "problem1"
    assert record["trusted_trace_check"]["nonzero_reconstructed_left_bits"] == 0
