# Astra automation handoff — run 55

Problem 1 remains open.

## Repository state

Run began at `e8331cf6f6529c70f2bf712c53dbcfdb3f4ee7b9`; no intervening work was present after run 54.

## New result

Derived exact adjacent-time-pair dynamics for the temporal-column reconstruction. Writing a length-`2p` column as even/odd length-`p` words `(r_i,s_i)`, with `d_i=r_i xor s_i`, gives an exact period-halved system on `(r_i,d_i)`. The pair derivative `d` alone is not closed: its evolution contains the auxiliary even-sample word `r`.

This gives a precise obstruction to the run-54 period-halving idea. Bare `Delta_2` is not a semiconjugacy to the ordinary length-`p` reconstruction; an explicit local state disproves the same-rule identity. The weaker claim restricted to terminating doubling-parent trajectories remains possible.

## Research file

`proofs/informal/problem1_pair_derivative_exact_dynamics.md`

Research commit: `801730b46dc032000d334dfc86027cb17d7bbe53`

## Next target

Search the special terminating basin for an invariant relation eliminating the auxiliary `r`, or a corrected derivative `e=d xor Phi(r,...)` that obeys the ordinary length-`p` reconstruction. Computationally, work directly in the exact halved `(r,d)` coordinates and inspect terminating trajectories for low-complexity relations; do not retry a global bare-Delta semiconjugacy.
