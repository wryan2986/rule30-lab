# Astra automation handoff — run 164 — 2026-09-20

Problem 1 remains OPEN. Run163 closed the terminal hidden-slack ambiguity for the sufficiently late TWO-BIT nonresetting passage; this run propagates that result into the complete original-cut itinerary.

## New result

Put `q=t+2` and retain

    d_k=s_(t+k+1)-s_(t+k), k=2,3,4,5.

Run163 gives `g_(t+5)=0`; run153 then gives

    d_2+d_3+d_4=3,
    d_5=2.

At q, actual and the SAME original global E-shadow agree at positions 1 and 2:

    (r_1,r_2)=(hat r_1,hat r_2)=(1,0).

The global-front identity therefore excludes `d_2>0` (which would make position 1 the first discrepancy) and, after `d_2=0`, excludes `d_3>0` (which would make position 2 the first discrepancy). Hence

    boxed: (d_2,d_3,d_4,d_5)=(0,0,3,2).

This is the unique complete cut/residence itinerary across the zero-delay plateau and forced birth.

Since `s_q=q`, the exact original-cut excess profile is

    boxed: (e_t,...,e_(t+6))=(2,1,0,-1,-2,0,1).

Thus terminal slack vanishes but interior hidden slack does NOT: it is forced to depths 1 and 2 at t+3,t+4, then repaid by `d_4=3` before the forced birth's terminal `d_5=2` jump.

## Birth/renewal consequence

This does not by itself improve the established >=8 spacing between sufficiently late nonresetting sources. It does replace the formerly variable cut geometry by a fixed charge pattern: two skipped characteristics, then residences 3 and 2. Any global birth-budget/renewal argument should count this exact pattern and must not charge only the terminal birth jump, because the passage contains forced interior debt `e_(t+4)=-2` repaid one step earlier.

## Next target

Use the exact `(0,0,3,2)` residence pattern and excess profile `(2,1,0,-1,-2,0,1)` in the global-front/finite-support accounting. Seek a monotone or bounded quantity tied to original finite support that must pay for the forced depth-2 debt/three-step repayment on every late TWO-BIT nonresetting passage. Do not reopen terminal hidden-slack enumeration.

See `proofs/informal/problem1_run164_zero_terminal_slack_forces_unique_full_cut_itinerary.md`.
