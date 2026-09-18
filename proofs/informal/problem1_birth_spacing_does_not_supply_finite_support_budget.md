# Birth spacing does not supply a finite-support budget

Status: `partial-proof` / stopping fence. Problem 1 remains OPEN.

## Setup

The established late `K=3` analysis gives two facts that are tempting to combine:

1. every sufficiently late nonresetting source is separated from the next nonresetting source by at least eight physical times;
2. in the two-bit nonresetting case, the return itself forces a new lag-one even row four steps after the cyclic repair endpoint.

The missing theorem in `ASTRA_HANDOFF.md` is a finite-support upper bound on the number of nonnegative cyclic births / regenerations for one actual finite survivor with its COMPLETE original fringe.

## Proposition: spacing alone cannot produce that upper bound

Let `B` be any infinite set of sufficiently late birth/source times satisfying a fixed separation condition

    |s-t| >= 8  for distinct s,t in B.

Then `B` can still be infinite; for example `{T+8j : j>=0}`. More generally, any lower bound on temporal spacing gives only

    # (B intersect [T,N]) <= 1 + floor((N-T)/8),

which diverges with `N`.

Finite initial spatial support does not change this conclusion without an additional injective or monotone charging theorem. Rule 30 has radius one, so the physical descendant cone of a finite initial support has width growing linearly in time. A later event's backward light cone can intersect the same original support cells as arbitrarily many earlier events. Locality therefore supplies no injection from distinct late births to distinct initial cells.

## Forced regeneration makes a naive current-population budget especially unsuitable

The nonreset-return theorem is stronger than mere permission: for the two-bit `t` source the next cyclic `u` source has `beta=1`, creating a new lag-one even row at `t+6`. Thus a budget defined only as "number of currently present lag rows", "number of current defects", or another renewable local population is not automatically decreasing across a repair passage. The passage can consume/repair one discrepancy and then regenerate another.

Consequently a valid finite-support budget must distinguish *uses* of the original finite fringe, not merely count current local objects. To imply finiteness it needs at least one of the following genuinely new properties:

- an injective charge from each relevant birth to a previously unused element of a finite original-fringe set;
- a well-founded original-fringe potential that strictly decreases at each regenerative cycle and cannot be replenished;
- an anchored incompatibility showing that the same original-fringe phase cannot support two sufficiently separated regenerative passages.

The existing spacing theorem proves none of these.

## Why this matters for the next step

This closes a misleading route: combining `>=8` spacing with finite initial support is not itself a birth budget. Any proposed budget should now be checked explicitly for **non-reuse under the forced beta=1 regeneration**. If the same original support/fringe datum can be charged twice, the argument has not crossed the all-depth gap.

A productive next target is therefore an original-fringe *non-reuse lemma*: identify a concrete finite datum carried from the COMPLETE initial fringe and prove that a two-bit nonresetting return changes/consumes that datum in a way that prevents the same charge from being used at a later nonresetting return.

Dependencies: `problem1_nonreset_return_birth_spacing.md`; `ASTRA_HANDOFF.md`.
