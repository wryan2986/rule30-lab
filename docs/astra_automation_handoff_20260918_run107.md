# Astra automation handoff — run 107 — 2026-09-18

## Starting state

No intervening repository work was present after run 106. Starting branch tip: `83c1a26dc4683df9ba2039187ed8ed90205ae438`.

## Repository consistency

`ASTRA_HANDOFF.md` still describes the recovered draft `proofs/informal/problem1_fixed_fringe_phase_collapse.md`, claiming finite-horizon uniqueness for a fixed fringe/core-width class, but that draft is absent from the current pushed `research/astra-next` tree. Its theorem was therefore not imported as a proved premise; only the handoff's stated logical shape was analyzed.

## New stopping fence

Added `proofs/informal/problem1_fixed_fringe_finite_horizon_uniqueness_no_go.md`.

The note proves a simple but important logical obstruction: nested finite-horizon candidate sets S_h with S_(h+1) subset S_h and eventual |S_h| <= 1 need not ever become empty. If all late S_h are nonempty, nesting simply identifies one candidate compatible with every horizon. Thus iterating a finite-prefix/phase-collapse uniqueness theorem cannot, by itself, exclude the last infinite survivor.

Finite physical restart does not repair this gap: successive singleton compatible states can simply be successive states of one actual orbit. To finish the route one needs an exclusionary ingredient beyond uniqueness—eventual emptiness, strict consumption of a nonrenewable original-fringe resource, incompatibility between independently anchored unique continuations, or a theorem forcing the unique continuation to create new maxima of Q.

This aligns the older fixed-fringe route with the recent scalar-ledger stopping fence: the missing mathematics is not another multiplicity reduction but a survivor-specific reason the final candidate cannot continue.

Problem 1 remains OPEN.

Research commit: `ffbdb98bcbc7c185522dedc024ba0207e98c407d`.
