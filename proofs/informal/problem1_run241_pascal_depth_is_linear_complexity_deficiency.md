# Problem 1 — run 241: Pascal depth is linear-complexity deficiency

Problem 1 remains open.

## Entry point

Run 240 identified the Pascal parity depth of an `N=2^m` periodic coordinate word

\[
X_r(z)=\sum_{t=0}^{N-1}x_r(t)z^t
\]

with its `(z+1)`-adic valuation

\[
\delta=\nu_{z+1}(X_r).
\]

It proposed studying how coefficientwise (Hadamard) multiplication acts on that filtration. This run gives a cleaner interpretation and also records a sharp warning about the generic Hadamard route.

## Exact reinterpretation by linear complexity

For a binary sequence of period `N=2^m`, the standard generating-polynomial formula for linear complexity is

\[
L(X)=N-\gcddeg(X(z),z^N-1).
\]

Since over `F_2`

\[
z^N-1=(z+1)^N,
\]

and `\gcd(X,(z+1)^N)=(z+1)^{\nu_{z+1}(X)}` for a nonzero word, we obtain the exact identity

\[
\boxed{L(X)=N-\nu_{z+1}(X).}
\]

Thus the invariant introduced in runs 239–240 is not a new ad hoc quantity:

\[
\boxed{\text{Pascal parity depth}=N-\text{linear complexity}.}
\]

When an identity is required for every initial state, the minimum Pascal depth is equivalently `N` minus the maximum linear complexity attained by the corresponding coordinate word.

This reframes the width-8 observation `delta_8(32)=6` as

\[
\boxed{\max_x L(x_8(0),\ldots,x_8(31))=26.}
\]

The forcing relation from run 240,

\[
zF_r=(1+z)X_r,
\]

also becomes

\[
\boxed{L(F_r)=L(X_r)-1}
\]

for every nonzero cyclic word (with the zero-word case handled separately).

## Exact small-width census at horizon 32

I independently enumerated all `2^{r+1}` prefix states under the established triangular recurrence

\[
x_0'=x_0,\qquad x_1'=x_1\oplus x_0,\qquad
x_r'=x_r\oplus(x_{r-1}\lor x_{r-2})\quad(r\ge2),
\]

recording each top-coordinate word for 32 time steps and computing its first nonzero Hasse/Pascal moment. The minimum valuations, hence maximum linear complexities, are:

| `r` | min `nu_{z+1}(X_r)` over states | max linear complexity `32-nu` |
|---:|---:|---:|
| 2 | 30 | 2 |
| 3 | 29 | 3 |
| 4 | 27 | 5 |
| 5 | 24 | 8 |
| 6 | 23 | 9 |
| 7 | 15 | 17 |
| 8 | 6 | 26 |

The width-8 value exactly reproduces run 239's depth six by an independent calculation.

The full valuation distributions also showed nested high valuations rather than a single exceptional state family. For `r=8`, the nonzero minimum layers begin

`nu = 6,15,23,24,27,29,30,31,32`,

with 128 states attaining the minimum `nu=6`. So the depth-six phenomenon is robust across a quarter of the 512 prefix states, not a lone witness.

## Generic Hadamard valuation bounds are too weak

Run 240 suggested bounding

\[
\nu(A+B+A\odot B)
\]

from the valuations of `A,B`. A positive lower bound for `A\odot B` from the two input valuations alone already fails badly.

For example, at any cyclic length `N>=4`, let

\[
A=1+z,\qquad B=z+z^2=z(1+z).
\]

Both have

\[
\nu_{z+1}(A)=\nu_{z+1}(B)=1,
\]

but coefficientwise multiplication gives

\[
A\odot B=z,
\]

so

\[
\boxed{\nu_{z+1}(A\odot B)=0.}
\]

The failure persists much deeper. At `N=32`, direct checks with cyclic shifts of the generator `(1+z)^d` give pairs `A,B` with both valuations at least `d` but `nu(A odot B)=0` for every tested `d=1,...,15`. In particular, even depth six by itself imposes no positive Hadamard-product depth.

Therefore a proof of the Rule-30 depth cannot come from a generic inequality depending only on `nu(A)` and `nu(B)`. It must use the special dynamical relation between adjacent coordinate words.

## Why the linear-complexity formulation is useful

There is a substantial existing algebraic toolkit for periodic binary sequences phrased in terms of linear complexity, connection polynomials, Games–Chan style dyadic recursion, and complexity of sums/products. The Rule-30 problem can now be asked in that language without carrying the Pascal-mask machinery explicitly.

For a fixed horizon/order `N=2^m`, define

\[
L_r(N)=\max_{\text{prefix states}}L(X_r).
\]

The computed `N=32` row is

\[
L_2,\ldots,L_8=2,3,5,8,9,17,26.
\]

The open structural question is to bound or recursively determine `L_r(N)` using the fact that adjacent words are not arbitrary sequences but satisfy

\[
(1+z)X_{r-1}=z\,(X_{r-2}\lor X_{r-3})
\]

and the analogous relation one level below.

## Next target

Do not pursue valuation-only inequalities for arbitrary Hadamard products; the explicit counterexample above shows that route loses the needed information.

Instead, derive a dyadic linear-complexity recursion for the *adjacent Rule-30 pair* `(X_{r-1},X_{r-2})`. The immediate benchmark is to explain the exact jump

\[
L_7(32)=17\longrightarrow L_8(32)=26
\]

while preserving the forced relation `L(F_8)=25`. A successful adjacent-pair recursion could turn plateau constraints into upper bounds on attainable linear complexity, equivalently lower bounds on Pascal depth.