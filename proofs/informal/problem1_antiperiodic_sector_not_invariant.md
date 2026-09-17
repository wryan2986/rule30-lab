# Problem 1: antiperiodic sector is not invariant under the boundary endpoint map

## Setup

Let `rho_n(x)` be the boundary-to-diagonal endpoint map established in runs 80–81: starting from `(x,0)`, iterate the unique off-zero inverse map until the first diagonal state `(a,a)`, and set `rho_n(x)=a`.

Run 82 proved rotation equivariance

`rho_n(S^k x) = S^k rho_n(x)`

and proposed testing whether, for even `n`, the antiperiodic sector

`A_n = {x : S^(n/2) x = complement(x)}`

is invariant under `rho_n`.

## Exact consequence of rotation equivariance

If `x in A_n`, then

`rho_n(complement(x)) = rho_n(S^(n/2)x) = S^(n/2) rho_n(x)`.

Thus the endpoints of the complementary pair `x, complement(x)` are always related by half-rotation. This is an exact constraint, but it does **not** imply that `rho_n(x)` is itself antiperiodic: that stronger conclusion would require complement equivariance of `rho_n`, which is false in general.

## Counterexample at n=4

Use the bit convention in which cyclic rotation direction is immaterial to the antiperiodicity statement. Take

`x = 0011`.

Its half-rotation is `1100 = complement(0011)`, so `x in A_4`.

Exact iteration of the established inverse recurrence from boundary state `(x,0)` reaches its first diagonal endpoint after 19 `T`-iterations, with

`rho_4(0011) = 1110`.

But half-rotating `1110` gives `1011`, whereas its complement is `0001`. Hence

`rho_4(0011) notin A_4`.

Therefore

**the antiperiodic sector is not invariant under `rho_n`, already at n=4.**

This rules out the proposed direct reduction of the p=32 portal to a 16-bit quotient by assuming antiperiodicity survives all the way to the diagonal endpoint.

## Small exhaustive census

An independent exhaustive implementation of the unique predecessor recurrence checked every antiperiodic boundary word for small even periods. Results:

| ambient period n | antiperiodic words | endpoints still antiperiodic |
|---:|---:|---:|
| 2 | 2 | 2 |
| 4 | 4 | 0 |
| 6 | 8 | 2 |
| 8 | 16 | 0 |

The first-return lengths observed in these exhaustive checks were at most 3, 19, 54, and 369 respectively. These numbers are computational observations, not claimed formulas.

## What survives and what fails

Survives exactly:

`rho_n(complement(x)) = S^(n/2) rho_n(x)` for antiperiodic `x`.

Fails:

`rho_n(x) in A_n` in general.

The reason the tempting invariance argument breaks is visible already in the inverse equation

`b = S y XOR (a OR y)`.

Half-rotation commutes with shift/XOR/OR, but complement does not commute with OR: `complement(a OR y) = complement(a) AND complement(y)`, not `complement(a) OR complement(y)`. Thus the relation `H a = complement(a), H b = complement(b)` is not preserved by one inverse step in general.

## Research consequence

For the long p=32 doubled-leaf portal, antiperiodicity is a property of the initial integration word but cannot be treated as an invariant state-space reduction. The next useful structural target should instead exploit the exact paired-endpoint law above, or search for a different symmetry/statistic preserved by the connector. A practical computational target is to enumerate `rho_n` on primitive necklaces for n <= 12 or 16 and test candidate invariants against the endpoint permutation before attempting another p=32 traversal.
