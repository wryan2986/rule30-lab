# Automation handoff — run161 — 2026-09-20

Problem 1 remains OPEN. Continue on `research/astra-next`.

## New result

The only remaining positive terminal hidden slack, `g_(t+5)=1`, now has a UNIQUE global-front itinerary and exact original-shadow signature.

Put `q=t+2`. Run153 gives, for g=1,

    d_2+d_3+d_4=2,  d_5=3.

The SAME original global E-shadow used in run160 satisfies at q

    (hat r_1,hat r_2)=(1,0),

while the distinguished actual source also has

    (r_1,r_2)=(1,0).

If d_2>0, the global-front identity would put the first discrepancy at position 1, contradiction. Hence d_2=0. If d_3>0, it would put the first discrepancy at position 2, contradiction. Hence d_3=0. Therefore

    (d_2,d_3,d_4,d_5)=(0,0,2,3).

Consequently `J(q)=q+3` and the first actual-vs-original-shadow discrepancy is exactly at position 3. Run155 already proves g>=1 forces actual `r_3(q)=1`, so necessarily

    (hat r_1,hat r_2,hat r_3)(q)=(1,0,0),
    (r_1,r_2,r_3)(q)=(1,0,1),
    m(q)=3.

Full proof: `proofs/informal/problem1_run161_g1_forces_unique_front_itinerary_and_shadow_bit.md`.

## Next target

There is no longer any scalar/front-itinerary ambiguity in the positive-slack branch. Exclude or realize exactly ONE configuration: itinerary `(0,0,2,3)` with first original-shadow discrepancy at position 3 on the distinguished q source.

First transport `hat r_3(q)` explicitly from the source-t global-shadow driver and combine the required value `hat r_3(q)=0` with the complete source/gate identities. If that remains algebraically compatible, stop local itinerary enumeration and seek a genuine finite-support/global-E-shadow witness or a wider all-depth invariant.

Do not redo g=2 or enumerate the five raw g=1 scalar triples; four are now excluded by the known shadow pair.
