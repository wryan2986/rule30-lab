# Problem 1: eliminate the doubling fiber into protected parent traces

## Setup

Use the one-bit lift recurrence from the existing doubling analysis

\[
w_s=2z_s+a_s,
\qquad
 a_{s+1}=c_s\oplus(b_s\lor a_s),
\]

where `a_s` is the newly introduced low fiber bit and `b_s,c_s` are traces belonging to the parent/high state. Suppose the parent trace has period `p`.

A genuine period doubling is equivalent to the one-period fiber return map being the transposition on `{0,1}`, equivalently

\[
a_{s+p}=1\oplus a_s
\]

for both initial fiber values.

## Exact elimination

For one time step define the fiber map

\[
f_s(a)=c_s\oplus(b_s\lor a).
\]

There are only two cases.

* If `b_s=1`, then

  \[
  f_s(a)=c_s\oplus1,
  \]

  which is constant, independent of `a`.

* If `b_s=0`, then

  \[
  f_s(a)=c_s\oplus a.
  \]

  This is the identity when `c_s=0` and the transposition when `c_s=1`.

Let

\[
F=f_{p-1}\circ\cdots\circ f_0
\]

be the return map after one parent period. If any `b_s=1`, one factor of the composition is constant. Every later composition remains constant, so `F` cannot be a transposition. Therefore a genuine doubling forces

\[
\boxed{b_s=0\quad\text{for every }0\le s<p.}
\]

When all `b_s=0`, composition is affine XOR:

\[
F(a)=a\oplus\bigoplus_{s=0}^{p-1}c_s.
\]

Hence `F` is the transposition exactly when

\[
\boxed{\bigoplus_{s=0}^{p-1}c_s=1.}
\]

Thus the low fiber can be eliminated completely:

\[
\boxed{
\text{genuine }p\to2p\text{ doubling}
\iff
\left(b_0=\cdots=b_{p-1}=0\right)
\ \text{and}\
\left(\bigoplus_{s=0}^{p-1}c_s=1\right).
}
\]

No history of the forced low bit `a` is needed to certify the doubling.

## Why this matters for the common-origin obstruction

Run 50 showed that the antiperiodic `a`-column lies exactly in the reset/forcing boundary layer, so its history cannot be transported verbatim into the original realization. The criterion above removes that obstruction at the algebraic level: it replaces the forced fiber certificate by a condition entirely on the parent/high traces `b,c`, which are the protected quantities singled out by the exact projection identity.

The condition is also substantially stronger than a single boundary hit. Every genuine doubling requires a full parent period of zeros in the `b` trace, together with odd parity of the companion `c` trace over exactly that period.

## Immediate next target

Identify `b_s` and `c_s` explicitly as spatial columns/coordinates of the common-origin realization at the relevant scan depth. Then ask whether infinitely many actual doublings force either:

1. arbitrarily long protected zero blocks in one family of temporal columns plus odd companion parity; or
2. a bounded-activity contradiction by charging each odd-parity `c` block to genuine joint-window activity.

The key point is that future work should use this parent-only criterion rather than attempting to transport the low forced fiber.

## Status

This is an exact local iff statement, conditional only on the established one-bit recurrence and the parent period `p`. It does not by itself prove Problem 1; the remaining task is to connect repeated parent-trace certificates on the scan to the fixed common-origin realization and the finite-entry/activity budget.
