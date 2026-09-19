# Distinguished `011` events do not give a finite label through the unconditional left-sensitive route

Status: `stopping-fence` / structural refinement. Problem 1 remains OPEN.

## Setup

Run133 showed that at every relevant preceding cyclic `t` source `q=t+2`, the sensitive-one route from the later forced birth reaches the exact neighborhood

    (r_-2(q), r_-1(q), r_0(q)) = 011.

The hope is that this distinguished source-relative family of `011` events, unlike generic `011` events, might carry an ordered label that can be charged to finite initial support.

## Exact left-sensitive continuation

Rule 30 is left-permutive:

    f(l,c,r) = l XOR (c OR r),

so the left input is Boolean-sensitive for every neighborhood. The output `r_-1(q+1)=1` of the distinguished `011` therefore has an unconditional sensitive predecessor `r_-2(q)=0`.

Continuing backward always through the unconditional left-sensitive edge moves one cell left per unit time. Thus the time-zero endpoint of this canonical continuation is

    (-2) - q = -q-2.

Equivalently, the distinguished event at source time `q` has canonical left-sensitive time-zero label

    lambda(q) = -q-2.

For successive source times `q_1 < q_2`,

    lambda(q_2) < lambda(q_1).

So these labels are indeed strictly ordered and never reused.

## Why this does not yield the finite birth budget

For a finite-support initial row with support contained in `[L,R]`, every sufficiently late source satisfies

    lambda(q) = -q-2 < L.

Hence its canonical endpoint is an initial **zero-tail** site, not one of the finitely many actual support sites. There are infinitely many such zero sites. Strict ordering of `lambda(q)` therefore supplies no finite upper bound on the number of distinguished `011` events.

This is a source-specific strengthening of the earlier general observation that the unconditional left-sensitive characteristic eventually escapes finite support. The new point is that even after run133 collapses the provenance fork to the distinguished `011` family, the most obvious ordered label is explicitly `-q-2`: it is injective but ranges through the infinite zero tail.

## Consequence

Do not count distinguished `011` events by their unconditional left-sensitive time-zero intercept. Any useful finite-resource theorem must either:

1. route state-dependently back to one of the finitely many initial **1** sites despite the `011` obstruction; or
2. attach a bounded object to the distinguished `011` event that is not merely a spacetime/zero-tail coordinate.

The remaining bottleneck is still a finite-support upper bound on the cyclic births forced by FULL.

Dependencies: `problem1_full_center_drop_forces_011_at_cyclic_t_source.md`, `problem1_left_sensitive_routed_provenance_escapes_support.md`, `problem1_sensitive_one_provenance_breaks_exactly_at_011.md`.
