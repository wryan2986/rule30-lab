# Sensitive 1-provenance breaks exactly at `011`

Status: `structural-lemma + stopping-fence`. Problem 1 remains OPEN.

## Motivation

Run127 left state-dependent branching as a possible way to route a late forced birth back to the finite original actual support. A natural strengthening of ordinary ancestry is to require a backward path that (a) follows Boolean-sensitive inputs and (b) remains on cells whose value is `1`, hoping that every present `1` can be assigned to an original actual `1`.

For Rule 30

    f(l,c,r) = l XOR (c OR r)
             = l XOR c XOR r XOR c r,

its Boolean derivatives are

    D_l f = 1,
    D_c f = 1 XOR r,
    D_r f = 1 XOR c.

Thus the left input is always sensitive, the center input is sensitive exactly when `r=0`, and the right input is sensitive exactly when `c=0`.

## Exact classification for output 1

The four predecessor triples producing output `1` are

    001, 010, 011, 100.

Inspecting sensitive inputs gives:

- `001`: the right input is a sensitive `1`-parent.
- `010`: the center input is a sensitive `1`-parent.
- `100`: the left input is a sensitive `1`-parent.
- `011`: neither of its two `1` inputs is sensitive (`D_c f = D_r f = 0`); the only unconditionally sensitive input is the left `0`.

Therefore:

> Every Rule-30 output `1` has a sensitive predecessor of value `1` **except exactly when its predecessor neighborhood is `011`**.

Equivalently, a backward path constrained to sensitive `1` cells can be continued uniquely/nonuniquely through `001`, `010`, and `100`, but must terminate at a `1` born from `011`.

This is stronger than the earlier observation that there is no canonical positional 1-parent: allowing state-dependent choice repairs all output-1 neighborhoods except one exact nonlinear creation motif.

## Computational sanity check: `011` is not a scarce resource

A direct exact simulation from the single-seed initial row (one `1` at coordinate 0) counted the number of sites at each step whose predecessor neighborhood is exactly `011`. For times `0..199`, the cumulative count is **5321**. The first 20 per-step counts are

    0,1,1,2,1,3,1,3,2,4,3,4,4,7,3,5,4,7,6,6.

There are **3931** such events during times `100..199` alone, and the maximum single-step count in the first 200 steps is 57.

This computation is not an all-time theorem, but it decisively rejects treating `011` events themselves as an obviously finite or rapidly exhausted resource arising from finite initial support.

## Consequence for the birth-budget route

State-dependent sensitive-1 routing does not automatically produce a charge into the finite original support. A route from a forced birth either reaches time zero at an original `1`, or terminates earlier at an `011` creation event. To turn this into the needed finite birth budget one would still have to prove a special theorem for the *particular forced cyclic births* showing, for example, that their routes avoid `011`, or that any encountered `011` events admit a separate bounded-reuse charge to original support.

The generic dynamics give no such scarcity: even a one-cell initial support produces thousands of `011` creation events over a short finite horizon.

## Next target

Apply this exact routing classification to the already-proved two-bit nonreset `001` forcing passage. Trace the forced later `beta=1` cell backward using sensitive-1 routing and determine whether the local `001 -> ... -> birth` geometry forces the route to cross an `011` termination motif. If it avoids `011` for structural reasons, that would finally connect this special birth to an original actual `1`; if it necessarily hits `011`, identify the first such motif relative to the source and test whether *that special family* has an ordered/bounded-reuse law. Do not treat generic `011` events as a finite resource.
