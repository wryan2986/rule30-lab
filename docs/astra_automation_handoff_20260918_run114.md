# Astra automation handoff — run 114 — 2026-09-18

Problem 1 remains OPEN. Continue on `research/astra-next`.

Starting tip was `72f3c9a549eb8482cd85dbaeb3f0f8426a7365b4`; no intervening work was present.

## New result

Added `proofs/informal/problem1_existing_nonreset_phase_has_no_odd_clock.md`.

Run 113 suggested checking the established FULL/nonreset machinery for a forced nonconstant odd-order phase that could contradict the theorem that every finite continuous instantaneous-fringe factor has only dyadic cycles.

Audit of the strongest pushed passage, `problem1_nonreset_return_birth_spacing.md`, finds no such odd clock. The established return forces a finite gate/source passage (`t,u,t` on the displayed even-source portion), finite shadow-center word `0,0,1`, and in the two-bit case a forced later `beta=1`; none is proved to be a recurrent 3-cycle or any odd-order deterministic return. A finite word of odd length must not be mistaken for an odd-period factor.

The richer core/phase drafts mentioned in `ASTRA_HANDOFF.md` remain absent from the pushed branch, so their details were not promoted beyond the handoff summary. The handoff says that machinery has a parity commutator and no phase-discarding quotient, suggesting core/source dependence; in any case it would have to be proved finite-prefix fringe-determined before run 113 applies.

## Stopping fence

Do not pursue the odd-clock route by relabeling `0,0,1`, `t,u,t`, or one repair/cyclic/birth passage as a period-three cycle. A valid dyadic contradiction needs both a deterministic recurrent odd-factor cycle and finite instantaneous-fringe determination.

The principal unresolved target remains a nonrenewable original-fringe/core resource or another finite-support upper bound on the infinitely required cyclic births.

Research commit: `c9a1059f48a3c19be8556a7bb9aa634462862148`.
