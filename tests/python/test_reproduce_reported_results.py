from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from rule30lab.core import center_bits_cell_array


SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "reproduce_reported_results.py"
SPEC = importlib.util.spec_from_file_location("reproduce_reported_results", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_small_supplied_reference_summary_matches_independent_engine() -> None:
    summary = MODULE.python_reference_summary(9)
    expected = bytes(center_bits_cell_array(9))
    assert summary["ones"] == sum(expected)
    assert summary["discrepancy"] == 2 * sum(expected) - len(expected)
    assert summary["count"] == len(expected)


def test_small_two_kernel_summary_has_equal_length_records() -> None:
    bits = bytes(center_bits_cell_array(128))
    summary = MODULE.two_kernel_summary(
        bits, first_level=1, last_level=3, prefix_length=8
    )
    assert [record["required_input_length"] for record in summary["levels"]] == [
        16,
        32,
        64,
    ]
    assert len(summary["canonical_level_records_sha256"]) == 64
    assert "nonautomaticity" in summary["interpretation"]


def test_two_kernel_rejects_insufficient_data() -> None:
    with pytest.raises(ValueError, match="require 64"):
        MODULE.two_kernel_summary(
            bytes(center_bits_cell_array(32)),
            first_level=1,
            last_level=3,
            prefix_length=8,
        )


def test_input_reader_rejects_nonbinary_byte(tmp_path: Path) -> None:
    path = tmp_path / "bad.u8"
    path.write_bytes(bytes((0, 1, 2)))
    with pytest.raises(ValueError, match="expected numeric 0 or 1"):
        MODULE._validated_input(path)
