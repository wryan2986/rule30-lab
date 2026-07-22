"""Exact bounded polynomial searches for local conservation identities.

The unknown density and flux are multilinear polynomials in Boolean cell
variables.  For a density on ``k`` cells, a time displacement ``tau``, and a
flux on ``k + 2*tau - 1`` cells, the finite system is

``rho(F^tau(w)) - rho(w[tau:tau+k]) = J(w[:-1]) - J(w[1:])``.

It is imposed on every binary word ``w`` of length ``k + 2*tau``.  The
coefficient search is linear even though the observables are nonlinear in the
cell values.  All ranks and nullspaces are computed exactly over either the
rationals or GF(2).

This is a deliberately bounded search.  In particular, a zero quotient
dimension is not evidence of global nonexistence outside the reported widths,
degrees, time displacement, and coefficient field.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import operator
from fractions import Fraction
from typing import Any, Iterable, Literal, Sequence

from rule30lab.conservation import bits_for, block_value, wolfram_local_update


Field = Literal["rational", "gf2"]
Scalar = int | Fraction

MAX_INPUT_WIDTH = 12
MAX_UNKNOWN_COUNT = 512
MAX_COBBOUNDARY_GENERATORS = 512


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


def _checked_field(field: str) -> Field:
    if field not in ("rational", "gf2"):
        raise ValueError("field must be 'rational' or 'gf2'")
    return field


def monomial_supports(width: int, maximum_degree: int) -> tuple[tuple[int, ...], ...]:
    """Return the canonical square-free monomial basis through a given degree."""
    checked_width = _integer(width, name="width", minimum=0)
    checked_degree = _integer(maximum_degree, name="maximum_degree", minimum=0)
    degree = min(checked_width, checked_degree)
    return tuple(
        support
        for size in range(degree + 1)
        for support in itertools.combinations(range(checked_width), size)
    )


def evaluate_monomial(bits: Sequence[int], support: Sequence[int]) -> int:
    """Evaluate a square-free monomial on one Boolean block."""
    value = 1
    previous = -1
    for position in support:
        checked = _integer(position, name="support position", minimum=0)
        if checked <= previous:
            raise ValueError("support positions must be strictly increasing")
        if checked >= len(bits):
            raise ValueError("support position is outside the block")
        bit = bits[checked]
        if bit not in (0, 1):
            raise ValueError("block values must be zero or one")
        value &= bit
        previous = checked
    return value


def evolve_block(
    input_block: Sequence[int], *, rule: int = 30, time_steps: int = 1
) -> tuple[int, ...]:
    """Evolve a finite block inward for exactly ``time_steps`` updates."""
    steps = _integer(time_steps, name="time_steps", minimum=1)
    current = tuple(input_block)
    if len(current) < 2 * steps:
        raise ValueError("input block is too short for the requested time steps")
    for index, bit in enumerate(current):
        if bit not in (0, 1):
            raise ValueError(f"input bit at index {index} must be zero or one")
    for _ in range(steps):
        current = tuple(
            wolfram_local_update(rule, left, center, right)
            for left, center, right in zip(current, current[1:], current[2:])
        )
    return current


def polynomial_conservation_matrix(
    density_width: int,
    density_degree: int,
    flux_degree: int,
    *,
    rule: int = 30,
    time_steps: int = 1,
) -> tuple[list[list[int]], tuple[tuple[int, ...], ...], tuple[tuple[int, ...], ...]]:
    """Build the complete integer matrix for one bounded polynomial ansatz."""
    width = _integer(density_width, name="density_width", minimum=1)
    steps = _integer(time_steps, name="time_steps", minimum=1)
    checked_rule = _integer(rule, name="rule", minimum=0)
    if checked_rule > 255:
        raise ValueError("rule must be at most 255")
    input_width = width + 2 * steps
    if input_width > MAX_INPUT_WIDTH:
        raise ValueError(
            f"input width {input_width} exceeds deterministic cap {MAX_INPUT_WIDTH}"
        )
    flux_width = input_width - 1
    density_basis = monomial_supports(width, density_degree)
    flux_basis = monomial_supports(flux_width, flux_degree)
    unknown_count = len(density_basis) + len(flux_basis)
    if unknown_count > MAX_UNKNOWN_COUNT:
        raise ValueError(
            f"unknown count {unknown_count} exceeds deterministic cap "
            f"{MAX_UNKNOWN_COUNT}"
        )
    generator_count = 1 << max(0, width - 1)
    if generator_count > MAX_COBBOUNDARY_GENERATORS:
        raise ValueError(
            f"coboundary generator count {generator_count} exceeds deterministic "
            f"cap {MAX_COBBOUNDARY_GENERATORS}"
        )

    rows: list[list[int]] = []
    for word_value in range(1 << input_width):
        word = bits_for(word_value, input_width)
        evolved = evolve_block(word, rule=checked_rule, time_steps=steps)
        current = word[steps : steps + width]
        left_flux = word[:-1]
        right_flux = word[1:]
        row = [
            evaluate_monomial(evolved, support)
            - evaluate_monomial(current, support)
            for support in density_basis
        ]
        row.extend(
            -evaluate_monomial(left_flux, support)
            + evaluate_monomial(right_flux, support)
            for support in flux_basis
        )
        rows.append(row)
    return rows, density_basis, flux_basis


def _canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def _field_value(value: Scalar, field: Field) -> Scalar:
    if field == "gf2":
        if isinstance(value, Fraction) and value.denominator != 1:
            raise ValueError("nonintegral values cannot be reduced modulo two")
        return int(value) & 1
    return value if isinstance(value, Fraction) else Fraction(value)


def _rref(
    rows: Sequence[Sequence[Scalar]], column_count: int, field: Field
) -> tuple[list[list[Scalar]], list[int]]:
    """Compute deterministic exact reduced row-echelon form."""
    checked_field = _checked_field(field)
    canonical_rows = {
        tuple(_field_value(value, checked_field) for value in row)
        for row in rows
    }
    if any(len(row) != column_count for row in canonical_rows):
        raise ValueError("matrix rows do not have the declared column count")
    zero: Scalar = 0 if checked_field == "gf2" else Fraction(0)
    matrix = [list(row) for row in sorted(canonical_rows) if any(row)]
    pivot_columns: list[int] = []
    pivot_row = 0

    for column in range(column_count):
        selected = next(
            (index for index in range(pivot_row, len(matrix)) if matrix[index][column]),
            None,
        )
        if selected is None:
            continue
        matrix[pivot_row], matrix[selected] = matrix[selected], matrix[pivot_row]
        if checked_field == "rational":
            pivot = matrix[pivot_row][column]
            matrix[pivot_row] = [value / pivot for value in matrix[pivot_row]]
        for index in range(len(matrix)):
            if index == pivot_row or not matrix[index][column]:
                continue
            factor = matrix[index][column]
            if checked_field == "gf2":
                matrix[index] = [
                    left ^ right
                    for left, right in zip(matrix[index], matrix[pivot_row])
                ]
            else:
                matrix[index] = [
                    left - factor * right
                    for left, right in zip(matrix[index], matrix[pivot_row])
                ]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(matrix):
            break
    return [row for row in matrix if any(value != zero for value in row)], pivot_columns


def _nullspace_basis(
    rows: Sequence[Sequence[Scalar]], column_count: int, field: Field
) -> tuple[list[list[Scalar]], list[list[Scalar]], list[int], list[int]]:
    rref, pivots = _rref(rows, column_count, field)
    pivot_set = set(pivots)
    free_columns = [column for column in range(column_count) if column not in pivot_set]
    zero: Scalar = 0 if field == "gf2" else Fraction(0)
    one: Scalar = 1 if field == "gf2" else Fraction(1)
    basis: list[list[Scalar]] = []
    for free in free_columns:
        vector = [zero] * column_count
        vector[free] = one
        for row, pivot in zip(rref, pivots):
            vector[pivot] = row[free] if field == "gf2" else -row[free]
        basis.append(vector)
    return basis, rref, pivots, free_columns


def _rank(rows: Sequence[Sequence[Scalar]], column_count: int, field: Field) -> int:
    return len(_rref(rows, column_count, field)[1])


def _annihilates(
    matrix: Sequence[Sequence[int]], vector: Sequence[Scalar], field: Field
) -> bool:
    for row in matrix:
        value = sum(
            (_field_value(coefficient, field) * item for coefficient, item in zip(row, vector)),
            start=0,
        )
        if field == "gf2":
            value &= 1
        if value:
            return False
    return True


def _truth_to_coefficients(values: Sequence[int], width: int, field: Field) -> list[Scalar]:
    """Convert a Boolean truth table to its unique multilinear coefficients."""
    if len(values) != 1 << width:
        raise ValueError("truth-table length does not match width")
    coefficients = [_field_value(value, field) for value in values]
    for bit in range(width):
        flag = 1 << bit
        for mask in range(1 << width):
            if mask & flag:
                if field == "gf2":
                    coefficients[mask] ^= coefficients[mask ^ flag]
                else:
                    coefficients[mask] -= coefficients[mask ^ flag]
    return coefficients


def _support_mask(support: Sequence[int], width: int) -> int:
    mask = 0
    for position in support:
        mask |= 1 << (width - 1 - position)
    return mask


def _combine_columns(
    columns: Sequence[Sequence[Scalar]], weights: Sequence[Scalar], field: Field
) -> list[Scalar]:
    if len(columns) != len(weights):
        raise ValueError("column and weight counts differ")
    if not columns:
        return []
    output: list[Scalar] = [0] * len(columns[0])
    for column, weight in zip(columns, weights):
        for index, value in enumerate(column):
            output[index] += weight * value
            if field == "gf2":
                output[index] &= 1
    return output


def _independent_subset(
    vectors: Iterable[Sequence[Scalar]], column_count: int, field: Field
) -> list[list[Scalar]]:
    selected: list[list[Scalar]] = []
    rank = 0
    for candidate in vectors:
        vector = list(candidate)
        trial_rank = _rank([*selected, vector], column_count, field)
        if trial_rank > rank:
            selected.append(vector)
            rank = trial_rank
    return selected


def _coboundary_basis(
    *,
    density_width: int,
    density_basis: Sequence[Sequence[int]],
    flux_basis: Sequence[Sequence[int]],
    rule: int,
    time_steps: int,
    field: Field,
) -> list[list[Scalar]]:
    """Return the full representable spatial-coboundary intersection.

    ``g`` ranges over every function on width-``density_width-1`` blocks.
    Linear constraints remove combinations whose induced density or flux has
    monomials outside the selected bases.  Thus the returned quotient does not
    mistake an omitted high-degree representation of a coboundary for excess.
    """
    width = density_width
    g_width = width - 1
    flux_width = width + 2 * time_steps - 1
    density_selected = {_support_mask(support, width) for support in density_basis}
    flux_selected = {_support_mask(support, flux_width) for support in flux_basis}
    selected_masks = [
        *(("rho", _support_mask(support, width)) for support in density_basis),
        *(
            ("flux", _support_mask(support, flux_width))
            for support in flux_basis
        ),
    ]
    excluded_masks = [
        *(
            ("rho", mask)
            for mask in range(1 << width)
            if mask not in density_selected
        ),
        *(
            ("flux", mask)
            for mask in range(1 << flux_width)
            if mask not in flux_selected
        ),
    ]
    selected_columns: list[list[Scalar]] = []
    excluded_columns: list[list[Scalar]] = []

    for g_value in range(1 << g_width):
        rho_truth: list[int] = []
        for value in range(1 << width):
            block = bits_for(value, width)
            rho_truth.append(
                int(block_value(block[:-1]) == g_value)
                - int(block_value(block[1:]) == g_value)
            )
        flux_truth: list[int] = []
        for value in range(1 << flux_width):
            block = bits_for(value, flux_width)
            evolved = evolve_block(block, rule=rule, time_steps=time_steps)
            current = block[time_steps : time_steps + g_width]
            flux_truth.append(
                int(block_value(evolved) == g_value)
                - int(block_value(current) == g_value)
            )
        rho_coefficients = _truth_to_coefficients(rho_truth, width, field)
        flux_coefficients = _truth_to_coefficients(flux_truth, flux_width, field)
        tables = {"rho": rho_coefficients, "flux": flux_coefficients}
        selected_columns.append([tables[kind][mask] for kind, mask in selected_masks])
        excluded_columns.append([tables[kind][mask] for kind, mask in excluded_masks])

    excluded_rows = [list(row) for row in zip(*excluded_columns)]
    admissible_weights, _, _, _ = _nullspace_basis(
        excluded_rows, len(selected_columns), field
    )
    candidates = [
        _combine_columns(selected_columns, weights, field)
        for weights in admissible_weights
    ]
    return _independent_subset(candidates, len(selected_masks), field)


def _scalar_json(value: Scalar) -> int | str:
    fraction = value if isinstance(value, Fraction) else Fraction(value)
    if fraction.denominator == 1:
        return fraction.numerator
    return f"{fraction.numerator}/{fraction.denominator}"


def _json_scalar(value: object, field: Field) -> Scalar:
    if isinstance(value, bool):
        raise ValueError("Boolean is not a certificate scalar")
    if isinstance(value, int):
        return value & 1 if field == "gf2" else Fraction(value)
    if field == "rational" and isinstance(value, str):
        try:
            return Fraction(value)
        except (ValueError, ZeroDivisionError) as exc:
            raise ValueError("invalid rational certificate scalar") from exc
    raise ValueError("invalid certificate scalar")


def _sparse_vector(vector: Sequence[Scalar]) -> list[list[int | str]]:
    return [
        [index, _scalar_json(value)]
        for index, value in enumerate(vector)
        if value
    ]


def _dense_vector(
    sparse: object, *, length: int, field: Field
) -> list[Scalar]:
    if not isinstance(sparse, list):
        raise ValueError("sparse vector must be a list")
    output: list[Scalar] = [0] * length
    previous = -1
    for item in sparse:
        if not isinstance(item, list) or len(item) != 2:
            raise ValueError("invalid sparse vector item")
        index = item[0]
        if isinstance(index, bool) or not isinstance(index, int):
            raise ValueError("invalid sparse vector index")
        if index <= previous or index >= length:
            raise ValueError("sparse vector indices must increase and fit")
        value = _json_scalar(item[1], field)
        if not value:
            raise ValueError("sparse vectors must omit zero entries")
        output[index] = value
        previous = index
    return output


def _serialized_basis(vectors: Sequence[Sequence[Scalar]]) -> list[list[list[int | str]]]:
    return [_sparse_vector(vector) for vector in vectors]


def _feature_labels(kind: str, supports: Sequence[Sequence[int]]) -> list[str]:
    return [
        f"{kind}:1" if not support else f"{kind}:" + "*".join(f"x{i}" for i in support)
        for support in supports
    ]


def search_polynomial_conservation(
    density_width: int,
    density_degree: int,
    flux_degree: int,
    *,
    rule: int = 30,
    time_steps: int = 1,
    field: Field = "rational",
) -> dict[str, Any]:
    """Solve and quotient one finite polynomial conservation system exactly."""
    checked_field = _checked_field(field)
    matrix, density_basis, flux_basis = polynomial_conservation_matrix(
        density_width,
        density_degree,
        flux_degree,
        rule=rule,
        time_steps=time_steps,
    )
    unknown_count = len(matrix[0])
    kernel, rref, pivots, free_columns = _nullspace_basis(
        matrix, unknown_count, checked_field
    )

    constant_density: list[Scalar] = [0] * unknown_count
    constant_density[0] = 1
    constant_flux: list[Scalar] = [0] * unknown_count
    constant_flux[len(density_basis)] = 1
    coboundaries = _coboundary_basis(
        density_width=density_width,
        density_basis=density_basis,
        flux_basis=flux_basis,
        rule=rule,
        time_steps=time_steps,
        field=checked_field,
    )
    trivial = _independent_subset(
        [constant_density, constant_flux, *coboundaries],
        unknown_count,
        checked_field,
    )
    if not all(_annihilates(matrix, vector, checked_field) for vector in trivial):
        raise AssertionError("constructed trivial quotient certificate is not in kernel")

    combined = list(trivial)
    excess: list[list[Scalar]] = []
    combined_rank = len(trivial)
    for candidate in kernel:
        trial_rank = _rank([*combined, candidate], unknown_count, checked_field)
        if trial_rank > combined_rank:
            excess.append(candidate)
            combined.append(candidate)
            combined_rank = trial_rank
    nullity = len(kernel)
    if combined_rank != nullity:
        raise AssertionError("trivial and excess certificates do not span the kernel")

    serialized_kernel = _serialized_basis(kernel)
    serialized_trivial = _serialized_basis(trivial)
    serialized_excess = _serialized_basis(excess)
    serialized_rref = _serialized_basis(rref)
    labels = _feature_labels("rho", density_basis) + _feature_labels(
        "flux", flux_basis
    )
    result: dict[str, Any] = {
        "schema_version": 1,
        "rule": rule,
        "field": checked_field,
        "density_width": density_width,
        "density_degree": min(density_width, density_degree),
        "time_steps": time_steps,
        "input_width": density_width + 2 * time_steps,
        "flux_width": density_width + 2 * time_steps - 1,
        "flux_degree": min(density_width + 2 * time_steps - 1, flux_degree),
        "equation_count": len(matrix),
        "distinct_nonzero_equation_count": len({tuple(row) for row in matrix if any(row)}),
        "unknown_count": unknown_count,
        "rank": len(pivots),
        "nullity": nullity,
        "certified_trivial_subspace_rank": len(trivial),
        "certified_spatial_coboundary_rank": len(coboundaries),
        "nontrivial_excess_nullity": len(excess),
        "feature_labels": labels,
        "coefficient_matrix_sha256": _canonical_json_sha256(matrix),
        "certificate": {
            "pivot_columns": pivots,
            "free_columns": free_columns,
            "rref_rows": serialized_rref,
            "kernel_basis": serialized_kernel,
            "trivial_basis": serialized_trivial,
            "excess_basis": serialized_excess,
            "rref_sha256": _canonical_json_sha256(serialized_rref),
            "kernel_basis_sha256": _canonical_json_sha256(serialized_kernel),
            "trivial_basis_sha256": _canonical_json_sha256(serialized_trivial),
            "excess_basis_sha256": _canonical_json_sha256(serialized_excess),
        },
        "caps": {
            "maximum_input_width": MAX_INPUT_WIDTH,
            "maximum_unknown_count": MAX_UNKNOWN_COUNT,
            "maximum_coboundary_generators": MAX_COBBOUNDARY_GENERATORS,
        },
        "status": "finite-exhaustive",
        "interpretation": (
            "Exact quotient dimension for this bounded multilinear density/flux "
            "system only. The quotient removes constant gauges and the full "
            "representable spatial-coboundary intersection."
        ),
        "limitations": [
            "width, degree, time displacement, and coefficient field are bounded",
            "zero excess does not imply global nonexistence",
            "a conserved spatial sum would not by itself prove center-column balance",
        ],
    }
    if not verify_search_certificate(result):
        raise AssertionError("self-verification of search certificate failed")
    return result


def verify_search_certificate(result: dict[str, Any]) -> bool:
    """Rebuild a search and independently verify all exposed certificates."""
    try:
        field = _checked_field(result["field"])
        matrix, density_basis, flux_basis = polynomial_conservation_matrix(
            result["density_width"],
            result["density_degree"],
            result["flux_degree"],
            rule=result["rule"],
            time_steps=result["time_steps"],
        )
        unknown_count = len(matrix[0])
        normalized_density_degree = min(
            result["density_width"], result["density_degree"]
        )
        normalized_flux_degree = min(
            result["density_width"] + 2 * result["time_steps"] - 1,
            result["flux_degree"],
        )
        if result["density_degree"] != normalized_density_degree:
            return False
        if result["flux_degree"] != normalized_flux_degree:
            return False
        if result["input_width"] != result["density_width"] + 2 * result["time_steps"]:
            return False
        if result["flux_width"] != result["input_width"] - 1:
            return False
        if result["feature_labels"] != (
            _feature_labels("rho", density_basis) + _feature_labels("flux", flux_basis)
        ):
            return False
        if result["equation_count"] != len(matrix):
            return False
        if result["distinct_nonzero_equation_count"] != len(
            {tuple(row) for row in matrix if any(row)}
        ):
            return False
        if result["unknown_count"] != unknown_count:
            return False
        if result["coefficient_matrix_sha256"] != _canonical_json_sha256(matrix):
            return False
        if result["caps"] != {
            "maximum_input_width": MAX_INPUT_WIDTH,
            "maximum_unknown_count": MAX_UNKNOWN_COUNT,
            "maximum_coboundary_generators": MAX_COBBOUNDARY_GENERATORS,
        }:
            return False
        certificate = result["certificate"]
        rref = [
            _dense_vector(vector, length=unknown_count, field=field)
            for vector in certificate["rref_rows"]
        ]
        kernel = [
            _dense_vector(vector, length=unknown_count, field=field)
            for vector in certificate["kernel_basis"]
        ]
        trivial = [
            _dense_vector(vector, length=unknown_count, field=field)
            for vector in certificate["trivial_basis"]
        ]
        excess = [
            _dense_vector(vector, length=unknown_count, field=field)
            for vector in certificate["excess_basis"]
        ]
        recomputed_rref, pivots = _rref(matrix, unknown_count, field)
        free_columns = [
            column for column in range(unknown_count) if column not in set(pivots)
        ]
        if rref != recomputed_rref:
            return False
        if certificate["pivot_columns"] != pivots:
            return False
        if certificate["free_columns"] != free_columns:
            return False
        if result["rank"] != len(pivots):
            return False
        if (
            result["nullity"] != unknown_count - len(pivots)
            or len(kernel) != result["nullity"]
        ):
            return False
        if _rank(kernel, unknown_count, field) != len(kernel):
            return False
        if not all(_annihilates(matrix, vector, field) for vector in kernel):
            return False
        if len(trivial) != result["certified_trivial_subspace_rank"]:
            return False
        if _rank(trivial, unknown_count, field) != len(trivial):
            return False
        if not all(_annihilates(matrix, vector, field) for vector in trivial):
            return False
        constant_density: list[Scalar] = [0] * unknown_count
        constant_density[0] = 1
        constant_flux: list[Scalar] = [0] * unknown_count
        constant_flux[len(density_basis)] = 1
        recomputed_coboundaries = _coboundary_basis(
            density_width=result["density_width"],
            density_basis=density_basis,
            flux_basis=flux_basis,
            rule=result["rule"],
            time_steps=result["time_steps"],
            field=field,
        )
        recomputed_trivial = _independent_subset(
            [constant_density, constant_flux, *recomputed_coboundaries],
            unknown_count,
            field,
        )
        if result["certified_spatial_coboundary_rank"] != len(
            recomputed_coboundaries
        ):
            return False
        if trivial != recomputed_trivial:
            return False
        if len(excess) != result["nontrivial_excess_nullity"]:
            return False
        if _rank([*trivial, *excess], unknown_count, field) != len(kernel):
            return False
        recomputed_combined = list(recomputed_trivial)
        recomputed_excess: list[list[Scalar]] = []
        combined_rank = len(recomputed_combined)
        for candidate in kernel:
            trial_rank = _rank(
                [*recomputed_combined, candidate], unknown_count, field
            )
            if trial_rank > combined_rank:
                recomputed_excess.append(candidate)
                recomputed_combined.append(candidate)
                combined_rank = trial_rank
        if excess != recomputed_excess:
            return False
        serialized = {
            "rref": certificate["rref_rows"],
            "kernel": certificate["kernel_basis"],
            "trivial": certificate["trivial_basis"],
            "excess": certificate["excess_basis"],
        }
        for name, value in serialized.items():
            hash_key = (
                f"{name}_basis_sha256" if name != "rref" else "rref_sha256"
            )
            if certificate[hash_key] != _canonical_json_sha256(value):
                return False
        return result["status"] == "finite-exhaustive"
    except (
        AttributeError,
        IndexError,
        KeyError,
        OverflowError,
        TypeError,
        UnicodeError,
        ValueError,
        ZeroDivisionError,
    ):
        return False
