# Bounded Problem 1 experiments

`run_sideways_search.py` emits deterministic JSON to standard output. It
checks pure-period and preperiod-plus-period descriptions with exact finite
parameters, validates the trusted true center trace by sideways reconstruction,
and summarizes explicitly fixed-width state graphs.

Default run:

```bash
cd .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/run_sideways_search.py \
  > /tmp/rule30-problem1-sideways-default.json
```

The JSON includes compact first-failure certificates and labels the result
`finite-exhaustive`. It does not claim eventual nonperiodicity.

See [`docs/problem1_sideways_research.md`](../../docs/problem1_sideways_research.md)
for conventions, validation, exact default results, and limitations.

Focused exact analyzers support the current right-edge proof work:

```bash
cd .
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_defect.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_two_adic_diagonal.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_inverse_lift_sections.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_quotient.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_renewal.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_2adic_zero_countermodels.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_schedule_survivor.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_schedule_coding.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_fringe_language.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two_first_return.py
```

The first exhausts each listed radius-`p` Boolean cone for the condition
`c_(t+p)=c_t`. The second exhausts finite 2-adic quotient maps and checks the
exact `-1/3,1/3` countermodel. The third audits three concrete mechanisms for
the smallest unresolved period, two. The fourth checks the exact inverse-lift
section recurrence. The fifth refutes three resulting finite quotient
candidates and verifies an exact arithmetic support criterion. The sixth
checks the exact renewal law and reduces any final zero streak to a partial
ordinary-integer recurrence controlled modulo 16. The seventh verifies two
rational 2-adic fixed points of that partial map and the linear shadowing bound
for their finite truncations. The eighth constructs the unique zero survivor
for the actual future moving-fringe schedule, proves the exact mismatch
valuation law, identifies the shift-zero survivor with the alternating inverse
lift, and emits its coupled output-pair transducer. The ninth verifies the exact
first-difference schedule coding, finite cylinder counts, ordinary degree law,
and the 304-bit consequence of the actual seven-block periodic shadow. The tenth
checks the autonomous packed fringe map, identifies the branch sequence with
the even-time cell-minus-two trace, and proves the all-time forbidden words
`uu`, `ttttt`, and `ututtu` from complete local dependency cones. The eleventh
derives the exact four-bit first-return selector at `u` events, the four
variable-length survivor return cylinders, and the shared neutral degree
cocycle. Their JSON status is `finite-exhaustive`; the all-width arguments are
separately stated in `proofs/informal/` and no analyzer proves center
nonperiodicity.

Tracked results are:

- `results/problem1/20260722_period_two_renewal_reduction.json`
- `results/problem1/20260722_period_two_2adic_zero_countermodels.json`
- `results/problem1/20260722_period_two_schedule_survivor.json`
- `results/problem1/20260722_period_two_schedule_coding.json`
- `results/problem1/20260722_period_two_fringe_language.json`
- `results/problem1/20260722_period_two_first_return.json`

The original controlled-run records contain machine-local operational metadata
and are intentionally untracked. Public certificate hashes, source commits,
direct reproduction commands, and scope statements are stored in
[`docs/public_provenance/20260722_controlled_run_manifest.json`](../../docs/public_provenance/20260722_controlled_run_manifest.json)
under these entries:

- `p1-period-defect-20260722`
- `p1-two-adic-diagonal-20260722`
- `p1-period-two-audit-20260722`
- `p1-inverse-lift-sections-20260722`
- `p1-period-two-quotient-20260722`
