from __future__ import annotations

from rule30lab.sideways import reconstruct_left_initial


def _step(state: int) -> int:
    return state ^ ((state << 1) | (state << 2))


def _direct_initial_row(seed: int) -> dict[int, int]:
    return {
        -depth: (seed >> depth) & 1
        for depth in range(seed.bit_length())
    }


def _direct_step(row: dict[int, int], minimum: int, maximum: int) -> dict[int, int]:
    return {
        position: row.get(position - 1, 0)
        ^ (row.get(position, 0) | row.get(position + 1, 0))
        for position in range(minimum, maximum + 1)
    }


def _moving_state_from_row(row: dict[int, int], time: int, width: int) -> int:
    return sum(row.get(time - depth, 0) << depth for depth in range(width))


def test_right_edge_integer_recurrence_matches_direct_rule30() -> None:
    for seed in range(1, 1 << 6, 2):
        state = seed
        row = _direct_initial_row(seed)
        minimum = -(seed.bit_length() - 1)
        for time in range(9):
            width = seed.bit_length() + 2 * time
            assert _moving_state_from_row(row, time, width) == state
            assert ((state >> time) & 1) == row.get(0, 0)
            assert state & 1 == 1
            state = _step(state)
            row = _direct_step(row, minimum - time - 1, time + 1)


def test_every_small_odd_seed_round_trips_through_sideways_reconstruction() -> None:
    horizon = 8
    for seed in range(1, 1 << 7, 2):
        state = seed
        center = bytearray()
        for time in range(horizon + 1):
            center.append((state >> time) & 1)
            state = _step(state)
        expected_left = bytearray(
            (seed >> depth) & 1 for depth in range(1, horizon + 1)
        )
        assert reconstruct_left_initial(center) == expected_left


def test_fixed_coordinate_power_of_two_period_bound_exhaustively() -> None:
    for width in range(1, 11):
        mask = (1 << width) - 1
        steps = 1 << (width - 1)
        for seed in range(1 << width):
            state = seed
            for _ in range(steps):
                state = _step(state) & mask
            assert state == seed
