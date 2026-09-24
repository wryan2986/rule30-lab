# Problem 1 — run 233: exact block formula for descended even-time parity

Problem 1 remains open.

## Setup

Continue runs 228–232. For a coordinate `r`, write its lower forcing as

\[
f_r(t)=x_{r-1}(t)\lor x_{r-2}(t),
\qquad x_r(t+1)=x_r(t)\oplus f_r(t).
\]

Run 232 introduced, with `r=R-2` and `L=O_R`,

\[
H_r^{(R)}(x)=\bigoplus_{j=0}^{L/2-1}x_r(2j),
\]

and showed that a suitable constant-order plateau forces this observable to vanish identically. The proposed next step was to differentiate in the initial bit `e_r`, hoping for a quarter-time parity one coordinate lower.

## First result: the proposed top-bit derivative is identically zero

For `R>=3`,

\[
\boxed{D_{e_r}H_r^{(R)}\equiv0.}
\]

Indeed, flipping only the initial `x_r` leaves every lower coordinate unchanged and hence leaves the forcing `f_r(t)` unchanged. Therefore the two `x_r` trajectories are complementary at every time. Every one of the `L/2` sampled terms toggles. Since `L=O_R` is divisible by `4`, `L/2` is even, so the toggles cancel in XOR.

Thus the most immediate derivative descent suggested at the end of run 232 is a dead end: differentiating `H` in its own coordinate cannot produce a quarter-time parity.

## Theorem: exact 4-block forcing formula

There is nevertheless a clean further dyadic identity. For `R>=3`, `r=R-2`, and `L=O_R`,

\[
\boxed{
H_r^{(R)}(x)
=
\bigoplus_{k=0}^{L/4-1}
\left(f_r(4k)\oplus f_r(4k+1)\right).
}
\]

Equivalently,

\[
\boxed{
H_r^{(R)}
=
\bigoplus_{k=0}^{L/4-1}
\Big[
(x_{r-1}(4k)\lor x_{r-2}(4k))
\oplus
(x_{r-1}(4k+1)\lor x_{r-2}(4k+1))
\Big].
}
\]

### Proof

Expand

\[
x_r(2j)=x_r(0)\oplus\bigoplus_{s=0}^{2j-1}f_r(s)
\]

and XOR over `j=0,...,L/2-1`. The initial bit occurs `L/2` times and cancels because `L/2` is even.

For a fixed forcing time `s`, its multiplicity is the number of sampled even times `2j` satisfying `2j>s`, namely

\[
L/2-1-\lfloor s/2\rfloor
\]

for `0<=s<=L-3`. Since `L/2` is even, this multiplicity is odd exactly when

\[
\lfloor s/2\rfloor\equiv0\pmod2,
\]

i.e. exactly for `s=4k` or `s=4k+1`. These are precisely the terms displayed above.

## Plateau consequence

Whenever the run-232 plateau hypothesis yields

\[
H_r^{(R)}\equiv0,
\]

we therefore obtain the all-state block cancellation

\[
\boxed{
\bigoplus_{k=0}^{L/4-1}
\left(f_r(4k)\oplus f_r(4k+1)\right)=0.
}
\]

This is a stronger description of what the descended cancellation means. It is not a pure quarter-time parity: the next dyadic level naturally becomes a parity of adjacent forcing pairs in each 4-step block.

## Interpretation

The repeated-descent hierarchy is more complicated than the naive pattern

`full orbit -> even times -> quarter times -> ...`.

Already at the next stage, the correct object is a Walsh-like block sum with mask `1100` on each four-step block. This suggests that further expansion should be organized by dyadic time masks rather than by explicit powers of `T` or by repeatedly differentiating the highest available state bit.

A useful next target is to derive the general time-mask recursion for

\[
S_q[y]=\bigoplus_t w_q(t)y(t)
\]

when `y(t+1)=y(t) xor f(t)`, starting from the masks appearing here. If those masks follow a simple Pascal/2-adic recursion, plateau constraints may still descend systematically even though they are not pure subsampling constraints.

## Dead end recorded

Do not retry `D_{e_r}H_r^{(R)}` as a route to quarter-time parity: it vanishes identically for the elementary complementarity reason above. The useful continuation is the dyadic time-mask/block formulation.