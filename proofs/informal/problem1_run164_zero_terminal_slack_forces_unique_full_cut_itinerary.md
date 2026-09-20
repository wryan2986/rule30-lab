# Vanishing terminal slack forces the complete original-cut itinerary

Status: `partial-proof` / structural strengthening. Problem 1 remains OPEN.

## Setup

Continue the sufficiently late TWO-BIT nonresetting passage and put `q=t+2`. Run163 proves the terminal hidden slack vanishes:

    g_(t+5)=0,

and run153 gives

    d_2+d_3+d_4+d_5=5,
    g_(t+5)=3-(d_2+d_3+d_4),
    d_5=g_(t+5)+2,

where

    d_k=s_(t+k+1)-s_(t+k),  k=2,3,4,5.

Therefore

    d_2+d_3+d_4=3,   d_5=2.                       (1)

At the threshold row q, `s_q=q`. The established TWO-BIT return has the same actual and original-global-shadow pair

    (r_1,r_2)(q)=(1,0),
    (hat r_1,hat r_2)(q)=(1,0).                    (2)

The global-front identity is

    J(u)=min{j:s_j>u},
    m(u)=J(u)-u,

with `m(u)` the physical position of the leftmost actual-vs-original-shadow discrepancy.

## The first two cut increments vanish

If `d_2>0`, then `s_(q+1)>q`, so `J(q)=q+1` and `m(q)=1`. That would require a discrepancy at physical position 1, contradicting (2). Hence

    d_2=0.                                          (3)

With `d_2=0`, if `d_3>0`, then `s_(q+1)=q` but `s_(q+2)>q`, so `J(q)=q+2` and `m(q)=2`. That would require a discrepancy at physical position 2, again contradicting (2). Hence

    d_3=0.                                          (4)

Combining (1), (3), and (4) gives the UNIQUE complete itinerary

    boxed: (d_2,d_3,d_4,d_5)=(0,0,3,2).            (5)

Thus run163's terminal jump-2 theorem rigidifies not only the last increment but every original-cut increment across the zero-delay plateau and forced birth.

## Exact hidden-slack profile

Since `s_q=q`, itinerary (5) gives

    s_(q+1)=q,
    s_(q+2)=q,
    s_(q+3)=q+3,
    s_(q+4)=q+5.

Recalling `e_j=s_j-j`, the original-cut excesses from `t` through `t+6` are therefore

    boxed: (e_t,...,e_(t+6))=(2,1,0,-1,-2,0,1).    (6)

After truncation, this is exactly the known physical-delay profile

    (2,1,0,0,0,0,1).

So the phrase "zero terminal slack" must not be strengthened to "no hidden slack on the plateau": the interior slack is in fact forced and exact. It grows to depth 2 at `t+4`, then is repaid by the three-step original-cut jump `d_4=3`, one step BEFORE the forced birth's terminal jump `d_5=2`.

Equivalently, the residence itinerary from q is

    boxed: (0,0,3,2),

so characteristics `q+1` and `q+2` are skipped, characteristic `q+3` has residence length 3, and characteristic `q+4` has residence length 2.

## Consequence for the birth/renewal route

This sharpens the existing nonreset-return birth accounting but does not itself improve the previously proved >=8 spacing between sufficiently late nonresetting sources. The forced birth at `t+6` is still a resetting one-bit t source, and the older exclusion of N sources through `t+7` remains the operative spacing argument.

What is new is an exact original-cut charge pattern attached to every sufficiently late TWO-BIT nonresetting passage:

    two skipped characteristics, then charges/residences 3 and 2,

with exact excess profile (6). Any future global birth-budget or renewal argument can now count this fixed cut geometry rather than an unknown plateau slack. In particular, a putative budget that charges only the terminal birth jump misses the forced interior debt `e_(t+4)=-2` and its preceding repayment at `d_4=3`.

No finite global birth budget or contradiction with FULL is claimed here.

Dependencies: `problem1_run163_local_two_step_collision_excludes_final_hidden_slack.md`; `problem1_run153_zero_plateau_slack_exact_repayment.md`; `problem1_run161_g1_forces_unique_front_itinerary_and_shadow_bit.md`; `problem1_nonreset_return_birth_spacing.md`; `problem1_global_discrepancy_front.md`.
