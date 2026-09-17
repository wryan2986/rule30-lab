# Astra automation handoff — run 85

## Main result: exact zero-return parent map

No intervening work was present after run 84 (`98ec3fbe15c18dbb7823642371811e130964ee82`).

Let `D(x)=S x XOR x`. Singular integration at a zero target `w` is exactly `D(x)=w`; when solvable, the two integrations are `x` and `complement(x)`. The connector from `(x,0)` ends at the next zero target `rho_n(x)`.

Therefore every zero-return edge has the exact form

`D(x) -> rho_n(x)`.

Since `rho_n` is a bijection, every nonzero target `a` has a unique parent

`P_n(a) = D(rho_n^{-1}(a))`.

Thus the reverse zero-return graph is the functional map

`P_n = D o rho_n^{-1}`.

This recovers unique-parent/no-merger immediately, shows all parents have even parity, and cleanly separates graph adjacency from connector length. Rotation equivariance and repetition naturality of `rho_n` and `D` imply the same properties for `P_n`, so all proper-period parent dynamics are recursively inherited.

The main strategic consequence is that run 84's huge cycles of `rho_n` do not rule out a useful statistic for the actual zero-return graph: the relevant map for ancestry is the composition `D o rho_n^{-1}`, not `rho_n` alone.

Full note:

`proofs/informal/problem1_zero_return_parent_map_conjugacy.md`

Research commit: `87fadfc565a55dee12e621c75183c09bef73a957`

## Status / next target

Problem 1 remains open. Next useful computation: enumerate `P_n` on primitive necklaces for manageable periods, identify odd-parity terminating leaves, measure their ancestor depths and branch structure, and search for a monotone/filtration statistic of `P_n`. This is more targeted than further invariant searches on the unrestricted endpoint permutation.
