# Problem 1: even-corridor terminal source sharpening

Status: exact refinement of the genuine-collision terminal source classification. Problem 1 remains open.

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
\qquad G=m-L.
\]

Assume the return corridor is even:

\[
G=2D>0.
\]

The first boundary-collision row is

\[
x=T^{D+1}(z).
\]

For

\[
u_j=A^j(x),\qquad s_j=T(u_j),
\]

the previous terminal-source theorem only used bit length and obtained

\[
s_{p-1}\pmod8\in\{1,2,5,6\}.
\]

The exact leading-bit structure of finite Rule-30 images sharpens this to only two possibilities.

## 1. Every nonzero finite Rule-30 image begins with binary `11`

Let a nonzero finite word `w` have highest set bit at position `k`.

Using

\[
T(w)=w\oplus((2w)\lor(4w)),
\]

the output bit at position `k+2` is `1`, because it receives the highest bit of `w` through the `4w` term and there is no contribution from `w` itself or `2w` at that position.

At position `k+1`, the `2w` term contributes the highest input bit `1`, so the OR term is also `1`; again `w` itself has no bit there.

Therefore the two highest output bits are always

\[
\boxed{11_2}.
\]

Equivalently, if `n=bitlength(w)`, then

\[
\boxed{
\left\lfloor\frac{T(w)}{2^n}\right\rfloor=3.
}
\]

This is stronger than the generic fact that `T(w)` gains two bits.

## 2. Exact terminal fringe quotient for even corridors

From the earlier collision calculation,

\[
 u_{p-1}
 =4T^D(z)
 +
 \left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor.
\]

Since `G=2D`,

\[
\operatorname{bitlength}(T^{D-1}(R))
=L+2D-2
=m-2.
\]

Set

\[
W=T^{D-1}(R).
\]

Then `bitlength(W)=m-2` and

\[
T^D(R)=T(W).
\]

By the universal leading-`11` fact,

\[
\boxed{
\left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor=3.
}
\]

Hence the penultimate normalized state has the exact form

\[
\boxed{
 u_{p-1}=4T^D(z)+3.
}
\]

Therefore

\[
 u_{p-1}\equiv
 \begin{cases}
 3\pmod8,&T^D(z)\text{ even},\\
 7\pmod8,&T^D(z)\text{ odd}.
 \end{cases}
\]

Using `T(y) == -y (mod 8)`, the terminal source symbol is exactly

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
\boxed{s_{p-1}\pmod8\in\{1,5\}.}
\]

The earlier possibilities `2` and `6` cannot occur for a genuine even-corridor collision.

In particular, the commutator automaton's one-symbol synchronizer

\[
s\equiv6\pmod8
\]

is **never** the terminal symbol of any genuine first collision, odd or even: odd corridors end in `{3,7}`, and even corridors end in `{1,5}`.

## 3. Penultimate source refinement for longer even corridors

Assume `D>=2`, equivalently `G>=4`.

The same calculation one step earlier gives

\[
 u_{p-2}
 =16T^{D-1}(z)
 +
 \left\lfloor
 \frac{T^{D-1}(R)}{2^{m-4}}
 \right\rfloor.
\]

Again put `W=T^(D-1)(R)`. Since `D>=2`, `W` itself is a nonzero Rule-30 image. Its two highest bits are therefore `11`.

Because `bitlength(W)=m-2`, the quotient

\[
\left\lfloor\frac{W}{2^{m-4}}\right\rfloor
\]

is its top three bits and must lie in

\[
\{6,7\}.
\]

The multiple `16T^(D-1)(z)` vanishes modulo 8, so

\[
\boxed{u_{p-2}\pmod8\in\{6,7\}.}
\]

and hence

\[
\boxed{s_{p-2}\pmod8\in\{2,1\}.}
\]

Thus every genuine even corridor with `G>=4` has a terminal two-symbol source suffix in

\[
\boxed{
(s_{p-2},s_{p-1})
\in
\{(1,1),(1,5),(2,1),(2,5)\}
\pmod8.
}
\]

Unlike the odd-corridor suffixes `(7,3)` and `(7,7)`, these four abstract two-symbol words do not all synchronize the three-state commutator automaton. Therefore the odd-corridor bounded-memory proof does not automatically extend to even corridors.

## 4. Consequence for the proof strategy

The genuine-collision terminal alphabet is now much smaller than previously believed:

- odd `G`: final source in `{3,7}`;
- even `G`: final source in `{1,5}`.

No genuine collision terminates in source `0`, and none terminates in the synchronizing source `6`.

For odd `G>=3`, the previous note shows the forced penultimate `7` makes the last two symbols synchronizing anyway.

For even `G>=4`, the penultimate source is in `{1,2}` and the final source is in `{1,5}`. The remaining sharp target is therefore to determine which of the four pairs above are actually realizable from return-fringe geometry and whether adding one more fringe-determined source symbol forces synchronization or at least determines a proper subset of terminal commutator states.
