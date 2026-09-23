# Problem 1 run 227 — top-coordinate orbit parity descends

Problem 1 remains open.

## Setup

Use the near-edge triangular automata from runs 223–226. Let `T_R` be the width-`R` map on coordinates `x_0,...,x_R`, with order `O_R`. Run 224 proved every `O_R` is a power of two; in particular `O_R` is even for every `R>=1`.

Define the top-coordinate orbit parity

\[
p_R(x)=\bigoplus_{t=0}^{O_R-1} x_R(t),
\]

where `x(t)=T_R^t x`. Let `e_R` flip only coordinate `R`.

## Theorem: top-bit flip invariance of p_R

For every `R>=1` and every state `x`,

\[
\boxed{p_R(x\oplus e_R)=p_R(x).}
\]

### Proof

The triangular recurrence has

\[
x_R(t+1)=x_R(t)\oplus f_R(x_0(t),...,x_{R-1}(t)),
\]

while all lower coordinates evolve independently of `x_R`. Therefore two trajectories starting at `x` and `x\oplus e_R` have identical coordinates below `R` at every time and complementary coordinate `R` at every time:

\[
x_R^{\star}(t)=x_R(t)\oplus1.
\]

Hence

\[
p_R(x\oplus e_R)\oplus p_R(x)
=\bigoplus_{t=0}^{O_R-1}1
=O_R\pmod2.
\]

For `R>=1`, `O_R` is even, so the right side is zero. QED.

## Consequence: p_R is really a lower-width observable

Because `p_R` is invariant under changing the newest bit, it factors through projection to the first `R` coordinates. Thus there exists a Boolean function `\bar p_R` on width `R-1` states such that

\[
\boxed{p_R(x_0,...,x_R)=\bar p_R(x_0,...,x_{R-1}).}
\]

This is useful together with run 226: the attempted `(g_R,p_R)` recursion does not require carrying arbitrary dependence on the newest coordinate. Both the top-flip derivative of `g_R` and `p_R` descend to lower-width orbit data.

## Related telescoping identity

Over a full `T_R` order, XORing the update equation for coordinate `R` gives

\[
0=\bigoplus_{t=0}^{O_R-1}(x_{R-1}(t)\lor x_{R-2}(t))
\]

for `R>=2`. Since the lower-width trajectory repeats `q_R=O_R/O_{R-1}` times, this is

\[
0=(q_R\bmod2)\,g_{R-1}(\pi x).
\]

When `q_R=1`, this forces `g_{R-1}\equiv0`; when `q_R=2`, it is automatic. This is exactly consistent with the run-225 doubling criterion, so it is a consistency identity rather than an independent new restriction. Recording it prevents a future run from mistaking the telescoping equation for additional leverage.

## Small-width diagnostic (finite evidence only)

Direct enumeration gives the following qualitative behavior for `p_R` at small widths: `p_1,p_2` are nonconstant; `p_3,p_4` vanish identically; `p_5` is nonconstant; `p_6,p_7` vanish identically. This does not yet justify a pattern or closed formula.

## Status

The new all-depth content is the factorization of `p_R` through width `R-1`. It narrows the recursion target, but does not by itself bound the growth of `m_R=v_2(O_R)` or solve the moving stopping-frontier problem.
