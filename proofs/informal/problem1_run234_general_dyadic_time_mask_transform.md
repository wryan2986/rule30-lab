# Problem 1 — run 234: general dyadic time-mask transform

Problem 1 remains open.

## Context

Run 233 showed that expanding the even-time parity does not produce pure quarter-time sampling. Instead the lower forcing is weighted by the periodic mask `1100`. This note gives the exact general transform behind that phenomenon.

Let a binary trajectory satisfy

\[
y(t+1)=y(t)\oplus f(t),\qquad 0\le t<N,
\]

and let `w=(w_0,...,w_{N-1})` be a binary time mask. Define

\[
S_w[y]=\bigoplus_{t=0}^{N-1} w_t y(t).
\]

## Theorem 1: exact mask transform

Define the strict suffix-parity transform

\[
(Aw)_s=\bigoplus_{t=s+1}^{N-1}w_t,\qquad 0\le s<N.
\]

Then

\[
\boxed{S_w[y]=\left(\bigoplus_{t=0}^{N-1}w_t\right)y(0)\oplus S_{Aw}[f].}
\]

In particular, whenever `w` has even Hamming parity, the initial bit disappears and the masked parity of `y` is exactly the transformed masked parity of its forcing.

### Proof

Use

\[
y(t)=y(0)\oplus\bigoplus_{s=0}^{t-1}f(s)
\]

inside `S_w[y]` and interchange the finite XOR sums. The coefficient of `y(0)` is the parity of `w`; the coefficient of `f(s)` is precisely the XOR of all `w_t` with `t>s`.

## Theorem 2: closed form for repeated transforms of the full mask

Let `1_N` denote the all-one mask of length `N`. For every integer `k>=1`,

\[
\boxed{(A^k1_N)_s=\binom{N-1-s}{k}\pmod2.}
\]

### Proof

For `k=1`, `(A1_N)_s=N-1-s (mod 2)=binom(N-1-s,1)`. More generally the matrix entries of `A^k` are

\[
(A^k)_{s,t}=\binom{t-s-1}{k-1}\pmod2\qquad(t>s),
\]

because a contribution corresponds to choosing `k-1` intermediate indices strictly between `s` and `t`. Summing over `t>s` and using the hockey-stick identity gives

\[
\sum_{t=s+1}^{N-1}\binom{t-s-1}{k-1}=\binom{N-1-s}{k}.
\]

## Corollary: powers of two give exact dyadic block masks

Suppose `N=2^m` and `0<=j<m`. Set `k=2^j`. Lucas' theorem mod 2 gives

\[
\binom{N-1-s}{2^j}\equiv \text{bit}_j(N-1-s)\pmod2.
\]

Since `N-1` is `m` binary ones, `N-1-s` is the `m`-bit complement of `s`. Hence

\[
\boxed{(A^{2^j}1_N)_s=1\oplus \text{bit}_j(s).}
\]

Thus `A^{2^j}1_N` is exactly the periodic block mask

\[
\boxed{1^{2^j}0^{2^j}1^{2^j}0^{2^j}\cdots.}
\]

Examples:

- `A 1_N = 101010...`;
- `A^2 1_N = 11001100...`;
- `A^4 1_N = 11110000 11110000...`;
- `A^8 1_N = 11111111 00000000 ...`.

This exactly explains both run 228's even-time mask and run 233's `1100` mask: they are the first two members of one binomial/Pascal hierarchy.

## General masks are Pascal/Sierpinski masks

For arbitrary `k`, the mask is not generally a single rectangular block wave; it is

\[
\boxed{w^{(k)}_s=\binom{N-1-s}{k}\bmod2.}
\]

By Lucas' theorem, `w^{(k)}_s=1` exactly when every 1-bit of `k` is also a 1-bit of `N-1-s`. Therefore the entire hierarchy is explicit and has the usual mod-2 Pascal/Sierpinski structure.

## Consequence for the plateau program

The time-mask side of the proposed descent is no longer an unknown. There is no need to rediscover masks by hand or expand explicit powers of the edge automaton. Whenever a plateau argument supplies a masked parity of a coordinate and that mask has even parity, one descent through

\[
x_r(t+1)=x_r(t)\oplus f_r(t)
\]

applies `A` to the mask. Repeated legal descents are governed exactly by the binomial masks above.

What remains nontrivial is **state-coordinate descent**: `f_r=x_{r-1}\lor x_{r-2}` is nonlinear, so a mask identity for `f_r` is not automatically a mask identity for a single lower coordinate. The next useful target is therefore not further time-mask algebra; that part is solved. Instead, analyze under which plateau/derivative hypotheses a masked OR-forcing identity can be converted into a masked parity identity for `x_{r-1}` or `x_{r-2}`. If that conversion can be iterated, the explicit `A^k` formula supplies the complete time structure.

## Dead-end avoidance

Do not spend further runs deriving the `1010`, `1100`, `11110000`, etc. masks separately. They are all instances of `A^k 1_N`, with the exact binomial formula above. The unresolved obstruction is the nonlinear OR forcing, not the temporal mask transform.