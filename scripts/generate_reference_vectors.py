#!/usr/bin/env python3
"""Generate provisional Rule 30 vectors from independent implementations."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import rule30_research_reference as supplied
from rule30lab.core import center_bits_cell_array, generate_rows

DEFAULT_OUTPUT = Path("tests/reference_vectors")


def sparse_rows(row_count: int) -> Iterator[bytearray]:
    """Yield ``row_count`` rows using a coordinate set of live cells."""
    if row_count < 0:
        raise ValueError("row_count must be nonnegative")

    live = {0}
    for time in range(row_count):
        yield bytearray(1 if coordinate in live else 0 for coordinate in range(-time, time + 1))
        next_live: set[int] = set()
        for coordinate in range(-time - 1, time + 2):
            left = coordinate - 1 in live
            center = coordinate in live
            right = coordinate + 1 in live
            if left ^ (center or right):
                next_live.add(coordinate)
        live = next_live


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_commit(repository: Path) -> str:
    return subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=repository,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _file_record(data: bytes) -> dict[str, Any]:
    return {"bytes": len(data), "sha256": _sha256(data)}


def generate_vectors(output: Path, row_count: int, center_count: int, repository: Path) -> dict[str, Any]:
    """Cross-check implementations, atomically write vectors, and return the manifest."""
    if row_count < 0 or center_count < 0:
        raise ValueError("vector sizes must be nonnegative")

    cell_rows = list(generate_rows(row_count - 1)) if row_count else []
    set_rows = list(sparse_rows(row_count))
    if cell_rows != set_rows:
        mismatch = next(
            index for index, (cell, sparse) in enumerate(zip(cell_rows, set_rows)) if cell != sparse
        )
        raise RuntimeError(f"independent complete-row mismatch at t={mismatch}")

    centers_cell = center_bits_cell_array(center_count)
    centers_supplied = (
        supplied.center_column(center_count - 1) if center_count else bytearray()
    )
    if centers_cell != centers_supplied:
        mismatch = next(
            index
            for index, (cell, reference) in enumerate(zip(centers_cell, centers_supplied))
            if cell != reference
        )
        raise RuntimeError(f"independent center mismatch at t={mismatch}")

    rows_data = "".join(
        f"{time:04d}\t{''.join(str(bit) for bit in row)}\n"
        for time, row in enumerate(cell_rows)
    ).encode("ascii")
    centers_u8 = bytes(centers_cell)
    centers_text = ("".join(str(bit) for bit in centers_cell) + "\n").encode("ascii")

    rows_name = f"rows_t0000_t{row_count - 1:04d}.txt" if row_count else "rows_empty.txt"
    center_u8_name = f"center_c00000000_c{center_count - 1:08d}.u8" if center_count else "center_empty.u8"
    center_text_name = (
        f"center_c00000000_c{center_count - 1:08d}.txt" if center_count else "center_empty.txt"
    )

    _atomic_write(output / rows_name, rows_data)
    _atomic_write(output / center_u8_name, centers_u8)
    _atomic_write(output / center_text_name, centers_text)

    checkpoints: dict[str, dict[str, int | float]] = {}
    for count in (10, 100, 1_000, 10_000):
        if count <= center_count:
            ones = sum(centers_cell[:count])
            checkpoints[str(count)] = {
                "ones": ones,
                "zeros": count - ones,
                "discrepancy": 2 * ones - count,
                "ones_fraction": ones / count,
            }

    reference_path = repository / "src/python/rule30_research_reference.py"
    manifest: dict[str, Any] = {
        "schema_version": 1,
        "status": "provisional-two-way",
        "source_git_commit": _git_commit(repository),
        "conventions": {
            "center": "exactly count bits c_0 through c_(count-1), one byte per bit",
            "rows": "row t spans j=-t through j=t in increasing coordinate",
        },
        "cross_checks": {
            "complete_rows": ["coordinate-bytearray", "live-coordinate-set"],
            "center_bits": ["coordinate-bytearray", "supplied-packed-integer"],
            "compiled_backend_pending": True,
        },
        "supplied_reference_sha256": _sha256(reference_path.read_bytes()),
        "parameters": {"row_count": row_count, "center_count": center_count},
        "files": {
            rows_name: _file_record(rows_data),
            center_u8_name: _file_record(centers_u8),
            center_text_name: _file_record(centers_text),
        },
        "balance_checkpoints": checkpoints,
    }
    manifest_data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    _atomic_write(output / "manifest.json", manifest_data)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--row-count", type=int, default=256)
    parser.add_argument("--center-count", type=int, default=10_000)
    args = parser.parse_args()

    repository = Path(__file__).resolve().parents[1]
    manifest = generate_vectors(
        args.output.resolve(), args.row_count, args.center_count, repository
    )
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
