# Astra automation handoff — run 163 — 2026-09-20

Problem 1 remains OPEN, but the hidden-slack branch for the sufficiently late TWO-BIT nonresetting passage is now CLOSED.

## New result

Run161 showed the last positive case `g_(t+5)=1` has unique residence itinerary

    (d_2,d_3,d_4,d_5)=(0,0,2,3)

and at `q=t+2` requires

    actual (r_1,r_2,r_3)=(1,0,1),
    original shadow (hat r_1,hat r_2,hat r_3)=(1,0,0),
    m(q)=3.

A direct two-step Rule-30 calculation now kills this case without any assumption on the wider driver. Since actual and shadow also share `r_0=hat r_0=1`, at `q+1`:

    actual (r_1,r_2)=(0,0),
    shadow (hat r_1,hat r_2)=(0,1),
    actual r_3(q+1)=1 regardless of r_4(q).

Therefore at `q+2`,

    r_2(q+2)=1,
    hat r_2(q+2)=1

regardless of the wider shadow driver. But itinerary `(0,0,2,3)` requires the next characteristic `q+4` to begin residence at `q+2`, so `m(q+2)=2` and position 2 must be the first actual/shadow discrepancy. Contradiction.

Hence

    g_(t+5) != 1.

Together with the earlier exclusions of `g=2,3`,

    g_(t+5)=0

exactly. By run153's repayment identity,

    s_(t+6)-s_(t+5)=2.

## What changed relative to run162

Do NOT pursue the proposed wider-driver witness search merely to decide `g=1`; it is no longer needed. The run162 driver condition `a*(b OR c)=0` is compatible locally, but the corresponding required global-front itinerary is not: the discrepancy at physical position 2 annihilates at `q+2` exactly when that itinerary requires a new front there.

## Next target

Propagate the exact zero-slack / terminal jump-2 theorem into the existing renewal/birth accounting. Check whether the now-rigid two-bit nonresetting passage yields a stronger spacing, charge, or cut-delay recurrence that can interact with FULL and finite original support. Avoid reopening local shadow-driver enumeration for this passage unless auditing run163.

See `proofs/informal/problem1_run163_local_two_step_collision_excludes_final_hidden_slack.md`.
