# Astra automation handoff — run 91 — 2026-09-17

## Starting state

No intervening repository work was present after run 90. Starting branch tip: `bdfb4e62b29533a251c1d6db655a5d3ed2ee1615`.

## New result

Added `proofs/informal/problem1_fixed_period_portal_trees_are_finite.md`.

Run 90 left open whether a newly attached exact-period-`n` portal tree can have an infinite branch. At fixed finite `n`, it cannot. The exact-period necklace state space is finite. An infinite descendant branch would therefore repeat a necklace and contain a directed cycle. A cycle cannot be entered from outside because the first cycle vertex would have two parents, contradicting the established unique-parent/no-merger property. The portal child itself cannot lie on a cycle either: it already has its proper-period portal parent, while the cycle would supply a distinct exact-period-`n` parent. Hence no branch repeats, so every branch is finite and terminates at odd parity by run 90's branching theorem.

A crude depth bound is the number of primitive necklaces

`N_prim(n)=(1/n) sum_{d|n} mu(d) 2^(n/d)`.

For dyadic `n=2^m`, this is `(2^n-2^(n/2))/n`. This bound is exponential and is not the structural control needed for Problem 1.

## Important scope correction

This resolves the fixed-period finiteness question raised by run 90, but it does **not** solve Problem 1. The authoritative `ASTRA_HANDOFF.md` bottleneck is still the contradiction between FULL and finite entry for one actual survivor with its complete original finite fringe / a finite-support birth budget. Fixed-state-space finiteness gives no useful uniform control as period or support grows.

## Problem 1 status

OPEN.

## Next target

Do not spend further runs proving fixed-period portal termination. Connect the portal/parent-map picture back to original finite support. Seek a portal-depth, full-period-birth, or descendant-count bound controlled by original support/width and substantially sharper than the trivial primitive-necklace count. Alternatively use the portal filtration to attack the one continuing candidate left by `problem1_fixed_fringe_phase_collapse.md`.

Research commit: `a6dfba57c31b9a57b3646e662f7d16463b829811`.
