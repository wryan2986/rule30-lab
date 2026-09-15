# Problem 1: immediate re-entry after a long corridor collapses the next same-period corridor

Status: exact theorem for every long corridor `G>=3`. If the first collision immediately re-enters the same `A^p`-fixed set, the re-entered state's own return corridor has length `0` for every even `G>=4`, and at most `1` for every odd `G>=3`. Problem 1 remains open.

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

## 2. Universal leading-edge facts

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
\qquad a_1^{(q)}=1\ (q\ge1),
\qquad a_2^{(q)}=0\ (q\ge2).
\]

For `q>=2`, therefore,

\[
a_3^{(q+1)}=1\oplus a_3^{(q)},
\qquad a_4^{(q+1)}=a_3^{(q)}\lor a_4^{(q)}.
\]

Two consequences are needed.

### Fifth leading bit after four steps

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
\Longrightarrow a_4^{(q)}=1.
}
\]

### The fourth/fifth pair after three steps cannot both vanish

At `q=3`, the same recurrences give

\[
a_3^{(3)}=1\oplus a_3^{(2)},
\qquad
a_4^{(3)}=a_3^{(2)}\lor a_4^{(2)}.
\]

Hence

\[
\boxed{
a_3^{(3)}\lor a_4^{(3)}=1.
}
\]

This two-bit statement is exactly what the `G=3` truncation needs. The previous run focused only on the fifth leading bit `a_4^(3)` and therefore left a spurious exceptional-prefix case: whenever that fifth bit vanishes, the fourth bit is forced to be one.

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

## 5. Odd corridor G=3: exact closure

Now let

\[
G=3,
\qquad D=1.
\]

Then

\[
R'=T^3(R)\bmod2^m.
\]

Since `R` has bitlength `m-3`, `T^3(R)` has bitlength

\[
(m-3)+6=m+3.
\]

Its highest bit is at position `m+2`. Reduction modulo `2^m` discards the first three leading bits, so the two highest positions that can remain are

- position `m-1`, carrying `a_3^(3)`;
- position `m-2`, carrying `a_4^(3)`.

But the three-step leading-edge identity above says

\[
a_3^{(3)}\lor a_4^{(3)}=1.
\]

Therefore at least one of positions `m-1,m-2` survives as a one. Hence

\[
\operatorname{bitlength}(R')\ge m-1
\]

and

\[
\boxed{G'\le1.}
\]

This proves the previously open `G=3` case for every period and every nonzero fringe; no admissibility or endpoint re-entry classification is needed beyond the assumption that the transported fringe is the return fringe of the re-entered state.

## 6. Uniform theorem

Combining the cases:

\[
\boxed{
G\ge4\text{ even and immediate re-entry}\Longrightarrow G'=0,
}
\]

and

\[
\boxed{
G\ge3\text{ odd and immediate re-entry}\Longrightarrow G'\le1.
}
\]

Thus every immediate re-entry after a long corridor terminates the long same-period persistence block. There is no exceptional `G=3` mechanism capable of chaining one long same-period corridor directly into another.

The exact finite-state data from periods 4 and 8 remains consistent with the theorem: at period 8 the 47 `G=3` immediate re-entries split into 31 cases with `G'=0` and 16 with `G'=1`.

## Consequence for the global proof strategy

The local immediate-reentry branch is now closed. A long return-fringe corridor can collide and immediately re-enter the same `A^p`-fixed set, but that re-entry necessarily lands in a state with corridor gap at most one (and exactly zero for every even long corridor). Therefore immediate re-entry cannot generate an indefinite chain of long same-period residence blocks.

Further work should return to the global FULL/common-origin/front-residence argument: the remaining task is to show that a finite survivor cannot evade the resulting loss of long same-period residence indefinitely by changing period/phase or by moving through the short-gap states.