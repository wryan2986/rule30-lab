# Problem 2 finite-prefix scaling analysis

## Scope and claim status

This analysis scans one explicit file containing `c_0` through `c_999999`,
encoded as one byte per bit. Every integer count below is exact for that finite
payload. Floating-point ratios are descriptive normalizations. The fitted
power-law exponent is heuristic.

The experiment protocol's allowed statuses are used as follows:

- `finite-exhaustive`: every indicated bit, interval, window, pair, or run in
  the bounded payload was scanned exactly;
- `empirical`: a descriptive floating-point normalization or measured runtime;
- `heuristic`: a model fit that is not a bound or theorem.

Nothing in this report establishes an asymptotic frequency or an asymptotic
discrepancy bound.

## Reproduction

From the repository root:

```bash
nice -n 10 .venv/bin/python \
  experiments/problem2_balance/run_scaling_analysis.py \
  --input /tmp/rule30-cpp-avx2-1000000.u8 \
  > /tmp/rule30-problem2-scaling-million.json
```

The default command requires exactly 1,000,000 bytes. It validates that every
byte is either `0` or `1` before analysis.

Payload identity and run provenance:

- input SHA-256:
  `6fc1e4e2abfb382255b94955467f259be88c1044d09ec361c5039970985a1669`;
- canonical scientific-payload SHA-256:
  `4966233342cce5b43c63dcf2d735d17c3faa2fca56419d55406fc8686d941b3f`;
- first run wall time: `4.642616983` seconds;
- repeat wall time: `4.797724889` seconds;
- first complete JSON-envelope SHA-256:
  `edffb53f04bac04f2795ffde7bb743fb5f2bdb87b1b1dcd195e1a51ed81c3033`.

The two runs produced byte-for-byte identical `scientific_payload` objects and
the same canonical hash. Their complete envelope hashes differ because wall
time is measured. Runtime covers path resolution, input reading, validation,
all analyses, and canonical hashing; it excludes indented JSON serialization.
The input path and runtime are excluded from the canonical scientific hash.
No timestamp is emitted.

A separate direct-loop oracle, without importing `rule30lab.statistics`,
independently matched every documented checkpoint, maximum, run count and
histogram, selected correlation numerator, block range, dyadic summary, and
the regression slope and intercept.

## Exact checkpoint discrepancy

For `D(N) = sum_(t=0)^(N-1) (2c_t - 1)`:

| N | ones | zeros | D(N) | D(N) / sqrt(N) | D(N) / N |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 7 | 3 | 4 | 1.2649110640673518 | 0.4 |
| 100 | 52 | 48 | 4 | 0.4 | 0.04 |
| 1,000 | 481 | 519 | -38 | -1.2016655108639842 | -0.038 |
| 10,000 | 5,032 | 4,968 | 64 | 0.64 | 0.0064 |
| 100,000 | 50,098 | 49,902 | 196 | 0.6198064213930023 | 0.00196 |
| 1,000,000 | 500,768 | 499,232 | 1,536 | 1.536 | 0.001536 |

The integer columns have status `finite-exhaustive`; the two ratio columns
have status `empirical` and result kind `descriptive_finite_normalization`.
The exact representation of the last column is also emitted as the fraction
`D(N)/N`.

## Maximum absolute prefix discrepancy

The first prefix attaining the maximum over all `0 <= n <= 1,000,000` is:

```text
n = 964778
D(n) = 1744
max |D(n)| = 1744
```

Status: `finite-exhaustive`.

## Aligned dyadic intervals

Only complete intervals `[k w, (k+1) w)` are included. The omitted suffix is
reported explicitly for widths that do not divide 1,000,000.

| width | intervals | covered | omitted | min D | max D | max abs D | first maximizing interval and signed D | sum D |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | :--- | ---: |
| 64 | 15,625 | 1,000,000 | 0 | -30 | 34 | 34 | `[874496,874560)`, 34 | 1,536 |
| 256 | 3,906 | 999,936 | 64 | -50 | 62 | 62 | `[674304,674560)`, 62 | 1,530 |
| 1,024 | 976 | 999,424 | 576 | -106 | 122 | 122 | `[624640,625664)`, 122 | 1,516 |
| 4,096 | 244 | 999,424 | 576 | -140 | 230 | 230 | `[622592,626688)`, 230 | 1,516 |
| 16,384 | 61 | 999,424 | 576 | -254 | 256 | 256 | `[212992,229376)`, 256 | 1,516 |
| 65,536 | 15 | 983,040 | 16,960 | -356 | 606 | 606 | `[196608,262144)`, 606 | 1,594 |
| 262,144 | 3 | 786,432 | 213,568 | 104 | 634 | 634 | `[0,262144)`, 634 | 1,158 |

Status: `finite-exhaustive` for the listed widths and complete aligned
intervals only.

## Overlapping block-frequency ranges

Zero-count words are included when taking each minimum. All possible words at
the selected widths occurred at least once in this payload.

| width | windows | observed / possible | minimum count | maximum count | range |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1,000,000 | 2 / 2 | 499,232 | 500,768 | 1,536 |
| 2 | 999,999 | 4 / 4 | 248,947 | 250,482 | 1,535 |
| 3 | 999,998 | 8 / 8 | 124,433 | 125,852 | 1,419 |
| 4 | 999,997 | 16 / 16 | 62,132 | 62,999 | 867 |
| 5 | 999,996 | 32 / 32 | 30,755 | 31,616 | 861 |
| 6 | 999,995 | 64 / 64 | 15,126 | 15,866 | 740 |
| 7 | 999,994 | 128 / 128 | 7,496 | 8,050 | 554 |
| 8 | 999,993 | 256 / 256 | 3,662 | 4,076 | 414 |
| 10 | 999,991 | 1,024 / 1,024 | 871 | 1,083 | 212 |
| 12 | 999,989 | 4,096 / 4,096 | 189 | 305 | 116 |

Status: `finite-exhaustive` for the selected widths and overlapping windows.

## Selected spin autocorrelations

Bits are mapped to `s_t = 2c_t - 1`. The exact numerator is
`sum_(t=0)^(N-lag-1) s_t s_(t+lag)` and the denominator is `N-lag`.

| lag | exact numerator | exact denominator | descriptive ratio |
| ---: | ---: | ---: | ---: |
| 1 | -1,141 | 999,999 | -0.001141001141001141 |
| 2 | 1,650 | 999,998 | 0.0016500033000066 |
| 3 | 359 | 999,997 | 0.000359001077003231 |
| 4 | -874 | 999,996 | -0.000874003496013984 |
| 5 | 257 | 999,995 | 0.000257001285006425 |
| 8 | 1,088 | 999,992 | 0.0010880087040696326 |
| 16 | 468 | 999,984 | 0.0004680074881198099 |
| 32 | -56 | 999,968 | -0.00005600179205734583 |
| 64 | -744 | 999,936 | -0.000744047619047619 |
| 128 | -402 | 999,872 | -0.00040205146258721116 |

The numerator and denominator scans have status `finite-exhaustive`; decimal
ratios have status `empirical` and are descriptive.

## Runs

Exact finite partition:

- run count: `500571`;
- zero runs: `250285`;
- one runs: `250286`;
- first bit: `1`;
- last bit: `1`;
- longest zero run: `19`;
- longest one run and longest overall run: `22`;
- mean run length, exact: `1000000 / 500571`;
- mean run length, decimal: `1.9977186053526872`.

The exact run-length histogram is:

```text
length:count
1:250983   2:124966   3:62042   4:31334   5:15480   6:7897
7:3975     8:1931     9:1025    10:492    11:206    12:114
13:65      14:27      15:13     16:7      17:4      18:4
19:4       20:0       21:1      22:1
```

The partition and histogram have status `finite-exhaustive`. The decimal mean
is a descriptive `empirical` normalization; its numerator and denominator are
retained exactly.

## Heuristic discrepancy-scaling fit

The script performs ordinary least squares on

```text
log(abs(D(N))) = intercept + slope * log(N)
```

using exactly the configured decimal checkpoints
`10, 100, 1000, 10000, 100000, 1000000`. Selection does not depend on the
observed discrepancy magnitude. For this payload no selected discrepancy was
zero. In general, a zero-discrepancy sample is listed and excluded because
`log(0)` is undefined; the driver adds no pseudocount or offset.

The result is:

```text
slope      = 0.5205325925511507
intercept  = -0.33097880171305194
coefficient= 0.7182203939212013
R^2        = 0.9494932898684302
```

Thus the fitted finite-sample form is
`abs(D(N)) approximately 0.7182203939 * N^0.5205325926` at this particular
sample selection. Status: `heuristic`. Changing the checkpoints can change the
slope. This is not an asymptotic estimate, an upper bound, or a proof about
Problem 2.

## Resource bounds and validation

The driver has hard caps of:

- 1,000,000 input bits/bytes;
- 16 selected values per parameter family;
- block width 16;
- 65,536 dense block-table entries.

It summarizes block tables rather than emitting all counts, writes JSON only
to standard output, and emits no timestamps. Focused verification:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest \
  -p no:cacheprovider tests/python/test_scaling_analysis.py -q
```

Result: `6 passed`. Tests cover hand-derived data, explicit zero handling in
the fit, invalid encodings, count and resource caps, deterministic hashing, and
the trusted 10,000-bit vector.
