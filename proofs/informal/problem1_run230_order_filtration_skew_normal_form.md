# Problem 1 — run 230: order-filtration skew normal form

Problem 1 remains open.

## Setup

For the near-edge triangular automaton `T_R`, coordinates satisfy

- `x'_0=x_0`,
- `x'_1=x_1 XOR x_0`,
- `x'_r=x_r XOR (x_{r-1} OR x_{r-2})` for `r>=2`.

Let `O_r=2^{m_r}` be the order of the width-`r` prefix automaton. Earlier runs proved `O_r | O_{r+1}` and `O_{r+1} in {O_r,2O_r}`.

## Theorem: iterate at a prefix order

Fix `s<R` and put `L=O_s`. Then `T_R^L` fixes coordinates `0,...,s` pointwise. Its action on coordinate `s+1` has the exact form

\[
(T_R^Lx)_{s+1}=x_{s+1}\oplus G_s(x_0,\ldots,x_s),
\]

where

\[
G_s(x_0,\ldots,x_s)
=\bigoplus_{t=0}^{L-1}
\bigl(x_s(t)\lor x_{s-1}(t)\bigr).
\]

In particular, `G_s` is independent of `x_{s+1}` and of every higher coordinate.

### Proof

The first `s+1` coordinates form a closed triangular subsystem whose order is `L`, so they return pointwise after `L` steps. At each single step coordinate `s+1` is toggled by `x_s OR x_{s-1}`. XORing those toggles over the `L` steps gives the displayed formula. Triangularity shows that the forcing trajectory depends only on the prefix through coordinate `s`. QED.

## Corollary: exact plateau criterion in the filtration

`O_{s+1}=O_s` iff `G_s` is identically zero on the width-`s` state space; otherwise `O_{s+1}=2O_s`.

This recovers the one-bit extension criterion, but now places it directly inside the order filtration requested by run 229: after advancing by the exact prefix order, all lower coordinates disappear from the dynamics except through one accumulated Boolean forcing observable.

More generally, suppose

\[
m_s=m_{s+1}=\cdots=m_t=q.
\]

Then `T_R^{2^q}` fixes coordinates `0,...,t` pointwise. The first coordinate beyond that plateau satisfies

\[
(T_R^{2^q}x)_{t+1}=x_{t+1}\oplus G_t(x_0,\ldots,x_t).
\]

Thus an entire constant-order plateau can be collapsed before studying the next coordinate; there is no need to carry symbolic formulas for `T^{2^q}` on the frozen prefix.

## What this does and does not achieve

This is an all-depth structural reduction, not a solution. It rigorously validates run 229's proposed filtration route and avoids the polynomial blow-up found in the explicit square-map calculation.

However, by itself it does not bound plateau lengths or prove sublinear growth of `m_R`: the accumulated forcing `G_t` may still be a complicated Boolean function of a growing prefix. The remaining target is therefore precise: find a recursion, invariant, or cancellation law for these prefix-order accumulated forcings `G_t` that does not require enumerating all `2^{t+1}` prefix states.

## Recommended continuation

Study `G_t` under flips of the highest few frozen-prefix coordinates and under projection across a constant-order plateau. In particular, test whether a plateau `m_s=...=m_t=q` forces any systematic derivative vanishing of `G_t`; such a statement would give genuine control of future doubling rather than merely restating the order criterion.
