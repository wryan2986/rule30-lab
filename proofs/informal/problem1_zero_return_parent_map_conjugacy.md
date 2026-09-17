# Problem 1: exact parent map for the zero-return graph

## Context

Run 84 gave an explicit inverse for the boundary-to-diagonal endpoint bijection `rho_n` and showed that its action on all primitive necklaces is often dominated by very large cycles. The useful object is therefore not the unrestricted endpoint permutation but the way `rho_n` interacts with singular integration at zero columns.

This note isolates that interaction exactly.

## Derivative map

Write

`D(x) = S x XOR x`.

At a zero target `(0,w)`, the singular predecessor equation is exactly

`D(x)=w`.

On a cyclic binary word, `D(x)=w` is solvable iff `w` has even XOR parity. When it is solvable there are exactly two solutions, `x` and `complement(x)`.

Starting from either boundary state `(x,0)`, the deterministic off-zero connector reaches the diagonal endpoint `(rho_n(x),rho_n(x))`, and the next inverse step produces the next zero target `(0,rho_n(x))`.

Therefore the zero-return graph has the exact edge description

`D(x) -> rho_n(x)`

for every nonzero `x`, with the two complementary integrations of the same even parent accounting for the two candidate outgoing branches.

## Exact parent map

Because `rho_n` is a bijection on nonzero words, every nonzero zero-return target `a` has a unique boundary preimage

`x = rho_n^{-1}(a)`.

Hence its zero-return parent is forced:

`P_n(a) = D(rho_n^{-1}(a))`.

So

`boxed: P_n = D o rho_n^{-1}`.

This is an exact functional description of the reverse zero-return graph. It packages an arbitrarily long connector into one endpoint permutation followed by the one-step derivative.

Several earlier structural facts become immediate from this formula:

1. **Unique parent / no merger.** Every nonzero target has exactly one parent word under `P_n`. Thus two distinct zero-return parents cannot merge into the same child.
2. **Parents always have even parity.** Every cyclic derivative `D(x)` has even XOR parity. Thus odd-parity vertices can occur only as terminating leaves, exactly matching the singular integration criterion.
3. **Children of an even parent.** If `w=D(x)`, its two integrations are `x` and `complement(x)`, so its two candidate children are `rho_n(x)` and `rho_n(complement(x))` (modulo rotational identification in the necklace quotient).
4. **The zero-return graph can be studied without connector lengths.** Connector length affects computational cost but not adjacency once `rho_n` or `rho_n^{-1}` is known.

## Naturality inherited from rho

Run 82 proved that `rho_n` is rotation-equivariant and commutes with repetition. The derivative `D` has the same two properties. Consequently `P_n` is rotation-equivariant:

`P_n(S^k a) = S^k P_n(a)`.

It also commutes with repetition. If `R_m` repeats a `q`-bit word `m` times into period `n=mq`, then

`P_n(R_m(a)) = R_m(P_q(a))`.

Thus the exact parent dynamics descends to necklaces and recursively inherits every proper-period sector. The genuinely new part at a doubled period is again confined to the full-period sector, but now this statement applies directly to the zero-return parent map rather than only to endpoint matching.

## Why this is useful

The run-84 proposal was to identify the sparse primitive necklaces that are actual terminating leaves and locate them inside the large `rho_n` cycles. The parent formula sharpens that target: an odd primitive necklace `a` is a terminating leaf, and its complete ancestry is obtained by iterating

`a, P_n(a), P_n^2(a), ...`

until the distinguished root/inherited sector is reached. Equivalently, rather than enumerating the full endpoint permutation and then separately reconstructing zero-return connectors, one can compute `rho_n^{-1}` only on the leaf/ancestor states actually needed and apply `D` after each first-hit computation.

This also suggests a potentially more useful invariant search: statistics need not be invariant under `rho_n`; they need only constrain the composed map `D o rho_n^{-1}` on the full-period sector. The huge primitive cycles of `rho_n` found in run 84 therefore do not by themselves rule out a simple monotone or filtration statistic for the actual zero-return tree.

## Status

Problem 1 remains open. The new result is an exact conjugacy-style formula for zero-return ancestry,

`P_n = D o rho_n^{-1}`,

which turns the sparse-leaf question into direct iteration of a functional parent map and separates graph adjacency from enormous connector lengths. The next computational target should be a census of `P_n` on primitive necklaces for manageable `n`, especially the odd-parity leaves and their ancestor depths, rather than another census of cycles of `rho_n` itself.
