# Problem 1: explicit off-diagonal cycle family and inverse parity identity

## Context

Run 78 corrected an overreach in the zero-return-tree argument: no-merger and acyclicity of the graph of *existing* zero returns do not prove that every deterministic connector has a subsequent zero return.  The off-zero inverse pair map may instead enter a periodic orbit disjoint from the diagonal.

This note shows that this obstruction is real, not merely hypothetical, and records a parity identity that may help separate doubled-leaf portal states from nonreturning cycles.

## Setup

For a nonzero current word `a`, the unique predecessor word `y` relative to the following word `b` is defined by

\[
 b=S y\oplus(a\lor y),
\]

and the inverse pair map is

\[
 T(a,b)=(y,a).
\]

A zero return occurs exactly when the pair reaches the diagonal `a=b`; then the unique predecessor is `y=0`.

## The off-diagonal obstruction exists at every even ambient period

Let `p` be even and let

\[
 a=0101\cdots01,\qquad b=1010\cdots10=\bar a,
\]

with the convention for `S` chosen consistently with the repository recurrence.  The two alternating words are spatial shifts of one another, so

\[
 S b=a,
\]

and because they are complements,

\[
 a\lor b=1^p.
\]

Set `y=b`.  Then

\[
 S y\oplus(a\lor y)=a\oplus1^p=\bar a=b.
\]

Thus `y=b` satisfies the predecessor equation, and uniqueness for `a != 0` gives

\[
 T(a,b)=(b,a).
\]

Applying the same argument with `a,b` interchanged gives

\[
 T(b,a)=(a,b).
\]

Therefore

\[
 \boxed{(a,b)\leftrightarrow(b,a)}
\]

is an exact period-two orbit of the off-zero inverse map for **every even `p`**.  It never hits the diagonal because `a != b`.

So a theorem asserting that every off-zero connector eventually returns to zero is false.  Any all-depth argument must use special structure of the states produced by singular integrations / doubled-leaf portals, rather than only finiteness and injectivity of the ambient inverse state space.

Modulo spatial rotation the two alternating words represent the same necklace, so this orbit may collapse in a spatial-rotation quotient of pair states.  That does not create a zero return: the exact pair never satisfies `a=b`, and the generated predecessor word is never zero.

## Small-period exact census

A direct exhaustive enumeration of the unique inverse pair map gives the following number of off-diagonal temporal cycles for small ambient periods (cycles identified up to temporal starting point, but not spatial rotation):

| p | off-diagonal cycles | temporal cycle lengths observed |
|---|---:|---|
| 1 | 0 | — |
| 2 | 1 | 2 |
| 3 | 0 | — |
| 4 | 2 | 2, 12 |
| 5 | 2 | 5, 110 |
| 6 | 8 | 2, 39, 60 |

The `p=2` cycle is exactly

`(01,10) -> (10,01) -> (01,10)`.

At `p=4`, the inherited alternating cycle is

`(0101,1010) -> (1010,0101) -> ...`,

but there is also a genuinely different 12-cycle.  Odd periods are not automatically safe: `p=5` already has cycles of lengths 5 and 110.  Thus simple parity of the ambient period cannot prove return existence.

These census values are exploratory computational facts; the explicit alternating family above is proved exactly and does not depend on the census.

## Exact parity identity for one inverse step

Rewrite the predecessor equation bitwise as

\[
 b=S y\oplus(a\lor y).
\]

Taking XOR parity over all coordinates and using `P(Sy)=P(y)`,

\[
 P(b)=P(y)\oplus P(a\lor y).
\]

Since bitwise

\[
 a\lor y = y\oplus(a\land\neg y),
\]

we obtain

\[
 \boxed{P(b)=P(a\land\neg y).}
\]

Equivalently, the parity of the old following column equals the parity of the set of sites where `a` has a 1 and its unique predecessor `y` has a 0.

For a temporal orbit written as consecutive columns `... , x_{t-1}, x_t, x_{t+1}, ...` under the inverse recurrence, this is

\[
 \boxed{P(x_{t-1})=P(x_t\land\neg x_{t+1}).}
\]

This identity is exact at every nonzero `x_t`.  It is not by itself a monotone quantity, but it is a local necessary constraint on every off-diagonal periodic orbit and is a plausible filter to combine with the antiperiodic structure of doubled-leaf portal integrations.

## Consequence for the current strategy

Run 78's return-existence gap cannot be closed by proving that the ambient inverse map has no off-diagonal cycles: such cycles exist in an infinite explicit family.  The target must be narrowed to the **portal subset**.

The useful next questions are therefore:

1. Identify an invariant or congruence satisfied by states obtained from doubled odd-parity leaves that is violated by all off-diagonal cycles.
2. Determine whether the portal antiperiodicity `S^p x = complement(x)` survives in some derived quantity under repeated inverse steps, even though it need not survive literally column-by-column.
3. Use exact cycle detection on the first `p=32` portal rather than only extending a no-return step bound; the existence of ambient cycles means a detected repeat would be a genuine counterexample to unconditional portal return.

## Status

This does **not** settle portal return existence.  It does settle a key meta-question: nonreturning off-diagonal periodic behavior is genuinely present in the inverse dynamics, including at every even period, so future proofs must exploit portal-specific structure.
