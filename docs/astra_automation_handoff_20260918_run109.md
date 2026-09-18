# Astra automation handoff — run 109 — 2026-09-18

## Starting state

No intervening repository work was present after run 108. Starting branch tip: `45932e6420ef6a445c4771edfdf3171b6f19554c`.

## New structural stopping fence

Added `proofs/informal/problem1_right_cone_ancestry_reuses_fixed_terminal_support.md`.

For original right support endpoint `R`, a cell at time `t` and fixed offset `j` behind the maximal right ray has coordinate `R+t-j`. Its radius-one time-zero backward cone is `[R-j,R+2t-j]`; intersecting the original support `x<=R` leaves exactly the fixed terminal block `[R-j,R]`, independent of `t`.

Thus repeated late events in any uniformly bounded-width right-fringe strip do not acquire new ancestral original support positions. In the extreme `j=0` case, every maximal-right-ray cell has only original cell `R` in its support-side ancestry. This sharpens run 108: an injective birth budget cannot come merely from assigning distinct late events to distinct ancestral cell positions.

A successful original-fringe non-reuse theorem must instead distinguish phase/state/history on this repeatedly reused terminal block and prove non-recurrence or strict consumption across the forced `beta=1` regenerative passage. A concrete next target is therefore the anchored terminal-fringe transition across a nonreset return: prove its relevant finite state graph is acyclic, or find recurrence and reject that candidate budget.

Problem 1 remains OPEN.

Research commit: `bda9e07dde715d8f9d92117a256c9c9f865a3746`.
