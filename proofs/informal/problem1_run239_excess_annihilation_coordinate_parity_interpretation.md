# Problem 1 — run 239: excess Pascal annihilation is a coordinate-parity hierarchy

Problem 1 remains open.

## Entry point

Run 238 disproved the naive separation conjecture and isolated the first positive-`k` excess annihilation

\[
(r,N,k)=(8,32,1),\qquad S_{A1_{32}}[f_8]\equiv0,
\]

where `f_r(t)=x_{r-1}(t) OR x_{r-2}(t)` and `N=O_7=32`.

The immediate question was whether this is a genuinely new nonlinear cancellation or an existing orbit-parity condition in disguise.

## Exact transform identity

For the coordinate recurrence

\[
x_r(t+1)=x_r(t)\oplus f_r(t),
\]

run 234's mask transform gives, for every finite mask `u`,

\[
S_u[x_r]=\operatorname{parity}(u)x_r(0)\oplus S_{Au}[f_r].
\]

Take `u=A^{k-1}1_N`. For `N=2^m` and `1<=k<=N-1`,

\[
\operatorname{parity}(A^{k-1}1_N)=\binom{N}{k}\pmod2=0.
\]

Therefore

\[
\boxed{S_{A^k1_N}[f_r]=S_{A^{k-1}1_N}[x_r]}
\]

for every `1<=k<=N-1`.

Thus positive-`k` excess annihilation is exactly a hierarchy of Pascal-masked parity identities for the *next coordinate itself*.

## k=1 is ordinary orbit parity

At `k=1`, `A^0 1_N=1_N`, so

\[
\boxed{S_{A1_N}[f_r]=\bigoplus_{t=0}^{N-1}x_r(t).}
\]

If `N=O_{r-1}=O_r`, this is exactly the full-orbit top-coordinate parity

\[
p_r=\bigoplus_{t=0}^{O_r-1}x_r(t).
\]

Hence on an order plateau,

\[
\boxed{E(r,N,1)\iff p_r\equiv0.}
\]

In particular, the run-238 example `(r,N,k)=(8,32,1)` is not an independent new type of cancellation: since `O_7=O_8=32`, it is precisely

\[
p_8\equiv0.
\]

It is still structurally nontrivial, because the known length-three plateau theorem does not force it: the local order pattern is `O_7=O_8=32`, followed by `O_9=64`.

## Census at minimal horizon N=O_{r-1}

I exhaustively enumerated all lower-prefix states for feasible widths and tested all `0<=k<=N-2`, keeping the horizon at its minimal natural value `N=O_{r-1}` so lifted duplicates are excluded.

Using

\[
O_0,\ldots,O_9=1,2,2,4,8,8,16,32,32,64,
\]

the excess-annihilating `k` values are:

| r | N=O_{r-1} | k with S_{A^k1_N}[f_r] identically zero |
|---|---:|---|
| 2 | 2 | 0 |
| 3 | 2 | none |
| 4 | 4 | none |
| 5 | 8 | 0 |
| 6 | 8 | none |
| 7 | 16 | none |
| 8 | 32 | 0,1,2,3,4,5,6 |
| 9 | 32 | none |

The striking point is that width 8 does not merely have the `k=1` parity cancellation. It has a consecutive block

\[
\boxed{k=0,1,2,3,4,5,6}
\]

of excess Pascal annihilations, while `k=7` is already nonzero for some state.

By the transform theorem, the positive part is equivalently

\[
S_{A^j1_{32}}[x_8]\equiv0\qquad (j=0,1,2,3,4,5),
\]

with the next Pascal-weighted coordinate parity failing.

This is a substantially stronger finite pattern than the isolated `k=1` example suggested.

## Interpretation

The excess-annihilation problem can now be reframed without the nonlinear OR forcing for every positive mask level:

- `k=0` measures whether the new coordinate doubles the prefix order;
- `k=1` measures ordinary top-coordinate orbit parity (when the order does not double);
- `k>=2` measures successively Pascal-weighted time parities of that coordinate.

So the width-8 phenomenon is a deep zero of a Pascal-moment hierarchy, not seven unrelated forcing cancellations.

This also explains why attempting to prove generic forcing separation was too strong: the coordinate sequence can have several vanishing Pascal moments even after periodic folding becomes nontrivial.

## Next target

Define the Pascal parity depth on a plateau `O_{r-1}=O_r=N` by

\[
d_r=\max\{d:\ S_{A^j1_N}[x_r]\equiv0\text{ for }0\le j<d\}.
\]

The data give `d_5=0` (ordinary parity is nonzero for some state) but `d_8>=6`, in fact the forcing census above gives exactly six consecutive vanishing coordinate masks before failure.

The next useful task is to derive `d_r` from the triangular recurrence or from Boolean derivatives, beginning with why width 8 has six vanishing Pascal moments. A theorem bounding or recursively propagating this depth would classify the positive-`k` excess cancellations and may connect directly back to restrictions on order plateaus.
