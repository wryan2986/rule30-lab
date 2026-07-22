from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from rule30lab.conservation import search_local_conservation
from rule30lab.polynomial_conservation import (
    MAX_INPUT_WIDTH,
    evaluate_monomial,
    evolve_block,
    monomial_supports,
    polynomial_conservation_matrix,
    search_polynomial_conservation,
    verify_search_certificate,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def test_monomial_basis_is_canonical_and_nonlinear() -> None:
    assert monomial_supports(3, 2) == (
        (),
        (0,),
        (1,),
        (2,),
        (0, 1),
        (0, 2),
        (1, 2),
    )
    assert evaluate_monomial((1, 0, 1), ()) == 1
    assert evaluate_monomial((1, 0, 1), (0, 2)) == 1
    assert evaluate_monomial((1, 0, 1), (0, 1)) == 0
    with pytest.raises(ValueError, match="strictly increasing"):
        evaluate_monomial((1, 1), (1, 0))


def test_two_step_block_evolution_matches_repeated_rule30_oracle() -> None:
    for value in range(1 << 6):
        word = tuple((value >> shift) & 1 for shift in range(5, -1, -1))
        first = tuple(
            left ^ (center | right)
            for left, center, right in zip(word, word[1:], word[2:])
        )
        expected = tuple(
            left ^ (center | right)
            for left, center, right in zip(first, first[1:], first[2:])
        )
        assert evolve_block(word, rule=30, time_steps=2) == expected


def test_polynomial_matrix_matches_direct_multistep_identity() -> None:
    matrix, density_basis, flux_basis = polynomial_conservation_matrix(
        2, 2, 2, rule=30, time_steps=2
    )
    density_coefficients = [3, -2, 5, 7]
    flux_coefficients = [
        11,
        13,
        -1,
        2,
        17,
        19,
        23,
        29,
        31,
        37,
        41,
        43,
        47,
        53,
        59,
        61,
    ]
    assert len(density_coefficients) == len(density_basis)
    assert len(flux_coefficients) == len(flux_basis)
    coefficients = density_coefficients + flux_coefficients

    def polynomial(
        block: tuple[int, ...],
        basis: tuple[tuple[int, ...], ...],
        values: list[int],
    ) -> int:
        return sum(
            coefficient * evaluate_monomial(block, support)
            for coefficient, support in zip(values, basis)
        )

    for word_value, row in enumerate(matrix):
        word = tuple(
            (word_value >> shift) & 1
            for shift in range(5, -1, -1)
        )
        evolved = evolve_block(word, rule=30, time_steps=2)
        direct = (
            polynomial(evolved, density_basis, density_coefficients)
            - polynomial(word[2:4], density_basis, density_coefficients)
            - polynomial(word[:-1], flux_basis, flux_coefficients)
            + polynomial(word[1:], flux_basis, flux_coefficients)
        )
        assert sum(left * right for left, right in zip(row, coefficients)) == direct


@pytest.mark.parametrize("field", ["rational", "gf2"])
def test_rule204_positive_control_and_rule30_negative_control(field: str) -> None:
    rule30 = search_polynomial_conservation(
        2, 2, 2, rule=30, time_steps=1, field=field
    )
    identity = search_polynomial_conservation(
        2, 2, 2, rule=204, time_steps=2, field=field
    )
    assert rule30["nontrivial_excess_nullity"] == 0
    assert identity["nontrivial_excess_nullity"] == 2
    assert verify_search_certificate(rule30)
    assert verify_search_certificate(identity)


@pytest.mark.parametrize("field", ["rational", "gf2"])
def test_full_lookup_basis_quotients_all_spatial_coboundaries(field: str) -> None:
    result = search_polynomial_conservation(
        3, 3, 4, rule=30, time_steps=1, field=field
    )
    assert result["certified_spatial_coboundary_rank"] == 3
    assert result["certified_trivial_subspace_rank"] == 5
    assert result["nullity"] == 5
    assert result["nontrivial_excess_nullity"] == 0


@pytest.mark.parametrize("field", ["rational", "gf2"])
def test_full_polynomial_basis_matches_independent_lookup_search(field: str) -> None:
    for width in range(1, 5):
        polynomial = search_polynomial_conservation(
            width,
            width,
            width + 1,
            rule=30,
            time_steps=1,
            field=field,
        )
        lookup = search_local_conservation(width, rule=30, field=field)
        assert polynomial["rank"] == lookup["rank"]
        assert polynomial["nullity"] == lookup["nullity"]
        assert (
            polynomial["certified_trivial_subspace_rank"]
            == lookup["certified_trivial_subspace_rank"]
        )
        assert (
            polynomial["nontrivial_excess_nullity"]
            == lookup["nontrivial_excess_nullity"]
        )


def test_search_output_is_deterministic() -> None:
    first = search_polynomial_conservation(
        3, 2, 2, rule=30, time_steps=2, field="gf2"
    )
    second = search_polynomial_conservation(
        3, 2, 2, rule=30, time_steps=2, field="gf2"
    )
    assert first == second


def test_certificate_verifier_rejects_false_excess_and_tampering() -> None:
    result = search_polynomial_conservation(
        2, 2, 2, rule=30, time_steps=1, field="rational"
    )

    false_excess = copy.deepcopy(result)
    false_excess["certified_trivial_subspace_rank"] -= 1
    false_excess["nontrivial_excess_nullity"] += 1
    false_excess["certificate"]["trivial_basis"].pop()
    assert not verify_search_certificate(false_excess)

    altered_matrix_claim = copy.deepcopy(result)
    altered_matrix_claim["coefficient_matrix_sha256"] = "0" * 64
    assert not verify_search_certificate(altered_matrix_claim)

    altered_kernel = copy.deepcopy(result)
    altered_kernel["certificate"]["kernel_basis"][0].append([2, 1])
    assert not verify_search_certificate(altered_kernel)


def test_deterministic_caps_reject_unbounded_campaigns() -> None:
    with pytest.raises(ValueError, match="input width"):
        polynomial_conservation_matrix(
            MAX_INPUT_WIDTH - 1, 1, 1, rule=30, time_steps=1
        )


def test_campaign_cli_emits_verified_structured_json() -> None:
    command = [
        sys.executable,
        str(
            REPOSITORY_ROOT
            / "experiments/problem2_balance/search_polynomial_conservation.py"
        ),
        "--minimum-width",
        "2",
        "--maximum-width",
        "2",
        "--density-degree",
        "2",
        "--flux-degree",
        "2",
        "--time-steps",
        "1",
        "--field",
        "gf2",
        "--compact",
    ]
    completed = subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stderr == ""
    payload = json.loads(completed.stdout)
    assert payload["status"] == "finite-exhaustive"
    assert payload["summary"]["finite_system_count"] == 1
    assert payload["summary"]["systems_with_excess"] == 0
    assert payload["summary"]["positive_controls_with_excess"] == 1
    assert verify_search_certificate(payload["results"][0])
    assert verify_search_certificate(payload["positive_controls"][0])
