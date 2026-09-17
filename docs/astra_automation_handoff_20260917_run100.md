# Astra automation handoff — run 100 — 2026-09-17

## Starting state

No intervening repository work was present after run 99. Starting branch tip: `c718a6a3df1d92efb145ee5368edb757158e01f9`.

## New exact result

Added `proofs/informal/problem1_normalized_excess_germ_is_physical_orbit_invariant.md`.

For a finite row `r` with right endpoint `R`, tail seed `v=L_R(r)`, and

    q_r(n)=tau(2^n v)-n-R,

the physical restart `r_t=T^t(r)` has endpoint `R+t` and tail seed `T^t(v)`. Combining the established physical-time tail conjugacy with endpoint motion gives, for every fixed `t` and all sufficiently large `n`,

    q_(r_t)(n)=q_r(n+2t).

Therefore the cut-invariant germ from run 99 is also invariant under every finite physical restart:

    Q(T^t r)=Q(r).

So `Q` is a genuine forward physical-orbit invariant. Boundedness/unboundedness above, infinite positive excursions, and `limsup=+infinity` are unchanged by discarding any finite physical transient.

## Why this helps

Future FULL/fringe arguments may restart at any convenient late physical row or source class without changing the scalar target. This is useful normalization freedom: a proof can choose a favorable late complete-fringe/core configuration, while still needing an intrinsic survivor-specific bounded-reuse or ordered-erasure mechanism to force overshoot.

It also fences off another class of false arguments: no quantity whose only force comes from retaining a special finite initial physical prefix can control the germ `Q`.

## Problem 1 status

OPEN. The missing theorem remains an all-depth FULL-dependent mechanism forcing the physical-orbit invariant germ `Q` to be unbounded above.

Research commit: `c35399da2de110d10a48d692ac87a27ba1de4f45`.
