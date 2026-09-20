# g=2 residence trace collapses to the single driver condition a=1

Status: `partial-proof` / stopping fence. Problem 1 remains open.

## Setup

Use the established TWO-BIT nonreset passage at time `t`, put `q=t+2`, and use the distinguished cyclic-source motif

    (r_-5,...,r_2)(q)=10101110.

Write

    a=r_3(q), b=r_4(q).

Run154 proved `g=g_(t+5)<=2`. For `g=2`, the exact global-front residence trace for characteristic `j=t+6` is

    r_2(q+1)=0,
    r_1(q+2)=0,
    r_0(q+3)=0,

followed by the final eraser

    r_-1(q+4)=1.                                  (1)

The question is whether the last two conditions in (1), or the full four-condition trace, impose any additional restriction beyond the first condition `a=1` found in run154.

## Exact Rule30 evaluation

From the rigid motif and Rule30 `F(l,c,r)=l XOR (c OR r)`, direct evolution gives

    r_2(q+1)=NOT a,
    r_1(q+2)=NOT a,
    r_0(q+3)=0,
    r_-1(q+4)=1.                                  (2)

The last two identities are unconditional: they do not depend on `a`, `b`, or any farther-right driver bit. The first two are identical and depend only on `a`.

Hence the complete residence trace required by `g=2` is equivalent, at the level of the distinguished source and its local forward cone, to the single condition

    a=1.                                           (3)

In particular `b` and the farther right fringe are completely invisible to this residence certificate.

This can also be checked by the four assignments `(a,b)=00,01,10,11`: the four cells in (1) are respectively

    a=0: (1,1,0,1),
    a=1: (0,0,0,1),

independently of `b`.

## Consequences for all remaining slack values

The same calculation classifies what the residence trace can see after run154:

- `g=0` requires only `r_0(q+3)=0` and the eraser `r_-1(q+4)=1`; both are automatic.
- `g=1` additionally requires `r_1(q+2)=0`, hence forces `a=1`.
- `g=2` additionally requires `r_2(q+1)=0`, but this is the same condition `a=1` and supplies no further information.

Therefore the exact local residence geometry distinguishes zero slack from positive slack only in the one-way sense

    g>=1  ==>  a=1,                               (4)

and it cannot distinguish `g=1` from `g=2` at all.

Importantly, (4) is not claimed as an equivalence: `a=1` does not determine the original-cut delay jump, because that jump depends on the complete original-shadow discrepancy tail.

## Stopping fence

Run154 excluded `g=3` because its residence reaches one step farther back to `(3,q)`, producing incompatible requirements `a=0` and `a=1`. This note shows that the analogous strategy is exhausted for `g<=2`: every cell of the `g=2` residence trace is already compatible with the distinguished motif once `a=1`, and no additional local cell in that residence remains to exploit.

Thus excluding `g=2` cannot come from extending the same residence-zero calculation. It requires information not contained in this local trace, for example an independent cyclic/gate/global-shadow restriction that forbids `a=1` in the `g=2` original-cut state, or a genuinely global relation tying the cut jump to the discrepancy tail.

Dependencies: `problem1_run154_distinguished_source_excludes_maximal_hidden_slack.md`; `problem1_global_discrepancy_front.md`; `problem1_full_trace_couples_distinguished_right_pair_to_far_left_bits.md`.
