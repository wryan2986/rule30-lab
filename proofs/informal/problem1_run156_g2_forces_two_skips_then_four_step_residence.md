# g=2 forces two skipped characteristics then a four-step residence

Status: `partial-proof` / structural reduction. Problem 1 remains open.

## Setup

Use the established TWO-BIT nonreset passage at time `t`. Put `q=t+2`. From run152/run153,

    s_(t+2)=t+2=q,
    s_(t+6)=t+7=q+5.

Write

    d_k=s_(t+k+1)-s_(t+k),  k=2,3,4,5.

These are nonnegative integers. By the global discrepancy-front residence theorem, `d_k` is exactly the residence length of characteristic `t+k+1`.

Run153 gives

    d_2+d_3+d_4+d_5=5,
    g_(t+5)=3-(d_2+d_3+d_4),
    d_5=g_(t+5)+2.

Run154/run155 reduce the unresolved terminal slack to `g in {0,1,2}` and show that `g=2` is locally compatible exactly when the distinguished driver bit `a=r_3(q)` equals 1.

## Exact global-front signature when g=2

Assume `g_(t+5)=2`. Then

    s_(t+5)=(t+5)-2=t+3=q+1.

Since `s_(t+2)=q`,

    d_2+d_3+d_4=s_(t+5)-s_(t+2)=1.              (1)

Each `d_k` is a nonnegative integer, so (1) implies that `(d_2,d_3,d_4)` is exactly one of

    (1,0,0), (0,1,0), (0,0,1).                    (2)

Thus among the three characteristics

    t+3, t+4, t+5,

exactly ONE is visited by the global discrepancy front, for exactly one physical time, and the other TWO are skipped completely.

The terminal increment is then

    d_5=g+2=4.                                      (3)

Hence characteristic `t+6` is visited for exactly four consecutive physical times. Its residence interval is

    [s_(t+5),s_(t+6))=[t+3,t+7)=[q+1,q+5).        (4)

This is precisely the four-cell residence certificate evaluated in run155.

Therefore `g=2` is equivalent, at the scalar/global-front level of this fixed passage, to the rigid residence-length pattern

    permutation of (1,0,0), followed by 4.          (5)

In words: **two skips and one one-step visit in the three characteristics after the pinned source, immediately followed by a four-step residence.**

## Consequence for the next proof target

Run155 showed that the four-step residence itself imposes only `a=1`; extending its local zero trace cannot exclude `g=2`. Equation (5) identifies the missing information more sharply: any contradiction must use the TWO skipped characteristics before that residence (or the location of the unique one-step visit), not more cells inside the terminal residence.

The global-front theorem also says every clock-doubling characteristic is skipped. Therefore a promising finite case split is now only the three possibilities in (2): compare the cyclic period/core transitions at `t+3,t+4,t+5` and ask whether two of these three characteristics can be skipped while retaining the distinguished `10101110` source, FULL phase, and the forced return at `t+6`. No converse `skip => clock doubling` is assumed here.

This does not yet exclude `g=2`; it converts an opaque original-cut slack value into an exact three-case global-front itinerary.

Dependencies: `problem1_run153_zero_plateau_slack_exact_repayment.md`; `problem1_run154_distinguished_source_excludes_maximal_hidden_slack.md`; `problem1_run155_g2_residence_trace_collapses_to_single_driver_bit.md`; `problem1_global_discrepancy_front.md`.
