# g=2: the third global-front itinerary is impossible

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue the distinguished sufficiently-late TWO-BIT nonreset passage from runs 150--156. Put

    q=t+2.

At the cyclic source row q the established exact block is

    (r_-5,...,r_2)(q)=10101110,

so in particular

    r_0(q)=1,  r_1(q)=1,  r_2(q)=0.                 (1)

Run156 showed that if the terminal hidden slack is

    g_(t+5)=2,

then, writing

    d_k=s_(t+k+1)-s_(t+k),   k=2,3,4,5,

the first three residence lengths must be exactly one of

    (d_2,d_3,d_4)=(1,0,0),(0,1,0),(0,0,1),          (2)

and d_5=4.

The point of this note is that the last case in (2) is already incompatible with the distinguished source bit r_2(q)=0.

## One-step residence endpoint rule

For characteristic j, the global-front residence interval is

    [s_(j-1),s_j).

The shared left-neighbor cell along that characteristic at residence time u has source-relative coordinate

    j-u-1.

Every nonfinal residence cell is zero, while the final residence cell is the erasing 1. Thus if the residence has length one, so that

    s_j=s_(j-1)+1,

the unique residence cell is necessarily

    r_(j-s_(j-1)-1)(s_(j-1))=1.                    (3)

This is just the length-one specialization of the global discrepancy-front residence certificate used in runs154--155.

## Apply (3) to the three g=2 itineraries

Because s_(t+2)=q, the unique one-step visit in each case of (2) begins at time q; all preceding increments in that case are zero.

### Case A: (1,0,0)

Here characteristic j=t+3=q+1 has its one-step residence on [q,q+1). Equation (3) requires

    r_0(q)=1,

which agrees with (1). So this case survives this test.

### Case B: (0,1,0)

The first increment is zero, hence s_(t+3)=q. Characteristic j=t+4=q+2 then has its one-step residence on [q,q+1). Equation (3) requires

    r_1(q)=1,

again agreeing with (1). This case also survives this test.

### Case C: (0,0,1)

The first two increments are zero, so s_(t+4)=q. Characteristic j=t+5=q+3 has its one-step residence on [q,q+1). Equation (3) requires

    r_2(q)=1.                                       (4)

But the distinguished cyclic-source block fixes r_2(q)=0. Contradiction.

Therefore

    (d_2,d_3,d_4) != (0,0,1),

and under g_(t+5)=2 only

    (d_2,d_3,d_4) in {(1,0,0),(0,1,0)}.             (5)

Equivalently, if g=2 then the unique one-step visit among characteristics t+3,t+4,t+5 must occur on t+3 or t+4; characteristic t+5 cannot be the unique visited one.

## Interpretation / next target

Run156 reduced g=2 to three global-front histories. The exact distinguished source immediately removes one of them, without any converse assumption of the form `skip => clock doubling`.

The two survivors correspond exactly to the two adjacent source bits r_0(q)=r_1(q)=1. The next useful target is therefore to test the cyclic gate/core transition at q and q+2 against these two histories separately. Local residence geometry alone does not distinguish them at time q: their required erasing cells are already present in the rigid source block.

Do not infer a period doubling merely from either zero residence increment; only the established forward implication `clock doubling => skip` is available.

Dependencies: `problem1_run156_g2_forces_two_skips_then_four_step_residence.md`; `problem1_global_discrepancy_front.md`; `problem1_run150_distinguished_source_forces_011_provenance_obstruction.md`.
