# Checkpointed multi-million discrepancy campaign

`experiments/problem2_balance/run_multimillion_discrepancy.py` measures exact
center-prefix counts at a small, explicit list of multi-million horizons using
the verified packed C++ engine. Each horizon is a fresh evolution. Completed
runs are atomically persisted under `results/runs`, so interruption repeats
only the first unfinished horizon.

Every larger run requests all earlier checkpoint counts from the C++ engine.
The driver rejects any disagreement between a smaller run's final count and
the same checkpoint inside a larger run. This overlap is a same-implementation
consistency check, not an independent correctness proof.

The default horizons are 1,000,000, 2,000,000, and 4,000,000, with a hard cap
of 8,000,000 and at most eight horizons. Each subprocess has an explicit wall
limit, runs at nice level 10 by default, emits at most a small JSON summary,
and does not retain the full center sequence. The checkpoint binds the ordered
horizons, backend, and executable SHA-256; `--resume` rejects mismatches.

Persistent output requires a clean committed script and checks HEAD, worktree,
script bytes, and executable bytes before and after the campaign. These are
local provenance checks, not a reproducible-build attestation.

Example after building the release C++ target:

```bash
nice -n 10 .venv/bin/python \
  experiments/problem2_balance/run_multimillion_discrepancy.py \
  --cpp-executable /tmp/rule30-followup-build/src/cpp/rule30_cpp \
  --counts 1000000,2000000,4000000 \
  --checkpoint-state results/runs/p2-multimillion-1m-2m-4m.checkpoint.state \
  --record results/problem2/p2-multimillion-1m-2m-4m.json \
  --experiment-id p2-multimillion-1m-2m-4m \
  --timeout-seconds 300
```

If interrupted after one or more horizons, rerun the exact command with
`--resume`. Checkpointing is between complete evolutions; it does not serialize
and resume the middle of one Rule 30 history.

The required `.checkpoint.state` suffix is covered by the repository ignore
rule. This prevents the runner's own restart artifact from invalidating its
post-run clean-tree provenance check. Top-level runtime is the sum of retained
native subprocess elapsed times, including horizons completed before a resume;
finalization and failed-publication overhead are reported separately or
excluded explicitly.

The record labels exact integer observations at the stated horizons and an
overlap consistency classification. A log-log fit is labeled `heuristic`.
Neither small discrepancy ratios nor a fitted exponent prove `D(N)=o(N)`, a
limiting frequency, or any form of randomness.
