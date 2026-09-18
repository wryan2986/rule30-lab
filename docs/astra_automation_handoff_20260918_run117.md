# Astra automation handoff — run 117 — 2026-09-18

Problem 1 remains OPEN. Continue on `research/astra-next`.

Starting tip was `379553c0488f44e7bbb711d35d87d2044135a7a5`; no intervening work was present.

## New result

Added `proofs/informal/problem1_left_edge_prefix_has_coalescing_dyadic_attractor.md`.

For moving-left-edge coordinates `b_j(t)=x_{L-t+j}(t)`, the exact autonomous prefix recurrence is

    b_j(t+1)=b_{j-2}(t) XOR (b_{j-1}(t) OR b_j(t)),

with negative indices zero. Physical finite-support rows have `b_0=1` forever, and `b_1=1` after one step. Unlike the right-edge prefix map, this map is noninjective.

Exhaustive enumeration of every prefix with `b_0=1` through width 19 (262144 states at width 19) found that all initial prefixes at each width coalesce onto one eventual cycle up to phase. Observed cycle lengths are 1 for widths 1-3, 2 for widths 4-8, and 4 for widths 9-19. Maximum transient lengths through widths 1..19 are `0,1,2,2,4,5,6,8,8,11,12,14,14,16,17,19,22,22,26`.

This is recorded as computational evidence, not an all-width theorem.

## Stopping fence / next target

A fixed left-edge prefix is not a promising nonrenewable original-support resource: it autonomously forgets initial data and, through width 19, collapses to a universal small dyadic attractor. Thus the run-116 source-indexed characteristic proposal must use unbounded depth/history rather than merely a bounded left-edge automaton.

Next target: trace the spacetime characteristic carrying a forced `beta=1` birth backward to time zero and test whether successive forced births have strictly ordered time-zero intercepts or crossing data with bounded reuse.

Research commit: `d75249b165a8fbcfc9179007ecd7524e5576383d`.
