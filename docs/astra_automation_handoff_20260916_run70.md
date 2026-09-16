# Astra automation handoff — 2026-09-16 run 70

## What changed

Continued directly from run 69's complete p=16 zero-return graph. There was no intervening work on `research/astra-next` after run 69.

Added:

- `proofs/informal/problem1_zero_return_graph_comparison_p1_p16.md`

Research commit: `2428cc09e0bfb00df485e5c283f90e2a124c82aa`.

## New result

Computed the exact zero-column first-return graphs for p=1,2,4,8 under the same conventions as the p=16 census and compared all five dyadic scales.

Census `(vertices, even internal, odd leaves, connector edges with multiplicity, simple edges)`:

- p=1: `(2,1,1,1,1)`;
- p=2: `(3,2,1,3,2)`;
- p=4: `(4,3,1,5,3)`;
- p=8: `(5,4,1,7,4)`;
- p=16: `(36,20,16,39,35)`.

After collapsing parallel phase-equivalent edges, G_1 through G_8 are paths. G_8 is explicitly

`00000000 -> 11111111 -> 01010101 -> 01110111 -> 00001011`

with connector lengths `3,5,21,371`.

At p=16 this exact lower-period path is inherited by repetition. The first five internal vertices have primitive periods `1,1,2,4,8`, ending at repeated p=8 leaf `0000101100001011`. The next target `0000110001010011` has full period 16.

The sharper new observation is that after parallel-edge collapse, G_16 is a rooted tree: 36 vertices, 35 simple edges, root indegree zero, and every other vertex indegree exactly one. Its genuinely period-16 part is a full binary tree with 15 internal vertices and 16 leaves. Every one of those 15 internal full-period targets has two distinct children, and no branches merge.

This explains the identity `16 leaves = 15 new full-period internal targets + 1` structurally, not just numerically.

## Evidence status

Exact finite computation. The p<=8 graphs were independently regenerated from the reverse recurrence. The p=16 counts agree with run 69; the new topology statistics were extracted from that exact graph. No all-scale tree theorem is claimed.

## Best next target

Do not jump immediately to a complete p=32 traversal. First analyze **mergers** in the zero-return map: derive a criterion for two distinct zero-target necklaces to have the same next-return child modulo rotation. The reverse-predecessor uniqueness theorem does not automatically rule this out after quotienting. If mergers can be excluded for full-period targets, then each genuine even branching vertex increases the terminating-leaf count by exactly one, reducing the counting problem to reachable full-period even zero targets.
