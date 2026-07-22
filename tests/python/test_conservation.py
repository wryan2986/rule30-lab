from __future__ import annotations

import itertools

import pytest

from rule30lab.conservation import (
    bits_for,
    block_value,
    conservation_matrix,
    matrix_rank,
    next_block,
    search_local_conservation,
    trivial_conservation_vectors,
    wolfram_local_update,
)


def test_rule_30_local_map_and_block_encoding() -> None:
    expected = [0, 1, 1, 1, 1, 0, 0, 0]
    for neighborhood in range(8):
        left, center, right = bits_for(neighborhood, 3)
        assert wolfram_local_update(30, left, center, right) == expected[neighborhood]
    for width in range(6):
        for value in range(1 << width):
            assert block_value(bits_for(value, width)) == value
    with pytest.raises(ValueError, match="does not fit"):
        bits_for(4, 2)


def test_next_block_matches_direct_sliding_oracle() -> None:
    for length in range(2, 8):
        for word in itertools.product((0, 1), repeat=length):
            assert next_block(word, rule=30) == tuple(
                left ^ (center | right)
                for left, center, right in zip(word, word[1:], word[2:])
            )


def test_conservation_rows_match_the_stated_identity() -> None:
    width = 2
    density_count = 1 << width
    rho = [3, -2, 5, 7]
    flux = [11, 13, -1, 2, 17, 19, 23, 29]
    values = rho + flux
    matrix = conservation_matrix(width, rule=30)

    for word_value, row in enumerate(matrix):
        word = bits_for(word_value, width + 2)
        direct = (
            rho[block_value(next_block(word))]
            - rho[block_value(word[1:-1])]
            - flux[block_value(word[:-1])]
            + flux[block_value(word[1:])]
        )
        assert sum(coefficient * value for coefficient, value in zip(row, values)) == direct
        assert len(row) == density_count + len(flux)


@pytest.mark.parametrize("field", ["rational", "gf2"])
def test_constructed_trivial_vectors_are_independent_solutions(field: str) -> None:
    for width in range(1, 5):
        matrix = conservation_matrix(width, rule=30)
        vectors = trivial_conservation_vectors(width, rule=30, field=field)
        for vector in vectors:
            for row in matrix:
                value = sum(a * b for a, b in zip(row, vector))
                assert value == 0 if field == "rational" else value % 2 == 0
        assert matrix_rank(vectors, field) == (1 << (width - 1)) + 1


def test_search_detects_identity_rule_density_but_not_rule30_at_width_one() -> None:
    for field in ("rational", "gf2"):
        rule30 = search_local_conservation(1, rule=30, field=field)
        identity = search_local_conservation(1, rule=204, field=field)
        assert rule30["nontrivial_excess_nullity"] == 0
        assert identity["nontrivial_excess_nullity"] >= 1
        assert rule30["status"] == "finite-exhaustive"
        assert "does not rule out" in rule30["interpretation"]
