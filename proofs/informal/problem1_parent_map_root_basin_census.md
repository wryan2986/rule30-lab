# Problem 1: root-basin census for the zero-return parent map

## Context

Run 85 identified the exact parent map

\[
P_n(a)=D(\rho_n^{-1}(a)),\qquad D(x)=Sx\oplus x,
\]

on nonzero zero-target words, with rotation equivariance.  This note carries out the proposed small-period computation, but with an important distinction: the full functional graph of `P_n` contains components that are not reachable from the terminal root.  The object relevant to the reverse Rule-30 basin is only the component whose forward `P_n` iterates reach `0`, modulo cyclic rotation.

## Exact computation

I implemented `rho_n^{-1}` using the exact reverse pair map from run 84,

\[
F(u,v)=(v,\;Su\oplus(v\lor u)),
\]

starting at `(a,a)` and iterating until the boundary section `(x,0)` is reached.  Then `P_n(a)=D(x)`.  Representatives were canonicalized by minimum cyclic rotation.  As a sanity check, the implementation reproduces the previously established period-4 connector `rho_4(0011)=1110` up to cyclic rotation, with connector length 19.

For every necklace at each `n<=10`, I computed `P_n` and retained exactly those necklaces whose `P_n` orbit reaches the root `0`.

| n | all binary necklaces | root-basin vertices (including 0) | leaves | primitive leaves | maximum parent depth |
|---:|---:|---:|---:|---:|---:|
| 2 | 3 | 3 | 1 | 1 | 2 |
| 3 | 4 | 2 | 1 | 0 | 1 |
| 4 | 6 | 4 | 1 | 1 | 3 |
| 5 | 8 | 2 | 1 | 0 | 1 |
| 6 | 14 | 3 | 1 | 0 | 2 |
| 7 | 20 | 2 | 1 | 0 | 1 |
| 8 | 36 | 5 | 1 | 1 | 4 |
| 9 | 60 | 2 | 1 | 0 | 1 |
| 10 | 108 | 3 | 1 | 0 | 2 |

Through `n=10` every root-basin vertex has at most one root-basin child, so these small basins are paths rather than genuinely branching trees.  This does **not** contradict the previously observed new full-period branching at period 16; it shows that branching first becomes visible beyond this small census.

The leaves (canonical necklace representatives) are:

- `n=2`: `01`
- `n=3`: `111`
- `n=4`: `0111`
- `n=5`: `11111`
- `n=6`: `010101`
- `n=7`: `1111111`
- `n=8`: `00001011`
- `n=9`: `111111111`
- `n=10`: `0101010101`

Each listed leaf has odd XOR parity, exactly as required for termination of singular integration.

## Dyadic inherited chain and connector lengths

The dyadic basins through period 8 expose the repetition structure particularly cleanly.

At period 8 the unique root-to-leaf chain, written in the parent direction, is

\[
00001011 \to 01110111 \to 01010101 \to 11111111 \to 00000000.
\]

The corresponding child-to-parent connector lengths from the root outward are

\[
1,\;3,\;19,\;369.
\]

The first three are inherited unchanged under repetition from periods 2 and 4, exactly as predicted by the naturality theorem for `rho_n`/`P_n`.  The new full-period period-8 edge has connector length 369.

This gives a useful consistency check against the later period-16/32 computations: connector lengths can grow extremely rapidly even while the zero-return graph itself remains combinatorially tiny.

## Important strategic correction

Enumerating the *entire* functional graph of `P_n` is too broad for Problem 1, for essentially the same reason that run 84 found the unrestricted `rho_n` permutation too broad.  `P_n` has functional components outside the terminal root basin.  For example, at period 3 the non-root even necklaces form a rotation-collapsed component that does not reach zero.  Such components are irrelevant to the reverse basin generated from the terminal zero state.

Therefore candidate monotone statistics should be tested first on the root basin (and, at dyadic doubling, on the newly attached full-period portal trees), not demanded globally on all zero-target necklaces.

## Consequence / next target

The small-period data strongly separates two phenomena:

1. inherited lower-period ancestry, whose connector lengths are unchanged by repetition; and
2. genuinely new full-period portal ancestry, which first becomes structurally important at the already studied period-16 stage and can have enormous connector lengths after doubling.

The next computation should therefore avoid a global `P_16` enumeration.  Instead, reconstruct only the known period-16 root basin/portal vertices from the existing research artifacts, express each edge using `P_16`, and compare the full-period children against their parents for statistics such as run structure, cyclic derivative weight, transition count, and exact rotational period.  This targets the finite set that actually matters and avoids spending work on unrelated functional components.
