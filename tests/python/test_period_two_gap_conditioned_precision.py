from __future__ import annotations

import importlib.util
from pathlib import Path

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_gap_conditioned_precision.py"
)
spec = importlib.util.spec_from_file_location("gap_conditioned_precision", MODULE_PATH)
assert spec is not None and spec.loader is not None
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_registered_bases_have_requested_return_gaps() -> None:
    for gap in module.RETURN_GAPS:
        for target_bits in range(5, 13):
            base = module.witness_base(gap, target_bits)
            assert module.first_return(base)[0] == gap


def test_required_source_bits_are_gap_specific() -> None:
    assert [
        module.required_source_bits(9, gap) for gap in module.RETURN_GAPS
    ] == [13, 15, 17, 19]


def test_small_width_witnesses_flip_top_target_bit() -> None:
    for gap in module.RETURN_GAPS:
        start = module.UNIFORM_FAMILIES[gap]["start_k"]
        for target_bits in range(5, start):
            row = module.precision_witness(gap, target_bits)
            assert row["successor_xor"] == 1 << (target_bits - 1)


def test_uniform_witness_families_hold_through_width_40() -> None:
    result = module.verify_uniform_families(40)
    assert result["all_checks_pass"]
    assert [row["gap"] for row in result["families"]] == [2, 3, 4, 5]


def test_stable_response_support_has_extreme_displacement() -> None:
    for gap, support in module.STABLE_RESPONSE_SUPPORTS.items():
        assert support[0] == -2 * gap
        assert all(value > -2 * gap for value in support[1:])


def test_default_campaign_scope_and_total() -> None:
    result = module.run_campaign()
    assert result["total_states_exhausted"] == 652800
    assert len(result["levels"]) == 16
    assert all(row["exact_precision"] for row in result["levels"])


def test_default_certificate_is_stable() -> None:
    assert (
        module.run_campaign()["certificate_sha256"]
        == "c012d44526c3309387ae1e4984ef41ece5cf676a547754481aafe8eadf2852c2"
    )
