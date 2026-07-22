# Polynomial conservation search

Status: `finite-exhaustive` for each listed linear system and `inconclusive`
for Problem 2.

## Search family

For a density `rho` on `k` cells, a time displacement `tau`, and a flux `J`
on `k + 2*tau - 1` cells, the search imposes

```text
rho(F^tau(w)) - rho(w[tau:tau+k]) = J(w[:-1]) - J(w[1:])
```

for every binary word `w` of length `k + 2*tau`. The density and flux are
multilinear polynomials in Boolean cell variables. Their canonical feature
bases contain every square-free monomial through separately bounded density
and flux degrees. The coefficients remain linear unknowns, so the resulting
systems can be solved exactly over the rationals or GF(2), even though degree
two and higher features are nonlinear functions of the cells.

The previous lookup-table search already spans every function on a block at a
fixed tested width. Thus polynomial coordinates do not add functions at those
same widths. Their value here is that bounded degree permits wider supports,
and the generalized equation also tests `tau > 1` identities. This distinction
prevents a change of basis from being misreported as a larger mathematical
family.

## Quotient and certificates

The reported `nontrivial_excess_nullity` quotients out:

- constant density;
- constant flux; and
- the full intersection of representable spatial coboundaries with the chosen
  polynomial basis.

For the third class, `g` ranges over every function on width-`k-1` blocks. The
implementation converts the induced density and flux truth tables to unique
multilinear coefficients, solves the exact constraints that discard
out-of-basis monomials, and retains the complete admissible image. This is
stronger than quotienting only a convenient list of low-degree `g` monomials.

Every result contains:

- the complete feature ordering and coefficient-matrix SHA-256;
- rank, nullity, trivial rank, coboundary rank, and excess nullity;
- pivot and free columns;
- sparse exact RREF, kernel, trivial, and quotient-complement bases;
- SHA-256 hashes for each certificate basis; and
- the deterministic caps used to bound the calculation.

`verify_search_certificate` reconstructs the finite matrix and the full
representable coboundary intersection, checks every kernel residual and rank,
and rejects altered quotient or excess claims. Tests include deliberate
certificate tampering to catch false positives.

Rule 204 is the positive control. Its identity evolution conserves nonconstant
cell observables, so every control below must retain nonzero excess after the
same quotient procedure.

## Reproduction commands

Run the focused tests:

```bash
cd /home/wryan/rule30-lab
PYTHONDONTWRITEBYTECODE=1 .venv/bin/pytest -q -p no:cacheprovider \
  tests/python/test_polynomial_conservation.py
```

Reproduce the three campaign blocks as structured JSON:

```bash
PYTHONDONTWRITEBYTECODE=1 nice -n 10 .venv/bin/python \
  experiments/problem2_balance/search_polynomial_conservation.py \
  --minimum-width 6 --maximum-width 8 \
  --density-degree 2 --flux-degree 2 --time-steps 1 \
  --field rational --field gf2 --compact

PYTHONDONTWRITEBYTECODE=1 nice -n 10 .venv/bin/python \
  experiments/problem2_balance/search_polynomial_conservation.py \
  --minimum-width 6 --maximum-width 7 \
  --density-degree 3 --flux-degree 3 --time-steps 1 \
  --field rational --field gf2 --compact

PYTHONDONTWRITEBYTECODE=1 nice -n 10 .venv/bin/python \
  experiments/problem2_balance/search_polynomial_conservation.py \
  --minimum-width 4 --maximum-width 6 \
  --density-degree 2 --flux-degree 2 --time-steps 2 \
  --field rational --field gf2 --compact
```

The script writes only to standard output. No result record is created or
overwritten.

## Small finite campaign

The campaign was run on 2026-07-21. In the table, `d` and `q` are density and
flux degree, `u` is the unknown count, and `T/C/E` are certified total trivial,
spatial-coboundary, and excess dimensions.

| Field | tau | k | d/q | Equations | u | Rank | Nullity | T/C/E |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rational | 1 | 6 | 2/2 | 256 | 51 | 49 | 2 | 2/0/0 |
| rational | 1 | 7 | 2/2 | 512 | 66 | 64 | 2 | 2/0/0 |
| rational | 1 | 8 | 2/2 | 1,024 | 83 | 81 | 2 | 2/0/0 |
| GF(2) | 1 | 6 | 2/2 | 256 | 51 | 44 | 7 | 7/5/0 |
| GF(2) | 1 | 7 | 2/2 | 512 | 66 | 58 | 8 | 8/6/0 |
| GF(2) | 1 | 8 | 2/2 | 1,024 | 83 | 74 | 9 | 9/7/0 |
| rational | 1 | 6 | 3/3 | 256 | 106 | 95 | 11 | 11/9/0 |
| rational | 1 | 7 | 3/3 | 512 | 157 | 144 | 13 | 13/11/0 |
| GF(2) | 1 | 6 | 3/3 | 256 | 106 | 95 | 11 | 11/9/0 |
| GF(2) | 1 | 7 | 3/3 | 512 | 157 | 144 | 13 | 13/11/0 |
| rational | 2 | 4 | 2/2 | 256 | 40 | 38 | 2 | 2/0/0 |
| rational | 2 | 5 | 2/2 | 512 | 53 | 51 | 2 | 2/0/0 |
| rational | 2 | 6 | 2/2 | 1,024 | 68 | 66 | 2 | 2/0/0 |
| GF(2) | 2 | 4 | 2/2 | 256 | 40 | 38 | 2 | 2/0/0 |
| GF(2) | 2 | 5 | 2/2 | 512 | 53 | 51 | 2 | 2/0/0 |
| GF(2) | 2 | 6 | 2/2 | 1,024 | 68 | 66 | 2 | 2/0/0 |

Campaign result-set SHA-256 values, computed over canonical structured result
arrays, were:

- one-step degree 2: `cc95c4cca2cb195c5d0ab2b2b3e9c5d64bd114f662df67cc3bbdc79b7ce86f72`;
- one-step degree 3: `f1688a4bf4c8b66f141d9521d63d0322f0c3efd6b12b94e9d6f02842fb49d44e`;
- two-step degree 2: `7566f58d12b9d61987231578751bbae4633d3d1c7301dc37fb4f7580ad863551`.

All 16 Rule 30 systems had zero excess after the certified quotient. All six
matching Rule 204 controls had excess nullity two. The differing rational and
GF(2) trivial dimensions in some one-step systems are expected: polynomial
degree after Boolean rule composition depends on the coefficient field, and
the quotient keeps only coboundaries representable in that system.

## Interpretation and limits

This campaign found no new conservation identity in its bounded family. It
does not show that Rule 30 lacks a conservation law, telescoping observable,
higher-degree identity, wider identity, longer-time relation, identity over a
different algebra, or nonlocal structure. Failure in this family also says
nothing by itself about the asymptotic center discrepancy `D(N)`.

GF(2) identities conserve parity-valued spatial sums in their stated algebra;
they must not be read as integer-valued balance identities without an
additional lifting argument.

The strongest immediate extension would raise degree and support selectively
where exact ranks remain tractable, or enlarge the ansatz to coupled
space-time observables. Any apparent excess should first be checked against an
expanded coboundary quotient and then verified independently before it is
treated as a mathematical lead.
