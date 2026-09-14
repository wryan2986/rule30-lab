# Problem 1: three-bit reduction of the commutator automaton and an exact memory obstruction

Status: exact simplification of the run-20 automaton; identifies both a synchronizing source symbol and a sharp obstruction to suffix-only compression. Problem 1 remains open.

## Setup

Use

\[
T(x)=x\oplus((2x)\lor(4x)),\qquad A(x)=T(x)\gg2.
\]

For a physical row `x`, let

\[
u_j=A^j(x),\qquad s_j=T(u_j),
\]

and compare the normalized orbit of `Tx` with the physical image of the normalized orbit of `x` via

\[
d_j=A^j(Tx)\oplus T(A^j x).
\]

The previous note proved that `d_j<4` and that

\[
d_{j+1}=F(d_j,s_j),
\]

where

\[
F(d,s)=A(s\oplus d)\oplus A(s)\oplus c(s),
\]

with

\[
c(s)=(s_0\lor s_1)+2(s_1\land\neg s_2).
\]

It was stated there that `F` needed `s mod 16`. The exact dependency is smaller.

## 1. Exact Boolean recurrence

Write the two bits of the discrepancy as

\[
d=a+2b,
\]

and write the low three source bits as

\[
s_0=x,\qquad s_1=y,\qquad s_2=z.
\]

A direct bit calculation gives

\[
\boxed{
 a'=(a\oplus x)\lor(b\oplus y)
}
\]

and

\[
\boxed{
 b'=(b\oplus y)\land\neg z.
}
\]

Therefore

\[
\boxed{F(d,s)\text{ depends only on }s\bmod8.}
\]

No fourth source bit is needed.

Equivalently, putting `r=s mod 4`, the transition has the following very compact form:

\[
\boxed{
F(d,s)=
\begin{cases}
0,&d=r,\\
3,&d_1\ne r_1\text{ and }s_2=0,\\
1,&\text{otherwise.}
\end{cases}}
\]

The first case follows because `a'=0` iff both discrepancy bits match the two discarded source bits. If there is a mismatch then `a'=1`; the high output bit survives precisely when the high discrepancy bit mismatches the high discarded bit and source bit 2 is zero.

## 2. State 2 is impossible

The Boolean recurrence immediately gives

\[
b'=1\Longrightarrow b\oplus y=1\Longrightarrow a'=1.
\]

Hence the output can never be binary `10`:

\[
\boxed{F(d,s)\ne2\quad\text{for every }d<4,s.}
\]

Since `d_0=0`, the actual commutator automaton lives on only three states:

\[
\boxed{d_j\in\{0,1,3\}.}
\]

Thus the four-state description from run 20 can be reduced to a three-state automaton driven by a three-bit alphabet.

## 3. Complete transition table on the reachable states

For source symbol `q=s mod 8`, the image of states `(0,1,3)` is

| q | 0 | 1 | 3 |
|---:|---:|---:|---:|
| 0 | 0 | 1 | 3 |
| 1 | 1 | 0 | 3 |
| 2 | 3 | 3 | 1 |
| 3 | 3 | 3 | 0 |
| 4 | 0 | 1 | 1 |
| 5 | 1 | 0 | 1 |
| 6 | 1 | 1 | 1 |
| 7 | 1 | 1 | 0 |

Two entries are structurally important.

### Source 6 is a synchronizing reset

For `s mod 8 = 6`,

\[
\boxed{F(d,s)=1\quad\text{for all reachable }d.}
\]

Therefore any occurrence of source symbol 6 erases the entire earlier commutator history. After the last such symbol, `d_p` is determined solely by the suffix following it.

### Source 0 is exactly the identity

For `s mod 8 = 0`,

\[
\boxed{F(d,s)=d\quad\text{for }d\in\{0,1,3\}.}
\]

Hence arbitrarily many trailing zero symbols preserve whatever memory was present before them.

## 4. Interpretation in normalized-orbit coordinates

Because

\[
s_j=T(u_j)=4u_{j+1}+r_j,
\]

where `r_j=s_j mod 4` is exactly the two-bit remainder discarded by normalization, source bit 2 is simply the parity of the next normalized state:

\[
(s_j)_2=(u_{j+1})_0.
\]

Thus the recurrence can be written without referring to an arbitrary three-bit source word:

\[
\boxed{
 d_{j+1}=0\iff d_j=r_j,
}
\]

and, when `d_j != r_j`,

\[
\boxed{
 d_{j+1}=3
 \iff
 (d_j)_1\ne(r_j)_1
 \text{ and }u_{j+1}\text{ is even},
}
\]

with output `1` in all remaining mismatch cases.

So the commutator state is comparing its current two-bit memory against the actual two bits discarded at each normalized Rule-30 step, with the parity of the next normalized row deciding whether a high-bit mismatch persists.

## 5. Exact obstruction to an automaton-only bounded-suffix theorem

The run-20 handoff asked whether `d_p` might be computable from a bounded suffix of the source word, independently of `p`.

The abstract commutator automaton itself cannot imply such a theorem.

For any `k>=1`, append `k` source symbols congruent to zero modulo 8. Since each zero symbol acts as the identity, two histories reaching distinct states before that suffix remain distinct after the entire common length-`k` suffix.

Therefore:

> **Memory obstruction.** No bound `k` exists such that the terminal state of every source word accepted by the abstract automaton is determined by its last `k` source symbols.

This does **not** yet prove that actual return-fringe collision histories require unbounded memory, because their source words are not arbitrary. It proves something narrower and useful: any bounded-suffix result must use a genuine geometric/dynamical restriction on collision-state source words. It cannot come from the finite automaton alone.

The source symbol `0` has a concrete orbit meaning. Since the triangular map `T mod 8` is a permutation and

\[
T(u)\equiv0\pmod8\iff u\equiv0\pmod8,
\]

a zero source symbol is exactly a normalized-orbit state divisible by 8. Thus the remaining question is whether actual return-fringe/common-origin collision histories can contain arbitrarily long terminal blocks of normalized states divisible by 8, or whether FULL/global-front structure bounds such blocks.

## 6. Research consequence

The source-history problem is now sharper:

1. The commutator memory has only three reachable states, not four.
2. Only three source bits per normalized step are needed.
3. A source symbol `6` resets all prior history to state `1`.
4. A source symbol `0` preserves all prior history exactly.
5. Therefore any proof that collision states have bounded commutator memory should target the **last occurrence of source 6**, or prove that long terminal runs avoiding synchronizing words (especially runs of source 0) are incompatible with return-fringe/common-origin geometry.

A particularly concrete next target is to classify terminal source words of genuine boundary-collision states and determine whether long corridors force a `6 mod 8` source symbol near the end of the normalized `p`-orbit. Failing that, construct genuine collision states with arbitrarily long terminal zero-source runs; such a family would rule out bounded-suffix compression even after imposing the collision geometry.
