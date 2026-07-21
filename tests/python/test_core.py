from __future__ import annotations

import itertools

import pytest

from rule30lab.core import center_bits_cell_array, evolve_row, generate_rows, rule30_bit


def test_truth_table_matches_rule_30_numbering() -> None:
    neighborhoods = list(itertools.product((1, 0), repeat=3))
    outputs = [rule30_bit(*triple) for triple in neighborhoods]
    assert outputs == [0, 0, 0, 1, 1, 1, 1, 0]


@pytest.mark.parametrize("position", range(3))
def test_local_rule_rejects_nonbits(position: int) -> None:
    values = [0, 0, 0]
    values[position] = 2
    with pytest.raises(ValueError, match="must be 0 or 1"):
        rule30_bit(*values)


def test_hand_derived_first_five_rows() -> None:
    rows = [bytes(row) for row in generate_rows(4)]
    assert rows == [
        b"\x01",
        b"\x01\x01\x01",
        b"\x01\x01\x00\x00\x01",
        b"\x01\x01\x00\x01\x01\x01\x01",
        b"\x01\x01\x00\x00\x01\x00\x00\x00\x01",
    ]


def test_evolve_row_checks_bits_and_boundaries() -> None:
    assert evolve_row([]) == bytearray((0, 0))
    assert evolve_row((1,)) == bytearray((1, 1, 1))
    with pytest.raises(ValueError):
        evolve_row((0, -1, 1))


def test_generate_rows_horizon_and_copy_semantics() -> None:
    rows = list(generate_rows(2))
    assert [len(row) for row in rows] == [1, 3, 5]
    rows[0][0] = 0
    assert rows[1] == bytearray((1, 1, 1))
    with pytest.raises(ValueError):
        list(generate_rows(-1))


def test_center_count_convention() -> None:
    assert center_bits_cell_array(0) == bytearray()
    assert center_bits_cell_array(1) == bytearray((1,))
    assert center_bits_cell_array(5) == bytearray((1, 1, 0, 1, 1))
    with pytest.raises(ValueError):
        center_bits_cell_array(-1)
