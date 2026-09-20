# Astra automation handoff — run 165 — 2026-09-20

Problem 1 remains OPEN. Run 164 fixed the complete original-cut itinerary of any sufficiently late TWO-BIT nonresetting passage to `(0,0,3,2)`. This run shows that itinerary is locally unrealizable against the SAME original global E-shadow.

## New result

Put `q=t+2`. Run 164 plus `m(u)=J(u)-u` forces first actual/shadow discrepancy positions

    m(q),m(q+1),m(q+2),m(q+3) = 3,2,1,1.

The established distinguished actual source at q has

    (r_-5,...,r_2)(q)=10101110.

Since m(q)=3, actual and shadow agree through position 2 and differ at position 3. Write `r_3(q)=x`, `hat r_3(q)=1-x`. Three direct Rule-30 steps, using no wider-tail assumptions, give:

- at q+1 the first discrepancy is indeed at 2;
- at q+2 it is indeed at 1, with common position-0 value equal to 1;
- at q+3 the common position-0 value remains equal, and position 1 is forced equal as well, for both x=0 and x=1.

Thus m(q+3)=1 is impossible. Therefore

    boxed: no sufficiently late TWO-BIT nonresetting source can occur.

See `proofs/informal/problem1_run165_unique_cut_itinerary_collides_with_local_shadow_dynamics.md` for the exact cell calculation.

## Scope check against the older classification

`problem1_nonresetting_core_returns.md` Section 3 classifies two late even N-source profiles: one-bit gate-u and two-bit gate-t. Section 4 says every two-bit even source is the offset-4 row of a six-step repair, but this is only the direction TWO-BIT -> repair-offset-4. It does not state that every repair/nonresetting episode must contain a two-bit N source. Therefore run165 must NOT yet be promoted to exclusion of all late nonresetting sources or to a solution of Problem 1.

## Next target

Analyze the surviving ONE-BIT gate-u nonresetting source with the same original-cut/global-front method. Its source delay is 1 and its source/global-shadow profile is already fixed in `problem1_nonresetting_core_returns.md`. Derive its exact cut/excess itinerary through the cyclic return and subsequent birth flag, rather than reusing the two-bit itinerary. If the one-bit type also collides with local shadow dynamics, then revisit the switch/birth inequality (equation (4) of the older classification) to see whether all sufficiently late N sources are excluded. If the one-bit type survives, isolate its exact front pattern and use that as the new bottleneck.
