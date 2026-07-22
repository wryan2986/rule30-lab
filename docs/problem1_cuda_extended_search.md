# Bounded CUDA preperiod/period search

`rule30_cuda_extended_period_search` exhaustively enumerates a configured,
finite box of eventually periodic center-trace descriptions and tests their
finite sideways reconstructions. It is a Problem 1 counterexample/exclusion
tool. It does not prove that the true center sequence is nonperiodic.

## Description convention

A description is `(q, p, code)`, where `q` is the preperiod, `p >= 1` is the
period, and `code` contains `q+p` bits. Bit index zero is the least-significant
bit. The generated finite trace is

```text
c[t] = code[t]                         for t < q
c[t] = code[q + ((t-q) mod p)]         for t >= q.
```

The search requires `horizon >= max_preperiod + max_period`, so every encoded
bit occurs in the tested trace. It first counts all `2^(q+p)` descriptions,
then rejects exactly those with `c[0] = 0`; the single-cell seed requires
`c[0] = 1`.

Different descriptions can denote the same finite trace. For example, pure
period `1` with word `1` and pure period `2` with word `11` both denote the
all-one trace. The implementation sorts packed traces, records exact
multiplicity, and evaluates each distinct finite trace once. Reports retain
both description-level and distinct-trace-level coverage, including
`duplicate_descriptions`.

## Exact finite test

For each distinct trace `c[0..H]`, the tool assumes the known all-zero initial
half-line to the right and reconstructs

```text
x[-1,0], x[-2,0], ..., x[-H,0]
```

using Rule 30 left-permutivity. The first reconstructed `1`, if any, is an
exact finite incompatibility witness. A zero reconstructed prefix is only
finite compatibility through depth `H`; it is not evidence of compatibility
at every depth.

The compact output contains a complete histogram by first-nonzero depth and,
subject to `--maximum-witnesses`, one deterministic canonical description for
each represented depth. It does not emit every rejected trace.

## CPU and CUDA paths

The CPU path independently generates, period-checks, and reconstructs each
trace with linear workspace:

```bash
/tmp/rule30-extended-search-build/src/cuda/rule30_cuda_extended_period_search \
  --backend cpu \
  --min-preperiod 0 --max-preperiod 2 \
  --min-period 1 --max-period 4 \
  --horizon 24 --evaluation-chunk 7 \
  --host-memory-budget-bytes 8388608 \
  --device-memory-budget-bytes 8388608 \
  --output-budget-bytes 65536 --maximum-witnesses 16
```

The CUDA path uses two existing, independently tested APIs for every outer
chunk:

1. `evaluate_period_candidates` verifies the declared eventual-period
   relation over the complete finite trace.
2. `reconstruct_left_initial_batch` performs the sideways reconstruction.

```bash
/tmp/rule30-extended-search-build/src/cuda/rule30_cuda_extended_period_search \
  --backend cuda \
  --min-preperiod 0 --max-preperiod 4 \
  --min-period 1 --max-period 8 \
  --horizon 64 --evaluation-chunk 256 \
  --threads 128 --device 0 \
  --host-memory-budget-bytes 268435456 \
  --device-memory-budget-bytes 134217728 \
  --output-budget-bytes 4194304 --maximum-witnesses 32
```

The JSON report separates periodicity-kernel time, sideways-kernel time, each
API's end-to-end time, and total search time. CPU reports kernel times as zero.

## Resource controls

- The description width is capped at 63 bits and the reconstruction horizon
  at 512, matching the bounded sideways API.
- `--host-memory-budget-bytes` preflights packed records, report workspace,
  CPU scratch space when applicable, and the largest evaluation chunk.
- `--device-memory-budget-bytes` is passed as a hard allocation budget to both
  CUDA batch APIs; those APIs also preserve free-device-memory headroom.
- `--output-budget-bytes` bounds each materialized CUDA result chunk and the
  final JSON report.
- `--evaluation-chunk` bounds deterministic outer chunks. The underlying CUDA
  APIs may subdivide further if device limits require it.
- No unbounded per-trace output is written. Exact totals and depth histograms
  are retained while witness examples are capped.

The host budget covers the explicitly controlled heap buffers. It is not an
OS-level process limit and does not account byte-for-byte for allocator
metadata, C++ runtime state, CUDA runtime state, or stack frames.

## Build and focused tests

The targets are fixed to the repository's native CUDA architecture setting,
`75-real`:

```bash
cmake -S /home/wryan/rule30-lab \
  -B /tmp/rule30-extended-search-build -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc \
  -DCMAKE_CUDA_ARCHITECTURES=75 \
  -DRULE30_ENABLE_CUDA=ON
nice -n 10 cmake --build /tmp/rule30-extended-search-build \
  --parallel 2 \
  --target rule30_cuda_extended_period_search \
           rule30_cuda_extended_period_search_tests
ctest --test-dir /tmp/rule30-extended-search-build \
  -R rule30_cuda_extended_period_search --output-on-failure
```

The CPU tests cover independent brute-force agreement, validation and caps,
`c[0]` filtering, duplicate descriptions versus distinct traces,
determinism, and chunk-boundary invariance. The GPU tests use 32 distinct
traces, 17-candidate chunks, and seven threads per block so neither launch
grid nor final chunk divides evenly. They compare every finite count,
histogram bin, and compact witness against the CPU path, then repeat with
five-candidate chunks.

During the 2026-07-21 canonical focused validation, CUDA 13.3 compiled both
targets for `sm_75`. The CPU suite passed, and the GPU suite ran directly on
the local RTX 2060 SUPER (compute capability 7.5) rather than relying on
CTest's skip handling. Every finite total, histogram bin, and compact witness
matched the CPU oracle for both uneven chunk configurations. The CPU path also
passed AddressSanitizer and UndefinedBehaviorSanitizer in a CUDA-enabled debug
build. `run_quality_gates.sh` invokes the GPU test directly, so an inaccessible
device is a hard failure on the canonical workstation.

## Focused finite observation

A conservative `nice -n 10` CPU-oracle run extended the development check to
`q=0..8`, `p=1..12`, and `H=64`, using 512-trace chunks and a 512 MiB host
budget. Exact accounting for that run was:

- 4,185,090 descriptions in the full box;
- 2,092,545 descriptions retained by the `c[0]=1` seed condition;
- 1,028,096 distinct finite traces after deduplication;
- 1,064,449 duplicate descriptions;
- zero traces compatible through all 64 reconstructed left cells;
- first nonzero witnesses at depths 1 through 20, with no later witness;
- 2.71 seconds internal end-to-end time and 199,936 KiB process maximum RSS.

The canonical rerun used 32,768-trace chunks for both backends. The CPU oracle
took 2,719.29 ms end to end. CUDA matched the complete finite payload and took
3,302.93 ms end to end, including 1,041.03 ms for common host generation and
deduplication. Its measured kernels totaled 1,709.03 ms and the two CUDA API
calls totaled 1,884.89 ms. Peak accounted device allocation was 10,715,136
bytes. The GPU was therefore about 21% slower end to end for this workload;
the result is a consistency validation, not a GPU speedup. The temperature was
40 C before and 41 C after the bounded run.

This is a finite exhaustive result for that exact description box and horizon
on two agreeing backends. In particular, the observed depth-20 ceiling is a
finite pattern, not a depth-independent invariant.

A subsequent pure-period CPU run covered every period description from 1
through 20 at horizon 128: 1,048,575 seed-compatible descriptions, 1,047,479
distinct finite traces, and no finite survivors. Its latest first witness was
again depth 20. This larger pure-period box is also only a finite result.

## Prefix-equivalence interpretation

The follow-up proof in
[`problem1_sideways_prefix_equivalence.md`](../proofs/informal/problem1_sideways_prefix_equivalence.md)
shows that, for a fixed initial center bit and zero right half, the first
reconstructed one is exactly the first time the proposed center trace differs
from the corresponding zero-left reference trace. The independent direct
prefix campaign reproduced every description-level histogram count above.

Consequently, this CUDA search produces valid finite incompatibility
certificates, but its first-witness exclusions contain the same mathematical
information as direct comparison with the trusted center prefix. Sideways
reconstruction remains useful for richer tail questions; it is not an
independent route to nonperiodicity when only the first reconstructed one is
recorded.

## Interpretation

`status: finite-exhaustive` means only that every description in the recorded
finite parameter box was accounted for and every distinct generated trace was
tested through the recorded horizon. Neither an incompatibility histogram nor
the absence of finite survivors establishes an infinite statement. Duplicate
descriptions are an encoding issue, not additional mathematical evidence.
