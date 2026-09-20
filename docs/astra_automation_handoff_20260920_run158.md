# Astra automation handoff — run 158 — 2026-09-20

Problem 1 remains OPEN.

## New result

The two `g_{t+5}=2` itineraries surviving run157,

    (d_2,d_3,d_4,d_5)=(1,0,0,4)
    (d_2,d_3,d_4,d_5)=(0,1,0,4),

cannot be distinguished by the proposed cyclic gate/core test from `q=t+2` to `q+2=t+4`.

The existing all-depth nonreset-return theorem already fixes the complete transition on both alternatives:

    gate(q)=t,
    gate(q+2)=u,
    Z_{q+2}=G(Z_t)=16 A^4 Z_t+7,

with complete code `I_3 I_1 shift^4 Theta(Z_t)`. These identities were derived independently of the original-cut residence itinerary. Thus any test using only the complete cyclic cores/codes or these gate symbols is provably blind to which survivor occurs unless a new theorem first couples the core to the global discrepancy-front residence.

At the local level the alternatives require respectively `r_0(q)=1` or `r_1(q)=1`, and the distinguished source `10101110` forces both. The common terminal four-step residence is also already compatible when `r_3(q)=1`.

Full note: `proofs/informal/problem1_run158_surviving_g2_itineraries_are_core_indistinguishable.md`.

## Next target

Do not repeat the core-only comparison. Attack the missing bridge directly: characterize `d_2=1` versus `d_3=1` from the complete global E-shadow/discrepancy tail at `q`, or construct a fully admissible finite-support witness for one survivor. The unresolved bit is global original-cut/front information that the cyclic core quotient has discarded.
