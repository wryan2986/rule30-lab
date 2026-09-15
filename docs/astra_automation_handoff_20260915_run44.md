# Astra automation handoff — 2026-09-15 run 44

## Branch state entering run

`research/astra-next` was still at run 43 handoff commit `3cdaaf512673e3288b7c458645dd26fde9309185`.

Run 43's live target was to turn infinitely many actual period doublings on one FULL/common-origin realization into unbounded multiplicity in one anchored depth/window, enough to contradict the uniform finite-entry bound on `J_n`.

## New result

Recorded `proofs/informal/problem1_naive_backward_event_pullback_fails.md`.

The scalar boundary-hit indicator has no backward monotonicity. From

`(Ax)_i = x_{i+2} XOR (x_{i+1} OR x_i)`, 

a local `001` pattern at coordinates `i,i+1,i+2` has zero boundary pair at time `t` but produces `(Ax)_i=1` at time `t+1`.

Therefore a late doubling-source boundary hit cannot be pulled backward at fixed depth merely by following the same boundary indicator. Distinct late sources likewise cannot be charged injectively to anchored hits without a stronger transport theorem.

Research commit: `4b2f96aa68bfd949b4622c06548f3022a77fd7eb`.

## Problem 1 status

OPEN.

The run does not produce the required multiplicity theorem, but it rules out a natural shortcut in the run-43 plan.

## Next target

Return to the exact doubling gate/source/return formulas and transport a structured certificate, not a naked boundary hit. Search for a property of the full local source window that:

1. is forced at every actual doubling passage;
2. survives a valid causal pullback/transport on the same original realization;
3. remains distinguishable for different doubling passages; and
4. makes `r` transported certificates force `f(r)->infinity` hits in one common anchored/joint window.

The joint-window machinery is the natural framework because it preserves spacetime neighborhood information that the scalar boundary indicator loses.