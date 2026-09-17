# Astra automation handoff — run 95 — 2026-09-17

## Starting state

No intervening repository work was present after run 94. Starting branch tip: `2c16dcc42ec20b8c8cdca12f60f3ee42297c3748`.

## New result / strategy no-go

Added `proofs/informal/problem1_portal_axioms_no_support_bound.md`.

Runs 90--94 give a strong abstract package for a new full-period portal component: unique parent/no mergers, binary branching at even vertices, odd terminal leaves, fixed-period finiteness, `O=E+1`, Kraft conservation, period filtration, and exact dyadic primitive parity counts. The new note proves that this package alone cannot imply the finite-support birth bound required by `ASTRA_HANDOFF.md`.

At dyadic `n`, a complete binary tree of depth `d` has `E=2^d-1` and `O=2^d` and satisfies all tree/parity/Kraft constraints. Whenever these fit inside the ambient exact counts `N_even(n)` and `N_odd(n)`, its vertices can be injectively labelled by the corresponding primitive parity classes. Hence the established abstract constraints admit countermodels with unbounded depth as `n` grows. In particular, at `n=32` a complete depth-25 tree already fits the census.

This is explicitly a logical countermodel to deduction from the current abstract constraints, not a claim that the actual Rule-30 parent map realizes such a tree.

## Strategic consequence

Further ambient necklace/parity/tree counting cannot close the authoritative gap unless it introduces information coupling the portal state to the one actual survivor's finite support or complete fringe. The next useful lemma should involve `(portal state, actual fringe phase)` or a branch-prefix/finite-support charging map. Candidate forms are listed in the new proof note.

## Problem 1 status

OPEN.

Research commit: `b50e8633853f9f6124b2159e40a8ab33eda1449c`.
