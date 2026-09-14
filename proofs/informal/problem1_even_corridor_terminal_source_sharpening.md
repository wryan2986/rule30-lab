# Problem 1: even-corridor terminal source sharpening

Status: corrected exact refinement of the genuine-collision terminal source classification. Problem 1 remains open.

> Correction note (run 25): the run-24 version of Section 3 incorrectly said that a word of bitlength `m-2`, divided by `2^(m-4)`, exposes its top three bits. It exposes its top **two** bits. The corrected calculation is stronger: for every even corridor `G=2D>=4`, the penultimate source is exactly `5 mod 8`, and in fact a whole suffix is forced to consist of `5` symbols.

## Setup

Let `z` have pure `A`-period `p` with

\[
T^p(z)=2^{2p}z+R,
\qquad 0<R<2^{2p}.
\]

Put

\[
m=2p,
\qquad L=\operatorname{bitlength}(R),
\qquad G=m-L=2D>0.
\]

The first boundary-collision row is

\[
x=T^{D+1}(z).
\]

For

\[
u_j=A^j(x),\qquad s_j=T(u_j),
\]
we use the separated-return formula. For every integer `r` in the separated range,

\[
\boxed{
 u_{p-r}
 =2^{2r}T^{D+1-r}(z)
 +
 \left\lfloor
 \frac{T^{D+1-r}(R)}{2^{m-2r}}
 \right\rfloor.
}
\]

## 1. Every nonzero finite Rule-30 image begins with binary `11`

Let a nonzero finite word `w` have highest set bit at position `k`. Using

\[
T(w)=w\oplus((2w)\lor(4w)),
\]

the output bits at positions `k+2` and `k+1` are both `1`. Therefore every nonzero finite Rule-30 image has two leading bits

\[
\boxed{11_2}.
\]

Equivalently, if `n=bitlength(w)`, then

\[
\boxed{
\left\lfloor\frac{T(w)}{2^n}\right\rfloor=3.
}
\]

## 2. Exact terminal source

Taking `r=1`,

\[
 u_{p-1}
 =4T^D(z)
 +
 \left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor.
\]

Since `T^D(R)` is a nonzero Rule-30 image of bitlength `m`, its top two bits are `11`, so the quotient is exactly `3`. Hence

\[
\boxed{u_{p-1}=4T^D(z)+3.}
\]

Using `T(y)\equiv-y\pmod8`,

\[
\boxed{
 s_{p-1}\equiv
 \begin{cases}
 5\pmod8,&T^D(z)\text{ even},\\
 1\pmod8,&T^D(z)\text{ odd}.
 \end{cases}
}
\]

Thus

\[
\boxed{s_{p-1}\in\{1,5\}\pmod8.}
\]

## 3. Corrected penultimate source and the full forced `5` suffix

Assume `D>=2`, i.e. `G>=4`.

For `r=2`,

\[
 u_{p-2}
 =16T^{D-1}(z)
 +
 \left\lfloor
 \frac{T^{D-1}(R)}{2^{m-4}}
 \right\rfloor.
\]

Now `T^{D-1}(R)` has bitlength `m-2`. Dividing by `2^(m-4)` retains its top **two** bits, not three. Since `D-1>=1`, this word is a nonzero Rule-30 image, so those two bits are `11`. Therefore

\[
\boxed{
\left\lfloor
 \frac{T^{D-1}(R)}{2^{m-4}}
\right\rfloor=3,
}
\]

and hence

\[
\boxed{u_{p-2}\equiv3\pmod8},
\qquad
\boxed{s_{p-2}\equiv5\pmod8}.
\]

The same argument works uniformly. For every

\[
2\le r\le D,
\]
we have `D+1-r>=1`, so `T^(D+1-r)(R)` is a nonzero Rule-30 image. Its bitlength is

\[
L+2(D+1-r)=m+2-2r.
\]

After division by `2^(m-2r)`, exactly its two leading bits remain, hence the quotient is again `3`. Since `2^(2r)T^(D+1-r)(z)` is divisible by `8` for `r>=2`,

\[
\boxed{u_{p-r}\equiv3\pmod8}
\]

and therefore

\[
\boxed{s_{p-r}\equiv5\pmod8}
\qquad(2\le r\le D).
\]

Thus every genuine even corridor `G=2D>=4` has the forced terminal source structure

\[
\boxed{
(s_{p-D},s_{p-D+1},\ldots,s_{p-2})
=(5,5,\ldots,5)
}
\]

with exactly `D-1` copies of `5`, followed by

\[
\boxed{s_{p-1}\in\{1,5\}.}
\]

This replaces the incorrect run-24 Cartesian-product claim `{1,2} x {1,5}`.

## 4. Exact effect on the three-state commutator automaton

On reachable commutator states `{0,1,3}`, source symbol `5` acts as

\[
0\mapsto1,\qquad1\mapsto0,\qquad3\mapsto1.
\]

After one source-`5` symbol the state is therefore in `{0,1}`, and on `{0,1}` both source `5` and source `1` act as the same transposition

\[
0\leftrightarrow1.
\]

Let

\[
h=d_{p-D}.
\]

For `D>=2`, the forced suffix contains `D-1` copies of source `5` and then one terminal source in `{1,5}`. The terminal choice no longer matters. The final commutator state is

\[
\boxed{
 d_p
 =
 \begin{cases}
 1,&D\text{ odd and }h\ne1,\\
 0,&D\text{ odd and }h=1,\\
 1,&D\text{ even and }h=1,\\
 0,&D\text{ even and }h\ne1.
 \end{cases}
}
\]

Equivalently,

\[
\boxed{
 d_p=
 \mathbf 1_{h\ne1}\oplus((D-1)\bmod2).
}
\]

In particular,

\[
\boxed{d_p\in\{0,1\}}
\]

for every even corridor `G>=4`: state `3` is impossible at the end of such a genuine collision.

This does not fully synchronize the history, because it retains one binary distinction: whether `d_(p-D)` equals `1` or lies in `{0,3}`. But it compresses the entire length-`D` collision suffix to that single bit plus the parity of `D`.

## 5. The source immediately before the forced suffix is read directly from the top of `R`

Because `G=2D` and `L=m-2D`, take `r=D+1`. Then `p-r=p-D-1>=0` and `D+1-r=0`, so the separated-return identity reduces directly to the original return equation:

\[
 u_{p-D-1}
 =2^{2D+2}z
 +
 \left\lfloor\frac{R}{2^{L-2}}\right\rfloor.
\]

Since `L` is positive and even, `L>=2`. The quotient is exactly the top two bits of `R`, hence is either `2` (`10_2`) or `3` (`11_2`). The first term is divisible by `8`, so

\[
\boxed{
 u_{p-D-1}\pmod8=
 \begin{cases}
 2,&R\text{ begins }10,\\
 3,&R\text{ begins }11.
 \end{cases}
}
\]

and therefore, using `T(y)\equiv-y\pmod8`,

\[
\boxed{
 s_{p-D-1}\equiv
 \begin{cases}
 6\pmod8,&R\text{ begins }10,\\
 5\pmod8,&R\text{ begins }11.
 \end{cases}
}
\]

This gives a sharp dichotomy.

### `R` begins `10`: complete synchronization

Source `6` is the automaton reset:

\[
F(d,6)=1
\qquad\text{for every reachable }d.
\]

Hence

\[
\boxed{d_{p-D}=1.}
\]

The entire earlier source history is erased before the forced `5` suffix begins. Substituting `h=1` into the formula above,

\[
\boxed{
 d_p=
 \begin{cases}
 0,&D\text{ odd},\\
 1,&D\text{ even}.
 \end{cases}
}
\]

Thus every even corridor `G>=4` whose return fringe begins `10` has a completely explicit terminal commutator state depending only on `D mod 2`.

### `R` begins `11`: exactly one unresolved history bit remains

Then `s_(p-D-1)=5`. This is not a synchronizer. It maps `{0,3}` together to `1` and maps `1` to `0`, so after this symbol

\[
d_{p-D}\in\{0,1\}
\]

and the only surviving information is whether the preceding state `d_(p-D-1)` was `1` or not.

Therefore the long-even-corridor obstruction has now been reduced to a single exceptional geometry:

\[
\boxed{R\text{ begins }11.}
\]

All `10`-leading even fringes synchronize completely.

## 6. Research consequence

The corrected even-corridor source word is far more rigid than the run-24 note claimed:

\[
\boxed{
(6\text{ or }5),\ 5^{D-1},\ (1\text{ or }5).
}
\]

The first symbol is determined by the top two bits of the original return fringe. If they are `10`, the automaton resets and `d_p` is explicit. If they are `11`, one binary distinction survives.

The next sharp target is therefore not a generic third terminal source. It is to decide whether a genuine long even return fringe can begin `11`, and, if so, whether common-origin/FULL geometry or one more bit of `R` determines whether `d_(p-D-1)=1`. A proof that long even fringes must begin `10` would completely settle the local commutator-memory problem for all even corridors `G>=4`.
