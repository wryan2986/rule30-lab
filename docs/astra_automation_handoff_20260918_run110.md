# Astra automation handoff — run 110 — 2026-09-18

## Starting state

No intervening repository work was present after run 109. Starting branch tip: `d049109f30a1f2d0557e9c150a481fc322a4e12e`.

## New stopping fence

Added `proofs/informal/problem1_moving_right_fringe_prefix_is_purely_periodic_no_go.md`.

For right endpoint `R`, define moving-edge bits

    a_j(t)=(T^t r)_{R+t-j}.

Rule 30 gives exactly

    a_j(t+1)=a_j(t) XOR (a_{j-1}(t) OR a_{j-2}(t)),

with `a_-1=a_-2=0`. Thus every fixed prefix `(a_0,...,a_J)` is autonomous. Its update is a triangular XOR map: each output coordinate is its old value XOR a function of lower coordinates. It is therefore bijective, with inverse recovered successively from low to high coordinates.

Hence every fixed-width moving-right-fringe prefix evolves by a permutation of a finite state space and is purely periodic from time zero. The state graph proposed as a possible target in run 109 cannot be acyclic; it is a disjoint union of cycles.

This rules out a finite-support budget based only on instantaneous bits in any fixed-width strip behind the maximal right ray. A successful non-reuse invariant must include information beyond such a prefix: e.g. unbounded-depth anchored phase/history, core/global-shadow coupling, or source/characteristic-indexed state.

Problem 1 remains OPEN.

Research commit: `cddc981994218a365142439ac5f76e6b08040cc2`.
