from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_return_precision.py"
)
spec = importlib.util.spec_from_file_location("return_precision", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_interior_impulse_lemma() -> None:
    assert module.isolated_impulse_support(5) == [
        -10,
        -9,
        -6,
        -1,
        1,
        2,
        3,
        4,
        6,
        7,
        10,
    ]


def test_known_first_returns() -> None:
    assert module.first_return(0) == (4, 56)
    assert module.first_return(7)[0] == 5
    assert module.first_return(28)[0] == 2


def test_gap_conditioned_precision_formula() -> None:
    assert [
        module.source_bits_for_gap(9, gap) for gap in (2, 3, 4, 5)
    ] == [13, 15, 17, 19]
    assert module.worst_case_source_bits(9) == 19


def test_all_finite_precision_witnesses() -> None:
    for bits in range(4, 13):
        row = module.precision_witness(bits)
        assert row["required_source_bits"] == bits + 10
        assert row["successor_xor"] == 1 << (bits - 1)


def test_uniform_sparse_witness_family() -> None:
    for bits in range(13, 25):
        row = module.precision_witness(bits)
        assert row["base_z"] == 7
        assert row["left_outcome"][0] == row["right_outcome"][0] == 5


def test_small_campaign_certificate() -> None:
    result = module.run_campaign(6)
    assert result["certificate_sha256"] == (
        "8c27ba880121f2b5e2d5190e7c9f2d5bb7e3961594397cfe78127c69d6c72ed5"
    )
    assert [row["target_bits"] for row in result["levels"]] == [4, 5, 6]


def test_controlled_limits() -> None:
    try:
        module.run_campaign(module.ABSOLUTE_MAXIMUM_EXHAUSTIVE_BITS + 1)
    except module.ReturnPrecisionLimitError:
        pass
    else:
        raise AssertionError("expected controlled-limit exception")
