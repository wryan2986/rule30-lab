# Astra automation handoff — run 111 — 2026-09-18

## Starting state

No intervening repository work was present after run 110. Starting branch tip: `71f8b84290d177d9ed10bf3d3dcecaa2a3479563`.

## New structural refinement

Added `proofs/informal/problem1_moving_fringe_periods_are_dyadic.md`.

For a fixed moving-right-fringe prefix, the Rule-30 update has triangular form

    y_j = x_j XOR f_j(x_0,...,x_{j-1}).

All such triangular XOR permutations on `n` bits form a finite group of size

    product_j 2^(2^j) = 2^(2^n-1).

Hence this group is a 2-group, so every element has power-of-two order. Therefore every fixed-width moving-right-fringe prefix of Rule 30 is not merely purely periodic: its period is a power of two.

A direct enumeration for widths 1 through 12 found only dyadic periods, with maximum observed periods

    1,2,2,4,8,8,16,32,32,64,64,64.

The proof does not depend on the computation.

This refines the stopping fence from run 110. Any invariant observing only finitely many moving-edge bits necessarily repeats after a sufficiently large dyadic shift. A potentially useful new route is to seek an anchored FULL/nonreset phase requirement incompatible with dyadic recurrence, or a coupling between the nested dyadic fringe clock and a core/source-indexed quantity with a non-dyadic obstruction.

Problem 1 remains OPEN.

Research commit: `da6c828cc585ee2f76a9ab432c21f87ab4956217`.
