# Rule 30 CUDA components

These components target the local RTX 2060 SUPER with native `sm_75` SASS.
They perform exact finite computations; none of their outputs proves an
infinite Rule 30 statement.

## Components

- `evaluate_period_candidates` preserves the original chunked batch-period
  equality search.
- `evolve_single_history` directly evolves one single-cell Rule 30 history.
  It returns exactly `N` numeric center bytes and the final packed row. One
  dependent kernel launch computes each row after the seed.
- `reconstruct_left_initial_batch` reconstructs the finite initial-left tail
  for many independent center traces using Rule 30 left-permutivity. One CUDA
  thread handles each trace, candidates are chunked, and the default horizon is
  bounded at 512.

Direct evolution maps final-row bit `i` to coordinate
`i - (N - 1)`. Unused bits in the final partial `uint64_t` are zero. Sideways
input and output are flat candidate-major numeric-byte arrays.

All APIs preserve 64 MiB of currently free GPU memory in addition to honoring
their configured hard budgets. Direct evolution defaults to a 256 MiB device
budget and 64 MiB host-output limit. Sideways reconstruction uses exactly three
`horizon + 2` byte work buffers per candidate and has the same default limits.

## Build and test

```bash
cmake -S src/cuda -B /tmp/rule30-cuda-build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
  -DBUILD_TESTING=ON
nice -n 10 cmake --build /tmp/rule30-cuda-build --parallel 2
nice -n 10 ctest --test-dir /tmp/rule30-cuda-build --output-on-failure
```

The generated compile rules must contain:

```text
--generate-code=arch=compute_75,code=[sm_75]
```

The CUDA tests cover:

- preserved batch-period behavior;
- direct counts 0 and 1;
- center-byte and packed-word transitions;
- final partial-word masking;
- partial grids;
- exact complete-row equality with an independent cell-array implementation;
- exact equality with the frozen 10,000-bit shared center vector;
- batched sideways equality with an independent CPU reconstruction;
- 1,003 sideways candidates forced through six chunks of 197 with 96-thread
  blocks;
- deterministic repeated output and resource-limit failures.

Release, warning-as-error Debug, and root-integrated tests passed on the RTX
2060 SUPER on 2026-07-21.

## Controlled benchmarks

Direct single-history evolution:

```bash
nice -n 10 /tmp/rule30-cuda-build/rule30_cuda_evolution_benchmark \
  --center-bits 32768 --repetitions 5 --threads 256 \
  --memory-budget-mib 64
```

For this exact workload, the independent packed CPU median was 36.820499 ms
and CUDA end-to-end median was 280.757527 ms. CUDA kernel-sequence median was
279.080902 ms and median total transfer time was 0.374398 ms. Outputs matched
exactly, with center hash `c5aa1c722b35125e` and final-row hash
`fab45601a97245ea`. Direct CUDA evolution was therefore slower for this input;
the sequential row dependency and 32,767 launches dominate.

Bounded batched sideways reconstruction:

```bash
nice -n 10 /tmp/rule30-cuda-build/rule30_cuda_sideways_benchmark \
  --candidates 4099 --horizon 63 --repetitions 5 --threads 128 \
  --memory-budget-mib 64
```

For this exact workload, the independent CPU median was 4.131626 ms, CUDA
end-to-end median was 3.946667 ms, kernel median was 2.592960 ms, and transfer
median was 0.219519 ms. All 258,237 output bytes matched, with hash
`9116225379191e6f`. This small end-to-end advantage is workload-specific.

Forcing 1,003 candidates into six chunks of 197 produced exact hash
`2dca0352d9c6c668`, but CUDA end-to-end median rose to 9.676108 ms versus a
0.996188 ms CPU median. Chunk and launch overhead therefore matters and a CUDA
version must not be called faster without workload-specific measurements.

The GPU was 39 C before and immediately after the benchmark runs; the final
snapshot after all validation was 40 C at 0% utilization. No clock, voltage,
fan, power, or thermal control was changed.

## Limitations

- Direct evolution performs sequential time steps and approximately quadratic
  packed-word work as `N` grows. It is a correctness and comparison backend,
  not an asymptotic shortcut for the center bit.
- Sideways reconstruction performs quadratic work in each finite horizon. The
  explicit `max_horizon` and memory/output budgets prevent accidental unbounded
  requests; increasing those controls is an intentional caller decision.
- Device buffers are chunked for sideways candidates, but a direct history's
  two rows and center output must fit the configured device budget.
- NVIDIA Compute Sanitizer 2026.2.1 could not instrument either new test binary
  in this WSL/WDDM environment. It returned exit code 99 with:
  `Failed to initialize WDDM debugger interface` and `Device not supported`,
  while the test binaries themselves still passed. Enabling the Windows WDDM
  debugger interface requires an administrator-level host change and was not
  attempted. This is a tooling limitation, not a successful memcheck result.
