"""Finite quotients of the Rule 30 right-edge diagonal map.

For a right-edge state ``S``, write

    T(S) = S XOR ((S << 1) OR (S << 2)).

The diagonal map samples bit ``t`` of ``T**t(S)`` at output bit ``t``.
These routines work modulo ``2**width``.  They are exact finite operations;
the corresponding statement on the 2-adic integers is proved separately in
``proofs/informal/problem1_two_adic_diagonal_map.md``.
"""

from __future__ import annotations


def _checked_width(width: int) -> int:
    if not isinstance(width, int) or isinstance(width, bool) or width <= 0:
        raise ValueError("width must be a positive integer")
    return width


def _checked_residue(value: int, width: int, *, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{name} must be an integer residue")
    if value < 0 or value >= (1 << width):
        raise ValueError(f"{name} does not fit the requested width")
    return value


def right_edge_step_mod(state: int, width: int) -> int:
    """Apply the right-edge recurrence modulo ``2**width``."""

    width = _checked_width(width)
    state = _checked_residue(state, width, name="state")
    mask = (1 << width) - 1
    return (state ^ ((state << 1) | (state << 2))) & mask


def diagonal_map_mod(seed: int, width: int) -> int:
    """Return the first ``width`` diagonal bits as one integer residue.

    Output bit ``t`` is bit ``t`` of ``T**t(seed)``.  Reduction after every
    update is exact because no output below ``width`` depends on a higher bit.
    """

    width = _checked_width(width)
    state = _checked_residue(seed, width, name="seed")
    output = 0
    for time in range(width):
        output |= ((state >> time) & 1) << time
        state = right_edge_step_mod(state, width)
    return output


def inverse_diagonal_map_mod(trace: int, width: int) -> int:
    """Invert the finite diagonal map by its unit triangular structure.

    When seed bit ``t`` is still zero, the mismatch between output bit ``t``
    and the requested trace bit is exactly the required value of seed bit
    ``t``.  Previously selected lower bits are never changed.
    """

    width = _checked_width(width)
    trace = _checked_residue(trace, width, name="trace")
    seed = 0
    for time in range(width):
        current = diagonal_map_mod(seed, time + 1)
        if ((current ^ trace) >> time) & 1:
            seed |= 1 << time
    return seed


def minus_one_third_mod(width: int) -> int:
    """Return the residue of ``-1/3`` modulo ``2**width``."""

    width = _checked_width(width)
    modulus = 1 << width
    return (-pow(3, -1, modulus)) % modulus


def plus_one_third_mod(width: int) -> int:
    """Return the residue of ``1/3`` modulo ``2**width``."""

    width = _checked_width(width)
    modulus = 1 << width
    return pow(3, -1, modulus)


__all__ = [
    "diagonal_map_mod",
    "inverse_diagonal_map_mod",
    "minus_one_third_mod",
    "plus_one_third_mod",
    "right_edge_step_mod",
]
