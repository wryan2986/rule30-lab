from __future__ import annotations

import collections
import sys

import pytest

import rule30_research_reference as supplied
from rule30lab.core import center_bits_cell_array


def test_supplied_center_column_matches_cell_array_for_small_horizons() -> None:
    for steps in range(65):
        assert supplied.center_column(steps) == center_bits_cell_array(steps + 1)


def test_supplied_center_column_edge_cases() -> None:
    assert supplied.center_column(0) == bytearray((1,))
    with pytest.raises(ValueError, match="nonnegative"):
        supplied.center_column(-1)


def test_supplied_balance_report(capsys: pytest.CaptureFixture[str]) -> None:
    supplied.balance_report(bytearray((1, 0, 1, 1)), (4, 2, 2, 0, 9))
    output = capsys.readouterr().out
    assert "N=        2" in output and "D=      0" in output
    assert "N=        4" in output and "D=      2" in output


def test_supplied_autocorrelation() -> None:
    assert supplied.autocorrelation((0, 1, 0, 1), 1) == -1.0
    assert supplied.autocorrelation((0, 1, 0, 1), 2) == 1.0
    for lag in (0, 4, 5):
        with pytest.raises(ValueError):
            supplied.autocorrelation((0, 1, 0, 1), lag)


def test_supplied_block_counts() -> None:
    assert supplied.block_counts((0, 0, 1, 0), 2) == collections.Counter(
        {0: 1, 1: 1, 2: 1, 3: 0}
    )
    for width in (0, 5):
        with pytest.raises(ValueError):
            supplied.block_counts((0, 1, 0, 1), width)


@pytest.mark.parametrize(
    ("bits", "expected"),
    [
        ((0,), 0),
        ((0, 0, 0, 0), 0),
        ((1, 1, 1, 1), 1),
        ((0, 1, 0, 1, 0, 1), 2),
        ((1, 0, 0, 1, 1, 0, 1), 4),
    ],
)
def test_supplied_berlekamp_massey_known_cases(bits: tuple[int, ...], expected: int) -> None:
    assert supplied.berlekamp_massey_binary(bits) == expected


def test_supplied_berlekamp_massey_empty_input_defect_is_characterized() -> None:
    with pytest.raises(IndexError):
        supplied.berlekamp_massey_binary(())


def test_supplied_longest_matching_suffix() -> None:
    bits = (0, 1, 0, 1, 0, 1, 1)
    assert supplied.longest_matching_suffix_for_period(bits, 2) == 0
    assert supplied.longest_matching_suffix_for_period(bits[:-1], 2) == 4
    for period in (0, len(bits)):
        with pytest.raises(ValueError):
            supplied.longest_matching_suffix_for_period(bits, period)


def test_supplied_two_kernel_distinct_prefixes() -> None:
    bits = bytearray((0, 1, 1, 1, 0, 1, 1, 1))
    assert supplied.two_kernel_distinct_prefixes(bits, 1, 4) == 2
    assert supplied.two_kernel_distinct_prefixes(bits, 2, 2) == 2


def test_supplied_sideways_reconstruction_true_trace() -> None:
    for horizon in range(9):
        center = center_bits_cell_array(horizon + 1)
        assert supplied.reconstruct_left_initial(center) == [0] * horizon
    assert supplied.reconstruct_left_initial(()) == []


def test_supplied_periodic_trace() -> None:
    assert supplied.periodic_trace("10", 7) == bytearray((1, 0, 1, 0, 1, 0, 1))
    assert supplied.periodic_trace("1", 0) == bytearray()
    for word in ("", "102", "x"):
        with pytest.raises(ValueError):
            supplied.periodic_trace(word, 3)


def test_supplied_main_smoke(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setattr(sys, "argv", ["rule30_research_reference.py", "--steps", "4"])
    supplied.main()
    output = capsys.readouterr().out
    assert "First 80 center bits:\n11011" in output
    assert "True trace sideways reconstruction over 4 cells: 0" in output
