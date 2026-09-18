# Astra automation handoff — run 108 — 2026-09-18

## Starting state

No intervening repository work was present after run 107. Starting branch tip: `842f6909bee218a994af560931dfd41ead3a5e34`.

## New stopping fence

Added `proofs/informal/problem1_birth_spacing_does_not_supply_finite_support_budget.md`.

The established `>=8` separation of sufficiently late nonresetting sources gives only a linear-in-time upper bound on their count and is fully compatible with infinitely many sparse events. Finite initial spatial support does not upgrade this to a finite count: radius-one locality allows arbitrarily many later event cones to reuse the same original support cells.

The existing two-bit nonresetting passage also forces `beta=1` regeneration at `t+6`. Therefore a naive budget based on current lag rows/defects/local population is renewable rather than manifestly decreasing. A genuine finite-support birth budget must prove non-reuse: injectively charge births to unused original-fringe data, strictly decrease a well-founded original-fringe potential, or establish anchored incompatibility between repeated regenerative passages.

This supplies a concrete audit criterion for the next proposed all-depth invariant: test it against the forced `beta=1` passage and reject it if the same original fringe datum can be charged again.

Problem 1 remains OPEN.

Research commit: `921d9b9fbe232a4fd06886d95d075c35b73553f3`.
