# Run 188 — the t+8 candidate gate bit is the complement of the terminal center

Status: `partial-proof`. Problem 1 remains OPEN.

## Starting point

Run 187 proved that in the beta=1 return branch, if the forced positive-delay row at physical time `t+8` is nonresetting, its gate bit is

\[
\alpha=1\oplus a\oplus b,
\]

where at the proved cyclic `u`-source at `t+4`

\[
(r_{-2},r_{-1},r_0,r_1,r_2,r_3)=(a,b,1,1,1,0).
\]

Run 186 had instead expressed the same bit as

\[
\alpha=x\oplus(r_3(t+6)\lor r_4(t+6)),
\qquad x=r_0(t+6),
\]

and therefore suggested that knowing `x` alone might be insufficient.  The following literal two-step calculation removes that apparent extra freedom.

## Exact center transport from t+4 to t+6

Use Rule 30 in the form

\[
F(l,c,r)=l\oplus(c\lor r).
\]

From the rigid `t+4` prefix,

\[
r_0(t+5)=b\oplus(1\lor1)=1\oplus b,
\]

while

\[
r_{-1}(t+5)=a\oplus(b\lor1)=1\oplus a
\]

and

\[
r_1(t+5)=1\oplus(1\lor1)=0.
\]

Therefore the terminal center bit at `t+6` is

\[
\begin{aligned}
x=r_0(t+6)
 &=r_{-1}(t+5)\oplus(r_0(t+5)\lor r_1(t+5))\\
 &=(1\oplus a)\oplus((1\oplus b)\lor0)\\
 &=a\oplus b.
\end{aligned}
\]

Hence

\[
\boxed{x=a\oplus b}.
\]

Combining with run 187 immediately gives

\[
\boxed{\alpha=1\oplus x}.
\]

Thus the pair `(a,b)` need not be classified separately merely to determine the candidate `t+8` gate: its equality bit is already exactly the terminal center bit.

## Conditional nonresetting classification

Run 185 proved that if `t+8` is nonresetting then `alpha=1` is the one-bit gate-`u` case with delay 1, while `alpha=0` is the two-bit gate-`t` case with delay 2.  The new identity therefore rewrites that classification entirely in terms of the actual terminal center at `t+6`:

* `x=0` => `alpha=1`: gate `u`, one-bit, `tau(Y_(t+8))=1`, `Delta_(t+7)=2`;
* `x=1` => `alpha=0`: gate `t`, two-bit, `tau(Y_(t+8))=2`, `Delta_(t+7)=3`.

This also corrects the run-186 interpretation that `x` by itself was insufficient.  Its wider-right OR term is not independent on this actual return trajectory.  Comparing

\[
\alpha=x\oplus\omega
\]

from run 186 with `alpha=1 xor x` gives, on this branch,

\[
\boxed{\omega=r_3(t+6)\lor r_4(t+6)=1}.
\]

That is a derived consistency identity, not an independent assumption.

## Exhaustive local audit

The center calculation was also exhaustively checked for all four `(a,b)` assignments and all eight assignments of the arbitrary `t+4` cells `(r_4,r_5,r_6)`.  In all 32 cases direct two-step Rule-30 evolution gives

\[
r_0(t+6)=a\oplus b,
\]

independent of those wider-right cells.

## What this does and does not prove

This does **not** prove that `t+8` is nonresetting, nor does it determine `x`.  It removes a false two-datum bottleneck: for purposes of classifying a hypothetical nonresetting recurrence at `t+8`, the single actual terminal center bit `x` is sufficient.

The next useful target is therefore the complete resetting one-bit `t`-source at `t+6`: determine whether its retained complete driver/global-front constraints force `x`, or alternatively classify resetting versus nonresetting at `t+8` directly as a function of `x`.  Do not separately chase `(r_-2,r_-1)(t+4)` unless needed for that stronger classification.
