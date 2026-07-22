# Reproducible same-workload benchmark matrix

`experiments/shared/run_benchmark_matrix.py` closes the initial benchmark
coverage gap with three deliberately modest, repeated workloads:

1. generation of the same complete finite center prefix by Python coordinate,
   C++ scalar, C++ AVX2, Rust packed, and CUDA direct evolution;
2. statistics over the existing trusted 10,000-byte center prefix; and
3. an exact, explicitly bounded predictor search with a strict training and
   held-out split.

This is a performance experiment, not a complexity lower bound. It makes no
claim that one backend is universally faster, and no finite run proves an
infinite Rule 30 statement.

## Measurement contract

The generation workload is exactly `N` numeric bytes `c_0` through
`c_(N-1)` from the single-black-cell initial condition. The driver launches all
five backends once and compares every byte directly with the canonical trusted
vector before it starts any timed run. Agreement among five wrong backends is
therefore insufficient. It then validates every warm-up, measured, and RSS
profile output against those trusted bytes and requires ordinary child stderr
to remain empty.

Warm-up and measured rounds use a recorded deterministic cyclic rotation of
Python coordinate, C++ scalar, C++ AVX2, Rust packed `uint64_t`, and CUDA
direct row evolution. Advancing the starting backend reduces systematic
frequency, scheduler, cache, and thermal bias relative to one fixed order.

Each timing is subprocess end-to-end. It includes process creation, dynamic
runtime or CUDA-context initialization, computation, and writing raw stdout. It
excludes parent-side hashing and validation. This scope is intentionally not a
kernel-only or inner-loop benchmark. At the default `N=4096`, startup costs can
be material.

This matrix compares end-to-end CLI paths that produce the same required
bytes; it does not claim that every implementation performs identical
auxiliary work. CUDA kernel and transfer decomposition is recorded separately
in [`20260722_cuda_direct_evolution_n32768.json`](../results/benchmarks/20260722_cuda_direct_evolution_n32768.json).

The driver records each sample and its minimum, median, maximum, arithmetic
mean, and population standard deviation. Host peak RSS comes from one separate,
untimed GNU `time %M` profile per workload. This avoids reporting the inherited
pre-exec memory floor that a Python-forked child can carry into a direct
`wait4` measurement. The GNU-time profiles regenerate and revalidate the same
complete output, but are explicitly excluded from timing samples. RSS is host
resident memory, not GPU-memory usage.

Before and after the matrix, the driver reads:

- CPU model, AVX2 visibility, cpufreq governor/driver/frequency state when WSL
  exposes it, and `/proc/cpuinfo` frequency snapshots otherwise;
- host memory availability; and
- NVIDIA model, VRAM, driver, temperature, P-state, clocks, and power fields
  through read-only `nvidia-smi` queries.

It does not pin CPU frequency or change CPU/GPU clocks, voltage, power, fan, or
thermal controls.

## Deterministic analysis workloads

The statistics workload uses
`tests/reference_vectors/center_c00000000_c00009999.u8` and explicitly fixes
checkpoints, block widths, autocorrelation lags, linear-complexity prefixes,
approximate-entropy widths, dyadic widths, and table limits. Optional spectral
analysis is not enabled for this matrix.

The predictor workload uses the first 5,000 trusted bits, with bits
`[0,2500)` for training and `[2500,5000)` held out. It explicitly bounds the
labeled-DFAO enumeration through three states, finite 2-kernel quotient,
depth 4 finite 2-kernel quotient with 64-bit fingerprints, GF(2) recurrence
enumeration through order 12, Berlekamp–Massey candidate, and Boolean-window
recurrence checks through width 12.

Both scripts emit deterministic JSON. The matrix establishes one untimed
reference output, requires every warm-up and measured output to match it
byte-for-byte, and records the exact argv, output byte count, and SHA-256. It
also verifies required fields, question, status, input count/hash, and—in the
predictor workload—the complete pinned parameter map, exact training/held-out
split, leakage-control statement, deterministic seed, and every component
completion flag. A failed bounded search has no universal or asymptotic
interpretation.

## Conservative controls

Defaults are one warm-up and three measured repetitions, `N=4096`, a 30-second
wall limit per subprocess, a 2 MiB combined stdout/stderr cap, CUDA device 0,
256 threads, a 64 MiB GPU-memory budget, a 16 MiB CUDA output budget, and nice
level 10. Hard caps prevent more than:

- 10,000 generated bits;
- 10 warm-ups or 20 measured repetitions;
- 300 seconds per subprocess;
- 16 MiB captured output;
- 2,048 MiB requested CUDA memory; or
- 64 MiB requested CUDA output.

stdout and stderr are drained concurrently from bounded pipes. A time or output
violation kills the new process group, including surviving descendants that
inherit a pipe after the direct child exits. A 250-millisecond post-kill drain
cap prevents a detached pipe holder from blocking the orchestrator. Trusted
inputs are capped at
1 MiB, executable hashing is incremental and capped at 512 MiB, and captured
bytes never exceed the exact combined cap. Commands are argument vectors whose
executables must be absolute paths; the driver never invokes a shell.
The matrix does not impose a cgroup or aggregate-RAM limit on native children;
its deliberately small count, strict wall/output caps, and separate RSS
profiles are the safeguards for this short benchmark. Long searches belong
under the controlled experiment runner.

## Build and run

The following uses WSL-native build directories and two conservative build
jobs. Replace only the build-root path if needed; pass the resulting executable
paths explicitly to the matrix.

```bash
cmake --fresh -S . \
  -B /tmp/rule30-benchmark-matrix-build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
  -DCMAKE_CUDA_ARCHITECTURES=75 \
  -DRULE30_ENABLE_CUDA=ON
nice -n 10 cmake --build /tmp/rule30-benchmark-matrix-build --parallel 2

env \
  RUSTUP_HOME=$PWD/.toolchains/rustup \
  CARGO_HOME=$PWD/.toolchains/cargo \
  CARGO_TARGET_DIR=/tmp/rule30-benchmark-matrix-rust \
  nice -n 10 cargo build --offline --locked --release \
    -p rule30-core --bin rule30-rust
```

Run a draft matrix after those binaries pass their normal correctness gates:

```bash
nice -n 10 .venv/bin/python \
  experiments/shared/run_benchmark_matrix.py \
  --python-executable .venv/bin/python \
  --cpp-executable /tmp/rule30-benchmark-matrix-build/src/cpp/rule30_cpp \
  --rust-executable /tmp/rule30-benchmark-matrix-rust/release/rule30-rust \
  --cuda-executable /tmp/rule30-benchmark-matrix-build/src/cuda/rule30_cuda_generate \
  --nice-executable /usr/bin/nice \
  --time-executable /usr/bin/time \
  --git-executable /usr/bin/git \
  --nvidia-smi-executable /usr/lib/wsl/lib/nvidia-smi \
  --cxx-compiler /usr/bin/g++ \
  --rustc-executable /usr/bin/rustc \
  --cargo-executable /usr/bin/cargo \
  --nvcc-executable /usr/local/cuda/bin/nvcc \
  --cpp-build-directory /tmp/rule30-benchmark-matrix-build \
  --cuda-build-directory /tmp/rule30-benchmark-matrix-build \
  --rust-build-directory /tmp/rule30-benchmark-matrix-rust \
  --trusted-prefix tests/reference_vectors/center_c00000000_c00009999.u8 \
  --count 4096 --warmups 1 --repetitions 5 \
  --timeout-seconds 30 --max-capture-bytes 2097152 \
  --nice-level 10 --cuda-device 0 --cuda-threads 256 \
  --cuda-memory-budget-mib 64 --cuda-output-budget-mib 16 \
  --output results/benchmarks/20260722_same_output_matrix_n4096.json
```

The outer `nice` keeps the orchestrator polite; every measured child also has
an explicit `nice -n 10` prefix recorded in its argv.

## Persistent record provenance

Without `--output`, the script prints a draft record. Persistent output
requires the driver to match `HEAD`, every tracked and non-ignored untracked
entry visible to `git status` to be clean, and the canonical repository trusted
vector. It also
requires explicit C++, CUDA, and Rust build directories; native executables
must reside beneath those directories, and each CMake cache must name this
repository as its source. Executable size and SHA-256 are measured before and
after the matrix and must remain unchanged. Relevant Git tree IDs, exact
executable hashes, retained CMake/Ninja flags, compiler versions, and the
normalized performance environment are recorded.
Immediately before record construction, the driver repeats the HEAD,
clean-worktree, relevant-tree, benchmark-script, executable, and trusted-vector
checks; persistent output is refused if any changed.

The destination must be directly under `results/benchmarks`; an existing
record is refused unless `--overwrite` is explicit. The write uses the
repository's validated atomic experiment-record path. These checks provide
strong local provenance evidence but are not a cryptographically attested
reproducible-build proof. The resulting top-level
status is `empirical`; exact byte equality is scoped to the recorded finite
runs, and performance conclusions remain workload- and machine-specific.

## Recorded 2026-07-22 matrix

The tracked record
[`20260722_same_output_matrix_n4096.json`](../results/benchmarks/20260722_same_output_matrix_n4096.json)
was run from clean commit
`cefb2619ff7df9cb1ed0b627e9bd9cba6607b4ba` using freshly configured external
build trees. Every preflight, warm-up, measured, and RSS-profile generation
matched the trusted 4,096-byte prefix with SHA-256
`c31df0a2310247e6452237d4b780467e31b86340ce2a6dd90b679dd94c8012ff`
(2,028 ones and 2,068 zeros).

Median startup-inclusive end-to-end generation times over five rotated runs
were:

| Backend | Median seconds | Minimum | Maximum |
|---|---:|---:|---:|
| C++ AVX2 | 0.004832 | 0.004723 | 0.005250 |
| Rust packed | 0.004876 | 0.004715 | 0.004994 |
| C++ scalar | 0.005578 | 0.005236 | 0.005693 |
| CUDA direct | 0.401417 | 0.341460 | 0.438318 |
| Python coordinate | 3.195124 | 3.169592 | 3.257848 |

The deterministic statistics workload median was 1.062213 seconds and the
bounded predictor workload median was 0.531320 seconds. GPU temperature was
41 C before and after the matrix; no hardware setting was changed. At this
small sequential generation size, CUDA context and dependent-launch overhead
dominated. These measurements do not rank the implementations for different
sizes or workloads and do not imply an asymptotic complexity claim.

## Tests

The focused suite uses fake backend results and short local subprocesses. It
does not need CUDA or a GPU:

```bash
PYTHONPYCACHEPREFIX=/tmp/rule30-benchmark-pyc \
  .venv/bin/pytest -q -p no:cacheprovider \
  tests/python/test_benchmark_matrix.py
```

It checks command construction, canonical trusted-vector anchoring (including
the all-backends-wrong case), rotated order, semantic deterministic-JSON
validation, descriptive timing calculations, isolated GNU-time RSS profiles,
exact wall/output caps, a pipe-inheriting descendant, and rejection of
PATH-based executable lookup.
