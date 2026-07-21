# Architecture

## Trust boundary

The supplied Python file is evidence to reproduce, not an oracle. A simple
coordinate-indexed cell-array implementation and hand-derived rows establish
the first trusted layer. Shared vectors are then frozen with hashes and used by
every backend.

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

The primary interchange format for a center sequence is one byte per bit for
small trusted artifacts and little-endian packed 64-bit words for large
streams. Every file records bit order, logical bit length, and SHA-256.

## CLI/backend boundary

The Python CLI invokes a common semantic operation. Native executables accept
the same explicit prefix convention and can emit JSON. Backend disagreement is
a failed verification, never resolved by majority vote.
