# Problem 1: zero-return graph no-merger theorem

## Purpose

Run 70 observed computationally that the simple zero-column first-return graph `G_16` has no mergers: every non-root vertex has indegree one. The handoff correctly noted that one-step reverse-predecessor uniqueness away from zero columns does not *by itself* prove this after quotienting by rotation. However, combining first-return minimality with deterministic **forward** evolution does prove a general no-merger theorem.

## Setup

Let the cyclic column-pair dynamics be

\[
F(a,b)=(b,\;Sa\oplus(b\lor a)).
\]

A zero state means a pair whose first component is zero, written `Z(w)=(0,w)`. The zero-return graph is oriented in the reverse-search direction: an edge

\[
[Z(w)]\longrightarrow[Z(z)]
\]

means that one admissible reverse integration at `Z(w)`, followed by unique reverse propagation through nonzero first components, first reaches the rotation class `[Z(z)]`. Thus the interior of the connector contains no zero state.

Cyclic rotation commutes with `F`, so `F(S^k a,S^k b)=S^kF(a,b)`.

## Theorem

**No-merger theorem.** In the simple zero-column first-return graph modulo cyclic rotation, every vertex has indegree at most one. Equivalently, two distinct zero-target necklaces cannot have the same next-return child necklace.

This statement is independent of period, parity, or the special p=16 census.

## Proof

Assume two simple edges merge:

\[
[A]\to[C],\qquad [B]\to[C],
\]

where `[A] != [B]` are zero-state rotation classes.

Choose a representative `C` of the common child class. Because the two reverse connectors may originally terminate at rotated representatives of `C`, rotate each whole connector so that both terminate at this same `C`. This is legitimate by shift-equivariance of both the forward and reverse equations.

Reverse the two connectors. We now have two **forward** orbit segments beginning at exactly the same state `C` and ending at zero states `A'` and `B'`, with no zero state in the interior of either segment. Since forward evolution `F` is a function, both segments are prefixes of the same unique forward orbit of `C`.

Let their positive lengths be `r` and `s`.

- If `r=s`, determinism gives `A'=B'`, hence `[A]=[B]`, contradiction.
- If, say, `r<s`, then the zero state `A'=F^r(C)` occurs strictly inside the length-`s` segment from `C` to `B'`. But that segment is the reversal of a zero-to-zero **first-return** connector, so by definition it has no interior zero state. Contradiction.

Therefore distinct zero-state necklaces cannot merge. QED.

## Consequences

1. The no-merger property observed at p=16 is structural, not empirical. No future `G_p` can contain a vertex with two distinct simple incoming edges.

2. Any finite reachable simple zero-return graph rooted at `(0,0)` is automatically a rooted tree once cycles are excluded. More generally, without an acyclicity assumption it is a rooted functional-predecessor structure with indegree at most one; any nontrivial cycle would have to be entered from no distinct earlier vertex.

3. Every genuine branching event in a finite acyclic terminating basin increases the number of leaves by exactly one. Hence for a rooted binary zero-return tree,

\[
L = B+1,
\]

where `B` is the number of vertices whose two complementary integrations yield two distinct child necklaces. Vertices whose integrations phase-collapse contribute one simple child and do not change the leaf count.

4. The p=16 identity `16 leaves = 15 genuine full-period branching vertices + 1` is therefore an instance of a general tree-counting law, provided the reachable basin is finite and acyclic.

## What remains open

The theorem removes **mergers** from the list of phenomena needing classification. The main unresolved graph-theoretic obstruction is now cycles / nontermination in the zero-return dynamics, together with the harder counting problem: which reachable even zero targets phase-collapse and which genuinely branch?

A productive next step is therefore to study whether a zero-return cycle can exist in the relevant dyadic terminating basin, or to find a monotone/invariant quantity excluding such cycles. If cycles are excluded, the reverse basin is a tree at every finite period and terminating-necklace counts reduce directly to genuine branch counts.
