# Astra automation handoff — run 89 — 2026-09-17

## Starting state

No intervening repository work was present after run 88. Starting branch tip: `dd75c68782033dd2ebccf7753efb16b319c7b57a`.

## New result

Added `proofs/informal/problem1_doubled_odd_portal_is_single_necklace_edge.md`.

Run 88 showed that for odd exact-period-`r` `w`, the two integrations of `ww` at period `2r` are complementary antiperiodic words `x, complement(x)` with

`S^r x = complement(x)`.

Therefore the two integrations are the same necklace. Rotation equivariance of `rho_{2r}` then gives

`rho_{2r}(complement(x)) = S^r rho_{2r}(x)`,

so their zero-return endpoints are also the same necklace.

Thus a doubled odd leaf creates exactly ONE new full-period portal child in the necklace-level zero-return graph, not two. Equivalently, odd exact-period-`r` necklaces are naturally in bijection with antiperiodic exact-period-`2r` portal necklaces.

This removes complementary-pair branching at portal birth. If a lower-period root basin has one odd leaf, its doubled copy receives one new portal child necklace. Any later branching must arise farther out in the full-period sector.

## Problem 1 status

OPEN.

## Next target

Determine whether a full-period portal subtree can branch after its unique portal child, or whether a further structural property forces the dyadic root basin to remain a path. A proof of path structure would reduce each dyadic stage to one full-period ancestry chain and make the period-32 obstruction substantially more rigid.

Research commit: `f31a71732706d82c2085f98e4c89b891771021e3`.
