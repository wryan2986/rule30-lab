from __future__ import annotations

import importlib.util
import json
from pathlib import Path


def _load_generator():
    script = Path(__file__).resolve().parents[2] / "scripts" / "generate_reference_vectors.py"
    spec = importlib.util.spec_from_file_location("generate_reference_vectors", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_sparse_rows_match_hand_values() -> None:
    generator = _load_generator()
    assert [bytes(row) for row in generator.sparse_rows(5)] == [
        b"\x01",
        b"\x01\x01\x01",
        b"\x01\x01\x00\x00\x01",
        b"\x01\x01\x00\x01\x01\x01\x01",
        b"\x01\x01\x00\x00\x01\x00\x00\x00\x01",
    ]


def test_small_generation_is_deterministic_and_self_describing(tmp_path: Path) -> None:
    generator = _load_generator()
    repository = Path(__file__).resolve().parents[2]
    manifest = generator.generate_vectors(tmp_path, 9, 100, repository)

    assert manifest["balance_checkpoints"]["100"]["ones"] == 52
    assert manifest["balance_checkpoints"]["100"]["discrepancy"] == 4
    assert manifest["status"] == "provisional-two-way"
    assert manifest["cross_checks"]["compiled_backend_pending"] is True

    disk_manifest = json.loads((tmp_path / "manifest.json").read_text(encoding="utf-8"))
    assert disk_manifest == manifest
    rows_path = tmp_path / "rows_t0000_t0008.txt"
    assert rows_path.read_text(encoding="ascii").splitlines()[-1] == "0008\t11001000111000001"
