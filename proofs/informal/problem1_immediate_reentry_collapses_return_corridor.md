# Problem 1: immediate re-entry after a long corridor collapses the next same-period corridor

Status: exact theorem for every even corridor `G>=4` and every odd corridor `G>=5`. If the first collision immediately re-enters the same `A^p`-fixed set, the re-entered state's own return corridor has length `0` (even case) or at most `1` (odd case). The exceptional odd case `G=3` is not covered by the leading-edge argument. Problem 1 remains open.

## Setup

Let

\[
T^p(z)=2^{m}z+R,\qquad m=2p,
\]

with positive return corridor

\[
G=m-\operatorname{bitlength}(R)>0,
\qquad D=\lfloor G/2\rfloor.
\]

The first collision row is

\[
x=T^{D+1}(z).
\]

Suppose that collision immediately re-enters:

\[
z':=T(x)=T^{D+2}(z),
\qquad A^p(z')=z'.
\]

Write the return identity for the re-entered state as

\[
T^p(z')=2^m z'+R',
\qquad 0\le R'<2^m.
\]

The question is whether `z'` can itself begin another long same-period persistence corridor.

## 1. Exact fringe transport modulo the normalization boundary

Because `z'` is `A^p`-fixed,

\[
R'=T^p(z')\bmod2^m.
\]

Since physical Rule 30 iterates commute,

\[
T^p(z')=T^{D+2}(T^p z).
\]

Also

\[
T^p z\equiv R\pmod{2^m}.
\]

The packed Rule-30 map is triangular in binary, so reduction modulo `2^m` commutes with every physical iterate. Hence

\[
\boxed{
R'=T^{D+2}(R)\bmod2^m.
}
\]

Thus the next fringe is obtained simply by evolving the old fringe through the collision/re-entry interval and discarding the bits that crossed the normalization boundary.

## 2. Universal fifth leading bit after four physical steps

Let a nonzero finite word `w` have highest occupied bit at position `h`. For `q>=0`, define the leading-edge bits

\[
a_j^{(q)}=(T^q w)_{h+2q-j},
\qquad j\ge0,
\]

so `a_0^(q)` is the highest bit and `a_4^(q)` is the fifth bit from the leading edge.

The local packed Rule-30 update gives the exact relative recurrence

\[
\boxed{
a_j^{(q+1)}
=a_{j-2}^{(q)}\oplus
\bigl(a_{j-1}^{(q)}\lor a_j^{(q)}\bigr),
}
\]

with negative-index `a`'s equal to zero.

Because `a_0^(0)=1`, the recurrence gives

\[
a_0^{(q)}=1
\]

for every `q`, and after one step

\[
a_1^{(q)}=1\qquad(q\ge1).
\]

Therefore

\[
a_2^{(q)}=0\qquad(q\ge2).
\]

For `q>=2`, the next two recurrences reduce to

\[
a_3^{(q+1)}=1\oplus a_3^{(q)},
\]

and

\[
a_4^{(q+1)}=a_3^{(q)}\lor a_4^{(q)}.
\]

In particular,

\[
\begin{aligned}
a_4^{(4)}
&=a_3^{(3)}\lor a_4^{(3)}\\
&=(1\oplus a_3^{(2)})
  \lor
  (a_3^{(2)}\lor a_4^{(2)})\\
&=1.
\end{aligned}
\]

Once `a_4` becomes 1, the recurrence keeps it 1 forever. Hence:

\[
\boxed{
q\ge4
\Longrightarrow
\text{the fifth bit from the leading edge of }T^q(w)\text{ is }1.
}
\]

This leading-edge fact is independent of all lower bits of `w`.

## 3. Even corridor G=2D>=4: the next corridor is exactly zero

Let

\[
G=2D\ge4.
\]

Then `D>=2` and the re-entry evolution length is

\[
q=D+2\ge4.
\]

The old fringe has bitlength

\[
L=m-2D.
\]

Therefore

\[
\operatorname{bitlength}(T^{D+2}R)
=L+2(D+2)=m+4.
\]

Its highest occupied bit is at position `m+3`. The fifth leading bit, offset four from that top bit, is therefore at position

\[
(m+3)-4=m-1.
\]

By the leading-edge lemma, that bit is 1.

Reduction modulo `2^m` deletes positions `m,m+1,m+2,m+3` but retains position `m-1`. Using the exact fringe transport formula,

\[
R'=T^{D+2}(R)\bmod2^m
\]

therefore has bit `m-1` equal to 1. Hence

\[
\operatorname{bitlength}(R')=m
\]

and the re-entered return corridor is

\[
\boxed{G'=m-\operatorname{bitlength}(R')=0.}
\]

So every immediate re-entry after an even corridor `G>=4` lands in a same-period state with **no positive return corridor at all**.

## 4. Odd corridor G=2D+1>=5: the next corridor is at most one

Now let

\[
G=2D+1\ge5.
\]

Again `D>=2`, so

\[
q=D+2\ge4.
\]

The old fringe has bitlength

\[
L=m-(2D+1).
\]

Thus

\[
\operatorname{bitlength}(T^{D+2}R)
=L+2(D+2)=m+3.
\]

Its highest occupied bit is at position `m+2`. The fifth leading bit is at

\[
(m+2)-4=m-2,
\]

and is therefore 1.

After reduction modulo `2^m`, position `m-2` remains set. Consequently

\[
\operatorname{bitlength}(R')\ge m-1
\]

and

\[
\boxed{G'\le1.}
\]

The bit at position `m-1` may be either zero or one, so both `G'=1` and `G'=0` are possible in principle.

Thus an immediate re-entry after any odd corridor `G>=5` also cannot initiate another long same-period persistence block.

## 5. Exceptional odd corridor G=3

For

\[
G=3,
\]

we have `D=1` and only

\[
q=D+2=3
\]

physical fringe steps before re-entry. The universal fifth-leading-bit lemma starts at four steps, so the proof above does not apply.

Exact finite-state data nevertheless shows the same collapse at periods 4 and 8:

- period 4 has two `G=3` immediate re-entries; their new corridors are `0` and `1`;
- period 8 has 47 `G=3` immediate re-entries; 31 give new corridor `0` and 16 give new corridor `1`.

This is evidence only. A general `G=3` theorem would require either an admissibility restriction on the leading bits of genuine return fringes or a separate three-step boundary calculation.

## 6. Exact finite-state check at period 8

For exact period 8, the finite-extension graph contains immediate re-entries from long corridors with the following counts:

- `G=3`: 47 re-entries;
- `G=4`: 7 re-entries;
- `G=5`: 9 re-entries;
- no re-entries for `G=6,7,8,9,10` in the exact period-8 census.

For every one of the 63 re-entering states,

\[
R'=T^{D+2}(R)\bmod2^{16}
\]

matches the directly reconstructed return fringe of `z'=T^{D+2}z`.

The post-re-entry corridor distribution is:

- from `G=3`: 31 cases with `G'=0`, 16 with `G'=1`;
- from `G=4`: all 7 cases have `G'=0`;
- from `G=5`: 2 cases with `G'=0`, 7 with `G'=1`.

This exactly matches the theorem in its covered range.

## Consequence for the global proof strategy

Immediate re-entry is much less dangerous than it first appeared.

For every collision with

\[
G\ge4
\]

except the parity-impossible odd value `G=4` wording aside—more precisely, for every even `G>=4` and every odd `G>=5`—an immediate re-entry is an isolated same-period event:

- even corridor: the next fixed state has `G'=0`;
- odd corridor: the next fixed state has `G'<=1`.

Therefore a long neutral plateau cannot cross its first collision by one-step re-entry and then immediately regenerate another long plateau of the same normalized period. Any proof route that counts long same-period residence blocks may treat such a re-entry as terminating that corridor, rather than as a reset into another long corridor.

The only unresolved immediate-reentry recurrence case is `G=3`. The next sharp target is to classify the top five bits of admissible `G=3` return fringes strongly enough to decide whether their three-step evolved fringe always has bit `m-2` set. If yes, the corridor-collapse theorem extends to every long odd corridor.
