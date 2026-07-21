"""Coordinate-explicit Rule 30 reference implementation.

This module is intentionally straightforward and independently written. Rows
are byte arrays in increasing spatial coordinate. Row ``t`` contains sites
``-t`` through ``t``, so its center is at index ``t``.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence


def _checked_bit(value: int, *, name: str) -> int:
    bit = int(value)
    if bit not in (0, 1):
        raise ValueError(f"{name} must be 0 or 1, got {value!r}")
    return bit


def rule30_bit(left: int, center: int, right: int) -> int:
    """Return the Rule 30 local map for three checked binary inputs."""
    left_bit = _checked_bit(left, name="left")
    center_bit = _checked_bit(center, name="center")
    right_bit = _checked_bit(right, name="right")
    return left_bit ^ (center_bit | right_bit)


def evolve_row(row: Sequence[int]) -> bytearray:
    """Evolve one finite row with implicit zero cells on both sides.

    The output has two more cells than the input. Empty rows are accepted and
    evolve to two zero boundary cells; normal single-seed evolution never uses
    that degenerate representation.
    """
    checked = bytearray(_checked_bit(bit, name="row bit") for bit in row)
    padded = bytearray(2)
    padded.extend(checked)
    padded.extend((0, 0))
    return bytearray(
        padded[index] ^ (padded[index + 1] | padded[index + 2])
        for index in range(len(checked) + 2)
    )


def generate_rows(updates: int) -> Iterator[bytearray]:
    """Yield rows at times 0 through ``updates`` inclusive."""
    if updates < 0:
        raise ValueError("updates must be nonnegative")

    row = bytearray((1,))
    yield row.copy()
    for _ in range(updates):
        row = evolve_row(row)
        yield row.copy()


def center_bits_cell_array(count: int) -> bytearray:
    """Return exactly ``count`` center bits, beginning with ``c_0``."""
    if count < 0:
        raise ValueError("count must be nonnegative")
    if count == 0:
        return bytearray()

    centers = bytearray(count)
    for time, row in enumerate(generate_rows(count - 1)):
        centers[time] = row[time]
    return centers


def rows_as_text(rows: Iterable[Sequence[int]]) -> str:
    """Serialize rows as one plain binary string per line."""
    return "".join(
        "".join(str(_checked_bit(bit, name="row bit")) for bit in row) + "\n"
        for row in rows
    )
