# Problem 1: immediate re-entry after a long corridor collapses the next same-period corridor

Status: exact theorem for every even corridor `G>=4` and every odd corridor `G>=5`. If the first collision immediately re-enters the same `A^p`-fixed set, the re-entered state's own return corridor has length `0` in the even case and at most `1` in the odd case. The exceptional odd case `G=3` remains open. Problem 1 remains open.

## Setup

Let

\[
T^p(z)=2^m z+R,\qquad m=2p,
\]

with

\[
G=m-\operatorname{bitlength}(R)>0,
\qquad D=\lfloor G/2\rfloor.
\]

The first collision row is

\[
x=T^{D+1}(z).
\]

Assume it immediately re-enters:

\[
z':=T(x)=T^{D+2}(z),
\qquad A^p(z')=z'.
\]

Write

\[
T^p(z')=2^m z'+R',\qquad 0\le R'<2^m.
\]

We determine how large the new return corridor

\[
G'=m-\operatorname{bitlength}(R')
\]

can be.

## 1. Exact fringe transport through re-entry

Because `z'` is `A^p`-fixed,

\[
R'=T^p(z')\bmod2^m.
\]

Physical iterates commute, and the packed Rule-30 map is triangular in binary, so reduction modulo `2^m` commutes with every physical iterate. Since

\[
T^p z\equiv R\pmod{2^m},
\]

we obtain

\[
\boxed{R'=T^{D+2}(R)\bmod2^m.}
\]

Thus the next fringe is simply the old fringe evolved through the collision/re-entry interval and truncated at the normalization boundary.

## 2. Universal fifth leading bit after four Rule-30 steps

Let a nonzero finite word `w` have highest occupied bit at position `h`. Define relative leading-edge bits

\[
a_j^{(q)}=(T^q w)_{h+2q-j},\qquad j\ge0.
\]

The packed Rule-30 rule gives

\[
\boxed{
a_j^{(q+1)}
=a_{j-2}^{(q)}\oplus
\bigl(a_{j-1}^{(q)}\lor a_j^{(q)}\bigr),
}
\]

with negative-index terms zero.

Since `a_0^(0)=1`, one gets

\[
a_0^{(q)}=1,
\qquad
a_1^{(q)}=1\ (q\ge1),
\qquad
a_2^{(q)}=0\ (q\ge2).
\]

For `q>=2`, therefore,

\[
a_3^{(q+1)}=1\oplus a_3^{(q)},
\qquad
a_4^{(q+1)}=a_3^{(q)}\lor a_4^{(q)}.
\]

Hence

\[
\begin{aligned}
a_4^{(4)}
&=a_3^{(3)}\lor a_4^{(3)}\\
&=(1\oplus a_3^{(2)})
 \lor(a_3^{(2)}\lor a_4^{(2)})\\
&=1.
\end{aligned}
\]

Once `a_4=1`, the second recurrence keeps it equal to 1. Thus

\[
\boxed{
q\ge4
\Longrightarrow
\text{the fifth bit from the leading edge of }T^q(w)\text{ is }1.
}
\]

## 3. Even corridor: immediate re-entry forces G'=0

Let

\[
G=2D\ge4.
\]

Then `D>=2` and `q=D+2>=4`. The old fringe has bitlength

\[
L=m-2D.
\]

Therefore

\[
\operatorname{bitlength}(T^{D+2}R)=L+2(D+2)=m+4.
\]

Its highest bit is at position `m+3`; the fifth leading bit is position `m-1`. By the lemma, that bit is 1.

Reduction modulo `2^m` removes positions `m` through `m+3` but retains position `m-1`. Therefore `R'` has bitlength exactly `m`, and

\[
\boxed{G'=0.}
\]

So every immediate re-entry after an even corridor `G>=4` lands in a same-period state with no positive return corridor.

## 4. Odd corridor G>=5: immediate re-entry forces G'<=1

Let

\[
G=2D+1\ge5.
\]

Again `D>=2` and `q=D+2>=4`. Now

\[
L=m-(2D+1)
\]

and therefore

\[
\operatorname{bitlength}(T^{D+2}R)=m+3.
\]

The highest bit is at position `m+2`, so the fifth leading bit is position `m-2`. The lemma makes that bit 1. After reduction modulo `2^m`, it remains set, giving

\[
\operatorname{bitlength}(R')\ge m-1
\]

and hence

\[
\boxed{G'\le1.}
\]

Thus an immediate re-entry after any odd corridor `G>=5` cannot initiate another long same-period persistence block.

## 5. Exceptional G=3 case

For `G=3`, `D=1`, so the fringe evolves only three physical steps before the re-entered state:

\[
R'=T^3(R)\bmod2^m.
\]

The universal fifth-leading-bit lemma starts at four steps, so it does not settle this case.

Exact finite-state data nevertheless shows the same collapse at the periods currently tractable:

- period 4: both `G=3` immediate re-entries have `G'` equal to `0` or `1`;
- period 8: all 47 `G=3` immediate re-entries have `G'` equal to `0` or `1` (31 with `G'=0`, 16 with `G'=1`).

This remains evidence, not a theorem.

## 6. Period-8 finite-state census

The exact period-8 finite-extension graph gives 63 immediate re-entries from corridors `G>=3`:

- `G=3`: 47;
- `G=4`: 7;
- `G=5`: 9;
- `G=6,7,8,9,10`: none.

For all 63,

\[
R'=T^{D+2}(R)\bmod2^{16}
\]

matches the directly reconstructed fringe of `z'=T^{D+2}z`.

The post-re-entry gaps are:

- from `G=3`: 31 with `G'=0`, 16 with `G'=1`;
- from `G=4`: all 7 with `G'=0`;
- from `G=5`: 2 with `G'=0`, 7 with `G'=1`.

## Consequence for the global proof strategy

For every even corridor `G>=4` and every odd corridor `G>=5`, one-step re-entry terminates the long same-period corridor rather than resetting into another long corridor:

\[
\boxed{
G\ge4\text{ even and re-entry}\Longrightarrow G'=0,
}
\]

\[
\boxed{
G\ge5\text{ odd and re-entry}\Longrightarrow G'\le1.
}
\]

This removes immediate re-entry as a mechanism for chaining arbitrarily long same-period residence blocks in all cases except `G=3`.

The next sharp target is the remaining three-step case. Direct leading-edge calculation shows that the fifth leading bit of `T^3(R)` can vanish only for a small set of initial leading prefixes; the useful question is whether any genuine `A^p` return fringe satisfying the `G=3` re-entry condition can realize those prefixes. A negative answer would extend the corridor-collapse theorem to every long odd corridor.