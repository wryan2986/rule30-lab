#!/usr/bin/env python3
"""Search exact bounded state summaries for Rule 30 sideways evolution.

The leftward evolution of adjacent temporal columns is treated as a
second-order cellular automaton.  If ``A_t`` is the current column and
``B_t`` its right neighbor, one leftward step is

    L_t = A_{t+1} XOR (A_t OR B_t),   (A, B) -> (L, A).

This script performs three deterministic searches:

* de Bruijn/coboundary linear algebra for local GF(2) parity invariants;
* exact closure tests for bounded-window one-bit state summaries; and
* greatest-fixed-point certificates in fixed-period cyclic-column models.

Every cap is explicit.  The cyclic-column model is stronger than an
eventually periodic center boundary: the forced right neighbor generally has
a transient and need not share the center period.  Consequently, even an
infinite-depth certificate in that finite model is not a proof of Rule 30
center nonperiodicity.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from collections.abc import Callable, Iterable, Sequence
from pathlib import Path
from typing import Any


DEFAULT_MAX_DENSITY_WIDTH = 3
DEFAULT_MAX_PHASE_PERIOD = 4
DEFAULT_MAX_AFFINE_WINDOW = 5
DEFAULT_MAX_BOOLEAN_WINDOW = 2
DEFAULT_MAX_IMAGE_WIDTH = 8
DEFAULT_MAX_CYCLIC_PERIOD = 8
DEFAULT_MAX_LINEAR_UNKNOWNS = 4_096
DEFAULT_MAX_LINEAR_EQUATIONS = 16_384
DEFAULT_MAX_SUMMARY_CANDIDATES = 1_000_000
DEFAULT_MAX_IMAGE_STATES = 65_536
DEFAULT_MAX_CYCLIC_STATES = 65_536


class InvariantSearchLimitError(RuntimeError):
    """Raised before an explicitly configured finite-search cap is crossed."""


def _positive_integer(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected an integer") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Search bounded local invariants, state summaries, and cyclic "
            "separating certificates for Rule 30 sideways evolution."
        )
    )
    parser.add_argument(
        "--max-density-width",
        type=_positive_integer,
        default=DEFAULT_MAX_DENSITY_WIDTH,
    )
    parser.add_argument(
        "--max-phase-period",
        type=_positive_integer,
        default=DEFAULT_MAX_PHASE_PERIOD,
    )
    parser.add_argument(
        "--max-affine-window",
        type=_positive_integer,
        default=DEFAULT_MAX_AFFINE_WINDOW,
    )
    parser.add_argument(
        "--max-boolean-window",
        type=_positive_integer,
        default=DEFAULT_MAX_BOOLEAN_WINDOW,
    )
    parser.add_argument(
        "--max-image-width",
        type=_positive_integer,
        default=DEFAULT_MAX_IMAGE_WIDTH,
    )
    parser.add_argument(
        "--max-cyclic-period",
        type=_positive_integer,
        default=DEFAULT_MAX_CYCLIC_PERIOD,
    )
    parser.add_argument(
        "--max-linear-unknowns",
        type=_positive_integer,
        default=DEFAULT_MAX_LINEAR_UNKNOWNS,
    )
    parser.add_argument(
        "--max-linear-equations",
        type=_positive_integer,
        default=DEFAULT_MAX_LINEAR_EQUATIONS,
    )
    parser.add_argument(
        "--max-summary-candidates",
        type=_positive_integer,
        default=DEFAULT_MAX_SUMMARY_CANDIDATES,
    )
    parser.add_argument(
        "--max-cyclic-states",
        type=_positive_integer,
        default=DEFAULT_MAX_CYCLIC_STATES,
    )
    parser.add_argument(
        "--max-image-states",
        type=_positive_integer,
        default=DEFAULT_MAX_IMAGE_STATES,
    )
    return parser


def _word_index(symbols: Sequence[int]) -> int:
    value = 0
    for symbol in symbols:
        if symbol < 0 or symbol >= 4:
            raise ValueError("pair symbols must be in 0..3")
        value = 4 * value + symbol
    return value


def _index_word(index: int, width: int) -> tuple[int, ...]:
    symbols = [0] * width
    for position in range(width - 1, -1, -1):
        symbols[position] = index & 3
        index >>= 2
    return tuple(symbols)


def _rule30_new_symbol(current: int, following: int) -> int:
    """Return ``(L_t, A_t)`` from old symbols ``(A_t,B_t),(A_t+1,B_t+1)``.

    Pair-symbol bit zero is the first/current column and bit one is its right
    neighbor.  The returned symbol uses the same convention for ``(L,A)``.
    """

    a = current & 1
    b = (current >> 1) & 1
    following_a = following & 1
    left = following_a ^ (a | b)
    return left | (a << 1)


def _identity_new_symbol(current: int, following: int) -> int:
    del following
    return current


LocalRule = Callable[[int, int], int]


def _rref(rows: Iterable[int], column_count: int) -> tuple[list[int], list[int]]:
    """Return canonical GF(2) reduced rows and their pivot columns."""

    reduced = [row for row in rows if row]
    pivot_columns: list[int] = []
    pivot_row = 0
    for column in range(column_count):
        selected = next(
            (
                row_index
                for row_index in range(pivot_row, len(reduced))
                if (reduced[row_index] >> column) & 1
            ),
            None,
        )
        if selected is None:
            continue
        reduced[pivot_row], reduced[selected] = (
            reduced[selected],
            reduced[pivot_row],
        )
        for row_index in range(len(reduced)):
            if row_index != pivot_row and (
                (reduced[row_index] >> column) & 1
            ):
                reduced[row_index] ^= reduced[pivot_row]
        pivot_columns.append(column)
        pivot_row += 1
        if pivot_row == len(reduced):
            break
    return reduced[:pivot_row], pivot_columns


def _nullspace(rows: Sequence[int], column_count: int) -> list[int]:
    reduced, pivots = _rref(rows, column_count)
    pivot_set = set(pivots)
    basis: list[int] = []
    for free_column in range(column_count):
        if free_column in pivot_set:
            continue
        vector = 1 << free_column
        for row, pivot in zip(reduced, pivots, strict=True):
            if (row >> free_column) & 1:
                vector |= 1 << pivot
        basis.append(vector)
    return basis


def _canonical_span(vectors: Iterable[int], bit_count: int) -> list[int]:
    reduced, _ = _rref(vectors, bit_count)
    return reduced


def _in_span(vector: int, basis: Sequence[int], bit_count: int) -> bool:
    return len(_canonical_span([*basis, vector], bit_count)) == len(basis)


def _vectors_sha256(vectors: Sequence[int], bit_count: int) -> str:
    width = max(1, (bit_count + 7) // 8)
    digest = hashlib.sha256()
    digest.update(len(vectors).to_bytes(8, "little"))
    digest.update(bit_count.to_bytes(8, "little"))
    for vector in vectors:
        digest.update(vector.to_bytes(width, "little"))
    return digest.hexdigest()


def _matrix_sha256(
    rows: Sequence[int], column_count: int, metadata: dict[str, int | str]
) -> str:
    row_bytes = max(1, (column_count + 7) // 8)
    digest = hashlib.sha256()
    digest.update(
        json.dumps(
            metadata, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode("ascii")
    )
    digest.update(b"\0")
    for row in rows:
        digest.update(row.to_bytes(row_bytes, "little"))
    return digest.hexdigest()


def _trivial_density_basis(phase_period: int, width: int) -> list[int]:
    """Return constants and temporal coboundaries for phase-aware densities."""

    words = 4**width
    vectors: list[int] = []
    for phase in range(phase_period):
        vectors.append(((1 << words) - 1) << (phase * words))

    if width > 1:
        shorter_words = 4 ** (width - 1)
        for phase in range(phase_period):
            previous_phase = (phase - 1) % phase_period
            for short_index in range(shorter_words):
                density = 0
                for word_index in range(words):
                    word = _index_word(word_index, width)
                    if _word_index(word[:-1]) == short_index:
                        density ^= 1 << (phase * words + word_index)
                    if _word_index(word[1:]) == short_index:
                        density ^= 1 << (
                            previous_phase * words + word_index
                        )
                vectors.append(density)
    return _canonical_span(vectors, phase_period * words)


def search_local_parity_conservation(
    phase_period: int,
    width: int,
    *,
    local_rule: LocalRule = _rule30_new_symbol,
    rule_name: str = "rule30-sideways",
    max_unknowns: int = DEFAULT_MAX_LINEAR_UNKNOWNS,
    max_equations: int = DEFAULT_MAX_LINEAR_EQUATIONS,
) -> dict[str, Any]:
    """Solve the exact de Bruijn coboundary equations over GF(2).

    A phase-aware density ``q_i`` is conserved on every cyclic temporal word
    whose length is a multiple of ``phase_period`` if

      q_i(old) + q_i(new) = h_i(prefix) + h_(i+1)(suffix)

    on every length-``width + 1`` pair-symbol block.  The right side telescopes
    on every cycle, so this is an all-cycle certificate rather than a sample
    of finitely many temporal periods.  The density width and phase period are
    nevertheless explicitly bounded search parameters.
    """

    if phase_period <= 0 or width <= 0:
        raise ValueError("phase_period and width must be positive")
    if max_unknowns <= 0 or max_equations <= 0:
        raise ValueError("linear-system caps must be positive")
    if 2 * phase_period > max_unknowns:
        raise InvariantSearchLimitError(
            f"linear system has more than {max_unknowns} unknowns"
        )
    density_words = 1
    for _ in range(width):
        if density_words > max_unknowns // (8 * phase_period):
            raise InvariantSearchLimitError(
                f"linear system has more than {max_unknowns} unknowns"
            )
        density_words *= 4
    unknown_count = 2 * phase_period * density_words
    if density_words > max_equations // (4 * phase_period):
        raise InvariantSearchLimitError(
            f"linear system has more than {max_equations} equations"
        )
    equation_count = phase_period * 4 * density_words
    if unknown_count > max_unknowns:
        raise InvariantSearchLimitError(
            f"linear system has {unknown_count} unknowns, cap is {max_unknowns}"
        )
    if equation_count > max_equations:
        raise InvariantSearchLimitError(
            f"linear system has {equation_count} equations, cap is "
            f"{max_equations}"
        )

    q_unknowns = phase_period * density_words
    rows: list[int] = []
    for phase in range(phase_period):
        next_phase = (phase + 1) % phase_period
        q_offset = phase * density_words
        h_prefix_offset = q_unknowns + phase * density_words
        h_suffix_offset = q_unknowns + next_phase * density_words
        for block_index in range(4 ** (width + 1)):
            block = _index_word(block_index, width + 1)
            old_word = block[:-1]
            new_word = tuple(
                local_rule(block[position], block[position + 1])
                for position in range(width)
            )
            row = 0
            row ^= 1 << (q_offset + _word_index(old_word))
            row ^= 1 << (q_offset + _word_index(new_word))
            row ^= 1 << (h_prefix_offset + _word_index(block[:-1]))
            row ^= 1 << (h_suffix_offset + _word_index(block[1:]))
            rows.append(row)

    reduced, _ = _rref(rows, unknown_count)
    nullspace = _nullspace(rows, unknown_count)
    q_mask = (1 << q_unknowns) - 1
    conserved_q_basis = _canonical_span(
        (vector & q_mask for vector in nullspace), q_unknowns
    )
    trivial_basis = _trivial_density_basis(phase_period, width)
    trivial_not_conserved = sum(
        not _in_span(vector, conserved_q_basis, q_unknowns)
        for vector in trivial_basis
    )
    combined = _canonical_span(
        [*trivial_basis, *conserved_q_basis], q_unknowns
    )
    quotient_dimension = len(combined) - len(trivial_basis)
    nontrivial_representatives = [
        vector
        for vector in conserved_q_basis
        if not _in_span(vector, trivial_basis, q_unknowns)
    ]

    metadata: dict[str, int | str] = {
        "equation_order": "phase_then_base4_block_index",
        "phase_period": phase_period,
        "rule": rule_name,
        "width": width,
    }
    return {
        "phase_period": phase_period,
        "density_width": width,
        "rule": rule_name,
        "pair_symbol_encoding": "low_bit=current_column_A; high_bit=right_neighbor_B",
        "unknown_count": unknown_count,
        "equation_count": equation_count,
        "matrix_rank": len(reduced),
        "solution_dimension_with_potentials": unknown_count - len(reduced),
        "conserved_density_dimension": len(conserved_q_basis),
        "trivial_constant_and_coboundary_dimension": len(trivial_basis),
        "nontrivial_quotient_dimension": quotient_dimension,
        "all_trivial_densities_verified_conserved": trivial_not_conserved == 0,
        "first_nontrivial_density_hex": (
            hex(nontrivial_representatives[0])
            if nontrivial_representatives
            else None
        ),
        "certificate": {
            "equation_matrix_sha256": _matrix_sha256(
                rows, unknown_count, metadata
            ),
            "conserved_density_basis_sha256": _vectors_sha256(
                conserved_q_basis, q_unknowns
            ),
            "trivial_density_basis_sha256": _vectors_sha256(
                trivial_basis, q_unknowns
            ),
            "canonical_encoding": (
                "metadata JSON then N little-endian coefficient bit-vectors; "
                "base-4 temporal words are lexicographic"
            ),
        },
        "depth_independence": (
            "Each solution is conserved for arbitrarily many leftward steps "
            "and every cyclic temporal word of length divisible by the phase "
            "period, because the displayed local difference is an exact de "
            "Bruijn coboundary. The density width and phase period remain "
            "bounded ansatz parameters."
        ),
    }


def _cyclic_density_total(
    density: int, width: int, symbols: Sequence[int]
) -> int:
    total = 0
    length = len(symbols)
    for start in range(length):
        word = tuple(symbols[(start + offset) % length] for offset in range(width))
        total ^= (density >> _word_index(word)) & 1
    return total


def _cyclic_step(symbols: Sequence[int], local_rule: LocalRule) -> tuple[int, ...]:
    return tuple(
        local_rule(symbols[index], symbols[(index + 1) % len(symbols)])
        for index in range(len(symbols))
    )


def find_density_counterexample(
    density: int,
    width: int,
    *,
    local_rule: LocalRule = _rule30_new_symbol,
    max_cycle_length: int = 4,
) -> dict[str, Any] | None:
    """Return the lexicographically first cyclic violation for a density."""

    for length in range(1, max_cycle_length + 1):
        for state_index in range(4**length):
            symbols = _index_word(state_index, length)
            new_symbols = _cyclic_step(symbols, local_rule)
            before = _cyclic_density_total(density, width, symbols)
            after = _cyclic_density_total(density, width, new_symbols)
            if before != after:
                return {
                    "cycle_length": length,
                    "old_pair_symbols": list(symbols),
                    "new_pair_symbols": list(new_symbols),
                    "old_total": before,
                    "new_total": after,
                }
    return None


def _next_window(state: int, width: int, extension_a: int) -> int:
    mask = (1 << width) - 1
    a_word = state & mask
    b_word = (state >> width) & mask
    following_a_word = (a_word >> 1) | (extension_a << (width - 1))
    left_word = following_a_word ^ (a_word | b_word)
    return left_word | (a_word << width)


def _identity_next_window(state: int, width: int, extension_a: int) -> int:
    del extension_a
    return state & ((1 << (2 * width)) - 1)


WindowRule = Callable[[int, int, int], int]


def _summary_transition(
    truth_table: int, width: int, window_rule: WindowRule
) -> tuple[int | None, int | None] | None:
    outputs: list[set[int]] = [set(), set()]
    for state in range(1 << (2 * width)):
        summary = (truth_table >> state) & 1
        for extension in (0, 1):
            next_state = window_rule(state, width, extension)
            outputs[summary].add((truth_table >> next_state) & 1)
    if any(len(values) > 1 for values in outputs):
        return None
    return tuple(next(iter(values)) if values else None for values in outputs)  # type: ignore[return-value]


def search_window_summaries(
    width: int,
    *,
    family: str,
    window_rule: WindowRule = _next_window,
    rule_name: str = "rule30-sideways",
    max_candidates: int = DEFAULT_MAX_SUMMARY_CANDIDATES,
) -> dict[str, Any]:
    """Exhaust one-bit summaries closed despite the unknown trailing input."""

    if width <= 0:
        raise ValueError("width must be positive")
    if max_candidates <= 0:
        raise ValueError("max_candidates must be positive")
    maximum_candidate_exponent = max_candidates.bit_length() - 1
    if family == "affine" and 2 * width + 1 > maximum_candidate_exponent:
        raise InvariantSearchLimitError(
            f"affine width-{width} search exceeds candidates cap {max_candidates}"
        )
    if family == "boolean":
        maximum_state_exponent = maximum_candidate_exponent.bit_length() - 1
        if 2 * width > maximum_state_exponent:
            raise InvariantSearchLimitError(
                f"boolean width-{width} search exceeds candidates cap "
                f"{max_candidates}"
            )
    state_count = 1 << (2 * width)
    if family == "affine":
        candidate_count = 1 << (2 * width + 1)

        def truth_tables() -> Iterable[int]:
            for coefficients in range(candidate_count):
                linear = coefficients & (state_count - 1)
                constant = (coefficients >> (2 * width)) & 1
                truth = 0
                for state in range(state_count):
                    value = constant ^ ((linear & state).bit_count() & 1)
                    truth |= value << state
                yield truth

    elif family == "boolean":
        candidate_count = 1 << state_count

        def truth_tables() -> Iterable[int]:
            return iter(range(candidate_count))

    else:
        raise ValueError("family must be 'affine' or 'boolean'")

    if candidate_count > max_candidates:
        raise InvariantSearchLimitError(
            f"{family} width-{width} search has {candidate_count} candidates, "
            f"cap is {max_candidates}"
        )
    accepted: list[tuple[int, tuple[int | None, int | None]]] = []
    for truth in truth_tables():
        transition = _summary_transition(truth, width, window_rule)
        if transition is not None:
            accepted.append((truth, transition))

    truth_bytes = max(1, (state_count + 7) // 8)
    certificate = hashlib.sha256()
    for truth, transition in accepted:
        certificate.update(truth.to_bytes(truth_bytes, "little"))
        certificate.update(
            bytes(2 if output is None else output for output in transition)
        )
    constants = {0, (1 << state_count) - 1}
    nonconstant = [item for item in accepted if item[0] not in constants]
    persistent_nonconstant = [
        item
        for item in nonconstant
        if item[1][0] is not None
        and item[1][1] is not None
        and item[1][0] != item[1][1]
    ]
    transition_histogram = Counter()
    for _, transition in accepted:
        if transition[0] is None or transition[1] is None:
            label = "one-input-class-unused"
        elif transition == (0, 1):
            label = "identity"
        elif transition == (1, 0):
            label = "toggle"
        else:
            label = f"constant-{transition[0]}"
        transition_histogram[label] += 1
    return {
        "rule": rule_name,
        "family": family,
        "window_width": width,
        "input_state_count": state_count,
        "candidate_count": candidate_count,
        "closed_summary_count": len(accepted),
        "closed_nonconstant_summary_count": len(nonconstant),
        "closed_persistent_nonconstant_summary_count": len(
            persistent_nonconstant
        ),
        "closed_transition_histogram": {
            key: transition_histogram[key] for key in sorted(transition_histogram)
        },
        "first_nonconstant_truth_table_hex": (
            hex(nonconstant[0][0]) if nonconstant else None
        ),
        "accepted_summaries_sha256": certificate.hexdigest(),
        "closure_obligation": (
            "For both unseen trailing bits and every visible pair-window, the "
            "next summary must be one deterministic function of the current "
            "summary alone."
        ),
        "depth_independence": (
            "An accepted summary has a fixed autonomous one-bit update and "
            "can therefore be iterated for arbitrary depth without enlarging "
            "the visible window. Rejection is only within the stated summary "
            "family and width."
        ),
    }


def search_image_subshift(
    max_width: int,
    *,
    max_states: int = DEFAULT_MAX_IMAGE_STATES,
) -> dict[str, Any]:
    """Characterize the exact finite-window image of one sideways step.

    In an output symbol ``(L_t,A_t)``, call the low bit ``L`` and high bit
    ``A``.  Eliminating the old right-neighbor bit shows that adjacent output
    symbols are possible exactly when

        high(current) = 0, or
        low(current) = 1 XOR high(following).

    This is a four-symbol shift of finite type.  Every symbol has exactly
    three incoming allowed edges, hence it has ``4 * 3**(w-1)`` words of width
    ``w``.  Direct image enumeration supplies a bounded independent check.
    """

    if max_width <= 0:
        raise ValueError("max_width must be positive")
    if max_states <= 0:
        raise ValueError("max_states must be positive")
    if 2 * max_width > max_states.bit_length() - 1:
        raise InvariantSearchLimitError(
            f"image width-{max_width} exceeds output states cap {max_states}"
        )
    largest_state_count = 1 << (2 * max_width)
    if largest_state_count > max_states:
        raise InvariantSearchLimitError(
            f"image width-{max_width} has {largest_state_count} output states, "
            f"cap is {max_states}"
        )

    allowed_edges: list[tuple[int, int]] = []
    forbidden_edges: list[tuple[int, int]] = []
    for current in range(4):
        for following in range(4):
            allowed = not ((current >> 1) & 1) or (
                (current & 1) == (1 ^ ((following >> 1) & 1))
            )
            (allowed_edges if allowed else forbidden_edges).append(
                (current, following)
            )
    edge_bytes = bytes(
        component for edge in allowed_edges for component in edge
    )
    per_width: list[dict[str, Any]] = []
    for width in range(1, max_width + 1):
        state_count = 1 << (2 * width)
        direct_image = {
            _next_window(state, width, extension)
            for state in range(state_count)
            for extension in (0, 1)
        }
        locally_admissible = {
            state
            for state in range(state_count)
            if all(
                (
                    ((state >> (width + time)) & 1) == 0
                    or ((state >> time) & 1)
                    == (1 ^ ((state >> (width + time + 1)) & 1))
                )
                for time in range(width - 1)
            )
        }
        if direct_image != locally_admissible:
            raise AssertionError("local image characterization failed")
        expected = 4 * 3 ** (width - 1)
        if len(direct_image) != expected:
            raise AssertionError("image word-count formula failed")
        image_bytes = bytearray(state_count)
        for state in direct_image:
            image_bytes[state] = 1
        per_width.append(
            {
                "width": width,
                "all_pair_windows": state_count,
                "admissible_image_windows": len(direct_image),
                "forbidden_windows": state_count - len(direct_image),
                "formula": "4 * 3**(width - 1)",
                "direct_image_equals_local_constraint_language": True,
                "ordered_image_membership_sha256_u8": hashlib.sha256(
                    image_bytes
                ).hexdigest(),
            }
        )
    return {
        "pair_symbols": {
            str(symbol): {
                "low_bit": symbol & 1,
                "high_bit": (symbol >> 1) & 1,
            }
            for symbol in range(4)
        },
        "allowed_edges": [list(edge) for edge in allowed_edges],
        "forbidden_edges": [list(edge) for edge in forbidden_edges],
        "allowed_edge_count": len(allowed_edges),
        "forbidden_edge_count": len(forbidden_edges),
        "each_symbol_in_degree": [
            sum(following == symbol for _, following in allowed_edges)
            for symbol in range(4)
        ],
        "allowed_edges_sha256_u8_pairs": hashlib.sha256(edge_bytes).hexdigest(),
        "bounded_direct_checks": per_width,
        "depth_independence": (
            "The four forbidden adjacent blocks are excluded from the image "
            "of every sideways step by the local Rule 30 equation, independent "
            "of depth or temporal horizon. Thus every pair of columns after "
            "the first leftward step lies in this same shift of finite type."
        ),
        "separation_limit": (
            "When both reconstructed initial bits are zero, the time-zero pair "
            "symbol has high bit zero, so this image constraint alone gives no "
            "contradiction. It restricts temporal blocks but does not separate "
            "an all-zero initial-left tail from every periodic boundary."
        ),
    }


def lossless_window_obstruction(width: int) -> dict[str, Any]:
    """Exhibit why a complete fixed-width next window is not closed."""

    if width <= 0:
        raise ValueError("width must be positive")
    old_state = 0
    next_zero = _next_window(old_state, width, 0)
    next_one = _next_window(old_state, width, 1)
    differing = next_zero ^ next_one
    return {
        "window_width": width,
        "shared_visible_state": format(old_state, f"0{2 * width}b"),
        "unseen_following_A_values": [0, 1],
        "next_state_with_zero_extension": format(next_zero, f"0{2 * width}b"),
        "next_state_with_one_extension": format(next_one, f"0{2 * width}b"),
        "differing_output_bit_positions": [
            position for position in range(2 * width) if (differing >> position) & 1
        ],
        "interpretation": (
            "The two inputs have the same complete visible window but differ "
            "only at unseen A_t+w. Their next windows differ at L_t+w-1. "
            "Thus a lossless fixed-width window is not a depth-closed state; "
            "one more temporal bit is required at every leftward step."
        ),
    }


def cyclic_pair_transition(state: int, period: int) -> int:
    """Advance an exact pair of cyclic temporal words one step leftward."""

    if period <= 0:
        raise ValueError("period must be positive")
    state_count = 1 << (2 * period)
    if state < 0 or state >= state_count:
        raise ValueError("state does not fit the requested period")
    mask = (1 << period) - 1
    a_word = state & mask
    b_word = (state >> period) & mask
    cyclic_following_a = (a_word >> 1) | ((a_word & 1) << (period - 1))
    left_word = cyclic_following_a ^ (a_word | b_word)
    return left_word | (a_word << period)


def search_cyclic_separating_certificate(
    period: int,
    *,
    max_states: int = DEFAULT_MAX_CYCLIC_STATES,
) -> dict[str, Any]:
    """Find the greatest set whose depth orbit keeps ``A_0 = 0`` forever."""

    if period <= 0:
        raise ValueError("period must be positive")
    if max_states <= 0:
        raise ValueError("max_states must be positive")
    if 2 * period > max_states.bit_length() - 1:
        raise InvariantSearchLimitError(
            f"cyclic period-{period} exceeds state cap {max_states}"
        )
    state_count = 1 << (2 * period)
    if state_count > max_states:
        raise InvariantSearchLimitError(
            f"cyclic period-{period} model has {state_count} states, cap is "
            f"{max_states}"
        )
    successors = [cyclic_pair_transition(state, period) for state in range(state_count)]
    survivor = bytearray(1 if not (state & 1) else 0 for state in range(state_count))
    removal_round = [0] * state_count
    removed_per_round: list[int] = []
    round_number = 1
    while True:
        removed = [
            state
            for state in range(state_count)
            if survivor[state] and not survivor[successors[state]]
        ]
        removed_per_round.append(len(removed))
        if not removed:
            break
        for state in removed:
            survivor[state] = 0
            removal_round[state] = round_number
        round_number += 1

    seed_starts = [state for state in range(state_count) if state & 1]
    forever_safe_seed_successors = sum(survivor[successors[state]] for state in seed_starts)
    witness_depths = bytearray()
    histogram: Counter[int] = Counter()
    max_depth = 0
    for state in seed_starts:
        current = state
        depth = 0
        seen: set[int] = set()
        while True:
            current = successors[current]
            depth += 1
            if current & 1:
                break
            if current in seen or depth > state_count:
                raise AssertionError("safe-orbit certificate contradicts fixed point")
            seen.add(current)
        if depth > 255:
            raise InvariantSearchLimitError(
                "witness depth exceeds one-byte certificate encoding"
            )
        witness_depths.append(depth)
        histogram[depth] += 1
        max_depth = max(max_depth, depth)

    removal_bytes = bytearray()
    for value in removal_round:
        removal_bytes.extend(value.to_bytes(4, "little"))
    survivor_bytes = bytes(survivor)
    return {
        "period": period,
        "state_count": state_count,
        "state_encoding": (
            "low period bits are A_0..A_(p-1); high period bits are "
            "B_0..B_(p-1)"
        ),
        "safe_predicate": "A_0 = 0",
        "greatest_forever_safe_set_size": sum(survivor),
        "greatest_forever_safe_states": [
            state for state, present in enumerate(survivor) if present
        ],
        "removed_per_fixed_point_round_including_final_zero": removed_per_round,
        "center_one_start_count": len(seed_starts),
        "center_one_starts_with_forever_safe_successor": forever_safe_seed_successors,
        "first_nonzero_left_depth_histogram": {
            str(depth): histogram[depth] for depth in sorted(histogram)
        },
        "maximum_first_nonzero_left_depth": max_depth,
        "certificate": {
            "successor_table_sha256_u32le": hashlib.sha256(
                b"".join(successor.to_bytes(4, "little") for successor in successors)
            ).hexdigest(),
            "greatest_safe_bitvector_sha256_u8": hashlib.sha256(
                survivor_bytes
            ).hexdigest(),
            "removal_rounds_sha256_u32le": hashlib.sha256(
                removal_bytes
            ).hexdigest(),
            "ordered_seed_witness_depths_sha256_u8": hashlib.sha256(
                witness_depths
            ).hexdigest(),
        },
        "depth_independence": (
            "The greatest-fixed-point computation certifies the safe predicate "
            "for infinitely many leftward iterations in this exact finite "
            "period-p cyclic-pair model; it is not a finite-horizon orbit test."
        ),
        "scope_obstruction": (
            "The original eventual-period hypothesis constrains only the center "
            "tail. The forced right-neighbor column can have a transient and a "
            "different eventual period, so it need not define one of these "
            "period-p cyclic pair states."
        ),
    }


def build_summary(args: argparse.Namespace) -> dict[str, Any]:
    conservation = []
    for phase_period in range(1, args.max_phase_period + 1):
        for width in range(1, args.max_density_width + 1):
            conservation.append(
                search_local_parity_conservation(
                    phase_period,
                    width,
                    max_unknowns=args.max_linear_unknowns,
                    max_equations=args.max_linear_equations,
                )
            )

    affine_summaries = [
        search_window_summaries(
            width,
            family="affine",
            max_candidates=args.max_summary_candidates,
        )
        for width in range(1, args.max_affine_window + 1)
    ]
    boolean_summaries = [
        search_window_summaries(
            width,
            family="boolean",
            max_candidates=args.max_summary_candidates,
        )
        for width in range(1, args.max_boolean_window + 1)
    ]
    image_subshift = search_image_subshift(
        args.max_image_width, max_states=args.max_image_states
    )
    cyclic_certificates = [
        search_cyclic_separating_certificate(
            period, max_states=args.max_cyclic_states
        )
        for period in range(1, args.max_cyclic_period + 1)
    ]

    identity_conservation = search_local_parity_conservation(
        1,
        1,
        local_rule=_identity_new_symbol,
        rule_name="identity-positive-control",
        max_unknowns=args.max_linear_unknowns,
        max_equations=args.max_linear_equations,
    )
    identity_summary = search_window_summaries(
        1,
        family="boolean",
        window_rule=_identity_next_window,
        rule_name="identity-positive-control",
        max_candidates=args.max_summary_candidates,
    )
    density_a_width_one = 0
    for symbol in range(4):
        density_a_width_one |= (symbol & 1) << symbol
    nonconserved_control = find_density_counterexample(
        density_a_width_one, 1
    )
    if identity_conservation["nontrivial_quotient_dimension"] <= 0:
        raise AssertionError("identity conservation positive control failed")
    if identity_summary["closed_nonconstant_summary_count"] <= 0:
        raise AssertionError("identity summary positive control failed")
    if nonconserved_control is None:
        raise AssertionError("known nonconserved density negative control failed")

    script_path = Path(__file__).resolve()
    no_local_invariants = all(
        result["nontrivial_quotient_dimension"] == 0 for result in conservation
    )
    no_persistent_closed_summaries = all(
        result["closed_persistent_nonconstant_summary_count"] == 0
        for result in [*affine_summaries, *boolean_summaries]
    )
    cyclic_separation = all(
        result["center_one_starts_with_forever_safe_successor"] == 0
        and result["greatest_forever_safe_states"] == [0]
        for result in cyclic_certificates
    )
    return {
        "schema_version": 1,
        "experiment_id": "problem1-sideways-invariant-search-v1",
        "question": "problem1",
        "hypothesis": (
            "A bounded, mathematically interpretable summary may be closed "
            "under arbitrary-depth sideways evolution and separate nonzero "
            "periodic traces from an all-zero reconstructed initial-left tail."
        ),
        "backend": "python-exact-gf2-and-finite-state",
        "implementation": {
            "path": "experiments/problem1_nonperiodicity/search_sideways_invariants.py",
            "sha256": hashlib.sha256(script_path.read_bytes()).hexdigest(),
        },
        "parameters": {
            "max_density_width": args.max_density_width,
            "max_phase_period": args.max_phase_period,
            "max_affine_window": args.max_affine_window,
            "max_boolean_window": args.max_boolean_window,
            "max_image_width": args.max_image_width,
            "max_cyclic_period": args.max_cyclic_period,
            "resource_limits": {
                "max_linear_unknowns_per_system": args.max_linear_unknowns,
                "max_linear_equations_per_system": args.max_linear_equations,
                "max_summary_candidates_per_search": args.max_summary_candidates,
                "max_image_states_per_width": args.max_image_states,
                "max_cyclic_states_per_period": args.max_cyclic_states,
            },
        },
        "local_parity_conservation_search": {
            "status": "finite-exhaustive",
            "systems": conservation,
            "all_tested_solutions_trivial": no_local_invariants,
            "meaning_of_trivial": (
                "phase constants or temporal coboundaries whose cyclic sum is "
                "state-independent or identically zero"
            ),
        },
        "bounded_window_summary_search": {
            "status": "finite-exhaustive",
            "affine": affine_summaries,
            "boolean": boolean_summaries,
            "all_tested_closed_summaries_lose_their_distinction_after_one_step": (
                no_persistent_closed_summaries
            ),
            "image_subshift": image_subshift,
            "lossless_window_obstructions": [
                lossless_window_obstruction(width)
                for width in range(1, max(args.max_affine_window, args.max_boolean_window) + 1)
            ],
        },
        "cyclic_pair_cycle_separation": {
            "status": "finite-exhaustive",
            "periods": cyclic_certificates,
            "all_tested_periods_separated_at_infinite_depth_in_model": cyclic_separation,
        },
        "controls": {
            "identity_conservation": identity_conservation,
            "identity_boolean_summary": identity_summary,
            "known_nonconserved_density_A_width_one": nonconserved_control,
            "controls_passed": True,
        },
        "status": "finite-exhaustive",
        "proof_scope": (
            "Exact solution of every stated bounded GF(2) ansatz, exact "
            "enumeration of every stated one-bit summary family, and exact "
            "greatest-fixed-point analysis of all pair states through the "
            "stated cyclic period. Coboundary and fixed-point certificates "
            "are depth-independent only inside their explicitly defined models."
        ),
        "result_summary": {
            "nontrivial_tested_local_parity_invariant_found": not no_local_invariants,
            "persistent_nonconstant_tested_closed_window_summary_found": (
                not no_persistent_closed_summaries
            ),
            "nonconstant_one_step_image_predicates_found": any(
                result["closed_nonconstant_summary_count"] > 0
                for result in [*affine_summaries, *boolean_summaries]
            ),
            "cyclic_pair_model_counterexample_found": not cyclic_separation,
            "strongest_obstruction": (
                "A complete width-w temporal window is not closed: the next "
                "window depends on unseen A_(t+w). The exact one-bit searches "
                "found no persistent nonconstant quotient that removes this "
                "dependence within the tested affine/Boolean families."
            ),
            "strongest_positive_lead": (
                "The exact four-edge forbidden-block subshift applies after "
                "every sideways step, and every cyclic pair period tested has "
                "only the all-zero state in its forever-safe kernel. Bridging "
                "the right-neighbor transient to these structures is missing."
            ),
        },
        "interpretation": (
            "The exact image subshift and cyclic-pair certificates are genuine "
            "bounded or conditional structure, while the tested local parity "
            "and persistent one-bit summary families yielded no separating "
            "invariant. None bridges eventual center periodicity to the required "
            "right-neighbor behavior."
        ),
        "limitations": [
            "bounded density widths do not exclude wider or nonlocal invariants",
            "bounded phase periods do not exclude more elaborate phase summaries",
            "one-bit affine and small Boolean summaries do not exhaust finite quotients",
            "cyclic-pair certificates assume both adjacent columns are exactly cyclic",
            "an eventually periodic center does not force its right neighbor to share that cycle from time zero",
            "none of these computations proves Rule 30 center nonperiodicity",
        ],
    }


def main() -> int:
    args = _parser().parse_args()
    summary = build_summary(args)
    print(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
