# Problem 1: hidden zero-delay slack is exactly negative tail excess, and a bound on it alone is insufficient

## Purpose

`ASTRA_AUTOMATION_HANDOFF.md` identifies the hidden slack at a zero-delay physical row,

    g_j = j - s_j >= 0,

as the most direct next scalar object after the signed residence ledger was shown to telescope. This note relates that slack exactly to the already-defined zero-extension excess on the finite-support tail and records a limitation: a uniform bound on hidden slack, by itself, cannot contradict an eventual finite strip.

No new finite census is used.

## Exact tail identity

Fix a nonzero finite original row, let `R` be its right support endpoint, and put

    v = L_R(r) > 0,
    h_n = tau(2^n v),
    e_v(n) = h_n - n.

For the physical tail index `j=R+n`, the original-cut delay is

    s_(R+n) = h_n.

Hence whenever the physical delay is zero, equivalently `s_(R+n) <= R+n` or `e_v(n) <= R`, the hidden slack is exactly

    g_(R+n)
      = (R+n) - s_(R+n)
      = R+n-h_n
      = R-e_v(n).                                      (1)

Thus hidden slack is not an independent scalar degree of freedom on the finite-support tail. It is precisely the amount by which the excess lies below the clipping threshold `R`.

The global-front formula may therefore be written as the two-sided decomposition

    tau(Y_(R+n)) = max(e_v(n)-R,0),
    g_(R+n)      = max(R-e_v(n),0),                    (2)

with at most one of the two quantities positive. Equivalently,

    e_v(n)-R = tau(Y_(R+n)) - g_(R+n).                 (3)

Equation (3) restores exactly the signed information lost by the `max` in the physical strip variable.

## A hidden-slack bound alone does not close the gap

Suppose one proved that all sufficiently late zero-delay rows satisfy

    g_(R+n) <= G.

By (1), this says only

    e_v(n) >= R-G

on the clipped part of the orbit. Together with an eventual physical strip `tau(Y)<=K`, equation (2) gives the two-sided bound

    R-G <= e_v(n) <= R+K                              (4)

for all sufficiently late `n` (with the lower inequality automatic on positive-delay rows because there `e_v(n)>R`).

But (4) is perfectly compatible with every scalar fact currently available about the zero-extension tower. For example, the abstract residence sequence

    h_n = n + C

has `delta_n=1`, `e_v(n)=C`, and `h_n -> infinity`, while both the physical delay and hidden slack are uniformly bounded (one is identically zero depending on the position of `C` relative to `R`). More generally, any bounded integer excess sequence with increments `e(n+1)-e(n)>=-1` gives nonnegative residence increments `delta_n=1+e(n+1)-e(n)` and can satisfy `h_n -> infinity`.

This is a logical no-go for deduction from the scalar ledger identities alone; it is not claimed that every such abstract sequence is realized by Rule 30.

Therefore the proposed theorem "hidden slack is uniformly bounded" is not, by itself, enough to establish

    limsup e_v(n) = infinity.

A successful repayment theorem must force more than recovery from negative excess back into a bounded interval.

## What a sufficient repayment statement must do

Using (3), a useful all-depth statement must force an actual positive overshoot. For example, any one of the following would be sufficient on the FULL finite-fringe domain:

1. after a zero-delay row of slack `g`, some later row has `tau(Y) >= Phi(g)` with `Phi(g)` unbounded and enough recurrence to force arbitrarily large positive delay;
2. each excursion below the clipping threshold must later return above its previous positive-delay maximum by a definite amount;
3. a non-telescoping charge couples the recovery of `g` to a finite original-support resource, so infinitely many FULL episodes cannot remain inside one fixed interval `[R-G,R+K]`.

In particular, merely proving `g<=G`, or merely proving that later evolution repays `g` back to zero, leaves open the bounded-excess model `e_v(n)=O(1)` and therefore does not contradict the eventual strip.

## Strategic consequence

The hidden-slack route remains useful because (3) gives the exact unclipped signed coordinate. But the next theorem should be phrased as an **overshoot / bounded-reuse theorem**, not as a standalone upper bound on `g`.

This also aligns with the portal-tree no-go: both abstract portal counting and scalar clipping identities admit bounded-support-independent countermodels. The missing ingredient in either language must couple the actual FULL dynamics to the complete original finite fringe strongly enough to force an overshoot or consume a finite resource.

## Status

Problem 1 remains open. This note is a structural identity plus strategy fence; it prevents treating a hidden-slack bound alone as the missing contradiction.
