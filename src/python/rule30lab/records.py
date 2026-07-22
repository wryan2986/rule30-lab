"""Atomic experiment-record support."""

from __future__ import annotations

import json
import math
import os
import re
import tempfile
from collections.abc import Mapping
from datetime import datetime, timedelta
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

_FULL_GIT_COMMIT = re.compile(r"[0-9a-f]{40}")


def _require_nonempty_string(record: Mapping[str, Any], field: str) -> None:
    value = record[field]
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")


def validate_record(record: Mapping[str, Any]) -> None:
    """Validate the stable top-level experiment-record contract."""
    missing = REQUIRED_FIELDS.difference(record)
    if missing:
        raise ValueError(f"missing experiment fields: {', '.join(sorted(missing))}")
    if record["status"] not in ALLOWED_STATUSES:
        raise ValueError(f"invalid experiment status: {record['status']!r}")
    if record["question"] not in {"problem1", "problem2", "problem3"}:
        raise ValueError(f"invalid question: {record['question']!r}")

    for field in (
        "experiment_id",
        "timestamp_utc",
        "git_commit",
        "hypothesis",
        "backend",
        "interpretation",
        "proof_scope",
    ):
        _require_nonempty_string(record, field)

    timestamp = record["timestamp_utc"]
    if not timestamp.endswith("Z"):
        raise ValueError("timestamp_utc must use an explicit UTC Z suffix")
    try:
        parsed_timestamp = datetime.fromisoformat(timestamp[:-1] + "+00:00")
    except ValueError as exc:
        raise ValueError("timestamp_utc must be an ISO-8601 timestamp") from exc
    if parsed_timestamp.utcoffset() != timedelta(0):
        raise ValueError("timestamp_utc must identify UTC")

    if _FULL_GIT_COMMIT.fullmatch(record["git_commit"]) is None:
        raise ValueError("git_commit must be a full lowercase 40-hex commit")

    runtime = record["runtime_seconds"]
    if (
        isinstance(runtime, bool)
        or not isinstance(runtime, (int, float))
        or not math.isfinite(runtime)
        or runtime < 0
    ):
        raise ValueError("runtime_seconds must be a finite nonnegative number")

    for field in ("parameters", "hardware", "software", "result_hashes", "result_summary"):
        if not isinstance(record[field], Mapping):
            raise ValueError(f"{field} must be a mapping")
    if not all(
        isinstance(name, str) and isinstance(value, str) and value
        for name, value in record["result_hashes"].items()
    ):
        raise ValueError("result_hashes must map string names to nonempty strings")

    limitations = record["limitations"]
    if not isinstance(limitations, list) or not all(
        isinstance(item, str) and item.strip() for item in limitations
    ):
        raise ValueError("limitations must be a list of nonempty strings")

    try:
        json.dumps(record, allow_nan=False)
    except (TypeError, ValueError) as exc:
        raise ValueError("experiment record must be finite JSON data") from exc


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
            json.dump(record, stream, indent=2, sort_keys=True, allow_nan=False)
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
