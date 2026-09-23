# Problem 1 run 229 — exact square-map forcing

Problem 1 remains open.

## Setup

For the near-edge automaton from runs 223–228,

\[
x'_0=x_0,\qquad x'_1=x_1\oplus x_0,
\]

and for `r>=2`,

\[
x'_r=x_r\oplus f_r(x),\qquad f_r(x)=x_{r-1}\lor x_{r-2}.
\]

Run 228 showed that the top-coordinate orbit parity is an even-time parity of this forcing and proposed analyzing the square map explicitly.

## Boolean derivative identity for OR

For Boolean bits `a,b,c,d`,

\[
\boxed{
(a\lor b)\oplus((a\oplus c)\lor(b\oplus d))
=c\oplus d\oplus ad\oplus bc\oplus cd.
}
\]

This follows immediately from the algebraic-normal form `a OR b = a+b+ab` over `GF(2)`.

## Exact square-map recurrence

For `r>=4`, put

\[
a=x_{r-1},\quad b=x_{r-2},\quad
c=x_{r-2}\lor x_{r-3},\quad
d=x_{r-3}\lor x_{r-4}.
\]

The first step changes the two inputs of `f_r` by `c` and `d`, respectively. Therefore

\[
T_R^2(x)_r=x_r\oplus h_r(x),
\]

where

\[
\boxed{
h_r=c\oplus d\oplus x_{r-1}d\oplus x_{r-2}c\oplus cd.}
\]

Equivalently,

\[
\boxed{
\begin{aligned}
h_r={}&(x_{r-2}\lor x_{r-3})\oplus(x_{r-3}\lor x_{r-4})\\
&\oplus x_{r-1}(x_{r-3}\lor x_{r-4})\\
&\oplus x_{r-2}(x_{r-2}\lor x_{r-3})\\
&\oplus (x_{r-2}\lor x_{r-3})(x_{r-3}\lor x_{r-4}).
\end{aligned}}
\]

The boundary coordinates `r<4` are obtained directly from the same update rule with the special formulas for coordinates 0 and 1.

## Structural consequence

The square map is still triangular and still has the form

\[
T_R^2(x)_r=x_r\oplus h_r(x_0,\ldots,x_{r-1}),
\]

but its forcing is no longer the original two-neighbor OR. One squaring expands the local forcing window from two lower coordinates to four lower coordinates and raises its algebraic complexity.

This is useful mainly as a negative result about the route proposed in run 228: repeated squaring does **not** obviously close inside the original Rule-30 edge recurrence family. Any recursion for `p_R` based on repeated squaring must track an enlarging class of Boolean forcing functions, rather than simply replacing `T` by a smaller copy of itself.

## Connection to run 228

Run 228 gave

\[
p_R(x)=\bigoplus_{j=0}^{O_R/2-1} f_R(T_R^{2j}x).
\]

Thus the sampled states evolve under `T_R^2`, while the sampled observable remains `f_R`. The formula above makes that square dynamics exact. It also shows why a naive self-similarity argument is unavailable: the square dynamics has a four-coordinate forcing polynomial `h_r`, not the original `x_{r-1} OR x_{r-2}`.

## Next target

Do not assume repeated squaring preserves the original local form. A better target is to exploit the proven order filtration directly: for a power `2^q`, coordinates whose automaton order divides `2^q` are frozen by `T_R^{2^q}`. Analyze the first coordinate above that frozen prefix as a one-bit skew extension. This may yield a recursive description indexed by the order exponent `m_r=v_2(O_r)` without tracking the full expanding square-map polynomial.