# Problem 1: zero-return graph comparison for p = 1,2,4,8,16

## Purpose

Run 69 completed the p=16 zero-column first-return graph and proposed comparing the smaller dyadic graphs before attempting p=32. This note carries out that comparison using the same exact reverse recurrence and rotation quotient.

## Setup

For cyclic p-bit words use

\[
q_{i+2}=S q_i\oplus(q_{i+1}\lor q_i),
\]

and the reverse predecessor equation

\[
w=Sx\oplus(u\lor x).
\]

Vertices of `G_p` are zero-column states `(0,w)` modulo cyclic rotation. Even-parity `w` are internal vertices; odd-parity `w` are leaves. At an even vertex, solve `Sx xor x = w`, then follow the unique reverse predecessor while the first component is nonzero, stopping at the next zero-column state. At `(0,0)` discard the trivial all-zero self-loop.

All calculations below are exact finite computations. For `u != 0`, the predecessor was obtained by the proved one-pass recurrence, not by state-pair enumeration.

## Graph census

| p | zero-target necklaces | even internal | odd leaves | connector edges with multiplicity | simple directed edges |
|---:|---:|---:|---:|---:|---:|
| 1 | 2 | 1 | 1 | 1 | 1 |
| 2 | 3 | 2 | 1 | 3 | 2 |
| 4 | 4 | 3 | 1 | 5 | 3 |
| 8 | 5 | 4 | 1 | 7 | 4 |
| 16 | 36 | 20 | 16 | 39 | 35 |

Thus `G_1,G_2,G_4,G_8`, after collapsing parallel edges caused by phase-equivalent complementary integrations, are simple directed paths. The first genuinely branching quotient graph is `G_16`.

The small paths are explicit:

- `G_1`: `0 -> 1`;
- `G_2`: `00 -> 11 -> 01`;
- `G_4`: `0000 -> 1111 -> 0101 -> 0111`;
- `G_8`: `00000000 -> 11111111 -> 01010101 -> 01110111 -> 00001011`.

(The final p=8 representative is a cyclic rotation of the previously used terminating word convention.)

The deterministic connector lengths along the p=8 path are respectively

\[
3,\ 5,\ 21,\ 371.
\]

These are inherited unchanged at p=16 through repetition, exactly as predicted by the earlier embedding lemma.

## Stronger p=16 topology

Run 69 established 36 vertices, 20 even internal vertices, 16 odd leaves, and 39 connector edges at p=16. The new comparison exposes a sharper graph-theoretic fact.

After identifying parallel edges with the same endpoints, the p=16 graph has exactly 35 simple edges on 36 vertices. Its indegrees are:

- root `(0,0)`: indegree 0;
- every other vertex: indegree exactly 1.

Since run 69 already checked that the graph is acyclic and every vertex is reachable from the root, the simple quotient graph is therefore a **rooted tree**.

Its first five internal vertices form the inherited lower-period spine:

```text
0000000000000000
 -> 1111111111111111
 -> 0101010101010101
 -> 0111011101110111
 -> 0000101100001011
```

Their primitive periods are `1,1,2,4,8`. The next return is the first genuinely period-16 internal target,

```text
0000110001010011
```

and from that point onward all 15 full-period internal vertices have two **distinct** children. There are exactly 16 odd full-period leaves.

Consequently the new part of `G_16`, beginning at `0000110001010011`, is a full binary tree in the graph-theoretic sense: 15 internal binary vertices and 16 leaves. It is not balanced; the leaf depths in the whole rooted graph are distributed as

- depth 7: 3 leaves;
- depth 8: 1;
- depth 10: 3;
- depth 11: 1;
- depth 13: 2;
- depth 14: 3;
- depth 15: 1;
- depth 16: 2.

So the identity `16 leaves = 15 new full-period internal vertices + 1` is not merely a numerical coincidence: it is realized by the exact rooted-tree topology.

## Interpretation

This comparison gives a cleaner replacement for the failed uniqueness conjecture.

For p <= 8, every complementary derivative pair collapses to one child necklace, so the zero-return graph is a path. At p=16, the inherited period-1/2/4/8 spine still behaves exactly that way. The first full-period return target then starts a finite binary branching tree in which every full-period even target has two distinct child necklaces and, empirically at p=16, no two branches ever merge.

The non-merging property is important. The exact predecessor theorem guarantees deterministic connectors away from zero columns, but it does **not** by itself prevent two different zero targets from eventually returning to the same later zero-target necklace after rotation quotienting. The p=16 census shows that no such merger occurs.

Thus a plausible next structural question is not a recurrence for leaf counts alone, but whether the genuinely new full-period part of `G_{2p}` is always a forest/tree grafted onto the repeated copy of `G_p`, and under what conditions mergers are impossible.

## Immediate next target

Before attempting a complete p=32 graph, derive a criterion for two distinct zero-target necklaces to have the same next-return child modulo rotation. If such a merger can be ruled out for full-period targets in the terminating basin, then every genuine even-parity branching event increases the leaf count by exactly one. In that case counting terminating necklaces reduces to counting reachable full-period even zero targets, rather than tracking the full reverse basin.
