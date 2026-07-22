from __future__ import annotations

import hashlib
import json
import signal
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from rule30lab import controlled_runner as runner
from rule30lab.records import atomic_write_json as real_atomic_write_json
from rule30lab.records import validate_record
from rule30lab.resources import NvidiaSnapshot, ResourceLimits, ResourceProfile


_SUCCESS_SCRIPT = """
import json
import sys

print(json.dumps({
    "schema_version": 1,
    "experiment_id": "tiny-child-v1",
    "question": "problem2",
    "hypothesis": "tiny bounded fixture",
    "backend": "python-test-child",
    "parameters": {"argv": sys.argv[1:]},
    "result_summary": {"value": 7},
    "status": "empirical",
    "proof_scope": "the tiny fixture only",
    "interpretation": "fixture output",
    "limitations": ["fixture only"]
}, sort_keys=True))
"""


class Harness:
    def __init__(
        self,
        repository: Path,
        allowlist: dict[str, runner.ExperimentSpec],
    ) -> None:
        self.repository = repository
        self.allowlist = allowlist
        self.counter = 0

    def add_script(
        self,
        source: str,
        *,
        name: str = "tiny",
        relative: Path | None = None,
    ) -> Path:
        relative = relative or Path("experiments/tiny.py")
        script = self.repository / relative
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text(source, encoding="utf-8")
        self.allowlist[name] = runner.ExperimentSpec(
            relative_path=relative,
            question="problem2",
            hypothesis="tiny bounded fixture",
            default_status="empirical",
            proof_scope="the tiny fixture only",
            limitations=("fixture only",),
        )
        return script

    def configuration(
        self,
        *,
        name: str = "tiny",
        child_args: tuple[str, ...] = (),
        wall_seconds: float = 2.0,
        stdout_cap_bytes: int = 64 * 1024,
        stderr_cap_bytes: int = 64 * 1024,
        telemetry_enabled: bool = False,
        resume_from: Path | None = None,
        experiment_id: str | None = None,
    ) -> runner.RunnerConfiguration:
        self.counter += 1
        limits = replace(
            ResourceLimits.conservative(ResourceProfile.INTERACTIVE),
            wall_seconds=wall_seconds,
            ram_bytes=256 * 1024**2,
            gpu_memory_bytes=32 * 1024**2,
            output_bytes=4 * 1024**2,
            disk_reserve_bytes=0,
            progress_seconds=0.02,
            gpu_pause_temperature_c=70,
            gpu_abort_temperature_c=80,
            cpu_workers=1,
        )
        return runner.RunnerConfiguration(
            experiment=name,
            child_args=child_args,
            run_directory=self.repository / "results" / "runs",
            experiment_id=experiment_id or f"tiny-run-{self.counter}",
            limits=limits,
            stdout_cap_bytes=stdout_cap_bytes,
            stderr_cap_bytes=stderr_cap_bytes,
            telemetry_enabled=telemetry_enabled,
            telemetry_seconds=0.01,
            termination_grace_seconds=0.05,
            resume_from=resume_from,
        )


@pytest.fixture
def harness(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Harness:
    repository = tmp_path / "repository"
    repository.mkdir()
    allowlist: dict[str, runner.ExperimentSpec] = {}
    monkeypatch.setattr(runner, "REPOSITORY_ROOT", repository)
    monkeypatch.setattr(runner, "EXPERIMENT_ALLOWLIST", allowlist)
    monkeypatch.setattr(runner, "_git_commit", lambda _root: "a" * 40)
    monkeypatch.setattr(runner, "_git_worktree_status", lambda _root: "")
    monkeypatch.setattr(runner, "_read_cpu_model", lambda: "test CPU")
    monkeypatch.setattr(runner, "_read_memory_total_bytes", lambda: 123456789)
    return Harness(repository, allowlist)


def _record(result: runner.RunResult) -> dict[str, Any]:
    return json.loads(result.record_path.read_text(encoding="utf-8"))


def _snapshot(
    *, temperature: int = 50, memory_used: int = 1, utilization: int = 2
) -> NvidiaSnapshot:
    return NvidiaSnapshot(
        timestamp_monotonic=0.0,
        temperature_c=temperature,
        gpu_utilization_percent=utilization,
        memory_used_bytes=memory_used,
        memory_total_bytes=128 * 1024**2,
        power_watts=42.0,
    )


def test_success_streams_atomic_artifacts_and_strict_record(
    harness: Harness, capsys: pytest.CaptureFixture[str]
) -> None:
    harness.add_script(_SUCCESS_SCRIPT)
    config = harness.configuration(child_args=("--alpha", "7"))

    result = runner.run_controlled_experiment(config)

    assert result.outcome is runner.RunOutcome.SUCCESS
    assert result.stdout_path.suffix == ".data"
    assert result.checkpoint_path.suffix == ".state"
    assert result.child_returncode == 0
    child = json.loads(result.stdout_path.read_text(encoding="utf-8"))
    assert child["parameters"]["argv"] == ["--alpha", "7"]
    record = _record(result)
    validate_record(record)
    assert record["status"] == "empirical"
    assert record["question"] == "problem2"
    assert record["parameters"]["execution_policy"]["local_only"] is True
    assert record["parameters"]["execution_policy"]["shell"] is False
    assert record["result_summary"]["stdout"]["child_stream_eof_observed"] is True
    assert record["result_summary"]["stdout"]["truncated_by_cap"] is False
    assert record["parameters"]["resume_semantics"] == {
        "child_continuation_supported": False,
        "mode": "restart-child-from-beginning",
    }
    stdout_bytes = result.stdout_path.read_bytes()
    assert record["result_hashes"]["stdout_sha256"] == hashlib.sha256(
        stdout_bytes
    ).hexdigest()
    checkpoint = json.loads(result.checkpoint_path.read_text(encoding="utf-8"))
    assert checkpoint["complete"] is True
    assert checkpoint["state"] == "complete"
    assert checkpoint["child_continuation_supported"] is False
    assert checkpoint["resume"]["mid_script_continuation_supported"] is False
    assert not list(result.record_path.parent.glob("*.tmp"))
    progress_lines = [
        json.loads(line)
        for line in capsys.readouterr().err.splitlines()
        if line.strip()
    ]
    assert progress_lines
    assert all(
        line["type"] == "rule30-controlled-runner-progress"
        for line in progress_lines
    )
    assert progress_lines[-1]["state"] == "complete"


def test_timeout_terminates_child_and_writes_inconclusive_record(
    harness: Harness,
) -> None:
    harness.add_script("import time\ntime.sleep(10)\n")
    config = harness.configuration(wall_seconds=0.06)

    result = runner.run_controlled_experiment(config)

    assert result.outcome is runner.RunOutcome.TIMEOUT
    assert result.child_returncode is not None
    assert _record(result)["status"] == "inconclusive"
    checkpoint = json.loads(result.checkpoint_path.read_text(encoding="utf-8"))
    assert checkpoint["complete"] is False
    assert checkpoint["state"] == "timeout"
    assert checkpoint["resume"]["restart_required"] is True


def test_timeout_kills_pipe_inheriting_descendant_after_parent_exits(
    harness: Harness,
) -> None:
    harness.add_script(
        """
import subprocess
import sys

subprocess.Popen(
    [sys.executable, "-c", "import time; time.sleep(10)"],
    stdout=sys.stdout,
    stderr=sys.stderr,
)
"""
    )
    started = time.monotonic()
    result = runner.run_controlled_experiment(
        harness.configuration(wall_seconds=0.08)
    )
    elapsed = time.monotonic() - started

    assert result.outcome is runner.RunOutcome.TIMEOUT
    assert elapsed < 1.0


@pytest.mark.parametrize(
    ("descriptor", "stdout_cap", "stderr_cap", "expected_path"),
    [
        (1, 31, 64 * 1024, "stdout_path"),
        (2, 64 * 1024, 31, "stderr_path"),
    ],
)
def test_streaming_output_caps_are_hard(
    harness: Harness,
    descriptor: int,
    stdout_cap: int,
    stderr_cap: int,
    expected_path: str,
) -> None:
    harness.add_script(
        f"import os, time\nos.write({descriptor}, b'x' * 1000000)\ntime.sleep(10)\n"
    )
    config = harness.configuration(
        stdout_cap_bytes=stdout_cap,
        stderr_cap_bytes=stderr_cap,
    )

    result = runner.run_controlled_experiment(config)

    assert result.outcome is runner.RunOutcome.OUTPUT_LIMIT
    limited_path = getattr(result, expected_path)
    assert limited_path.stat().st_size == 31
    record = _record(result)
    stream_name = "stdout" if descriptor == 1 else "stderr"
    assert record["result_summary"][stream_name]["bytes_captured"] == 31
    assert record["result_summary"][stream_name]["truncated_by_cap"] is True
    assert (
        record["result_summary"][stream_name]["child_stream_eof_observed"] is False
    )
    assert "hard cap 31 bytes" in record["result_summary"]["reason"]


def test_address_space_setup_hook_uses_shared_primitive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[int] = []
    monkeypatch.setattr(runner, "apply_address_space_limit", calls.append)

    setup = runner._make_child_preexec(987654)
    setup()

    assert calls == [987654]


def test_interruption_terminates_and_atomically_checkpoints(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    harness.add_script("import time\ntime.sleep(10)\n")

    class ImmediateInterruption:
        requested = True
        signal_number = signal.SIGTERM

        def __enter__(self) -> "ImmediateInterruption":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

    monkeypatch.setattr(runner, "GracefulInterruption", ImmediateInterruption)
    result = runner.run_controlled_experiment(harness.configuration())

    assert result.outcome is runner.RunOutcome.INTERRUPTED
    assert result.exit_code == 128 + signal.SIGTERM
    checkpoint = json.loads(result.checkpoint_path.read_text(encoding="utf-8"))
    assert checkpoint["state"] == "interrupted"
    assert checkpoint["complete"] is False
    assert checkpoint["stdout"]["sha256_captured"] == hashlib.sha256(
        result.stdout_path.read_bytes()
    ).hexdigest()
    assert not list(result.checkpoint_path.parent.glob("*.tmp"))


def test_resume_validates_checkpoint_but_restarts_child(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    harness.add_script(_SUCCESS_SCRIPT)
    real_interruption = runner.GracefulInterruption

    class ImmediateInterruption:
        requested = True
        signal_number = signal.SIGINT

        def __enter__(self) -> "ImmediateInterruption":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

    experiment_id = "resume-fixture"
    first_config = harness.configuration(experiment_id=experiment_id)
    monkeypatch.setattr(runner, "GracefulInterruption", ImmediateInterruption)
    first = runner.run_controlled_experiment(first_config)
    assert first.outcome is runner.RunOutcome.INTERRUPTED

    monkeypatch.setattr(runner, "GracefulInterruption", real_interruption)
    resumed_config = replace(first_config, resume_from=first.checkpoint_path)
    resumed = runner.run_controlled_experiment(resumed_config)

    assert resumed.outcome is runner.RunOutcome.SUCCESS
    checkpoint = json.loads(resumed.checkpoint_path.read_text(encoding="utf-8"))
    assert checkpoint["attempt"] == 2
    assert checkpoint["resumed_from"]["mode"] == "validated-restart-from-beginning"
    record = _record(resumed)
    assert record["parameters"]["resume"]["mid_script_continuation"] is False
    assert "from the beginning" in " ".join(record["limitations"])


def test_resume_rejects_different_argv(harness: Harness) -> None:
    harness.add_script("import time\ntime.sleep(10)\n")
    config = harness.configuration(wall_seconds=0.04, child_args=("--one",))
    first = runner.run_controlled_experiment(config)
    assert first.outcome is runner.RunOutcome.TIMEOUT
    mismatched = replace(
        config,
        child_args=("--two",),
        resume_from=first.checkpoint_path,
    )

    with pytest.raises(runner.RunnerConfigurationError, match="argv does not match"):
        runner.run_controlled_experiment(mismatched)


def test_resume_is_bound_to_exact_artifact_directory(harness: Harness) -> None:
    harness.add_script("import time\ntime.sleep(10)\n")
    config = harness.configuration(wall_seconds=0.04, experiment_id="bound-resume")
    first = runner.run_controlled_experiment(config)
    copied = harness.repository / "results" / "runs" / "copied.checkpoint.state"
    copied.write_bytes(first.checkpoint_path.read_bytes())
    other = replace(
        config,
        run_directory=harness.repository / "results" / "runs" / "other",
        resume_from=copied,
    )
    with pytest.raises(runner.RunnerConfigurationError, match="exact run directory"):
        runner.run_controlled_experiment(other)


def test_unlisted_name_and_parent_escape_are_rejected(
    harness: Harness,
) -> None:
    with pytest.raises(runner.RunnerConfigurationError, match="not allowlisted"):
        runner.run_controlled_experiment(harness.configuration(name="not-a-script"))

    outside = harness.repository.parent / "outside.py"
    outside.write_text(_SUCCESS_SCRIPT, encoding="utf-8")
    harness.allowlist["escape"] = runner.ExperimentSpec(
        Path("../outside.py"),
        "problem2",
        "fixture",
        "empirical",
        "fixture",
        ("fixture",),
    )
    with pytest.raises(runner.RunnerConfigurationError, match="repository-relative"):
        runner.run_controlled_experiment(harness.configuration(name="escape"))


def test_run_directory_and_child_side_outputs_are_confined(harness: Harness) -> None:
    harness.add_script(_SUCCESS_SCRIPT)
    escaped = replace(
        harness.configuration(),
        run_directory=harness.repository.parent / "outside-runs",
    )
    with pytest.raises(runner.RunnerConfigurationError, match="controlled artifact root"):
        runner.run_controlled_experiment(escaped)

    with pytest.raises(runner.RunnerConfigurationError, match="disabled"):
        runner.run_controlled_experiment(
            harness.configuration(
                child_args=("--export-graphs-dir", "../../outside")
            )
        )


def test_symlinked_allowlisted_script_is_rejected(harness: Harness) -> None:
    outside = harness.repository.parent / "outside.py"
    outside.write_text(_SUCCESS_SCRIPT, encoding="utf-8")
    link = harness.repository / "experiments" / "linked.py"
    link.parent.mkdir(parents=True)
    try:
        link.symlink_to(outside)
    except OSError as exc:
        pytest.skip(f"symlink unavailable: {exc}")
    harness.allowlist["linked"] = runner.ExperimentSpec(
        Path("experiments/linked.py"),
        "problem2",
        "fixture",
        "empirical",
        "fixture",
        ("fixture",),
    )

    with pytest.raises(runner.RunnerConfigurationError, match="symlink"):
        runner.run_controlled_experiment(harness.configuration(name="linked"))


def test_child_process_uses_argv_and_never_a_shell(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    script = harness.add_script(_SUCCESS_SCRIPT)
    original_popen = subprocess.Popen
    observed: list[tuple[tuple[str, ...], dict[str, Any]]] = []

    def checked_popen(
        command: Sequence[str], **kwargs: Any
    ) -> subprocess.Popen[bytes]:
        observed.append((tuple(command), kwargs.copy()))
        assert kwargs["shell"] is False
        assert kwargs["stdin"] is subprocess.DEVNULL
        return original_popen(command, **kwargs)

    monkeypatch.setattr(runner.subprocess, "Popen", checked_popen)
    result = runner.run_controlled_experiment(
        harness.configuration(child_args=("argument with spaces", ";touch", "never"))
    )

    assert result.outcome is runner.RunOutcome.SUCCESS
    assert len(observed) == 1
    command, kwargs = observed[0]
    assert command == (
        sys.executable,
        "-I",
        str(script.resolve()),
        "argument with spaces",
        ";touch",
        "never",
    )
    assert kwargs["cwd"] == harness.repository
    assert not (harness.repository / "never").exists()


def test_final_record_uses_atomic_write_json_primitive(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    harness.add_script(_SUCCESS_SCRIPT)
    calls: list[Path] = []

    def recording_writer(path: Path, record: Mapping[str, Any]) -> None:
        calls.append(path)
        real_atomic_write_json(path, record)

    monkeypatch.setattr(runner, "atomic_write_json", recording_writer)
    result = runner.run_controlled_experiment(harness.configuration())

    assert calls == [result.record_path]
    validate_record(_record(result))


def test_deterministic_output_and_argv_hashes_across_attempts(
    harness: Harness,
) -> None:
    harness.add_script(_SUCCESS_SCRIPT)
    first = runner.run_controlled_experiment(
        harness.configuration(child_args=("--fixed", "1"))
    )
    second = runner.run_controlled_experiment(
        harness.configuration(child_args=("--fixed", "1"))
    )

    first_hashes = _record(first)["result_hashes"]
    second_hashes = _record(second)["result_hashes"]
    for name in (
        "stdout_sha256",
        "stderr_sha256",
        "logical_argv_sha256",
        "child_script_sha256_before",
        "child_script_sha256_after",
        "runner_module_sha256",
        "canonical_child_json_sha256",
    ):
        assert first_hashes[name] == second_hashes[name]


def test_invalid_success_output_is_inconclusive(harness: Harness) -> None:
    harness.add_script("print('not-json')\n")

    result = runner.run_controlled_experiment(harness.configuration())

    assert result.outcome is runner.RunOutcome.INVALID_OUTPUT
    record = _record(result)
    assert record["status"] == "inconclusive"
    assert record["result_summary"]["child_json_valid"] is False


def test_empty_json_object_cannot_be_promoted_to_scientific_success(
    harness: Harness,
) -> None:
    harness.add_script("print('{}')\n")
    result = runner.run_controlled_experiment(harness.configuration())
    assert result.outcome is runner.RunOutcome.INVALID_OUTPUT
    assert _record(result)["status"] == "inconclusive"


def test_computational_child_cannot_self_assign_proof_status(
    harness: Harness,
) -> None:
    harness.add_script(
        _SUCCESS_SCRIPT.replace('"empirical"', '"rigorous-proof"')
    )

    result = runner.run_controlled_experiment(harness.configuration())

    assert result.outcome is runner.RunOutcome.INVALID_OUTPUT
    record = _record(result)
    assert record["status"] == "inconclusive"
    assert "may not emit a proof status" in record["result_summary"]["reason"]


def test_module_cli_routes_child_arguments_after_delimiter(
    harness: Harness, capsys: pytest.CaptureFixture[str]
) -> None:
    harness.add_script(_SUCCESS_SCRIPT)
    exit_code = runner.main(
        [
            "--run-directory",
            str(harness.repository / "results" / "runs" / "cli-runs"),
            "--experiment-id",
            "cli-fixture",
            "--disk-reserve-mib",
            "0",
            "tiny",
            "--",
            "--value",
            "9",
        ]
    )

    assert exit_code == 0
    terminal = json.loads(capsys.readouterr().out)
    assert terminal["outcome"] == "success"
    child = json.loads(Path(terminal["stdout_path"]).read_text(encoding="utf-8"))
    assert child["parameters"]["argv"] == ["--value", "9"]


def test_telemetry_policy_decisions_use_shared_thresholds() -> None:
    limits = replace(
        ResourceLimits.conservative(),
        gpu_memory_bytes=100,
        gpu_pause_temperature_c=70,
        gpu_abort_temperature_c=80,
    )
    assert runner.classify_telemetry(
        _snapshot(temperature=69, memory_used=100), limits
    ) is runner.TelemetryAction.CONTINUE
    assert runner.classify_telemetry(
        _snapshot(temperature=70, memory_used=100), limits
    ) is runner.TelemetryAction.PAUSE
    assert runner.classify_telemetry(
        _snapshot(temperature=80, memory_used=100), limits
    ) is runner.TelemetryAction.ABORT_TEMPERATURE
    assert runner.classify_telemetry(
        _snapshot(temperature=50, memory_used=101), limits
    ) is runner.TelemetryAction.ABORT_GPU_MEMORY
    assert runner.classify_telemetry(
        _snapshot(temperature=70, memory_used=101), limits
    ) is runner.TelemetryAction.ABORT_GPU_MEMORY


def test_disabled_telemetry_never_invokes_nvidia_smi(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    harness.add_script(_SUCCESS_SCRIPT)

    def forbidden_query(*_args: object, **_kwargs: object) -> NvidiaSnapshot:
        raise AssertionError("nvidia-smi must remain optional")

    monkeypatch.setattr(runner, "query_nvidia_snapshot", forbidden_query)
    result = runner.run_controlled_experiment(harness.configuration())

    assert result.outcome is runner.RunOutcome.SUCCESS
    gpu = _record(result)["hardware"]["gpu_telemetry"]
    assert gpu["enabled"] is False
    assert gpu["queried"] is False


def test_enabled_telemetry_pauses_and_resumes_only_the_child_process(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    harness.add_script("import time\ntime.sleep(0.08)\n" + _SUCCESS_SCRIPT)
    samples = iter(
        [
            _snapshot(temperature=70),
            _snapshot(temperature=60),
            _snapshot(temperature=60),
            _snapshot(temperature=60),
            _snapshot(temperature=60),
            _snapshot(temperature=60),
            _snapshot(temperature=60),
            _snapshot(temperature=60),
            _snapshot(temperature=60),
            _snapshot(temperature=60),
        ]
    )
    monkeypatch.setattr(
        runner, "query_nvidia_snapshot", lambda **_kwargs: next(samples)
    )
    original_signal = runner._signal_process_group
    sent: list[int] = []

    def recording_signal(process: subprocess.Popen[bytes], number: int) -> None:
        sent.append(number)
        original_signal(process, number)

    monkeypatch.setattr(runner, "_signal_process_group", recording_signal)
    result = runner.run_controlled_experiment(
        harness.configuration(telemetry_enabled=True)
    )

    assert result.outcome is runner.RunOutcome.SUCCESS
    assert sent[:2] == [signal.SIGSTOP, signal.SIGCONT]
    telemetry = _record(result)["hardware"]["gpu_telemetry"]
    assert telemetry["read_only"] is True
    assert telemetry["hardware_settings_changed"] is False
    assert telemetry["pause_count"] == 1


def test_hot_gpu_telemetry_aborts_without_hardware_change(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    harness.add_script("import time\ntime.sleep(10)\n")
    monkeypatch.setattr(
        runner,
        "query_nvidia_snapshot",
        lambda **_kwargs: _snapshot(temperature=80),
    )

    result = runner.run_controlled_experiment(
        harness.configuration(telemetry_enabled=True)
    )

    assert result.outcome is runner.RunOutcome.GPU_ABORT
    record = _record(result)
    assert record["status"] == "inconclusive"
    assert record["hardware"]["hardware_settings_changed"] is False
    assert "no hardware setting was changed" in record["result_summary"]["reason"]


def test_output_and_disk_preflight_use_combined_planned_size(
    harness: Harness, monkeypatch: pytest.MonkeyPatch
) -> None:
    harness.add_script(_SUCCESS_SCRIPT)
    observed: list[tuple[Path, int]] = []

    def fake_disk(path: Path, planned: int, _limits: ResourceLimits) -> None:
        observed.append((path, planned))

    monkeypatch.setattr(runner, "ensure_disk_budget", fake_disk)
    config = harness.configuration(stdout_cap_bytes=123, stderr_cap_bytes=456)
    spec, script, artifacts, logical_hash = runner._validate_configuration(config)

    assert spec.question == "problem2"
    assert script.is_file()
    assert len(logical_hash) == 64
    assert observed == [
        (
            artifacts.record,
            123
            + 456
            + runner.RECORD_RESERVE_BYTES
            + runner.CHECKPOINT_RESERVE_BYTES,
        )
    ]
