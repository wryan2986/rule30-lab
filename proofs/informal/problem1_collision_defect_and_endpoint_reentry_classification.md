# Problem 1: exact collision-defect and fringe-endpoint re-entry classification

Status: exact local theorem for genuine first return-fringe collisions. It classifies the first collision mask for every positive corridor and reduces immediate re-entry for every long corridor to bounded endpoint data of the return fringe. Problem 1 remains open.

## Setup

Use

\[
T(x)=x\oplus((2x)\lor(4x)),\qquad A(x)=T(x)\gg2.
\]

Let `z` be an `A^p`-fixed finite word, with

\[
T^p(z)=2^{2p}z+R.
\]

Put

\[
m=2p,\qquad L=\operatorname{bitlength}(R),\qquad G=m-L>0,
\]

and

\[
D=\lfloor G/2\rfloor.
\]

The return-fringe persistence theorem gives

\[
E_p(T^qz):=A^p(T^qz)\oplus T^qz=0
\]

through `q=D`, and the first failing physical row is

\[
x=T^{D+1}(z).
\]

Write

\[
y=T^D(z),
\]

so `x=T(y)` and `E_p(y)=0`.

The run-28 exact commutator formula is

\[
d_p(w):=A^p(Tw)\oplus T(A^pw)
=c\!\left((T^p(w)\gg(m-2))\bmod8\right),
\]

where

\[
c(s)=(s_0\lor s_1)+2(s_1\land\neg s_2)\in\{0,1,3\}.
\]

Because `E_p(y)=0`, the exact defect update from the earlier re-entry note collapses to

\[
\boxed{E_p(x)=d_p(y).}
\]

This makes the first collision mask directly computable from the return fringe.

## 1. Exact first-collision mask

At the last persistent row, the shifted body and fringe are still separated, hence

\[
T^p(y)=T^D(T^p z)=2^m y+T^D(R).
\]

Therefore

\[
(T^p(y)\gg(m-2))\bmod8
=
4(y\bmod2)
+
\left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor.
\]

### Odd corridor

Suppose

\[
G=2D+1.
\]

Then

\[
\operatorname{bitlength}(T^D(R))
=L+2D
=m-1,
\]

so

\[
\left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor=1.
\]

The commutator source is therefore `1` or `5` modulo 8. Since

\[
c(1)=c(5)=1,
\]

we obtain

\[
\boxed{G\text{ odd}\Longrightarrow E_p(x)=1.}
\]

This includes the short case `G=1` as well as all longer odd corridors.

### Even corridor

Suppose

\[
G=2D.
\]

Here `D>=1`, and

\[
\operatorname{bitlength}(T^D(R))=m.
\]

Every nonzero finite Rule-30 image begins with binary `11`. Hence the two retained leading fringe bits are exactly `11` and

\[
\left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor=3.
\]

The commutator source is consequently `3` when `y` is even and `7` when `y` is odd. Since

\[
c(3)=3,\qquad c(7)=1,
\]

and Rule 30 preserves parity,

\[
E_p(x)=
\begin{cases}
3,&z\text{ even},\\
1,&z\text{ odd}.
\end{cases}
\]

Reducing the return identity modulo 2 gives `R == z (mod 2)`, so the result is intrinsic to the fringe:

\[
\boxed{
G\text{ even}\Longrightarrow
E_p(x)=
\begin{cases}
3,&R\text{ even},\\
1,&R\text{ odd}.
\end{cases}
}
\]

Thus the complete first-collision-mask classification is determined by only the parity of `G` and the parity of `R`.

## 2. Odd long corridors: re-entry from the bottom two fringe bits

Assume

\[
G=2D+1\ge3.
\]

The earlier odd-corridor theorem proved

\[
E_p(Tx)=0
\iff
T^D(z)\equiv1\pmod4.
\]

The low-bit identity

\[
T(w)\equiv-w\pmod8
\]

implies, modulo 4,

\[
T^D(z)\equiv(-1)^Dz.
\]

The return identity gives

\[
R\equiv T^p(z)\equiv(-1)^pz\pmod4,
\]

hence

\[
T^D(z)\equiv(-1)^{p+D}R\pmod4.
\]

Therefore immediate re-entry after every odd corridor `G>=3` is decided by the bottom two fringe bits and one parity:

\[
\boxed{
E_p(Tx)=0
\iff
R\equiv
\begin{cases}
1\pmod4,&p+D\text{ even},\\
3\pmod4,&p+D\text{ odd}.
\end{cases}
}
\]

In particular, an odd long corridor can re-enter only when `R` itself is odd.

## 3. Even long corridors: every odd fringe is non-reentering

Now assume

\[
G=2D\ge4.
\]

Run 28 proved that the terminal commutator state at the collision row satisfies

\[
d_p(x)\in\{0,1\}.
\]

If `R` is odd, Section 1 gives

\[
E_p(x)=1.
\]

But the exact defect-1 re-entry classifier requires

\[
d_p(x)=3.
\]

That is impossible. Therefore

\[
\boxed{
G\ge4\text{ even and }R\text{ odd}
\Longrightarrow
E_p(Tx)\ne0.
}
\]

This excludes half of the fringe parities from immediate re-entry without any further geometric information.

## 4. Even long corridors with even R: exact endpoint criterion

Let `R` be even. Then Section 1 gives

\[
E_p(x)=3.
\]

The exact defect-3 re-entry classifier says

\[
E_p(Tx)=0
\iff
x_2=1,\quad x_0\oplus x_1=1,\quad d_p(x)=1.
\]

Because parity is preserved and `R` is even, `x` is even. Thus `x_0=0`, and the two low-bit conditions reduce simply to

\[
\boxed{x\equiv6\pmod8.}
\]

Again using `T(w) == -w (mod 8)`, together with

\[
R\equiv T^p(z)\equiv(-1)^pz\pmod8,
\]

we get

\[
x=T^{D+1}(z)\equiv(-1)^{p+D+1}R\pmod8.
\]

Hence

\[
\boxed{
x\equiv6\pmod8
\iff
R\equiv
\begin{cases}
2\pmod8,&p+D\text{ even},\\
6\pmod8,&p+D\text{ odd}.
\end{cases}}
\]

It remains only to impose `d_p(x)=1`.

Define the leading-four-bit class

\[
H(R)=
\begin{cases}
0,&R\text{ begins }1000,1001,1010,1011,\text{ or }1100,\\
1,&R\text{ begins }1101,1110,\text{ or }1111.
\end{cases}
\]

The run-28 classification can be written compactly as

\[
\boxed{d_p(x)=1\oplus(D\bmod2)\oplus H(R).}
\]

Therefore

\[
\boxed{d_p(x)=1\iff H(R)=D\bmod2.}
\]

Combining the two independent endpoint conditions gives the exact long-even re-entry theorem:

\[
\boxed{
E_p(Tx)=0
}
\]

if and only if all of the following hold:

1. `R` is even;
2. `R mod 8 = 2` when `p+D` is even, and `R mod 8 = 6` when `p+D` is odd;
3. `H(R)=D mod 2`.

Equivalently:

- if `D` is even, the leading four bits must lie in `1000,1001,1010,1011,1100`;
- if `D` is odd, the leading four bits must lie in `1101,1110,1111`;
- independently, the bottom three bits are fixed to `010` or `110` according to the parity of `p+D`.

No interior fringe bits enter the criterion.

## 5. Finite-state verification at period 8

The existing exact finite-extension graph for `p=8` contains 126 exact-period-8 states with even corridor `G>=4`.

Evaluating the theorem on all 126 gives zero mismatches with direct computation of

\[
A^8(Tx)=Tx.
\]

Exactly 7 of those 126 states re-enter immediately. All 7 satisfy the endpoint criterion above. In the `G=4`, `D=2`, `p=8` case the criterion becomes

\[
R\bmod8=2
\]

and a leading-four-bit class with `H(R)=0`; the seven observed re-entry fringes have precisely that form.

This is computational verification only; the classification itself follows from the exact identities above.

## Consequence for the global proof strategy

The local boundary behavior is now bounded more strongly than in run 28:

- the first collision mask is known from `(G mod 2, R mod 2)`;
- every long odd-corridor immediate re-entry is known from `R mod 4` and `p+D mod 2`;
- every long even-corridor immediate re-entry is known from the top four bits of `R`, the bottom three bits of `R`, and the parities of `p` and `D`;
- every odd-`R` long-even collision is forced to leave the `A^p`-fixed set for at least the next physical row.

Thus there is no remaining hidden interior-fringe or source-history variable in the *one-step* collision/re-entry problem.

The next global question is not how a single collision behaves, but whether a fixed finite seed can encounter infinitely many return plateaus whose fringe endpoint classes satisfy the re-entry conditions above. That must be attacked with the common-origin/front/residence machinery, or else by constructing a recurring family showing that these bounded endpoint classes are reusable.
