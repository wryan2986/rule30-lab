# Astra automation handoff — 2026-09-20 run157

Problem 1 remains OPEN.

## Repository state

Run began at `b922fa94c3842a8a8c93662b7727cc13c4c4da73` (run156); no intervening research commits were present.

## New result

Run156 reduced `g_(t+5)=2` to three possible residence itineraries

    (d_2,d_3,d_4) in {(1,0,0),(0,1,0),(0,0,1)},

followed by `d_5=4`, where `q=t+2` and `s_(t+2)=q`.

A one-step residence of characteristic `j` beginning at time `u` has only its final erasing cell, so the global-front residence certificate requires

    r_(j-u-1)(u)=1.

All three possible one-step visits begin at `u=q`. Therefore the three itineraries respectively require

    r_0(q)=1,
    r_1(q)=1,
    r_2(q)=1.

But the exact distinguished cyclic source is

    (r_-5,...,r_2)(q)=10101110,

so `(r_0,r_1,r_2)(q)=(1,1,0)`. Hence the third itinerary `(0,0,1)` is impossible.

Thus under `g=2` only

    (d_2,d_3,d_4) in {(1,0,0),(0,1,0)}.

New proof: `proofs/informal/problem1_run157_g2_third_itinerary_excluded_by_source_bit.md`.

## Next target

Case-split the two survivors using cyclic gate/core information at `q=t+2` and the next cyclic row `q+2=t+4`. The residence test at time q is exhausted for these cases: it merely asks for `r_0(q)=1` or `r_1(q)=1`, both already fixed by the distinguished source.

Do NOT use `skip => clock doubling`; only the converse direction has been established. Seek an independent gate/core constraint that distinguishes whether the unique one-step visit is characteristic `t+3` or `t+4`, or construct a fully admissible witness for one/both cases.
