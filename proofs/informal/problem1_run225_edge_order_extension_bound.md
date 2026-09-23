# Problem 1 run 225 — one-coordinate edge-order extension bound

## Status

Problem 1 remains open. This note proves an all-depth structural refinement of the run-224 2-adic edge-period hierarchy.

## Setup

For fixed `R`, let

\[
T_R:\{0,1\}^{R+1}\to\{0,1\}^{R+1}
\]

be the near-edge automaton on

\[
(E_0,\dots,E_R),\qquad E_r(k)=d_{2k-r}(k),
\]

with triangular update

\[
E'_0=E_0,\quad E'_1=E_1\oplus E_0,
\]

and for `r>=2`,

\[
E'_r=E_r\oplus(E_{r-1}\lor E_{r-2}).
\]

Write

\[
O_R=\operatorname{ord}(T_R).
\]

Run 224 proved that every `O_R` is a power of two and that `O_R | O_{R+1}`.

## New theorem

For every `R>=0`,

\[
\boxed{O_{R+1}\mid 2O_R.}
\]

Together with the run-224 divisibility relation,

\[
\boxed{O_{R+1}\in\{O_R,2O_R\}.}
\]

Equivalently, if

\[
m_R=v_2(O_R),
\]

then

\[
\boxed{m_{R+1}-m_R\in\{0,1\}.}
\]

So adding one deeper transient coordinate can increase the edge-automaton order by at most one binary digit.

## Proof

Write a width-`R+1` state as `(x,z)`, where

\[
x=(E_0,\dots,E_R)\in\{0,1\}^{R+1},\qquad z=E_{R+1}.
\]

Because the map is triangular, the extension has the skew-product form

\[
T_{R+1}(x,z)=(T_Rx,\ z\oplus f(x))
\]

for a Boolean function `f` of the lower coordinates only. (For the concrete edge map, `f(x)=E_R\lor E_{R-1}` when the new coordinate index is at least 2.)

Iterating `O_R` times gives

\[
T_{R+1}^{O_R}(x,z)
 =\left(x,\ z\oplus \bigoplus_{j=0}^{O_R-1} f(T_R^j x)\right).
\]

Define

\[
g(x)=\bigoplus_{j=0}^{O_R-1} f(T_R^j x).
\]

Thus

\[
T_{R+1}^{O_R}(x,z)=(x,z\oplus g(x)).
\]

The base coordinate `x` is now fixed. Applying the same map a second time toggles the last bit by the same `g(x)` again, hence

\[
T_{R+1}^{2O_R}(x,z)=(x,z\oplus g(x)\oplus g(x))=(x,z).
\]

Therefore `T_{R+1}^{2O_R}=id`, proving

\[
O_{R+1}\mid 2O_R.
\]

Projection onto the first `R+1` coordinates intertwines `T_{R+1}` with `T_R`, so run 224 already gives `O_R|O_{R+1}`. The only positive divisors of `2O_R` divisible by `O_R` are `O_R` and `2O_R`, proving the dichotomy.

## Exact criterion for doubling

The proof gives a useful criterion:

\[
\boxed{O_{R+1}=2O_R}
\]

iff there exists a base state `x` for which

\[
\boxed{g(x)=\bigoplus_{j=0}^{O_R-1} f(T_R^j x)=1.}
\]

Otherwise `g(x)=0` for every `x` and `O_{R+1}=O_R`.

So the unresolved order sequence is reduced to an orbit-parity question for the newly attached Boolean cocycle. This is substantially narrower than classifying the full permutation.

## Finite check

Direct exhaustive enumeration reproduces the run-224 orders through width 16 and extends them two steps:

`R = 0..17`

`O_R = 1,2,2,4,8,8,16,32,32,64,64,64,128,256,256,512,512,1024`.

The enumeration is only finite evidence. The extension theorem and doubling criterion above are all-depth proofs.

## Consequence for the stopping frontier

For

\[
F_n=E_{\Delta_n}(a_{n-1}),
\]

the required time modulus at depth `Delta_n` grows through a nested sequence in which each newly exposed transient layer either leaves the modulus unchanged or doubles it. Thus the transient phase complexity cannot jump faster than one bit per unit increase of depth.

This does not yet bound `m_R`, since repeated doubling can still make it grow linearly with `R`. The next target is to analyze the cocycle parity `g` structurally: identify when extension doubles and whether long runs of forced non-doubling occur. A useful parallel target is to compare `m_{Delta_n}` with the 2-adic valuation/information carried by the stopping times `a_{n-1}`.
