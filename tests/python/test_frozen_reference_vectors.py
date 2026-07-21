from __future__ import annotations

import hashlib
import json
from pathlib import Path

import rule30_research_reference as supplied

VECTORS = Path(__file__).resolve().parents[1] / "reference_vectors"


def test_manifest_hashes_match_files() -> None:
    manifest = json.loads((VECTORS / "manifest.json").read_text(encoding="utf-8"))
    for filename, expected in manifest["files"].items():
        data = (VECTORS / filename).read_bytes()
        assert len(data) == expected["bytes"]
        assert hashlib.sha256(data).hexdigest() == expected["sha256"]


def test_complete_rows_have_explicit_coordinate_convention() -> None:
    lines = (VECTORS / "rows_t0000_t0255.txt").read_text(encoding="ascii").splitlines()
    assert len(lines) == 256
    centers = bytearray()
    for time, line in enumerate(lines):
        label, row = line.split("\t")
        assert label == f"{time:04d}"
        assert len(row) == 2 * time + 1
        assert set(row) <= {"0", "1"}
        centers.append(int(row[time]))

    frozen = (VECTORS / "center_c00000000_c00009999.u8").read_bytes()
    assert centers == frozen[:256]


def test_frozen_center_matches_supplied_reference() -> None:
    frozen = (VECTORS / "center_c00000000_c00009999.u8").read_bytes()
    assert len(frozen) == 10_000
    assert frozen == supplied.center_column(9_999)
