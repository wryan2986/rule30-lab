# Astra automation handoff — run 98 — 2026-09-17

## Starting state

No intervening repository work was present after run 97. Starting branch tip: `a466dba598d5120e1a6847c6f07bbf88f79bc1d5`.

## New exact covariance / strategy fence

Added `proofs/informal/problem1_support_bound_extension_is_tail_covariant.md`.

For a finite row, choose a right support bound `R` and `v=L_R(r)`. If the same row is represented with the later nominal support bound `R'=R+m`, then `v'=2^m v`, and exactly

    e_(v')(n)-R' = e_v(n+m)-R.

Thus appending nominal zero cuts does not strengthen normalized physical excess; it only deletes a finite prefix. This is the spatial-cut analogue of run 97's physical-time restart covariance.

## Strategic consequence

Do not attempt to create overshoot by moving the bookkeeping support bound farther into the zero tail. The arbitrary absolute coordinate `R` and trailing-zero padding are not usable finite resources. A successful non-covariant argument must be attached to intrinsic actual-support / complete-fringe data (e.g. last actual 1, support width relative to a fixed intrinsic origin, bounded-use fringe state, or ordered erasure).

The unresolved target remains an all-depth mechanism forcing new maxima of `e_v(n)-R` (or an equivalent non-telescoping charge) on the FULL finite-fringe domain.

## Problem 1 status

OPEN.

Research commit: `a620c03acd518ee046034144d2c54720a61926dc`.
