"""Local-only, resource-bounded execution of repository experiments.

The runner accepts an experiment *name*, never a script path.  Each child is
an audited repository script and is started with an argument vector
without a shell.  Child stdout and stderr are streamed into bounded, atomic
artifacts while the parent enforces wall-clock, address-space, disk, output,
and optional read-only GPU-telemetry policies.

Checkpoints describe runner state only.  The current experiment scripts do not
implement a generic mid-script checkpoint protocol, so resuming a checkpoint
always validates the prior invocation and restarts the child from the
beginning.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import re
import selectors
import signal
import subprocess
import sys
import tempfile
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path
from typing import Any, BinaryIO

from .records import ALLOWED_STATUSES, atomic_write_json
from .resources import (
    GracefulInterruption,
    NvidiaSnapshot,
    ResourceLimitExceeded,
    ResourceLimits,
    ResourceProfile,
    apply_address_space_limit,
    atomic_write_checkpoint,
    check_wall_time,
    ensure_disk_budget,
    ensure_output_budget,
    query_nvidia_snapshot,
)


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
CONTROLLED_RUN_RELATIVE_ROOT = Path("results/runs")
CHECKPOINT_KIND = "rule30-controlled-runner-checkpoint-v1"
RUNNER_SCHEMA_VERSION = 1
READ_CHUNK_BYTES = 64 * 1024
RECORD_RESERVE_BYTES = 2 * 1024 * 1024
CHECKPOINT_RESERVE_BYTES = 512 * 1024
MAX_STDOUT_CAP_BYTES = 64 * 1024 * 1024
MAX_STDERR_CAP_BYTES = 64 * 1024 * 1024
MAX_CHILD_ARGUMENTS = 128
MAX_CHILD_ARGUMENT_BYTES = 16 * 1024
POST_KILL_DRAIN_SECONDS = 0.25
_EXPERIMENT_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}")
_READ_PATH_OPTIONS: Mapping[str, frozenset[str]] = {
    "problem1-sideways": frozenset({"--trusted-center"}),
    "problem1-sideways-invariants": frozenset(),
    "problem1-sideways-prefix-equivalence": frozenset(),
    "problem1-eventual-zero-tail": frozenset(),
    "problem1-period-defect": frozenset(),
    "problem1-period-two": frozenset(),
    "problem1-two-adic-diagonal": frozenset(),
    "problem1-inverse-lift-sections": frozenset(),
    "problem1-period-two-quotient": frozenset(),
    "problem2-finite-prefix": frozenset({"--input"}),
    "problem2-scaling": frozenset({"--input"}),
    "problem2-conservation": frozenset(),
    "problem2-polynomial-conservation": frozenset(),
    "problem3-exact-searches": frozenset({"--input"}),
    "problem3-extended-model-searches": frozenset({"--input"}),
}
_FORBIDDEN_SIDE_OUTPUT_OPTIONS = frozenset({"--export-graphs-dir"})


class ControlledRunnerError(RuntimeError):
    """Base class for controlled-runner errors."""


class RunnerConfigurationError(ControlledRunnerError):
    """Raised before execution when a requested run is unsafe or ambiguous."""


class TelemetryAction(StrEnum):
    """A process-only response to read-only NVIDIA telemetry."""

    CONTINUE = "continue"
    PAUSE = "pause"
    ABORT_TEMPERATURE = "abort-temperature"
    ABORT_GPU_MEMORY = "abort-gpu-memory"


class RunOutcome(StrEnum):
    SUCCESS = "success"
    CHILD_ERROR = "child-error"
    INVALID_OUTPUT = "invalid-output"
    TIMEOUT = "timeout"
    OUTPUT_LIMIT = "output-limit"
    INTERRUPTED = "interrupted"
    GPU_ABORT = "gpu-abort"
    TELEMETRY_ERROR = "telemetry-error"
    SPAWN_ERROR = "spawn-error"
    INTERNAL_ERROR = "internal-error"


@dataclass(frozen=True)
class ExperimentSpec:
    """Immutable policy metadata for one internal experiment entry point."""

    relative_path: Path
    question: str
    hypothesis: str
    default_status: str
    proof_scope: str
    limitations: tuple[str, ...]
    child_continuation_supported: bool = False


EXPERIMENT_ALLOWLIST: Mapping[str, ExperimentSpec] = {
    "problem1-sideways": ExperimentSpec(
        Path("experiments/problem1_nonperiodicity/run_sideways_search.py"),
        "problem1",
        "Test explicitly bounded eventually periodic traces by finite sideways reconstruction.",
        "finite-exhaustive",
        "Only the explicit finite candidate box, horizon, and fixed-width graphs emitted by the child.",
        (
            "No finite reconstruction horizon proves eventual nonperiodicity.",
            "Untested preperiods, periods, and reconstruction depths remain open.",
        ),
    ),
    "problem1-sideways-invariants": ExperimentSpec(
        Path("experiments/problem1_nonperiodicity/search_sideways_invariants.py"),
        "problem1",
        "Search bounded depth-independent invariants and exact cyclic-pair certificates for sideways evolution.",
        "finite-exhaustive",
        "Only the exact bounded ansatzes and finite cyclic models emitted by the child.",
        (
            "Bounded invariant families do not exhaust nonlocal or wider invariants.",
            "The cyclic-pair model assumes both adjacent columns are exactly cyclic.",
        ),
    ),
    "problem1-sideways-prefix-equivalence": ExperimentSpec(
        Path(
            "experiments/problem1_nonperiodicity/"
            "analyze_sideways_prefix_equivalence.py"
        ),
        "problem1",
        "Cross-check the finite identity between first sideways witnesses and first trusted-prefix mismatches.",
        "finite-exhaustive",
        "Only the exhaustive finite horizons and eventual-period description box emitted by the child.",
        (
            "The computational cross-check does not prove the horizon-independent lemma.",
            "The finite lemma does not establish center nonperiodicity.",
        ),
    ),
    "problem1-eventual-zero-tail": ExperimentSpec(
        Path(
            "experiments/problem1_nonperiodicity/"
            "search_eventual_zero_tail.py"
        ),
        "problem1",
        (
            "Measure complete reconstructed-left prefixes for a bounded box "
            "of eventually periodic center traces."
        ),
        "finite-exhaustive",
        (
            "Only the explicit finite description box and reconstruction "
            "checkpoints emitted by the child."
        ),
        (
            (
                "Finite interval occupancy does not prove infinitely many "
                "reconstructed ones."
            ),
            (
                "Descriptions outside the finite box and depths beyond the "
                "final checkpoint remain open."
            ),
        ),
    ),
    "problem1-period-defect": ExperimentSpec(
        Path(
            "experiments/problem1_nonperiodicity/"
            "analyze_period_defect.py"
        ),
        "problem1",
        (
            "Audit exact finite Boolean constraints induced by candidate "
            "center periods."
        ),
        "finite-exhaustive",
        "Every Boolean assignment in each explicitly listed finite p-step cone.",
        (
            "Finite period bounds do not cover arbitrary eventual periods.",
            "Full-cone ANF growth does not exclude a nonlocal identity.",
        ),
    ),
    "problem1-period-two": ExperimentSpec(
        Path(
            "experiments/problem1_nonperiodicity/"
            "analyze_period_two.py"
        ),
        "problem1",
        "Audit three concrete local mechanisms for excluding center period two.",
        "finite-exhaustive",
        (
            "Only the exact cone and explicitly bounded reconstruction, "
            "2-adic lift, and forced-half-line checks emitted by the child."
        ),
        (
            "Finite failed mechanisms do not prove period two is possible.",
            "The complete finite-support period-two case remains open.",
        ),
    ),
    "problem1-two-adic-diagonal": ExperimentSpec(
        Path(
            "experiments/problem1_nonperiodicity/"
            "analyze_two_adic_diagonal.py"
        ),
        "problem1",
        (
            "Audit finite quotients of the 2-adic diagonal bijection and "
            "the rational infinite-support countermodel."
        ),
        "finite-exhaustive",
        "Every residue modulo 2^m for each explicitly listed finite width m.",
        (
            "The executable campaign alone covers only finite quotient widths.",
            "The rational countermodel has infinite spatial support.",
        ),
    ),
    "problem1-inverse-lift-sections": ExperimentSpec(
        Path(
            "experiments/problem1_nonperiodicity/"
            "analyze_inverse_lift_sections.py"
        ),
        "problem1",
        (
            "Audit exact inverse-lift branch recurrences and bounded section "
            "closure on the period-two control trace."
        ),
        "finite-exhaustive",
        (
            "Every residue and continuation in the explicitly listed finite "
            "quotients, depths, and lookahead."
        ),
        (
            "Finite section growth does not prove unbounded state growth.",
            "The complete finite-support period-two case remains open.",
        ),
    ),
    "problem1-period-two-quotient": ExperimentSpec(
        Path(
            "experiments/problem1_nonperiodicity/"
            "analyze_period_two_quotient.py"
        ),
        "problem1",
        (
            "Audit the schedule-head and dyadic-endpoint candidates for a "
            "period-two inverse-lift quotient."
        ),
        "finite-exhaustive",
        (
            "Every listed finite lift bit, schedule state, fringe block, and "
            "all 16 two-cell local transition assignments; the all-width "
            "support criterion is proved separately."
        ),
        (
            "Counterexamples to the named candidates do not exclude every "
            "period-two quotient.",
            "Finite leading-run checks do not prove asymptotic growth.",
            "The complete finite-support period-two case remains open.",
        ),
    ),
    "problem2-finite-prefix": ExperimentSpec(
        Path("experiments/problem2_balance/run_finite_prefix.py"),
        "problem2",
        "Measure exact counts and descriptive statistics on one identified finite center prefix.",
        "empirical",
        "The identified finite center-sequence prefix only.",
        (
            "Finite statistics do not prove limiting balance.",
            "Descriptive tests do not establish randomness or normality.",
        ),
    ),
    "problem2-scaling": ExperimentSpec(
        Path("experiments/problem2_balance/run_scaling_analysis.py"),
        "problem2",
        "Measure finite discrepancy scaling and related statistics on an identified prefix.",
        "empirical",
        "The identified finite center-sequence prefix only.",
        (
            "A fitted finite-prefix slope is heuristic, not an asymptotic bound.",
            "Finite measurements do not establish the limiting frequency.",
        ),
    ),
    "problem2-conservation": ExperimentSpec(
        Path("experiments/problem2_balance/search_local_conservation.py"),
        "problem2",
        "Search an explicitly bounded exact ansatz for local telescoping identities.",
        "finite-exhaustive",
        "Only the exact finite linear systems and bounded ansatz emitted by the child.",
        (
            "Failure in a bounded ansatz does not prove that no conservation identity exists.",
            "Other radii, rings, and nonlocal identities remain untested.",
        ),
    ),
    "problem2-polynomial-conservation": ExperimentSpec(
        Path("experiments/problem2_balance/search_polynomial_conservation.py"),
        "problem2",
        "Search exact bounded-degree polynomial density/flux identities after quotienting representable coboundaries.",
        "finite-exhaustive",
        "Only the exact fields, degrees, widths, and time displacements emitted by the child.",
        (
            "A bounded polynomial ansatz does not exhaust conservation identities.",
            "A conserved quantity would still require a separate link to center discrepancy.",
        ),
    ),
    "problem3-exact-searches": ExperimentSpec(
        Path("experiments/problem3_complexity/run_exact_searches.py"),
        "problem3",
        "Search explicitly bounded exact predictor and recurrence model classes with held-out checking.",
        "finite-exhaustive",
        "Only completed finite model enumerations and finite prefix comparisons emitted by the child.",
        (
            "Failure to find a predictor does not prove a computational lower bound.",
            "Finite 2-kernel or recurrence evidence does not prove nonautomaticity.",
        ),
    ),
    "problem3-extended-model-searches": ExperimentSpec(
        Path("experiments/problem3_complexity/run_extended_model_searches.py"),
        "problem3",
        "Search bounded affine GF(2) digit-matrix models and refine a finite multiscale 2-kernel quotient.",
        "finite-exhaustive",
        "Only the exact finite model IDs, prefix splits, and sampled kernel nodes emitted by the child.",
        (
            "Failed finite models do not prove nonautomaticity.",
            "No result establishes a universal computational lower bound.",
        ),
    ),
}


@dataclass(frozen=True)
class RunnerConfiguration:
    """Complete immutable configuration for one controlled child attempt."""

    experiment: str
    child_args: tuple[str, ...]
    run_directory: Path
    experiment_id: str
    limits: ResourceLimits
    stdout_cap_bytes: int
    stderr_cap_bytes: int
    telemetry_enabled: bool = False
    telemetry_seconds: float = 5.0
    termination_grace_seconds: float = 3.0
    overwrite: bool = False
    resume_from: Path | None = None


@dataclass(frozen=True)
class RunArtifacts:
    stdout: Path
    stderr: Path
    checkpoint: Path
    record: Path


@dataclass(frozen=True)
class RunResult:
    outcome: RunOutcome
    child_returncode: int | None
    record_path: Path
    checkpoint_path: Path
    stdout_path: Path
    stderr_path: Path
    signal_number: int | None = None

    @property
    def exit_code(self) -> int:
        if self.outcome is RunOutcome.SUCCESS:
            return 0
        if self.outcome is RunOutcome.INTERRUPTED and self.signal_number is not None:
            return 128 + self.signal_number
        if self.outcome is RunOutcome.TIMEOUT:
            return 124
        if self.outcome in {
            RunOutcome.OUTPUT_LIMIT,
            RunOutcome.GPU_ABORT,
            RunOutcome.TELEMETRY_ERROR,
        }:
            return 125
        return 1

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome.value,
            "child_returncode": self.child_returncode,
            "record_path": str(self.record_path),
            "checkpoint_path": str(self.checkpoint_path),
            "stdout_path": str(self.stdout_path),
            "stderr_path": str(self.stderr_path),
            "signal_number": self.signal_number,
            "exit_code": self.exit_code,
        }


@dataclass
class _TelemetrySummary:
    count: int = 0
    minimum_temperature_c: int | None = None
    maximum_temperature_c: int | None = None
    maximum_memory_used_bytes: int = 0
    maximum_utilization_percent: int = 0
    maximum_power_watts: float = 0.0
    pause_count: int = 0
    last: NvidiaSnapshot | None = None

    def add(self, snapshot: NvidiaSnapshot) -> None:
        self.count += 1
        self.minimum_temperature_c = (
            snapshot.temperature_c
            if self.minimum_temperature_c is None
            else min(self.minimum_temperature_c, snapshot.temperature_c)
        )
        self.maximum_temperature_c = (
            snapshot.temperature_c
            if self.maximum_temperature_c is None
            else max(self.maximum_temperature_c, snapshot.temperature_c)
        )
        self.maximum_memory_used_bytes = max(
            self.maximum_memory_used_bytes, snapshot.memory_used_bytes
        )
        self.maximum_utilization_percent = max(
            self.maximum_utilization_percent,
            snapshot.gpu_utilization_percent,
        )
        self.maximum_power_watts = max(self.maximum_power_watts, snapshot.power_watts)
        self.last = snapshot

    def to_jsonable(self, *, enabled: bool) -> dict[str, Any]:
        if not enabled:
            return {
                "enabled": False,
                "queried": False,
                "note": "GPU state was not queried and no GPU setting was changed.",
            }
        last = None
        if self.last is not None:
            last = {
                "temperature_c": self.last.temperature_c,
                "gpu_utilization_percent": self.last.gpu_utilization_percent,
                "memory_used_bytes": self.last.memory_used_bytes,
                "memory_total_bytes": self.last.memory_total_bytes,
                "power_watts": self.last.power_watts,
            }
        return {
            "enabled": True,
            "query_count": self.count,
            "minimum_temperature_c": self.minimum_temperature_c,
            "maximum_temperature_c": self.maximum_temperature_c,
            "maximum_memory_used_bytes": self.maximum_memory_used_bytes,
            "maximum_utilization_percent": self.maximum_utilization_percent,
            "maximum_power_watts": self.maximum_power_watts,
            "pause_count": self.pause_count,
            "last_snapshot": last,
            "read_only": True,
            "hardware_settings_changed": False,
        }


class _Capture:
    """A same-directory temporary output file with an incremental SHA-256."""

    def __init__(self, destination: Path, cap_bytes: int) -> None:
        self.destination = destination
        self.cap_bytes = cap_bytes
        self.byte_count = 0
        self.hasher = hashlib.sha256()
        self._published = False
        self.stream_eof_observed = False
        self.truncated_by_cap = False
        destination.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{destination.name}.", suffix=".tmp", dir=destination.parent
        )
        self.temporary_path = Path(temporary_name)
        self.stream: BinaryIO = os.fdopen(descriptor, "wb", buffering=0)

    @property
    def remaining(self) -> int:
        return self.cap_bytes - self.byte_count

    def consume(self, chunk: bytes) -> bool:
        """Write at most the remaining cap; return true if bytes overflowed it."""
        accepted = chunk[: self.remaining]
        if accepted:
            self.stream.write(accepted)
            self.hasher.update(accepted)
            self.byte_count += len(accepted)
        overflowed = len(chunk) > len(accepted)
        self.truncated_by_cap = self.truncated_by_cap or overflowed
        return overflowed

    def flush_durable(self) -> None:
        if self.stream.closed:
            return
        self.stream.flush()
        os.fsync(self.stream.fileno())

    def snapshot(self, *, finalized: bool) -> dict[str, Any]:
        return {
            "bytes_captured": self.byte_count,
            "cap_bytes": self.cap_bytes,
            "sha256_captured": self.hasher.copy().hexdigest(),
            "capture_finalized": finalized,
            "child_stream_eof_observed": self.stream_eof_observed,
            "truncated_by_cap": self.truncated_by_cap,
            "destination": str(self.destination.resolve()),
        }

    def publish(self) -> None:
        if self._published:
            return
        self.flush_durable()
        self.stream.close()
        os.replace(self.temporary_path, self.destination)
        self._published = True

    def cleanup(self) -> None:
        if not self.stream.closed:
            self.stream.close()
        if not self._published:
            try:
                self.temporary_path.unlink()
            except FileNotFoundError:
                pass


def classify_telemetry(
    snapshot: NvidiaSnapshot, limits: ResourceLimits
) -> TelemetryAction:
    """Convert the shared telemetry policy into a process-only runner action."""
    if (
        not math.isfinite(snapshot.power_watts)
        or snapshot.temperature_c < 0
        or snapshot.gpu_utilization_percent < 0
        or snapshot.memory_used_bytes < 0
        or snapshot.memory_total_bytes <= 0
        or snapshot.memory_used_bytes > snapshot.memory_total_bytes
    ):
        raise ValueError("NVIDIA telemetry contains a nonfinite or negative value")
    if snapshot.memory_used_bytes > limits.gpu_memory_bytes:
        return TelemetryAction.ABORT_GPU_MEMORY
    if snapshot.temperature_c >= limits.gpu_abort_temperature_c:
        return TelemetryAction.ABORT_TEMPERATURE
    if snapshot.temperature_c >= limits.gpu_pause_temperature_c:
        return TelemetryAction.PAUSE
    return TelemetryAction.CONTINUE


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="microseconds").replace(
        "+00:00", "Z"
    )


def _canonical_json_sha256(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while chunk := stream.read(READ_CHUNK_BYTES):
            digest.update(chunk)
    return digest.hexdigest()


def _artifacts(config: RunnerConfiguration) -> RunArtifacts:
    base = config.run_directory.expanduser().resolve() / config.experiment_id
    return RunArtifacts(
        stdout=Path(f"{base}.stdout.data"),
        stderr=Path(f"{base}.stderr.log"),
        checkpoint=Path(f"{base}.checkpoint.state"),
        record=Path(f"{base}.record.json"),
    )


def _controlled_run_root() -> Path:
    repository = REPOSITORY_ROOT.resolve(strict=True)
    current = repository
    for part in CONTROLLED_RUN_RELATIVE_ROOT.parts:
        current = current / part
        if current.is_symlink():
            raise RunnerConfigurationError(
                "controlled artifact root must not contain a symlink"
            )
    return current


def _require_within_repository(path_text: str, *, option: str) -> None:
    path = Path(path_text).expanduser()
    candidate = path if path.is_absolute() else REPOSITORY_ROOT / path
    try:
        candidate.resolve().relative_to(REPOSITORY_ROOT.resolve(strict=True))
    except ValueError as exc:
        raise RunnerConfigurationError(
            f"{option} must resolve inside the Rule 30 repository"
        ) from exc


def _validate_child_path_arguments(
    experiment: str, child_args: Sequence[str]
) -> None:
    read_options = _READ_PATH_OPTIONS.get(experiment, frozenset())
    index = 0
    while index < len(child_args):
        argument = child_args[index]
        option, separator, inline_value = argument.partition("=")
        guarded_options = read_options | _FORBIDDEN_SIDE_OUTPUT_OPTIONS
        if (
            option.startswith("--")
            and option not in guarded_options
            and any(full_option.startswith(option) for full_option in guarded_options)
        ):
            raise RunnerConfigurationError(
                f"abbreviated path-bearing child option {option!r} is forbidden; "
                "use the complete option name"
            )
        if option in _FORBIDDEN_SIDE_OUTPUT_OPTIONS:
            raise RunnerConfigurationError(
                f"{option} is disabled in the controlled runner because generic "
                "side-output files are outside its capture budget"
            )
        if option in read_options:
            if separator:
                value = inline_value
            else:
                index += 1
                if index >= len(child_args):
                    raise RunnerConfigurationError(f"{option} requires a path value")
                value = child_args[index]
            if not value:
                raise RunnerConfigurationError(f"{option} requires a nonempty path")
            _require_within_repository(value, option=option)
        index += 1


def _resolve_experiment_script(
    experiment: str,
) -> tuple[ExperimentSpec, Path]:
    try:
        spec = EXPERIMENT_ALLOWLIST[experiment]
    except KeyError as exc:
        names = ", ".join(sorted(EXPERIMENT_ALLOWLIST))
        raise RunnerConfigurationError(
            f"experiment {experiment!r} is not allowlisted; choose one of: {names}"
        ) from exc
    relative = spec.relative_path
    if relative.is_absolute() or ".." in relative.parts:
        raise RunnerConfigurationError("allowlisted script path must remain repository-relative")
    root = REPOSITORY_ROOT.resolve(strict=True)
    candidate = root / relative
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise RunnerConfigurationError(
                f"allowlisted script path contains a symlink: {relative}"
            )
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (FileNotFoundError, ValueError) as exc:
        raise RunnerConfigurationError(
            f"allowlisted script does not resolve inside the repository: {relative}"
        ) from exc
    if not resolved.is_file() or resolved.suffix != ".py":
        raise RunnerConfigurationError(
            f"allowlisted experiment is not a regular Python file: {relative}"
        )
    return spec, resolved


def _logical_argv_hash(experiment: str, child_args: Sequence[str]) -> str:
    return _canonical_json_sha256(
        {"experiment": experiment, "child_argv": list(child_args)}
    )


def _validate_configuration(
    config: RunnerConfiguration,
) -> tuple[ExperimentSpec, Path, RunArtifacts, str]:
    if sys.platform != "linux":
        raise RunnerConfigurationError(
            "the controlled runner requires Linux/WSL for RLIMIT_AS enforcement"
        )
    if _EXPERIMENT_ID.fullmatch(config.experiment_id) is None:
        raise RunnerConfigurationError(
            "experiment_id must use 1-128 ASCII letters, digits, dots, underscores, or hyphens"
        )
    if len(config.child_args) > MAX_CHILD_ARGUMENTS:
        raise RunnerConfigurationError(
            f"at most {MAX_CHILD_ARGUMENTS} child arguments are allowed"
        )
    argument_bytes = 0
    for argument in config.child_args:
        if not isinstance(argument, str):
            raise RunnerConfigurationError("every child argument must be a string")
        if "\0" in argument:
            raise RunnerConfigurationError("child arguments may not contain NUL bytes")
        argument_bytes += len(argument.encode("utf-8"))
    if argument_bytes > MAX_CHILD_ARGUMENT_BYTES:
        raise RunnerConfigurationError(
            f"child arguments exceed the {MAX_CHILD_ARGUMENT_BYTES}-byte cap"
        )
    if (
        not math.isfinite(config.limits.wall_seconds)
        or config.limits.wall_seconds <= 0
        or config.limits.ram_bytes <= 0
    ):
        raise RunnerConfigurationError("wall and RAM limits must be positive")
    if (
        not math.isfinite(config.limits.progress_seconds)
        or config.limits.progress_seconds <= 0
    ):
        raise RunnerConfigurationError("progress interval must be positive")
    if config.limits.cpu_workers <= 0:
        raise RunnerConfigurationError("cpu_workers must be positive")
    if not (
        0 < config.limits.gpu_pause_temperature_c
        < config.limits.gpu_abort_temperature_c
    ):
        raise RunnerConfigurationError(
            "GPU pause temperature must be positive and below abort temperature"
        )
    if not 0 <= config.stdout_cap_bytes <= MAX_STDOUT_CAP_BYTES:
        raise RunnerConfigurationError(
            f"stdout cap must be between 0 and {MAX_STDOUT_CAP_BYTES} bytes"
        )
    if not 0 <= config.stderr_cap_bytes <= MAX_STDERR_CAP_BYTES:
        raise RunnerConfigurationError(
            f"stderr cap must be between 0 and {MAX_STDERR_CAP_BYTES} bytes"
        )
    if (
        not math.isfinite(config.telemetry_seconds)
        or not math.isfinite(config.termination_grace_seconds)
        or config.telemetry_seconds <= 0
        or config.termination_grace_seconds <= 0
    ):
        raise RunnerConfigurationError(
            "telemetry and termination-grace intervals must be positive"
        )
    spec, script = _resolve_experiment_script(config.experiment)
    _validate_child_path_arguments(config.experiment, config.child_args)
    if spec.default_status not in ALLOWED_STATUSES:
        raise RunnerConfigurationError(
            f"allowlist has invalid default status {spec.default_status!r}"
        )
    run_root = _controlled_run_root()
    run_directory = config.run_directory.expanduser().resolve()
    try:
        run_directory.relative_to(run_root)
    except ValueError as exc:
        raise RunnerConfigurationError(
            f"run_directory must resolve under the controlled artifact root {run_root}"
        ) from exc
    artifacts = _artifacts(config)
    if len({artifact.resolve() for artifact in artifacts.__dict__.values()}) != 4:
        raise RunnerConfigurationError("run artifact paths must be distinct")
    planned_bytes = (
        config.stdout_cap_bytes
        + config.stderr_cap_bytes
        + RECORD_RESERVE_BYTES
        + CHECKPOINT_RESERVE_BYTES
    )
    ensure_output_budget(planned_bytes, config.limits)
    ensure_disk_budget(artifacts.record, planned_bytes, config.limits)
    existing = [path for path in artifacts.__dict__.values() if path.exists()]
    if config.resume_from is None and not config.overwrite and existing:
        raise RunnerConfigurationError(
            "refusing to replace existing run artifacts without --overwrite: "
            + ", ".join(str(path) for path in existing)
        )
    if config.resume_from is not None:
        try:
            resume_path = config.resume_from.expanduser().resolve(strict=True)
        except FileNotFoundError as exc:
            raise RunnerConfigurationError("resume checkpoint does not exist") from exc
        if resume_path != artifacts.checkpoint.resolve():
            raise RunnerConfigurationError(
                "resume checkpoint must be the checkpoint for this exact run "
                "directory and experiment_id"
            )
    return spec, script, artifacts, _logical_argv_hash(
        config.experiment, config.child_args
    )


def _load_resume_checkpoint(
    config: RunnerConfiguration,
    logical_argv_sha256: str,
    expected_argv: Sequence[str],
    artifacts: RunArtifacts,
) -> dict[str, Any] | None:
    if config.resume_from is None:
        return None
    path = config.resume_from.resolve(strict=True)
    if path.stat().st_size > CHECKPOINT_RESERVE_BYTES:
        raise RunnerConfigurationError("resume checkpoint exceeds its size reserve")
    try:
        raw = path.read_bytes()
        checkpoint = json.loads(raw)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RunnerConfigurationError("resume checkpoint is not valid JSON") from exc
    if not isinstance(checkpoint, dict) or checkpoint.get("kind") != CHECKPOINT_KIND:
        raise RunnerConfigurationError("resume checkpoint has the wrong schema kind")
    if checkpoint.get("schema_version") != RUNNER_SCHEMA_VERSION:
        raise RunnerConfigurationError("resume checkpoint has the wrong schema version")
    if checkpoint.get("complete") is not False:
        raise RunnerConfigurationError("a completed run does not need resuming")
    if checkpoint.get("experiment") != config.experiment:
        raise RunnerConfigurationError("resume checkpoint experiment does not match")
    if checkpoint.get("experiment_id") != config.experiment_id:
        raise RunnerConfigurationError("resume checkpoint experiment_id does not match")
    if checkpoint.get("logical_argv_sha256") != logical_argv_sha256:
        raise RunnerConfigurationError("resume checkpoint child argv does not match")
    if checkpoint.get("child_argv") != list(expected_argv):
        raise RunnerConfigurationError("resume checkpoint full child argv does not match")
    if checkpoint.get("child_continuation_supported") is not False:
        raise RunnerConfigurationError(
            "checkpoint does not declare the required restart-only semantics"
        )
    attempt = checkpoint.get("attempt")
    if isinstance(attempt, bool) or not isinstance(attempt, int) or attempt <= 0:
        raise RunnerConfigurationError("resume checkpoint attempt must be positive")
    state = checkpoint.get("state")
    if not isinstance(state, str) or not state.strip():
        raise RunnerConfigurationError("resume checkpoint state must be nonempty")
    for name, destination in (
        ("stdout", artifacts.stdout),
        ("stderr", artifacts.stderr),
    ):
        capture = checkpoint.get(name)
        if not isinstance(capture, dict):
            raise RunnerConfigurationError(
                f"resume checkpoint {name} capture metadata is missing"
            )
        try:
            recorded_destination = Path(capture["destination"]).resolve()
        except (KeyError, TypeError) as exc:
            raise RunnerConfigurationError(
                f"resume checkpoint {name} destination is invalid"
            ) from exc
        if recorded_destination != destination.resolve():
            raise RunnerConfigurationError(
                f"resume checkpoint {name} destination does not match this run"
            )
    return {
        "checkpoint_path": str(path),
        "checkpoint_sha256": hashlib.sha256(raw).hexdigest(),
        "prior_attempt": attempt,
        "prior_state": state,
        "mode": "validated-restart-from-beginning",
        "mid_script_continuation": False,
    }


def _make_child_preexec(ram_bytes: int) -> Any:
    """Return the Linux child-only address-space setup hook."""

    def apply_limit() -> None:
        apply_address_space_limit(ram_bytes)

    return apply_limit


def _child_environment(limits: ResourceLimits) -> dict[str, str]:
    environment = {
        "PATH": "/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/wsl/lib",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONNOUSERSITE": "1",
    }
    for name in ("HOME", "TMPDIR", "TZ"):
        value = os.environ.get(name)
        if value:
            environment[name] = value
    worker_count = str(limits.cpu_workers)
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "RAYON_NUM_THREADS",
    ):
        environment[name] = worker_count
    environment["PYTHONHASHSEED"] = "0"
    return environment


def _emit_progress(
    *,
    config: RunnerConfiguration,
    state: str,
    elapsed_seconds: float,
    stdout_capture: _Capture,
    stderr_capture: _Capture,
    child_pid: int | None,
    telemetry: _TelemetrySummary,
) -> None:
    line = {
        "type": "rule30-controlled-runner-progress",
        "schema_version": RUNNER_SCHEMA_VERSION,
        "experiment_id": config.experiment_id,
        "experiment": config.experiment,
        "state": state,
        "elapsed_seconds": round(elapsed_seconds, 6),
        "child_pid": child_pid,
        "stdout_bytes": stdout_capture.byte_count,
        "stderr_bytes": stderr_capture.byte_count,
        "telemetry_samples": telemetry.count,
        "timestamp_utc": _utc_now(),
    }
    print(
        json.dumps(line, sort_keys=True, separators=(",", ":"), allow_nan=False),
        file=sys.stderr,
        flush=True,
    )


def _checkpoint_payload(
    *,
    config: RunnerConfiguration,
    state: str,
    attempt: int,
    elapsed_seconds: float,
    argv: Sequence[str],
    logical_argv_sha256: str,
    stdout_capture: _Capture,
    stderr_capture: _Capture,
    captures_complete: bool,
    child_pid: int | None,
    child_returncode: int | None,
    complete: bool,
    reason: str | None,
    resumed_from: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "kind": CHECKPOINT_KIND,
        "schema_version": RUNNER_SCHEMA_VERSION,
        "experiment_id": config.experiment_id,
        "experiment": config.experiment,
        "state": state,
        "attempt": attempt,
        "timestamp_utc": _utc_now(),
        "elapsed_seconds": elapsed_seconds,
        "child_pid": child_pid,
        "child_returncode": child_returncode,
        "child_argv": list(argv),
        "logical_argv_sha256": logical_argv_sha256,
        "stdout": stdout_capture.snapshot(finalized=captures_complete),
        "stderr": stderr_capture.snapshot(finalized=captures_complete),
        "complete": complete,
        "reason": reason,
        "child_continuation_supported": False,
        "resume": {
            "runner_checkpoint_supported": True,
            "mid_script_continuation_supported": False,
            "mode": "restart-child-from-beginning",
            "restart_required": not complete,
            "statement": (
                "This checkpoint can validate a new attempt, but the child must "
                "restart from its first instruction. No completed child work is "
                "claimed reusable."
            ),
        },
        "resumed_from": resumed_from,
    }


def _write_checkpoint(
    path: Path,
    *,
    config: RunnerConfiguration,
    state: str,
    attempt: int,
    elapsed_seconds: float,
    argv: Sequence[str],
    logical_argv_sha256: str,
    stdout_capture: _Capture,
    stderr_capture: _Capture,
    captures_complete: bool,
    child_pid: int | None,
    child_returncode: int | None,
    complete: bool,
    reason: str | None,
    resumed_from: dict[str, Any] | None,
) -> None:
    stdout_capture.flush_durable()
    stderr_capture.flush_durable()
    atomic_write_checkpoint(
        path,
        _checkpoint_payload(
            config=config,
            state=state,
            attempt=attempt,
            elapsed_seconds=elapsed_seconds,
            argv=argv,
            logical_argv_sha256=logical_argv_sha256,
            stdout_capture=stdout_capture,
            stderr_capture=stderr_capture,
            captures_complete=captures_complete,
            child_pid=child_pid,
            child_returncode=child_returncode,
            complete=complete,
            reason=reason,
            resumed_from=resumed_from,
        ),
    )


def _signal_process_group(process: subprocess.Popen[bytes], signal_number: int) -> None:
    try:
        os.killpg(process.pid, signal_number)
    except ProcessLookupError:
        return


def _close_pipe(
    selector: selectors.BaseSelector,
    active: dict[int, tuple[str, BinaryIO, _Capture]],
    descriptor: int,
    *,
    eof_observed: bool,
) -> None:
    _name, pipe, capture = active.pop(descriptor)
    capture.stream_eof_observed = capture.stream_eof_observed or eof_observed
    try:
        selector.unregister(descriptor)
    except KeyError:
        pass
    pipe.close()


def _parse_child_json(
    path: Path, spec: ExperimentSpec
) -> tuple[dict[str, Any] | None, str | None, str | None]:
    try:
        with path.open("r", encoding="utf-8") as stream:
            outer = json.load(stream)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, None, f"child stdout is not one complete UTF-8 JSON value: {exc}"
    if not isinstance(outer, dict):
        return None, None, "child JSON must be an object"
    scientific = outer.get("scientific_payload", outer)
    if not isinstance(scientific, dict):
        return None, None, "scientific_payload must be an object when present"
    if scientific.get("schema_version") != 1:
        return None, None, "child scientific payload must use schema_version 1"
    question = scientific.get("question")
    if question != spec.question:
        return None, None, (
            f"child question {question!r} does not match allowlist {spec.question!r}"
        )
    status = scientific.get("status")
    if status in {"partial-proof", "rigorous-proof"}:
        return None, None, (
            "computational experiment children may not emit a proof status; "
            "proof records require a separate reviewed proof workflow"
        )
    if status not in {spec.default_status, "inconclusive"}:
        return None, None, f"child status {status!r} is not allowed"
    hypothesis = scientific.get("hypothesis")
    if hypothesis is not None and (
        not isinstance(hypothesis, str) or not hypothesis.strip()
    ):
        return None, None, "child hypothesis must be omitted or a nonempty string"
    interpretation = scientific.get("interpretation")
    if not isinstance(interpretation, str) or not interpretation.strip():
        return None, None, "child interpretation must be a nonempty string"
    if not isinstance(scientific.get("parameters"), dict):
        return None, None, "child parameters must be an object"
    limitations = scientific.get("limitations")
    if not isinstance(limitations, list) or not all(
        isinstance(item, str) and item.strip() for item in limitations
    ):
        return None, None, "child limitations must be a list of nonempty strings"
    result_payload = next(
        (
            scientific[field]
            for field in (
                "result_summary",
                "results",
                "subresults",
                "pure_period_search",
            )
            if field in scientific
        ),
        None,
    )
    if not isinstance(result_payload, (dict, list)) or not result_payload:
        return None, None, "child JSON does not contain a recognized result payload"
    canonical_hash = _canonical_json_sha256(outer)
    metadata: dict[str, Any] = {
        "schema_version": scientific.get("schema_version"),
        "experiment_id": scientific.get("experiment_id"),
        "question": question,
        "hypothesis": scientific.get("hypothesis"),
        "backend": scientific.get("backend"),
        "status": status,
        "proof_scope": scientific.get("proof_scope"),
        "interpretation": scientific.get("interpretation"),
        "limitations": scientific.get("limitations"),
        "top_level_keys": sorted(outer),
        "scientific_payload_keys": sorted(scientific),
    }
    return metadata, canonical_hash, None


def _read_cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unavailable"


def _read_memory_total_bytes() -> int | None:
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("MemTotal:"):
                return int(line.split()[1]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    return None


def _git_commit(repository_root: Path) -> str:
    git_environment = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C",
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
    }
    completed = subprocess.run(
        ("/usr/bin/git", "-C", str(repository_root), "rev-parse", "HEAD"),
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
        shell=False,
        env=git_environment,
    )
    commit = completed.stdout.strip()
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise RunnerConfigurationError("git rev-parse did not return a full commit")
    return commit


def _git_worktree_status(repository_root: Path) -> str:
    git_environment = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C",
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": "/dev/null",
    }
    completed = subprocess.run(
        (
            "/usr/bin/git",
            "-C",
            str(repository_root),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ),
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
        shell=False,
        env=git_environment,
    )
    return completed.stdout


def _deduplicate_strings(values: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        cleaned = value.strip()
        if cleaned and cleaned not in seen:
            seen.add(cleaned)
            result.append(cleaned)
    return result


def _build_record(
    *,
    config: RunnerConfiguration,
    spec: ExperimentSpec,
    script: Path,
    artifacts: RunArtifacts,
    outcome: RunOutcome,
    reason: str | None,
    started_utc: str,
    runtime_seconds: float,
    argv: Sequence[str],
    logical_argv_sha256: str,
    stdout_capture: _Capture,
    stderr_capture: _Capture,
    child_returncode: int | None,
    child_metadata: dict[str, Any] | None,
    canonical_child_json_sha256: str | None,
    child_script_sha256_before: str,
    child_script_sha256_after: str,
    runner_module_sha256: str,
    runner_module_sha256_after: str,
    git_commit: str,
    git_commit_after: str,
    repository_clean_after_run: bool,
    telemetry: _TelemetrySummary,
    resumed_from: dict[str, Any] | None,
) -> dict[str, Any]:
    child_status = None if child_metadata is None else child_metadata.get("status")
    successful = outcome is RunOutcome.SUCCESS
    status = (
        child_status
        if successful and child_status in ALLOWED_STATUSES
        else spec.default_status if successful else "inconclusive"
    )
    child_hypothesis = (
        None if child_metadata is None else child_metadata.get("hypothesis")
    )
    hypothesis = (
        child_hypothesis
        if isinstance(child_hypothesis, str) and child_hypothesis.strip()
        else spec.hypothesis
    )
    child_proof_scope = (
        None if child_metadata is None else child_metadata.get("proof_scope")
    )
    proof_scope = (
        child_proof_scope
        if successful
        and isinstance(child_proof_scope, str)
        and child_proof_scope.strip()
        else (
            spec.proof_scope
            if successful
            else (
                "No scientific claim: the controlled run did not complete "
                "successfully."
            )
        )
    )
    child_backend = None if child_metadata is None else child_metadata.get("backend")
    backend = (
        f"controlled-runner:{child_backend}"
        if isinstance(child_backend, str) and child_backend.strip()
        else "controlled-runner:python-child"
    )
    child_limitations = (
        child_metadata.get("limitations", []) if child_metadata is not None else []
    )
    if not isinstance(child_limitations, list) or not all(
        isinstance(item, str) for item in child_limitations
    ):
        child_limitations = []
    limitations = _deduplicate_strings(
        [
            *spec.limitations,
            *child_limitations,
            "No finite computation in this run proves an infinite Rule 30 statement.",
            (
                "The checkpoint records runner capture state only; this child "
                "does not support mid-script continuation and resume restarts it "
                "from the beginning."
            ),
            (
                "NVIDIA telemetry, when enabled, is global device telemetry and "
                "is not attributed exclusively to this child."
            ),
        ]
    )
    result_hashes = {
        "stdout_sha256": stdout_capture.hasher.hexdigest(),
        "stderr_sha256": stderr_capture.hasher.hexdigest(),
        "logical_argv_sha256": logical_argv_sha256,
        "child_script_sha256_before": child_script_sha256_before,
        "child_script_sha256_after": child_script_sha256_after,
        "runner_module_sha256": runner_module_sha256,
        "runner_module_sha256_after": runner_module_sha256_after,
    }
    if canonical_child_json_sha256 is not None:
        result_hashes["canonical_child_json_sha256"] = canonical_child_json_sha256
    interpretation = (
        "The allowlisted local child completed successfully; captured bytes and "
        "the parsed finite-scope JSON are identified by deterministic SHA-256 hashes."
        if successful
        else f"The controlled attempt ended as {outcome.value}; no scientific conclusion is drawn."
    )
    if reason:
        interpretation += f" Runner reason: {reason}"
    hardware = {
        "execution_scope": "this local WSL/Linux instance only",
        "hostname": platform.node(),
        "machine": platform.machine(),
        "kernel": platform.release(),
        "cpu_model": _read_cpu_model(),
        "logical_cpu_count": os.cpu_count(),
        "linux_memory_total_bytes": _read_memory_total_bytes(),
        "gpu_telemetry": telemetry.to_jsonable(enabled=config.telemetry_enabled),
        "remote_compute_used": False,
        "hardware_settings_changed": False,
    }
    return {
        "experiment_id": config.experiment_id,
        "timestamp_utc": started_utc,
        "git_commit": git_commit,
        "question": spec.question,
        "hypothesis": hypothesis,
        "backend": backend,
        "parameters": {
            "allowlisted_experiment": config.experiment,
            "child_argv": list(argv),
            "child_arguments": list(config.child_args),
            "resource_limits": config.limits.to_jsonable(),
            "stdout_cap_bytes": config.stdout_cap_bytes,
            "stderr_cap_bytes": config.stderr_cap_bytes,
            "telemetry_enabled": config.telemetry_enabled,
            "telemetry_seconds": config.telemetry_seconds,
            "termination_grace_seconds": config.termination_grace_seconds,
            "execution_policy": {
                "local_only": True,
                "shell": False,
                "stdin": "devnull",
                "linux_address_space_limit_applied_in_child": True,
                "worker_environment_limit": config.limits.cpu_workers,
            },
            "resume": resumed_from,
            "resume_semantics": {
                "child_continuation_supported": False,
                "mode": "restart-child-from-beginning",
            },
        },
        "hardware": hardware,
        "software": {
            "runner": "rule30lab.controlled_runner",
            "runner_schema_version": RUNNER_SCHEMA_VERSION,
            "python_version": platform.python_version(),
            "python_implementation": platform.python_implementation(),
            "python_executable": sys.executable,
            "child_script": str(script.relative_to(REPOSITORY_ROOT.resolve())),
            "child_script_sha256_before": child_script_sha256_before,
            "child_script_sha256_after": child_script_sha256_after,
            "child_script_unchanged_during_run": (
                child_script_sha256_before == child_script_sha256_after
            ),
            "runner_module_sha256": runner_module_sha256,
            "runner_module_sha256_after": runner_module_sha256_after,
            "runner_module_unchanged_during_run": (
                runner_module_sha256 == runner_module_sha256_after
            ),
            "git_commit": git_commit,
            "git_commit_after": git_commit_after,
            "git_commit_unchanged_during_run": git_commit == git_commit_after,
            "repository_clean_before_run": True,
            "repository_clean_after_run": repository_clean_after_run,
            "provenance_policy": (
                "all tracked and non-ignored untracked Git worktree entries "
                "were required to be clean before the child was launched"
            ),
        },
        "runtime_seconds": runtime_seconds,
        "result_hashes": result_hashes,
        "result_summary": {
            "outcome": outcome.value,
            "reason": reason,
            "child_returncode": child_returncode,
            "stdout": stdout_capture.snapshot(finalized=True),
            "stderr": stderr_capture.snapshot(finalized=True),
            "child_json_valid": child_metadata is not None,
            "child_metadata": child_metadata,
            "artifacts": {
                "stdout": str(artifacts.stdout.resolve()),
                "stderr": str(artifacts.stderr.resolve()),
                "checkpoint": str(artifacts.checkpoint.resolve()),
                "record": str(artifacts.record.resolve()),
            },
        },
        "interpretation": interpretation,
        "status": status,
        "proof_scope": proof_scope,
        "limitations": limitations,
    }


def run_controlled_experiment(config: RunnerConfiguration) -> RunResult:
    """Execute one allowlisted child and atomically publish all run artifacts."""
    spec, script, artifacts, logical_argv_sha256 = _validate_configuration(config)
    argv = (sys.executable, "-I", str(script), *config.child_args)
    resumed_from = _load_resume_checkpoint(
        config, logical_argv_sha256, argv, artifacts
    )
    attempt = 1 if resumed_from is None else resumed_from["prior_attempt"] + 1
    artifacts.record.parent.mkdir(parents=True, exist_ok=True)
    git_commit = _git_commit(REPOSITORY_ROOT)
    worktree_status = _git_worktree_status(REPOSITORY_ROOT)
    if worktree_status:
        raise RunnerConfigurationError(
            "controlled scientific records require a clean Git worktree; "
            "commit or remove every tracked and non-ignored untracked change "
            "before running"
        )
    child_script_sha256_before = _file_sha256(script)
    runner_module_sha256 = _file_sha256(Path(__file__).resolve())
    started_utc = _utc_now()
    started_monotonic = time.monotonic()
    stdout_capture = _Capture(artifacts.stdout, config.stdout_cap_bytes)
    stderr_capture = _Capture(artifacts.stderr, config.stderr_cap_bytes)
    telemetry = _TelemetrySummary()
    process: subprocess.Popen[bytes] | None = None
    selector: selectors.BaseSelector | None = None
    active: dict[int, tuple[str, BinaryIO, _Capture]] = {}
    outcome: RunOutcome | None = None
    reason: str | None = None
    signal_number: int | None = None
    paused = False
    termination_started: float | None = None
    kill_sent = False
    next_progress = started_monotonic
    next_telemetry = started_monotonic

    try:
        with GracefulInterruption() as interruption:
            try:
                process = subprocess.Popen(
                    argv,
                    cwd=REPOSITORY_ROOT,
                    env=_child_environment(config.limits),
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0,
                    close_fds=True,
                    start_new_session=True,
                    preexec_fn=_make_child_preexec(config.limits.ram_bytes),
                    shell=False,
                )
            except (OSError, subprocess.SubprocessError) as exc:
                outcome = RunOutcome.SPAWN_ERROR
                reason = f"child spawn failed: {type(exc).__name__}: {exc}"

            if process is not None:
                assert process.stdout is not None
                assert process.stderr is not None
                selector = selectors.DefaultSelector()
                for name, pipe, capture in (
                    ("stdout", process.stdout, stdout_capture),
                    ("stderr", process.stderr, stderr_capture),
                ):
                    descriptor = pipe.fileno()
                    os.set_blocking(descriptor, False)
                    active[descriptor] = (name, pipe, capture)
                    selector.register(descriptor, selectors.EVENT_READ)

                while active or process.poll() is None:
                    now = time.monotonic()
                    elapsed = now - started_monotonic

                    if outcome is None and interruption.requested:
                        outcome = RunOutcome.INTERRUPTED
                        signal_number = interruption.signal_number
                        reason = (
                            "parent received "
                            + (
                                signal.Signals(signal_number).name
                                if signal_number is not None
                                else "an interruption request"
                            )
                        )

                    if outcome is None:
                        try:
                            check_wall_time(started_monotonic, config.limits)
                        except ResourceLimitExceeded as exc:
                            outcome = RunOutcome.TIMEOUT
                            reason = str(exc)

                    if (
                        outcome is None
                        and config.telemetry_enabled
                        and now >= next_telemetry
                    ):
                        next_telemetry = now + config.telemetry_seconds
                        try:
                            snapshot = query_nvidia_snapshot(
                                executable="/usr/lib/wsl/lib/nvidia-smi"
                            )
                            telemetry.add(snapshot)
                            action = classify_telemetry(snapshot, config.limits)
                        except Exception as exc:  # fixed read-only probe; fail closed
                            outcome = RunOutcome.TELEMETRY_ERROR
                            reason = (
                                "read-only nvidia-smi telemetry failed: "
                                f"{type(exc).__name__}: {exc}"
                            )
                        else:
                            if action is TelemetryAction.PAUSE and not paused:
                                _signal_process_group(process, signal.SIGSTOP)
                                paused = True
                                telemetry.pause_count += 1
                            elif action is TelemetryAction.CONTINUE and paused:
                                _signal_process_group(process, signal.SIGCONT)
                                paused = False
                            elif action in {
                                TelemetryAction.ABORT_TEMPERATURE,
                                TelemetryAction.ABORT_GPU_MEMORY,
                            }:
                                outcome = RunOutcome.GPU_ABORT
                                reason = (
                                    "read-only telemetry policy selected "
                                    f"{action.value}; no hardware setting was changed"
                                )

                    state = "paused-thermal" if paused else "running"
                    if outcome is not None:
                        state = f"terminating-{outcome.value}"
                        if termination_started is None:
                            if paused:
                                _signal_process_group(process, signal.SIGCONT)
                                paused = False
                            _signal_process_group(process, signal.SIGTERM)
                            termination_started = now
                            _write_checkpoint(
                                artifacts.checkpoint,
                                config=config,
                                state=state,
                                attempt=attempt,
                                elapsed_seconds=elapsed,
                                argv=argv,
                                logical_argv_sha256=logical_argv_sha256,
                                stdout_capture=stdout_capture,
                                stderr_capture=stderr_capture,
                                captures_complete=False,
                                child_pid=process.pid,
                                child_returncode=process.poll(),
                                complete=False,
                                reason=reason,
                                resumed_from=resumed_from,
                            )
                        elif (
                            termination_started is not None
                            and not kill_sent
                            and now - termination_started
                            >= config.termination_grace_seconds
                        ):
                            _signal_process_group(process, signal.SIGKILL)
                            kill_sent = True
                        elif (
                            termination_started is not None
                            and kill_sent
                            and active
                            and now - termination_started
                            >= config.termination_grace_seconds
                            + POST_KILL_DRAIN_SECONDS
                        ):
                            reason = (
                                (reason + "; " if reason else "")
                                + "bounded pipe-drain interval expired after process-group kill"
                            )
                            assert selector is not None
                            for descriptor in list(active):
                                _close_pipe(
                                    selector,
                                    active,
                                    descriptor,
                                    eof_observed=False,
                                )

                    if now >= next_progress:
                        _emit_progress(
                            config=config,
                            state=state,
                            elapsed_seconds=elapsed,
                            stdout_capture=stdout_capture,
                            stderr_capture=stderr_capture,
                            child_pid=process.pid,
                            telemetry=telemetry,
                        )
                        _write_checkpoint(
                            artifacts.checkpoint,
                            config=config,
                            state=state,
                            attempt=attempt,
                            elapsed_seconds=elapsed,
                            argv=argv,
                            logical_argv_sha256=logical_argv_sha256,
                            stdout_capture=stdout_capture,
                            stderr_capture=stderr_capture,
                            captures_complete=False,
                            child_pid=process.pid,
                            child_returncode=process.poll(),
                            complete=False,
                            reason=reason,
                            resumed_from=resumed_from,
                        )
                        next_progress = now + config.limits.progress_seconds

                    select_timeout = 0.05
                    if paused and config.telemetry_enabled:
                        select_timeout = min(
                            select_timeout, max(0.0, next_telemetry - time.monotonic())
                        )
                    events = selector.select(select_timeout) if selector else []
                    for key, _mask in events:
                        descriptor = int(key.fd)
                        name, _pipe, capture = active[descriptor]
                        read_size = min(READ_CHUNK_BYTES, capture.remaining + 1)
                        try:
                            chunk = os.read(descriptor, max(1, read_size))
                        except BlockingIOError:
                            continue
                        if not chunk:
                            _close_pipe(
                                selector, active, descriptor, eof_observed=True
                            )
                            continue
                        overflowed = capture.consume(chunk)
                        if overflowed:
                            _close_pipe(
                                selector, active, descriptor, eof_observed=False
                            )
                            if outcome is None:
                                outcome = RunOutcome.OUTPUT_LIMIT
                                reason = (
                                    f"child {name} exceeded hard cap "
                                    f"{capture.cap_bytes} bytes"
                                )

                process.wait()

        if outcome is None:
            if process is None:
                outcome = RunOutcome.SPAWN_ERROR
                reason = reason or "child did not start"
            elif process.returncode != 0:
                outcome = RunOutcome.CHILD_ERROR
                reason = f"child exited with status {process.returncode}"

    except Exception as exc:
        outcome = RunOutcome.INTERNAL_ERROR
        reason = f"runner internal error: {type(exc).__name__}: {exc}"
        if process is not None:
            try:
                if paused:
                    _signal_process_group(process, signal.SIGCONT)
                _signal_process_group(process, signal.SIGKILL)
                if process.poll() is None:
                    process.wait(timeout=5)
            except (OSError, subprocess.SubprocessError):
                pass
    finally:
        if selector is not None:
            selector.close()
        for _name, pipe, _capture in list(active.values()):
            pipe.close()
        active.clear()

    try:
        stdout_capture.publish()
        stderr_capture.publish()
        child_metadata: dict[str, Any] | None = None
        canonical_child_json_sha256: str | None = None
        if outcome is None or outcome is RunOutcome.SUCCESS:
            child_metadata, canonical_child_json_sha256, parse_error = _parse_child_json(
                artifacts.stdout, spec
            )
            if parse_error is not None:
                outcome = RunOutcome.INVALID_OUTPUT
                reason = parse_error
            else:
                outcome = RunOutcome.SUCCESS
        runtime_seconds = time.monotonic() - started_monotonic
        assert outcome is not None
        child_script_sha256_after = _file_sha256(script)
        runner_module_sha256_after = _file_sha256(Path(__file__).resolve())
        git_commit_after = _git_commit(REPOSITORY_ROOT)
        repository_clean_after_run = not bool(
            _git_worktree_status(REPOSITORY_ROOT)
        )
        provenance_failures: list[str] = []
        if child_script_sha256_after != child_script_sha256_before:
            provenance_failures.append("allowlisted child script changed")
        if runner_module_sha256_after != runner_module_sha256:
            provenance_failures.append("controlled runner module changed")
        if git_commit_after != git_commit:
            provenance_failures.append("Git HEAD changed")
        if not repository_clean_after_run:
            provenance_failures.append("Git worktree became dirty")
        if provenance_failures:
            outcome = RunOutcome.INVALID_OUTPUT
            reason = (
                "exact code provenance is not stable: "
                + ", ".join(provenance_failures)
            )
        child_returncode = None if process is None else process.returncode
        terminal_state = "complete" if outcome is RunOutcome.SUCCESS else outcome.value
        _write_checkpoint(
            artifacts.checkpoint,
            config=config,
            state=terminal_state,
            attempt=attempt,
            elapsed_seconds=runtime_seconds,
            argv=argv,
            logical_argv_sha256=logical_argv_sha256,
            stdout_capture=stdout_capture,
            stderr_capture=stderr_capture,
            captures_complete=True,
            child_pid=None if process is None else process.pid,
            child_returncode=child_returncode,
            complete=outcome is RunOutcome.SUCCESS,
            reason=reason,
            resumed_from=resumed_from,
        )
        record = _build_record(
            config=config,
            spec=spec,
            script=script,
            artifacts=artifacts,
            outcome=outcome,
            reason=reason,
            started_utc=started_utc,
            runtime_seconds=runtime_seconds,
            argv=argv,
            logical_argv_sha256=logical_argv_sha256,
            stdout_capture=stdout_capture,
            stderr_capture=stderr_capture,
            child_returncode=child_returncode,
            child_metadata=child_metadata,
            canonical_child_json_sha256=canonical_child_json_sha256,
            child_script_sha256_before=child_script_sha256_before,
            child_script_sha256_after=child_script_sha256_after,
            runner_module_sha256=runner_module_sha256,
            runner_module_sha256_after=runner_module_sha256_after,
            git_commit=git_commit,
            git_commit_after=git_commit_after,
            repository_clean_after_run=repository_clean_after_run,
            telemetry=telemetry,
            resumed_from=resumed_from,
        )
        atomic_write_json(artifacts.record, record)
        _emit_progress(
            config=config,
            state=terminal_state,
            elapsed_seconds=runtime_seconds,
            stdout_capture=stdout_capture,
            stderr_capture=stderr_capture,
            child_pid=None,
            telemetry=telemetry,
        )
        return RunResult(
            outcome=outcome,
            child_returncode=child_returncode,
            record_path=artifacts.record,
            checkpoint_path=artifacts.checkpoint,
            stdout_path=artifacts.stdout,
            stderr_path=artifacts.stderr,
            signal_number=signal_number,
        )
    finally:
        stdout_capture.cleanup()
        stderr_capture.cleanup()


def _positive_float(text: str) -> float:
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive number") from exc
    if not math.isfinite(value) or not value > 0:
        raise argparse.ArgumentTypeError("expected a positive number")
    return value


def _positive_integer(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive integer") from exc
    if value <= 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def _nonnegative_integer(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a nonnegative integer") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative integer")
    return value


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m rule30lab.controlled_runner",
        description=(
            "Run one internal Rule 30 experiment locally with bounded streamed "
            "output, checkpoints, and a strict atomic result record. Put runner "
            "options before EXPERIMENT and child options after '--'."
        ),
    )
    parser.add_argument("--profile", choices=tuple(ResourceProfile), default="interactive")
    parser.add_argument(
        "--run-directory",
        type=Path,
        default=REPOSITORY_ROOT / "results" / "runs",
    )
    parser.add_argument("--experiment-id")
    parser.add_argument("--wall-seconds", type=_positive_float)
    parser.add_argument("--ram-mib", type=_positive_integer)
    parser.add_argument("--gpu-memory-mib", type=_positive_integer)
    parser.add_argument("--output-budget-mib", type=_positive_integer)
    parser.add_argument("--disk-reserve-mib", type=_nonnegative_integer)
    parser.add_argument("--progress-seconds", type=_positive_float)
    parser.add_argument("--cpu-workers", type=_positive_integer)
    parser.add_argument("--gpu-pause-temperature-c", type=_positive_integer)
    parser.add_argument("--gpu-abort-temperature-c", type=_positive_integer)
    parser.add_argument("--stdout-cap-mib", type=_nonnegative_integer)
    parser.add_argument("--stderr-cap-mib", type=_nonnegative_integer)
    parser.add_argument("--gpu-telemetry", action="store_true")
    parser.add_argument("--telemetry-seconds", type=_positive_float, default=5.0)
    parser.add_argument(
        "--termination-grace-seconds", type=_positive_float, default=3.0
    )
    parser.add_argument("--resume-from", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("experiment", choices=tuple(sorted(EXPERIMENT_ALLOWLIST)))
    parser.add_argument("child_args", nargs=argparse.REMAINDER)
    return parser


def _default_capture_caps(profile: ResourceProfile) -> tuple[int, int]:
    if profile is ResourceProfile.IDLE:
        return 64 * 1024**2, 16 * 1024**2
    return 16 * 1024**2, 4 * 1024**2


def _configuration_from_args(args: argparse.Namespace) -> RunnerConfiguration:
    profile = ResourceProfile(args.profile)
    limits = ResourceLimits.conservative(profile)
    replacements: dict[str, Any] = {}
    for argument_name, field_name in (
        ("wall_seconds", "wall_seconds"),
        ("progress_seconds", "progress_seconds"),
        ("cpu_workers", "cpu_workers"),
        ("gpu_pause_temperature_c", "gpu_pause_temperature_c"),
        ("gpu_abort_temperature_c", "gpu_abort_temperature_c"),
    ):
        value = getattr(args, argument_name)
        if value is not None:
            replacements[field_name] = value
    for argument_name, field_name in (
        ("ram_mib", "ram_bytes"),
        ("gpu_memory_mib", "gpu_memory_bytes"),
        ("output_budget_mib", "output_bytes"),
        ("disk_reserve_mib", "disk_reserve_bytes"),
    ):
        value = getattr(args, argument_name)
        if value is not None:
            replacements[field_name] = value * 1024**2
    limits = replace(limits, **replacements)
    stdout_default, stderr_default = _default_capture_caps(profile)
    stdout_cap = (
        stdout_default
        if args.stdout_cap_mib is None
        else args.stdout_cap_mib * 1024**2
    )
    stderr_cap = (
        stderr_default
        if args.stderr_cap_mib is None
        else args.stderr_cap_mib * 1024**2
    )
    child_args = tuple(args.child_args)
    if child_args[:1] == ("--",):
        child_args = child_args[1:]
    if args.resume_from is not None and args.experiment_id is None:
        raise RunnerConfigurationError(
            "--experiment-id is required with --resume-from so artifact identity is explicit"
        )
    experiment_id = args.experiment_id or (
        f"controlled-{args.experiment}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{os.getpid()}"
    )
    return RunnerConfiguration(
        experiment=args.experiment,
        child_args=child_args,
        run_directory=args.run_directory,
        experiment_id=experiment_id,
        limits=limits,
        stdout_cap_bytes=stdout_cap,
        stderr_cap_bytes=stderr_cap,
        telemetry_enabled=args.gpu_telemetry,
        telemetry_seconds=args.telemetry_seconds,
        termination_grace_seconds=args.termination_grace_seconds,
        overwrite=args.overwrite,
        resume_from=args.resume_from,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        config = _configuration_from_args(args)
        result = run_controlled_experiment(config)
    except (ControlledRunnerError, ResourceLimitExceeded, OSError, ValueError) as exc:
        print(
            json.dumps(
                {
                    "type": "rule30-controlled-runner-error",
                    "error": f"{type(exc).__name__}: {exc}",
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
            file=sys.stderr,
        )
        return 2
    print(json.dumps(result.to_jsonable(), indent=2, sort_keys=True))
    return result.exit_code


if __name__ == "__main__":
    raise SystemExit(main())
