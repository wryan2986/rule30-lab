# Problem 1 — run 236: plateau position bound from the terminal Pascal mask

Problem 1 remains open.

## Context

Run 235 proved the two-coordinate descent

\[
S_{A^k1_N}[f_r]\equiv0\Longrightarrow S_{A^{k+j}1_N}[f_{r-2j}]\equiv0
\]

as long as the descended Pascal masks have even parity. A three-level constant-order plateau

\[
O_{s-1}=O_s=O_{s+1}=N
\]

starts this tower at

\[
S_{A1_N}[f_{s-1}]\equiv0.
\]

The previous handoff asked whether the bottom boundary gives a contradiction or an automatic identity. The answer is: the very bottom `f_2` is automatic, but the last even Pascal mask already gives a contradiction at every `f_r` with `r>=3`. This yields a quantitative restriction on where a three-level plateau can occur.

## Lemma 1: the last even Pascal mask is two adjacent ones

Let `N=2^m`. Run 234 gives

\[
(A^k1_N)_u=\binom{N-1-u}{k}\pmod2.
\]

For `k=N-2`, the binomial coefficient can be nonzero only for `u=0,1`. At those two positions it equals

\[
\binom{N-1}{N-2}=N-1\equiv1\pmod2,
\qquad
\binom{N-2}{N-2}=1.
\]

Hence

\[
\boxed{A^{N-2}1_N=(1,1,0,\ldots,0).}
\]

This mask is even, as required by the run-235 descent.

## Lemma 2: `S_{A^{N-2}1_N}[f_r]` cannot vanish identically for `r>=3`

For this mask,

\[
S_{A^{N-2}1_N}[f_r]=f_r(0)\oplus f_r(1).
\]

Recall

\[
f_r=x_{r-1}\lor x_{r-2}.
\]

For every `r>=3`, choose the initial state with `x_{r-3}=1` and every other coordinate through `r-1` equal to zero. (For `r=3`, this means `x_0=1,x_1=x_2=0`.) Initially

\[
f_r(0)=0.
\]

After one update, `x_{r-2}` becomes `1`: for `r=3`, `x_1'=x_1\oplus x_0=1`; for `r>=4`,

\[
x_{r-2}'=x_{r-2}\oplus(x_{r-3}\lor x_{r-4})=1.
\]

Therefore `f_r(1)=1`, and

\[
\boxed{S_{A^{N-2}1_N}[f_r]=1}
\]

on this explicit state. Thus the all-state identity is impossible for every `r>=3`.

## Theorem: quantitative position bound for a three-level plateau

Assume `N>=4` and

\[
O_{s-1}=O_s=O_{s+1}=N.
\]

Run 235 starts with exponent `k=1` at forcing coordinate `r=s-1`. Descend `j=N-3` times. Every intermediate mask exponent is at most `N-2`, hence has even parity, so all descent steps are valid. We obtain

\[
S_{A^{N-2}1_N}[f_{s-1-2(N-3)}]\equiv0.
\]

The terminal forcing coordinate is

\[
r=s-2N+5.
\]

If `s>=2N-2`, then `r>=3`, contradicting Lemma 2. Consequently

\[
\boxed{s\le 2N-3.}
\]

Equivalently, if three consecutive prefix orders are equal to `N`, their middle/right indexing cannot occur arbitrarily far out: a plateau

\[
O_{s-1}=O_s=O_{s+1}=N
\]

requires `s<2N-2`.

This is the first quantitative restriction extracted from the Pascal-mask descent rather than another equivalent cancellation criterion.

## Boundary check: why `f_2` itself gives no contradiction

The exact boundary dynamics are

- `x_0'=x_0`,
- `x_1'=x_1 XOR x_0`,
- `f_2=x_1 OR x_0`.

If `x_0=0`, then `f_2(t)=x_1(0)` is constant. If `x_0=1`, then `f_2(t)=1` is constant. Therefore for every even mask `w`,

\[
S_w[f_2]\equiv0.
\]

So a descent that reaches `f_2` genuinely terminates automatically. The contradiction above comes one stage earlier: the special last-even mask `(1,1,0,...)` cannot annihilate any interior forcing `f_r`, `r>=3`.

## Significance and remaining obstruction

The theorem does not yet solve Problem 1. Since `N=O_s` can itself be large, `s\le2N-3` is far too weak by itself to bound the order exponent `m_s=\log_2N` in the direction needed for the prize problem. But it is genuine new leverage: a length-three constant-order plateau now has a proved position/order inequality.

The next target should be to use earlier Pascal masks, not just `A^{N-2}1_N`, to derive stronger non-annihilation criteria for `f_r`. In particular, classify for each `k` the smallest coordinate `r` for which `S_{A^k1_N}[f_r]` can vanish identically. Any lower bound growing substantially faster than `2k` would sharpen the plateau position bound. Computational census at modest `(N,k,r)` should guide the conjecture before attempting another all-depth proof.
