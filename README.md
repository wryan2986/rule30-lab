# Rule 30 Lab

Rule 30 Lab is a local, reproducible computational-mathematics environment for
investigating Stephen Wolfram's three Rule 30 prize problems. It provides an
immutable copy of the supplied Python research harness, independently checked
Python/C++20/Rust/CUDA implementations, trusted vectors, bounded searches,
statistical diagnostics, resource-controlled experiment execution, and a small
Lean 4 development.

> **Open-problem warning:** this repository does not solve any of the three
> prize problems. Finite agreement, exhaustive search over a finite box, and
> random-looking statistics are not proofs of an infinite statement. Only the
> explicitly scoped all-one-tail exclusion is currently classified as a
> `partial-proof`.

All compute is local and there is no cloud, remote, distributed, or paid
compute dependency. The CPU-compatible code can be run on any machine with
Python 3.11+; C++20, Rust, and CUDA components are optional accelerators.

## Current status

The initial reproducible research environment is implemented. Python, C++
scalar/AVX2, Rust packed, and CUDA paths match shared vectors; bounded Problem
1--3 experiments and structured records are present; and the supplied
million-bit observations have been independently reproduced. The exact claim
ledger is in [research status](docs/research_status.md), while detected machine
facts are in [the environment report](results/environment/environment_report.md).

The most important current lead is sideways reconstruction: an eventually
periodic proposed center trace drives an exactly invertible reconstruction to
the left. Small finite search boxes strongly constrain such traces, but no
depth-independent state bound or invariant has yet been proved.

## Setup and GPU verification

Run commands inside the repository directory:

```bash
cd rule30-lab
python3 -m venv .venv
.venv/bin/python -m pip install -e . --no-deps
.venv/bin/python -m pip install -r requirements-dev.lock
source .venv/bin/activate
```

The pinned Rust and Lean setup, approved system packages, and official-source
links are recorded in [WSL/CUDA setup](docs/setup_wsl_cuda.md) and
[system changes](docs/system_changes.md). Verify the Windows-provided WSL GPU
interface without changing hardware state:

```bash
/usr/lib/wsl/lib/nvidia-smi
/usr/local/cuda/bin/nvcc --version
```

Do not install a Linux NVIDIA display driver in this WSL distribution. The
Windows driver supplies `libcuda`; only Linux-side CUDA development components
are needed.

## Build and test

Build release C++ and CUDA binaries for the detected compute capability 7.5:

```bash
cmake --fresh -S . -B /tmp/rule30-lab-release -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
  -DCMAKE_CUDA_ARCHITECTURES=75 \
  -DRULE30_ENABLE_CUDA=ON
nice -n 10 cmake --build /tmp/rule30-lab-release --parallel 2
ctest --test-dir /tmp/rule30-lab-release --output-on-failure
cuda_build=/tmp/rule30-lab-release/src/cuda
nice -n 10 "$cuda_build/rule30_cuda_probe"
nice -n 10 "$cuda_build/tests/rule30_cuda_tests"
nice -n 10 "$cuda_build/tests/rule30_cuda_evolution_tests"
nice -n 10 "$cuda_build/tests/rule30_cuda_sideways_tests"
nice -n 10 "$cuda_build/tests/rule30_cuda_generate_contract_tests" \
  gpu "$cuda_build/rule30_cuda_generate" \
  "$PWD/tests/reference_vectors/center_c00000000_c00009999.u8"
```

Build and test Rust with the project-local toolchain:

```bash
env RUSTUP_HOME="$PWD/.toolchains/rustup" \
  CARGO_HOME="$PWD/.toolchains/cargo" \
  CARGO_TARGET_DIR=/tmp/rule30-lab-rust \
  cargo test --offline --locked --release --workspace
```

Run every required gate, including Python, release C++/CUDA, direct GPU
contracts, sanitizer-enabled C++, Rust formatting/clippy/tests, record
validation, and Lean:

```bash
RULE30_BUILD_ROOT=/tmp/rule30-lab-quality-gates \
  nice -n 10 scripts/run_quality_gates.sh
```

CTest uses return code 77 to skip CUDA cases when a device is inaccessible, so
CTest success alone is not the canonical GPU gate. The direct commands above
and `scripts/run_quality_gates.sh` make device unavailability a failure. NVIDIA
Compute Sanitizer is not included in the success claim because its WDDM
debugger initialization fails in this WSL configuration.

## Unified CLI

The primary entry point is `.venv/bin/rule30`; all bit ranges use
`c_0, ..., c_(N-1)` and JSON output states finite scope and limitations.

```bash
rule30 generate --count 80
rule30 verify --count 10000 \
  --backend python --backend cpp-scalar --backend cpp-avx2 --backend rust \
  --cpp-executable /tmp/rule30-lab-release/src/cpp/rule30_cpp \
  --rust-executable /tmp/rule30-lab-rust/release/rule30-rust --json
rule30 balance --count 1000000 --backend cpp-avx2 \
  --cpp-executable /tmp/rule30-lab-release/src/cpp/rule30_cpp \
  --checkpoint 100 --checkpoint 1000 --checkpoint 10000 \
  --checkpoint 100000 --checkpoint 1000000 --json
rule30 linear-complexity --count 5000 --json
rule30 sideways-reconstruct --horizon 500 --json
rule30 automaticity-search --min-level 1 --max-level 9 \
  --prefix-length 64 --json
rule30 predictor-search --count 10000 --train-length 5000 \
  --method all --max-states 3 --max-order 12 --max-window 12 --json
```

See [CLI semantics](docs/cli.md) for every command, backend adapter, cap, output
encoding, and exit convention.

## Reproduce the main finite results

Reproduce the immutable supplied-Python million-bit hash and counts:

```bash
nice -n 10 .venv/bin/python scripts/reproduce_reported_results.py \
  python-million
```

Reproduce the independently compiled million-bit balance result:

```bash
nice -n 10 .venv/bin/rule30 balance --count 1000000 \
  --backend cpp-avx2 \
  --cpp-executable /tmp/rule30-lab-release/src/cpp/rule30_cpp \
  --checkpoint 100 --checkpoint 1000 --checkpoint 10000 \
  --checkpoint 100000 --checkpoint 1000000 --json
```

Reproduce the finite sideways, balance/statistics, and exact predictor drivers:

```bash
.venv/bin/python experiments/problem1_nonperiodicity/run_sideways_search.py \
  --horizon 500 --max-period 10 --max-preperiod 3 \
  --eventual-max-period 5 \
  --true-prefix-lengths 1,2,4,8,16,32,64,128,256
.venv/bin/python experiments/problem2_balance/run_finite_prefix.py \
  --input tests/reference_vectors/center_c00000000_c00009999.u8
.venv/bin/python experiments/problem3_complexity/run_exact_searches.py \
  --input tests/reference_vectors/center_c00000000_c00009999.u8 \
  --limit-bits 5000 --train-length 2500
```

Exact record-specific argv and input/output hashes are retained in each JSON
under `results/`.

## Benchmarks

The comparable five-backend matrix verifies every generated byte against the
trusted 10,000-bit vector before timing. Its command, build evidence, rotated
orders, all samples, RSS profiles, and thermal snapshots are documented in
[benchmark protocol](docs/benchmark_matrix.md) and recorded in
[the 4,096-bit matrix](results/benchmarks/20260722_same_output_matrix_n4096.json).

```bash
# First build the explicit release trees above, then run the complete command
# from docs/benchmark_matrix.md with --repetitions 5 and --output PATH.
```

The matrix is startup-inclusive and workload-specific. Separate CUDA records
report kernel, transfer, and end-to-end timings for batch-period, sideways, and
direct evolution workloads. No benchmark is a complexity lower bound.

## Controlled experiments

Nontrivial runs should use the allowlisted controlled route:

```bash
rule30 experiment controlled -- \
  --profile interactive \
  --experiment-id p2-conservation-widths-1-5 \
  problem2-conservation -- \
  --minimum-width 1 --maximum-width 5
```

It provides conservative interactive/idle profiles, wall and per-process
address-space limits, exact streamed-output caps, disk reserve checks, atomic
artifacts, progress/checkpoint records, graceful interruption, and optional
read-only GPU telemetry. It is an audited local execution envelope, not a
hostile-code, network, cgroup, or aggregate-memory sandbox. See
[resource controls](docs/resource_controls.md).

## Repository and result map

- `src/python/`: immutable supplied source and maintained orchestration/CLI.
- `src/cpp/`: packed scalar and runtime-dispatched AVX2 C++20 engines.
- `src/rust/`: independent safe coordinate and packed Rust engines.
- `src/cuda/`: direct evolution plus batched period and sideways workloads.
- `tests/reference_vectors/`: complete rows through step 255 and 10,000 trusted
  center bytes with hashes/checkpoints.
- `experiments/`: deterministic Problem 1, 2, 3, and shared drivers.
- `results/environment/`: detected WSL, CPU, RAM, GPU, driver, and tools.
- `results/benchmarks/`: structured timing and correctness records.
- `results/problem1/`, `problem2/`, `problem3/`: claim-scoped records.
- `docs/public_provenance/`: path-neutral certificate manifests for controlled
  runs whose machine-local operational records under `results/runs/` remain
  intentionally ignored.
- `proofs/informal/` and `proofs/lean/`: synchronized informal and formal work.
- `docs/research_log.md` and `docs/adversarial_review.md`: dated history and an
  internal automated challenge review performed in a separate agent context.

## Result language and limitations

Allowed statuses are `empirical`, `finite-exhaustive`, `heuristic`,
`partial-proof`, `rigorous-proof`, `refuted`, and `inconclusive`; their meanings
are fixed by [the experiment protocol](docs/experiment_protocol.md). Important
remaining limitations include:

- no proof of center nonperiodicity, limiting balance, or a universal
  computational lower bound;
- bounded searches exclude only their exact finite model classes;
- the external width-two theorem used by the all-one-tail argument is reviewed
  informally but is not formalized in Lean here;
- benchmark binaries have strong local hash/build-tree evidence, not a
  cryptographically attested reproducible-build certificate;
- CPU frequency is observed rather than pinned, and direct CUDA row evolution
  is launch-dominated at the measured small/sequential workloads;
- the controlled runner's RAM limit is per process, not aggregate cgroup RSS;
  and
- Compute Sanitizer could not initialize under the current WSL/WDDM stack.

A source archive produced with `git archive` omits `.git`. It can reproduce
source-level algorithms and certificate hashes, but a full Git clone is required
to validate commit existence, clean-tree state, and history-bound provenance.

The repository uses the MIT license. See [LICENSE](LICENSE).
