from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import rule30lab.cli as cli
from rule30lab.cli import main


def _json_output(capsys: pytest.CaptureFixture[str]) -> dict[str, object]:
    return json.loads(capsys.readouterr().out)


def _write_executable(path: Path, body: str) -> Path:
    path.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
    path.chmod(0o755)
    return path


def _native_generator(
    path: Path,
    *,
    expected_backend: str | None,
    bits: bytes = bytes((1, 1, 0, 1, 1, 1, 0, 0)),
) -> Path:
    backend_check = (
        "assert argv[argv.index('--backend') + 1] == " + repr(expected_backend)
        if expected_backend is not None
        else "assert '--backend' not in argv"
    )
    return _write_executable(
        path,
        "import sys\n"
        "argv = sys.argv[1:]\n"
        "assert argv[0] == 'generate'\n"
        "assert argv[argv.index('--format') + 1] == 'raw'\n"
        f"{backend_check}\n"
        "count = int(argv[argv.index('--count') + 1])\n"
        f"bits = {bits!r}\n"
        "sys.stdout.buffer.write((bits * ((count + len(bits) - 1) // len(bits)))[:count])\n",
    )


def test_generate_text(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(("generate", "--count", "5")) == 0
    assert capsys.readouterr().out == "11011\n"


def test_generate_json_compatibility_alias(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(("generate", "--count", "5", "--json")) == 0
    payload = _json_output(capsys)
    assert payload["bits"] == "11011"
    assert payload["count"] == 5
    assert payload["bit_order"] == "c_0_to_c_n_minus_1"
    assert payload["status"] == "finite-exhaustive"
    assert len(str(payload["sha256_u8"])) == 64


def test_generate_explicit_json_format(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(("generate", "--count", "5", "--format", "json")) == 0
    assert _json_output(capsys)["bits"] == "11011"


def test_generate_raw_is_numeric_bytes(
    capsysbinary: pytest.CaptureFixture[bytes],
) -> None:
    assert main(("generate", "--count", "5", "--format", "raw")) == 0
    assert capsysbinary.readouterr().out == bytes((1, 1, 0, 1, 1))


def test_generate_zero_count_json(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(("generate", "--count", "0", "--json")) == 0
    payload = _json_output(capsys)
    assert payload["bits"] == ""
    assert payload["count"] == 0
    assert payload["ones"] == payload["zeros"] == 0


def test_json_alias_rejects_text_format(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit, match="2"):
        main(("generate", "--count", "5", "--json", "--format", "text"))
    assert "conflicts" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("backend", "option", "expected_native"),
    (
        ("cpp-scalar", "--cpp-executable", "scalar"),
        ("cpp-avx2", "--cpp-executable", "avx2"),
        ("rust", "--rust-executable", "packed"),
        ("cuda", "--cuda-executable", None),
    ),
)
def test_native_backend_argument_mapping(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    backend: str,
    option: str,
    expected_native: str | None,
) -> None:
    executable = _native_generator(
        tmp_path / backend.replace("-", "_"), expected_backend=expected_native
    )
    assert (
        main(
            (
                "generate",
                "--count",
                "5",
                "--backend",
                backend,
                option,
                str(executable),
                "--json",
            )
        )
        == 0
    )
    payload = _json_output(capsys)
    assert payload["backend"] == backend
    assert payload["bits"] == "11011"


def test_native_executable_environment_override(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    executable = _native_generator(
        tmp_path / "rule30-rust-env", expected_backend="packed"
    )
    monkeypatch.setenv("RULE30_RUST_EXECUTABLE", str(executable))
    assert main(("generate", "--count", "4", "--backend", "rust", "--json")) == 0
    assert _json_output(capsys)["bits"] == "1101"


def test_native_ascii_digits_are_rejected(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    executable = _write_executable(
        tmp_path / "ascii-generator",
        "import sys\nsys.stdout.buffer.write(b'11')\n",
    )
    with pytest.raises(SystemExit, match="2"):
        main(
            (
                "generate",
                "--count",
                "2",
                "--backend",
                "cpp-scalar",
                "--cpp-executable",
                str(executable),
            )
        )
    assert "non-binary raw byte" in capsys.readouterr().err


def test_native_wrong_length_and_nonzero_exit_are_clear(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    short = _write_executable(
        tmp_path / "short-generator", "import sys\nsys.stdout.buffer.write(bytes([1]))\n"
    )
    with pytest.raises(SystemExit):
        main(
            (
                "generate",
                "--count",
                "2",
                "--backend",
                "rust",
                "--rust-executable",
                str(short),
            )
        )
    assert "expected exactly 2" in capsys.readouterr().err

    failing = _write_executable(
        tmp_path / "failing-generator",
        "import sys\nsys.stderr.write('intentional failure')\nraise SystemExit(7)\n",
    )
    with pytest.raises(SystemExit):
        main(
            (
                "generate",
                "--count",
                "2",
                "--backend",
                "rust",
                "--rust-executable",
                str(failing),
            )
        )
    error = capsys.readouterr().err
    assert "status 7" in error
    assert "intentional failure" in error


def test_unavailable_native_executable_has_configuration_hint(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.delenv("RULE30_CPP_EXECUTABLE", raising=False)
    monkeypatch.setattr(cli.shutil, "which", lambda _candidate: None)
    with pytest.raises(SystemExit):
        main(("generate", "--count", "2", "--backend", "cpp-scalar"))
    error = capsys.readouterr().err
    assert "RULE30_CPP_EXECUTABLE" in error
    assert "unavailable" in error


def test_subprocess_adapter_never_uses_a_shell(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    observed: dict[str, object] = {}

    def fake_run(command: list[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        observed["command"] = command
        observed.update(kwargs)
        return subprocess.CompletedProcess(command, 0, stdout=bytes((1, 1)), stderr=b"")

    monkeypatch.setattr(cli.shutil, "which", lambda candidate: f"/fake/{candidate}")
    monkeypatch.setattr(cli.subprocess, "run", fake_run)
    assert main(("generate", "--count", "2", "--backend", "cpp-avx2", "--json")) == 0
    _json_output(capsys)
    assert observed["shell"] is False
    assert observed["command"] == [
        "/fake/rule30_cpp",
        "generate",
        "--count",
        "2",
        "--backend",
        "avx2",
        "--format",
        "raw",
    ]


def test_native_timeout_is_reported(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(cli.shutil, "which", lambda candidate: f"/fake/{candidate}")

    def timeout(*_args: object, **_kwargs: object) -> None:
        raise subprocess.TimeoutExpired("fake", 0.01)

    monkeypatch.setattr(cli.subprocess, "run", timeout)
    with pytest.raises(SystemExit):
        main(
            (
                "generate",
                "--count",
                "2",
                "--backend",
                "rust",
                "--timeout",
                "0.01",
            )
        )
    assert "timeout" in capsys.readouterr().err


def test_verify_compares_actual_bytes(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    executable = _native_generator(
        tmp_path / "cpp-correct", expected_backend="scalar"
    )
    assert (
        main(
            (
                "verify",
                "--count",
                "8",
                "--backend",
                "python",
                "--backend",
                "cpp-scalar",
                "--cpp-executable",
                str(executable),
                "--json",
            )
        )
        == 0
    )
    payload = _json_output(capsys)
    assert payload["all_equal"] is True
    comparison = payload["comparisons"][0]
    assert comparison["equal_bytes"] is True
    assert comparison["first_mismatch_index"] is None


def test_verify_reports_first_byte_mismatch(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    executable = _native_generator(
        tmp_path / "cpp-wrong",
        expected_backend="scalar",
        bits=bytes((1, 0, 0, 1, 1)),
    )
    assert (
        main(
            (
                "verify",
                "--count",
                "5",
                "--backend",
                "python",
                "--backend",
                "cpp-scalar",
                "--cpp-executable",
                str(executable),
                "--json",
            )
        )
        == 1
    )
    payload = _json_output(capsys)
    assert payload["status"] == "refuted"
    assert payload["comparisons"][0]["first_mismatch_index"] == 1


@pytest.mark.parametrize(
    "backends",
    (("python",), ("python", "python")),
)
def test_verify_requires_two_distinct_backends(
    backends: tuple[str, ...],
    capsys: pytest.CaptureFixture[str],
) -> None:
    arguments = ["verify", "--count", "5"]
    for backend in backends:
        arguments.extend(("--backend", backend))
    with pytest.raises(SystemExit):
        main(arguments)
    assert "backend" in capsys.readouterr().err


def test_benchmark_emits_repetition_statistics(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        main(
            (
                "benchmark",
                "--count",
                "5",
                "--warmups",
                "0",
                "--repetitions",
                "3",
                "--json",
            )
        )
        == 0
    )
    payload = _json_output(capsys)
    assert payload["status"] == "empirical"
    assert payload["result"]["repetitions"] == 3
    assert len(payload["result"]["seconds"]) == 3
    assert payload["result"]["deterministic_output_across_repetitions"] is True


def test_benchmark_repetition_cap(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(("benchmark", "--count", "2", "--repetitions", "51"))
    assert "capped" in capsys.readouterr().err


def test_balance_reports_exact_checkpoints(capsys: pytest.CaptureFixture[str]) -> None:
    assert (
        main(
            (
                "balance",
                "--count",
                "10",
                "--checkpoint",
                "5",
                "--checkpoint",
                "10",
                "--json",
            )
        )
        == 0
    )
    payload = _json_output(capsys)
    assert payload["status"] == "finite-exhaustive"
    assert [record["discrepancy"] for record in payload["result"]["checkpoints"]] == [
        3,
        4,
    ]
    assert payload["result"]["maximum_absolute_prefix_discrepancy"] == {
        "absolute_discrepancy": 4,
        "discrepancy": 4,
        "n": 6,
    }


def test_balance_rejects_checkpoint_beyond_count(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(("balance", "--count", "5", "--checkpoint", "6"))
    assert "checkpoint" in capsys.readouterr().err


def test_blocks_delegates_sparse_and_dense_counts(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        main(
            (
                "blocks",
                "--count",
                "8",
                "--width",
                "2",
                "--include-zero-counts",
                "--json",
            )
        )
        == 0
    )
    result = _json_output(capsys)["result"][0]
    assert result["window_count"] == 7
    assert result["counts"] == {"0": 1, "1": 1, "2": 2, "3": 3}


def test_blocks_enforces_cli_table_cap(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        main(
            (
                "blocks",
                "--count",
                "8",
                "--width",
                "2",
                "--max-table-entries",
                str(cli.MAX_BLOCK_TABLE_ENTRIES + 1),
            )
        )
    assert "cannot exceed" in capsys.readouterr().err


def test_autocorrelation_reports_exact_fraction(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(("autocorrelation", "--count", "8", "--lag", "2", "--json")) == 0
    result = _json_output(capsys)["result"][0]
    assert result["numerator"] == -2
    assert result["denominator"] == 6


def test_autocorrelation_rejects_lag_at_count(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(("autocorrelation", "--count", "8", "--lag", "8"))
    assert "smaller than prefix length" in capsys.readouterr().err


def test_linear_complexity_is_finite_prefix_value(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(("linear-complexity", "--count", "10", "--json")) == 0
    payload = _json_output(capsys)
    assert payload["result"]["linear_complexity"] == 6
    assert "finite prefix" in payload["interpretation"]


def test_linear_complexity_enforces_quadratic_work_cap(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(
            (
                "linear-complexity",
                "--count",
                str(cli.MAX_LINEAR_COMPLEXITY_BITS + 1),
                "--backend",
                "cpp-scalar",
            )
        )
    assert "linear-complexity" in capsys.readouterr().err


def test_period_search_uses_deterministic_ranking(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(("period-search", "--count", "20", "--max-period", "5", "--json")) == 0
    payload = _json_output(capsys)
    assert payload["result"]["candidate_count"] == 5
    assert payload["result"]["reported_top"][0] == {
        "matching_suffix_length": 6,
        "period": 4,
    }
    assert "not eventual periodicity" in payload["interpretation"]


@pytest.mark.parametrize(
    ("bits", "period", "expected"),
    (
        (bytes((0, 1, 0, 1)), 2, 4),
        (bytes((1, 0, 0, 1, 0, 1)), 2, 4),
    ),
)
def test_period_suffix_length_includes_the_period_base(
    bits: bytes, period: int, expected: int
) -> None:
    assert cli._matching_suffix_for_period(bits, period) == expected


def test_period_search_rejects_invalid_range(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(("period-search", "--count", "5", "--max-period", "5"))
    assert "smaller than --count" in capsys.readouterr().err


def test_true_trace_sideways_reconstructs_zero_left_prefix(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(("sideways-reconstruct", "--horizon", "8", "--json")) == 0
    result = _json_output(capsys)["result"]
    assert result["initial_left_bits"] == "0" * 8
    assert result["first_nonzero_left_depth"] is None


def test_sideways_supports_eventually_periodic_trace(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        main(
            (
                "sideways-reconstruct",
                "--horizon",
                "7",
                "--preperiod",
                "1",
                "--period",
                "01",
                "--json",
            )
        )
        == 0
    )
    result = _json_output(capsys)["result"]
    assert result["source"] == {
        "kind": "preperiod-plus-period",
        "period": "01",
        "preperiod": "1",
    }
    assert len(result["initial_left_bits"]) == 7


def test_sideways_rejects_wrong_trace_length(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(("sideways-reconstruct", "--horizon", "4", "--trace", "101"))
    assert "requires exactly 5" in capsys.readouterr().err


def test_automaticity_search_uses_equal_length_prefixes(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        main(
            (
                "automaticity-search",
                "--min-level",
                "1",
                "--max-level",
                "3",
                "--prefix-length",
                "4",
                "--json",
            )
        )
        == 0
    )
    payload = _json_output(capsys)
    assert payload["sample"]["count"] == 32
    levels = payload["result"]["levels"]
    assert [record["required_input_length"] for record in levels] == [8, 16, 32]
    assert "does not establish nonautomaticity" in payload["interpretation"]


def test_automaticity_search_rejects_insufficient_explicit_count(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(
            (
                "automaticity-search",
                "--count",
                "31",
                "--max-level",
                "3",
                "--prefix-length",
                "4",
            )
        )
    assert "requires at least 32" in capsys.readouterr().err


@pytest.mark.parametrize(
    "method",
    ("berlekamp-massey", "gf2", "dfao", "boolean-window"),
)
def test_predictor_search_methods_use_strict_holdout(
    method: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert (
        main(
            (
                "predictor-search",
                "--count",
                "24",
                "--train-length",
                "16",
                "--method",
                method,
                "--max-states",
                "1",
                "--max-models",
                "16",
                "--max-order",
                "3",
                "--max-window",
                "3",
                "--max-completions",
                "16",
                "--json",
            )
        )
        == 0
    )
    payload = _json_output(capsys)
    assert payload["result"]["train_length"] == 16
    assert payload["result"]["held_out_start"] == 16
    assert list(payload["result"]["methods"]) == [method]
    assert "lower bound" in payload["limitations"][-2]


def test_predictor_search_rejects_leakage_free_split_without_holdout(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(("predictor-search", "--count", "10", "--train-length", "10"))
    assert "held-out" in capsys.readouterr().err


def _configure_fake_experiment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    body: str,
) -> Path:
    script = tmp_path / "fake_experiment.py"
    script.write_text(body, encoding="utf-8")
    monkeypatch.setattr(cli, "REPOSITORY_ROOT", tmp_path)
    monkeypatch.setattr(cli, "EXPERIMENT_ALLOWLIST", {"fake": Path(script.name)})
    return script


def test_experiment_run_dispatches_only_allowlisted_script(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _configure_fake_experiment(
        tmp_path,
        monkeypatch,
        "import json, sys\n"
        "print(json.dumps({'argv': sys.argv[1:], "
        "'status': 'finite-exhaustive'}))\n",
    )
    assert (
        main(
            (
                "experiment",
                "run",
                "--json",
                "fake",
                "--",
                "--limit",
                "3",
            )
        )
        == 0
    )
    payload = _json_output(capsys)
    assert payload["experiment"] == "fake"
    assert payload["script_arguments"] == ["--limit", "3"]
    assert payload["parsed_output"]["argv"] == ["--limit", "3"]


def test_experiment_reproduce_compares_exact_stdout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _configure_fake_experiment(tmp_path, monkeypatch, "print('deterministic')\n")
    assert main(("experiment", "reproduce", "--json", "fake")) == 0
    payload = _json_output(capsys)
    assert payload["match"] is True
    assert payload["comparison_scope"] == "exact_stdout_bytes"
    assert payload["status"] == "finite-exhaustive"


def test_experiment_reproduce_prefers_documented_scientific_hash(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _configure_fake_experiment(
        tmp_path,
        monkeypatch,
        "import json, time\n"
        "print(json.dumps({'scientific_payload_sha256': 'a' * 64, 'runtime': time.time_ns()}))\n",
    )
    assert main(("experiment", "reproduce", "--json", "fake")) == 0
    payload = _json_output(capsys)
    assert payload["match"] is True
    assert payload["comparison_scope"] == "scientific_payload_sha256"
    assert payload["first_value"] == "a" * 64


def test_experiment_rejects_path_escaping_repository(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    repository = tmp_path / "repo"
    repository.mkdir()
    outside = tmp_path / "outside.py"
    outside.write_text("print('no')\n", encoding="utf-8")
    monkeypatch.setattr(cli, "REPOSITORY_ROOT", repository)
    monkeypatch.setattr(
        cli, "EXPERIMENT_ALLOWLIST", {"fake": Path("..") / outside.name}
    )
    with pytest.raises(SystemExit):
        main(("experiment", "run", "fake"))
    assert "outside the repository" in capsys.readouterr().err


def test_experiment_unknown_name_is_rejected_before_execution(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(("experiment", "run", "not-allowlisted"))
    assert "invalid choice" in capsys.readouterr().err


def test_python_generation_cap_is_conservative(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit):
        main(("generate", "--count", str(cli.BACKEND_COUNT_LIMITS["python"] + 1)))
    assert "conservative python limit" in capsys.readouterr().err


def test_human_analytical_output_states_finite_scope(
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(("balance", "--count", "10")) == 0
    output = capsys.readouterr().out
    assert "D=4" in output
    assert "Finite measurements" in output


@pytest.mark.parametrize(
    "arguments",
    (
        ("balance", "--count", "8", "--json"),
        ("blocks", "--count", "8", "--width", "2", "--json"),
        ("autocorrelation", "--count", "8", "--lag", "1", "--json"),
        ("linear-complexity", "--count", "8", "--json"),
        ("period-search", "--count", "8", "--max-period", "3", "--json"),
        ("sideways-reconstruct", "--horizon", "4", "--json"),
        (
            "automaticity-search",
            "--max-level",
            "1",
            "--prefix-length",
            "3",
            "--json",
        ),
        (
            "predictor-search",
            "--count",
            "12",
            "--train-length",
            "8",
            "--json",
        ),
    ),
)
def test_every_analytical_json_has_status_and_finite_limitations(
    arguments: tuple[str, ...],
    capsys: pytest.CaptureFixture[str],
) -> None:
    assert main(arguments) == 0
    payload = _json_output(capsys)
    assert payload["status"] in {"finite-exhaustive", "empirical", "inconclusive"}
    assert "finite" in " ".join(payload["limitations"]).lower()
    assert payload["proof_scope"]
