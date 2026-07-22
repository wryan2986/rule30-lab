# Whole-tail equivalence and the right-edge recurrence

Status: complete informal proof of the stated equivalences and finite-coordinate
period bound. This does not prove Rule 30 center nonperiodicity.

## Setup

Write the Rule 30 local map as

\[
f(a,b,c)=a\mathbin{\oplus}(b\lor c).
\]

Let \(C=(c_t)_{t\geq0}\) be any infinite binary trace with \(c_0=1\).
Force the initial cells at positive coordinates to zero and use
left-permutive inversion to reconstruct

\[
L(C)=(\ell_d)_{d\geq1},\qquad \ell_d=x_{-d}(0).
\]

Define the associated initial configuration \(x^C\) by

\[
x^C_j=
\begin{cases}
0,&j>0,\\
1,&j=0,\\
\ell_{-j},&j<0.
\end{cases}
\]

## Infinite reconstruction is legitimate

For each horizon \(H\), finite sideways inversion reconstructs exactly
\(\ell_1,\ldots,\ell_H\), and its finite round-trip theorem says that forward
evolution has center prefix \(c_0,\ldots,c_H\). These finite reconstructions
are prefix-consistent: increasing the horizon cannot change a previously
reconstructed initial cell.

Fix any time \(t\) and apply the finite theorem with \(H=t\). The center at
time \(t\) depends only on the finite initial causal cone, so the same equality
holds in the infinite configuration \(x^C\):

\[
F^t(x^C)_0=c_t.
\]

Thus \(C\) is the complete center trace of \(x^C\). The same finite inversion
also proves uniqueness among configurations with the supplied zero right
half-line.

## Whole-tail equivalence

The reconstructed tail \(L(C)\) is eventually zero if and only if \(x^C\) has
finite support. Because \(x^C_0=1\) and every positive coordinate is zero,
coordinate zero is then its rightmost nonzero cell.

Conversely, let \(x\) be any finite-support binary configuration whose
rightmost nonzero cell is at coordinate zero. Its center trace starts with one.
Finite sideways inversion of every center prefix uniquely recovers
\(x_{-1},x_{-2},\ldots\), which is eventually zero.

Therefore the focused whole-tail conjecture is equivalent to the following
uniform statement:

> For every finite-support Rule 30 configuration whose rightmost one is at
> coordinate zero, the temporal trace at coordinate zero is not eventually
> periodic.

This is a genuine strengthening in quantifier scope of the prize problem's
single seed, not a reduction to an already finite-state question.

## Exact right-edge moving frame

For such a finite configuration, define

\[
s_{t,k}=F^t(x)_{t-k}\quad(k\geq0),
\qquad
S_t=\sum_{k\geq0}s_{t,k}2^k.
\]

The sum is finite at every finite time. The rightmost cell remains one and
moves one coordinate right per step: the induction step is
\(f(1,0,0)=1\), while finite propagation leaves every cell farther right
zero. Hence \(s_{t,0}=1\).

With the conventions \(s_{t,-1}=s_{t,-2}=0\), the local rule gives

\[
s_{t+1,k}
=f(s_{t,k},s_{t,k-1},s_{t,k-2})
=s_{t,k}\mathbin{\oplus}(s_{t,k-1}\lor s_{t,k-2}).
\]

Equivalently, for nonnegative integers,

\[
S_{t+1}=T(S_t)
=S_t\mathbin{\mathtt{xor}}
 \bigl((S_t\ll1)\mathbin{\mathtt{or}}(S_t\ll2)\bigr).
\]

The fixed spatial center lies \(t\) places behind the moving right edge, so

\[
F^t(x)_0=s_{t,t}=\operatorname{bit}_t(T^t(S_0)).
\]

Every finite initial configuration in the equivalence corresponds uniquely to
an odd positive integer \(S_0\), and every odd positive integer gives one.
Consequently, the focused conjecture is also equivalent to

\[
\forall S\text{ odd and positive},\quad
\bigl(\operatorname{bit}_t(T^t(S))\bigr)_{t\geq0}
\text{ is not eventually periodic}.
\]

The original prize instance is only \(S=1\).

## Fixed coordinates are periodic, but the diagonal is not controlled

For every initial \(S\), bit zero of \(T^t(S)\) is fixed. Inductively assume
bits below \(k\) have periods dividing \(2^0,\ldots,2^{k-1}\). Bit \(k\)
is toggled by the periodic driver

\[
\operatorname{bit}_{k-1}(T^t(S))
\lor
\operatorname{bit}_{k-2}(T^t(S)),
\]

whose period divides \(2^{k-1}\). Over one driver period, bit \(k\) either
returns to its starting value or flips; in the latter case a second driver
period returns it. Thus bit \(k\) has a period dividing \(2^k\). In particular,
for every \(m\geq1\),

\[
T^{2^{m-1}}(S)\equiv S\pmod {2^m}.
\]

This recovers the power-of-two periodicity of every fixed right-edge diagonal.
It does not settle the center sequence because the observed coordinate grows
with time: at time \(t\), the center samples bit \(t\), not any fixed bit.

## Research consequence

Larger finite terminal-zero searches cannot by themselves bridge this moving
diagonal. A useful continuation must exploit the interaction between a claimed
temporal period and the recursively periodic fixed coordinates, or derive a
new obstruction specific to an eventually-zero initial tail. The congruence
above alone supplies neither.
