# Astra automation handoff — run 166 — 2026-09-20

Problem 1 remains OPEN. Run165 excluded sufficiently late TWO-BIT nonresetting sources. This run audited the proposed transfer of the global-front collision to the surviving ONE-BIT gate-u nonresetting source and found a precise stopping fence.

## New reduction / blocker

For a one-bit gate-u nonresetting source at even time `t`, the established source theorem gives `x=Y_t`, `z=cyc(x)`, `x=z XOR 1`, and the exact full-cut identity

    A x = A z.

The selected original global-shadow pair is `(hat r_1,hat r_2)=(1,1)`, matching the actual right source cells; the source discrepancy is at the center and the complete right cut heals after one A step.

Crucially, the known source delay `tau(Y_t)=1` is a CYCLICIZATION delay, not an original-cut characteristic residence time. Existing one-bit classification does not determine `J(t+1)` or `m(t+1)=J(t+1)-(t+1)` after the healing step. Therefore run165's method cannot be transferred by treating `tau=1` as a one-step global-front residence.

After `A x=A z`, further local A-evolution of this pair remains equal forever and contains no information about where the next discrepancy from the ORIGINAL finite-support ancestry enters. The missing datum is the next characteristic stopping time `s_j` exceeding the physical time.

See `proofs/informal/problem1_run166_one_bit_nonresetting_front_stopping_fence.md`.

## Next target

Search the existing original-cut / finite-entry / stopping-time lemmas for a bridge that fixes or bounds `J(t+1)` at a late one-bit gate-u nonresetting source. The useful result would be a short original-cut residence itinerary analogous to the two-bit `(0,0,3,2)` itinerary. Do NOT infer it from `tau=1`, and do NOT spend time extending the healed local `(x,z)` pair: that simulation is tautological after the first step.
