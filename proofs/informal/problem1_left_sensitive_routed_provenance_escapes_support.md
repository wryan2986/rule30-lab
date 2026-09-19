# The canonical left-sensitive provenance ray escapes finite original support

Status: `stopping-fence`. Problem 1 remains OPEN.

## Claim

The most canonical routed-provenance refinement left after support-cone saturation cannot supply the missing finite-support birth budget.

Rule 30 is

    f(l,c,r) = l XOR (c OR r).

For every fixed `(c,r)`, flipping `l` flips the output. Hence the left input is unconditionally Boolean-sensitive at every spacetime cell. Following this sensitivity backward gives a canonical dependency ray: from physical cell `(j,t)` go to `(j-1,t-1)`, and after `t` steps arrive at the unique time-zero coordinate

    j-t.                                                   (1)

Now let the original finite actual support be contained in `[L,R]`. For any source-relative event cell whose physical coordinate is bounded, say `j in [a,b]` independently of the episode time `t`, equation (1) gives a time-zero intercept in

    [a-t,b-t].                                             (2)

Once `t > b-L`, the entire interval (2) lies strictly left of `L`. Thus every canonical left-sensitive provenance ray from every cell in that bounded event window misses the original actual support at all sufficiently late episodes.

The same conclusion holds for any fixed finite collection of source-relative cells: its left-sensitive intercept set translates left at speed one and eventually becomes disjoint from the finite original support.

## Consequence

Run126 showed that ordinary backward cones eventually contain *all* original support and therefore lose discrimination. The opposite extreme also fails: selecting the unique unconditional left-sensitive characteristic does not choose a useful support label; it eventually chooses no original-support site at all.

Therefore an admissible routed-provenance selector must use state-dependent branching/crossing information inside the cone. It cannot be merely (i) the set of causally reachable original support sites, or (ii) the unconditional left-permutive sensitivity ray. In particular, left-permutivity/injectivity alone cannot furnish the requested bounded-reuse charge.

This does not rule out a state-dependent path whose branch decisions depend on the actual/shadow episode, nor a cut-crossing invariant carrying more than a single sensitivity ray. Any such proposal must prove that its selected label remains in the finite original support and has a one-way or bounded-reuse transition law across both resetting and nonresetting passages.

## Relation to existing stopping fences

This complements `problem1_support_cone_selector_eventually_saturates.md`: the full cone becomes too broad, while the canonical left-sensitive ray becomes too narrow and escapes the support. It also sharpens `problem1_actual_ancestry_alone_cannot_bound_births.md`: even the strongest locally canonical ancestry supplied directly by left-permutivity does not yield a late support charge.
