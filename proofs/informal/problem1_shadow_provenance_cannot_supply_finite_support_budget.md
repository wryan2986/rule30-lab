# Shadow provenance cannot by itself supply the finite-support birth budget

Status: `partial-proof` / stopping fence. This note corrects the next-target proposal in run120. It does not exclude FULL. Problem 1 remains OPEN.

## 1. Proposed route and hidden mismatch

Run120 isolated the two-bit nonreset birth forcing to the source-relative shadow word `001` and proposed tracing those three shadow cells backward to time zero, hoping successive births might have strictly ordered time-zero provenance/intercepts and therefore bounded reuse.

That proposal conflates two different finite objects:

1. the original ACTUAL finite support of `r(0)`, and
2. the time-zero support/disagreement set of the GLOBAL SHADOW `E(r(0))`.

The second object is not finite. `problem1_global_cycle_shadow.md` Section 3 already proves that for every nonzero finitely supported actual row, `E(r)` has infinitely many 1s to the right of the actual support, hence the initial disagreement set `{i:r_i != E(r)_i}` is infinite.

Therefore an injective or strictly ordered assignment of successive forced births to time-zero SHADOW cells, or even to time-zero actual/shadow DISAGREEMENTS, would not yield a contradiction. There is an infinite right-hand reservoir available from the start.

## 2. Exact cone geometry for the 001 motif

At a two-bit nonreset source time `t`, run120 uses shadow cells at positions `0,1,2`. Rule 30 has radius one, so their time-zero backward cones are respectively

    [-t,t], [1-t,1+t], [2-t,2+t].

Their union is

    [-t, t+2].                                      (1)

Thus later occurrences naturally inspect progressively farther-right initial shadow coordinates. This is exactly the direction in which the global-shadow theorem supplies infinitely many initial disagreements. A theorem saying that successive motifs use strictly increasing rightmost intercepts would therefore be compatible with infinitely many forced births, not contradictory to finite ACTUAL support.

The same issue was already identified for renewal injections in `problem1_global_cycle_shadow.md` Section 4: a valid initial ancestor is an actual/shadow disagreement `d_k(0)=1`, but this cannot automatically be charged to an original nonzero actual bit, and no bounded reuse is known. The right-half disagreement supply is infinite.

## 3. Consequence

The provenance route only becomes a finite-support budget if it proves an additional bridge of one of the following forms:

* every charged shadow/disagreement ancestor maps injectively (or with uniformly bounded multiplicity) to an ORIGINAL ACTUAL nonzero cell; or
* the charged ancestors lie in a fixed finite interval determined by the original actual support; or
* some finite quantity derived from the actual row is irreversibly consumed when a new shadow provenance class is used.

Ordering shadow intercepts alone is insufficient. Bounded reuse of shadow intercepts alone is also insufficient, because there are infinitely many available intercepts.

For the run120 `001` motif, the minimal Boolean forcing certificate contains no such bridge: it is entirely in the auxiliary shadow spacetime. Continuing its three cells backward through `E(r)` without a separate actual-support charge therefore cannot close the birth budget.

## 4. Revised target

Do not spend another run merely computing or ordering the time-zero intercepts of the three `001` shadow cells. First seek a bridge from the forced birth to the finite ACTUAL initial row. A viable characteristic statement must end at an original actual `1` (or another demonstrably finite original resource), with a proof of bounded reuse. If no such bridge can be derived, the characteristic/provenance route is blocked for the same reason as the earlier renewal-ancestry route.

Dependencies: `problem1_two_bit_birth_forcing_cone_collapses_to_001.md`, `problem1_global_cycle_shadow.md` Sections 3-4, `problem1_nonreset_return_birth_spacing.md`.
