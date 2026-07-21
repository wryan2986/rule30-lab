from __future__ import annotations

import json
from pathlib import Path

import pytest

from rule30lab.records import atomic_write_json, validate_record


def complete_record() -> dict[str, object]:
    return {
        "experiment_id": "test-1",
        "timestamp_utc": "2026-07-21T00:00:00Z",
        "git_commit": "0" * 40,
        "question": "problem1",
        "hypothesis": "bounded test fixture",
        "backend": "python",
        "parameters": {},
        "hardware": {},
        "software": {},
        "runtime_seconds": 0.0,
        "result_hashes": {},
        "result_summary": {},
        "interpretation": "fixture only",
        "status": "empirical",
        "proof_scope": "none",
        "limitations": ["fixture"],
    }


def test_record_validation() -> None:
    validate_record(complete_record())
    missing = complete_record()
    del missing["backend"]
    with pytest.raises(ValueError, match="missing experiment fields"):
        validate_record(missing)
    bad_status = complete_record()
    bad_status["status"] = "proved-by-testing"
    with pytest.raises(ValueError, match="invalid experiment status"):
        validate_record(bad_status)


def test_atomic_write_json(tmp_path: Path) -> None:
    destination = tmp_path / "nested" / "record.json"
    record = complete_record()
    atomic_write_json(destination, record)
    assert json.loads(destination.read_text(encoding="utf-8")) == record
    assert not list(destination.parent.glob("*.tmp"))
