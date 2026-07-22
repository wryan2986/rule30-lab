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
```

The first exhausts each listed radius-`p` Boolean cone for the condition
`c_(t+p)=c_t`. The second exhausts finite 2-adic quotient maps and checks the
exact `-1/3,1/3` countermodel. The third audits three concrete mechanisms for
the smallest unresolved period, two. The fourth checks the exact inverse-lift
section recurrence. The fifth refutes three resulting finite quotient
candidates and verifies an exact arithmetic support criterion. Their JSON
status is `finite-exhaustive`; the all-width arguments are separately stated
in `proofs/informal/` and no analyzer proves center nonperiodicity.

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
