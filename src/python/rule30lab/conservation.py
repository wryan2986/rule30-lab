"""Exact bounded searches for one-dimensional local conservation identities.

For a density ``rho`` on width-``k`` blocks and a flux ``J`` on
width-``k+1`` blocks, this module solves the finite linear system

``rho(F_k(w)) - rho(w[1:-1]) = J(w[:-1]) - J(w[1:])``

for every binary word ``w`` of length ``k+2``.  Summing such an identity over
space telescopes the flux terms.  The search is exact over either the rationals
or GF(2), but it covers only this bounded ansatz and cannot establish that no
other identity or proof method exists.
"""

from __future__ import annotations

import hashlib
import json
import operator
from fractions import Fraction
from typing import Any, Literal


Field = Literal["rational", "gf2"]


def _integer(value: int, *, name: str, minimum: int) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be an integer, not bool")
    try:
        result = operator.index(value)
    except TypeError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if result < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return result


def bits_for(value: int, width: int) -> tuple[int, ...]:
    """Return ``width`` bits in left-to-right, most-significant-first order."""
    checked_width = _integer(width, name="width", minimum=0)
    checked_value = _integer(value, name="value", minimum=0)
    if checked_value >= 1 << checked_width:
        raise ValueError("value does not fit in width bits")
    return tuple(
        (checked_value >> shift) & 1
        for shift in range(checked_width - 1, -1, -1)
    )


def block_value(bits: tuple[int, ...]) -> int:
    """Encode a left-to-right binary block as a nonnegative integer."""
    value = 0
    for index, bit in enumerate(bits):
        if bit not in (0, 1):
            raise ValueError(f"bit at index {index} must be zero or one")
        value = (value << 1) | bit
    return value


def wolfram_local_update(rule: int, left: int, center: int, right: int) -> int:
    """Evaluate an elementary cellular-automaton rule numbered 0 through 255."""
    checked_rule = _integer(rule, name="rule", minimum=0)
    if checked_rule > 255:
        raise ValueError("rule must be at most 255")
    if left not in (0, 1) or center not in (0, 1) or right not in (0, 1):
        raise ValueError("neighborhood values must be zero or one")
    neighborhood = (left << 2) | (center << 1) | right
    return (checked_rule >> neighborhood) & 1


def next_block(input_block: tuple[int, ...], *, rule: int = 30) -> tuple[int, ...]:
    """Map a length-``k+2`` input block to its length-``k`` next-time block."""
    if len(input_block) < 2:
        raise ValueError("input block must contain at least two boundary bits")
    return tuple(
        wolfram_local_update(
            rule,
            input_block[index],
            input_block[index + 1],
            input_block[index + 2],
        )
        for index in range(len(input_block) - 2)
    )


def conservation_matrix(width: int, *, rule: int = 30) -> list[list[int]]:
    """Build the exact integer coefficient matrix for the bounded ansatz."""
    density_width = _integer(width, name="width", minimum=1)
    checked_rule = _integer(rule, name="rule", minimum=0)
    if checked_rule > 255:
        raise ValueError("rule must be at most 255")

    density_count = 1 << density_width
    flux_count = 1 << (density_width + 1)
    unknown_count = density_count + flux_count
    rows: list[list[int]] = []

    for word_value in range(1 << (density_width + 2)):
        word = bits_for(word_value, density_width + 2)
        evolved = next_block(word, rule=checked_rule)
        current = word[1:-1]
        left_flux = word[:-1]
        right_flux = word[1:]

        row = [0] * unknown_count
        row[block_value(evolved)] += 1
        row[block_value(current)] -= 1
        row[density_count + block_value(left_flux)] -= 1
        row[density_count + block_value(right_flux)] += 1
        rows.append(row)
    return rows


def _rational_rank(rows: list[list[int]]) -> int:
    if not rows:
        return 0
    matrix = [[Fraction(value) for value in row] for row in rows]
    row_count = len(matrix)
    column_count = len(matrix[0])
    rank = 0

    for column in range(column_count):
        pivot = next(
            (index for index in range(rank, row_count) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        pivot_value = matrix[rank][column]
        for index in range(rank + 1, row_count):
            if not matrix[index][column]:
                continue
            factor = matrix[index][column] / pivot_value
            for position in range(column, column_count):
                matrix[index][position] -= factor * matrix[rank][position]
        rank += 1
        if rank == row_count:
            break
    return rank


def _gf2_rank(rows: list[list[int]]) -> int:
    basis: dict[int, int] = {}
    for row in rows:
        packed = 0
        for column, value in enumerate(row):
            packed |= (value & 1) << column
        while packed:
            pivot = packed.bit_length() - 1
            if pivot in basis:
                packed ^= basis[pivot]
            else:
                basis[pivot] = packed
                break
    return len(basis)


def matrix_rank(rows: list[list[int]], field: Field) -> int:
    """Return exact rank over the requested field."""
    if field == "rational":
        return _rational_rank(rows)
    if field == "gf2":
        return _gf2_rank(rows)
    raise ValueError("field must be 'rational' or 'gf2'")


def trivial_conservation_vectors(
    width: int, *, rule: int = 30, field: Field = "rational"
) -> list[list[int]]:
    """Return certified constant and spatial-coboundary solution vectors.

    A function ``g`` on width-``k-1`` blocks gives the trivial density
    ``rho(v) = g(v[:-1]) - g(v[1:])``.  Its corresponding flux is
    ``J(u) = g(F_(k-1)(u)) - g(u[1:k])``.  One reference value of ``g`` is
    omitted because adding a constant changes neither density nor flux.
    """
    density_width = _integer(width, name="width", minimum=1)
    matrix = conservation_matrix(density_width, rule=rule)
    unknown_count = len(matrix[0])
    density_count = 1 << density_width
    flux_count = 1 << (density_width + 1)
    vectors: list[list[int]] = []

    constant_density = [0] * unknown_count
    constant_density[:density_count] = [1] * density_count
    vectors.append(constant_density)

    constant_flux = [0] * unknown_count
    constant_flux[density_count:] = [1] * flux_count
    vectors.append(constant_flux)

    coboundary_block_count = 1 << (density_width - 1)
    for selected in range(1, coboundary_block_count):
        vector = [0] * unknown_count
        for value in range(density_count):
            block = bits_for(value, density_width)
            vector[value] = int(block_value(block[:-1]) == selected) - int(
                block_value(block[1:]) == selected
            )
        for value in range(flux_count):
            block = bits_for(value, density_width + 1)
            evolved = next_block(block, rule=rule)
            current_middle = block[1:density_width]
            vector[density_count + value] = int(
                block_value(evolved) == selected
            ) - int(block_value(current_middle) == selected)
        vectors.append(vector)

    if field == "gf2":
        return [[value & 1 for value in vector] for vector in vectors]
    if field != "rational":
        raise ValueError("field must be 'rational' or 'gf2'")
    return vectors


def _annihilates(matrix: list[list[int]], vector: list[int], field: Field) -> bool:
    for row in matrix:
        value = sum(coefficient * item for coefficient, item in zip(row, vector))
        if field == "gf2":
            value &= 1
        if value:
            return False
    return True


def search_local_conservation(
    width: int, *, rule: int = 30, field: Field = "rational"
) -> dict[str, Any]:
    """Solve and classify one finite conservation-law linear system exactly."""
    matrix = conservation_matrix(width, rule=rule)
    rank = matrix_rank(matrix, field)
    unknown_count = len(matrix[0])
    nullity = unknown_count - rank
    trivial = trivial_conservation_vectors(width, rule=rule, field=field)
    if not all(_annihilates(matrix, vector, field) for vector in trivial):
        raise AssertionError("constructed trivial certificate does not solve the system")
    trivial_rank = matrix_rank(trivial, field)
    if trivial_rank > nullity:
        raise AssertionError("trivial certificate rank exceeds nullity")

    canonical_matrix = json.dumps(
        matrix, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return {
        "rule": rule,
        "density_width": width,
        "flux_width": width + 1,
        "field": field,
        "equation_count": len(matrix),
        "unknown_count": unknown_count,
        "rank": rank,
        "nullity": nullity,
        "certified_trivial_subspace_rank": trivial_rank,
        "nontrivial_excess_nullity": nullity - trivial_rank,
        "coefficient_matrix_sha256": hashlib.sha256(canonical_matrix).hexdigest(),
        "status": "finite-exhaustive",
        "interpretation": (
            "Exact solution-space dimensions for this bounded local-density/flux "
            "ansatz only. Zero excess does not rule out identities at larger width, "
            "with another algebra, or outside this form."
        ),
    }
