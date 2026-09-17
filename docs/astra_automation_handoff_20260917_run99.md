# Astra automation handoff — run 99 — 2026-09-17

## Starting state

No intervening repository work was present after run 98. Starting branch tip: `bd28acc3425e4b78c8a38b813a54ebd35d50340e`.

## New exact formulation

Added `proofs/informal/problem1_normalized_excess_germ_is_cut_invariant.md`.

For one fixed finite row and any admissible right support bound `R`, define

    q_R(n) = tau(2^n L_R(r)) - n - R.

Run 98's exact covariance immediately gives, for any later cut `R'=R+m`,

    q_(R')(n) = q_R(n+m).

Therefore all admissible cuts define one intrinsic sequence germ `Q(r)=[q_R]` modulo deletion of finite prefixes. In particular boundedness/unboundedness above, infinite positive excursions, and `limsup=+infinity` are cut-independent properties.

The physical delay identity becomes

    tau(Y_(R+n)) = max(q_R(n),0),

so the unresolved scalar target can be stated without any arbitrary bookkeeping coordinate:

> On the FULL finite-fringe domain of an actual finite survivor, prove that the intrinsic normalized-excess germ `Q(r)` is unbounded above.

This is a formulation/normalization advance, not the missing overshoot theorem. It fences off arguments that accidentally charge nominal zero padding or absolute `R`.

## Repository consistency note

The older `ASTRA_HANDOFF.md` still references recovered worktree drafts such as `proofs/informal/problem1_fixed_fringe_phase_collapse.md`; that particular path is not present in the current pushed branch, so its argument was not used as a premise in this run.

## Problem 1 status

OPEN.

Research commit: `697e1aafce4be4e06dfe9d13338d99c5bfc673cc`.
