# Bounded local-conservation search

Status: `finite-exhaustive` for each listed linear system; `inconclusive` for
Problem 2.

For a width-`k` density `rho` and width-`k+1` flux `J`, the search imposes

```text
rho(F_k(w)) - rho(w[1:-1]) = J(w[:-1]) - J(w[1:])
```

on every binary word `w` of length `k+2`. Here `F_k(w)` is the width-`k`
block obtained by applying Rule 30 to each consecutive neighborhood. Summing
the right side over adjacent spatial positions telescopes.

The implementation builds the complete finite coefficient matrix and computes
its rank exactly over both the rationals and GF(2). It also constructs and
checks an explicit trivial subspace consisting of:

- constant density;
- constant flux; and
- spatial-coboundary densities `g(prefix) - g(suffix)` with their induced
  fluxes.

`nontrivial_excess_nullity` is the dimension left after this certified
subspace. Rule 204 (the identity cellular automaton) is used as a positive
control because the single-cell density is conserved.

Run the bounded search with:

```bash
PYTHONPATH=src/python .venv/bin/python \
  experiments/problem2_balance/search_local_conservation.py \
  --minimum-width 1 --maximum-width 5
```

Even a zero excess at every tested width would not prove that Rule 30 has no
useful telescoping identity. The ansatz fixes the locality, one-step form,
scalar block observables, and coefficient field. It also concerns spatial
sums; a discovered conservation law would still need a separate argument to
control the center-column discrepancy `D(N)`.
