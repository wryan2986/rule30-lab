# Problem 1: inverse endpoint map and primitive-necklace cycle census

## Context

Run 81 defined the boundary-to-diagonal bijection `rho_n`: start the off-zero inverse dynamics at `(x,0)`, `x != 0`, and stop at the first diagonal state `(a,a)`; then `rho_n(x)=a`. Run 82 proved rotation equivariance, repetition naturality, and exact-period preservation. Run 83 disproved invariance of the antiperiodic sector.

This note records a useful exact inverse description and an exhaustive census of the induced permutation on primitive necklaces for small `n`.

## Explicit inverse pair map

The off-zero inverse map is

`T(a,b) = (y,a)`

where `y` is uniquely determined by

`b = S y XOR (a OR y)`.

If an output pair `(u,v)` is known, then the previous pair is forced:

`a=v`,

`b = S u XOR (v OR u)`.

Thus define

`F(u,v) = (v, S u XOR (v OR u))`.

Whenever the relevant off-zero predecessor exists,

`F = T^{-1}`.

Consequently `rho_n^{-1}` has an exact first-hit description: start at the diagonal `(a,a)` and iterate `F` backward along the unique connector until the first state whose second component is zero. If that boundary state is `(x,0)`, then

`rho_n^{-1}(a)=x`.

This makes `rho_n` a Poincare/first-hit matching between the nonzero boundary section `{(x,0)}` and nonzero diagonal section `{(a,a)}` of the same reversible off-zero pair dynamics. It does not by itself accelerate long connectors, but it is useful structurally: endpoint questions can be attacked from either section.

## Exhaustive primitive-necklace census

I enumerated every nonzero word for `2 <= n <= 10`, computed `rho_n` by exact predecessor iteration, restricted to words of exact rotational period `n`, quotient by cyclic rotation using the lexicographically/numerically least rotation, and decomposed the induced permutation into cycles.

The results are:

| n | primitive necklaces | cycle lengths of induced rho_n |
|---|---:|---|
| 2 | 1 | 1 |
| 3 | 2 | 1, 1 |
| 4 | 3 | 1, 2 |
| 5 | 6 | 1, 5 |
| 6 | 9 | 1, 2, 2, 4 |
| 7 | 18 | 1, 2, 6, 9 |
| 8 | 30 | 1, 1, 28 |
| 9 | 56 | 1, 5, 50 |
| 10 | 99 | 2, 5, 6, 8, 9, 20, 49 |

Sanity check against run 83: with the same bit/shift convention, `rho_4(0011)=1110` after exactly 19 `T` iterations.

### Immediate implications

1. The primitive-necklace action is not close to an involution. Already at `n=5` it contains a 5-cycle; at `n=8` one cycle contains 28 of the 30 primitive necklaces; at `n=9` one cycle contains 50 of 56.
2. There is no universal primitive-necklace fixed point: at `n=10` there are no 1-cycles at all.
3. The large cycles at `n=8,9` make any strong invariant that partitions primitive necklaces into many small classes unlikely. Any proposed invariant preserved by `rho_n` must be constant on each listed cycle; in particular at `n=8` it must take the same value on 28/30 primitive necklaces, and at `n=9` on 50/56.
4. This supports shifting attention away from simple endpoint statistics (weight, parity, run counts, antiperiodicity, etc.) toward either the first-hit geometry of the reversible pair map or special properties of the zero-return tree/leaf subset.

## Additional statistic checks

On primitive words, Hamming weight and parity are not generally preserved. Exact counts of primitive words for which they happen to agree between input and endpoint are:

| n | primitive words | weight preserved | parity preserved |
|---|---:|---:|---:|
| 2 | 2 | 2 | 2 |
| 3 | 6 | 6 | 6 |
| 4 | 12 | 4 | 4 |
| 5 | 30 | 5 | 10 |
| 6 | 54 | 6 | 42 |
| 7 | 126 | 21 | 70 |
| 8 | 240 | 32 | 96 |

So neither is a viable general endpoint invariant.

## Status

Problem 1 remains open. This run did not find a new conserved endpoint statistic; instead it gives a stronger negative result: the primitive endpoint permutation can have very large cycles, so simple invariant-partition strategies are severely constrained.

The most promising next target is to exploit the explicit reverse map `F` on the *special diagonal endpoints relevant to zero-return leaves*, or to characterize which primitive necklaces are terminating leaves under the zero-return graph and see how that sparse subset sits inside the large `rho_n` cycles. That is more targeted than searching for invariants on all primitive necklaces.
