# Problem 1: exact two-bit commutator automaton and immediate-reentry classifier

Status: proved exact finite-state transport identity. Problem 1 remains open.

## Setup

Use

\[
T(x)=x\oplus((2x)\lor(4x)),\qquad A(x)=T(x)\gg2.
\]

The previous note proved the one-step commutator

\[
A(Tx)=T(Ax)\oplus c(Tx),
\]

where

\[
c(s)=(s_0\lor s_1)+2(s_1\land\neg s_2)\in\{0,1,3\}.
\]

For a fixed return length \(p\), define the physical-return defect

\[
E_p(x):=A^p(x)\oplus x.
\]

The open question was whether augmenting \(E_p\) by a small amount of source/phase information yields an exact recurrence under one physical step \(x\mapsto T(x)\).

It does.

## 1. A two-bit discrepancy automaton

Let

\[
u_j=A^j(x),\qquad v_j=A^j(Tx),
\]

and define

\[
d_j:=v_j\oplus T(u_j).
\]

Initially \(d_0=0\).

Claim: for every \(j\ge0\),

\[
\boxed{d_j<4}.
\]

Indeed, suppose \(d_j<4\). Put \(s_j=T(u_j)\). Then

\[
\begin{aligned}
d_{j+1}
&=A(v_j)\oplus T(Au_j)\\
&=A(s_j\oplus d_j)\oplus T(Au_j)\\
&=\bigl(A(s_j\oplus d_j)\oplus A(s_j)\bigr)\oplus c(s_j).
\end{aligned}
\]

Since \(d_j\) changes only input bits 0 and 1, and output bit \(i\) of \(A\) depends only on input bits \(i,i+1,i+2\), the difference

\[
A(s_j\oplus d_j)\oplus A(s_j)
\]

is also supported only in bits 0 and 1. The same is true of \(c(s_j)\). Hence \(d_{j+1}<4\).

Thus the exact recurrence is

\[
\boxed{
 d_{j+1}=F(d_j,s_j\bmod16)
}
\]

with

\[
\boxed{
F(d,s)=A(s\oplus d)\oplus A(s)\oplus c(s),
\qquad d\in\{0,1,2,3\}.
}
\]

Only the four low bits of \(s_j=T(A^j x)\) are needed because the low two bits of \(A(s_j\oplus d_j)\oplus A(s_j)\) depend only on input bits 0 through 3.

Therefore a \(p\)-step near-return can be transported one physical Rule-30 step using a four-state discrepancy automaton driven by the sequence

\[
T(x)\bmod16,\ T(Ax)\bmod16,\ldots,\ T(A^{p-1}x)\bmod16.
\]

This is an exact finite-state source-history description; no unbounded defect support is generated inside the commutator bookkeeping.

## 2. Exact update formula for the p-step defect

At \(j=p\),

\[
A^p(Tx)=T(A^p x)\oplus d_p.
\]

Since \(A^p x=x\oplus E_p(x)\),

\[
\boxed{
E_p(Tx)
=
T(x\oplus E_p(x))\oplus T(x)\oplus d_p.
}
\]

This separates the next defect into two pieces:

1. the direct physical image of the old defect,
2. a two-bit source correction \(d_p\) obtained from the four-state automaton above.

The previous counterexamples are therefore not arbitrary phase effects: all missing information is compressed into the two-bit terminal state \(d_p\), driven by the low-four-bit source word along the normalized \(p\)-orbit.

## 3. Exact immediate-reentry criterion for boundary defect 1

Suppose

\[
E_p(x)=1.
\]

Direct evaluation of Rule 30 gives

\[
T(x\oplus1)\oplus T(x)
=
\begin{cases}
3,&x_1=1,\\
7,&x_1=0.
\end{cases}
\]

Because \(d_p<4\), exact re-entry

\[
E_p(Tx)=0
\]

is possible iff the direct defect is 3 and \(d_p=3\). Hence

\[
\boxed{
E_p(x)=1\ \Longrightarrow\
E_p(Tx)=0
\iff
x_1=1\text{ and }d_p=3.
}
\]

This distinguishes the two known examples exactly:

- \(x=455503\): \(x_1=1\), terminal automaton state \(d_4=3\), so re-entry occurs;
- \(x=401\): \(x_1=0\), so re-entry is impossible even though \(d_2=3\); indeed the next defect is 4.

## 4. Exact immediate-reentry criterion for boundary defect 3

Suppose

\[
E_p(x)=3.
\]

For the low three bits of \(x\), direct evaluation gives

\[
T(x\oplus3)\oplus T(x)\in\{1,5,9,13\}.
\]

The value is 1 exactly when

\[
\boxed{x_2=1\quad\text{and}\quad x_0\oplus x_1=1.}
\]

Since \(d_p<4\), re-entry requires the direct defect itself to be 1 and \(d_p=1\). Therefore

\[
\boxed{
E_p(x)=3\ \Longrightarrow\
E_p(Tx)=0
\iff
x_2=1,\ x_0\oplus x_1=1,\ d_p=1.
}
\]

Again this classifies the known examples:

- \(x=3282734\): low bits satisfy \(x_2=1\) and \(x_0\oplus x_1=1\), with \(d_4=1\), so re-entry occurs;
- \(x=802\): the direct physical defect is 9 and \(d_2=0\), so re-entry does not occur.

## 5. Consequence for the proof strategy

The augmented-state proposal from the previous handoff is viable in a precise sense: the noncommutation of \(A^p\) with one physical \(T\)-step is governed by a four-state automaton, not by an expanding error word.

However, the driver is the low-four-bit source sequence along the entire normalized \(p\)-orbit. Thus this result does not yet give a state space whose size is independent of \(p\) unless that source word can itself be constrained by the return-fringe/common-origin structure.

The next useful target is therefore sharply defined:

- specialize the source sequence \(T(A^j x)\bmod16\) to actual return-fringe collision states;
- determine whether the corridor geometry forces the terminal automaton state \(d_p\), or restricts it to a proper subset;
- if so, test whether repeated long corridors require incompatible or non-reusable source words for the same fixed physical seed.

The important positive result is that all commutator memory needed after reading that source word is only two bits.
