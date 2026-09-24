# Astra automation handoff — run 242 — 2026-09-24

Problem 1 remains open.

## Entry state

The branch entered at run 241 commit `270d19f364be198013d7a5eb1769bf3b924014a7`; there was no intervening work.

Run 241 identified Pascal depth with linear-complexity deficiency and left the benchmark of explaining the census jump `L_7(32)=17 -> L_8(32)=26` structurally.

## New results

Two exact dyadic results were proved.

First, if `P=O_{r-1}` and the extension doubles, `O_r=2P`, then the top coordinate over length `2P` has halves `(A, Abar)` for a state witnessing the doubling. Games–Chan therefore gives

`max L(X_r) = P + 1 = O_r/2 + 1`.

This exactly explains `L_7(32)=17`, and likewise the earlier doubling-step maxima 3, 5, 9, 17.

Second, suppose `O_{r-2}=P` and `O_{r-1}=2P`. At horizon `2P`, write

`x_{r-1}=(A,A)` or `(A,Abar)`, and `x_{r-2}=(B,B)`.

For `f_r=x_{r-1} OR x_{r-2}`, on the complementary branch the two forcing halves satisfy the exact identity

`F0 XOR F1 = NOT B`.

Therefore Games–Chan gives

`L(F_r)=P+L(NOT B)`

and cyclic integration gives

`L(X_r)=P+L(NOT B)+1`.

At width 8, `P=16` and the maximal complexity of `B=x_6` is 9, so every state has `L(X_8)<=26`; run 241 already supplied exhaustive witnesses attaining 26. Hence

`L_8(32)=26 = 16+9+1`.

The formerly unexplained width-8 complexity is now structurally accounted for.

## Files added

- `proofs/informal/problem1_run242_doubling_step_linear_complexity_exact.md`
- `proofs/informal/problem1_run242_nondoubling_after_doubling_complexity_bound.md`
- this handoff

## Next target

Develop the dyadic half-difference rule across longer doubling/non-doubling patterns. The immediate technical issue is compatibility of maximizers: the upper bound `P+L_{r-2}(P)+1` is automatic after a preceding doubling, but equality requires a state that both selects the complementary branch at level `r-1` and maximizes the lower coordinate complexity. A compatibility lemma, or a counterexample to one, is the next useful target.

Do not return to generic Hadamard valuation inequalities; run 241 already showed they lose the needed dynamical information.