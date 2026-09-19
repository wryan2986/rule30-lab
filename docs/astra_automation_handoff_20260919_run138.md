# Astra automation handoff — 2026-09-19 run 138

## Starting state

Started from branch `research/astra-next` after run 137. No intervening research work was found before this run.

Problem 1 remains open.

## New result

Derived an exact moving-frame recurrence at the deterministic left support front of every finite-support Rule-30 orbit.

If `L` is the initial leftmost 1 and

`y_j(t)=x_{L-t+j}(t)`,

then, with `y_{-1}=y_{-2}=0`,

`y_j(t+1)=F(y_{j-2}(t),y_{j-1}(t),y_j(t))`.

This is triangular and autonomous on every fixed-width prefix. It immediately yields the universal stabilized prefix `110`, with offset 3 alternating with period 2.

Full note:

`proofs/informal/problem1_left_front_moving_frame_exact_recurrence.md`

## Why it matters / stopping fence

This gives an exact finite-state moving-cut representation of the finite-support boundary, a natural candidate for the finite-range half of the missing birth-budget argument.

But the distinguished source-relative `011` events from runs 133--137 stay near the fixed center while the left front moves left at speed one. Their moving-frame index therefore grows linearly. Consequently, no fixed-width left-front state directly counts those events. Do not spend another run merely enlarging a fixed front window unless a transported quantity to the source has been identified.

## Best next target

Look for a low-complexity quantity transported from the triangular left-front system along the right-moving sensitive characteristic terminating at the distinguished `011` event. The quantity must have finite range and bounded reuse across cyclic episodes. A parity/affine invariant or small finite automaton is the most concrete next computational target.

Problem 1 remains open.