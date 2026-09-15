# Repaired long corridor forces a parity-determined next collision mask

Status: `partial-proof`. This sharpens the run-32 forced-recollision result. It does not close Problem 1.

## Setup

Let `z` be a finite `A^p`-fixed row with return identity

\[
T^p(z)=2^{2p}z+R,
\]

and long corridor `G>=3`. Put `D=floor(G/2)`. Let

\[
x=T^{D+1}(z)
\]

be the first collision row, and assume immediate same-period re-entry:

\[
z'=T(x)=T^{D+2}(z),\qquad A^p(z')=z'.
\]

Write the re-entered return identity as

\[
T^p(z')=2^{2p}z'+R',
\]

with `m=2p` and `G'=m-bitlength(R')`.

Runs 29-31 proved the exact fringe transport

\[
R'=T^{D+2}(R)\pmod{2^m},
\]

and the corridor collapse

- even original `G>=4`: `G'=0`;
- odd original `G>=3`: `G' in {0,1}`.

Run 32 then observed that `T(z')` is necessarily the very next same-period collision.

The purpose of this note is to classify the defect mask at that forced recollision.

## Lemma 1: first-collision mask also has an exact `G=0` version

The earlier collision-mask theorem was stated for positive corridor. For `G'=0`, the fixed row `z'` itself is still collision-free (`E_p(z')=0`), and its next row has

\[
E_p(Tz')=d_p(z').
\]

Use the exact commutator boundary formula

\[
d_p(w)=c\!\left((T^p(w)\gg(m-2))\bmod 8\right),
\]

where

\[
c(s)=(s_0\lor s_1)+2(s_1\land\neg s_2).
\]

Because `G'=0`, `R'` has bitlength exactly `m`. Hence

\[
Q:=\left\lfloor R'/2^{m-2}\right\rfloor\in\{2,3\}.
\]

From

\[
T^p(z')=2^m z'+R'
\]

we obtain

\[
(T^p(z')\gg(m-2))\bmod8=4(z'\bmod2)+Q.
\]

Directly,

\[
c(2)=c(3)=3,\qquad c(6)=c(7)=1.
\]

Therefore the top two bits of `R'` do not matter:

\[
\boxed{
G'=0\Longrightarrow E_p(Tz')=
\begin{cases}
3,&z'\text{ even},\\
1,&z'\text{ odd}.
\end{cases}}
\]

Reducing the return identity modulo 2 gives `R' == z' (mod 2)`, so equivalently

\[
\boxed{
G'=0\Longrightarrow E_p(Tz')=
\begin{cases}
3,&R'\text{ even},\\
1,&R'\text{ odd}.
\end{cases}}
\]

This is exactly the same parity rule previously obtained for positive even corridors.

For `G'=1`, the earlier odd-corridor calculation already applies and gives

\[
\boxed{G'=1\Longrightarrow E_p(Tz')=1.}
\]

## Lemma 2: fringe transport preserves parity

Rule 30 preserves the least significant bit because

\[
T(w)=w\oplus((2w)\lor(4w))\equiv w\pmod2.
\]

Reduction modulo `2^m` also preserves the least significant bit. Hence the exact transport law gives

\[
\boxed{R'\equiv R\pmod2.}
\]

## Theorem: the forced recollision mask remembers only the parity class of the original long corridor

### Original odd corridor

For every odd long corridor `G>=3`, the exact immediate-reentry criterion from run 29 requires `R` odd. Thus `R'` is odd.

If the collapsed corridor is `G'=1`, its first-collision mask is `1`. If it is `G'=0`, Lemma 1 and odd `R'` again give mask `1`.

Therefore

\[
\boxed{
G\ge3\text{ odd and immediate re-entry}
\Longrightarrow E_p(Tz')=1.
}
\]

This is independent of whether the exact run-31 formula produces `G'=0` or `G'=1`.

### Original even corridor

For every even long corridor `G>=4`, immediate re-entry requires `R` even, and corridor collapse gives `G'=0` exactly. Hence `R'` is even. Lemma 1 gives

\[
\boxed{
G\ge4\text{ even and immediate re-entry}
\Longrightarrow E_p(Tz')=3.
}
\]

Thus the run-32 forced next-step recollision has a completely determined mask:

\[
\boxed{
E_p(Tz')=
\begin{cases}
1,&G\text{ odd},\\
3,&G\text{ even}.
\end{cases}}
\]

for every repaired long corridor.

## Consequence

A repaired long corridor does not merely funnel immediately into another collision. It funnels into one of exactly two defect classes, selected by the parity of the original corridor:

    odd long G  -> repair -> G' in {0,1} -> next-step defect 1
    even long G -> repair -> G'=0        -> next-step defect 3

No interior fringe information, leading-four-bit class, or distinction between `G'=0` and `G'=1` survives into this next collision mask.

This is useful because the existing exact defect-1 and defect-3 successor classifiers can now be applied to the forced recollision without an unknown incoming mask. The remaining local/global bridge question is whether the special transported fringe `R'=T^(D+2)(R) mod 2^(2p)` forces or forbids a second immediate re-entry from these two mask classes. A restriction there would bound the length of same-period repair chains and feed directly into the period/phase accounting needed by the FULL/common-origin argument.

## Dependencies

Used only:

- exact commutator boundary formula from run 28;
- exact long-corridor immediate-reentry endpoint classification from run 29;
- exact fringe transport and corridor collapse from runs 29-31;
- run-32 observation that `G'<=1` forces the next physical row to be a same-period collision.

No census or density assumption is used.
