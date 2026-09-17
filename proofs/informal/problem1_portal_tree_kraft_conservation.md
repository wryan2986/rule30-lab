# Problem 1: Kraft conservation for fixed-period portal trees

## Statement

Fix one genuinely new exact-period-`n` portal component in the zero-return graph, modulo rotation. By the established results on `research/astra-next`, this component is a finite full binary tree: every even-parity exact-period vertex has exactly two children and every odd-parity vertex is terminal.

Measure depth from the portal child, so the root has depth 0. If the terminal odd leaves have depths `d_1,...,d_O`, then

`sum_i 2^(-d_i) = 1`.

Equivalently, if `L_d` is the number of terminal odd leaves at depth `d`, then

`sum_{d>=0} L_d / 2^d = 1`.

This is stronger than the unweighted leaf balance `O=E+1`: it constrains where the terminal leaves can occur, not merely how many there are.

## Proof

Give the portal root mass 1. Whenever an even/nonterminal vertex has mass `m`, give each of its two children mass `m/2`. A vertex at depth `d` therefore has mass `2^(-d)`.

Because the tree is finite, repeatedly replacing the mass of each internal vertex by the equal total mass of its two children eventually moves all mass to the terminal leaves without changing total mass. The root began with mass 1, hence the leaf masses sum to 1.

## Consequences

1. For every `D>=0`, the number of terminal leaves at depth at most `D` is at most `2^D`.

2. If there are `O` terminal leaves, at least one leaf has depth at most `floor(log2 O)`. Otherwise every leaf would have depth strictly greater than `log2 O`, giving `sum_i 2^(-d_i)<1`, contradiction.

3. More generally, the portal component can be viewed as an exact prefix code: continuing through an even vertex consumes one binary branch choice, and terminal odd vertices are precisely the codewords. No terminal leaf can be an ancestor of another terminal leaf, and completeness is expressed by the Kraft equality rather than merely the Kraft inequality.

## Relevance to the finite-support bottleneck

The previous leaf-balance reduction showed that it is enough to bound the number `O` of terminal odd leaves by resources of the original finite survivor. Kraft conservation gives a potentially more flexible route: a charging argument may assign resources to *branch cylinders* rather than inject leaves one-for-one. A resource controlling all descendants below depth `k` naturally carries dyadic mass `2^(-k)`.

However, Kraft conservation alone does **not** bound `O`: arbitrarily large finite full binary trees still satisfy the equality. It therefore does not supply the missing finite-support birth budget by itself. Any use in the main proof still requires a new statement tying branch depth or dyadic branch mass to the original finite fringe/support.

## Strategic implication

When searching for the finite-support bridge, test whether an original-support event fixes a finite prefix of portal branch choices. If so, the event corresponds to a dyadic cylinder of mass `2^(-k)`, and disjointness of terminal cylinders may permit a weighted charging argument even when a literal injection of individual leaves is unavailable. This is the precise additional information supplied beyond `O=E+1`.
