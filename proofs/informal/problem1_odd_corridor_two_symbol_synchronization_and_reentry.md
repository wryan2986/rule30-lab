# Problem 1: odd corridors force two-symbol commutator synchronization

Status: exact theorem for genuine first return-fringe collisions with odd corridor length `G>=3`. It removes all earlier commutator memory at the collision boundary and gives an exact immediate-reentry criterion. Problem 1 remains open.

## Setup

Use

\[
T(x)=x\oplus((2x)\lor(4x)),\qquad A(x)=T(x)\gg2.
\]

Let `z` have pure `A`-period `p`, with

\[
T^p(z)=2^{2p}z+R,
\qquad 0<R<2^{2p}.
\]

Write

\[
m=2p,
\qquad L=\operatorname{bitlength}(R),
\qquad G=m-L.
\]

Assume the return corridor is odd and at least three cells long:

\[
G=2D+1,\qquad D\ge1.
\]

The first physical row that loses the `A^p` return is

\[
x=T^{D+1}(z),
\]

and the boundary-collision theorem gives

\[
E_p(x):=A^p(x)\oplus x=1
\]

for odd `G`.

For the normalized orbit

\[
u_j=A^j(x),\qquad s_j=T(u_j),
\]

let `d_j` be the three-state commutator discrepancy from the earlier automaton note. Its transition depends only on `q=s_j mod 8`, with reachable-state table

| q | 0 | 1 | 3 |
|---:|---:|---:|---:|
| 3 | 3 | 3 | 0 |
| 7 | 1 | 1 | 0 |

(the columns are the incoming states `d_j=0,1,3`).

The previous run proved that for odd `G`, the last source symbol satisfies

\[
s_{p-1}\in\{3,7\}\pmod8.
\]

The key new point is that the preceding source symbol is actually forced.

## 1. Exact penultimate-two normalized state

Since

\[
x=T^{D+1}(z),
\]

we have

\[
A^{p-2}(x)
=
\left\lfloor
\frac{T^{p+D-1}(z)}{2^{m-4}}
\right\rfloor.
\]

Using the return identity and corridor separation through physical time `D-1`,

\[
T^{p+D-1}(z)
=
T^{D-1}(2^m z+R)
=
2^mT^{D-1}(z)+T^{D-1}(R).
\]

Therefore

\[
\boxed{
 u_{p-2}
 =16T^{D-1}(z)
 +
 \left\lfloor
 \frac{T^{D-1}(R)}{2^{m-4}}
 \right\rfloor.
}
\]

Because every nonzero finite Rule-30 word gains exactly two bits per physical step,

\[
\operatorname{bitlength}(T^{D-1}(R))
=L+2D-2.
\]

For `G=2D+1`, `L=m-(2D+1)`, hence

\[
L+2D-2=m-3.
\]

Thus `T^(D-1)(R)` has top bit exactly at position `m-4`, and no bit above it. Consequently

\[
\left\lfloor
\frac{T^{D-1}(R)}{2^{m-4}}
\right\rfloor=1.
\]

So in fact

\[
\boxed{
 u_{p-2}=16T^{D-1}(z)+1
}
\]

and therefore

\[
\boxed{u_{p-2}\equiv1\pmod8.}
\]

Using the exact low-bit identity

\[
T(y)\equiv-y\pmod8,
\]

the preceding source symbol is forced:

\[
\boxed{s_{p-2}\equiv7\pmod8.}
\]

Hence every genuine odd-corridor collision with `G>=3` ends in one of only two source suffixes:

\[
\boxed{(s_{p-2},s_{p-1})\equiv(7,3)\text{ or }(7,7)\pmod8.}
\]

## 2. The two-symbol suffix synchronizes the commutator

The source-7 transition maps the three reachable states as

\[
0\mapsto1,\qquad1\mapsto1,\qquad3\mapsto0.
\]

Thus after reading the forced penultimate symbol `7`, the possible commutator state set is reduced from

\[
\{0,1,3\}
\]

to

\[
\{0,1\}.
\]

Now apply the final symbol.

For final source `3`, both remaining states map to `3`:

\[
0\mapsto3,\qquad1\mapsto3.
\]

For final source `7`, both remaining states map to `1`:

\[
0\mapsto1,\qquad1\mapsto1.
\]

Therefore the collision-specific two-symbol suffix erases *all* earlier commutator history:

\[
\boxed{
 d_p=
 \begin{cases}
 3,&s_{p-1}\equiv3\pmod8,\\
 1,&s_{p-1}\equiv7\pmod8.
 \end{cases}
}
\]

This is the bounded-suffix theorem that the unrestricted automaton could not provide. It holds because return-fringe geometry forces the penultimate source to be `7`.

## 3. Expressing the terminal state directly from the physical return row

The previous terminal-state formula for odd `G` is

\[
 u_{p-1}=4T^D(z)+1.
\]

Hence

\[
 u_{p-1}\equiv
 \begin{cases}
 1\pmod8,&T^D(z)\text{ even},\\
 5\pmod8,&T^D(z)\text{ odd}.
 \end{cases}
\]

Since `s == -u (mod 8)`, this gives

\[
 s_{p-1}\equiv
 \begin{cases}
 7\pmod8,&T^D(z)\text{ even},\\
 3\pmod8,&T^D(z)\text{ odd}.
 \end{cases}
\]

Combining with the synchronization result yields the especially simple formula

\[
\boxed{
 d_p=
 \begin{cases}
 1,&T^D(z)\text{ even},\\
 3,&T^D(z)\text{ odd}.
 \end{cases}
}
\]

Equivalently,

\[
\boxed{d_p=1+2\,(T^D(z)\bmod2).}
\]

So for every genuine odd corridor of length at least three, the full length-`p` commutator history collapses to one parity bit of the physical row immediately before collision.

## 4. Exact immediate-reentry criterion

For odd `G`, the first collision has boundary defect

\[
E_p(x)=1.
\]

The earlier re-entry classifier proved

\[
E_p(Tx)=0
\iff
x_1=1\text{ and }d_p=3.
\]

Put

\[
y=T^D(z),
\]

so `x=T(y)`.

From the formula above,

\[
d_p=3\iff y\text{ is odd}.
\]

Also `T(y) == -y (mod 4)`, so

\[
x_1=1
\iff
x\bmod4\in\{2,3\}
\iff
y\bmod4\in\{1,2\}.
\]

Combining this with `y` odd leaves exactly one residue class:

\[
\boxed{
E_p(Tx)=0
\iff
T^D(z)\equiv1\pmod4.
}
\]

Thus immediate physical re-entry after an odd-corridor collision is no longer governed by an unresolved source history. It is decided exactly by the two low bits of the pre-collision physical row.

## 5. Scope and significance

The argument requires `D>=1`, equivalently odd corridor `G>=3`, because deriving `s_(p-2)` uses one physical step before the collision interval. The short case `G=1` is not covered by this two-symbol proof and remains separate.

For every longer odd corridor, however:

1. the final source suffix is exactly `(7,3)` or `(7,7)`;
2. that suffix synchronizes the three-state commutator automaton;
3. `d_p` is determined solely by the parity of `T^D(z)`;
4. immediate re-entry is equivalent to `T^D(z) == 1 (mod 4)`.

This eliminates unbounded commutator memory completely on the odd-corridor side. Any remaining obstruction to a global Problem-1 proof must therefore come from the even-corridor geometry, from the short `G=1` odd case, or from how these local collision/re-entry events accumulate across plateaus.

## Next target

Perform the analogous two-symbol analysis for even corridors `G=2D`. There

\[
\operatorname{bitlength}(T^{D-1}(R))=m-2,
\]

so `u_(p-2) mod 8` is the top three-bit prefix of `T^(D-1)(R)` and lies in `{4,5,6,7}`. The resulting penultimate source lies in `{4,3,2,1}`. The useful question is whether the Rule-30 evolution of that top three-bit prefix constrains its pairing with the known final source set `{1,2,5,6}` strongly enough to force synchronization or a small explicit list of terminal commutator states.
