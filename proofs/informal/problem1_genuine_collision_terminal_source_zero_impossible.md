# Problem 1: genuine return-fringe collisions cannot end in source zero

Status: exact theorem. This resolves the empirical target from run 22. Problem 1 remains open.

## Setup

Use

\[
T(x)=x\oplus((2x)\lor(4x)),\qquad A(x)=T(x)\gg2.
\]

Let `z` be a pure `A`-periodic return state of exact period `p`, so

\[
T^p(z)=2^{2p}z+R,
\qquad 0<R<2^{2p}.
\]

Write

\[
m=2p,
\qquad L=\operatorname{bitlength}(R),
\qquad G=m-L>0,
\qquad D=\left\lfloor\frac G2\right\rfloor.
\]

The previous return-fringe persistence result shows that the first physical row that loses the `A^p` return is

\[
x=T^{D+1}(z),
\]

and the boundary-collision theorem gives

\[
A^p(x)=x\oplus\varepsilon,
\qquad \varepsilon\in\{1,3\}.
\]

For the normalized orbit

\[
u_j=A^j(x),\qquad s_j=T(u_j),
\]

run 22 asked whether a genuine first collision could have a terminal source-zero symbol

\[
s_{p-1}\equiv0\pmod8,
\]

equivalently, using `T(y) == -y (mod 8)`, whether

\[
u_{p-1}\equiv0\pmod8.
\]

It cannot.

## 1. Exact formula for the penultimate normalized state

Because normalized iteration is physical iteration followed by the accumulated right shift,

\[
A^{p-1}(x)
=
\left\lfloor
\frac{T^{p-1}(x)}{2^{2p-2}}
\right\rfloor.
\]

Since `x=T^(D+1)(z)`, this becomes

\[
u_{p-1}
=
\left\lfloor
\frac{T^{p+D}(z)}{2^{m-2}}
\right\rfloor.
\]

Now use the return identity at `z`:

\[
T^{p+D}(z)
=
T^D(2^m z+R).
\]

The corridor still separates the fringe from the regenerated copy through physical time `D` (this is exactly the persistence interval proved in the earlier return-fringe note), hence

\[
T^D(2^m z+R)
=
2^mT^D(z)+T^D(R).
\]

Therefore

\[
\boxed{
 u_{p-1}
 =
 4T^D(z)
 +
 \left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor.
}
\]

This formula exposes the terminal normalized residue directly from the fringe immediately before the boundary collision.

## 2. Bit length of the evolved fringe

Every nonzero finite Rule-30 word gains exactly two bits per physical step, so

\[
\operatorname{bitlength}(T^D(R))=L+2D.
\]

There are two parity cases for `G`.

### Odd corridor: `G=2D+1`

Then

\[
L=m-(2D+1),
\]
so

\[
\operatorname{bitlength}(T^D(R))=m-1.
\]

Thus bit `m-2` of `T^D(R)` is `1`, while all bits at positions `m-1` and above are zero. Hence

\[
\left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor=1.
\]

Consequently

\[
\boxed{
 u_{p-1}\equiv1\text{ or }5\pmod8.
}
\]

In particular it is never `0 mod 8`.

### Even corridor: `G=2D`

Now

\[
L=m-2D,
\]
so

\[
\operatorname{bitlength}(T^D(R))=m.
\]

The quotient by `2^(m-2)` is therefore exactly the top two bits of a word of bit length `m`, hence

\[
\left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor\in\{2,3\}.
\]

Therefore

\[
\boxed{
 u_{p-1}\pmod8\in\{2,3,6,7\}.
}
\]

Again zero is impossible.

Combining the two cases gives the theorem.

> **Terminal-zero exclusion theorem.** For every genuine first return-fringe boundary collision `x` arising from a positive corridor `G>0`,
> \[
> \boxed{A^{p-1}(x)\not\equiv0\pmod8.}
> \]
> Equivalently,
> \[
> \boxed{s_{p-1}=T(A^{p-1}(x))\not\equiv0\pmod8.}
> \]

This proves the empirical exclusion observed in the run-22 scan.

## 3. Stronger residue classification

Using `s == -u (mod 8)`, the final source symbol belongs to a much smaller parity-dependent set:

- if `G` is odd,
  \[
  \boxed{s_{p-1}\pmod8\in\{3,7\};}
  \]
- if `G` is even,
  \[
  \boxed{s_{p-1}\pmod8\in\{1,2,5,6\}.}
  \]

Thus the identity source symbol `0` is not merely uncommon: collision geometry forbids it exactly.

The synchronizing symbol `6` from the run-21 automaton can occur only in the even-`G` case, and more specifically only when

\[
 u_{p-1}\equiv2\pmod8.
\]

The theorem does not yet show that synchronization is forced; it removes the strongest arbitrary-memory construction (an arbitrarily long terminal block of identity symbols).

## 4. Relation to the run-22 valuation ladder

Run 22 showed that a terminal source-zero symbol would force

\[
A^{p-1}(x)=4r
\]

with an even finite ancestor core and hence `x xor epsilon = T(r)`.

The present argument shows why that ancestry can never arise for a genuine return-fringe collision: immediately before collision, the evolved return fringe necessarily occupies at least one of the two quotient bits retained by the final normalization. Its contribution is exactly

- `1` for odd `G`, or
- `2`/`3` for even `G`,

so the penultimate normalized state can never be divisible by eight.

This is a geometric obstruction coming directly from the return-fringe boundary, not from the near-return equation alone.

## 5. Research consequence

The run-21 abstract automaton admitted unbounded suffix memory because source `0 mod 8` is the identity transition. Genuine first return-fringe collisions cannot terminate with that symbol, so that particular obstruction is eliminated.

The next useful target is to classify the transition action of the allowed final-symbol sets

\[
\{3,7\}\quad(G\text{ odd}),
\qquad
\{1,2,5,6\}\quad(G\text{ even}),
\]

together with the boundary defect `epsilon` and the parity/top-bit data already present in the collision theorem. In particular, determine whether genuine collision geometry forces a synchronizing word of bounded length near the end, even though the unrestricted three-state automaton has no universal bounded-suffix synchronization.
