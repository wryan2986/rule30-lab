# One-bit extension theorem for finite A-cycles

Status: exact structural theorem. Problem 1 remains open, but uniqueness/power-of-two periodicity is reduced to one explicit parity obstruction.

## Setup

Recall

\[
A(x)=T(x)\gg2,
\qquad
(Ax)_i=x_{i+2}\oplus(x_{i+1}\lor x_i).
\]

For an `n`-bit word `x`, write

\[
u=x\gg1,\qquad b=x_0,\qquad x=2u+b.
\]

The upper `n-1` bits evolve independently of the new low bit:

\[
A(x)\gg1=A(u).
\]

Indeed, for every `i>=1`, coordinate `(Ax)_i` depends only on `x_i,x_{i+1},x_{i+2}`, hence only on `u`.

The new low bit obeys the exact skew-product rule

\[
\boxed{b'=u_1\oplus(u_0\lor b).}
\]

Equivalently,

\[
b'=\begin{cases}
1\oplus u_1,&u_0=1,\\
b\oplus u_1,&u_0=0.
\end{cases}
\]

Thus a parent row with low bit `1` is a **reset row**: the child low bit after that step is independent of its previous value. A parent row with low bit `0` transports the child bit bijectively, possibly toggling it according to `u_1`.

## Exact cycle lifting theorem

Let

\[
C=(u^{(0)},u^{(1)},\ldots,u^{(p-1)})
\]

be a parent cycle of exact period `p` under `A`. Consider all `n`-bit states whose quotient by 2 lies on `C`.

### Case 1: the parent cycle contains a reset row

If

\[
(u^{(j)})_0=1
\]

for at least one phase `j`, then the `p`-step return map on the added bit `b` is constant, because composition contains a constant/reset map.

Therefore exactly one of the two lifts over each parent phase lies on a periodic orbit. The lifted periodic orbit is unique and has exact period `p`.

Moreover, any two lifts over the same parent trajectory synchronize no later than the first reset row.

### Case 2: the parent cycle has no reset row

Suppose

\[
(u^{(j)})_0=0\quad\text{for every }j.
\]

Then every fiber map is

\[
b\mapsto b\oplus (u^{(j)})_1.
\]

After one parent period,

\[
\boxed{b\mapsto b\oplus S(C)},
\qquad
S(C)=\bigoplus_{j=0}^{p-1}(u^{(j)})_1.
\]

Hence there are exactly two possibilities:

- If `S(C)=1`, the two lifts are exchanged after `p` steps and together form **one cycle of exact period `2p`**.
- If `S(C)=0`, each lift returns to itself after `p` steps and there are **two distinct cycles of exact period `p`**.

This classification is exhaustive.

## Consequence for the run-37 uniqueness/power-of-two conjecture

Run 37 observed exactly one periodic orbit at every bitlength through 400, with periods

\[
1,2,4,8
\]

on the intervals `1..3`, `4..8`, `9..29`, `30..400`.

The theorem above explains exactly how such a pattern can propagate one bitlength at a time.

Assume the `(n-1)`-bit system has one cycle of period `p`. Then the `n`-bit system has:

1. one cycle of period `p` if the parent cycle contains a state with LSB 1;
2. one cycle of period `2p` if the parent LSB is identically 0 and `S(C)=1`;
3. two cycles of period `p` if the parent LSB is identically 0 and `S(C)=0`.

Therefore the entire conjecture

> every bitlength has exactly one periodic orbit, and its period is a power of two

reduces inductively to ruling out one explicit bad event:

\[
\boxed{
(u^{(j)})_0=0\ \forall j
\quad\text{and}\quad
\bigoplus_j (u^{(j)})_1=0.
}
\]

If this bad event never occurs on the unique parent cycle, uniqueness follows for every bitlength. Starting from the one-bit fixed point, every period can then only stay unchanged or double, so every exact period is automatically a power of two.

This is substantially sharper than a generic highest-disagreement contraction argument: the only failure of synchronization is now identified exactly.

## Threshold interpretation

A period-doubling threshold occurs precisely when the unique parent cycle has

\[
u_0\equiv0
\]

throughout the cycle and

\[
S(C)=1.
\]

Thus the observed threshold starts `4,9,30,401` are exactly lengths one greater than parent cycles where the LSB never becomes 1 and the XOR parity of the next bit is odd.

This gives a concrete target for explaining the threshold sequence: characterize the bit-column parity vector of the unique cycle, rather than enumerate `Fix(A^16)`.

## Remaining blocker

The missing theorem is now precise:

> For every finite A-cycle whose LSB is identically zero, prove that the XOR over one exact period of bit 1 equals 1.

A counterexample would immediately produce two periodic orbits at the next bitlength and disprove the run-37 uniqueness conjecture. A proof would establish, by induction from bitlength 1, both uniqueness of the periodic orbit at every bitlength and the power-of-two exact-period theorem.

The next run should attack this parity statement using the coordinate recurrence on a periodic spacetime cylinder. In particular, when `u_0=0` throughout a cycle, the bit-0 recurrence itself forces `u_2=u_1` phasewise; XORing the bit-1 and higher coordinate recurrences over a full period may propagate parity constraints upward and potentially force `S(C)=1` from the fixed leading `1` boundary.