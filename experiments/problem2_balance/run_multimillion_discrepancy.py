#!/usr/bin/env python3
"""Checkpointed exact discrepancy observations at multi-million horizons.

Each requested horizon is evolved independently by the verified C++ engine.
After a horizon completes, its exact JSON is validated and atomically added to
the restart state.  Larger runs request every earlier checkpoint, so overlap
consistency is checked rather than assumed.  This is finite computation, not
an asymptotic balance result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PYTHON_SOURCE = REPOSITORY_ROOT / "src" / "python"
if str(PYTHON_SOURCE) not in sys.path:
    sys.path.insert(0, str(PYTHON_SOURCE))

from rule30lab.records import atomic_write_json  # noqa: E402
from rule30lab.resources import atomic_write_checkpoint  # noqa: E402


SCRIPT_RELATIVE_PATH = Path(
    "experiments/problem2_balance/run_multimillion_discrepancy.py"
)
STATE_SCHEMA_VERSION = 1
HARD_MAX_COUNT = 8_000_000
HARD_MAX_HORIZONS = 8
HARD_MAX_TIMEOUT_SECONDS = 1_800.0
HARD_MAX_STDOUT_BYTES = 1 << 20
EXPERIMENT_ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")


class CampaignError(RuntimeError):
    """Raised when campaign configuration or native output is invalid."""


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(1 << 20):
            digest.update(chunk)
    return digest.hexdigest()


def parse_counts(text: str) -> tuple[int, ...]:
    try:
        raw = tuple(int(item.strip()) for item in text.split(",") if item.strip())
    except ValueError as exc:
        raise CampaignError("counts must be comma-separated integers") from exc
    if not raw:
        raise CampaignError("at least one horizon is required")
    if len(raw) > HARD_MAX_HORIZONS:
        raise CampaignError(f"at most {HARD_MAX_HORIZONS} horizons are allowed")
    if len(set(raw)) != len(raw):
        raise CampaignError("duplicate horizons are not allowed")
    counts = tuple(sorted(raw))
    if counts[0] < 1_000_000:
        raise CampaignError("this campaign requires horizons of at least 1,000,000")
    if counts[-1] > HARD_MAX_COUNT:
        raise CampaignError(f"horizon exceeds hard cap {HARD_MAX_COUNT}")
    return counts


def validate_cpp_payload(
    payload: Mapping[str, Any],
    *,
    run_count: int,
    requested_checkpoints: Sequence[int],
    backend: str,
) -> dict[str, Any]:
    required = {"count", "ones", "zeros", "discrepancy", "backend", "checkpoints"}
    if not required.issubset(payload):
        missing = sorted(required.difference(payload))
        raise CampaignError(f"native JSON is missing fields: {missing}")
    if payload["count"] != run_count:
        raise CampaignError("native count does not match the requested horizon")
    ones = payload["ones"]
    zeros = payload["zeros"]
    discrepancy = payload["discrepancy"]
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (ones, zeros, discrepancy)):
        raise CampaignError("native counts and discrepancy must be integers")
    if ones < 0 or zeros < 0 or ones + zeros != run_count:
        raise CampaignError("native ones/zeros do not partition the horizon")
    if discrepancy != 2 * ones - run_count:
        raise CampaignError("native discrepancy is inconsistent with ones")
    if payload["backend"] != backend:
        raise CampaignError(
            f"native backend {payload['backend']!r} does not equal {backend!r}"
        )
    checkpoints = payload["checkpoints"]
    if not isinstance(checkpoints, list):
        raise CampaignError("native checkpoints must be a list")
    expected = tuple(requested_checkpoints)
    if tuple(item.get("count") for item in checkpoints if isinstance(item, dict)) != expected:
        raise CampaignError("native checkpoint counts do not match the exact request")
    validated_checkpoints: list[dict[str, int]] = []
    for item in checkpoints:
        if not isinstance(item, dict) or set(item) != {"count", "ones", "discrepancy"}:
            raise CampaignError("native checkpoint shape is invalid")
        count = item["count"]
        checkpoint_ones = item["ones"]
        checkpoint_discrepancy = item["discrepancy"]
        if any(
            isinstance(value, bool) or not isinstance(value, int)
            for value in (count, checkpoint_ones, checkpoint_discrepancy)
        ):
            raise CampaignError("native checkpoint fields must be integers")
        if checkpoint_ones < 0 or checkpoint_ones > count:
            raise CampaignError("native checkpoint ones is outside its range")
        if checkpoint_discrepancy != 2 * checkpoint_ones - count:
            raise CampaignError("native checkpoint discrepancy is inconsistent")
        validated_checkpoints.append(
            {
                "count": count,
                "ones": checkpoint_ones,
                "discrepancy": checkpoint_discrepancy,
            }
        )
    if validated_checkpoints[-1] != {
        "count": run_count,
        "ones": ones,
        "discrepancy": discrepancy,
    }:
        raise CampaignError("final checkpoint does not match the native summary")
    return {
        "count": run_count,
        "ones": ones,
        "zeros": zeros,
        "discrepancy": discrepancy,
        "backend": backend,
        "checkpoints": validated_checkpoints,
    }


def discrepancy_fit(observations: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    usable = [
        {"n": int(item["n"]), "discrepancy": int(item["discrepancy"])}
        for item in observations
        if int(item["discrepancy"]) != 0
    ]
    base = {
        "status": "heuristic",
        "model": "log(abs(D(N))) = intercept + slope * log(N)",
        "selection": "all requested nonzero-discrepancy horizons",
        "limitations": [
            "the horizons are sparse and selected before observing this run",
            "the fit is descriptive and is not an upper bound",
            "no asymptotic behavior follows from finitely many observations",
        ],
        "included": usable,
        "excluded_zero_discrepancy": [
            int(item["n"])
            for item in observations
            if int(item["discrepancy"]) == 0
        ],
    }
    if len(usable) < 2:
        return {**base, "status": "inconclusive", "slope": None, "intercept": None, "r_squared": None}
    xs = [math.log(item["n"]) for item in usable]
    ys = [math.log(abs(item["discrepancy"])) for item in usable]
    x_mean = math.fsum(xs) / len(xs)
    y_mean = math.fsum(ys) / len(ys)
    sum_xx = math.fsum((value - x_mean) ** 2 for value in xs)
    if sum_xx == 0.0:
        return {**base, "status": "inconclusive", "slope": None, "intercept": None, "r_squared": None}
    slope = math.fsum(
        (x - x_mean) * (y - y_mean) for x, y in zip(xs, ys, strict=True)
    ) / sum_xx
    intercept = y_mean - slope * x_mean
    residual = math.fsum(
        (y - (intercept + slope * x)) ** 2
        for x, y in zip(xs, ys, strict=True)
    )
    total = math.fsum((y - y_mean) ** 2 for y in ys)
    return {
        **base,
        "slope": slope,
        "intercept": intercept,
        "coefficient": math.exp(intercept),
        "r_squared": None if total == 0.0 else 1.0 - residual / total,
    }


def build_scientific_payload(
    counts: Sequence[int], completed_runs: Sequence[Mapping[str, Any]]
) -> dict[str, Any]:
    if tuple(item["count"] for item in completed_runs) != tuple(counts):
        raise CampaignError("completed runs do not exactly cover configured horizons")
    overlap: dict[int, tuple[int, int]] = {}
    overlap_sources: dict[int, list[int]] = {}
    for run in completed_runs:
        for checkpoint in run["checkpoints"]:
            count = int(checkpoint["count"])
            value = (int(checkpoint["ones"]), int(checkpoint["discrepancy"]))
            if count in overlap and overlap[count] != value:
                raise CampaignError(f"overlap mismatch at checkpoint {count}")
            overlap[count] = value
            overlap_sources.setdefault(count, []).append(int(run["count"]))
    observations = []
    for count in counts:
        ones, discrepancy = overlap[count]
        observations.append(
            {
                "n": count,
                "ones": ones,
                "zeros": count - ones,
                "discrepancy": discrepancy,
                "discrepancy_over_sqrt_n": discrepancy / math.sqrt(count),
                "discrepancy_over_n": discrepancy / count,
                "overlap_run_horizons": overlap_sources[count],
            }
        )
    return {
        "schema_version": 1,
        "question": "problem2",
        "status": "empirical",
        "hypothesis": (
            "Selected multi-million center-prefix discrepancies remain small "
            "relative to N; the observations do not establish a limit."
        ),
        "parameters": {
            "horizons": list(counts),
            "prefix_convention": "c_0 through c_(N-1)",
            "initial_condition": "single black cell",
        },
        "finite_observations": observations,
        "overlap_consistency": {
            "status": "finite-exhaustive",
            "all_repeated_checkpoints_equal": True,
            "comparison_count": sum(
                max(0, len(sources) - 1) for sources in overlap_sources.values()
            ),
        },
        "heuristic_fit": discrepancy_fit(observations),
        "interpretation": (
            "Every listed integer was emitted by independently restarted native "
            "evolutions and repeated checkpoint values agreed exactly."
        ),
        "limitations": [
            "only the explicitly listed finite horizons were observed",
            "restarted runs share the same implementation and are not independent algorithms",
            "small D(N)/N at finite N does not prove D(N)=o(N)",
            "the log-log fit is heuristic and highly checkpoint-dependent",
        ],
    }


def validate_resume_state(
    state: Mapping[str, Any],
    *,
    counts: Sequence[int],
    backend: str,
    executable_sha256: str,
) -> list[dict[str, Any]]:
    if state.get("schema_version") != STATE_SCHEMA_VERSION:
        raise CampaignError("checkpoint schema version mismatch")
    configuration = state.get("configuration")
    if configuration != {
        "counts": list(counts),
        "backend": backend,
        "executable_sha256": executable_sha256,
    }:
        raise CampaignError("checkpoint configuration does not match this run")
    completed = state.get("completed_runs")
    if not isinstance(completed, list):
        raise CampaignError("checkpoint completed_runs must be a list")
    expected_prefix = list(counts[: len(completed)])
    if [item.get("count") for item in completed if isinstance(item, dict)] != expected_prefix:
        raise CampaignError("checkpoint does not contain a valid horizon prefix")
    return [dict(item) for item in completed]


def validate_checkpoint_path(path: Path) -> Path:
    resolved = path.resolve()
    runs_root = (REPOSITORY_ROOT / "results" / "runs").resolve()
    if resolved.parent != runs_root or not resolved.name.endswith(
        ".checkpoint.state"
    ):
        raise CampaignError(
            "checkpoint state must be directly under results/runs and end "
            "with .checkpoint.state so it remains an ignored restart artifact"
        )
    return resolved


def _git(arguments: Sequence[str]) -> bytes:
    environment = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C",
        "LC_ALL": "C",
        "HOME": str(REPOSITORY_ROOT),
    }
    completed = subprocess.run(
        ["/usr/bin/git", "-C", str(REPOSITORY_ROOT), *arguments],
        check=True,
        capture_output=True,
        env=environment,
    )
    return completed.stdout


def repository_provenance() -> dict[str, Any]:
    head = _git(["rev-parse", "HEAD"]).decode("ascii").strip()
    status = _git(["status", "--porcelain=v1", "--untracked-files=all"])
    working_script = (REPOSITORY_ROOT / SCRIPT_RELATIVE_PATH).read_bytes()
    head_script = _git(["show", f"HEAD:{SCRIPT_RELATIVE_PATH.as_posix()}"])
    return {
        "head": head,
        "clean": not status,
        "script_sha256": _sha256_bytes(working_script),
        "script_matches_head": working_script == head_script,
    }


def _cpu_model() -> str:
    for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
        if line.startswith("model name"):
            return line.split(":", 1)[1].strip()
    return "unknown"


def run_native_horizon(
    executable: Path,
    *,
    count: int,
    checkpoints: Sequence[int],
    backend: str,
    timeout_seconds: float,
    nice_level: int,
) -> dict[str, Any]:
    argv = [
        "/usr/bin/nice",
        "-n",
        str(nice_level),
        str(executable),
        "generate",
        "--count",
        str(count),
        "--backend",
        backend,
        "--format",
        "json",
    ]
    for checkpoint in checkpoints:
        argv.extend(("--checkpoint", str(checkpoint)))
    environment = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C",
        "LC_ALL": "C",
        "OMP_NUM_THREADS": "1",
    }
    start = time.monotonic()
    try:
        completed = subprocess.run(
            argv,
            cwd=REPOSITORY_ROOT,
            env=environment,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise CampaignError(f"native horizon {count} exceeded its wall limit") from exc
    elapsed = time.monotonic() - start
    if completed.returncode != 0:
        raise CampaignError(
            f"native horizon {count} failed with {completed.returncode}: "
            f"{completed.stderr[:4096].decode('utf-8', errors='replace')}"
        )
    if completed.stderr:
        raise CampaignError(f"native horizon {count} emitted unexpected stderr")
    if len(completed.stdout) > HARD_MAX_STDOUT_BYTES:
        raise CampaignError("native JSON exceeds the hard output cap")
    try:
        decoded = json.loads(completed.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CampaignError("native stdout is not one valid JSON document") from exc
    if not isinstance(decoded, dict):
        raise CampaignError("native JSON must be an object")
    validated = validate_cpp_payload(
        decoded,
        run_count=count,
        requested_checkpoints=checkpoints,
        backend=backend,
    )
    return {
        **validated,
        "argv": argv,
        "runtime_seconds": elapsed,
        "stdout_sha256": _sha256_bytes(completed.stdout),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cpp-executable", type=Path, required=True)
    parser.add_argument("--counts", default="1000000,2000000,4000000")
    parser.add_argument("--backend", choices=("scalar", "avx2"), default="avx2")
    parser.add_argument("--checkpoint-state", type=Path, required=True)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--timeout-seconds", type=float, default=300.0)
    parser.add_argument("--nice-level", type=int, default=10)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--overwrite-record", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if EXPERIMENT_ID_PATTERN.fullmatch(args.experiment_id) is None:
        raise CampaignError("experiment ID contains unsupported characters")
    counts = parse_counts(args.counts)
    if not (0.0 < args.timeout_seconds <= HARD_MAX_TIMEOUT_SECONDS):
        raise CampaignError(
            f"timeout must be in (0,{HARD_MAX_TIMEOUT_SECONDS}] seconds"
        )
    if not 0 <= args.nice_level <= 19:
        raise CampaignError("nice level must be between 0 and 19")
    executable = args.cpp_executable.resolve(strict=True)
    if not executable.is_file() or not os.access(executable, os.X_OK):
        raise CampaignError("C++ executable must be an executable regular file")
    checkpoint_path = validate_checkpoint_path(args.checkpoint_state)
    record_path = args.record.resolve()
    result_root = (REPOSITORY_ROOT / "results" / "problem2").resolve()
    if record_path.parent != result_root or record_path.suffix != ".json":
        raise CampaignError("record must be directly under results/problem2")
    if record_path.exists() and not args.overwrite_record:
        raise CampaignError("record already exists; use --overwrite-record explicitly")

    provenance_before = repository_provenance()
    if not provenance_before["clean"] or not provenance_before["script_matches_head"]:
        raise CampaignError("persistent campaigns require a clean committed script")
    executable_hash = file_sha256(executable)
    configuration = {
        "counts": list(counts),
        "backend": args.backend,
        "executable_sha256": executable_hash,
    }
    if args.resume:
        if not checkpoint_path.exists():
            raise CampaignError("--resume requires an existing checkpoint state")
        state = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        completed_runs = validate_resume_state(
            state,
            counts=counts,
            backend=args.backend,
            executable_sha256=executable_hash,
        )
    else:
        if checkpoint_path.exists():
            raise CampaignError("checkpoint exists; use --resume or a new path")
        completed_runs = []

    campaign_start = time.monotonic()
    for count in counts[len(completed_runs) :]:
        requested = tuple(value for value in counts if value <= count)
        print(
            json.dumps(
                {
                    "event": "horizon_start",
                    "count": count,
                    "completed_horizons": len(completed_runs),
                },
                sort_keys=True,
            ),
            file=sys.stderr,
            flush=True,
        )
        run = run_native_horizon(
            executable,
            count=count,
            checkpoints=requested,
            backend=args.backend,
            timeout_seconds=args.timeout_seconds,
            nice_level=args.nice_level,
        )
        completed_runs.append(run)
        atomic_write_checkpoint(
            checkpoint_path,
            {
                "schema_version": STATE_SCHEMA_VERSION,
                "configuration": configuration,
                "completed_runs": completed_runs,
                "complete": len(completed_runs) == len(counts),
                "resume_semantics": "restart only the first unfinished independent horizon",
            },
        )
        print(
            json.dumps(
                {
                    "event": "horizon_complete",
                    "count": count,
                    "discrepancy": run["discrepancy"],
                    "runtime_seconds": run["runtime_seconds"],
                },
                sort_keys=True,
            ),
            file=sys.stderr,
            flush=True,
        )

    scientific = build_scientific_payload(counts, completed_runs)
    scientific_bytes = json.dumps(
        scientific, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")
    provenance_after = repository_provenance()
    if provenance_after != provenance_before:
        raise CampaignError("repository provenance changed during the campaign")
    if file_sha256(executable) != executable_hash:
        raise CampaignError("native executable changed during the campaign")
    finalization_invocation_seconds = time.monotonic() - campaign_start
    runtime_seconds = math.fsum(
        float(run["runtime_seconds"]) for run in completed_runs
    )
    checkpoint_hash = file_sha256(checkpoint_path)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )
    record = {
        "experiment_id": args.experiment_id,
        "timestamp_utc": timestamp,
        "git_commit": provenance_before["head"],
        "question": "problem2",
        "hypothesis": scientific["hypothesis"],
        "backend": f"cpp-{args.backend}-independent-horizon-restarts",
        "parameters": {
            "counts": list(counts),
            "timeout_seconds_per_horizon": args.timeout_seconds,
            "nice_level": args.nice_level,
            "checkpoint_path": str(checkpoint_path),
            "resume_requested": args.resume,
            "hard_max_count": HARD_MAX_COUNT,
        },
        "hardware": {
            "execution_scope": "local WSL2 host only",
            "cpu_model": _cpu_model(),
            "logical_cpu_count": os.cpu_count(),
            "machine": platform.machine(),
            "remote_compute_used": False,
            "hardware_settings_changed": False,
        },
        "software": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "cpp_executable": str(executable),
            "script": str(SCRIPT_RELATIVE_PATH),
            "repository_clean_before_and_after": True,
            "script_matches_head": True,
            "runtime_scope": (
                "sum of native subprocess elapsed times retained across "
                "checkpoint/resume attempts"
            ),
            "finalization_invocation_seconds": finalization_invocation_seconds,
        },
        "runtime_seconds": runtime_seconds,
        "result_hashes": {
            "scientific_payload_sha256": _sha256_bytes(scientific_bytes),
            "cpp_executable_sha256": executable_hash,
            "script_sha256": provenance_before["script_sha256"],
            "checkpoint_state_sha256": checkpoint_hash,
        },
        "result_summary": {
            "scientific_payload": scientific,
            "native_runs": completed_runs,
            "all_horizons_completed": True,
        },
        "interpretation": scientific["interpretation"],
        "status": "empirical",
        "proof_scope": (
            "Exact counts only for the listed finite horizons and overlap "
            "checks; the fitted exponent is heuristic."
        ),
        "limitations": scientific["limitations"]
        + [
            "native executable hashes and a clean source tree are provenance evidence, not build attestation",
            "checkpointing is between independent complete evolutions, not within a single evolution",
            "top-level runtime sums native subprocess times and excludes failed-publication and orchestration overhead",
        ],
    }
    atomic_write_json(record_path, record)
    print(json.dumps(record, indent=2, sort_keys=True, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
