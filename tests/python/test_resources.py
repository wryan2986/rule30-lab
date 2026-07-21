from __future__ import annotations

import json
import time
from dataclasses import replace
from pathlib import Path

import pytest

from rule30lab.resources import (
    NvidiaSnapshot,
    ResourceLimitExceeded,
    ResourceLimits,
    ResourceProfile,
    atomic_write_checkpoint,
    check_gpu_snapshot,
    check_wall_time,
    ensure_disk_budget,
    ensure_output_budget,
)


def test_profiles_leave_interactive_headroom() -> None:
    interactive = ResourceLimits.conservative(ResourceProfile.INTERACTIVE)
    idle = ResourceLimits.conservative(ResourceProfile.IDLE)
    assert interactive.cpu_workers <= idle.cpu_workers
    assert interactive.ram_bytes < idle.ram_bytes
    assert interactive.gpu_memory_bytes < idle.gpu_memory_bytes
    assert interactive.gpu_abort_temperature_c < 89
    assert idle.gpu_abort_temperature_c < 89


def test_output_and_disk_budgets(tmp_path: Path) -> None:
    limits = replace(
        ResourceLimits.conservative(), output_bytes=100, disk_reserve_bytes=0
    )
    ensure_output_budget(100, limits)
    ensure_disk_budget(tmp_path / "future" / "result.json", 100, limits)
    with pytest.raises(ResourceLimitExceeded):
        ensure_output_budget(101, limits)
    with pytest.raises(ValueError):
        ensure_output_budget(-1, limits)


def test_wall_limit() -> None:
    limits = replace(ResourceLimits.conservative(), wall_seconds=0.01)
    assert check_wall_time(time.monotonic(), limits) >= 0
    with pytest.raises(ResourceLimitExceeded):
        check_wall_time(time.monotonic() - 1, limits)


def test_gpu_actions_are_read_only_policy_decisions() -> None:
    limits = replace(
        ResourceLimits.conservative(),
        gpu_memory_bytes=4_000,
        gpu_pause_temperature_c=78,
        gpu_abort_temperature_c=84,
    )
    ordinary = NvidiaSnapshot(0.0, 60, 10, 3_000, 8_000, 100.0)
    assert check_gpu_snapshot(ordinary, limits) == "continue"
    assert check_gpu_snapshot(replace(ordinary, memory_used_bytes=4_001), limits) == "reduce-chunk"
    assert check_gpu_snapshot(replace(ordinary, temperature_c=78), limits) == "pause"
    with pytest.raises(ResourceLimitExceeded):
        check_gpu_snapshot(replace(ordinary, temperature_c=84), limits)


def test_checkpoint_write_is_atomic(tmp_path: Path) -> None:
    path = tmp_path / "checkpoints" / "state.json"
    atomic_write_checkpoint(path, {"next": 17, "complete": False})
    assert json.loads(path.read_text(encoding="utf-8")) == {
        "complete": False,
        "next": 17,
    }
    assert not list(path.parent.glob("*.tmp"))
