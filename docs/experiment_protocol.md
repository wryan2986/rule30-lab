# Experiment protocol

## Claim statuses

- `empirical`: observed output for explicitly listed finite inputs.
- `finite-exhaustive`: every member of an explicitly bounded finite set was
  checked by a verified implementation.
- `heuristic`: an extrapolation, model fit, or search-guided indication.
- `partial-proof`: a rigorous argument proving less than the full target or
  still conditional on a separately identified fact.
- `rigorous-proof`: a complete mathematical proof whose definitions and
  hypotheses match the stated problem and which has been independently
  checked.
- `refuted`: a precise claim has a verified counterexample.
- `inconclusive`: the procedure does not discriminate the alternatives.

`rigorous-proof` is prohibited for statistical tests, bounded searches, model
fits, and unverified literature deductions.

## Required record

Every nontrivial run writes JSON atomically with these fields:

```json
{
  "experiment_id": "unique-id",
  "timestamp_utc": "ISO-8601",
  "git_commit": "full commit hash",
  "question": "problem1 | problem2 | problem3",
  "hypothesis": "precise statement",
  "backend": "cpp-avx2",
  "parameters": {},
  "hardware": {},
  "software": {},
  "runtime_seconds": 0.0,
  "result_hashes": {},
  "result_summary": {},
  "interpretation": "",
  "status": "empirical",
  "proof_scope": "",
  "limitations": []
}
```

The writer first creates a same-directory temporary file, flushes and closes
it, and then atomically replaces the destination. Interrupted jobs retain a
checkpoint but never a partly written final record.

## Correctness gate

1. Hand-derived rows and an independently written cell-array implementation.
2. Immutable supplied Python reference.
3. Shared vectors and hashes.
4. Compiled scalar implementation.
5. Optimized CPU/Rust/CUDA implementations.
6. Sanitizers and edge cases.
7. Benchmarks only after all previous gates pass.

## Benchmark comparability

Record warm-up, repetitions, median, minimum, maximum, standard deviation,
compiler and flags, input/output sizes, peak memory where available, GPU
transfer time, kernel time, and end-to-end time. Compare only implementations
that produce materially identical outputs and statistics.

## Resource safety

Long jobs expose wall-time, RAM, GPU-memory, and output-size limits. They check
free disk space, checkpoint, resume, log progress, and handle interruption.
Interactive runs use conservative CPU concurrency and chunked GPU work. No
tool may change clocks, voltage, power limits, drivers, or thermal controls.
