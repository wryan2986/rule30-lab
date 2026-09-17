# Problem 1: boundary-to-diagonal bijection for the off-zero inverse dynamics

## Setup

Fix finite spatial period `p`. For `a != 0`, let

`T(a,b) = (y,a)`

where `y` is the unique solution of

`b = S y XOR (a OR y)`.

Previous runs established:

1. `T` is injective on the domain `a != 0`.
2. A zero return occurs exactly when the current pair is diagonal: `a=b` (with `a != 0`), because then the next predecessor word is zero.
3. Every post-zero connector begins at a boundary state `(x,0)`, `x != 0`, and every such boundary-launched connector reaches a diagonal state in finite time.

Define

- boundary `B = {(x,0): x != 0}`;
- nonzero diagonal `Delta = {(a,a): a != 0}`.

Both sets have cardinality `2^p - 1`.

## Theorem

The first-diagonal endpoint map

`R : B -> Delta`

obtained by iterating `T` from `(x,0)` until its first diagonal hit is a bijection.

Equivalently, every nonzero diagonal state `(a,a)` is reached from exactly one post-zero boundary state `(x,0)`.

## Proof

Existence of `R(x,0)` for every boundary state is the return-existence theorem from run 80.

It remains to prove injectivity. Suppose two distinct boundary states `u=(x,0)` and `v=(x',0)` first hit the same diagonal state `d`, after respectively `m` and `n` iterations:

`T^m(u)=d=T^n(v)`.

Assume without loss of generality `m <= n`.

Because all states before the first diagonal hit remain in the off-zero domain, injectivity of `T` lets us cancel equal images backwards `m` times. Hence

`u = T^(n-m)(v)`.

If `m=n`, this gives `u=v`, contrary to distinctness.

If `m<n`, then `u` has an off-zero predecessor along the orbit from `v`. But no boundary state `(x,0)` has any predecessor in the off-zero domain: the second component of every image `T(a,b)=(y,a)` equals the nonzero input `a`, whereas a boundary state's second component is zero. Contradiction.

Thus distinct boundary states have distinct diagonal endpoints, so `R` is injective. Since `|B|=|Delta|=2^p-1`, it is bijective. QED.

## Structural consequence: chain/cycle decomposition

Consider states with both components nonzero. The map is injective wherever it is defined. Boundary states are precisely the natural sources for the transient connector chains, while diagonal states are the zero-return exits.

The theorem shows that the boundary-launched part consists of exactly `2^p-1` pairwise-disjoint finite directed chains, each connecting one boundary state to one distinct nonzero diagonal state. Any remaining recurrent off-diagonal states belong to cycles inaccessible from these chains (as already observed computationally in runs 78-79).

Therefore the inverse dynamics induces a permutation-like matching

`rho_p : {nonzero p-bit words} -> {nonzero p-bit words}`

where `rho_p(x)=a` iff the connector launched from `(x,0)` first reaches `(a,a)`.

This matching is a bijection, although no efficient formula for `rho_p` is currently known.

## Explicit universal connector-length bound

Before hitting its diagonal endpoint, a boundary-launched chain cannot repeat any state. After the initial boundary state, every pre-return state has both components nonzero and is off diagonal. There are

`(2^p-1)(2^p-2)`

ordered off-diagonal pairs with both entries nonzero.

Hence every boundary connector reaches the diagonal after at most

`1 + (2^p-1)(2^p-2)`

applications of `T` (depending on whether the initial boundary-to-interior step is counted separately; the important scale is strictly below `2^(2p)`).

This bound is far too large to make `p=32` brute force practical, but it is an unconditional finite upper bound derived solely from injectivity and the boundary condition.

## Why this matters for Problem 1

The zero-return operation is not merely total on post-zero integrations: at fixed period it pairs all `2^p-1` possible nonzero boundary words bijectively with all `2^p-1` possible nonzero zero-return targets.

This suggests replacing long connector traversal by direct study of the induced bijection `rho_p`. For the dyadic `p -> 2p` program, the next useful question is whether `rho_{2p}` has a recursion on doubled / antiperiodic inputs inherited from `rho_p`. Such a recursion could bypass the >100 million-step connectors encountered at `p=32`.