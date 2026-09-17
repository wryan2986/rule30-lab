# Problem 1: full-period zero-return vertices branch unless terminal

## Context

Run 89 showed that the two complementary integrations born at a doubled odd leaf collapse to one necklace because those integrations are antiperiodic. This raised the question whether the new full-period portal subtree might remain a path.

The answer is essentially the opposite once one leaves the inherited portal parent: every **even-parity full-period** zero target has two distinct child necklaces. Thus post-portal branching is forced unless the full-period portal child is already odd (terminal).

## Setup

For a zero target `w`, singular integration solves

`D(x) = Sx XOR x = w`.

If `w` has even XOR parity, there are exactly two integrations, `x` and `complement(x)`. Their candidate zero-return children are

`rho_n(x)` and `rho_n(complement(x))`.

Rotation equivariance and bijectivity of `rho_n` imply that these two children are the same necklace iff `x` and `complement(x)` are the same necklace.

## Lemma: complementary integrations of a full-period target are distinct necklaces

Assume `w` has exact rotational period `n` and even parity. Let `D(x)=w`.

Suppose for contradiction that `x` and `complement(x)` are the same necklace. Then for some cyclic shift `S^k`,

`S^k x = complement(x)`.

Apply `D`. Since `D` commutes with rotation and complement has the same derivative as the original word,

`S^k w = D(S^k x) = D(complement(x)) = D(x) = w`.

Because `w` has exact period `n`, this forces `k = 0 mod n`. But then `x = complement(x)`, impossible for a binary word.

Therefore `x` and `complement(x)` lie in distinct necklaces.

By rotation equivariance and injectivity of `rho_n`, their endpoints also lie in distinct necklaces.

Hence:

**Theorem.** Every even-parity exact-period-`n` zero-return vertex has exactly two distinct child necklaces. Every odd-parity vertex has no children. In particular, within the exact-period-`n` sector there is no one-child continuation.

## Relation to run 89

There is no contradiction with the single portal edge of run 89. A doubled odd leaf `ww` has exact period `r`, not `2r`; its two integrations at ambient period `2r` are antiperiodic and therefore are rotations of one another. That inherited proper-period parent has one new full-period portal child necklace.

After that portal child is reached, however, it has exact period `2r`. If its parity is odd, it terminates immediately. If its parity is even, the theorem above forces two distinct child necklaces.

Thus a genuinely new full-period portal component has the local form:

- one portal edge born from the doubled odd lower-period leaf;
- thereafter every nonterminal full-period vertex branches into exactly two necklace children;
- terminal full-period vertices are exactly the odd-parity ones.

Together with unique-parent/no-merger, the new full-period component is therefore a rooted **full binary tree** (possibly finite or infinite in depth), not a path, after its unique portal root.

## Consequence for the research strategy

The path hypothesis proposed after run 89 is false unless every portal child happens to be odd. More importantly, the branching structure is now completely rigid: there is no irregular one-child branching to classify. The unresolved issue is solely whether every branch of this full binary tree reaches odd parity in finite depth (or, equivalently in the dyadic setting, whether the newly attached full-period tree is finite).

This reframes the period-32 obstruction. A very long connector controls the adjacency of one branch, but combinatorially any even full-period target necessarily has two distinct descendants. A proof of Problem 1 cannot rely on path structure; it needs a well-founded statistic, finite-depth argument, or global counting obstruction that forces odd leaves on every full-period branch.

## Status

Problem 1 remains open. This note rules out the post-portal path hypothesis and proves exact binary branching at every nonterminal full-period zero-return vertex.
