# Problem 1: exact commutator boundary formula and four-bit fringe core

Status: exact structural theorem. Problem 1 remains open.

## Setup

Let

\[
T(x)=x\oplus((2x)\lor(4x)),\qquad A(x)=T(x)\gg2.
\]

For a bit position `i`, write `x_i` for bit `i`, with negative-index bits zero. Then

\[
(Tx)_i=x_i\oplus(x_{i-1}\lor x_{i-2}).
\]

The earlier commutator notes defined

\[
d_k(x):=A^k(Tx)\oplus T(A^k x),
\]

and proved indirectly that `d_k(x)` always lies in `{0,1,3}`. The run-27 fringe-core state is exactly `C_n(R)=d_(n-1)(y_R)` for a particular physical preimage `y_R` of the return fringe.

This note gives a closed form for `d_k(x)` and therefore an exact four-bit formula for `C_n(R)`.

## 1. Quotient commutator for one Rule-30 step

For every integer `Y>=0` and every `h>=2`, define

\[
Q_h(Y):=(T(Y)\gg h)\oplus T(Y\gg h).
\]

All quotient bits at positions `j>=2` agree. Indeed, output bit `h+j` of `T(Y)` depends only on input bits `h+j,h+j-1,h+j-2`, all of which lie at or above the quotient boundary when `j>=2`.

Only quotient bits `0` and `1` can differ. Put

\[
a=Y_{h-2},\qquad b=Y_{h-1},\qquad q=Y_h.
\]

For quotient bit zero,

\[
(TY)_h\oplus (T(Y\gg h))_0
=(q\oplus(b\lor a))\oplus q
=a\lor b.
\]

For quotient bit one,

\[
\begin{aligned}
(TY)_{h+1}\oplus (T(Y\gg h))_1
&=[Y_{h+1}\oplus(q\lor b)]\oplus[Y_{h+1}\oplus q]\\
&=b\land\neg q.
\end{aligned}
\]

Hence

\[
\boxed{
Q_h(Y)=(a\lor b)+2(b\land\neg q).
}
\]

Define the three-bit boundary function

\[
\boxed{
c(s)=(s_0\lor s_1)+2(s_1\land\neg s_2).}
\]

Then the quotient identity is

\[
\boxed{
(T(Y)\gg h)\oplus T(Y\gg h)
=c\!\left((Y\gg(h-2))\bmod 8\right).
}
\]

In particular the discrepancy is always in `{0,1,3}`.

## 2. Normalized iterates are physical iterates followed by one final quotient

For every `k>=0`,

\[
\boxed{A^k(x)=T^k(x)\gg 2k.}
\]

Proof is by induction. The claim is trivial for `k=0`. Suppose it holds for `k`, put `Y=T^k(x)`, and apply the quotient identity with `h=2k` (the case `k=0` is just the definition of `A`). It says

\[
T(Y\gg2k)=(T(Y)\gg2k)\oplus e,
\qquad e<4.
\]

After shifting right by two, the error disappears:

\[
\begin{aligned}
A^{k+1}(x)
&=T(A^k x)\gg2\\
&=T(Y\gg2k)\gg2\\
&=T(Y)\gg(2k+2)\\
&=T^{k+1}(x)\gg2(k+1).
\end{aligned}
\]

So intermediate normalization does not alter the final normalized row; it only discards information that lies outside the future normalized light cone.

## 3. Closed form for the `k`-step commutator

For `k>=1`, put `Y=T^k(x)`. By the previous theorem,

\[
A^k(Tx)=T^{k+1}(x)\gg2k=T(Y)\gg2k
\]

and

\[
T(A^k x)=T(Y\gg2k).
\]

Applying the quotient identity at `h=2k` gives

\[
\boxed{
d_k(x)=c\!\left((T^k(x)\gg(2k-2))\bmod8\right).}
\]

This replaces the length-`k` three-state commutator automaton by a direct local formula: the entire accumulated commutator is determined by exactly three physical bits at the moving normalization boundary of `T^k(x)`.

The earlier automaton recurrence is therefore a streaming implementation of this boundary formula, not a genuinely history-dependent state machine.

## 4. Exact four-bit formula for the run-27 fringe core

Now take an even-length nonzero fringe `R` with

\[
L=\operatorname{bitlength}(R)=2n\ge4
\]

and define, as in run 27,

\[
y_R=T^{1-n}(R)\pmod{2^{2n}}.
\]

The fringe-core state is

\[
C_n(R)=d_{n-1}(y_R).
\]

Because `T` is bijective modulo `2^(2n)`,

\[
T^{n-1}(y_R)\equiv R\pmod{2^{2n}}.
\]

The closed commutator formula only reads physical positions

\[
2(n-1)-2=2n-4,\quad2n-3,\quad2n-2,
\]

all below position `2n`. Therefore the congruence is sufficient and

\[
\boxed{
C_n(R)=c\!\left((R\gg(2n-4))\bmod8\right).
}
\]

Thus **the fringe core depends only on the top four bits of `R`**, for every even fringe length, with no admissibility assumption.

If the leading four-bit nibble is `h`, the complete table is

| top four bits of `R` | `C_n(R)` |
|---|---:|
| `1000` | 0 |
| `1001` | 1 |
| `1010` | 3 |
| `1011` | 3 |
| `1100` | 0 |
| `1101` | 1 |
| `1110` | 1 |
| `1111` | 1 |

In particular, for the exceptional `11`-leading long-even corridors isolated in runs 25-27,

\[
\boxed{
C_n(R)=
\begin{cases}
0,&R\text{ begins }1100,\\
1,&R\text{ begins }1101,1110,\text{ or }1111.
\end{cases}
}
\]

The empirical period-eight split from run 27 is therefore universal; it was not a period-eight or admissibility phenomenon.

## 5. Final commutator classification for every long-even collision

Retain the run-27 notation

\[
G=2D\ge4.
\]

For `11`-leading fringes, run 27 proved

\[
d_p=\mathbf1_{C_n(R)\ne1}\oplus(D\bmod2).
\]

Substituting the exact four-bit formula gives

\[
\boxed{
R\text{ begins }1100
\implies d_p=1\oplus(D\bmod2),
}
\]

while

\[
\boxed{
R\text{ begins }1101,1110,\text{ or }1111
\implies d_p=D\bmod2.
}
\]

For `10`-leading fringes, the previous synchronizer result already gave

\[
\boxed{d_p=1\oplus(D\bmod2).}
\]

Therefore **every genuine long-even collision has its final commutator state determined by only `D mod 2` and the leading four bits of `R`**. There is no residual unbounded commutator-memory obstruction.

Equivalently, the `10xx` and `1100` classes share one parity branch, while `1101`, `1110`, and `1111` share the other.

## 6. Research consequence

Runs 20-27 progressively compressed the commutator history from a length-`p` source word, to a three-state automaton, to a fringe-core function. The exact quotient formula closes that line completely:

- the automaton state is just a local physical boundary defect;
- the run-27 core reads only three bits from the top four bits of `R`;
- the long-even collision state `d_p` is bounded data, independent of `p` and the interior of the fringe.

This does **not** by itself solve Problem 1. The next useful target is to feed the now-explicit odd/even collision classification into the existing re-entry/FULL/residence-growth machinery. In particular, the local-memory route should no longer spend effort trying to classify deeper fringe information: the commutator contribution is already completely classified.