# Initial-one ancestry exists, but generic reuse is unbounded

## Context

Run134 showed that the unconditional left-sensitive intercept of each distinguished source-relative `011` event is strictly ordered but eventually lands in the infinite initial zero tail. The suggested alternative was to route state-dependently back to the finite set of initial 1-sites.

There is an important stopping fence here: **existence of such a route is automatic for every 1-cell, but existence alone gives no budget.**

## Lemma: every 1-cell has a backward path through 1-cells to an initial 1

For Rule 30 the output-1 neighborhoods are exactly

    001, 010, 011, 100.

Every one contains at least one 1-parent. Therefore, given any spacetime cell of value 1 at positive time, choose any 1-valued parent in its predecessor neighborhood. Repeating decreases time by one at each step and preserves cell value 1, so after finitely many steps the path reaches time zero at a 1-site.

For finite-support initial data, that endpoint belongs to the finite initial support.

This remains true at the exceptional sensitive-provenance motif `011`: although neither of its 1-parents is Boolean-sensitive, either the center or right 1 can still be chosen as an ordinary 1-ancestry parent.

## Why this does not solve the birth budget

The map from later 1-events to initial 1-sites can have arbitrarily large reuse. The sharpest example is the single-seed initial condition. Its initial support contains exactly one 1-site. Consequently **every 1-cell at every later time has every complete 1-parent ancestry route ending at that same single initial 1-site** (there is no other possible time-zero 1 endpoint).

In particular, all `011` events occurring in the single-seed orbit charge to the same initial 1. Earlier computation in this branch already found thousands of generic `011` events by time 199. Thus merely reconnecting a distinguished `011` event to an initial 1-site cannot provide a finite event bound; even support size one allows unboundedly many later events to reuse the sole label in generic Rule-30 evolution.

## Consequence for Problem 1

A useful theorem must prove **bounded multiplicity specifically for the distinguished source-relative events**, not merely existence, uniqueness-by-convention, or finite range of an ancestry label. Equivalently, if a canonical 1-parent routing is introduced, the missing statement is of the form:

> under FULL and the cyclic-source constraints, each initial 1-site can be the endpoint of at most C distinguished `011` events (or some analogous finite bound).

Without a source-relative bounded-reuse theorem, state-dependent routing to initial 1-sites is only a relabeling and does not close the contradiction.

This complements run134: unconditional sensitive routing gives injective labels in an infinite zero tail, while ordinary 1-ancestry gives labels in a finite set but has no injectivity/bounded-reuse property. A successful resource must combine both features rather than supplying only one of them.
