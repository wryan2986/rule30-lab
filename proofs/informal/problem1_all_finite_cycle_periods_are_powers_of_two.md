# Problem 1: all finite A-cycle periods are powers of two

## Context

Runs 37--40 isolated a one-bit extension structure for the finite-state map `A`:

`A(x) >> 1 = A(x >> 1)`.

Run 38 analyzed lifts of a parent cycle in detail and used the no-reset parity obstruction to study *uniqueness* of the lifted orbit.  For the weaker but important question of which exact periods can occur, that parity obstruction is unnecessary.

## Theorem

Every finite periodic point of `A` has exact period a power of two.

## Proof

Let `x(t)` be an `n`-bit periodic orbit of exact period `p`, and project away its least significant bit:

`u(t) = x(t) >> 1`.

The triangular identity

`A(x) >> 1 = A(x >> 1)`

shows that `u(t)` is itself a periodic orbit of `A` on at most `n-1` bits.  Let its exact period be `q`.  Necessarily `q | p`.

Write

`x(t) = 2 u(t) + b(t)`,  `b(t) in {0,1}`.

During one parent period `q`, the low bit is updated by a deterministic composition of `q` maps `{0,1} -> {0,1}`.  Call the resulting return map `F`.

Because `x(t)` is periodic, `b(t)` lies on a periodic orbit of `F`.  But a self-map of a two-element set has no cycles except lengths 1 and 2.  Therefore the number `r` of parent periods required for the full lifted state to return satisfies

`r in {1,2}`.

Hence

`p = q r`,

so every one-bit extension either preserves the exact period or doubles it.

At one bit the only possible exact period is 1.  Induction on bitlength therefore gives

`p = 2^k`

for some `k >= 0`.

This proves the theorem.

## Relation to the previous parity obstruction

The primitive-cylinder parity theorem from runs 38--40 is still relevant, but only for the stronger observed claim that there is exactly one finite periodic orbit at each bitlength.

Indeed, over a parent cycle the fiber return map can be:

- constant: one lifted periodic orbit, with the parent period;
- identity: two lifted periodic orbits, each with the parent period;
- transposition: one lifted periodic orbit, with doubled period.

The unresolved no-reset parity lemma is precisely what would exclude the identity case in the finite terminating cylinders of interest.  It is **not** needed to exclude odd or otherwise non-power-of-two exact periods.

## Consequence for the global Problem 1 route

The computational observation from run 36 that finite exact periods 3,5,6,7 do not occur is now a theorem in full generality, not merely evidence through `Fix(A^8)`.

Thus any hypothetical finite survivor that evades the same-period collision/repair bounds by changing exact period can only move among powers of two.  In particular, every genuine increase of exact period is a doubling (possibly after stretches in which bitlength grows while the exact period stays fixed).

The remaining global task is to connect this dyadic period hierarchy to the existing FULL/common-origin/finite-entry accounting.  Separately, proving the primitive-cylinder odd-parity lemma would upgrade the result to uniqueness of the periodic orbit at each bitlength and determine exactly when the period doubles.
