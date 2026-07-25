from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_return_word_precision.py"
)
spec = importlib.util.spec_from_file_location("return_word_precision", MODULE_PATH)
assert spec is not None and spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_initial_return_sequence_from_zero() -> None:
    word, successor = mod.follow_returns(0, 5)
    assert word == (4, 2, 5, 2, 5)
    assert successor >= 0


def test_span_six_exact_census() -> None:
    representatives = mod.enumerate_return_words(6)
    assert len(representatives) == 10
    assert {word for word in representatives if len(word) == 1} == {
        (2,),
        (3,),
        (4,),
        (5,),
    }
    assert (2, 2, 2) in representatives


def test_representatives_lie_in_dependency_cylinders() -> None:
    for word, representative in mod.enumerate_return_words(7).items():
        span = sum(word)
        assert representative < 1 << (2 * span)
        observed, _ = mod.follow_returns(representative, len(word))
        assert observed == word


def test_precision_witness_preserves_complete_word() -> None:
    representatives = mod.enumerate_return_words(8)
    for word, representative in representatives.items():
        span = sum(word)
        target = mod.universal_threshold(span)
        witness = mod.precision_witness(word, representative, target)
        assert witness["return_word_preserved"] is True
        assert witness["successor_xor"] == 1 << (target - 1)
        assert witness["required_source_bits"] == target + 2 * span


def test_precision_formulas_and_validation() -> None:
    assert mod.required_source_bits(17, 6) == 29
    assert mod.universal_threshold(6) == 29
    with pytest.raises(ValueError):
        mod.required_source_bits(0, 6)
    with pytest.raises(ValueError):
        mod.precision_witness((4,), 0, 20)


def test_controlled_limit_guard() -> None:
    with pytest.raises(mod.ReturnWordPrecisionLimitError):
        mod.enumerate_return_words(0)
    with pytest.raises(mod.ReturnWordPrecisionLimitError):
        mod.enumerate_return_words(mod.ABSOLUTE_SPAN_CAP + 1)


def test_span_six_certificate_is_stable() -> None:
    payload = mod.run_campaign(6)
    assert payload["certificate_sha256"] == (
        "95813839cad593ab6954fa54a40c1d85315f81b8e37694265822272dafd9b18f"
    )
    assert payload["census"]["witness_checks"] == 50
