"""Atomic experiment-record support."""

from __future__ import annotations

import json
import os
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = frozenset(
    {
        "empirical",
        "finite-exhaustive",
        "heuristic",
        "partial-proof",
        "rigorous-proof",
        "refuted",
        "inconclusive",
    }
)

REQUIRED_FIELDS = frozenset(
    {
        "experiment_id",
        "timestamp_utc",
        "git_commit",
        "question",
        "hypothesis",
        "backend",
        "parameters",
        "hardware",
        "software",
        "runtime_seconds",
        "result_hashes",
        "result_summary",
        "interpretation",
        "status",
        "proof_scope",
        "limitations",
    }
)


def validate_record(record: Mapping[str, Any]) -> None:
    """Validate the stable top-level experiment-record contract."""
    missing = REQUIRED_FIELDS.difference(record)
    if missing:
        raise ValueError(f"missing experiment fields: {', '.join(sorted(missing))}")
    if record["status"] not in ALLOWED_STATUSES:
        raise ValueError(f"invalid experiment status: {record['status']!r}")
    if record["question"] not in {"problem1", "problem2", "problem3"}:
        raise ValueError(f"invalid question: {record['question']!r}")
    runtime = record["runtime_seconds"]
    if not isinstance(runtime, (int, float)) or runtime < 0:
        raise ValueError("runtime_seconds must be a nonnegative number")


def atomic_write_json(path: Path, record: Mapping[str, Any]) -> None:
    """Validate and atomically replace ``path`` with deterministic JSON."""
    validate_record(record)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(record, stream, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise
