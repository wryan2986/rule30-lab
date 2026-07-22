# Rational 2-adic countermodels for the period-two zero-streak map

Status: complete informal proof of two exact rational 2-adic fixed points and a
finite-truncation shadowing bound, with finite-quotient regression checks. This
is a negative structural result: it identifies what a period-two proof must
use. It does not provide a finite-support counterexample and does not solve
Problem 1.

## 1. The partial zero-streak map

The renewal reduction associates to a normalized inverse word `K` the 2-adic
preimage

\[
x=K^{-1}(0).
\]

Zero emission is equivalent to `x=3 mod 4`. A second zero is possible only in
two cylinders:

\[
\begin{aligned}
x\equiv7\pmod{16}&\quad\Longrightarrow\quad q=u,\\
x\equiv11\pmod{16}&\quad\Longrightarrow\quad q=t.
\end{aligned}
\]

Since the forced low bits are `11`, division by four means `(x-3)/4`, not an
ambiguous 2-adic right shift. The two branches are therefore

\[
\begin{aligned}
Z_u(x)&=U\!\left(P\!\left(\frac{x-3}{4}\right)\right),
&&x\equiv7\pmod{16},\\
Z_t(x)&=T\!\left(P\!\left(\frac{x-3}{4}\right)\right),
&&x\equiv11\pmod{16}.
\end{aligned}
\]

The maps `T`, `P`, and `U` are the unit-triangular 2-adic isometries from the
inverse-section development.

## 2. Two exact fixed points

Use the already-proved exact 2-cycle

\[
T(-1/3)=1/3,
\qquad
T(1/3)=-1/3.
\]

Both `-1/3` and `1/3` are odd. On odd inputs, `P=U=J circ T`, where `J`
toggles the low bit. Hence

\[
P(-1/3)=U(-1/3)=-2/3.
\]

The even input `-2/3=2(-1/3)` satisfies

\[
P(-2/3)=1+2U(-1/3)=-1/3,
\]

using the exact section identity `P(2R)=1+2U(R)`. Also

\[
U(-2/3)=1+2T(-1/3)=5/3.
\]

### Constant-`u` branch

The rational `5/3` satisfies

\[
5/3\equiv7\pmod{16}
\]

and

\[
\frac{5/3-3}{4}=-1/3.
\]

Therefore

\[
Z_u(5/3)
=U(P(-1/3))
=U(-2/3)
=5/3.
\]

### Constant-`t` branch

The rational `1/3` satisfies

\[
1/3\equiv11\pmod{16}
\]

and

\[
\frac{1/3-3}{4}=-2/3.
\]

Therefore

\[
Z_t(1/3)
=T(P(-2/3))
=T(-1/3)
=1/3.
\]

Thus

\[
\boxed{Z_u(5/3)=5/3,
\qquad Z_t(1/3)=1/3.}
\]

These are infinite-support 2-adic states. Neither is an ordinary nonnegative
integer.

## 3. Uniqueness inside each constant branch

Suppose `x` and `y` lie in the same branch cylinder. Removing the common low
block gives

\[
v_2\!\left(\frac{x-3}{4}-\frac{y-3}{4}\right)
=v_2(x-y)-2.
\]

Because `P` and the selected `Q in {T,U}` are 2-adic isometries,

\[
\boxed{v_2(Z_Q(x)-Z_Q(y))=v_2(x-y)-2.}
\]

If two distinct points in one cylinder were fixed, the left side would equal
`v_2(x-y)`, contradicting the displayed identity. Therefore `5/3` and `1/3`
are the unique fixed points in their respective constant-branch cylinders.

The map is expanding in the 2-adic metric by a factor of four. That does not
prevent a fixed point; it makes the fixed point unique and makes nearby finite
truncations eventually leave its branch.

## 4. Finite truncations shadow for arbitrarily long

Let `x_*` be either fixed point and let `x_N` be its least nonnegative residue
modulo `2^N`. Initially

\[
v_2(x_N-x_*)\ge N.
\]

As long as the same branch is followed, each zero step loses exactly two bits
of agreement. Before step `j`, the agreement is at least `N-2j`. The branch
cylinder is determined by four low bits, so the constant branch is guaranteed
whenever

\[
N-2j\ge4.
\]

Consequently the ordinary finite truncation follows the rational fixed point
for at least

\[
\boxed{\left\lfloor\frac{N-4}{2}\right\rfloor+1}
\]

zero-emitting steps.

This lower bound tends to infinity with `N`. Therefore there can be no uniform
finite zero-run bound over all ordinary finite integers derived only from a
fixed low-bit horizon of this partial map.

The truncations still terminate or leave the constant branch eventually. They
are finite counterexample leads to a *uniform bounded-run claim*, not
counterexamples to the desired infinite-support theorem.

## 5. Consequence for the proof program

The zero-streak integer map on the full 2-adic space admits exact infinite
orbits. Therefore none of the following can finish the period-two argument by
itself:

- compactness of the low-residue survivor sets;
- absence of short ordinary-integer cycles;
- a uniform bound inferred from finite quotient depth;
- a low-bit ranking function that ignores eventual-zero high support; or
- the statement that the zero map expands bit length.

A successful proof must distinguish ordinary eventually-zero binary expansions
from the rational fixed points, or show that the actual moving-fringe schedule
cannot match the branch sequence required by any infinite zero orbit.

The next admitted target is therefore a **support/schedule cocycle**: a quantity
that couples the high zero tail or the autonomous period-two fringe to the
normalized integer orbit. Longer zero-run searches alone are now explicitly
non-admissible.
