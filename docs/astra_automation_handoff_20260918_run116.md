# Astra automation handoff — run 116 — 2026-09-18

Problem 1 remains OPEN. Continue on `research/astra-next`.

Starting tip was `a06c6baeb456b912e0d615ac82d14f1c930d75f6`; no intervening work was present.

## New result

Added `proofs/informal/problem1_finite_support_escapes_fringe_recurrence_at_depth.md`.

For an actual nonzero finite-support row with original endpoints `L,R`, write moving-right-edge coordinates `a_j(t)=x_{R+t-j}(t)` and `D(t)=max{j:a_j(t)=1}`. The triangular moving-fringe rule gives exactly

    D(t+1)=D(t)+2,
    D(t)=(R-L)+2t.

Indeed if `M=D(t)`, then the next two deepest bits are both forced to 1, while every coordinate deeper than `M+2` stays zero. Thus finite-support physical orbits never return globally in moving coordinates even though every fixed prefix has the established pro-2 recurrence. The failure of global recurrence is carried at depths escaping every fixed observation window.

This explains precisely how finite support evades run 115's continuous-potential no-go: support depth is discontinuous in the product topology. The exact anchored quantity `D(t)-2t=R-L` remembers original support width, but it is conserved rather than consumed and therefore does not itself bound regenerative births.

## Stopping fence / next target

Do not interpret pro-2 prefix recurrence as global recurrence of an actual finite-support row. Any finite-support resource that escapes the continuous-fringe no-go must use observation depth growing with time, equivalent left-boundary/core/history data, or another discontinuous quantity. A merely large fixed fringe window remains ruled out.

A concrete next target is a source-indexed depth/characteristic invariant: test whether forced cyclic births can be charged to strictly ordered characteristics reaching the expanding left boundary, with a proved bounded-reuse property. Support width alone has deterministic `+2` drift independent of births and supplies no depletion.

Research commit: `68270b4f8e599e4fc3004c00fe69b9423ad3bb29`.
