# Problem 1: exact leaf balance in a fixed-period portal tree

## Statement

Fix a finite period `n` and one genuinely new exact-period-`n` portal component in the zero-return graph, modulo rotation. Assume the previously established facts on `research/astra-next`:

1. every vertex in the component has a unique parent (no mergers);
2. every even-parity exact-period-`n` vertex has exactly two child necklaces;
3. every odd-parity exact-period-`n` vertex has no children; and
4. the fixed-period portal component is finite.

Let `E` be the number of even-parity vertices in the component and `O` the number of odd-parity vertices. Then

`O = E + 1`.

Consequently the total number of full-period vertices is

`V = E + O = 2E + 1 = 2O - 1`,

so every fixed-period portal component has odd cardinality. In particular, if `N_prim(n)` is the number of primitive binary necklaces of length `n`, then

`E <= floor((N_prim(n)-1)/2)`

and

`O <= floor((N_prim(n)+1)/2)`.

For dyadic `n=2^m`, where

`N_prim(n) = (2^n - 2^(n/2))/n`,

this improves the crude full-period internal-vertex count by a factor of about two, but remains exponential and therefore does not supply the finite-support birth budget required by the main Problem 1 argument.

## Proof

By facts 1 and 4, the portal component is a finite rooted tree: the portal child is the root of the new exact-period component, and every other vertex has exactly one incoming edge from within the component.

By facts 2 and 3, every vertex has outdegree either two (exactly the even-parity vertices) or zero (exactly the odd-parity vertices). Thus the component is a finite full binary tree.

A finite rooted tree with `V` vertices has exactly `V-1` edges. Counting those same edges by parent outdegree gives exactly `2E` edges. Hence

`2E = V - 1 = E + O - 1`,

and therefore

`O = E + 1`.

The remaining identities and primitive-necklace bounds follow immediately.

## Interpretation

This is an exact conservation law for the new full-period component: every nonterminal even target creates two children, but globally the finite no-merger structure forces precisely one more terminal odd target than nonterminal even targets. The portal tree therefore cannot hide an excess of continuing even states without paying for them with terminal odd leaves.

This does **not** yet connect the count to the original finite support. The key unresolved bridge remains to bound `E` (or equivalently `O`) in terms of the width/support of the original finite configuration, rather than in terms of the ambient primitive-necklace state count.

## Possible use in the finite-support argument

Any future injection from portal-tree odd leaves into a finite family of original-support resources would immediately bound the entire portal component: if at most `B` such resources are available, then `O <= B`, `E <= B-1`, and `V <= 2B-1`. Thus it is enough to control terminal odd leaves; one does not separately need a bound on all internal full-period births.
