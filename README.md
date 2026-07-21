# Rule 30 Lab

Rule 30 Lab is a local, reproducible computational-mathematics environment for
investigating Stephen Wolfram's three Rule 30 prize problems. It contains
independent Python, C++20, Rust, and CUDA implementations; shared reference
vectors; finite searches; statistical diagnostics; and small Lean 4
formalizations.

> **Open-problem warning:** no finite computation establishes an infinite
> Rule 30 claim. Unless a result is explicitly marked `rigorous-proof` and has
> a complete independently checked argument, all three prize problems remain
> open in this repository.

The project is intentionally local to this Windows/WSL2 workstation. It does
not use cloud, remote, or distributed compute. The Git repository has no
remote and must not be published before the project owner's review.

## Current state

Environment setup and reference validation are in progress. See
[`docs/research_status.md`](docs/research_status.md) for claim-level status and
[`results/environment/environment_report.md`](results/environment/environment_report.md)
for the detected machine configuration.

## Quick start

All commands are run inside WSL from the repository root:

```bash
cd /home/wryan/rule30-lab
source .venv/bin/activate
```

Build, test, benchmark, and experiment commands will be added only after each
backend passes the shared reference vectors. Setup details and the exact
system changes are recorded in [`docs/setup_wsl_cuda.md`](docs/setup_wsl_cuda.md)
and [`docs/system_changes.md`](docs/system_changes.md).

## Repository map

- `src/python/`: immutable supplied reference plus the maintained Python CLI.
- `src/cpp/`: scalar packed and optional AVX2 C++20 engines.
- `src/rust/`: independent safe and optimized Rust engines.
- `src/cuda/`: CUDA batch engines and measured row-evolution comparison.
- `tests/reference_vectors/`: independently established trusted data.
- `experiments/`: reproducible Problem 1, 2, and 3 drivers.
- `results/`: machine-readable records and compact derived artifacts.
- `proofs/`: informal arguments and Lean 4 formalizations.
- `docs/`: definitions, protocols, architecture, setup, and research status.

## Result language

Every nontrivial result uses one of these statuses: `empirical`,
`finite-exhaustive`, `heuristic`, `partial-proof`, `rigorous-proof`, `refuted`,
or `inconclusive`. The meanings are fixed by
[`docs/experiment_protocol.md`](docs/experiment_protocol.md).
