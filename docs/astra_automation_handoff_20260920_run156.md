# Astra automation handoff — 2026-09-20 run156

Problem 1 remains OPEN.

## New result

Run155 left `g_(t+5)=2` locally compatible exactly through the driver condition `a=r_3(q)=1`, where `q=t+2`. Run156 converts `g=2` into an exact global-front itinerary.

From the pinned endpoint delays,

    s_(t+2)=t+2=q,
    s_(t+6)=t+7=q+5.

Let `d_k=s_(t+k+1)-s_(t+k)` for `k=2,3,4,5`; by the global-front theorem these are residence lengths of characteristics `t+k+1`.

If `g_(t+5)=2`, then `s_(t+5)=t+3=q+1`, hence

    d_2+d_3+d_4=1.

Therefore

    (d_2,d_3,d_4) in {(1,0,0),(0,1,0),(0,0,1)}.

Exactly one of characteristics `t+3,t+4,t+5` is visited, for one time step, and the other two are skipped completely. Run153 then gives

    d_5=g+2=4,

so characteristic `t+6` has the four-step residence `[t+3,t+7)=[q+1,q+5)` already evaluated in run155.

Thus `g=2` has the rigid global-front signature: a permutation of `(1,0,0)` followed by `4`.

## Stopping fence / next target

Do not extend the terminal four-step residence trace; run155 exhausted it. The missing information is now isolated to the TWO skipped characteristics immediately before that residence and the location of the unique one-step visit.

Next, case-split the three itineraries above using cyclic period/core/gate data at `t+3,t+4,t+5`. The global-front theorem proves `clock doubling => skip`, but NOT the converse, so do not silently identify every skip with a doubling. Determine whether two of these three characteristics can be skipped under the distinguished `10101110` source, FULL phase, and forced return at `t+6`.

New proof: `proofs/informal/problem1_run156_g2_forces_two_skips_then_four_step_residence.md`.
