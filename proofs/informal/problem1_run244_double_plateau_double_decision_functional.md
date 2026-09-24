# Problem 1 — run 244: exact decision functional for double / plateau / double

Problem 1 remains open.

Run 243 resolved compatibility after two consecutive doublings.  The next unresolved local order pattern is `double / plateau / double`.  This note derives an exact Boolean functional deciding the final doubling.  It also identifies a strong empirical rigidity that remains to be proved.

## Setup

Assume

\[
O_{r-3}=Q,\qquad O_{r-2}=2Q,\qquad O_{r-1}=2Q,
\]

with `Q` a power of two and `Q>=2`.  Consider a state whose coordinate `r-2` realizes the first doubling.  Over a horizon `2Q`, write

\[
X_{r-2}=(C,\bar C),\qquad X_{r-3}=(B,B).
\]

Let

\[
Y=X_{r-1}=(Y_0,Y_1)
\]

be the plateau coordinate, and define its half-difference word

\[
D:=Y_0\oplus Y_1.
\]

Let `G=f_{r-1}=x_{r-2}\lor x_{r-3}` be the forcing of the plateau coordinate.

## The plateau half-difference is an integral of the lower word

Run 242's pointwise OR half-difference identity gives

\[
G_0\oplus G_1=\bar B.
\]

Since `y(t+1)=y(t)\oplus g(t)`, the half-difference satisfies

\[
D(t)=y(t+Q)\oplus y(t).
\]

Taking one time difference,

\[
D(t+1)\oplus D(t)
 =g(t+Q)\oplus g(t)
 =\bar B(t).
\]

Thus

\[
\boxed{\Delta D=\bar B.}
\]

This is the word-level mechanism behind the run-242 plateau complexity formula: when `D` is nonzero, Games–Chan gives

\[
L(Y)=Q+L(D),
\]

and cyclic integration gives `L(D)=L(\bar B)+1` in the nondegenerate cases used previously.

## Exact Boolean identity for the next forcing

Now inspect the forcing of coordinate `r`,

\[
H=f_r=Y\lor X_{r-2}.
\]

At a fixed first-half time let

\[
y=Y_0(t),\quad x=C(t),\quad d=D(t).
\]

Then the corresponding second-half bits are `y+d` and `1+x`.  Using `a OR b = a+b+ab` over `F_2`, one gets the exact pointwise identity

\[
(y\lor x)\oplus((y+d)\lor(1+x))
 =1+y+dx.
\]

Therefore

\[
\boxed{H_0\oplus H_1=1+Y_0+D\odot C,}
\]

where `odot` is coefficientwise product.

The parity over the full `2Q` forcing block is the parity of this half-difference.  Since `Q` is even,

\[
\boxed{
\operatorname{parity}(H)
 =\operatorname{parity}(Y_0)
  \oplus \langle D,C\rangle,
}
\]

with

\[
\langle D,C\rangle=\bigoplus_{t=0}^{Q-1}D(t)C(t).
\]

For a binary skew extension, coordinate `r` doubles the lower orbit exactly when this forcing parity is one.  Hence, on a full-period `2Q` lower orbit,

\[
\boxed{
O_r=4Q
\iff
\operatorname{parity}(Y_0)\oplus\langle D,C\rangle=1.
}
\]

This is the exact local decision functional for the `double / plateau / double` pattern.

## Exhaustive evidence: the decision selects the high-complexity plateau class

Two instances of this pattern are available at feasible widths:

- `O_3,O_4,O_5,O_6 = 4,8,8,16` (`Q=4`);
- `O_6,O_7,O_8,O_9 = 16,32,32,64` (`Q=16`).

Exhaustive enumeration gives a striking split among full-period plateau states:

- at coordinate 5, period-8 states have top-coordinate linear complexity either `5` or `8`; every state that subsequently witnesses the doubling to `O_6=16` lies in the `8` class;
- at coordinate 8, period-32 states have top-coordinate linear complexity either `17` or `26`; every state that subsequently witnesses the doubling to `O_9=64` lies in the `26` class.

Thus in both available cases the bilinear decision functional above rejects the low-complexity plateau branch and selects exactly the maximal-complexity branch.

This is stronger than the generic period argument: a full-period plateau prefix alone does **not** force maximal top-coordinate complexity.

## What is proved and what remains

Proved here:

1. `Delta D = bar(B)` for the plateau half-difference;
2. `H_0 xor H_1 = 1 + Y_0 + D*C` pointwise;
3. the exact final-doubling criterion
   `parity(Y_0) xor <D,C> = 1`;
4. exhaustive verification at the two available `double / plateau / double` instances that final-doubling witnesses all occupy the maximal plateau-complexity class.

The unresolved theorem is now precise: explain why, for **adjacent Rule-30 orbit words**, the functional

\[
\operatorname{parity}(Y_0)\oplus\langle D,C\rangle
\]

can be one only on the high-complexity plateau branch (or find the first counterexample at greater width).  A proof would extend run 243's automatic compatibility result across an intervening plateau and provide a recursive constraint on admissible order-decision words.
