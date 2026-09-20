# Terminal hidden slack g=1 forces a unique front itinerary and exact third shadow bit

Status: `partial-proof` / structural advance. Problem 1 remains OPEN.

## Setup

Continue the sufficiently late TWO-BIT nonresetting source `t` in the eventual K=3 branch and put `q=t+2`. Let

    d_k = s_(t+k+1)-s_(t+k),  k=2,3,4,5,

be the original-cut residence increments across the zero plateau and forced birth. Run153 proves

    d_2+d_3+d_4+d_5=5,
    g_(t+5)=3-(d_2+d_3+d_4),
    d_5=g_(t+5)+2.

Run160 excludes g=2 and run154 excludes g=3, leaving only g in {0,1}. This note classifies the remaining positive case g=1.

## Scalar possibilities for g=1

If `g=1`, then

    d_2+d_3+d_4=2,   d_5=3.                         (1)

The zero-plateau inequalities give `d_2<=1` and `d_2+d_3<=2`, so scalar bookkeeping alone leaves five triples:

    (d_2,d_3,d_4) in
      {(1,1,0),(1,0,1),(0,2,0),(0,1,1),(0,0,2)}.

We now use the SAME original global E-shadow as in run160.

## The known shadow pair eliminates every itinerary except (0,0,2)

At the threshold row q, run152 gives

    s_q=q.

The global-front identity is

    J(u)=min{j:s_j>u},
    m(u)=J(u)-u,

where `m(u)` is the physical position of the leftmost actual-vs-original-shadow discrepancy.

The older all-depth nonreset-return theorem, equation (3), gives for this TWO-BIT source

    (hat r_1(q),hat r_2(q))=(1,0).                  (2)

The distinguished actual source has

    (r_1(q),r_2(q))=(1,0).                          (3)

Thus actual and shadow agree at positions 1 and 2.

If `d_2>0`, then `s_(q+1)>q`, so `J(q)=q+1` and `m(q)=1`. That would force a discrepancy at position 1, contradicting (2)-(3). Hence

    d_2=0.                                          (4)

With `d_2=0`, if `d_3>0`, then `s_(q+1)=q` but `s_(q+2)>q`, so `J(q)=q+2` and `m(q)=2`. That would force a discrepancy at position 2, again contradicting (2)-(3). Hence

    d_3=0.                                          (5)

Combining (1), (4), and (5) gives the UNIQUE g=1 itinerary

    boxed: (d_2,d_3,d_4,d_5)=(0,0,2,3).            (6)

This eliminates four of the five scalar possibilities without any new finite-cone assumption.

## Exact third shadow bit

Under (6),

    s_(q+1)=q,
    s_(q+2)=q,
    s_(q+3)=q+2>q.

Therefore

    J(q)=q+3,   m(q)=3.                             (7)

So actual and original shadow agree through position 2 and first differ exactly at position 3.

Run155's complete residence classification proves that every positive terminal slack (`g>=1`) requires the distinguished actual driver bit

    r_3(q)=1.                                       (8)

Equations (7)-(8) therefore force

    boxed: hat r_3(q)=0.                            (9)

Hence the entire remaining positive-hidden-slack branch has now been reduced to the exact global-shadow/front signature

    boxed:
      (d_2,d_3,d_4,d_5)=(0,0,2,3),
      (hat r_1,hat r_2,hat r_3)(q)=(1,0,0),
      (r_1,r_2,r_3)(q)=(1,0,1),
      m(q)=3.

## What this does and does not prove

This does not yet exclude `g=1`: the older return theorem fixes the shadow only through position 2, and `hat r_3(q)=0` is not visibly contradictory to its wider free driver.

It does, however, remove all itinerary ambiguity. Any future exclusion of positive hidden slack need only rule out ONE all-depth configuration: a first original-shadow discrepancy at position 3 on the distinguished q source, equivalently the shadow prefix `100` against actual prefix `101`, together with the residence itinerary `(0,0,2,3)`.

A useful next check is to transport `hat r_3(q)` explicitly from the source-t shadow driver and combine `hat r_3(q)=0` with the complete source/gate/global-shadow identities. If that condition remains realizable, seek a finite-support/global-E-shadow witness rather than enumerating more scalar itineraries.

Dependencies: `problem1_run160_global_shadow_excludes_g2.md`; `problem1_run155_g2_residence_trace_collapses_to_single_driver_bit.md`; `problem1_run153_zero_plateau_slack_exact_repayment.md`; `problem1_run152_hidden_slack_boundary_pinning.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_global_discrepancy_front.md`.
