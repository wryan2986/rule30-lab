# Architecture

## Trust boundary

The supplied Python file is evidence to reproduce, not an oracle. A simple
coordinate-indexed cell-array implementation and hand-derived rows establish
the first trusted layer. Shared vectors are then frozen with hashes and used by
every backend.

Trust proceeds in one direction:

1. hand-derived local-rule cases and independently indexed Python rows;
2. agreement with the immutable supplied implementation;
3. frozen complete rows, center bytes, checkpoint counts, and SHA-256 values;
4. bit-for-bit validation of every native implementation against those frozen
   artifacts; and
5. experiments and benchmarks that refuse backend disagreement.

Agreement is never decided by majority vote. A mismatch stops promotion of the
new implementation or result until the boundary convention and algorithm are
independently resolved.

## Components

- Python owns orchestration, experiment metadata, portable reference logic,
  and the `rule30` CLI.
- C++ owns packed 64-bit scalar evolution, runtime-dispatched AVX2, streaming
  output, and the baseline native benchmark.
- Rust independently implements safe packed evolution and a separately tested
  optimized path.
- CUDA owns batched independent searches and a measured single-history row
  implementation for comparison, targeting the detected `sm_75` device.
- Lean states and proves only stable local and finite reconstruction lemmas.
- `rule30lab.controlled_runner` owns the production envelope for allowlisted
  experiments: confinement, wall/address-space/output/disk limits, progress,
  checkpoints, stream hashes, and strict result publication.
- `experiments/shared/run_benchmark_matrix.py` owns the same-output performance
  comparison. It anchors outputs to a trusted vector, rotates backend order,
  captures bounded subprocess streams, and records source/build/executable
  evidence before and after timing.

The primary interchange format for a center sequence is one byte per bit for
small trusted artifacts and little-endian packed 64-bit words for large
streams. Every file records bit order, logical bit length, and SHA-256.

## CLI/backend boundary

The Python CLI invokes a common semantic operation. Native executables accept
the same explicit prefix convention and can emit JSON. Backend disagreement is
a failed verification, never resolved by majority vote.

Native generators are child processes invoked with explicit argument vectors
and `shell=False`. The CLI validates return code, exact byte count, and that
every raw byte is zero or one. Analysis commands consume the validated byte
stream and emit both human-readable and structured finite-scope output.

## Experiment and record boundary

Every tracked nontrivial result is a schema-versioned JSON document containing
the full Git commit, explicit question and hypothesis, parameters, hardware,
software, runtime, result hashes, interpretation, status, proof scope, and
limitations. Validation happens before atomic publication and again in the
repository test suite.

The controlled runner accepts only five fixed repository scripts. Read paths
must remain within the repository, child side-output paths are rejected, and
the destination remains under a non-symlink `results/runs`. Raw stdout,
stderr, and checkpoints are kept separately from the interpreted record so a
researcher can audit exact child bytes. Restart checkpoints preserve runner
capture state; the current scientific scripts restart from the beginning
rather than claiming durable mid-algorithm continuation.

Result status does not flow upward automatically. For example, a child may
exhaust a finite model box, but neither the runner nor a benchmark may relabel
that as a theorem about all traces or algorithms.

## Build and provenance boundary

CMake/Ninja builds C++20 and CUDA in external WSL-native build trees. CUDA is
compiled for architecture 75. Cargo builds Rust from the pinned lockfile and
toolchain; Lake builds the pinned Lean project. Debug C++ gates enable Address
and UndefinedBehavior Sanitizers, while release gates execute direct CUDA
contracts on the canonical GPU.

Benchmark records include Git tree IDs, compiler versions, retained CMake and
Ninja evidence, exact executable hashes, and before/after stability checks.
This is strong local provenance evidence, but it is not a cryptographically
attested reproducible-build proof that a native binary came from one commit.

## Resource boundary

The project never changes clocks, voltage, power, fans, or Windows/NVIDIA
safety controls. Interactive runs default to reduced worker counts and
conservative RAM/GPU/output budgets; idle runs remain bounded. NVIDIA queries
are read-only and device-global. Linux `RLIMIT_AS` is inherited per process,
not an aggregate cgroup limit, and the runner is not a hostile-code or network
sandbox. These limits and interruption semantics are specified in
`docs/resource_controls.md`.
