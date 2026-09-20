# Astra automation handoff — 2026-09-19 run150

Problem 1 remains OPEN.

## New result

A synthesis of two already-proved local descriptions removes the `001` branch from the forced-birth provenance dichotomy for a two-bit nonresetting `t` source.

At the cyclic return `q=t+2`, the distinguished FULL source block is

    (r_-5,...,r_2)(q)=10101110.

Because `q` is cyclic, this is the actual row as well as the global shadow. Therefore

    (r_-2,r_-1,r_0)(q)=011,

so the fork bit in `problem1_forced_birth_sensitive_route_previous_source_dichotomy.md` is always `a=r_-1(q)=1`. The alternative `001` reconnection to the previous cyclic center cannot occur in this distinguished passage.

Thus every forced birth at `t+6` from such a two-bit source traces backward to the unique `011` sensitive-one obstruction at `q=t+2`.

Full note: `proofs/informal/problem1_run150_distinguished_source_forces_011_provenance_obstruction.md`.

## Why this matters

The earlier provenance route had two alternatives: `001` could recycle the previous cyclic center indefinitely, while `011` terminated at a creation obstruction. The first escape is now gone for the actual distinguished two-bit passage. A future budget argument only has to understand repeated distinguished `011` events.

## Next target

Do not return to finite FULL-prefix driver compression; runs147-148 prove that route cannot work. Do not identify the resetting source at `t+6` with a cyclic-source birth law; run149 records the domain mismatch.

Instead compare successive forced `011` events geometrically. Each comes with the larger fixed source block `1011` on positions `-3..0` at its cyclic return. Test whether successive event coordinates align along one Rule-30 characteristic/staircase so that the flip/provenance identities telescope against finite-support boundaries. If they do not align, determine whether the required ancestor coordinate moves outward at the generic light-cone rate and record that obstruction precisely.
