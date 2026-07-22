#!/usr/bin/env python3
"""Run a conservative, same-workload Rule 30 benchmark matrix.

Every subprocess is launched from an explicit absolute executable path with
``shell=False``.  Complete numeric-byte outputs are compared before any timed
generation run.  Timings are subprocess end-to-end measurements: process
startup, runtime initialization, computation, and writing stdout are included;
parent-side hashing and validation are excluded.

The script normally prints a draft record to stdout.  Persistent output
requires this exact script to match ``HEAD``, a clean worktree, the canonical
trusted vector, explicit build directories, and unchanged executable hashes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import platform
import selectors
import signal
import statistics
import subprocess
import sys
import time
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_RELATIVE_PATH = Path("experiments/shared/run_benchmark_matrix.py")
REFERENCE_PREFIX = (
    REPOSITORY_ROOT
    / "tests"
    / "reference_vectors"
    / "center_c00000000_c00009999.u8"
)
STATISTICS_SCRIPT = (
    REPOSITORY_ROOT / "experiments/problem2_balance/run_finite_prefix.py"
)
PREDICTOR_SCRIPT = (
    REPOSITORY_ROOT / "experiments/problem3_complexity/run_exact_searches.py"
)
RESULT_DIRECTORY = REPOSITORY_ROOT / "results" / "benchmarks"

DEFAULT_COUNT = 4_096
DEFAULT_WARMUPS = 1
DEFAULT_REPETITIONS = 3
DEFAULT_TIMEOUT_SECONDS = 30.0
DEFAULT_MAX_CAPTURE_BYTES = 2 * 1024 * 1024
HARD_MAX_COUNT = 10_000
HARD_MAX_WARMUPS = 10
HARD_MAX_REPETITIONS = 20
HARD_MAX_TIMEOUT_SECONDS = 300.0
HARD_MAX_CAPTURE_BYTES = 16 * 1024 * 1024
HARD_MAX_INPUT_BYTES = 1024 * 1024
HARD_MAX_BINARY_BYTES = 512 * 1024 * 1024
POST_KILL_DRAIN_SECONDS = 1.0
RSS_MARKER = "__RULE30_TARGET_MAX_RSS_KIB__="


class MatrixError(RuntimeError):
    """A benchmark contract, safety-limit, or subprocess failure."""


@dataclass(frozen=True)
class CommandSpec:
    """One named, explicit argv vector."""

    name: str
    argv: tuple[str, ...]


@dataclass(frozen=True)
class ProcessResult:
    """Captured direct-child result and Linux wait4 resource measurement."""

    argv: tuple[str, ...]
    returncode: int
    stdout: bytes
    stderr: bytes
    elapsed_seconds: float
    peak_rss_kib: int | None


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_sha256(path: Path, *, maximum_bytes: int) -> tuple[int, str]:
    size = path.stat().st_size
    if size < 0 or size > maximum_bytes:
        raise MatrixError(
            f"file {path} has {size} bytes; maximum permitted is {maximum_bytes}"
        )
    digest = hashlib.sha256()
    observed = 0
    with path.open("rb") as stream:
        while chunk := stream.read(1024 * 1024):
            observed += len(chunk)
            if observed > maximum_bytes:
                raise MatrixError(f"file {path} grew beyond its size cap while hashing")
            digest.update(chunk)
    if observed != size:
        raise MatrixError(f"file {path} changed size while it was hashed")
    return observed, digest.hexdigest()


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


def _positive_float(text: str) -> float:
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive number") from exc
    if not math.isfinite(value) or value <= 0.0:
        raise argparse.ArgumentTypeError("expected a finite positive number")
    return value


def _resolved_executable(path: Path, *, name: str) -> Path:
    expanded = path.expanduser()
    if not expanded.is_absolute():
        raise MatrixError(f"{name} path must be absolute: {expanded}")
    # Preserve an explicitly supplied virtual-environment symlink.  Resolving
    # it to /usr/bin/python would change Python's environment semantics.
    if not expanded.exists() or not expanded.is_file() or not os.access(expanded, os.X_OK):
        raise MatrixError(f"{name} is not an executable file: {expanded}")
    return expanded


def _resolved_directory(path: Path, *, name: str) -> Path:
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_dir():
        raise MatrixError(f"{name} is not a directory: {resolved}")
    return resolved


def _require_descendant(path: Path, directory: Path, *, name: str) -> None:
    try:
        path.resolve(strict=True).relative_to(directory.resolve(strict=True))
    except ValueError as exc:
        raise MatrixError(f"{name} must be located under {directory}") from exc


def _require_cmake_source(build_directory: Path) -> None:
    cache = build_directory / "CMakeCache.txt"
    text = _read_text(cache)
    if text is None:
        raise MatrixError(f"persistent output requires {cache}")
    prefix = "CMAKE_HOME_DIRECTORY:INTERNAL="
    values = [
        line.removeprefix(prefix)
        for line in text.splitlines()
        if line.startswith(prefix)
    ]
    if len(values) != 1 or Path(values[0]).resolve() != REPOSITORY_ROOT.resolve():
        raise MatrixError(
            f"CMake build {build_directory} is not bound to this repository source"
        )


class ProcessRunner:
    """Run capped subprocesses without a shell and collect direct-child rusage.

    stdout and stderr are drained concurrently from bounded kernel pipes.  Once
    their combined captured size exceeds ``max_capture_bytes``, the new process
    group is killed.  Wall time is independently enforced.  On Linux, ``wait4``
    supplies the direct child's ``ru_maxrss`` in KiB.  Because ``Popen`` may
    fork the Python orchestrator before exec, that value is not reported as a
    target-only memory measurement.  Separate untimed GNU ``time`` profiles
    below fork targets after a small native wrapper has execed.
    """

    def __init__(self, *, timeout_seconds: float, max_capture_bytes: int) -> None:
        if not 0.0 < timeout_seconds <= HARD_MAX_TIMEOUT_SECONDS:
            raise MatrixError(
                f"timeout must be in (0, {HARD_MAX_TIMEOUT_SECONDS:g}] seconds"
            )
        if not 1 <= max_capture_bytes <= HARD_MAX_CAPTURE_BYTES:
            raise MatrixError(
                f"capture cap must be in [1, {HARD_MAX_CAPTURE_BYTES}] bytes"
            )
        if not hasattr(os, "wait4"):
            raise MatrixError("this WSL benchmark requires Linux os.wait4 support")
        self.timeout_seconds = timeout_seconds
        self.max_capture_bytes = max_capture_bytes

    @staticmethod
    def _kill_group(process: subprocess.Popen[bytes]) -> None:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass

    @staticmethod
    def _wait4(pid: int, options: int) -> tuple[int, int, Any]:
        while True:
            try:
                return os.wait4(pid, options)
            except InterruptedError:
                continue

    def run(
        self,
        argv: Sequence[str],
        *,
        cwd: Path,
        environment: Mapping[str, str],
        check: bool = True,
    ) -> ProcessResult:
        command = tuple(str(argument) for argument in argv)
        if not command:
            raise MatrixError("subprocess argv must not be empty")
        executable = Path(command[0])
        if not executable.is_absolute():
            raise MatrixError(f"subprocess executable must be absolute: {command[0]!r}")
        if any("\x00" in argument for argument in command):
            raise MatrixError("subprocess argv contains a NUL byte")

        started = time.perf_counter()
        process = subprocess.Popen(
            command,
            cwd=str(cwd),
            env=dict(environment),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            start_new_session=True,
        )
        assert process.stdout is not None
        assert process.stderr is not None
        output = bytearray()
        errors = bytearray()
        streams = selectors.DefaultSelector()
        for stream, destination in (
            (process.stdout, output),
            (process.stderr, errors),
        ):
            os.set_blocking(stream.fileno(), False)
            streams.register(stream, selectors.EVENT_READ, destination)

        reaped = False
        returncode: int | None = None
        peak_rss_kib: int | None = None
        failure_reason: str | None = None
        failure_started: float | None = None
        deadline = started + self.timeout_seconds

        try:
            while streams.get_map() or not reaped:
                remaining = deadline - time.perf_counter()
                if remaining <= 0.0 and failure_reason is None:
                    failure_reason = (
                        f"subprocess exceeded {self.timeout_seconds:g}-second wall cap"
                    )
                    failure_started = time.perf_counter()
                    self._kill_group(process)

                wait_seconds = max(0.0, min(0.02, remaining))
                for key, _event in streams.select(wait_seconds):
                    stream = key.fileobj
                    try:
                        chunk = os.read(stream.fileno(), 64 * 1024)
                    except BlockingIOError:
                        continue
                    if not chunk:
                        streams.unregister(stream)
                        stream.close()
                        continue
                    destination: bytearray = key.data
                    capture_remaining = self.max_capture_bytes - len(output) - len(errors)
                    accepted = chunk[: max(0, capture_remaining)]
                    destination.extend(accepted)
                    if len(accepted) != len(chunk) and failure_reason is None:
                        failure_reason = (
                            "subprocess exceeded combined stdout/stderr cap of "
                            f"{self.max_capture_bytes} bytes"
                        )
                        failure_started = time.perf_counter()
                        self._kill_group(process)

                if (
                    failure_started is not None
                    and streams.get_map()
                    and time.perf_counter() - failure_started
                    >= POST_KILL_DRAIN_SECONDS
                ):
                    for registered in list(streams.get_map().values()):
                        stream = registered.fileobj
                        streams.unregister(stream)
                        stream.close()

                if not reaped:
                    waited_pid, status, usage = self._wait4(process.pid, os.WNOHANG)
                    if waited_pid != 0:
                        reaped = True
                        returncode = os.waitstatus_to_exitcode(status)
                        process.returncode = returncode
                        peak_rss_kib = int(usage.ru_maxrss)

            if not reaped:
                waited_pid, status, usage = self._wait4(process.pid, 0)
                if waited_pid != process.pid:
                    raise MatrixError("wait4 reaped an unexpected process")
                returncode = os.waitstatus_to_exitcode(status)
                process.returncode = returncode
                peak_rss_kib = int(usage.ru_maxrss)
        except BaseException:
            if not reaped:
                self._kill_group(process)
                try:
                    _pid, status, _usage = self._wait4(process.pid, 0)
                    process.returncode = os.waitstatus_to_exitcode(status)
                except ChildProcessError:
                    pass
            raise
        finally:
            streams.close()
            if not process.stdout.closed:
                process.stdout.close()
            if not process.stderr.closed:
                process.stderr.close()

        elapsed = time.perf_counter() - started
        if failure_reason is not None:
            raise MatrixError(f"{failure_reason}: {list(command)!r}")
        assert returncode is not None
        result = ProcessResult(
            argv=command,
            returncode=returncode,
            stdout=bytes(output),
            stderr=bytes(errors),
            elapsed_seconds=elapsed,
            peak_rss_kib=peak_rss_kib,
        )
        if check and returncode != 0:
            diagnostic = result.stderr.decode("utf-8", errors="replace").strip()
            raise MatrixError(
                f"subprocess exited {returncode}: {list(command)!r}"
                + (f"\nstderr: {diagnostic}" if diagnostic else "")
            )
        return result


def timing_summary(samples: Sequence[float]) -> dict[str, Any]:
    """Return explicit descriptive statistics with population stddev."""
    values = [float(value) for value in samples]
    if not values or any(not math.isfinite(value) or value < 0.0 for value in values):
        raise MatrixError("timing samples must be nonempty, finite, and nonnegative")
    return {
        "unit": "seconds",
        "samples": values,
        "minimum": min(values),
        "median": statistics.median(values),
        "maximum": max(values),
        "mean": statistics.fmean(values),
        "population_standard_deviation": statistics.pstdev(values),
        "scope": (
            "subprocess end-to-end: process startup, runtime initialization, "
            "computation, and stdout writes; parent hashing/validation excluded"
        ),
    }


def _require_quiet_stderr(result: ProcessResult, *, name: str, phase: str) -> None:
    if result.stderr:
        digest = _sha256(result.stderr)
        raise MatrixError(
            f"{name} emitted unexpected stderr during {phase} "
            f"({len(result.stderr)} bytes, sha256={digest})"
        )


def _rotated_commands(
    commands: Sequence[CommandSpec], round_index: int
) -> tuple[CommandSpec, ...]:
    if not commands:
        return ()
    offset = round_index % len(commands)
    values = tuple(commands)
    return values[offset:] + values[:offset]


def profile_peak_rss(
    command: CommandSpec,
    *,
    time_executable: Path,
    runner: ProcessRunner,
    environment: Mapping[str, str],
) -> tuple[dict[str, Any], bytes]:
    """Run one untimed GNU-time profile and return target max RSS and stdout."""
    if len(command.argv) < 4 or command.argv[1] != "-n":
        raise MatrixError("RSS profiling expects the recorded nice prefix")
    profile_argv = (
        *command.argv[:3],
        str(time_executable),
        "--format",
        RSS_MARKER + "%M",
        "--",
        *command.argv[3:],
    )
    result = runner.run(
        profile_argv,
        cwd=REPOSITORY_ROOT,
        environment=environment,
    )
    marker_values: list[int] = []
    unexpected_lines: list[str] = []
    for line in result.stderr.decode("utf-8", errors="replace").splitlines():
        if line.startswith(RSS_MARKER):
            value = line.removeprefix(RSS_MARKER)
            if value.isdecimal():
                marker_values.append(int(value))
                continue
        if line.strip():
            unexpected_lines.append(line)
    if len(marker_values) != 1:
        raise MatrixError(
            f"GNU time emitted {len(marker_values)} valid RSS markers for {command.name}"
        )
    if unexpected_lines:
        raise MatrixError(
            f"{command.name} emitted unexpected stderr during RSS profiling: "
            + repr(unexpected_lines[:4])
        )
    return (
        {
            "reliable": True,
            "source": "GNU time %M: maximum resident set size of the target (KiB)",
            "peak_rss_kib": marker_values[0],
            "profile_runs": 1,
            "profile_command": list(profile_argv),
            "included_in_timing_samples": False,
            "limitations": (
                "host resident memory only; excludes CUDA device allocations"
            ),
        },
        result.stdout,
    )


def _nice_prefix(nice_executable: Path, level: int) -> tuple[str, ...]:
    if not 0 <= level <= 19:
        raise MatrixError("nice level must be between 0 and 19")
    return (str(nice_executable), "-n", str(level))


def build_generation_commands(
    *,
    count: int,
    python_executable: Path,
    cpp_executable: Path,
    rust_executable: Path,
    cuda_executable: Path,
    nice_executable: Path,
    nice_level: int,
    cuda_device: int,
    cuda_threads: int,
    cuda_memory_budget_mib: int,
    cuda_output_budget_mib: int,
) -> list[CommandSpec]:
    """Build the five materially identical finite-prefix commands."""
    prefix = _nice_prefix(nice_executable, nice_level)
    count_text = str(count)
    return [
        CommandSpec(
            "python-coordinate",
            prefix
            + (
                str(python_executable),
                "-m",
                "rule30lab.cli",
                "generate",
                "--count",
                count_text,
                "--backend",
                "python",
                "--format",
                "raw",
            ),
        ),
        CommandSpec(
            "cpp-scalar",
            prefix
            + (
                str(cpp_executable),
                "generate",
                "--count",
                count_text,
                "--backend",
                "scalar",
                "--format",
                "raw",
                "--chunk-size",
                "65536",
            ),
        ),
        CommandSpec(
            "cpp-avx2",
            prefix
            + (
                str(cpp_executable),
                "generate",
                "--count",
                count_text,
                "--backend",
                "avx2",
                "--format",
                "raw",
                "--chunk-size",
                "65536",
            ),
        ),
        CommandSpec(
            "rust-packed",
            prefix
            + (
                str(rust_executable),
                "generate",
                "--count",
                count_text,
                "--backend",
                "packed",
                "--format",
                "raw",
            ),
        ),
        CommandSpec(
            "cuda-direct",
            prefix
            + (
                str(cuda_executable),
                "generate",
                "--count",
                count_text,
                "--format",
                "raw",
                "--device",
                str(cuda_device),
                "--threads",
                str(cuda_threads),
                "--memory-budget-mib",
                str(cuda_memory_budget_mib),
                "--max-output-mib",
                str(cuda_output_budget_mib),
            ),
        ),
    ]


def _validate_numeric_bits(output: bytes, count: int, *, name: str) -> None:
    if len(output) != count:
        raise MatrixError(f"{name} emitted {len(output)} bytes; expected {count}")
    invalid = next(
        ((index, value) for index, value in enumerate(output) if value not in (0, 1)),
        None,
    )
    if invalid is not None:
        index, value = invalid
        raise MatrixError(f"{name} emitted non-bit byte {value} at index {index}")


def benchmark_generation(
    commands: Sequence[CommandSpec],
    *,
    count: int,
    trusted_reference: bytes,
    warmups: int,
    repetitions: int,
    time_executable: Path,
    runner: ProcessRunner,
    environment: Mapping[str, str],
) -> dict[str, Any]:
    """Verify all complete streams, then time them in round-robin order."""
    if len({command.name for command in commands}) != len(commands):
        raise MatrixError("generation benchmark names must be unique")
    if len(commands) < 2:
        raise MatrixError("at least two generation backends are required")
    _validate_numeric_bits(trusted_reference, count, name="trusted reference")

    verified: dict[str, bytes] = {}
    verification_runs: dict[str, dict[str, Any]] = {}
    for command in commands:
        result = runner.run(
            command.argv,
            cwd=REPOSITORY_ROOT,
            environment=environment,
        )
        _validate_numeric_bits(result.stdout, count, name=command.name)
        _require_quiet_stderr(
            result, name=command.name, phase="pre-timing verification"
        )
        if result.stdout != trusted_reference:
            first_difference = next(
                index
                for index, (observed, trusted) in enumerate(
                    zip(result.stdout, trusted_reference, strict=True)
                )
                if observed != trusted
            )
            raise MatrixError(
                f"{command.name} differs from the trusted vector at byte "
                f"{first_difference}; no timings were collected"
            )
        verified[command.name] = result.stdout
        verification_runs[command.name] = {
            "output_bytes": len(result.stdout),
            "sha256_u8": _sha256(result.stdout),
            "stderr_bytes": len(result.stderr),
            "command": list(command.argv),
        }

    reference_name = "trusted-vector"
    reference = trusted_reference
    for command in commands[1:]:
        if verified[command.name] != reference:
            first_difference = next(
                index
                for index, (left, right) in enumerate(
                    zip(reference, verified[command.name], strict=True)
                )
                if left != right
            )
            raise MatrixError(
                f"{command.name} differs from {reference_name} at byte "
                f"{first_difference}; no timings were collected"
            )

    warmup_orders: list[list[str]] = []
    for warmup_index in range(warmups):
        ordered = _rotated_commands(commands, warmup_index)
        warmup_orders.append([command.name for command in ordered])
        for command in ordered:
            result = runner.run(
                command.argv,
                cwd=REPOSITORY_ROOT,
                environment=environment,
            )
            if result.stdout != reference:
                raise MatrixError(f"{command.name} warmup output changed")
            _require_quiet_stderr(result, name=command.name, phase="warmup")

    seconds = {command.name: [] for command in commands}
    measured_orders: list[list[str]] = []
    for repetition_index in range(repetitions):
        ordered = _rotated_commands(commands, warmups + repetition_index)
        measured_orders.append([command.name for command in ordered])
        for command in ordered:
            result = runner.run(
                command.argv,
                cwd=REPOSITORY_ROOT,
                environment=environment,
            )
            if result.stdout != reference:
                raise MatrixError(f"{command.name} timed output changed")
            _require_quiet_stderr(result, name=command.name, phase="timed run")
            seconds[command.name].append(result.elapsed_seconds)

    peak_rss: dict[str, dict[str, Any]] = {}
    for command in commands:
        profile, output = profile_peak_rss(
            command,
            time_executable=time_executable,
            runner=runner,
            environment=environment,
        )
        if output != reference:
            raise MatrixError(f"{command.name} RSS-profile output changed")
        peak_rss[command.name] = profile

    return {
        "workload": "generate exactly c_0 through c_(N-1) from one black cell",
        "input": {
            "center_bit_count": count,
            "initial_condition": "x_0(0)=1 and x_j(0)=0 for j!=0",
            "input_representation": "explicit decimal N plus fixed single-cell seed",
        },
        "output": {
            "encoding": "one numeric byte (0 or 1) per bit, c_0 first",
            "size_bytes": len(reference),
            "sha256_u8": _sha256(reference),
            "ones": sum(reference),
            "zeros": len(reference) - sum(reference),
        },
        "pre_timing_verification": {
            "full_byte_equality": True,
            "reference_backend": reference_name,
            "trusted_reference_sha256_u8": _sha256(trusted_reference),
            "backend_runs": verification_runs,
        },
        "protocol": {
            "warmups_per_backend": warmups,
            "measured_repetitions_per_backend": repetitions,
            "warmup_orders": warmup_orders,
            "measured_orders": measured_orders,
            "ordering_policy": (
                "deterministic cyclic rotation; the starting backend advances "
                "by one for each warmup and measured round"
            ),
            "all_warmup_and_measured_outputs_matched": True,
        },
        "backends": {
            command.name: {
                "command": list(command.argv),
                "timing": timing_summary(seconds[command.name]),
                "host_peak_rss": peak_rss[command.name],
            }
            for command in commands
        },
    }


def build_statistics_command(
    *,
    python_executable: Path,
    trusted_prefix: Path,
    nice_executable: Path,
    nice_level: int,
) -> CommandSpec:
    return CommandSpec(
        "statistics-existing-prefix",
        _nice_prefix(nice_executable, nice_level)
        + (
            str(python_executable),
            str(STATISTICS_SCRIPT),
            "--input",
            str(trusted_prefix),
            "--checkpoints",
            "10,100,1000,10000",
            "--block-widths",
            "1,2,3,4,5,6,7,8",
            "--lags",
            "1,2,3,4,5,8,16,32,64,128",
            "--linear-prefixes",
            "1000,2000,5000",
            "--apen-patterns",
            "1,2,3,4,5,6",
            "--dyadic-widths",
            "64,256,1024,4096",
            "--max-table-entries",
            "1048576",
            "--max-block-width",
            "64",
            "--spectral-top-k",
            "8",
        ),
    )


def build_predictor_command(
    *,
    python_executable: Path,
    trusted_prefix: Path,
    nice_executable: Path,
    nice_level: int,
) -> CommandSpec:
    return CommandSpec(
        "bounded-predictor-search",
        _nice_prefix(nice_executable, nice_level)
        + (
            str(python_executable),
            str(PREDICTOR_SCRIPT),
            "--input",
            str(trusted_prefix),
            "--limit-bits",
            "5000",
            "--train-length",
            "2500",
            "--max-reported-errors",
            "8",
            "--dfao-min-states",
            "1",
            "--dfao-max-states",
            "3",
            "--dfao-start-model-id",
            "0",
            "--dfao-max-models",
            "100000",
            "--dfao-max-state-count-cap",
            "16",
            "--kernel-depth",
            "4",
            "--kernel-fingerprint-length",
            "64",
            "--kernel-max-nodes",
            "131071",
            "--kernel-max-fingerprint-bytes",
            "67108864",
            "--gf2-max-order",
            "12",
            "--gf2-start-candidate-id",
            "0",
            "--gf2-max-candidates",
            "1000000",
            "--gf2-max-order-cap",
            "64",
            "--boolean-min-window",
            "1",
            "--boolean-max-window",
            "12",
            "--boolean-start-completion-id",
            "0",
            "--boolean-max-completions",
            "1000000",
            "--boolean-max-unseen-contexts",
            "20",
            "--boolean-max-table-entries",
            "1048576",
        ),
    )


def benchmark_deterministic_json(
    command: CommandSpec,
    *,
    expected_question: str,
    expected_input: bytes,
    warmups: int,
    repetitions: int,
    time_executable: Path,
    runner: ProcessRunner,
    environment: Mapping[str, str],
) -> dict[str, Any]:
    """Verify deterministic JSON before measuring repeated subprocess runs."""
    verification = runner.run(
        command.argv,
        cwd=REPOSITORY_ROOT,
        environment=environment,
    )
    _require_quiet_stderr(
        verification, name=command.name, phase="pre-timing verification"
    )
    try:
        parsed = json.loads(verification.stdout)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise MatrixError(f"{command.name} did not emit valid UTF-8 JSON") from exc
    if not isinstance(parsed, dict):
        raise MatrixError(f"{command.name} JSON root is not an object")
    required = {
        "experiment_id",
        "question",
        "hypothesis",
        "backend",
        "parameters",
        "input",
        "result_summary",
        "interpretation",
        "status",
        "proof_scope",
        "limitations",
    }
    missing = sorted(required.difference(parsed))
    if missing:
        raise MatrixError(f"{command.name} JSON is missing fields: {missing}")
    if parsed["question"] != expected_question:
        raise MatrixError(
            f"{command.name} question {parsed['question']!r} does not match "
            f"{expected_question!r}"
        )
    if parsed["status"] not in {"empirical", "finite-exhaustive", "heuristic"}:
        raise MatrixError(f"{command.name} reported invalid benchmark status")
    if not isinstance(parsed["parameters"], dict) or not isinstance(
        parsed["result_summary"], dict
    ):
        raise MatrixError(f"{command.name} parameters/result_summary must be objects")
    input_record = parsed["input"]
    if not isinstance(input_record, dict):
        raise MatrixError(f"{command.name} input metadata must be an object")
    expected_hash = _sha256(expected_input)
    if command.name == "statistics-existing-prefix":
        observed_count = input_record.get("count")
        observed_hash = input_record.get("sha256_u8")
    elif command.name == "bounded-predictor-search":
        observed_count = input_record.get("used_bit_count")
        observed_hash = input_record.get("sha256_used_u8")
        protocol = parsed.get("training_validation_protocol")
        completion = parsed["result_summary"].get("completion")
        if not isinstance(protocol, dict) or not isinstance(completion, dict):
            raise MatrixError(
                "bounded predictor JSON lacks protocol or completion metadata"
            )
        if completion.get("all_requested_searches_completed") is not True:
            raise MatrixError("bounded predictor search did not complete every request")
    else:
        raise MatrixError(f"no semantic JSON contract for {command.name}")
    if observed_count != len(expected_input) or observed_hash != expected_hash:
        raise MatrixError(
            f"{command.name} input identity does not match the expected trusted bytes"
        )

    for _warmup in range(warmups):
        result = runner.run(
            command.argv,
            cwd=REPOSITORY_ROOT,
            environment=environment,
        )
        if result.stdout != verification.stdout:
            raise MatrixError(f"{command.name} warmup JSON changed byte-for-byte")
        _require_quiet_stderr(result, name=command.name, phase="warmup")

    seconds: list[float] = []
    for _repetition in range(repetitions):
        result = runner.run(
            command.argv,
            cwd=REPOSITORY_ROOT,
            environment=environment,
        )
        if result.stdout != verification.stdout:
            raise MatrixError(f"{command.name} measured JSON changed byte-for-byte")
        _require_quiet_stderr(result, name=command.name, phase="timed run")
        seconds.append(result.elapsed_seconds)

    peak_rss, profiled_output = profile_peak_rss(
        command,
        time_executable=time_executable,
        runner=runner,
        environment=environment,
    )
    if profiled_output != verification.stdout:
        raise MatrixError(f"{command.name} RSS-profile JSON changed byte-for-byte")

    compact_result: dict[str, Any] = {
        "experiment_id": parsed.get("experiment_id"),
        "status": parsed.get("status"),
        "input": parsed.get("input"),
    }
    if command.name == "bounded-predictor-search":
        compact_result["training_validation_protocol"] = parsed.get(
            "training_validation_protocol"
        )
        compact_result["completion"] = (
            parsed.get("result_summary", {}).get("completion")
            if isinstance(parsed.get("result_summary"), dict)
            else None
        )

    return {
        "command": list(command.argv),
        "protocol": {
            "verification_runs_before_timing": 1,
            "warmups": warmups,
            "measured_repetitions": repetitions,
            "all_outputs_matched_byte_for_byte": True,
        },
        "deterministic_output": {
            "encoding": "UTF-8 JSON",
            "size_bytes": len(verification.stdout),
            "sha256": _sha256(verification.stdout),
            "reported_fields": compact_result,
        },
        "timing": timing_summary(seconds),
        "host_peak_rss": peak_rss,
    }


def _read_text(path: Path) -> str | None:
    try:
        if path.stat().st_size > 8 * 1024 * 1024:
            return None
        return path.read_text(encoding="utf-8").strip()
    except (FileNotFoundError, OSError, UnicodeError):
        return None


def _numeric_summary(values: Sequence[float]) -> dict[str, Any] | None:
    if not values:
        return None
    return {
        "sample_count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": statistics.fmean(values),
    }


def cpu_frequency_snapshot() -> dict[str, Any]:
    """Read governor and frequency state without changing it."""
    cpu_directories = sorted(Path("/sys/devices/system/cpu").glob("cpu[0-9]*"))
    governors: Counter[str] = Counter()
    drivers: Counter[str] = Counter()
    current_khz: list[float] = []
    minimum_khz: list[float] = []
    maximum_khz: list[float] = []
    for directory in cpu_directories:
        cpufreq = directory / "cpufreq"
        governor = _read_text(cpufreq / "scaling_governor")
        driver = _read_text(cpufreq / "scaling_driver")
        if governor:
            governors[governor] += 1
        if driver:
            drivers[driver] += 1
        for path, destination in (
            (cpufreq / "scaling_cur_freq", current_khz),
            (cpufreq / "scaling_min_freq", minimum_khz),
            (cpufreq / "scaling_max_freq", maximum_khz),
        ):
            value = _read_text(path)
            if value is not None:
                try:
                    destination.append(float(value))
                except ValueError:
                    pass

    proc_mhz: list[float] = []
    cpuinfo = _read_text(Path("/proc/cpuinfo")) or ""
    for line in cpuinfo.splitlines():
        if line.lower().startswith("cpu mhz") and ":" in line:
            try:
                proc_mhz.append(float(line.split(":", 1)[1].strip()))
            except ValueError:
                pass

    available = bool(governors or drivers or current_khz)
    return {
        "cpufreq_sysfs_available": available,
        "cpufreq_unavailable_reason": (
            None
            if available
            else "the WSL kernel did not expose per-CPU cpufreq policy files"
        ),
        "sampled_cpu_directories": len(cpu_directories),
        "governors": dict(sorted(governors.items())),
        "drivers": dict(sorted(drivers.items())),
        "scaling_current_khz": _numeric_summary(current_khz),
        "scaling_minimum_khz": _numeric_summary(minimum_khz),
        "scaling_maximum_khz": _numeric_summary(maximum_khz),
        "proc_cpuinfo_mhz": _numeric_summary(proc_mhz),
        "interpretation": (
            "read-only snapshots; frequency was neither pinned nor controlled and "
            "may vary during each subprocess"
        ),
    }


def cpu_metadata() -> dict[str, Any]:
    cpuinfo = _read_text(Path("/proc/cpuinfo")) or ""
    models: list[str] = []
    flags: set[str] = set()
    for line in cpuinfo.splitlines():
        if line.startswith("model name") and ":" in line:
            model = line.split(":", 1)[1].strip()
            if model not in models:
                models.append(model)
        if line.startswith("flags") and ":" in line:
            flags.update(line.split(":", 1)[1].split())
    return {
        "model_names": models,
        "logical_cpu_count": os.cpu_count(),
        "avx2_reported": "avx2" in flags,
        "selected_instruction_flags": sorted(
            flag for flag in ("sse2", "avx", "avx2", "fma", "bmi1", "bmi2") if flag in flags
        ),
    }


def memory_snapshot() -> dict[str, int]:
    fields: dict[str, int] = {}
    text = _read_text(Path("/proc/meminfo")) or ""
    for line in text.splitlines():
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        if name in {"MemTotal", "MemAvailable", "SwapTotal", "SwapFree"}:
            token = value.strip().split()[0]
            try:
                fields[f"{name}_kib"] = int(token)
            except ValueError:
                pass
    return fields


def _probe(
    runner: ProcessRunner,
    argv: Sequence[str],
    *,
    environment: Mapping[str, str],
) -> dict[str, Any]:
    try:
        result = runner.run(
            argv,
            cwd=REPOSITORY_ROOT,
            environment=environment,
            check=False,
        )
    except (MatrixError, OSError) as exc:
        return {"available": False, "command": list(argv), "error": str(exc)}
    return {
        "available": result.returncode == 0,
        "command": list(argv),
        "returncode": result.returncode,
        "stdout": result.stdout.decode("utf-8", errors="replace").strip(),
        "stderr": result.stderr.decode("utf-8", errors="replace").strip(),
    }


def gpu_snapshot(
    runner: ProcessRunner,
    nvidia_smi_executable: Path,
    *,
    environment: Mapping[str, str],
) -> dict[str, Any]:
    fields = (
        "index,name,memory.total,driver_version,temperature.gpu,pstate,"
        "clocks.current.graphics,power.draw,power.limit"
    )
    probe = _probe(
        runner,
        (
            str(nvidia_smi_executable),
            f"--query-gpu={fields}",
            "--format=csv,noheader,nounits",
        ),
        environment=environment,
    )
    probe["queried_fields"] = fields.split(",")
    probe["interpretation"] = (
        "read-only snapshot; no clocks, power, voltage, fan, or thermal controls changed"
    )
    return probe


def _binary_metadata(path: Path) -> dict[str, Any]:
    size, digest = _file_sha256(path, maximum_bytes=HARD_MAX_BINARY_BYTES)
    return {
        "path": str(path),
        "size_bytes": size,
        "sha256": digest,
    }


def cmake_build_metadata(build_directory: Path | None) -> dict[str, Any]:
    """Collect retained CMake cache and target flags where discoverable."""
    if build_directory is None:
        return {"available": False, "reason": "no build directory was supplied"}
    selected: dict[str, list[str]] = {}
    candidates = [
        build_directory / "CMakeCache.txt",
        build_directory / "build.ninja",
    ]
    candidates.extend(sorted(build_directory.glob("**/flags.make"))[:128])
    for path in candidates:
        text = _read_text(path)
        if text is None:
            continue
        if path.name == "build.ninja":
            lines = [
                line
                for line in text.splitlines()
                if (
                    "rule30_" in line
                    or line.lstrip().startswith(("FLAGS =", "DEFINES =", "LINK_FLAGS ="))
                )
            ][:512]
        else:
            lines = [
                line
                for line in text.splitlines()
                if line.startswith(
                    (
                        "CMAKE_BUILD_TYPE:",
                        "CMAKE_CXX_COMPILER:",
                        "CMAKE_CUDA_COMPILER:",
                        "CMAKE_CUDA_ARCHITECTURES:",
                        "CMAKE_HOME_DIRECTORY:",
                        "CMAKE_CXX_FLAGS:",
                        "CMAKE_CXX_FLAGS_RELEASE:",
                        "CMAKE_CUDA_FLAGS:",
                        "CMAKE_CUDA_FLAGS_RELEASE:",
                        "CXX_DEFINES =",
                        "CXX_FLAGS =",
                        "CUDA_DEFINES =",
                        "CUDA_FLAGS =",
                        "# Custom options:",
                    )
                )
            ]
        if lines:
            selected[str(path.relative_to(build_directory))] = lines
    compile_commands: list[dict[str, Any]] = []
    compile_commands_text = _read_text(build_directory / "compile_commands.json")
    if compile_commands_text is not None:
        try:
            raw_commands = json.loads(compile_commands_text)
        except json.JSONDecodeError as exc:
            raise MatrixError("compile_commands.json is invalid JSON") from exc
        if not isinstance(raw_commands, list):
            raise MatrixError("compile_commands.json root must be an array")
        for entry in raw_commands:
            if not isinstance(entry, dict):
                continue
            source = str(entry.get("file", ""))
            if "/src/cpp/" not in source and "/src/cuda/" not in source:
                continue
            compile_commands.append(
                {
                    key: entry[key]
                    for key in ("directory", "file", "command", "arguments", "output")
                    if key in entry
                }
            )
            if len(compile_commands) >= 128:
                break
    return {
        "available": bool(selected or compile_commands),
        "build_directory": str(build_directory),
        "retained_configuration_and_flag_lines": selected,
        "target_compile_commands": compile_commands,
        "limitations": (
            "retained CMake files are reported verbatim; absence means exact "
            "compile invocations were not recoverable from this build tree"
        ),
    }


def git_provenance(
    *,
    git_executable: Path,
    runner: ProcessRunner,
    environment: Mapping[str, str],
) -> dict[str, Any]:
    head_result = runner.run(
        (str(git_executable), "-C", str(REPOSITORY_ROOT), "rev-parse", "HEAD"),
        cwd=REPOSITORY_ROOT,
        environment=environment,
    )
    head = head_result.stdout.decode("ascii").strip()
    if len(head) != 40 or any(character not in "0123456789abcdef" for character in head):
        raise MatrixError(f"git returned an invalid full commit id: {head!r}")

    show = runner.run(
        (
            str(git_executable),
            "-C",
            str(REPOSITORY_ROOT),
            "show",
            f"HEAD:{SCRIPT_RELATIVE_PATH.as_posix()}",
        ),
        cwd=REPOSITORY_ROOT,
        environment=environment,
        check=False,
    )
    script_bytes = (REPOSITORY_ROOT / SCRIPT_RELATIVE_PATH).read_bytes()
    tracked_in_head = show.returncode == 0
    matches_head = tracked_in_head and show.stdout == script_bytes
    status = runner.run(
        (
            str(git_executable),
            "-C",
            str(REPOSITORY_ROOT),
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
        ),
        cwd=REPOSITORY_ROOT,
        environment=environment,
    )
    worktree_clean = status.stdout == b""
    tree_ids: dict[str, str] = {}
    for relative in (
        "src/python",
        "src/cpp",
        "src/cuda",
        "src/rust",
        "experiments/problem2_balance",
        "experiments/problem3_complexity",
        "tests/reference_vectors",
    ):
        result = runner.run(
            (
                str(git_executable),
                "-C",
                str(REPOSITORY_ROOT),
                "rev-parse",
                f"HEAD:{relative}",
            ),
            cwd=REPOSITORY_ROOT,
            environment=environment,
        )
        tree_id = result.stdout.decode("ascii").strip()
        if len(tree_id) != 40:
            raise MatrixError(f"invalid Git tree id for {relative}: {tree_id!r}")
        tree_ids[relative] = tree_id
    return {
        "head_commit": head,
        "script_relative_path": SCRIPT_RELATIVE_PATH.as_posix(),
        "script_sha256": _sha256(script_bytes),
        "script_tracked_in_head": tracked_in_head,
        "script_byte_identical_to_head": matches_head,
        "worktree_clean_before_benchmark": worktree_clean,
        "worktree_status_sha256": _sha256(status.stdout),
        "worktree_status_entry_count": len(status.stdout.splitlines()),
        "relevant_head_tree_ids": tree_ids,
        "persistent_record_eligible": matches_head and worktree_clean,
    }


def _environment() -> dict[str, str]:
    environment = {
        "PATH": (
            "/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:"
            "/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/wsl/lib"
        ),
        "PYTHONPATH": str(REPOSITORY_ROOT / "src" / "python"),
        "PYTHONHASHSEED": "0",
        "PYTHONNOUSERSITE": "1",
        "LC_ALL": "C",
        "LANG": "C",
        "OMP_NUM_THREADS": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "NUMEXPR_NUM_THREADS": "1",
        "RAYON_NUM_THREADS": "1",
    }
    for name in ("HOME", "TMPDIR", "CUDA_CACHE_PATH", "CUDA_VISIBLE_DEVICES"):
        value = os.environ.get(name)
        if value:
            environment[name] = value
    return environment


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python-executable", type=Path, required=True)
    parser.add_argument("--cpp-executable", type=Path, required=True)
    parser.add_argument("--rust-executable", type=Path, required=True)
    parser.add_argument("--cuda-executable", type=Path, required=True)
    parser.add_argument("--nice-executable", type=Path, default=Path("/usr/bin/nice"))
    parser.add_argument("--time-executable", type=Path, default=Path("/usr/bin/time"))
    parser.add_argument("--git-executable", type=Path, default=Path("/usr/bin/git"))
    parser.add_argument(
        "--nvidia-smi-executable",
        type=Path,
        default=Path("/usr/lib/wsl/lib/nvidia-smi"),
    )
    parser.add_argument("--cxx-compiler", type=Path)
    parser.add_argument("--rustc-executable", type=Path)
    parser.add_argument("--cargo-executable", type=Path)
    parser.add_argument("--nvcc-executable", type=Path)
    parser.add_argument("--cpp-build-directory", type=Path)
    parser.add_argument("--cuda-build-directory", type=Path)
    parser.add_argument("--rust-build-directory", type=Path)
    parser.add_argument("--trusted-prefix", type=Path, default=REFERENCE_PREFIX)
    parser.add_argument("--count", type=_positive_integer, default=DEFAULT_COUNT)
    parser.add_argument("--warmups", type=_nonnegative_integer, default=DEFAULT_WARMUPS)
    parser.add_argument(
        "--repetitions", type=_positive_integer, default=DEFAULT_REPETITIONS
    )
    parser.add_argument(
        "--timeout-seconds", type=_positive_float, default=DEFAULT_TIMEOUT_SECONDS
    )
    parser.add_argument(
        "--max-capture-bytes",
        type=_positive_integer,
        default=DEFAULT_MAX_CAPTURE_BYTES,
    )
    parser.add_argument("--nice-level", type=_nonnegative_integer, default=10)
    parser.add_argument("--cuda-device", type=_nonnegative_integer, default=0)
    parser.add_argument("--cuda-threads", type=_positive_integer, default=256)
    parser.add_argument(
        "--cuda-memory-budget-mib", type=_positive_integer, default=64
    )
    parser.add_argument(
        "--cuda-output-budget-mib", type=_positive_integer, default=16
    )
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "atomically write a strict result under results/benchmarks; refused "
            "unless this exact script is committed in HEAD"
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="replace an existing benchmark record explicitly",
    )
    return parser


def _validate_args(args: argparse.Namespace) -> None:
    if args.count > HARD_MAX_COUNT:
        raise MatrixError(f"count exceeds conservative hard cap {HARD_MAX_COUNT}")
    if args.warmups > HARD_MAX_WARMUPS:
        raise MatrixError(f"warmups exceed hard cap {HARD_MAX_WARMUPS}")
    if args.repetitions > HARD_MAX_REPETITIONS:
        raise MatrixError(f"repetitions exceed hard cap {HARD_MAX_REPETITIONS}")
    if args.timeout_seconds > HARD_MAX_TIMEOUT_SECONDS:
        raise MatrixError(
            f"timeout exceeds hard cap {HARD_MAX_TIMEOUT_SECONDS:g} seconds"
        )
    if args.max_capture_bytes > HARD_MAX_CAPTURE_BYTES:
        raise MatrixError(
            f"capture cap exceeds hard cap {HARD_MAX_CAPTURE_BYTES} bytes"
        )
    if not 0 <= args.nice_level <= 19:
        raise MatrixError("nice level must be between 0 and 19")
    if args.cuda_threads > 1024:
        raise MatrixError("CUDA threads exceed conservative cap 1024")
    if args.cuda_memory_budget_mib > 2048:
        raise MatrixError("CUDA memory budget exceeds conservative cap 2048 MiB")
    if args.cuda_output_budget_mib > 64:
        raise MatrixError("CUDA output budget exceeds conservative cap 64 MiB")


def _atomic_write_record(path: Path, record: Mapping[str, Any]) -> None:
    sys.path.insert(0, str(REPOSITORY_ROOT / "src" / "python"))
    from rule30lab.records import atomic_write_json  # noqa: PLC0415

    atomic_write_json(path, record)


def run_matrix(args: argparse.Namespace) -> dict[str, Any]:
    _validate_args(args)
    python_executable = _resolved_executable(
        args.python_executable, name="Python executable"
    )
    cpp_executable = _resolved_executable(args.cpp_executable, name="C++ executable")
    rust_executable = _resolved_executable(
        args.rust_executable, name="Rust executable"
    )
    cuda_executable = _resolved_executable(
        args.cuda_executable, name="CUDA executable"
    )
    nice_executable = _resolved_executable(
        args.nice_executable, name="nice executable"
    )
    time_executable = _resolved_executable(
        args.time_executable, name="GNU time executable"
    )
    git_executable = _resolved_executable(args.git_executable, name="Git executable")
    nvidia_smi_executable = _resolved_executable(
        args.nvidia_smi_executable, name="nvidia-smi executable"
    )
    optional_executables: dict[str, Path | None] = {}
    for attribute, label in (
        ("cxx_compiler", "C++ compiler"),
        ("rustc_executable", "rustc executable"),
        ("cargo_executable", "Cargo executable"),
        ("nvcc_executable", "nvcc executable"),
    ):
        value = getattr(args, attribute)
        optional_executables[attribute] = (
            None if value is None else _resolved_executable(value, name=label)
        )

    cpp_build_directory = (
        None
        if args.cpp_build_directory is None
        else _resolved_directory(args.cpp_build_directory, name="C++ build directory")
    )
    cuda_build_directory = (
        None
        if args.cuda_build_directory is None
        else _resolved_directory(args.cuda_build_directory, name="CUDA build directory")
    )
    rust_build_directory = (
        None
        if args.rust_build_directory is None
        else _resolved_directory(args.rust_build_directory, name="Rust build directory")
    )
    if args.output is not None:
        if (
            cpp_build_directory is None
            or cuda_build_directory is None
            or rust_build_directory is None
        ):
            raise MatrixError(
                "persistent output requires explicit C++, CUDA, and Rust build directories"
            )
        _require_descendant(
            cpp_executable, cpp_build_directory, name="C++ executable"
        )
        _require_descendant(
            cuda_executable, cuda_build_directory, name="CUDA executable"
        )
        _require_descendant(
            rust_executable, rust_build_directory, name="Rust executable"
        )
        _require_cmake_source(cpp_build_directory)
        _require_cmake_source(cuda_build_directory)
    trusted_prefix = args.trusted_prefix.expanduser().resolve(strict=True)
    if args.output is not None and trusted_prefix != REFERENCE_PREFIX.resolve(strict=True):
        raise MatrixError(
            "persistent output requires the repository canonical trusted prefix"
        )
    trusted_size = trusted_prefix.stat().st_size
    if trusted_size > HARD_MAX_INPUT_BYTES:
        raise MatrixError(
            f"trusted prefix has {trusted_size} bytes; cap is {HARD_MAX_INPUT_BYTES}"
        )
    trusted_bits = trusted_prefix.read_bytes()
    if len(trusted_bits) != trusted_size:
        raise MatrixError("trusted prefix changed size while it was read")
    _validate_numeric_bits(trusted_bits, len(trusted_bits), name="trusted prefix")
    if args.count > len(trusted_bits):
        raise MatrixError(
            f"count {args.count} exceeds trusted prefix length {len(trusted_bits)}"
        )
    if len(trusted_bits) < 5_000:
        raise MatrixError(
            "trusted prefix must contain at least 5000 bits for the predictor workload"
        )

    environment = _environment()
    runner = ProcessRunner(
        timeout_seconds=args.timeout_seconds,
        max_capture_bytes=args.max_capture_bytes,
    )
    provenance = git_provenance(
        git_executable=git_executable,
        runner=runner,
        environment=environment,
    )
    if args.output is not None and not provenance["persistent_record_eligible"]:
        raise MatrixError(
            "--output refused: the benchmark script must match HEAD and the full "
            "tracked/untracked worktree must be clean; commit or remove changes, "
            "rebuild from that commit, and rerun"
        )
    executable_paths = {
        "python": python_executable,
        "cpp": cpp_executable,
        "rust": rust_executable,
        "cuda": cuda_executable,
        "nice": nice_executable,
        "time": time_executable,
    }
    executable_metadata_before = {
        name: _binary_metadata(path) for name, path in executable_paths.items()
    }

    started = time.perf_counter()
    frequency_before = cpu_frequency_snapshot()
    memory_before = memory_snapshot()
    gpu_before = gpu_snapshot(
        runner, nvidia_smi_executable, environment=environment
    )

    generation_commands = build_generation_commands(
        count=args.count,
        python_executable=python_executable,
        cpp_executable=cpp_executable,
        rust_executable=rust_executable,
        cuda_executable=cuda_executable,
        nice_executable=nice_executable,
        nice_level=args.nice_level,
        cuda_device=args.cuda_device,
        cuda_threads=args.cuda_threads,
        cuda_memory_budget_mib=args.cuda_memory_budget_mib,
        cuda_output_budget_mib=args.cuda_output_budget_mib,
    )
    generation = benchmark_generation(
        generation_commands,
        count=args.count,
        trusted_reference=trusted_bits[: args.count],
        warmups=args.warmups,
        repetitions=args.repetitions,
        time_executable=time_executable,
        runner=runner,
        environment=environment,
    )

    statistics_command = build_statistics_command(
        python_executable=python_executable,
        trusted_prefix=trusted_prefix,
        nice_executable=nice_executable,
        nice_level=args.nice_level,
    )
    statistics_benchmark = benchmark_deterministic_json(
        statistics_command,
        expected_question="problem2",
        expected_input=trusted_bits,
        warmups=args.warmups,
        repetitions=args.repetitions,
        time_executable=time_executable,
        runner=runner,
        environment=environment,
    )
    predictor_command = build_predictor_command(
        python_executable=python_executable,
        trusted_prefix=trusted_prefix,
        nice_executable=nice_executable,
        nice_level=args.nice_level,
    )
    predictor_benchmark = benchmark_deterministic_json(
        predictor_command,
        expected_question="problem3",
        expected_input=trusted_bits[:5_000],
        warmups=args.warmups,
        repetitions=args.repetitions,
        time_executable=time_executable,
        runner=runner,
        environment=environment,
    )

    gpu_after = gpu_snapshot(runner, nvidia_smi_executable, environment=environment)
    frequency_after = cpu_frequency_snapshot()
    memory_after = memory_snapshot()
    runtime_seconds = time.perf_counter() - started
    executable_metadata_after = {
        name: _binary_metadata(path) for name, path in executable_paths.items()
    }
    if executable_metadata_after != executable_metadata_before:
        raise MatrixError("one or more benchmark executables changed during the run")

    software: dict[str, Any] = {
        "platform": platform.platform(),
        "python_runtime": sys.version,
        "executables": {
            "before": executable_metadata_before,
            "after": executable_metadata_after,
            "unchanged_during_benchmark": True,
        },
        "normalized_environment": {
            name: value
            for name, value in environment.items()
            if name not in {"HOME"}
        },
        "versions": {
            "python": _probe(
                runner,
                (str(python_executable), "--version"),
                environment=environment,
            ),
        },
        "cpp_build": cmake_build_metadata(cpp_build_directory),
        "cuda_build": cmake_build_metadata(cuda_build_directory),
        "rust_release_profile": {
            "source": str(REPOSITORY_ROOT / "Cargo.toml"),
            "build_directory": (
                None if rust_build_directory is None else str(rust_build_directory)
            ),
            "manifest_hashes": {
                relative: {
                    "size_bytes": metadata[0],
                    "sha256": metadata[1],
                }
                for relative, metadata in {
                    path: _file_sha256(
                        REPOSITORY_ROOT / path, maximum_bytes=1024 * 1024
                    )
                    for path in (
                        "Cargo.toml",
                        "Cargo.lock",
                        "src/rust/rule30-core/Cargo.toml",
                    )
                }.items()
            },
            "retained_settings": {"lto": "thin", "codegen-units": 1},
            "note": (
                "Cargo release defaults supply optimization; exact rustc argv is "
                "not recoverable from the final binary unless retained by the build"
            ),
        },
        "code_provenance": provenance,
    }
    version_arguments = {
        "cxx": ("cxx_compiler", ("--version",)),
        "rustc": ("rustc_executable", ("--version", "--verbose")),
        "cargo": ("cargo_executable", ("--version",)),
        "nvcc": ("nvcc_executable", ("--version",)),
    }
    for name, (key, suffix) in version_arguments.items():
        executable = optional_executables[key]
        software["versions"][name] = (
            {"available": False, "reason": "no explicit executable supplied"}
            if executable is None
            else _probe(
                runner,
                (str(executable), *suffix),
                environment=environment,
            )
        )

    timestamp = datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    record: dict[str, Any] = {
        "schema_version": 1,
        "experiment_id": (
            "benchmark-same-workload-matrix-" + timestamp.replace(":", "").replace("-", "")
        ),
        "timestamp_utc": timestamp,
        "git_commit": provenance["head_commit"],
        "question": "problem3",
        "hypothesis": (
            "Verified implementations of the same finite center-prefix workload "
            "may have different subprocess end-to-end costs on this host; repeated "
            "measurements characterize only these explicit workloads."
        ),
        "backend": "python-coordinate|cpp-scalar|cpp-avx2|rust-packed|cuda-direct",
        "parameters": {
            "generation_count": args.count,
            "warmups": args.warmups,
            "repetitions": args.repetitions,
            "timeout_seconds_per_subprocess": args.timeout_seconds,
            "combined_stdout_stderr_cap_bytes": args.max_capture_bytes,
            "nice_level": args.nice_level,
            "cuda": {
                "device": args.cuda_device,
                "threads": args.cuda_threads,
                "memory_budget_mib": args.cuda_memory_budget_mib,
                "output_budget_mib": args.cuda_output_budget_mib,
            },
            "trusted_prefix": {
                "path": str(trusted_prefix),
                "size_bytes": len(trusted_bits),
                "sha256_u8": _sha256(trusted_bits),
            },
        },
        "hardware": {
            "cpu": cpu_metadata(),
            "cpu_frequency_behavior": {
                "before": frequency_before,
                "after": frequency_after,
            },
            "memory": {"before": memory_before, "after": memory_after},
            "gpu": {"before": gpu_before, "after": gpu_after},
        },
        "software": software,
        "runtime_seconds": runtime_seconds,
        "result_hashes": {
            "generation_center_u8_sha256": generation["output"]["sha256_u8"],
            "statistics_json_sha256": statistics_benchmark["deterministic_output"][
                "sha256"
            ],
            "predictor_json_sha256": predictor_benchmark["deterministic_output"][
                "sha256"
            ],
            "benchmark_script_sha256": provenance["script_sha256"],
            "python_executable_sha256": executable_metadata_before["python"]["sha256"],
            "cpp_executable_sha256": executable_metadata_before["cpp"]["sha256"],
            "rust_executable_sha256": executable_metadata_before["rust"]["sha256"],
            "cuda_executable_sha256": executable_metadata_before["cuda"]["sha256"],
            "trusted_prefix_sha256": _sha256(trusted_bits),
        },
        "result_summary": {
            "generation_same_workload": generation,
            "statistics_over_existing_trusted_prefix": statistics_benchmark,
            "bounded_predictor_search": predictor_benchmark,
            "persistent_record_eligible": provenance["persistent_record_eligible"],
        },
        "interpretation": (
            "The five generation streams matched completely before timing and in "
            "every measured run. Timings are empirical subprocess end-to-end "
            "measurements for one modest finite N; no backend is called universally "
            "faster and no complexity-theoretic conclusion is drawn."
        ),
        "status": "empirical",
        "proof_scope": (
            "exact equality of every emitted finite center byte in the stated runs; "
            "descriptive timing and separate GNU-time target RSS profiles only"
        ),
        "limitations": [
            "subprocess startup and runtime initialization can dominate modest N",
            "CUDA timings include context setup and host/device orchestration, not only kernels",
            "CPU frequencies were observed but neither pinned nor controlled",
            "peak RSS is host memory and does not measure CUDA device allocation",
            "a benchmark does not establish an asymptotic upper or lower bound",
            "finite equality does not prove correctness for all horizons",
            "no finite experiment proves any infinite Rule 30 prize statement",
            (
                "clean source, build-directory binding, flags, and executable "
                "hashes are provenance evidence, not a cryptographically "
                "attested reproducible-build proof"
            ),
            (
                "the record is classified under problem3 because it includes "
                "the bounded predictor workload, but it also embeds a problem2 "
                "finite-prefix statistics timing"
            ),
        ],
    }
    return record


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        record = run_matrix(args)
        if args.output is not None:
            destination = args.output.expanduser().resolve()
            if destination.parent != RESULT_DIRECTORY.resolve():
                raise MatrixError(
                    f"--output must be directly under {RESULT_DIRECTORY.resolve()}"
                )
            if destination.exists() and not args.overwrite:
                raise MatrixError(
                    f"refusing to replace existing benchmark record without "
                    f"--overwrite: {destination}"
                )
            _atomic_write_record(destination, record)
            print(destination)
        else:
            print(json.dumps(record, indent=2, sort_keys=True, allow_nan=False))
        return 0
    except (MatrixError, OSError, ValueError) as exc:
        print(f"benchmark matrix failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
