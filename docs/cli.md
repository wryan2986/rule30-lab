# Unified command-line interface

`rule30` is the finite-scope front end for the verified Python analysis
modules and the independently built native center-sequence engines. It does
not make an infinite mathematical claim from a finite computation.

Install the local package in the project virtual environment, or invoke the
module directly:

```bash
.venv/bin/pip install -e .
.venv/bin/rule30 --help
.venv/bin/python -m rule30lab.cli --help
```

## Output conventions

Every analytical command supports `--format text` and `--format json`.
`--json` remains an exact compatibility alias for `--format json`. Supplying
`--json` together with a non-JSON format is an error.

`generate` additionally supports `--format raw`:

- `text` writes one ASCII `0`/`1` string followed by a newline;
- `raw` writes exactly `N` numeric bytes, each with value zero or one, with no
  header or newline;
- `json` includes the same finite prefix as an ASCII bit string plus its count,
  counts of ones and zeros, discrepancy, bit order, and SHA-256 over the
  numeric-byte representation.

The bit order is always `c_0, c_1, ..., c_(N-1)`. Hash fields ending in
`sha256_u8` cover exactly the one-byte-per-bit numeric representation, not the
ASCII text form.

Analytical JSON has a top-level `status`, `proof_scope`, `interpretation`, and
`limitations`. Statuses describe the stated finite operation only. In
particular, `finite-exhaustive` means every item in an explicitly bounded set
was checked, not that an infinite prize problem was proved.

## Backends and native adapters

Commands that obtain a center prefix accept:

```text
--backend python|cpp-scalar|cpp-avx2|rust|cuda
```

The Python backend is the coordinate-explicit reference implementation. Native
backends are separate processes. The CLI validates their exit status, exact
output length, and every raw byte before analysis. It never invokes a shell.

The executable can be supplied by command option, environment variable, or
`PATH`, in that order:

| Backend | Option | Environment | Default executable |
|---|---|---|---|
| C++ scalar/AVX2 | `--cpp-executable PATH` | `RULE30_CPP_EXECUTABLE` | `rule30_cpp` |
| Rust | `--rust-executable PATH` | `RULE30_RUST_EXECUTABLE` | `rule30-rust` |
| CUDA | `--cuda-executable PATH` | `RULE30_CUDA_EXECUTABLE` | `rule30_cuda_generate` |

The adapters issue these exact interface shapes:

```text
rule30_cpp generate --count N --backend scalar|avx2 --format raw
rule30-rust generate --count N --backend packed --format raw
rule30_cuda_generate generate --count N --format raw
```

The CUDA generator is built as `rule30_cuda_generate`. Selecting `cuda` gives
a clear unavailable-binary error until that executable is placed on `PATH` or
explicitly configured. `--timeout SECONDS` applies to each native process and
is capped at one hour; the default is 120 seconds.

## Generation, verification, and timing

Generate a small Python reference prefix:

```bash
rule30 generate --count 80
rule30 generate --count 10000 --format raw > center_10000.u8
rule30 generate --count 10000 --json
```

Generate with a native engine:

```bash
rule30 generate --count 1000000 --backend cpp-avx2 \
  --cpp-executable /path/to/rule30_cpp --format raw > center_1m.u8
```

`verify` requires at least two distinct repeated `--backend` options. It
compares the actual numeric-byte arrays and reports hashes and the first
mismatch, rather than accepting matching summary counts:

```bash
rule30 verify --count 10000 \
  --backend python --backend cpp-scalar --backend cpp-avx2 --backend rust \
  --cpp-executable /path/to/rule30_cpp \
  --rust-executable /path/to/rule30-rust --json
```

`benchmark` repeatedly generates and materializes the same raw-byte output and
checks that every repetition is identical:

```bash
rule30 benchmark --count 250000 --backend cpp-avx2 \
  --warmups 1 --repetitions 7 --json
```

For Python, timing is in-process generation plus byte materialization. For a
native backend it includes process launch, generation, and pipe capture. The
scope is recorded explicitly, and the CLI makes no cross-workload speed claim.

## Finite analyses

Balance and discrepancy at explicit checkpoints:

```bash
rule30 balance --count 1000000 --backend cpp-avx2 \
  --checkpoint 100 --checkpoint 1000 --checkpoint 10000 \
  --checkpoint 100000 --checkpoint 1000000 --json
```

Overlapping block counts and uncentered spin autocorrelation:

```bash
rule30 blocks --count 10000 --width 4 --width 8 --json
rule30 autocorrelation --count 10000 --lag 1 --lag 2 --lag 16 --json
```

Finite-prefix GF(2) Berlekamp–Massey complexity:

```bash
rule30 linear-complexity --count 5000 --json
```

Bounded final-suffix period comparison:

```bash
rule30 period-search --count 10000 --min-period 1 --max-period 1000 \
  --top 20 --json
```

For each candidate period `p`, this compares backward from the end while
`c_t = c_(t-p)` and reports the bit length of the maximal final suffix obeying
that recurrence. The final `p` bits form the vacuous base of such a suffix.
Even a long finite match does not establish eventual periodicity.

Finite sideways reconstruction can use the true generated trace, an explicit
trace, a pure periodic trace, or a preperiod-plus-period trace:

```bash
rule30 sideways-reconstruct --horizon 500 --json
rule30 sideways-reconstruct --horizon 20 --trace 110111001101001111001 --json
rule30 sideways-reconstruct --horizon 100 --period 01101 --json
rule30 sideways-reconstruct --horizon 100 --preperiod 110 --period 01 --json
```

The supplied trace contains `H+1` bits `c_0` through `c_H`; output contains
the `H` reconstructed cells `x_-1(0)` through `x_-H(0)`. A finite all-zero
output does not imply an infinite all-zero tail.

Equal-length finite 2-kernel diagnostics:

```bash
rule30 automaticity-search --min-level 1 --max-level 9 \
  --prefix-length 64 --backend cpp-avx2 \
  --cpp-executable /path/to/rule30_cpp --json
```

When `--count` is omitted, the command generates exactly
`prefix_length * 2^max_level` bits. An explicit smaller count is rejected.
Distinct finite prefixes do not establish nonautomaticity.

Bounded predictor searches use a strict training/held-out split:

```bash
rule30 predictor-search --count 10000 --train-length 5000 \
  --method berlekamp-massey --json
rule30 predictor-search --count 10000 --train-length 5000 \
  --method dfao --max-states 3 --max-models 100000 --json
rule30 predictor-search --count 10000 --train-length 5000 \
  --method gf2 --max-order 12 --max-completions 100000 --json
rule30 predictor-search --count 10000 --train-length 5000 \
  --method boolean-window --max-window 12 --max-completions 100000 --json
```

`--method all` runs all four bounded families. Models are fixed from training
bits before held-out validation. A failed search is not a lower bound; a
finite held-out fit is not an infinite recurrence.

## Allowlisted experiments

`experiment` can execute only these repository scripts:

| Name | Script |
|---|---|
| `problem1-sideways` | `experiments/problem1_nonperiodicity/run_sideways_search.py` |
| `problem2-finite-prefix` | `experiments/problem2_balance/run_finite_prefix.py` |
| `problem2-scaling` | `experiments/problem2_balance/run_scaling_analysis.py` |
| `problem2-conservation` | `experiments/problem2_balance/search_local_conservation.py` |
| `problem3-exact-searches` | `experiments/problem3_complexity/run_exact_searches.py` |

No command string, shell syntax, or arbitrary script path is accepted. Child
arguments are separate argv entries following `--`:

```bash
rule30 experiment run problem2-conservation -- \
  --minimum-width 1 --maximum-width 5
rule30 experiment reproduce --json problem3-exact-searches -- \
  --limit-bits 10000 --train-length 5000
```

`run` records the child stdout hash and parses JSON when possible.
`reproduce` executes the same argv twice. It compares exact stdout bytes by
default; when both JSON outputs publish `scientific_payload_sha256`, it compares
that documented scientific payload hash so empirical runtime metadata may
differ without masking scientific reproducibility.

## Conservative controls

The CLI applies hard local caps before expensive work:

| Resource | Cap |
|---|---:|
| Python coordinate generator | 10,000 bits |
| C++ scalar/AVX2 generator | 10,000,000 bits |
| Rust packed generator | 10,000,000 bits |
| CUDA direct generator | 100,000 bits |
| General Python analysis input | 1,000,000 bits |
| Berlekamp–Massey / predictor input | 20,000 bits |
| Sideways horizon | 2,000 |
| Block-frequency table | 65,536 entries |
| Candidate-period worst-case comparisons | 50,000,000 |
| CLI text/JSON/raw output | 16 MiB |
| Allowlisted child stdout or stderr | 16 MiB each |
| Native process timeout | 3,600 seconds maximum |

These caps are intentionally conservative and are not performance claims.
Use a native packed backend for larger prefixes. The CLI performs no network
access, hardware control, overclocking, or remote execution.

Successful commands return zero. `verify` returns one for a byte mismatch, and
`experiment reproduce` returns one for a reproducibility mismatch. Usage,
validation, unavailable-executable, resource-limit, child-process, and timeout
errors return two through `argparse`.
