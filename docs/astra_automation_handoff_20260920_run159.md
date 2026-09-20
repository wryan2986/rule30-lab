# Astra automation handoff — run 159

Problem 1 remains OPEN.

## New result

The two g_(t+5)=2 itineraries surviving run157 are now identified exactly with the complete original-shadow front at the distinguished cyclic source q=t+2.

Using J(u)=min{j:s_j>u} and m(u)=J(u)-u:

- (d_2,d_3,d_4,d_5)=(1,0,0,4) gives J(q)=q+1, hence m(q)=1. Since actual r_1(q)=1, this forces hat r_1(q)=0.
- (0,1,0,4) gives J(q)=q+2, hence m(q)=2. Actual/shadow agree at position 1 and disagree at position 2. Since actual (r_1,r_2)(q)=(1,0), this forces (hat r_1,hat r_2)(q)=(1,1).

So the remaining distinction discarded by the cyclic-core quotient is exactly:

    A <=> hat r_1(q)=0,
    B <=> (hat r_1,hat r_2)(q)=11,

inside the established g=2 distinguished-source branch.

## Next target

Search established global-shadow/source identities for a constraint on hat r_1(q) or (hat r_1,hat r_2)(q). If none exists, perform a complete-shadow finite-support witness search conditioned on the distinguished source and g=2. Do not return to core-only or residence-only comparison; run158 and run159 isolate why those cannot distinguish the survivors.

Main note: `proofs/informal/problem1_run159_g2_itineraries_equal_exact_shadow_front_patterns.md`.
