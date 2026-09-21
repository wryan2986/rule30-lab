# Run 181: beta=1 forces the original-cut front to position 1 at t+7

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue the sufficiently late one-bit gate-u nonresetting passage in the `beta=1` branch. Run 180 proved, for the SAME original global E shadow, that at physical row `t+6`

    actual (r_1,r_2) = (0,1),
    shadow (h_1,h_2) = (1,1).

The exact six-step itinerary gives

    s_(t+5)=t+5,
    s_(t+6)=t+7.

Hence the characteristic-front residence formula implies

    J(t+6)=t+6,
    m(t+6)=0.

Thus position 0 is the leftmost discrepancy at `t+6`; in particular

    d_0(t+6)=1.

This point is important: run 180's right-pair discrepancy at position 1 is not the leftmost discrepancy in the beta=1 terminal row.

## Position 0 heals at t+7

The residence of characteristic `t+6` is

    [s_(t+5),s_(t+6)) = [t+5,t+7),

so `t+6` is its final physical row. The exact global-front eraser identity says that on the final row of a residence, the shared cell immediately to the LEFT of the front is 1. Since the front is at physical position 0 at `t+6`,

    r_(-1)(t+6)=h_(-1)(t+6)=1.

The exact discrepancy transport at the next cell therefore gives

    d_0(t+7)=1 XOR r_(-1)(t+6)=0.

So the old position-0 front bit is erased at the next step, as required by the residence theorem.

## Position 1 remains discrepant

At `t+6`, run 180 gives actual/shadow right pairs `01` and `11`. Write the complementary center cells as

    r_0(t+6)=x,
    h_0(t+6)=1 XOR x,

because `d_0(t+6)=1`.

Rule 30 at position 1 gives

    r_1(t+7) = x XOR (0 OR 1) = 1 XOR x,
    h_1(t+7) = (1 XOR x) XOR (1 OR 1) = x.

Therefore

    d_1(t+7)=1

independently of `x` and of every wider-right cell.

Together with `d_0(t+7)=0`, and with all negative positions agreeing because the reset step cannot move the leftmost discrepancy left of the erased front, this proves

    m(t+7)=1,
    J(t+7)=t+8.

Equivalently, characteristic `t+7` is skipped completely. Indeed monotonicity gives `s_(t+7)>=s_(t+6)=t+7`, while `J(t+7)=t+8` gives `s_(t+7)<=t+7`; hence

    s_(t+7)=t+7.

So the beta=1 terminal residence has the exact continuation

    J(t+6)=t+6  ->  J(t+7)=t+8,

with the front jumping from physical position 0 to physical position 1 after the final erasure.

## Extra rigid local data at t+7

The second right cell also becomes independent of all wider data:

    r_2(t+7)=0 XOR (1 OR r_3(t+6))=0,
    h_2(t+7)=1 XOR (1 OR h_3(t+6))=0.

Thus at `t+7`

    actual (r_1,r_2) = (1 XOR x,0),
    shadow (h_1,h_2) = (x,0).

The two right-pair zero flags are opposite, but which row has the zero pair depends only on the still-undetermined actual center bit `x=r_0(t+6)`.

## Consequence / next target

The first post-terminal row is now exact at the global-front level: `m(t+7)=1`, `J(t+7)=t+8`, and characteristic `t+7` is skipped. This strengthens the previous spacing statement without applying the cyclic-source birth law at the noncyclic resetting endpoint.

The next unresolved datum is the center bit `x=r_0(t+6)` (equivalently which of the actual/shadow right pairs at `t+7` is `00`). Determine whether the complete resetting-core classification fixes `x`. If it does, the `t+7 -> t+8` gate transition may be classifiable without importing arbitrary wider shadow cells. If it does not, the exact obstruction is now a single center-bit branch rather than an unspecified right-tail driver.

Dependencies: `problem1_run180_terminal_shadow_pair_is_rigid.md`; `problem1_global_discrepancy_front.md`; exact itinerary from runs 175-176.