# Run 170: the one-bit nonresetting third residence is exactly one

Status: `partial-proof`. Problem 1 remains OPEN.

## Setup

Let `t` be a sufficiently late one-bit gate-u nonresetting source in the eventual `K=3` regime. Runs 167--169 established, using the original finite-support stopping times and the same global E-shadow,

    s_t = s_(t+1) = t+1,
    s_(t+2) = t+2,
    J(t+2) = t+3.

In particular the last identity says

    s_(t+3) > t+2.                                  (1)

Run 169 correctly stopped short of replacing (1) by equality.

## Imported all-depth delay information

The earlier nonreset-return theorem applies to this same one-bit source. With gate-u indicator `u=1`, its source delay is `d=2-u=1`, and its complete delay profile through the two cyclic returns is

    tau(Y_t),...,tau(Y_(t+6)) = 1,0,0,0,0,0,beta.   (2)

Thus in particular

    tau(Y_(t+3)) = 0.                                (3)

This is not a local cyclicization/residence identification: (3) is an independently established physical delay statement for the original actual orbit.

Use the already established original-cut threshold identity

    tau(Y_j) = max(s_j-j,0).                         (4)

Putting `j=t+3` into (3)--(4) gives

    s_(t+3) <= t+3.                                  (5)

Together, (1) and (5), and integrality of stopping times, force

    s_(t+3) = t+3.                                   (6)

Therefore

    Delta_(t+2) = s_(t+3)-s_(t+2) = 1.              (7)

So the one-bit gate-u original-cut itinerary begins exactly

    (Delta_t,Delta_(t+1),Delta_(t+2)) = (0,1,1).

Equivalently, after skipping characteristic `t+1`, the global discrepancy front visits characteristics `t+2` and `t+3` for exactly one physical step each.

## Why this closes the run-169 gap

Run 169 supplied the strict lower bound `s_(t+3)>t+2` from the global shadow front. The old nonreset-return delay theorem supplies the missing upper bound `s_(t+3)<=t+3`. Neither ingredient alone determines the residence.

## Next target

The same imported delay profile gives `tau(Y_(t+4))=0`, hence only

    t+3 = s_(t+3) <= s_(t+4) <= t+4.

Thus `Delta_(t+3)` is now binary: 0 or 1. Determine whether characteristic `t+4` is skipped by propagating the same original global shadow one more step, or derive a global-front constraint that distinguishes the two cases. Do not infer it merely from cyclicity.

Dependencies: `problem1_nonreset_return_birth_spacing.md`; runs 167--169; original-cut threshold identity `tau(Y_j)=max(s_j-j,0)`.
