# Astra automation handoff — 2026-09-24 run 241

## Status

Problem 1 remains open. No intervening work was present after run 240 when this run began.

## New result

Run 240's `(z+1)`-adic/Pascal-depth invariant has an exact standard interpretation. For an `N=2^m` periodic binary word `X`,

\[
L(X)=N-\nu_{z+1}(X),
\]

where `L` is binary linear complexity. Therefore Pascal parity depth is exactly linear-complexity deficiency.

At horizon `N=32`, exhaustive prefix-state enumeration gives:

- `r=2`: min valuation 30, max LC 2
- `r=3`: 29, max LC 3
- `r=4`: 27, max LC 5
- `r=5`: 24, max LC 8
- `r=6`: 23, max LC 9
- `r=7`: 15, max LC 17
- `r=8`: 6, max LC 26

This independently reproduces the width-8 depth-six result.

The cyclic forcing identity `z F_r=(1+z)X_r` is equivalently `L(F_r)=L(X_r)-1` for nonzero words.

## Dead end closed

A generic Hadamard-product valuation inequality is insufficient. `A=1+z` and `B=z+z^2` both have valuation 1, but `A odot B=z` has valuation 0. At `N=32`, cyclic shifts of `(1+z)^d` similarly produce valuation-zero products for every tested `d=1,...,15` despite both inputs having valuation at least `d`.

So any useful lower bound must exploit the special adjacent-coordinate dynamical relation, not just the two input valuations.

## Next target

Work in linear-complexity language and seek a dyadic recursion for adjacent Rule-30 coordinate words. The concrete benchmark is to explain

`L_7(32)=17 -> L_8(32)=26`

while `L(F_8)=25` is forced by the coordinate recurrence.

Primary note: `proofs/informal/problem1_run241_pascal_depth_is_linear_complexity_deficiency.md`.