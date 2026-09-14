# Problem 1: return fringe determines the periodic state and the residual commutator core

Status: exact structural reduction. Problem 1 remains open.

## Setup

Let

\[
T(x)=x\oplus((2x)\lor(4x)),\qquad A(x)=T(x)\gg2.
\]

Suppose a finite nonzero word `z` is fixed by `A^p` and write

\[
T^p(z)=2^{2p}z+R,\qquad 0\le R<2^{2p}.
\]

For the long-even-corridor case put

\[
G=2D\ge4,\qquad L=\operatorname{bitlength}(R)=2p-G,
\]

and

\[
n=p-D=L/2.
\]

The first boundary-collision row is

\[
x=T^{D+1}(z).
\]

The commutator state from the previous notes is

\[
d_0=0,\qquad d_{j+1}=F(d_j,s_j),\qquad s_j=T(A^j x)\bmod8,
\]

with reachable states `d_j in {0,1,3}`.

## 1. `T` is triangular and bijective modulo every power of two

Writing `x_i` for bit `i` of `x`,

\[
(Tx)_i=x_i\oplus(x_{i-1}\lor x_{i-2}),
\]

where negative-index bits are zero.

Therefore `(Tx)_i` is `x_i` xor a function of lower bits only. Given the output bits from low to high, `x_i` is recovered recursively. Hence for every `M>=1`,

\[
\boxed{T:\mathbb Z/2^M\mathbb Z\to\mathbb Z/2^M\mathbb Z\text{ is a bijection}.}
\]

The same is true of every iterate `T^p`.

## 2. The low `2p` bits uniquely determine an `A^p`-fixed configuration

Put `m=2p`. Iterating the triangular bit relation preserves the diagonal bit, so for every position `k`,

\[
(T^p x)_k=x_k\oplus\Phi_{p,k}(x_0,\ldots,x_{k-1})
\]

for some Boolean function `Phi` involving only lower bits.

The fixed-point equation `A^p(x)=x` is

\[
(T^p x)_{i+m}=x_i\qquad(i\ge0).
\]

Thus

\[
x_{i+m}=x_i\oplus\Phi_{p,i+m}(x_0,\ldots,x_{i+m-1}).
\]

Once `x_0,...,x_(m-1)` are known, this equation determines `x_m`, then `x_(m+1)`, and so on, uniquely.

Therefore:

\[
\boxed{\text{For fixed }p,\text{ an }A^p\text{-fixed one-sided configuration is uniquely determined by its low }2p\text{ bits}.}
\]

A low `2p`-bit seed may generate an infinite configuration; it corresponds to a finite integer exactly when the deterministic extension eventually becomes all zero.

This explains the run-26 finite-type graph observation: every `2p`-bit state has exactly one legal upward successor. Reachability of zero is an admissibility test, not a choice among multiple upper-boundary paths.

## 3. The full return fringe `R` uniquely determines `z`

Reduce the return equation modulo `2^(2p)`:

\[
R\equiv T^p(z)\pmod{2^{2p}}.
\]

Because `T^p` is bijective modulo `2^(2p)`,

\[
z\bmod2^{2p}=T^{-p}(R)\bmod2^{2p}
\]

is uniquely determined by `R`.

By the fixed-point extension result above, those low `2p` bits uniquely determine the entire `A^p`-fixed configuration. Consequently:

\[
\boxed{\text{For fixed }p,\text{ a return fringe }R\text{ can belong to at most one }A^p\text{-fixed configuration }z.}
\]

In particular, there is no independent finite high-boundary path left to classify after the complete fringe is fixed. The path is encoded by `R`.

## 4. The unresolved long-even history bit is intrinsic to the fringe

Now assume `G=2D>=4` and `R` begins with `11`, the only even-corridor case left unsynchronized by the previous notes.

Recall

\[
L=2n,\qquad n=p-D.
\]

Reduce the return equation modulo `2^L`. Since `T` is bijective modulo `2^L`,

\[
z\equiv T^{-p}(R)\pmod{2^L}.
\]

Therefore the collision row satisfies

\[
\begin{aligned}
x=T^{D+1}(z)
&\equiv T^{D+1-p}(R)\pmod{2^L}\\
&=T^{1-n}(R)\pmod{2^L}.
\end{aligned}
\]

Define the intrinsic fringe preimage

\[
\boxed{y_R:=T^{1-n}(R)\pmod{2^{2n}}.}
\]

To compute `d_(n-1)`, only source symbols `s_0,...,s_(n-2)` are needed. The low three bits of `A^j(x)` depend only on input bits of `x` through position `2j+2`. For `j<=n-2`,

\[
2j+2\le2n-2<L.
\]

Hence those source symbols depend only on `x mod 2^L`, and therefore only on `y_R`.

Define the **fringe-core commutator state**

\[
\boxed{
C_n(R):=d_{n-1}
}
\]

by starting from `d_0=0` and driving the three-state automaton for `n-1` steps using

\[
s_j=T(A^j y_R)\bmod8,\qquad 0\le j\le n-2.
\]

Then for every genuine collision with this fringe,

\[
\boxed{d_{p-D-1}=C_n(R).}
\]

Thus the one history bit left open in runs 25-26 is not high-boundary information. It is an intrinsic finite computation on the fringe itself.

## 5. Exact final-state formula for `11`-leading even corridors

The previous even-corridor sharpening proved that when `R` begins `11`,

\[
s_{p-D-1}=5,
\]

followed by `D-1` further copies of source `5` and then a terminal source in `{1,5}`.

Source `5` maps

\[
0\mapsto1,\qquad1\mapsto0,\qquad3\mapsto1.
\]

Thus after the first `5`, the state is

\[
h=d_{p-D}=\mathbf 1_{C_n(R)\ne1}.
\]

All remaining `D` source symbols act as swaps on `{0,1}`: the `D-1` forced `5`s and the final symbol, which is either `1` or `5` and acts identically on `{0,1}`. Therefore

\[
\boxed{
d_p=\mathbf 1_{C_n(R)\ne1}\oplus(D\bmod2).
}
\]

This is the exact fringe-only replacement for the unresolved run-25 history bit.

For comparison, if `R` begins `10`, the preceding source is the synchronizer `6`, so the already-known formula is

\[
\boxed{d_p=1\oplus(D\bmod2).}
\]

Hence every long even collision has an explicit terminal commutator state computable from `(D,R)` alone.

## 6. Computational consequence and p=8 pattern

The run-26 finite-type data are consistent with the theorem. For exact period `p=8`, every admissible `11`-leading even corridor is uniquely reconstructed from its fringe.

For the 50 exact-period-eight cases with `G=4`, the final state has an especially simple empirical classification:

\[
\boxed{
d_8=1\iff R\text{ begins }1100.
}
\]

The other observed four-bit prefixes `1101`, `1110`, and `1111` all give `d_8=0`.

Across the smaller samples with `G=6,8,10`, the same prefix split appears with the parity flip predicted by the boxed formula above: `1100` selects one core branch and the other `11xx` prefixes select the other branch. This is computational evidence only; no period-independent four-bit-prefix theorem is claimed here.

## 7. Research consequence

Run 26 proposed looking for an invariant involving both the fringe and an independent finite upper-boundary path. The uniqueness theorem shows that these are not independent variables.

The sharper remaining target is:

1. understand the intrinsic fringe-core function `C_n(R)`;
2. determine whether `C_n(R)=1` admits a bounded-prefix/suffix characterization on *admissible* return fringes;
3. if not, treat `C_n` as a finite transducer on the inverse-normalized fringe and connect that transducer directly to the existing FULL/common-origin or residence-growth arguments.

The important reduction is that the exceptional long-even problem is now entirely internal to `R`; reconstructing the very large periodic word `z` is unnecessary.