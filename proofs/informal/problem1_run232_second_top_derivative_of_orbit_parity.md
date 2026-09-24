# Problem 1 — run 232: second-top derivative of orbit parity

Problem 1 remains open.

## Setup

Use the near-edge triangular automata from runs 223–231. For width `R`, let `O_R` be the order and

\[
p_R(x)=\bigoplus_{t=0}^{O_R-1}x_R(t).
\]

Run 228 proved the exact even-time formula

\[
p_R(x)=\bigoplus_{j=0}^{O_R/2-1}
\bigl(x_{R-1}(2j)\lor x_{R-2}(2j)\bigr).
\]

Run 231 showed that a length-three constant-order plateau forces a lower `p` observable to vanish identically. The next question was whether that vanishing itself has a descended consequence.

## Theorem: derivative in the second-highest initial bit

For `R>=3`, define the even-time parity

\[
H_{R-2}^{(R)}(x)=\bigoplus_{j=0}^{O_R/2-1}x_{R-2}(2j).
\]

Then

\[
\boxed{D_{e_{R-1}}p_R(x)=H_{R-2}^{(R)}(x).}
\]

Here `D_e f(x)=f(x)\oplus f(x\oplus e)`.

### Proof

Flip only the initial coordinate `x_{R-1}`. By triangularity, all coordinates below `R-1` evolve identically in the two trajectories, while coordinate `R-1` stays complementary at every time: its update forcing depends only on lower coordinates, which are unchanged.

Apply the run-228 formula to the two trajectories. At each even time, write

\[
a=x_{R-1}(2j),\qquad b=x_{R-2}(2j).
\]

The contribution to the derivative is

\[
(a\lor b)\oplus((a\oplus1)\lor b)=1\oplus b.
\]

Therefore

\[
D_{e_{R-1}}p_R
=\bigoplus_{j=0}^{O_R/2-1}(1\oplus x_{R-2}(2j)).
\]

For `R>=3`, `O_R` is divisible by `4` (the proved order hierarchy plus the base values gives this immediately), so `O_R/2` is even and the constant ones cancel. Hence

\[
D_{e_{R-1}}p_R
=\bigoplus_{j=0}^{O_R/2-1}x_{R-2}(2j),
\]

as claimed.

## Plateau consequence

If a length-three constant-order plateau gives

\[
p_R\equiv0,
\]

then every Boolean derivative of `p_R` vanishes. In particular,

\[
\boxed{H_{R-2}^{(R)}\equiv0.}
\]

Thus the run-231 cancellation descends one step further: it forces an all-state parity cancellation of coordinate `R-2` sampled only at even times over the full width-`R` order horizon.

This is genuinely different from ordinary full-orbit parity. It is naturally an observable of the square map `T^2`, but unlike the abandoned run-229 route, no explicit polynomial expansion of `T^2` is needed.

## Why this matters

A second consecutive non-doubling does not merely force `p_R=0`; it also forces a square-map parity one level lower to vanish. This begins the proposed hierarchy of descended constraints. Repeated coordinate derivatives of the run-228 even-time formula are now a concrete route for testing whether a long order plateau forces successively finer `2^k`-time sampled parity cancellations.

## Computational check

Direct exhaustive/random checks at small widths agree with the identity. No finite computation is used in the proof.

## Remaining obstruction

The identity alone does not yet show that the descended even-time parity is impossible, nor does it bound plateau length. The next useful target is to differentiate `H_{R-2}^{(R)}` in coordinate `e_{R-2}` or derive its analogue from a `T^2` orbit sum, looking for a quarter-time parity at coordinate `R-3`. If the pattern iterates, a plateau can be converted into a hierarchy of dyadically sampled cancellations without expanding `T^{2^k}` explicitly.