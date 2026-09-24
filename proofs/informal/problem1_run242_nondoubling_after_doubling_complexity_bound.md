# Problem 1 — run 242: non-doubling immediately after a doubling

Problem 1 remains open.

This note continues the same run after `problem1_run242_doubling_step_linear_complexity_exact.md`. The first result explained `L_7(32)=17`. The calculation below also explains the next, previously unexplained, value `L_8(32)=26` without exhaustive search for the upper bound.

## Half-block forcing identity

Let `N=2P`. Suppose coordinate `r-1` is an extension of a lower prefix of order `P`, so over an `N` horizon

\[
x_{r-1}=(A,A)\quad\text{or}\quad(A,\bar A),
\]

according as its lower forcing parity `c` is `0` or `1`. Since coordinate `r-2` belongs to that lower prefix, its length-`N` word is

\[
x_{r-2}=(B,B)
\]

for a length-`P` word `B`.

For

\[
f_r=x_{r-1}\lor x_{r-2},
\]

write its two halves as `F_0,F_1`.

If `c=0`, clearly

\[
F_0=F_1=A\lor B.
\]

If `c=1`, then

\[
F_0=A\lor B,\qquad F_1=\bar A\lor B.
\]

Coefficientwise over `F_2`, the elementary Boolean identity

\[
(a\lor b)\oplus(\bar a\lor b)=\bar b
\]

gives the exact half-difference formula

\[
\boxed{F_0\oplus F_1=\bar B.}
\]

Thus the dependence on the complicated half-word `A` disappears completely from the Games–Chan difference.

## Linear complexity of the forcing

Apply the dyadic Games–Chan recursion to the length-`N=2P` forcing word.

For `c=0`, its halves agree, hence

\[
L(F_r)=L(F_0)\le P.
\]

For `c=1`, its halves differ by `\bar B`, hence

\[
\boxed{L(F_r)=P+L(\bar B).}
\]

The cyclic coordinate recurrence gives, for nonzero words,

\[
L(X_r)=L(F_r)+1.
\]

Therefore

\[
\boxed{
L(X_r)\le
\begin{cases}
P+1,&c=0,\\
P+L(\bar B)+1,&c=1.
\end{cases}}
\]

If `L(B)>1`, complementing the word does not change its linear complexity. Indeed the all-one length-`P` word has complexity 1, equivalently `(z+1)`-valuation `P-1`; adding it cannot change the smaller valuation corresponding to a word of complexity greater than 1. Hence

\[
L(\bar B)=L(B)\qquad\text{when }L(B)>1.
\]

This yields the structural upper bound

\[
\boxed{L(X_r)\le P+L(B)+1}
\]

on the complementary-half branch.

## Width 8

For `r=8`, the established orders are

\[
O_6=16,\qquad O_7=32,\qquad O_8=32.
\]

Take `N=32`, `P=16`. Coordinate 7 is exactly a doubling extension over the width-6 prefix, while coordinate 6 supplies the repeated half-word `B`.

The first run-242 theorem gives

\[
\max L(B)=L_6(16)=9.
\]

Therefore every width-8 top-coordinate word satisfies

\[
L(X_8)\le16+9+1=26
\]

on the complementary branch, while the equal-half branch gives only `L(X_8)\le17`. Consequently

\[
\boxed{L_8(32)\le26.}
\]

Run 241's independent exhaustive census exhibited many states attaining complexity 26 (equivalently valuation 6). Combining that witness with the structural upper bound proves

\[
\boxed{L_8(32)=26.}
\]

Thus the formerly unexplained jump

\[
17\longrightarrow26
\]

has a precise source:

\[
\boxed{26=16+9+1.}
\]

The `16` is the Games–Chan half-length contribution, the `9` is the maximal complexity two coordinates below, and the final `1` is the discrete integration from forcing to coordinate word.

## General pattern suggested

Suppose

\[
O_{r-2}=P,\qquad O_{r-1}=2P,
\]

so the preceding extension is a doubling. At horizon `2P`, the calculation above gives for every state on the complementary branch

\[
L(X_r)=P+L(\overline{X_{r-2}^{[P]}})+1,
\]

where `X_{r-2}^{[P]}` is its length-`P` word. Hence, whenever the relevant maximizing state is compatible with the complementary branch,

\[
L_r(2P)\le P+L_{r-2}(P)+1.
\]

For width 8 this bound is sharp.

This is substantially more informative than a generic Hadamard-product estimate: the Rule-30 OR nonlinearity collapses under the dyadic half-difference to the complement of the coordinate two levels below.

## Next target

Test and prove the corresponding recursion across longer order patterns. In particular, iterate the half-difference calculation through runs of `doubling / non-doubling` decisions and determine whether the maximal linear complexity is governed by a two-step recursion involving `L_{r-2}`. The key issue is **compatibility of maximizers**: an upper bound follows immediately, but equality requires a state that simultaneously lies on the complementary branch at level `r-1` and maximizes the lower word complexity. A structural compatibility lemma would turn the observed complexity census into an exact recursion and may constrain which order plateau patterns are possible.