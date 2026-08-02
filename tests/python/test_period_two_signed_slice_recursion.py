from __future__ import annotations

import functools
import importlib.util
import sys
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments/problem1_nonperiodicity/analyze_period_two_signed_slice_recursion.py"
)
SPEC = importlib.util.spec_from_file_location('signed_slice', MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
signed_slice = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = signed_slice
SPEC.loader.exec_module(signed_slice)


@functools.lru_cache(maxsize=None)
def campaign(maximum_complexity: int):
    return signed_slice.run_campaign(maximum_complexity)


def test_frontier_generator_and_small_levels() -> None:
    assert signed_slice.forward_generator('t', 1) == 7
    assert signed_slice.forward_generator('u', 1) == 6
    assert signed_slice.forward_generator('p', 1) == 6
    levels = signed_slice.build_levels(5)
    assert [len(levels[k]) for k in range(1, 6)] == [1, 2, 4, 9, 18]


def test_local_signed_factor_table() -> None:
    assert signed_slice.local_signed_factor(0b1011, 0b1011) == -1
    assert signed_slice.local_signed_factor(0b1011, 0b1111) == 1
    assert signed_slice.local_signed_factor(0b1100, 0b1011) == 0
    assert signed_slice.local_signed_factor(0b1111, 0b1111) == 1


def test_controlled_campaign_16() -> None:
    result = campaign(16)
    assert result['outputs_built'] == 43_970
    assert result['gap_222_cylinders'] == 10
    assert result['ancestor_cylinders'] == 16
    assert result['signed_zero_ancestor_cylinders'] == 0
    assert result['signed_slice_disagreements'] == 0
    assert result['certificate_sha256'] == '459ad0505c55ef7c7622c203ad3d8df8a1dfaf454c00de168be28ead355f1e39'


def test_controlled_campaign_18() -> None:
    result = campaign(18)
    assert result['outputs_built'] == 144_173
    assert result['gap_222_cylinders'] == 26
    assert result['ancestor_cylinders'] == 43
    assert result['signed_zero_ancestor_cylinders'] == 0
    assert result['minimum_absolute_ancestor_mass'] == 2
    assert result['signed_slice_disagreements'] == 0
    assert result['certificate_sha256'] == '6153f7a60f7ea8c2a2d4f28950e8e19d8a9e51b43e673fc8b58af86d073268d8'


def test_exact_slice_prediction_on_obstruction() -> None:
    levels = signed_slice.build_levels(18)
    node = signed_slice.Cylinder(18, 0x642E4D2F1, 3)
    assert signed_slice.predicted_child_mass(levels, node) == signed_slice.signed_mass(levels, node) == -83


def test_scalar_magnitude_obstruction() -> None:
    obstruction = campaign(18)['scalar_magnitude_obstruction']
    assert obstruction is not None
    assert obstruction['parent_a']['signed_mass'] == obstruction['parent_b']['signed_mass'] == 1650
    assert obstruction['a']['current_masks'][0] == obstruction['b']['current_masks'][0] == '1011'
    assert {obstruction['a']['signed_mass'], obstruction['b']['signed_mass']} == {104, 605}


def test_scalar_sign_obstruction_and_limit() -> None:
    obstruction = campaign(18)['scalar_sign_obstruction']
    assert obstruction is not None
    assert obstruction['parent_a']['signed_mass'] > 0
    assert obstruction['parent_b']['signed_mass'] > 0
    assert obstruction['a']['current_masks'][0] == obstruction['b']['current_masks'][0] == '1011'
    assert obstruction['a']['signed_mass'] == -83
    assert obstruction['b']['signed_mass'] == 2
    with pytest.raises(signed_slice.SignedSliceLimitError):
        signed_slice.run_campaign(19)
