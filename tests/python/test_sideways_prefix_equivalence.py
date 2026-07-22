from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_sideways_prefix_equivalence.py"
)
SPEC = importlib.util.spec_from_file_location("sideways_prefix_equivalence", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)


def test_first_mismatch_index_contract() -> None:
    assert module.first_mismatch_index((1, 0, 1), (1, 0, 1)) is None
    assert module.first_mismatch_index((1, 0, 1), (1, 1, 1)) == 1
    with pytest.raises(ValueError, match="equal length"):
        module.first_mismatch_index((1,), (1, 0))


def test_reference_center_handles_both_initial_center_bits() -> None:
    assert module.reference_center(0, 4) == bytes(5)
    assert module.reference_center(1, 4) == bytes((1, 1, 0, 1, 1))
    with pytest.raises(ValueError, match="c0"):
        module.reference_center(2, 4)


def test_exhaustive_equivalence_small_family() -> None:
    result = module.exhaustive_equivalence(8)
    assert result["traces_checked"] == 2 * ((1 << 9) - 1)
    assert result["failures"] == 0
    assert result["per_horizon"][-1]["equal_reference_traces"] == 2
    assert result["per_horizon"][-1]["first_mismatch_histogram"]["8"] == 2


def test_exhaustive_equivalence_caps_before_work() -> None:
    with pytest.raises(module.PrefixEquivalenceLimitError, match="traces"):
        module.exhaustive_equivalence(8, max_traces=100)
    with pytest.raises(module.PrefixEquivalenceLimitError, match="logical"):
        module.exhaustive_equivalence(8, max_logical_cell_updates=100)


def test_direct_periodic_description_histogram_matches_reconstruction() -> None:
    direct = module.periodic_description_prefix_search(2, 4, 16)

    from rule30lab.sideways import (
        eventually_periodic_trace,
        first_nonzero_left_depth,
    )

    expected: dict[str, int] = {}
    descriptions = 0
    for preperiod_length in range(3):
        for period_length in range(1, 5):
            for code in range(1, 1 << (preperiod_length + period_length), 2):
                preperiod = tuple(
                    (code >> index) & 1 for index in range(preperiod_length)
                )
                period = tuple(
                    (code >> (preperiod_length + index)) & 1
                    for index in range(period_length)
                )
                trace = eventually_periodic_trace(preperiod, period, 16)
                depth = first_nonzero_left_depth(trace)
                assert depth is not None
                expected[str(depth)] = expected.get(str(depth), 0) + 1
                descriptions += 1

    assert direct["descriptions_checked"] == descriptions
    assert direct["descriptions_matching_through_horizon"] == 0
    assert direct["first_mismatch_histogram"] == expected


def test_periodic_description_validation_and_cap() -> None:
    with pytest.raises(ValueError, match="horizon"):
        module.periodic_description_prefix_search(3, 4, 6)
    with pytest.raises(module.PrefixEquivalenceLimitError, match="descriptions"):
        module.periodic_description_prefix_search(3, 4, 16, max_descriptions=10)
