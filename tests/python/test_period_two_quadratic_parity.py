from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[2]
    / "experiments"
    / "problem1_nonperiodicity"
    / "analyze_period_two_quadratic_parity.py"
)
SPEC = importlib.util.spec_from_file_location("period_two_quadratic_parity", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
QUADRATIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUADRATIC)


def test_factor_parity_implementations_agree() -> None:
    patterns = QUADRATIC.factor_patterns(3)
    for word in [(), ("t",), ("t", "p", "u", "t", "t", "u")]:
        assert QUADRATIC.factor_parities_direct(word, patterns) == (
            QUADRATIC.factor_parities_streaming(word, patterns)
        )


def test_range_one_quadratic_system_forces_constant_terminal_potential() -> None:
    result = QUADRATIC.verify_range(1)
    assert result["all_checks_pass"] is True
    assert result["combined_branch_system"]["rank"] == 10
    assert result["combined_branch_system"]["nullity"] == 2


def test_range_two_quadratic_system_forces_constant_terminal_potential() -> None:
    result = QUADRATIC.verify_range(2)
    assert result["all_checks_pass"] is True
    assert result["quadratic_monomials"] == 78
    assert result["combined_branch_system"]["rank"] == 69
    assert result["combined_branch_system"]["terminal_potential"] == (
        "V_00=V_01=V_10=V_11"
    )


def test_range_three_quadratic_system_forces_constant_terminal_potential() -> None:
    result = QUADRATIC.verify_range(3)
    assert result["all_checks_pass"] is True
    assert result["factor_parity_features"] == 39
    assert result["quadratic_monomials"] == 780
    assert result["combined_branch_system"]["equations"] == 6422
    assert result["combined_branch_system"]["variables"] == 786
    assert result["combined_branch_system"]["rank"] == 582


def test_campaign_is_deterministic() -> None:
    left = QUADRATIC.run_campaign(2)
    right = QUADRATIC.run_campaign(2)
    assert left == right
    assert len(left["certificate_sha256"]) == 64


def test_invalid_factor_ranges_are_rejected() -> None:
    with pytest.raises(ValueError):
        QUADRATIC.factor_patterns(0)
    with pytest.raises(QUADRATIC.QuadraticParityLimitError):
        QUADRATIC.run_campaign(4)
