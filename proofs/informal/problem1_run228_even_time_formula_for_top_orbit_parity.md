# Problem 1 run 228 — even-time formula for top-coordinate orbit parity

Problem 1 remains open.

## Setup

Use the near-edge triangular automata from runs 223–227. Let `T_R` act on coordinates `x_0,...,x_R`, let its order be `O_R`, and for `R>=2` write the top-coordinate update as

\[
x_R(t+1)=x_R(t)\oplus f_R(t),\qquad
f_R(t)=x_{R-1}(t)\lor x_{R-2}(t).
\]

Run 224 proved `O_R` is an even power of two for `R>=1`. Define

\[
p_R(x)=\bigoplus_{t=0}^{O_R-1}x_R(t).
\]

Run 227 proved that `p_R` is independent of the initial top bit. The following gives an explicit lower-width formula for it.

## Theorem: p_R is the even-time cocycle parity

For every `R>=2`,

\[
\boxed{
 p_R(x)=\bigoplus_{\substack{0\le s\le O_R-2\\ s\text{ even}}}
 \bigl(x_{R-1}(s)\lor x_{R-2}(s)\bigr).
}
\]

Equivalently, because `O_R` is even,

\[
\boxed{
 p_R(x)=\bigoplus_{j=0}^{O_R/2-1} f_R(T_R^{2j}x).
}
\]

The right side depends only on the width-`R-1` projection, so this also reproves the descent result of run 227 constructively.

### Proof

Iterating the one-bit skew recurrence gives

\[
x_R(t)=x_R(0)\oplus\bigoplus_{s=0}^{t-1}f_R(s).
\]

XOR this for `t=0,...,O_R-1`. The initial bit occurs `O_R` times and cancels because `O_R` is even. A fixed forcing term `f_R(s)` occurs in the summands for `t=s+1,...,O_R-1`, hence exactly `O_R-1-s` times. Modulo two, since `O_R` is even,

\[
O_R-1-s\equiv1-s\pmod2,
\]

which is odd exactly when `s` is even. Therefore only the even-time forcing terms survive. QED.

## Interpretation

The observable `p_R` is not an arbitrary descended Boolean function. It is a parity accumulated along the even-time subsequence of the lower triangular dynamics. Thus the next recursion target should be the dynamics of `T_{R-1}^2`, rather than coordinate derivatives of an opaque truth table.

If `O_R=O_{R-1}` (the preceding extension did not double), the formula samples exactly half of one lower-width period. If `O_R=2O_{R-1}`, it samples `O_{R-1}` even-time positions across two lower periods. The distinction suggests analyzing how the lower orbit decomposes under the square map `T_{R-1}^2`.

## Useful companion identity

The full cocycle parity over the same interval is

\[
\bigoplus_{s=0}^{O_R-1}f_R(s),
\]

while `p_R` is its even-time half. Hence the odd-time half is the XOR of the full cocycle parity and `p_R`. This isolates precisely what information was lost in the telescoping identity recorded as a dead end in run 227: telescoping sees only even XOR odd, whereas `p_R` retains one parity class separately.

## Status

This is an all-depth identity. It does not yet bound `m_R=v_2(O_R)`, but it replaces the proposed successive-coordinate-derivative search with a more structured square-map problem. The next run should analyze `T_R^2` explicitly, especially whether its triangular forcing admits a similar two-step formula that recursively expresses `p_R` in lower-depth cocycles.
