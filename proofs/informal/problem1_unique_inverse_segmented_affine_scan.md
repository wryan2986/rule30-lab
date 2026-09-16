# Problem 1: segmented-affine form of the unique inverse scan

## Context

Run 75 found that the first tested `p=32` doubled-leaf portal requires more than 10,000,000 exact one-column inverse steps before its next zero return. The bottleneck is therefore repeated evaluation of the unique predecessor equation

`b = S y xor (a or y)`

for nonzero `a`.

This note rewrites that predecessor in a form that exposes substantially more structure than a generic Boolean solve.

## Exact local recurrence

Index cyclic words so `(S y)_i = y_{i+1}`. Bit `i` of the predecessor equation is

`b_i = y_{i+1} xor (a_i or y_i)`.

Using

`a_i or y_i = a_i xor ((not a_i) and y_i)`, 

we obtain

\[
y_{i+1}= (\neg a_i)y_i \oplus (b_i\oplus a_i).
\]

Equivalently,

\[
\boxed{
y_{i+1}=\begin{cases}
 b_i\oplus y_i,&a_i=0,\\
 \neg b_i,&a_i=1.
\end{cases}}
\]

Thus a `1` in `a` is a **reset bit**: it destroys all dependence on the incoming value of `y_i` and fixes the next predecessor bit to `not b_i`. A zero in `a` merely propagates the current bit while XORing `b_i`.

This gives another short proof of predecessor uniqueness for `a != 0`: choose any reset position `j` with `a_j=1`; it fixes `y_{j+1}`, and scanning once around the cyclic word determines every remaining bit. No consistency choice remains when the scan returns to the reset.

## Zero-run closed form

Suppose `a_j=1`, followed cyclically by a zero run

`a_{j+1}=...=a_{j+r}=0`.

Then

\[
y_{j+1}=\neg b_j,
\]

and for `1 <= k <= r`,

\[
\boxed{y_{j+k+1}=\neg b_j\oplus b_{j+1}\oplus\cdots\oplus b_{j+k}.}
\]

So the whole predecessor word is a collection of independent prefix-XOR scans of `b`, segmented by the 1-bits of `a`.

## Affine-map composition

Each position acts on one bit by an affine map over `F_2`,

\[
f_i(t)=\alpha_i t\oplus\beta_i,
\qquad
\alpha_i=\neg a_i,
\quad
\beta_i=b_i\oplus a_i.
\]

Composition stays in the same two-parameter family:

\[
(\alpha_2,\beta_2)\circ(\alpha_1,\beta_1)
=(\alpha_2\alpha_1,\;\alpha_2\beta_1\oplus\beta_2).
\]

A reset is exactly an affine map with `alpha=0`. Therefore predecessor evaluation is a **segmented affine prefix scan**, not a general nonlinear solve.

For machine-word periods such as `p=32`, this admits a broadword implementation using a logarithmic number of shift/mask prefix-composition stages (segmented Kogge-Stone style), replacing a per-bit cyclic scan/solver with fixed word operations. It does not reduce the number of CA columns in a >10^7 connector, but it gives a principled exact route to making each column much cheaper while preserving zero-hit detection.

## Limitation / next target

This is not yet the desired multi-column jump operator. The pair update `(a,b)->(y,a)` changes the segmentation mask `a` at every column, so one cannot simply exponentiate a fixed affine map. The useful next algebraic question is whether several consecutive predecessor steps can themselves be represented by a compact composable transducer on `(a,b)`, or whether the reset positions yield a statistic that bounds/predicts the next zero return.

Still, the recurrence materially narrows the implementation problem: the exact inverse column is a reset-segmented XOR scan, and any optimized `p=32` explorer should implement this primitive directly before further brute-force portal work.
