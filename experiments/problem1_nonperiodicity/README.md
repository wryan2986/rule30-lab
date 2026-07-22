# Bounded Problem 1 experiments

`run_sideways_search.py` emits deterministic JSON to standard output. It
checks pure-period and preperiod-plus-period descriptions with exact finite
parameters, validates the trusted true center trace by sideways reconstruction,
and summarizes explicitly fixed-width state graphs.

Default run:

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/run_sideways_search.py \
  > /tmp/rule30-problem1-sideways-default.json
```

The JSON includes compact first-failure certificates and labels the result
`finite-exhaustive`. It does not claim eventual nonperiodicity.

See [`docs/problem1_sideways_research.md`](../../docs/problem1_sideways_research.md)
for conventions, validation, exact default results, and limitations.

Two focused exact analyzers support the current right-edge proof work:

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_defect.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_two_adic_diagonal.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  experiments/problem1_nonperiodicity/analyze_period_two.py
```

The first exhausts each listed radius-`p` Boolean cone for the condition
`c_(t+p)=c_t`. The second exhausts finite 2-adic quotient maps and checks the
exact `-1/3,1/3` countermodel. The third audits three concrete mechanisms for
the smallest unresolved period, two. Their JSON status is
`finite-exhaustive`; the all-width arguments are separately stated in
`proofs/informal/` and no analyzer proves center nonperiodicity.

Reviewed controlled-run records for the defaults are stored at:

- `results/runs/p1-period-defect-20260722.record.json`
- `results/runs/p1-two-adic-diagonal-20260722.record.json`
- `results/runs/p1-period-two-audit-20260722.record.json`
