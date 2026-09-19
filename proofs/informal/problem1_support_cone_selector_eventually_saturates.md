# Problem 1: support-cone selectors eventually saturate

## Status

Problem 1 remains open. This note closes one literal version of the run125 proposal: selecting an original-support label merely from membership in the backward light cone of a late bounded-location source/birth cannot yield the missing monotone finite budget.

## Setup

Let the actual time-zero Rule-30 row `x` have finite support

`S = {i : x_i(0)=1}`

contained in `[L,R]`. A spacetime cell `(j,t)` has radius-one backward light cone on time zero

`I(j,t) = [j-t, j+t]`.

More generally, any event whose determining cells at time `t` lie in a fixed bounded spatial window `J=[a,b]` has time-zero backward cone

`I(J,t) = [a-t, b+t]`.

The late source machinery used in the current Problem 1 argument is anchored to a fixed finite source-relative window (the two-bit nonreset forcing event, for example, is already known to collapse to a three-cell `001` motif). Thus this is the relevant geometric test for a selector that uses only which original support sites are causally reachable from that bounded event window.

## Lemma: eventual support saturation

For every finite `S subset [L,R]` and fixed finite window `J=[a,b]`, there is

`T = max(a-L, R-b, 0)`

such that for every `t >= T`,

`S subset I(J,t)`.

### Proof

For `t >= a-L`, `a-t <= L`; for `t >= R-b`, `b+t >= R`. Hence `[L,R] subset [a-t,b+t]`, and therefore `S subset I(J,t)`. QED.

In particular, the set-valued selector

`Q_t = S intersect I(J,t)`

is eventually exactly `S`. Any observable depending only on `Q_t` (cardinality, leftmost/rightmost reachable support index, ordered list of reachable original 1s, etc.) is therefore eventually constant.

## Consequence for the birth-budget search

Run125 correctly required an episode-dependent selector rather than a function of the reconstructed initial row alone. But episode dependence supplied only by *causal-cone membership* is still insufficient: for late bounded-location episodes the cone has already swallowed the entire finite original support.

So a useful selector must contain finer information than

`which original actual 1s can causally influence this episode?`

It must distinguish how influence/provenance is routed inside the cone, or carry an oriented crossing/order datum that changes from episode to episode. This is consistent with the earlier stopping fences: ancestry alone permits unlimited reuse, while recovered-row observables are conserved.

## What this does not prove

This does not rule out a support-index selector defined by a canonical *path*, first/last crossing of a moving cut, parity/phase decoration, or another episode-relative routing rule. It only rules out selectors that are functions of the intersection of the finite original support with the ordinary backward light cone of a fixed bounded source-relative window.

## Next target

If the finite-support selector route is continued, require a transition law for a routed label, not mere reachability. A minimal candidate would attach to each forced birth a canonical crossing of a moving spacetime cut and prove that the crossing's original-support label advances (or has uniformly bounded reuse) across both resetting and nonresetting passages.
