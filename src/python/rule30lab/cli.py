"""Unified, finite-scope command-line interface for Rule 30 research.

The CLI deliberately separates generation backends from Python analysis.  A
native backend is invoked as an argument vector (never through a shell), and
its one-byte-per-bit output is validated before any result is trusted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import statistics as timing_statistics
import subprocess
import sys
import time
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from . import __version__
from .automaticity import two_kernel_prefix_diagnostic
from .core import center_bits_cell_array
from .predictor_search import (
    fit_berlekamp_massey_candidate,
    search_boolean_window_recurrences,
    search_labeled_dfaos,
    search_short_gf2_recurrences,
)
from .sideways import (
    SidewaysLimits,
    eventually_periodic_trace,
    first_nonzero_left_depth,
    periodic_trace,
    reconstruct_left_initial,
)
from .statistics import (
    balance_checkpoints,
    berlekamp_massey_binary,
    block_frequencies,
    max_absolute_prefix_discrepancy,
    spin_autocorrelation,
)


BACKENDS = ("python", "cpp-scalar", "cpp-avx2", "rust", "cuda")
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]

# The coordinate-explicit Python reference is intentionally quadratic.  Large
# finite prefixes belong on a verified packed backend.
BACKEND_COUNT_LIMITS: Mapping[str, int] = {
    "python": 10_000,
    "cpp-scalar": 10_000_000,
    "cpp-avx2": 10_000_000,
    "rust": 10_000_000,
    "cuda": 100_000,
}
MAX_OUTPUT_BYTES = 16 * 1024 * 1024
MAX_ANALYSIS_BITS = 1_000_000
MAX_LINEAR_COMPLEXITY_BITS = 20_000
MAX_PERIOD_COMPARISONS = 50_000_000
MAX_BLOCK_TABLE_ENTRIES = 65_536
MAX_AUTOMATICITY_LEVEL = 13
MAX_AUTOMATICITY_PREFIX = 4_096
MAX_SIDEWAYS_HORIZON = 2_000
MAX_SUBPROCESS_TIMEOUT_SECONDS = 3_600.0
DEFAULT_SUBPROCESS_TIMEOUT_SECONDS = 120.0
MAX_EXPERIMENT_OUTPUT_BYTES = 16 * 1024 * 1024
MAX_EXPERIMENT_ARGUMENTS = 128
MAX_EXPERIMENT_ARGUMENT_BYTES = 4_096

EXECUTABLE_ENVIRONMENT = {
    "cpp": "RULE30_CPP_EXECUTABLE",
    "rust": "RULE30_RUST_EXECUTABLE",
    "cuda": "RULE30_CUDA_EXECUTABLE",
}
EXECUTABLE_DEFAULTS = {
    "cpp": "rule30_cpp",
    "rust": "rule30-rust",
    "cuda": "rule30_cuda_generate",
}

EXPERIMENT_ALLOWLIST: Mapping[str, Path] = {
    "problem1-sideways": Path(
        "experiments/problem1_nonperiodicity/run_sideways_search.py"
    ),
    "problem2-finite-prefix": Path(
        "experiments/problem2_balance/run_finite_prefix.py"
    ),
    "problem2-scaling": Path(
        "experiments/problem2_balance/run_scaling_analysis.py"
    ),
    "problem2-conservation": Path(
        "experiments/problem2_balance/search_local_conservation.py"
    ),
    "problem3-exact-searches": Path(
        "experiments/problem3_complexity/run_exact_searches.py"
    ),
}

FINITE_LIMITATIONS = [
    "the result concerns only the explicitly stated finite input or search box",
    "no finite computation proves an infinite Rule 30 statement",
]


class CliError(RuntimeError):
    """A concise, user-facing command-line failure."""


def _nonnegative_integer(text: str) -> int:
    try:
        value = int(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a nonnegative integer") from exc
    if value < 0:
        raise argparse.ArgumentTypeError("expected a nonnegative integer")
    return value


def _positive_integer(text: str) -> int:
    value = _nonnegative_integer(text)
    if value == 0:
        raise argparse.ArgumentTypeError("expected a positive integer")
    return value


def _positive_timeout(text: str) -> float:
    try:
        value = float(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected a positive timeout") from exc
    if not 0.0 < value <= MAX_SUBPROCESS_TIMEOUT_SECONDS:
        raise argparse.ArgumentTypeError(
            "timeout must be positive and at most "
            f"{MAX_SUBPROCESS_TIMEOUT_SECONDS:g} seconds"
        )
    return value


def _binary_word(text: str, *, name: str, allow_empty: bool = False) -> bytes:
    if not text and not allow_empty:
        raise CliError(f"{name} must be a nonempty binary word")
    if any(character not in "01" for character in text):
        raise CliError(f"{name} must contain only 0 and 1")
    return bytes(int(character) for character in text)


def _add_backend_options(
    parser: argparse.ArgumentParser,
    *,
    repeated: bool = False,
    required: bool = False,
) -> None:
    if repeated:
        parser.add_argument(
            "--backend",
            dest="backends",
            action="append",
            choices=BACKENDS,
            required=required,
            help="backend to compare; repeat for each backend",
        )
    else:
        parser.add_argument(
            "--backend", choices=BACKENDS, default="python", help="generation backend"
        )
    parser.add_argument(
        "--cpp-executable",
        help=f"C++ executable (or ${EXECUTABLE_ENVIRONMENT['cpp']})",
    )
    parser.add_argument(
        "--rust-executable",
        help=f"Rust executable (or ${EXECUTABLE_ENVIRONMENT['rust']})",
    )
    parser.add_argument(
        "--cuda-executable",
        help=f"CUDA executable (or ${EXECUTABLE_ENVIRONMENT['cuda']})",
    )
    parser.add_argument(
        "--timeout",
        type=_positive_timeout,
        default=DEFAULT_SUBPROCESS_TIMEOUT_SECONDS,
        metavar="SECONDS",
        help="per-native-process timeout (maximum 3600 seconds)",
    )


def _add_format_options(
    parser: argparse.ArgumentParser, *, raw: bool = False
) -> None:
    choices = ("text", "raw", "json") if raw else ("text", "json")
    parser.add_argument(
        "--format",
        choices=choices,
        help="output convention; defaults to text",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="compatibility alias for --format json",
    )


def _add_generated_prefix_options(
    parser: argparse.ArgumentParser,
    *,
    count_required: bool = True,
) -> None:
    parser.add_argument(
        "--count",
        type=_positive_integer,
        required=count_required,
        help="finite number of bits beginning at c_0",
    )
    _add_backend_options(parser)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rule30", description="Rule 30 research CLI")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subcommands = parser.add_subparsers(dest="command", required=True)

    generate = subcommands.add_parser("generate", help="generate a center-sequence prefix")
    generate.add_argument(
        "--count", type=_nonnegative_integer, required=True, help="number of bits c_0 onward"
    )
    _add_backend_options(generate)
    _add_format_options(generate, raw=True)

    verify = subcommands.add_parser(
        "verify", help="compare actual finite center bytes across backends"
    )
    verify.add_argument("--count", type=_nonnegative_integer, required=True)
    _add_backend_options(verify, repeated=True, required=True)
    _add_format_options(verify)

    benchmark = subcommands.add_parser(
        "benchmark", help="time generation of the same finite numeric-byte output"
    )
    benchmark.add_argument("--count", type=_positive_integer, required=True)
    benchmark.add_argument("--warmups", type=_nonnegative_integer, default=1)
    benchmark.add_argument("--repetitions", type=_positive_integer, default=5)
    _add_backend_options(benchmark)
    _add_format_options(benchmark)

    balance = subcommands.add_parser("balance", help="compute finite balance and discrepancy")
    _add_generated_prefix_options(balance)
    balance.add_argument(
        "--checkpoint",
        type=_nonnegative_integer,
        action="append",
        help="prefix length to report; repeat as needed (default: --count)",
    )
    _add_format_options(balance)

    blocks = subcommands.add_parser("blocks", help="measure finite block frequencies")
    _add_generated_prefix_options(blocks)
    blocks.add_argument("--width", type=_positive_integer, action="append", required=True)
    blocks.add_argument("--include-zero-counts", action="store_true")
    blocks.add_argument(
        "--max-table-entries",
        type=_positive_integer,
        default=MAX_BLOCK_TABLE_ENTRIES,
    )
    _add_format_options(blocks)

    correlation = subcommands.add_parser(
        "autocorrelation", help="measure finite uncentered spin autocorrelation"
    )
    _add_generated_prefix_options(correlation)
    correlation.add_argument("--lag", type=_nonnegative_integer, action="append", required=True)
    _add_format_options(correlation)

    linear = subcommands.add_parser(
        "linear-complexity", help="compute finite-prefix binary Berlekamp--Massey complexity"
    )
    _add_generated_prefix_options(linear)
    _add_format_options(linear)

    period = subcommands.add_parser(
        "period-search", help="rank bounded periods by final suffix agreement"
    )
    _add_generated_prefix_options(period)
    period.add_argument("--min-period", type=_positive_integer, default=1)
    period.add_argument("--max-period", type=_positive_integer, required=True)
    period.add_argument("--top", type=_positive_integer, default=10)
    _add_format_options(period)

    sideways = subcommands.add_parser(
        "sideways-reconstruct", help="reconstruct a finite initial-left prefix"
    )
    sideways.add_argument("--horizon", type=_nonnegative_integer, required=True)
    _add_backend_options(sideways)
    source = sideways.add_mutually_exclusive_group()
    source.add_argument("--trace", help="explicit c_0...c_H binary word")
    source.add_argument("--period", help="nonempty periodic boundary word")
    sideways.add_argument(
        "--preperiod",
        help="binary preperiod used with --period; the empty string is allowed",
    )
    _add_format_options(sideways)

    automaticity = subcommands.add_parser(
        "automaticity-search", help="compare bounded equal-length 2-kernel prefixes"
    )
    automaticity.add_argument(
        "--count",
        type=_positive_integer,
        help="generated bits (default: exact amount required by the largest level)",
    )
    automaticity.add_argument("--min-level", type=_nonnegative_integer, default=0)
    automaticity.add_argument("--max-level", type=_nonnegative_integer, required=True)
    automaticity.add_argument("--prefix-length", type=_positive_integer, required=True)
    automaticity.add_argument("--include-prefixes", action="store_true")
    _add_backend_options(automaticity)
    _add_format_options(automaticity)

    predictor = subcommands.add_parser(
        "predictor-search", help="run bounded exact predictor and recurrence searches"
    )
    _add_generated_prefix_options(predictor)
    predictor.add_argument("--train-length", type=_positive_integer, required=True)
    predictor.add_argument(
        "--method",
        choices=("berlekamp-massey", "gf2", "dfao", "boolean-window", "all"),
        default="berlekamp-massey",
    )
    predictor.add_argument("--max-states", type=_positive_integer, default=3)
    predictor.add_argument("--max-models", type=_positive_integer, default=100_000)
    predictor.add_argument("--max-order", type=_nonnegative_integer, default=12)
    predictor.add_argument("--max-window", type=_positive_integer, default=12)
    predictor.add_argument("--max-completions", type=_positive_integer, default=100_000)
    predictor.add_argument("--max-reported-errors", type=_nonnegative_integer, default=8)
    _add_format_options(predictor)

    experiment = subcommands.add_parser(
        "experiment", help="run only an allowlisted repository experiment"
    )
    experiment_commands = experiment.add_subparsers(
        dest="experiment_command", required=True
    )
    for command_name, help_text in (
        ("run", "run one allowlisted experiment once"),
        ("reproduce", "run one allowlisted experiment twice and compare output"),
    ):
        command = experiment_commands.add_parser(command_name, help=help_text)
        command.add_argument(
            "--timeout",
            type=_positive_timeout,
            default=DEFAULT_SUBPROCESS_TIMEOUT_SECONDS,
            metavar="SECONDS",
        )
        _add_format_options(command)
        command.add_argument("name", choices=tuple(EXPERIMENT_ALLOWLIST))
        command.add_argument(
            "script_args",
            nargs="*",
            help="arguments after -- are passed as separate argv entries",
        )
    return parser


def _selected_format(args: argparse.Namespace, *, default: str = "text") -> str:
    explicit = getattr(args, "format", None)
    compatibility_json = bool(getattr(args, "json", False))
    if compatibility_json and explicit not in (None, "json"):
        raise CliError("--json conflicts with a non-JSON --format")
    return "json" if compatibility_json else explicit or default


def _json_text(payload: Mapping[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, allow_nan=False)


def _emit(payload: Mapping[str, Any], *, output_format: str, text: str) -> None:
    if output_format == "json":
        encoded = _json_text(payload)
        if len(encoded.encode("utf-8")) > MAX_OUTPUT_BYTES:
            raise CliError(
                f"JSON output exceeds the {MAX_OUTPUT_BYTES}-byte safety cap"
            )
        print(encoded)
    else:
        if len(text.encode("utf-8")) > MAX_OUTPUT_BYTES:
            raise CliError(
                f"text output exceeds the {MAX_OUTPUT_BYTES}-byte safety cap"
            )
        print(text)


def _executable_override(args: argparse.Namespace, family: str) -> str | None:
    return getattr(args, f"{family}_executable", None)


def _resolve_executable(args: argparse.Namespace, family: str) -> str:
    override = _executable_override(args, family)
    environment_name = EXECUTABLE_ENVIRONMENT[family]
    candidate = override or os.environ.get(environment_name) or EXECUTABLE_DEFAULTS[family]
    resolved = shutil.which(candidate)
    if resolved is not None:
        return resolved

    path = Path(candidate).expanduser()
    if path.is_file() and os.access(path, os.X_OK):
        return str(path.resolve())
    source = (
        f"--{family}-executable"
        if override
        else f"${environment_name} or PATH"
    )
    raise CliError(
        f"{family.upper()} executable {candidate!r} is unavailable or not executable; "
        f"configure it with {source}"
    )


def _native_command(
    backend: str, count: int, args: argparse.Namespace
) -> list[str]:
    if backend.startswith("cpp-"):
        executable = _resolve_executable(args, "cpp")
        native_backend = "scalar" if backend == "cpp-scalar" else "avx2"
        return [
            executable,
            "generate",
            "--count",
            str(count),
            "--backend",
            native_backend,
            "--format",
            "raw",
        ]
    if backend == "rust":
        executable = _resolve_executable(args, "rust")
        return [
            executable,
            "generate",
            "--count",
            str(count),
            "--backend",
            "packed",
            "--format",
            "raw",
        ]
    if backend == "cuda":
        executable = _resolve_executable(args, "cuda")
        return [
            executable,
            "generate",
            "--count",
            str(count),
            "--format",
            "raw",
        ]
    raise CliError(f"backend {backend!r} is not a native backend")


def _run_subprocess(
    command: Sequence[str],
    *,
    timeout: float,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[bytes]:
    try:
        completed = subprocess.run(
            list(command),
            cwd=None if cwd is None else str(cwd),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
            shell=False,
        )
    except FileNotFoundError as exc:
        raise CliError(f"executable disappeared before launch: {command[0]!r}") from exc
    except PermissionError as exc:
        raise CliError(f"executable is not launchable: {command[0]!r}") from exc
    except subprocess.TimeoutExpired as exc:
        raise CliError(
            f"subprocess exceeded the {timeout:g}-second timeout: {command[0]!r}"
        ) from exc
    return completed


def _validated_native_bits(
    backend: str,
    count: int,
    completed: subprocess.CompletedProcess[bytes],
) -> bytes:
    if completed.returncode != 0:
        message = completed.stderr[:8_192].decode("utf-8", errors="replace").strip()
        suffix = f": {message}" if message else ""
        raise CliError(
            f"{backend} process exited with status {completed.returncode}{suffix}"
        )
    output = completed.stdout
    if len(output) != count:
        raise CliError(
            f"{backend} emitted {len(output)} raw bytes; expected exactly {count}"
        )
    invalid = next(
        ((index, value) for index, value in enumerate(output) if value not in (0, 1)),
        None,
    )
    if invalid is not None:
        index, value = invalid
        raise CliError(
            f"{backend} emitted non-binary raw byte {value} at index {index}"
        )
    return output


def _enforce_generation_limits(backend: str, count: int) -> None:
    if count > MAX_OUTPUT_BYTES:
        raise CliError(
            f"count {count} exceeds the {MAX_OUTPUT_BYTES}-byte output cap"
        )
    limit = BACKEND_COUNT_LIMITS[backend]
    if count > limit:
        raise CliError(
            f"count {count} exceeds the conservative {backend} limit {limit}"
        )


def _generate_bits(backend: str, count: int, args: argparse.Namespace) -> bytes:
    _enforce_generation_limits(backend, count)
    if backend == "python":
        return bytes(center_bits_cell_array(count))
    command = _native_command(backend, count, args)
    completed = _run_subprocess(command, timeout=args.timeout)
    return _validated_native_bits(backend, count, completed)


def _sample_metadata(bits: bytes, backend: str) -> dict[str, Any]:
    ones = sum(bits)
    return {
        "backend": backend,
        "bit_order": "c_0_to_c_n_minus_1",
        "count": len(bits),
        "ones": ones,
        "zeros": len(bits) - ones,
        "discrepancy": 2 * ones - len(bits),
        "sha256_u8": hashlib.sha256(bits).hexdigest(),
    }


def _finite_payload(
    *,
    command: str,
    sample: Mapping[str, Any],
    result: Any,
    status: str = "finite-exhaustive",
    interpretation: str,
    limitations: Sequence[str] = (),
) -> dict[str, Any]:
    return {
        "command": command,
        "sample": dict(sample),
        "result": result,
        "status": status,
        "proof_scope": "the explicitly parameterized finite computation only",
        "interpretation": interpretation,
        "limitations": [*FINITE_LIMITATIONS, *limitations],
    }


def _write_raw_stdout(bits: bytes) -> None:
    stream = getattr(sys.stdout, "buffer", None)
    if stream is None:
        # This fallback is primarily for embedding environments with a text-only
        # stdout replacement.  Latin-1 preserves byte values 0 and 1 exactly.
        sys.stdout.write(bits.decode("latin1"))
        sys.stdout.flush()
    else:
        stream.write(bits)
        stream.flush()


def _generate(args: argparse.Namespace) -> int:
    bits = _generate_bits(args.backend, args.count, args)
    output_format = _selected_format(args)
    if output_format == "raw":
        _write_raw_stdout(bits)
        return 0

    bit_string = "".join(str(bit) for bit in bits)
    if output_format == "json":
        payload = {
            **_sample_metadata(bits, args.backend),
            "bits": bit_string,
            "format": "json",
            "status": "finite-exhaustive",
            "interpretation": "Exact generated bytes for this finite prefix only.",
            "limitations": FINITE_LIMITATIONS,
        }
        _emit(payload, output_format="json", text="")
    else:
        # Preserve the original CLI contract: one ASCII bit string and newline.
        _emit({}, output_format="text", text=bit_string)
    return 0


def _first_mismatch(left: bytes, right: bytes) -> int | None:
    return next(
        (index for index, (a, b) in enumerate(zip(left, right, strict=True)) if a != b),
        None,
    )


def _verify(args: argparse.Namespace) -> int:
    backends = list(args.backends)
    if len(backends) < 2:
        raise CliError("verify requires at least two --backend values")
    if len(set(backends)) != len(backends):
        raise CliError("verify backends must be distinct")

    outputs = {backend: _generate_bits(backend, args.count, args) for backend in backends}
    reference_backend = backends[0]
    reference = outputs[reference_backend]
    comparisons: list[dict[str, Any]] = []
    all_equal = True
    for backend in backends[1:]:
        mismatch = _first_mismatch(reference, outputs[backend])
        equal = mismatch is None
        all_equal &= equal
        comparisons.append(
            {
                "reference_backend": reference_backend,
                "backend": backend,
                "equal_bytes": equal,
                "first_mismatch_index": mismatch,
                "reference_value": None if mismatch is None else reference[mismatch],
                "backend_value": None if mismatch is None else outputs[backend][mismatch],
            }
        )
    payload = {
        "command": "verify",
        "count": args.count,
        "bit_order": "c_0_to_c_n_minus_1",
        "backends": [_sample_metadata(outputs[name], name) for name in backends],
        "comparisons": comparisons,
        "all_equal": all_equal,
        "comparison": "full_numeric_byte_arrays_and_sha256",
        "status": "finite-exhaustive" if all_equal else "refuted",
        "proof_scope": "byte-for-byte equality for this finite prefix only",
        "interpretation": (
            "All requested implementations emitted identical finite bytes."
            if all_equal
            else "At least one requested implementation emitted a different finite byte."
        ),
        "limitations": FINITE_LIMITATIONS,
    }
    lines = [
        f"verify count={args.count} reference={reference_backend} "
        f"status={payload['status']}"
    ]
    lines.extend(
        f"{item['backend']}: equal={str(item['equal_bytes']).lower()} "
        f"sha256={hashlib.sha256(outputs[item['backend']]).hexdigest()} "
        f"first_mismatch={item['first_mismatch_index']}"
        for item in comparisons
    )
    lines.append("Finite-prefix equality is not an infinite mathematical proof.")
    _emit(payload, output_format=_selected_format(args), text="\n".join(lines))
    return 0 if all_equal else 1


def _timing_summary(samples: Sequence[float]) -> dict[str, float]:
    return {
        "minimum": min(samples),
        "median": timing_statistics.median(samples),
        "maximum": max(samples),
        "mean": timing_statistics.fmean(samples),
        "standard_deviation": timing_statistics.pstdev(samples),
    }


def _benchmark(args: argparse.Namespace) -> int:
    if args.warmups > 10:
        raise CliError("warmups is capped at 10")
    if args.repetitions > 50:
        raise CliError("repetitions is capped at 50")

    reference: bytes | None = None
    for _ in range(args.warmups):
        output = _generate_bits(args.backend, args.count, args)
        if reference is None:
            reference = output
        elif output != reference:
            raise CliError("backend output changed during benchmark warm-up")

    seconds: list[float] = []
    for _ in range(args.repetitions):
        started = time.perf_counter()
        output = _generate_bits(args.backend, args.count, args)
        seconds.append(time.perf_counter() - started)
        if reference is None:
            reference = output
        elif output != reference:
            raise CliError("backend output changed between benchmark repetitions")
    assert reference is not None

    summary = _timing_summary(seconds)
    payload = _finite_payload(
        command="benchmark",
        sample=_sample_metadata(reference, args.backend),
        result={
            "warmups": args.warmups,
            "repetitions": args.repetitions,
            "seconds": seconds,
            "summary_seconds": summary,
            "timing_scope": (
                "in-process generation and byte materialization"
                if args.backend == "python"
                else "native subprocess launch, generation, and raw-byte capture"
            ),
            "deterministic_output_across_repetitions": True,
        },
        status="empirical",
        interpretation=(
            "Wall-clock measurements for one explicitly defined finite workload; "
            "no speed claim is made for other workloads."
        ),
        limitations=("subprocess startup is included for native backends",),
    )
    text = (
        f"benchmark backend={args.backend} count={args.count} "
        f"repetitions={args.repetitions}\n"
        f"median={summary['median']:.9f}s min={summary['minimum']:.9f}s "
        f"max={summary['maximum']:.9f}s stddev={summary['standard_deviation']:.9f}s\n"
        "Timing is empirical and workload-specific."
    )
    _emit(payload, output_format=_selected_format(args), text=text)
    return 0


def _analysis_bits(args: argparse.Namespace, count: int | None = None) -> bytes:
    selected_count = args.count if count is None else count
    if selected_count > MAX_ANALYSIS_BITS:
        raise CliError(
            f"analysis count {selected_count} exceeds the {MAX_ANALYSIS_BITS}-bit cap"
        )
    return _generate_bits(args.backend, selected_count, args)


def _balance(args: argparse.Namespace) -> int:
    bits = _analysis_bits(args)
    checkpoints = args.checkpoint or [args.count]
    if max(checkpoints, default=0) > args.count:
        raise CliError("a checkpoint exceeds --count")
    records = balance_checkpoints(bits, checkpoints)
    result = {
        "checkpoints": records,
        "maximum_absolute_prefix_discrepancy": max_absolute_prefix_discrepancy(bits),
    }
    payload = _finite_payload(
        command="balance",
        sample=_sample_metadata(bits, args.backend),
        result=result,
        interpretation=(
            "Exact counts and discrepancies for the requested finite prefixes; "
            "they do not establish limiting balance."
        ),
    )
    lines = [f"balance backend={args.backend} count={args.count}"]
    lines.extend(
        f"N={record['n']} ones={record['ones']} zeros={record['zeros']} "
        f"D={record['discrepancy']}"
        for record in records
    )
    maximum = result["maximum_absolute_prefix_discrepancy"]
    lines.append(
        f"max |D|={maximum['absolute_discrepancy']} at N={maximum['n']} "
        f"(D={maximum['discrepancy']})"
    )
    lines.append("Finite measurements do not establish limiting balance.")
    _emit(payload, output_format=_selected_format(args), text="\n".join(lines))
    return 0


def _blocks(args: argparse.Namespace) -> int:
    if args.max_table_entries > MAX_BLOCK_TABLE_ENTRIES:
        raise CliError(
            f"--max-table-entries cannot exceed {MAX_BLOCK_TABLE_ENTRIES}"
        )
    widths = sorted(set(args.width))
    bits = _analysis_bits(args)
    results = [
        block_frequencies(
            bits,
            width,
            include_zero_counts=args.include_zero_counts,
            max_table_entries=args.max_table_entries,
            max_width=20,
        )
        for width in widths
    ]
    payload = _finite_payload(
        command="blocks",
        sample=_sample_metadata(bits, args.backend),
        result=results,
        interpretation=(
            "Exact overlapping block counts for the requested finite prefix; "
            "they do not establish a limiting block distribution."
        ),
    )
    lines = [f"blocks backend={args.backend} count={args.count}"]
    for result in results:
        lines.append(
            f"width={result['width']} windows={result['window_count']} "
            f"observed={result['observed_block_count']}/"
            f"{result['possible_block_count']}"
        )
        lines.extend(
            f"  {key:0{result['width']}b}: {value}"
            for key, value in result["counts"].items()
        )
    lines.append("Counts describe this finite prefix only.")
    _emit(payload, output_format=_selected_format(args), text="\n".join(lines))
    return 0


def _autocorrelation(args: argparse.Namespace) -> int:
    lags = sorted(set(args.lag))
    bits = _analysis_bits(args)
    results = [spin_autocorrelation(bits, lag) for lag in lags]
    payload = _finite_payload(
        command="autocorrelation",
        sample=_sample_metadata(bits, args.backend),
        result=results,
        interpretation=(
            "Exact uncentered spin-product means at the requested finite lags; "
            "they do not establish correlation decay or randomness."
        ),
    )
    lines = [f"autocorrelation backend={args.backend} count={args.count}"]
    lines.extend(
        f"lag={result['lag']} numerator={result['numerator']} "
        f"denominator={result['denominator']} value={result['value']:.9f}"
        for result in results
    )
    lines.append("Finite correlations do not establish randomness or mixing.")
    _emit(payload, output_format=_selected_format(args), text="\n".join(lines))
    return 0


def _linear_complexity(args: argparse.Namespace) -> int:
    if args.count > MAX_LINEAR_COMPLEXITY_BITS:
        raise CliError(
            f"linear-complexity count exceeds the {MAX_LINEAR_COMPLEXITY_BITS}-bit cap"
        )
    bits = _analysis_bits(args)
    complexity = berlekamp_massey_binary(bits)
    payload = _finite_payload(
        command="linear-complexity",
        sample=_sample_metadata(bits, args.backend),
        result={
            "field": "GF(2)",
            "linear_complexity": complexity,
            "ratio_to_count": complexity / len(bits),
        },
        interpretation=(
            "Exact Berlekamp--Massey complexity of this finite prefix only; it "
            "does not establish the absence of an infinite recurrence."
        ),
    )
    text = (
        f"linear-complexity backend={args.backend} N={len(bits)} "
        f"L={complexity} over GF(2)\n"
        "This is a finite-prefix result, not a complexity lower bound."
    )
    _emit(payload, output_format=_selected_format(args), text=text)
    return 0


def _matching_suffix_for_period(bits: bytes, period: int) -> int:
    matched_constraints = 0
    for index in range(len(bits) - 1, period - 1, -1):
        if bits[index] != bits[index - period]:
            break
        matched_constraints += 1

    # A suffix of ``period`` bits satisfies the period-p recurrence
    # vacuously.  Each additional trailing equality extends that bit suffix by
    # one.  The supplied reference program reported only the equality count;
    # this maintained interface deliberately returns the documented bit
    # length instead (see docs/reference_audit.md, finding C2).
    return period + matched_constraints


def _period_search(args: argparse.Namespace) -> int:
    if args.max_period < args.min_period:
        raise CliError("--max-period must be at least --min-period")
    if args.max_period >= args.count:
        raise CliError("--max-period must be smaller than --count")
    candidate_count = args.max_period - args.min_period + 1
    worst_case = candidate_count * (args.count - args.min_period)
    if worst_case > MAX_PERIOD_COMPARISONS:
        raise CliError(
            f"period search worst-case work {worst_case} exceeds the "
            f"{MAX_PERIOD_COMPARISONS}-comparison cap"
        )
    if args.top > 1_000:
        raise CliError("--top is capped at 1000")

    bits = _analysis_bits(args)
    ranking = sorted(
        (
            {
                "period": period,
                "matching_suffix_length": _matching_suffix_for_period(bits, period),
            }
            for period in range(args.min_period, args.max_period + 1)
        ),
        key=lambda record: (-record["matching_suffix_length"], record["period"]),
    )
    reported = ranking[: min(args.top, len(ranking))]
    payload = _finite_payload(
        command="period-search",
        sample=_sample_metadata(bits, args.backend),
        result={
            "minimum_period": args.min_period,
            "maximum_period": args.max_period,
            "candidate_count": candidate_count,
            "ranking_order": "matching_suffix_length_descending_then_period_ascending",
            "reported_top": reported,
        },
        interpretation=(
            "Every period in the stated finite range was compared against the "
            "final suffix of this prefix; agreement is not eventual periodicity."
        ),
    )
    lines = [
        f"period-search backend={args.backend} count={args.count} "
        f"periods={args.min_period}..{args.max_period}"
    ]
    lines.extend(
        f"period={record['period']} matching_suffix={record['matching_suffix_length']}"
        for record in reported
    )
    lines.append("Finite suffix agreement cannot establish eventual periodicity.")
    _emit(payload, output_format=_selected_format(args), text="\n".join(lines))
    return 0


def _sideways_reconstruct(args: argparse.Namespace) -> int:
    if args.horizon > MAX_SIDEWAYS_HORIZON:
        raise CliError(
            f"horizon exceeds the conservative {MAX_SIDEWAYS_HORIZON}-step cap"
        )
    if args.preperiod is not None and args.period is None:
        raise CliError("--preperiod requires --period")

    source: dict[str, Any]
    if args.trace is not None:
        trace = _binary_word(args.trace, name="trace")
        if len(trace) != args.horizon + 1:
            raise CliError(
                f"--trace has {len(trace)} bits; horizon {args.horizon} requires "
                f"exactly {args.horizon + 1}"
            )
        source = {"kind": "explicit-trace", "trace": args.trace}
    elif args.period is not None:
        period = _binary_word(args.period, name="period")
        if args.preperiod is None:
            trace = bytes(periodic_trace(period, args.horizon))
            source = {"kind": "pure-period", "period": args.period}
        else:
            preperiod = _binary_word(
                args.preperiod, name="preperiod", allow_empty=True
            )
            trace = bytes(eventually_periodic_trace(preperiod, period, args.horizon))
            source = {
                "kind": "preperiod-plus-period",
                "preperiod": args.preperiod,
                "period": args.period,
            }
    else:
        trace = _generate_bits(args.backend, args.horizon + 1, args)
        source = {"kind": "generated-single-cell-center", "backend": args.backend}

    limits = SidewaysLimits(
        max_horizon=MAX_SIDEWAYS_HORIZON,
        max_candidates=1,
        max_logical_cell_updates=10_000_000,
        max_certificate_bytes=MAX_OUTPUT_BYTES,
        max_graph_states=1,
        max_reported_survivors=1,
    )
    reconstructed = bytes(reconstruct_left_initial(trace, limits=limits))
    first_nonzero = first_nonzero_left_depth(trace, limits=limits)
    result = {
        "horizon": args.horizon,
        "trace_sha256_u8": hashlib.sha256(trace).hexdigest(),
        "source": source,
        "initial_left_bit_order": "x_-1_0_to_x_-H_0",
        "initial_left_bits": "".join(str(bit) for bit in reconstructed),
        "initial_left_sha256_u8": hashlib.sha256(reconstructed).hexdigest(),
        "nonzero_count": sum(reconstructed),
        "first_nonzero_left_depth": first_nonzero,
    }
    payload = _finite_payload(
        command="sideways-reconstruct",
        sample=_sample_metadata(trace, source.get("backend", "explicit-trace")),
        result=result,
        interpretation=(
            "The left initial cells are reconstructed exactly through this finite "
            "horizon under the fixed zero right-half initial condition."
        ),
        limitations=(
            "an all-zero reconstructed finite prefix does not imply an all-zero infinite tail",
        ),
    )
    text = (
        f"sideways-reconstruct horizon={args.horizon} source={source['kind']}\n"
        f"initial-left={result['initial_left_bits']}\n"
        f"nonzero_count={result['nonzero_count']} "
        f"first_nonzero_depth={first_nonzero}\n"
        "The reconstruction claim stops at the stated finite horizon."
    )
    _emit(payload, output_format=_selected_format(args), text=text)
    return 0


def _automaticity_search(args: argparse.Namespace) -> int:
    if args.max_level < args.min_level:
        raise CliError("--max-level must be at least --min-level")
    if args.max_level > MAX_AUTOMATICITY_LEVEL:
        raise CliError(
            f"--max-level exceeds the conservative cap {MAX_AUTOMATICITY_LEVEL}"
        )
    if args.prefix_length > MAX_AUTOMATICITY_PREFIX:
        raise CliError(
            f"--prefix-length exceeds the cap {MAX_AUTOMATICITY_PREFIX}"
        )
    required = args.prefix_length * (1 << args.max_level)
    count = required if args.count is None else args.count
    if count < required:
        raise CliError(
            f"count {count} is insufficient; level {args.max_level} with prefix "
            f"length {args.prefix_length} requires at least {required} bits"
        )
    bits = _analysis_bits(args, count)
    results = [
        two_kernel_prefix_diagnostic(
            bits,
            level,
            args.prefix_length,
            include_prefixes=args.include_prefixes,
        )
        for level in range(args.min_level, args.max_level + 1)
    ]
    payload = _finite_payload(
        command="automaticity-search",
        sample=_sample_metadata(bits, args.backend),
        result={
            "minimum_level": args.min_level,
            "maximum_level": args.max_level,
            "prefix_length": args.prefix_length,
            "levels": results,
        },
        status="empirical",
        interpretation=(
            "Exact equality classes of equally long finite 2-kernel prefixes; "
            "distinctness does not establish nonautomaticity."
        ),
        limitations=(
            "a finite 2-kernel diagnostic cannot prove or refute automaticity",
        ),
    )
    lines = [
        f"automaticity-search backend={args.backend} count={count} "
        f"prefix_length={args.prefix_length}"
    ]
    lines.extend(
        f"level={result['level']} distinct={result['distinct_prefix_count']}/"
        f"{result['modulus']}"
        for result in results
    )
    lines.append("Finite 2-kernel distinctness does not prove nonautomaticity.")
    _emit(payload, output_format=_selected_format(args), text="\n".join(lines))
    return 0


def _predictor_search(args: argparse.Namespace) -> int:
    if args.count > MAX_LINEAR_COMPLEXITY_BITS:
        raise CliError(
            f"predictor-search count exceeds the {MAX_LINEAR_COMPLEXITY_BITS}-bit cap"
        )
    if args.train_length >= args.count:
        raise CliError("--train-length must leave at least one held-out bit")
    if args.max_states > 4:
        raise CliError("--max-states is capped at 4")
    if args.max_models > 1_000_000:
        raise CliError("--max-models is capped at 1000000")
    if args.max_order > 20:
        raise CliError("--max-order is capped at 20")
    if args.max_window > 16:
        raise CliError("--max-window is capped at 16")
    if args.max_completions > 1_000_000:
        raise CliError("--max-completions is capped at 1000000")

    bits = _analysis_bits(args)
    methods = (
        ("dfao", "gf2", "berlekamp-massey", "boolean-window")
        if args.method == "all"
        else (args.method,)
    )
    results: dict[str, Any] = {}
    for method in methods:
        if method == "dfao":
            results[method] = search_labeled_dfaos(
                bits,
                train_length=args.train_length,
                min_states=1,
                max_states=args.max_states,
                max_models=args.max_models,
                stop_after_fits=1,
                max_reported_fits=1,
                max_reported_errors=args.max_reported_errors,
                max_state_count_cap=4,
            )
        elif method == "gf2":
            results[method] = search_short_gf2_recurrences(
                bits,
                train_length=args.train_length,
                max_order=args.max_order,
                max_candidates=args.max_completions,
                stop_after_fits=1,
                max_reported_fits=1,
                max_reported_errors=args.max_reported_errors,
                max_order_cap=20,
            )
        elif method == "berlekamp-massey":
            results[method] = fit_berlekamp_massey_candidate(
                bits,
                train_length=args.train_length,
                max_reported_errors=args.max_reported_errors,
            )
        elif method == "boolean-window":
            results[method] = search_boolean_window_recurrences(
                bits,
                train_length=args.train_length,
                min_window=1,
                max_window=args.max_window,
                max_completions=args.max_completions,
                max_unseen_contexts=16,
                max_table_entries=1 << 16,
                max_reported_candidates=4,
                max_reported_table_entries=256,
                max_reported_errors=args.max_reported_errors,
            )
        else:  # pragma: no cover - argparse enforces the choices
            raise AssertionError(f"unhandled predictor method {method}")

    statuses = {result.get("status", "empirical") for result in results.values()}
    status = "inconclusive" if "inconclusive" in statuses else "empirical"
    payload = _finite_payload(
        command="predictor-search",
        sample=_sample_metadata(bits, args.backend),
        result={
            "train_length": args.train_length,
            "held_out_start": args.train_length,
            "held_out_stop": args.count,
            "methods": results,
        },
        status=status,
        interpretation=(
            "Models are fit only on the stated training prefix and checked on a "
            "disjoint held-out prefix; failures imply no universal lower bound."
        ),
        limitations=(
            "a failed bounded search proves neither nonexistence of another "
            "exact algorithm nor any lower bound",
            "a finite held-out fit does not establish an infinite identity",
        ),
    )
    lines = [
        f"predictor-search backend={args.backend} count={args.count} "
        f"train={args.train_length} status={status}"
    ]
    lines.extend(
        f"{method}: status={result.get('status', 'empirical')} "
        f"search={result.get('search_name', method)}"
        for method, result in results.items()
    )
    lines.append("Bounded search failure is not a computational lower bound.")
    _emit(payload, output_format=_selected_format(args), text="\n".join(lines))
    return 0


def _normalized_experiment_arguments(arguments: Sequence[str]) -> list[str]:
    values = list(arguments)
    if values and values[0] == "--":
        values.pop(0)
    if len(values) > MAX_EXPERIMENT_ARGUMENTS:
        raise CliError(
            f"experiment argument count exceeds the cap {MAX_EXPERIMENT_ARGUMENTS}"
        )
    for value in values:
        if "\x00" in value:
            raise CliError("experiment arguments may not contain NUL bytes")
        if len(value.encode("utf-8")) > MAX_EXPERIMENT_ARGUMENT_BYTES:
            raise CliError(
                "an experiment argument exceeds the per-argument byte cap "
                f"{MAX_EXPERIMENT_ARGUMENT_BYTES}"
            )
    return values


def _experiment_once(args: argparse.Namespace) -> tuple[bytes, bytes]:
    relative_script = EXPERIMENT_ALLOWLIST[args.name]
    script = (REPOSITORY_ROOT / relative_script).resolve()
    try:
        script.relative_to(REPOSITORY_ROOT.resolve())
    except ValueError as exc:  # protects monkeypatched/configured allowlists too
        raise CliError("allowlisted experiment resolves outside the repository") from exc
    if not script.is_file():
        raise CliError(f"allowlisted experiment script is missing: {relative_script}")
    script_arguments = _normalized_experiment_arguments(args.script_args)
    command = [sys.executable, str(script), *script_arguments]
    completed = _run_subprocess(command, timeout=args.timeout, cwd=REPOSITORY_ROOT)
    if len(completed.stdout) > MAX_EXPERIMENT_OUTPUT_BYTES:
        raise CliError(
            f"experiment stdout exceeds the {MAX_EXPERIMENT_OUTPUT_BYTES}-byte cap"
        )
    if len(completed.stderr) > MAX_EXPERIMENT_OUTPUT_BYTES:
        raise CliError(
            f"experiment stderr exceeds the {MAX_EXPERIMENT_OUTPUT_BYTES}-byte cap"
        )
    if completed.returncode != 0:
        message = completed.stderr[:8_192].decode("utf-8", errors="replace").strip()
        suffix = f": {message}" if message else ""
        raise CliError(
            f"allowlisted experiment {args.name!r} exited with status "
            f"{completed.returncode}{suffix}"
        )
    return completed.stdout, completed.stderr


def _parse_json_output(output: bytes) -> Any | None:
    try:
        return json.loads(output)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def _experiment_run(args: argparse.Namespace) -> int:
    stdout, stderr = _experiment_once(args)
    parsed = _parse_json_output(stdout)
    payload = {
        "command": "experiment run",
        "experiment": args.name,
        "script": str(EXPERIMENT_ALLOWLIST[args.name]),
        "script_arguments": _normalized_experiment_arguments(args.script_args),
        "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
        "stdout_bytes": len(stdout),
        "stderr": stderr.decode("utf-8", errors="replace"),
        "parsed_output": parsed,
        "status": "empirical",
        "proof_scope": "one local execution of one allowlisted finite experiment",
        "interpretation": "The allowlisted repository script completed locally.",
        "limitations": FINITE_LIMITATIONS,
    }
    text = (
        f"experiment={args.name} stdout_bytes={len(stdout)} "
        f"sha256={payload['stdout_sha256']}\n"
        + stdout.decode("utf-8", errors="replace").rstrip("\n")
    )
    _emit(payload, output_format=_selected_format(args), text=text)
    return 0


def _scientific_hash(parsed: Any | None) -> str | None:
    if not isinstance(parsed, dict):
        return None
    value = parsed.get("scientific_payload_sha256")
    return value if isinstance(value, str) and len(value) == 64 else None


def _experiment_reproduce(args: argparse.Namespace) -> int:
    first_stdout, first_stderr = _experiment_once(args)
    second_stdout, second_stderr = _experiment_once(args)
    first_parsed = _parse_json_output(first_stdout)
    second_parsed = _parse_json_output(second_stdout)
    first_scientific = _scientific_hash(first_parsed)
    second_scientific = _scientific_hash(second_parsed)
    if first_scientific is not None and second_scientific is not None:
        scope = "scientific_payload_sha256"
        first_value = first_scientific
        second_value = second_scientific
        match = first_value == second_value
    else:
        scope = "exact_stdout_bytes"
        first_value = hashlib.sha256(first_stdout).hexdigest()
        second_value = hashlib.sha256(second_stdout).hexdigest()
        match = first_stdout == second_stdout

    payload = {
        "command": "experiment reproduce",
        "experiment": args.name,
        "script": str(EXPERIMENT_ALLOWLIST[args.name]),
        "script_arguments": _normalized_experiment_arguments(args.script_args),
        "comparison_scope": scope,
        "first_value": first_value,
        "second_value": second_value,
        "match": match,
        "first_stdout_sha256": hashlib.sha256(first_stdout).hexdigest(),
        "second_stdout_sha256": hashlib.sha256(second_stdout).hexdigest(),
        "first_stderr": first_stderr.decode("utf-8", errors="replace"),
        "second_stderr": second_stderr.decode("utf-8", errors="replace"),
        "first_parsed_output": first_parsed,
        "status": "finite-exhaustive" if match else "inconclusive",
        "proof_scope": "two local executions with identical argv",
        "interpretation": (
            "The selected deterministic comparison value matched across two runs."
            if match
            else "The selected deterministic comparison value differed across two runs."
        ),
        "limitations": [
            *FINITE_LIMITATIONS,
            "two matching executions do not establish reproducibility on other systems",
        ],
    }
    text = (
        f"experiment={args.name} reproduce match={str(match).lower()} "
        f"scope={scope}\nfirst={first_value}\nsecond={second_value}\n"
        "This comparison concerns two local executions only."
    )
    _emit(payload, output_format=_selected_format(args), text=text)
    return 0 if match else 1


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    handlers = {
        "generate": _generate,
        "verify": _verify,
        "benchmark": _benchmark,
        "balance": _balance,
        "blocks": _blocks,
        "autocorrelation": _autocorrelation,
        "linear-complexity": _linear_complexity,
        "period-search": _period_search,
        "sideways-reconstruct": _sideways_reconstruct,
        "automaticity-search": _automaticity_search,
        "predictor-search": _predictor_search,
    }
    try:
        if args.command == "experiment":
            if args.experiment_command == "run":
                return _experiment_run(args)
            return _experiment_reproduce(args)
        return handlers[args.command](args)
    except (CliError, MemoryError, OSError, ValueError) as exc:
        parser.error(str(exc))
    return 2  # pragma: no cover - argparse.error raises SystemExit


if __name__ == "__main__":
    sys.exit(main())
