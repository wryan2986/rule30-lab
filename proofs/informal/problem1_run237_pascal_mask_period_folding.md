# Problem 1 — run 237: Pascal-mask folding over power-of-two periods

Problem 1 remains open.

## Context

Run 236 suggested classifying earlier Pascal masks `A^k 1_N` to see whether they can contradict an all-state forcing cancellation earlier than the terminal mask `A^{N-2}1_N=(1,1,0,...)`.

There is an exact periodicity obstruction that should be accounted for before looking for such witnesses. Every forcing sequence

\[
f_r(t)=x_{r-1}(t)\lor x_{r-2}(t)
\]

has period dividing the lower-prefix order `O_{r-1}`. Therefore a time mask can annihilate `f_r` for a completely formal reason: its XOR-folding modulo that period may be zero. For the Pascal masks this folding threshold can be computed exactly.

## Setup

Let

\[
N=2^M,\qquad w^{(k)}=A^k1_N,
\]

so by run 234

\[
w^{(k)}_t=\binom{N-1-t}{k}\pmod2,
\qquad 0\le t<N.
\]

For a power-of-two period `P=2^p` dividing `N`, define the folded mask

\[
(F_Pw)_a=\bigoplus_{0\le t<N\atop t\equiv a\pmod P}w_t,
\qquad 0\le a<P.
\]

If `z(t)` is `P`-periodic, then

\[
S_w[z]=S_{F_Pw}[z|_{0,\ldots,P-1}].
\]

Thus `F_Pw=0` implies that `w` annihilates every `P`-periodic sequence.

## Theorem: exact folding threshold

For `0\le k\le N-2`, put

\[
P_*(k)=2^{\lceil\log_2(N-k)\rceil}.
\]

Then for every power of two `P|N`,

\[
\boxed{F_P(A^k1_N)=0\quad\text{whenever }P<P_*(k).}
\]

Moreover at the threshold,

\[
\boxed{F_{P_*(k)}(A^k1_N)\ne0.}
\]

So `P_*(k)` is the smallest power-of-two period on which the Pascal mask can possibly detect a periodic sequence.

### Proof of vanishing below the threshold

Write `P=2^p` and `N=QP`. For a residue `a`, reverse the index by setting `j=N-1-t`. As `t` runs through one residue modulo `P`, `j` runs through one residue `b=N-1-a (mod P)`. Hence

\[
(F_Pw^{(k)})_a
=\bigoplus_{q=0}^{Q-1}\binom{b+qP}{k}\pmod2,
\]

with the understood range `0\le b+qP<N`.

By Lucas' theorem, `binom(j,k)` is odd exactly when every 1-bit of `k` is also a 1-bit of `j`. Split the bits of `j` into the low `p` bits fixed by `b` and the high `M-p` bits supplied by `q`.

If the low bits of `b` fail to contain the low bits of `k`, every summand is zero. Otherwise the allowed `q` are precisely those whose high bits contain the high bits of `k`. Their number is

\[
2^{(M-p)-\operatorname{popcount}(k_{\ge p})}.
\]

Its parity is odd exactly when all `M-p` high bit positions of `k` are 1. Therefore `F_Pw^{(k)}` is nonzero exactly when

\[
k\ge N-P.
\]

Equivalently,

\[
P\ge N-k.
\]

Since `P` is a power of two, the least such `P` is

\[
P_*(k)=2^{\lceil\log_2(N-k)\rceil}.
\]

This proves both claims.

## Corollary for the Rule-30 edge forcing

Because `f_r(t)` depends only on coordinates through `r-1`, its period divides `O_{r-1}`. Therefore

\[
\boxed{O_{r-1}<P_*(k)\Longrightarrow S_{A^k1_N}[f_r]\equiv0.}
\]

This is an automatic identity; no special Rule-30 cancellation is involved.

Consequently an earlier Pascal mask cannot yield a contradiction at coordinate `r` unless

\[
\boxed{O_{r-1}\ge 2^{\lceil\log_2(N-k)\rceil}.}
\]

For the terminal mask `k=N-2`, this threshold is only `2`, which is why run 236 could construct a one-step witness at every interior forcing coordinate `r>=3`.

At the other extreme, for every `k<N/2`, `P_*(k)=N`. Such a mask automatically annihilates every forcing sequence whose lower-prefix order is strictly below the plateau order `N`. Thus the earliest half of the Pascal hierarchy cannot improve run 236 merely by a local non-annihilation argument deep below an `N`-plateau.

## Computational check

Direct folding for `N=8,16,32` agrees exactly with the theorem. Examples for `N=16`:

- `k=1,...,7`: first detectable period `16`;
- `k=8,...,11`: first detectable period `8`;
- `k=12,13`: first detectable period `4`;
- `k=14`: first detectable period `2`.

Independent exhaustive state enumeration at small widths showed the same transition for `S_{A^k1_N}[f_r]`: the observed first non-identically-zero coordinate occurs when the lower-prefix order reaches the folding threshold (checked for `N=4,8,16` over feasible widths). This latter equality is evidence, not yet an all-depth theorem, because nonzero folded mask alone does not prove that the actual family of forcing sequences separates it.

## Significance / corrected next target

Run 236 proposed searching earlier masks for substantially stronger non-annihilation. This theorem shows a hard limitation: much of the apparent vanishing of earlier masks is forced solely by temporal periodicity. Any proof that ignores this folding threshold will rediscover automatic identities rather than new Rule-30 structure.

The useful remaining question is now sharper:

> Separation conjecture: whenever `O_{r-1}>=P_*(k)`, is `S_{A^k1_N}[f_r]` necessarily nonzero for some initial state?

Small exhaustive data support this in the tested range. Proving it would exactly classify Pascal-mask annihilation in terms of prefix order and convert the descent tower into inequalities among the order sequence itself. If false, the first counterexample identifies genuinely nonlinear cancellation beyond periodic folding.
