# Astra automation handoff — 2026-09-18 run 113

## Repository state reviewed

Starting branch: `research/astra-next`

Starting tip: `eb64b6f7f5311e4e4cdda333ec18c6ff139133a6`

No intervening work was present after run 112. The current unresolved target remains Wolfram Prize Problem 1. The recent line of work has established that fixed moving-right-fringe prefixes evolve by triangular Boolean permutations of 2-power order, and run 112 upgraded this to pro-2 recurrence of the infinite instantaneous moving fringe.

## New result

Added:

`proofs/informal/problem1_finite_fringe_factors_have_only_dyadic_cycles.md`

The new theorem strengthens run 112 as follows.

Let `Phi` be any continuous finite-valued observable of the instantaneous infinite moving-right fringe that is a genuine dynamical factor: `Phi(Fx)=G(Phi(x))` for a deterministic finite-state update `G`. Continuity into a finite discrete state space forces `Phi` to depend on some finite prefix. Since that prefix update has 2-power order, every reachable cycle of `G` also has power-of-two length.

Hence no finite deterministic summary of the instantaneous moving fringe can carry a nonconstant odd-order clock. In particular, if a FULL/nonreset argument can produce a finite fringe-determined phase whose actual cycle has odd period (or any period with an odd prime factor), that would immediately contradict the pro-2 fringe dynamics.

This also supplies a stopping fence: merely enlarging the fringe prefix, assigning more finite phase labels, or quotienting the prefix into a finite automaton cannot create a non-dyadic recurrence. Any useful non-dyadic phase must either yield the contradiction above or necessarily depend on extra source/history/core/global-shadow information.

## Next target

Audit the existing FULL/nonreset source-phase machinery for a forced nonconstant odd-order phase cycle. For any candidate phase, check three properties separately:

1. Is it determined by the instantaneous moving fringe (therefore by a finite prefix)?
2. Is its time transport deterministic from that state?
3. Does FULL force a reachable cycle with an odd factor in its period?

If all three hold, Problem 1 gets a direct contradiction. If not, record exactly which extra history/core datum the phase needs; that datum is a candidate location for the missing non-telescoping information.

## Status

Problem 1 remains OPEN.

Research commit for the new proof note: `eb3b6d3275c801109d61aa516266d1105d0071c2`.
