# Run 185: any beta=1 nonreset candidate at t+8 has exact delay 1 or 2

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Continue the sufficiently late one-bit gate-u nonresetting source at even physical time `t` in the terminal branch `beta=1`.

Run 181 established, with `x=r_0(t+6)`, that at `t+7`

    actual (r_0,r_1,r_2) = (1 XOR x, 1 XOR x, 0),
    m(t+7)=1,
    J(t+7)=t+8,
    s_(t+7)=t+7.

Run 184 then proved

    m(t+8)=0,
    J(t+8)=t+8,
    s_(t+8)>=t+9,
    tau(Y_(t+8))>=1.

Thus `t+8` is the first time not already excluded by the eight-step nonresetting-source spacing theorem, and it is certainly a positive-delay row.

## Exact actual gate at t+8

Put

    y = 1 XOR x,
    p = r_3(t+7).

The known actual row at `t+7` has

    (r_0,r_1,r_2,r_3)=(y,y,0,p).

One Rule-30 step gives

    r_1(t+8)= y XOR (y OR 0)=0,

and

    r_2(t+8)= y XOR (0 OR p)=y XOR p.

Define the single complete-driver bit

    alpha := y XOR p.

Then the actual right pair at `t+8` is exactly

    (r_1,r_2)(t+8)=(0,alpha).

Therefore the actual gate-u indicator at `t+8` is exactly `alpha`: `alpha=0` is gate t and `alpha=1` is gate u.

No cyclicity or birth law is used here.

## Conditional classification if t+8 is nonresetting

The pushed nonresetting-core return theorem applies to every sufficiently late nonresetting source under the current eventual `K=3` bound. If its actual gate-u indicator is `u`, its source delay is

    d=2-u.

Consequently, if `N_(t+8)` holds, then `u=alpha` and

    tau(Y_(t+8)) = 2-alpha.

Thus the forced positive delay from run 184 is not merely bounded below: under the candidate nonresetting hypothesis it has one of exactly two values,

    alpha=1 (gate u): tau(Y_(t+8))=1,
    alpha=0 (gate t): tau(Y_(t+8))=2.

Since run 184 has `J(t+8)=t+8`, the threshold identity is on its positive branch, so

    s_(t+8)=t+8+tau(Y_(t+8))=t+10-alpha.

Using `s_(t+7)=t+7`, this is equivalently

    Delta_(t+7)=s_(t+8)-s_(t+7)=3-alpha.

Hence a hypothetical new nonresetting source at the first allowed time has the exact dichotomy

    alpha=1: one-bit gate-u source, Delta_(t+7)=2,
    alpha=0: two-bit gate-t source, Delta_(t+7)=3.

In particular, any observation or theorem forcing `Delta_(t+7)>=4` would immediately exclude `N_(t+8)`; conversely, determining `alpha` reduces the complete source type and exact residence endpoint to one bit.

## Fence and next target

This does not prove `N_(t+8)`, and it does not classify the resetting alternative. The new point is that the candidate nonresetting branch has no residual scalar-delay freedom: its gate, source width, delay, residence endpoint, and `Delta_(t+7)` are all controlled by the single actual cell `p=r_3(t+7)` relative to `x`.

The next useful target is to express `alpha=(1 XOR x) XOR r_3(t+7)` in terms of the complete resetting endpoint at `t+6`, or to show that the resetting-core condition at `t+8` is selected by the same bit. This is preferable to extending an unconstrained gate prefix.

Dependencies: `problem1_run181_beta_one_forces_tplus7_front.md`; `problem1_run184_beta_one_forces_tplus8_center_crossing.md`; `problem1_nonreset_return_birth_spacing.md`.
