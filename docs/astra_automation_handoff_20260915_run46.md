# Astra automation handoff — 2026-09-15 run 46

Problem 1 remains open.

## New progress

Added `proofs/informal/problem1_doubling_tower_temporal_rank.md`.

For a genuine one-bit lift from exact period `p` to exact period `2p`, run 45 gave `b(t+p)=1 xor b(t)`. Because all finite cycle periods are powers of two, the new fiber column itself must have exact temporal period `2p`: its period divides `2p`, but antiperiodicity excludes every divisor of `p`.

For a nested genuine doubling tower

`p, 2p, 4p, ..., 2^r p`,

the introduced fiber columns `b_j`, viewed on the final temporal period, satisfy `per(b_j)=2^j p`. Hence they are F2-linearly independent: every linear combination of earlier columns has period dividing `2^{j-1}p`, while `b_j` does not. Therefore `r` doublings force temporal column rank `r`.

This supplies a genuine non-reuse invariant once multiple certificates coexist in one spacetime object. It is stronger than scalar boundary hits and full-cycle parity, both of which lost information in runs 43--45.

## Limitation

No contradiction with finite entry yet. A growing finite state can support growing temporal rank. The existing bounded-activity result currently bounds boundary/joint-window occupancy, not obviously F2 rank.

## Highest-value next step

Audit the exact common-origin joint-window transport lemmas for whether they preserve whole coordinate histories, or restrictions long enough to preserve the period-filtration/rank argument. Then seek either:

1. a uniform rank bound under bounded activity/finite entry, or
2. an inequality converting rank `r` in one common joint window into activity tending to infinity.

If the existing transport only preserves scalar occupancy, record that explicitly: it would identify the precise missing theorem as rank-preserving common-origin transport rather than another local doubling certificate.