# Astra automation handoff — run 121

Problem 1 remains OPEN.

Starting branch tip: `b0e250efef5dd04e8d9b1a16a5720c6c63171dc7` (`research/astra-next`). No intervening work was found after run120.

## New result / correction

Run120 proposed tracing the source-relative shadow `001` motif backward to time zero and seeking strictly ordered provenance/intercepts. That target cannot by itself yield the required finite-support birth budget.

The global shadow `E(r)` is a second initial row, not the finite actual row. For every nonzero finitely supported actual `r`, the already-proved global-shadow theorem says `E(r)` has infinitely many 1s to the right of the actual support, hence infinitely many initial actual/shadow disagreements. At source time `t`, the three shadow cells at positions 0,1,2 have combined time-zero cone `[-t,t+2]`, which grows precisely into that infinite right-hand reservoir.

Therefore even a theorem that successive forced births have distinct, strictly ordered, or bounded-reuse SHADOW intercepts would be compatible with infinitely many births. It does not contradict finite ACTUAL support.

Recorded in `proofs/informal/problem1_shadow_provenance_cannot_supply_finite_support_budget.md`.

## Stopping fence

Do not merely trace/order the `001` cells through the global shadow. Shadow provenance is an infinite resource. This is the same structural obstruction already noted for renewal ancestry: an initial disagreement ancestor is not automatically an original actual nonzero bit.

## Revised target

A characteristic budget now needs an explicit bridge to a genuinely finite original ACTUAL resource: e.g. prove every forced birth charges an original actual 1 with uniformly bounded multiplicity, prove all charged ancestors lie in a fixed finite interval, or identify another finite actual-row quantity irreversibly consumed. Without such a bridge, the provenance route is blocked.
