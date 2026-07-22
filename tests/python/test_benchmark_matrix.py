from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPOSITORY_ROOT))

import experiments.shared.run_benchmark_matrix as matrix
from experiments.shared.run_benchmark_matrix import (
    CommandSpec,
    MatrixError,
    ProcessResult,
    ProcessRunner,
    RSS_MARKER,
    benchmark_deterministic_json,
    benchmark_generation,
    build_generation_commands,
    build_predictor_command,
    build_statistics_command,
    git_provenance,
    timing_summary,
)


class FakeRunner:
    """Deterministic subprocess stand-in; it never invokes a GPU or executable."""

    def __init__(self, outputs: Mapping[str, bytes]) -> None:
        self.outputs = dict(outputs)
        self.calls: list[tuple[str, ...]] = []

    def run(
        self,
        argv: Sequence[str],
        *,
        cwd: Path,
        environment: Mapping[str, str],
        check: bool = True,
    ) -> ProcessResult:
        del cwd, environment, check
        command = tuple(argv)
        self.calls.append(command)
        key = command[-1]
        call_number = sum(call[-1] == key for call in self.calls)
        stderr = (
            b"__RULE30_TARGET_MAX_RSS_KIB__=2048\n"
            if any(argument.startswith(RSS_MARKER) for argument in command)
            else b""
        )
        return ProcessResult(
            argv=command,
            returncode=0,
            stdout=self.outputs[key],
            stderr=stderr,
            elapsed_seconds=call_number / 1000.0,
            peak_rss_kib=1_000 + call_number,
        )


def _fake_commands(names: Sequence[str]) -> list[CommandSpec]:
    return [
        CommandSpec(
            name,
            ("/usr/bin/nice", "-n", "10", "/fake/explicit-executable", name),
        )
        for name in names
    ]


def test_timing_summary_uses_population_standard_deviation() -> None:
    report = timing_summary([1.0, 2.0, 3.0, 4.0])
    assert report["minimum"] == 1.0
    assert report["median"] == 2.5
    assert report["maximum"] == 4.0
    assert report["mean"] == 2.5
    assert report["population_standard_deviation"] == pytest.approx(
        math.sqrt(1.25)
    )
    assert "subprocess end-to-end" in report["scope"]


@pytest.mark.parametrize("samples", [[], [-1.0], [math.inf], [math.nan]])
def test_timing_summary_rejects_invalid_samples(samples: list[float]) -> None:
    with pytest.raises(MatrixError):
        timing_summary(samples)


def test_generation_commands_are_explicit_and_use_one_identical_count() -> None:
    commands = build_generation_commands(
        count=257,
        python_executable=Path("/opt/rule30/python"),
        cpp_executable=Path("/opt/rule30/rule30_cpp"),
        rust_executable=Path("/opt/rule30/rule30-rust"),
        cuda_executable=Path("/opt/rule30/rule30_cuda_generate"),
        nice_executable=Path("/usr/bin/nice"),
        nice_level=10,
        cuda_device=0,
        cuda_threads=128,
        cuda_memory_budget_mib=64,
        cuda_output_budget_mib=16,
    )
    assert [command.name for command in commands] == [
        "python-coordinate",
        "cpp-scalar",
        "cpp-avx2",
        "rust-packed",
        "cuda-direct",
    ]
    for command in commands:
        assert Path(command.argv[0]).is_absolute()
        assert command.argv[:3] == ("/usr/bin/nice", "-n", "10")
        count_index = command.argv.index("--count")
        assert command.argv[count_index + 1] == "257"
        assert command.argv[command.argv.index("--format") + 1] == "raw"
    assert "python" in commands[0].argv
    assert commands[1].argv[commands[1].argv.index("--backend") + 1] == "scalar"
    assert commands[2].argv[commands[2].argv.index("--backend") + 1] == "avx2"
    assert commands[3].argv[commands[3].argv.index("--backend") + 1] == "packed"
    assert "--device" in commands[4].argv
    assert "--memory-budget-mib" in commands[4].argv


def test_generation_matrix_verifies_every_byte_before_timing() -> None:
    names = (
        "python-coordinate",
        "cpp-scalar",
        "cpp-avx2",
        "rust-packed",
        "cuda-direct",
    )
    bits = bytes([1, 1, 0, 1, 1, 1, 0, 0])
    runner = FakeRunner({name: bits for name in names})
    report = benchmark_generation(
        _fake_commands(names),
        count=len(bits),
        trusted_reference=bits,
        warmups=1,
        repetitions=2,
        time_executable=Path("/usr/bin/time"),
        runner=runner,  # type: ignore[arg-type]
        environment={},
    )

    assert report["pre_timing_verification"]["full_byte_equality"] is True
    assert report["pre_timing_verification"]["reference_backend"] == "trusted-vector"
    assert report["protocol"]["all_warmup_and_measured_outputs_matched"] is True
    assert report["output"]["size_bytes"] == len(bits)
    assert report["output"]["ones"] == 5
    assert len(runner.calls) == len(names) * (1 + 1 + 2 + 1)
    assert report["protocol"]["measured_orders"][0] != report["protocol"][
        "measured_orders"
    ][1]
    for backend in names:
        assert len(report["backends"][backend]["timing"]["samples"]) == 2
        rss = report["backends"][backend]["host_peak_rss"]
        assert rss["reliable"] is True
        assert rss["peak_rss_kib"] == 2048
        assert rss["included_in_timing_samples"] is False


def test_generation_mismatch_aborts_before_warmup_or_timing() -> None:
    names = ("reference", "wrong", "third")
    runner = FakeRunner(
        {
            "reference": b"\x01\x00\x01",
            "wrong": b"\x01\x01\x01",
            "third": b"\x01\x00\x01",
        }
    )
    with pytest.raises(MatrixError, match="differs"):
        benchmark_generation(
            _fake_commands(names),
            count=3,
            trusted_reference=b"\x01\x00\x01",
            warmups=1,
            repetitions=2,
            time_executable=Path("/usr/bin/time"),
            runner=runner,  # type: ignore[arg-type]
            environment={},
        )
    assert len(runner.calls) == 2


def test_generation_rejects_non_numeric_bit_output() -> None:
    runner = FakeRunner({"left": b"010", "right": b"010"})
    with pytest.raises(MatrixError, match="non-bit byte"):
        benchmark_generation(
            _fake_commands(("left", "right")),
            count=3,
            trusted_reference=b"\x01\x00\x01",
            warmups=0,
            repetitions=1,
            time_executable=Path("/usr/bin/time"),
            runner=runner,  # type: ignore[arg-type]
            environment={},
        )


def test_generation_all_backends_wrong_cannot_outvote_trusted_vector() -> None:
    names = ("one", "two", "three", "four", "five")
    wrong = b"\x01\x01\x01"
    runner = FakeRunner({name: wrong for name in names})
    with pytest.raises(MatrixError, match="trusted vector"):
        benchmark_generation(
            _fake_commands(names),
            count=3,
            trusted_reference=b"\x01\x00\x01",
            warmups=1,
            repetitions=1,
            time_executable=Path("/usr/bin/time"),
            runner=runner,  # type: ignore[arg-type]
            environment={},
        )
    assert len(runner.calls) == 1


def test_deterministic_json_workload_is_repeated_and_hashed() -> None:
    payload = {
        "experiment_id": "fake-bounded-search",
        "question": "problem3",
        "hypothesis": "bounded fixture",
        "backend": "python",
        "parameters": {
            "limit_bits": 5000,
            "train_length": 2500,
            "max_reported_errors": 8,
            "dfao": {
                "min_states": 1,
                "max_states": 3,
                "start_state": None,
                "start_model_id": 0,
                "max_models": 100000,
                "max_state_count_cap": 16,
            },
            "two_kernel": {
                "depth": 4,
                "fingerprint_length": 64,
                "max_nodes": 131071,
                "max_fingerprint_bytes": 67108864,
            },
            "gf2": {
                "max_order": 12,
                "start_candidate_id": 0,
                "max_candidates": 1000000,
                "max_order_cap": 64,
            },
            "boolean_recurrence": {
                "min_window": 1,
                "max_window": 12,
                "start_window": None,
                "start_completion_id": 0,
                "max_completions": 1000000,
                "max_unseen_contexts": 20,
                "max_table_entries": 1048576,
            },
        },
        "status": "finite-exhaustive",
        "input": {
            "used_bit_count": 5000,
            "sha256_used_u8": hashlib.sha256(bytes(5000)).hexdigest(),
        },
        "training_validation_protocol": {
            "training": {"start": 0, "stop": 2500},
            "held_out": {"start": 2500, "stop": 5000},
            "leakage_control": (
                "all models and deterministic enumeration choices are fixed from "
                "training bits before held-out bits are inspected"
            ),
            "deterministic_seed": 0,
            "randomness_used": False,
        },
        "result_summary": {
            "completion": {
                "all_requested_searches_completed": True,
                "berlekamp_massey_candidate_checked": True,
                "boolean_completed": True,
                "dfao_completed": True,
                "gf2_completed": True,
                "kernel_construction_checked": True,
            }
        },
        "interpretation": "finite fixture",
        "proof_scope": "fixture only",
        "limitations": ["fixture only"],
    }
    encoded = json.dumps(payload, sort_keys=True).encode()
    runner = FakeRunner({"bounded-predictor-search": encoded})
    report = benchmark_deterministic_json(
        CommandSpec(
            "bounded-predictor-search",
            (
                "/usr/bin/nice",
                "-n",
                "10",
                "/fake/explicit-executable",
                "bounded-predictor-search",
            ),
        ),
        expected_question="problem3",
        expected_input=bytes(5000),
        warmups=1,
        repetitions=3,
        time_executable=Path("/usr/bin/time"),
        runner=runner,  # type: ignore[arg-type]
        environment={},
    )
    assert len(runner.calls) == 6
    assert report["protocol"]["all_outputs_matched_byte_for_byte"] is True
    assert report["deterministic_output"]["size_bytes"] == len(encoded)
    assert report["deterministic_output"]["reported_fields"]["completion"] == {
        "all_requested_searches_completed": True,
        "berlekamp_massey_candidate_checked": True,
        "boolean_completed": True,
        "dfao_completed": True,
        "gf2_completed": True,
        "kernel_construction_checked": True,
    }

    bad_payload = json.loads(encoded)
    bad_payload["parameters"]["dfao"]["max_states"] = 4
    bad_runner = FakeRunner(
        {"bounded-predictor-search": json.dumps(bad_payload, sort_keys=True).encode()}
    )
    with pytest.raises(MatrixError, match="parameters differ"):
        benchmark_deterministic_json(
            CommandSpec(
                "bounded-predictor-search",
                (
                    "/usr/bin/nice",
                    "-n",
                    "10",
                    "/fake/explicit-executable",
                    "bounded-predictor-search",
                ),
            ),
            expected_question="problem3",
            expected_input=bytes(5000),
            warmups=0,
            repetitions=1,
            time_executable=Path("/usr/bin/time"),
            runner=bad_runner,  # type: ignore[arg-type]
            environment={},
        )


def test_analysis_commands_pin_all_material_parameters(tmp_path: Path) -> None:
    prefix = tmp_path / "trusted.u8"
    prefix.write_bytes(b"\x01\x00")
    common = {
        "python_executable": Path("/opt/rule30/python"),
        "trusted_prefix": prefix,
        "nice_executable": Path("/usr/bin/nice"),
        "nice_level": 10,
    }
    stats = build_statistics_command(**common)
    predictor = build_predictor_command(**common)
    assert str(prefix) in stats.argv
    assert "--checkpoints" in stats.argv
    assert "--block-widths" in stats.argv
    assert "--linear-prefixes" in stats.argv
    assert "--limit-bits" in predictor.argv
    assert predictor.argv[predictor.argv.index("--limit-bits") + 1] == "5000"
    assert predictor.argv[predictor.argv.index("--train-length") + 1] == "2500"
    assert "--dfao-max-states" in predictor.argv
    assert predictor.argv[predictor.argv.index("--kernel-depth") + 1] == "4"
    assert predictor.argv[predictor.argv.index("--kernel-fingerprint-length") + 1] == "64"
    assert "--gf2-max-order" in predictor.argv
    assert "--boolean-max-window" in predictor.argv


def test_process_runner_captures_peak_rss_without_shell(tmp_path: Path) -> None:
    runner = ProcessRunner(timeout_seconds=2.0, max_capture_bytes=4096)
    result = runner.run(
        (sys.executable, "-c", "import sys; sys.stdout.buffer.write(bytes([1,0,1]))"),
        cwd=tmp_path,
        environment={"LC_ALL": "C"},
    )
    assert result.stdout == b"\x01\x00\x01"
    assert result.stderr == b""
    assert result.returncode == 0
    assert result.elapsed_seconds >= 0.0
    assert result.peak_rss_kib is not None
    assert result.peak_rss_kib > 0


def test_process_runner_enforces_combined_output_cap(tmp_path: Path) -> None:
    runner = ProcessRunner(timeout_seconds=2.0, max_capture_bytes=1024)
    with pytest.raises(MatrixError, match="stdout/stderr cap"):
        runner.run(
            (sys.executable, "-c", "import sys; sys.stdout.write('x' * 4096)"),
            cwd=tmp_path,
            environment={"LC_ALL": "C"},
        )


def test_process_runner_enforces_wall_timeout(tmp_path: Path) -> None:
    runner = ProcessRunner(timeout_seconds=0.05, max_capture_bytes=1024)
    with pytest.raises(MatrixError, match="wall cap"):
        runner.run(
            (sys.executable, "-c", "import time; time.sleep(2)"),
            cwd=tmp_path,
            environment={"LC_ALL": "C"},
        )


def test_process_runner_timeout_covers_pipe_inheriting_descendant(
    tmp_path: Path,
) -> None:
    runner = ProcessRunner(timeout_seconds=0.08, max_capture_bytes=1024)
    source = (
        "import subprocess,sys;"
        "subprocess.Popen([sys.executable,'-c','import time;time.sleep(10)'],"
        "stdout=sys.stdout,stderr=sys.stderr)"
    )
    with pytest.raises(MatrixError, match="wall cap"):
        runner.run(
            (sys.executable, "-c", source),
            cwd=tmp_path,
            environment={"LC_ALL": "C"},
        )


def test_process_runner_timeout_bounds_detached_pipe_holder(
    tmp_path: Path,
) -> None:
    runner = ProcessRunner(timeout_seconds=0.05, max_capture_bytes=1024)
    source = (
        "import subprocess,sys;"
        "subprocess.Popen([sys.executable,'-c','import time;time.sleep(2)'],"
        "stdout=sys.stdout,stderr=sys.stderr,start_new_session=True)"
    )
    started = time.monotonic()
    with pytest.raises(MatrixError, match="wall cap"):
        runner.run(
            (sys.executable, "-c", source),
            cwd=tmp_path,
            environment={"LC_ALL": "C"},
        )
    assert time.monotonic() - started < 1.0


def test_process_runner_rejects_path_lookup() -> None:
    runner = ProcessRunner(timeout_seconds=1.0, max_capture_bytes=1024)
    with pytest.raises(MatrixError, match="must be absolute"):
        runner.run(
            ("python", "--version"),
            cwd=Path.cwd(),
            environment={},
        )


def test_persistent_provenance_requires_clean_complete_worktree(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository = tmp_path / "repo"
    required_files = (
        "experiments/shared/run_benchmark_matrix.py",
        "src/python/marker.py",
        "src/cpp/marker.cpp",
        "src/cuda/marker.cu",
        "src/rust/marker.rs",
        "experiments/problem2_balance/marker.py",
        "experiments/problem3_complexity/marker.py",
        "tests/reference_vectors/marker.u8",
    )
    for relative in required_files:
        path = repository / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(relative + "\n", encoding="utf-8")
    subprocess.run(("/usr/bin/git", "init", "-q"), cwd=repository, check=True)
    subprocess.run(("/usr/bin/git", "add", "."), cwd=repository, check=True)
    subprocess.run(
        (
            "/usr/bin/git",
            "-c",
            "user.name=Rule30 Test",
            "-c",
            "user.email=rule30-test@example.invalid",
            "commit",
            "-q",
            "-m",
            "fixture",
        ),
        cwd=repository,
        check=True,
    )
    monkeypatch.setattr(matrix, "REPOSITORY_ROOT", repository)
    runner = ProcessRunner(timeout_seconds=2.0, max_capture_bytes=1024 * 1024)
    environment = {"LC_ALL": "C", "PATH": "/usr/bin:/bin"}

    clean = git_provenance(
        git_executable=Path("/usr/bin/git"),
        runner=runner,
        environment=environment,
    )
    assert clean["script_byte_identical_to_head"] is True
    assert clean["worktree_clean_before_benchmark"] is True
    assert clean["persistent_record_eligible"] is True

    script = repository / "experiments/shared/run_benchmark_matrix.py"
    script.write_text("changed\n", encoding="utf-8")
    dirty = git_provenance(
        git_executable=Path("/usr/bin/git"),
        runner=runner,
        environment=environment,
    )
    assert dirty["script_byte_identical_to_head"] is False
    assert dirty["worktree_clean_before_benchmark"] is False
    assert dirty["persistent_record_eligible"] is False
