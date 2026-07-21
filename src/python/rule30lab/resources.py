"""Conservative resource controls for local experiments.

This module changes no clock, voltage, power, driver, or thermal setting. It
only constrains project processes and reads operating-system/NVIDIA telemetry.
"""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from types import FrameType
from typing import Any


class ResourceLimitExceeded(RuntimeError):
    """Raised before a configured local resource budget is exceeded."""


class ResourceProfile(StrEnum):
    INTERACTIVE = "interactive"
    IDLE = "idle"


@dataclass(frozen=True)
class ResourceLimits:
    profile: ResourceProfile
    wall_seconds: float
    ram_bytes: int
    gpu_memory_bytes: int
    output_bytes: int
    disk_reserve_bytes: int
    progress_seconds: float
    gpu_pause_temperature_c: int
    gpu_abort_temperature_c: int
    cpu_workers: int

    @classmethod
    def conservative(cls, profile: ResourceProfile = ResourceProfile.INTERACTIVE) -> "ResourceLimits":
        logical_cpus = os.cpu_count() or 1
        if profile is ResourceProfile.IDLE:
            return cls(
                profile=profile,
                wall_seconds=6 * 60 * 60,
                ram_bytes=13 * 1024**3,
                gpu_memory_bytes=6 * 1024**3,
                output_bytes=4 * 1024**3,
                disk_reserve_bytes=10 * 1024**3,
                progress_seconds=15.0,
                gpu_pause_temperature_c=82,
                gpu_abort_temperature_c=86,
                cpu_workers=logical_cpus,
            )
        return cls(
            profile=profile,
            wall_seconds=60 * 60,
            ram_bytes=8 * 1024**3,
            gpu_memory_bytes=4 * 1024**3,
            output_bytes=1024**3,
            disk_reserve_bytes=10 * 1024**3,
            progress_seconds=10.0,
            gpu_pause_temperature_c=78,
            gpu_abort_temperature_c=84,
            cpu_workers=max(1, logical_cpus - 2),
        )

    def to_jsonable(self) -> dict[str, Any]:
        result = asdict(self)
        result["profile"] = self.profile.value
        return result


@dataclass(frozen=True)
class NvidiaSnapshot:
    timestamp_monotonic: float
    temperature_c: int
    gpu_utilization_percent: int
    memory_used_bytes: int
    memory_total_bytes: int
    power_watts: float


def ensure_output_budget(planned_bytes: int, limits: ResourceLimits) -> None:
    if planned_bytes < 0:
        raise ValueError("planned output size must be nonnegative")
    if planned_bytes > limits.output_bytes:
        raise ResourceLimitExceeded(
            f"planned output {planned_bytes} exceeds limit {limits.output_bytes} bytes"
        )


def ensure_disk_budget(path: Path, planned_bytes: int, limits: ResourceLimits) -> None:
    ensure_output_budget(planned_bytes, limits)
    existing = Path(path).resolve()
    while not existing.exists():
        if existing.parent == existing:
            raise FileNotFoundError(path)
        existing = existing.parent
    free_bytes = shutil.disk_usage(existing).free
    required = planned_bytes + limits.disk_reserve_bytes
    if free_bytes < required:
        raise ResourceLimitExceeded(
            f"free disk {free_bytes} is below planned output plus reserve {required} bytes"
        )


def check_wall_time(started_monotonic: float, limits: ResourceLimits) -> float:
    elapsed = time.monotonic() - started_monotonic
    if elapsed > limits.wall_seconds:
        raise ResourceLimitExceeded(
            f"elapsed time {elapsed:.3f}s exceeds limit {limits.wall_seconds:.3f}s"
        )
    return elapsed


def apply_address_space_limit(ram_bytes: int) -> None:
    """Apply a Linux address-space ceiling to the current process.

    Call this only in a dedicated experiment child process because lowering a
    hard limit cannot generally be undone.
    """
    if ram_bytes <= 0:
        raise ValueError("RAM limit must be positive")
    import resource

    resource.setrlimit(resource.RLIMIT_AS, (ram_bytes, ram_bytes))


def query_nvidia_snapshot(executable: str = "nvidia-smi") -> NvidiaSnapshot:
    """Read GPU telemetry without changing device state."""
    fields = (
        "temperature.gpu,utilization.gpu,memory.used,memory.total,power.draw"
    )
    completed = subprocess.run(
        (
            executable,
            f"--query-gpu={fields}",
            "--format=csv,noheader,nounits",
        ),
        check=True,
        capture_output=True,
        text=True,
        timeout=10,
    )
    lines = [line.strip() for line in completed.stdout.splitlines() if line.strip()]
    if len(lines) != 1:
        raise RuntimeError(f"expected exactly one NVIDIA GPU, received {len(lines)}")
    values = [value.strip() for value in lines[0].split(",")]
    if len(values) != 5:
        raise RuntimeError(f"unexpected nvidia-smi telemetry: {lines[0]!r}")
    temperature, utilization, memory_used_mib, memory_total_mib, power = values
    return NvidiaSnapshot(
        timestamp_monotonic=time.monotonic(),
        temperature_c=int(temperature),
        gpu_utilization_percent=int(utilization),
        memory_used_bytes=int(memory_used_mib) * 1024**2,
        memory_total_bytes=int(memory_total_mib) * 1024**2,
        power_watts=float(power),
    )


def check_gpu_snapshot(snapshot: NvidiaSnapshot, limits: ResourceLimits) -> str:
    if snapshot.temperature_c >= limits.gpu_abort_temperature_c:
        raise ResourceLimitExceeded(
            f"GPU temperature {snapshot.temperature_c}C reached abort threshold "
            f"{limits.gpu_abort_temperature_c}C"
        )
    if snapshot.temperature_c >= limits.gpu_pause_temperature_c:
        return "pause"
    if snapshot.memory_used_bytes > limits.gpu_memory_bytes:
        return "reduce-chunk"
    return "continue"


def atomic_write_checkpoint(path: Path, checkpoint: dict[str, Any]) -> None:
    """Atomically replace a resumable JSON checkpoint."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(checkpoint, stream, indent=2, sort_keys=True)
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


class GracefulInterruption:
    """Context manager that converts SIGINT/SIGTERM into a polled flag."""

    def __init__(self) -> None:
        self.requested = False
        self.signal_number: int | None = None
        self._previous: dict[int, Any] = {}

    def _handler(self, signal_number: int, _frame: FrameType | None) -> None:
        self.requested = True
        self.signal_number = signal_number

    def __enter__(self) -> "GracefulInterruption":
        for signal_number in (signal.SIGINT, signal.SIGTERM):
            self._previous[signal_number] = signal.getsignal(signal_number)
            signal.signal(signal_number, self._handler)
        return self

    def __exit__(self, _type: Any, _value: Any, _traceback: Any) -> None:
        for signal_number, previous in self._previous.items():
            signal.signal(signal_number, previous)
