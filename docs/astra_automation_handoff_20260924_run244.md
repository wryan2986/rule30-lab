# Astra automation handoff — run 244 — 2026-09-24

Problem 1 remains open.

## Entry state

The branch entered at run 243 commit `6400f72cb7bd85b258cef6dbf8e5a2a1dc117318`; there was no intervening work.

Run 243 proved compatibility after two consecutive doublings and explicitly directed the next run to an intervening plateau, especially `double / plateau / double`.

## New result

For

`O_{r-3}=Q`, `O_{r-2}=2Q`, `O_{r-1}=2Q`,

on a state realizing the first doubling write

`X_{r-2}=(C,bar C)`, `X_{r-3}=(B,B)`, `Y=X_{r-1}=(Y0,Y1)`, and `D=Y0 xor Y1`.

The plateau half-difference obeys

`Delta D = bar B`.

For the next forcing `H=f_r=Y OR X_{r-2}`, exact Boolean algebra gives

`H0 xor H1 = 1 + Y0 + D*C`

pointwise.  Since `Q` is even, the full forcing parity is therefore

`parity(H) = parity(Y0) xor <D,C>`.

Thus the final doubling in the `double / plateau / double` pattern is decided exactly by

`parity(Y0) xor <D,C> = 1`.

This reduces the next order decision to a concrete bilinear parity functional instead of a generic compatibility question.

## Computational evidence

Exhaustive enumeration at both available instances shows an additional rigidity:

- `4 -> 8 -> 8 -> 16`: full-period coordinate-5 plateau states have top-coordinate complexity 5 or 8; every witness of the subsequent doubling lies in complexity class 8.
- `16 -> 32 -> 32 -> 64`: full-period coordinate-8 plateau states have top-coordinate complexity 17 or 26; every witness of the subsequent doubling lies in complexity class 26.

So a full-period plateau alone does not force maximal complexity, but the next-doubling functional empirically selects exactly the high-complexity class.

## Files added

- `proofs/informal/problem1_run244_double_plateau_double_decision_functional.md`
- this handoff

## Next target

Prove, using the special adjacent Rule-30 relations, why `parity(Y0) xor <D,C>` can be 1 only on the high-complexity plateau branch, or find the first larger-width counterexample.  Do not retreat to a generic Hadamard-product valuation bound; run 241 already showed that valuations alone are insufficient.  The useful structure is now the exact relation `Delta D=bar B` together with the adjacency relation between `B` and `C`.