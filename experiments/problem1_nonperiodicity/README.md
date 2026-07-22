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
