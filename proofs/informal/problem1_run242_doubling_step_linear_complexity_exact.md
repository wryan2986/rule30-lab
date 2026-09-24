# Problem 1 — run 242: exact linear complexity at an order-doubling step

Problem 1 remains open.

## Entry point

Run 241 reinterpreted Pascal depth as linear-complexity deficiency and proposed deriving a dyadic recursion that uses the dynamical relation between adjacent Rule-30 coordinate words. This run obtains an exact recursion at every genuine order-doubling step. It explains the previously unexplained census values `L_7(32)=17` and, at their minimal horizons, the analogous values at earlier doubling steps.

## Setup

Use the established triangular recurrence

\[
x_0'=x_0,\qquad x_1'=x_1\oplus x_0,\qquad
x_r'=x_r\oplus f_r,\qquad f_r=x_{r-1}\lor x_{r-2}.
\]

Let the lower prefix through coordinate `r-1` have order `P=O_{r-1}`. Then `f_r(t)` is `P`-periodic for every initial state. Put

\[
c_r=\bigoplus_{t=0}^{P-1} f_r(t).
\]

Iterating the top-coordinate recurrence through one lower-prefix period gives, for every `t`,

\[
\boxed{x_r(t+P)=x_r(t)\oplus c_r.}
\]

Thus over a `2P` horizon the top-coordinate word has only two possible dyadic forms:

\[
X_r=(A,A)\quad(c_r=0),
\]

or

\[
X_r=(A,\bar A)\quad(c_r=1),
\]

where `A` is the first length-`P` half and `\bar A=A\oplus 1_P`.

## Games–Chan recursion

For a binary word `X=(A,B)` of length `2P`, with `P` a power of two, the standard dyadic linear-complexity recursion is

\[
L_{2P}(A,B)=
\begin{cases}
L_P(A), & A=B,\\
P+L_P(A\oplus B), & A\ne B.
\end{cases}
\]

Apply this to the two forms above.

If `c_r=0`, the halves agree, so

\[
L(X_r)=L(A)\le P.
\]

If `c_r=1`, the halves are complementary, hence

\[
A\oplus\bar A=1_P.
\]

The nonzero constant word has linear complexity `1`, so

\[
\boxed{L(X_r)=P+1.}
\]

Therefore, for every state,

\[
\boxed{L(X_r)\le P+1.}
\]

and equality holds exactly for states with odd full-period forcing parity `c_r=1`.

## Exact theorem at an order doubling

The triangular skew-product order criterion says that the extension from width `r-1` to width `r` doubles precisely when the forcing parity is nonzero for at least one lower-prefix state. Equivalently,

\[
O_r=2O_{r-1}=2P
\]

iff there exists a state with `c_r=1`.

Combining this criterion with the dyadic calculation gives the exact result

\[
\boxed{
O_r=2O_{r-1}=2P
\quad\Longrightarrow\quad
\max_{\text{prefix states}}L(X_r)=P+1=\frac{O_r}{2}+1.
}
\]

Equivalently, at the minimal horizon `N=O_r=2P`, the minimum Pascal depth / `(z+1)`-valuation is

\[
\boxed{
\min_x\nu_{z+1}(X_r)=N-(P+1)=P-1=\frac N2-1.
}
\]

This is exact, not merely a bound.

## Explanation of the run-241 census

The established order sequence begins

\[
1,2,2,4,8,8,16,32,32,64,\ldots
\]

At `r=7`, `O_6=16` and `O_7=32`, so the theorem gives immediately

\[
\boxed{L_7(32)=16+1=17,}
\]

exactly the value found experimentally in run 241.

The same theorem explains the earlier doubling-step maxima at their minimal horizons:

- `O_3=4=2O_2` gives `L_3(4)=3`;
- `O_4=8=2O_3` gives `L_4(8)=5`;
- `O_6=16=2O_5` gives `L_6(16)=9`;
- `O_7=32=2O_6` gives `L_7(32)=17`.

Repeating a shorter periodic word to the run-241 horizon 32 does not change its linear complexity, so these are exactly the census values `3,5,9,17` observed there.

## Consequence for the research direction

The large jumps in linear complexity at genuine order doublings are now completely understood: they are forced by complementary dyadic halves, and their value is always `O_r/2+1`.

Therefore the genuinely difficult cases are the **non-doubling extensions** `O_r=O_{r-1}=N`. At such a step `c_r=0` for every state over the full lower-prefix period `N`, which only says the length-`2N` word would be `(A,A)`; it gives no internal half relation inside the minimal length-`N` word `A`. This is exactly where the width-8 value

\[
L_8(32)=26
\]

lives, since `O_7=O_8=32`.

The next target should therefore be narrowed from a general adjacent-pair complexity recursion to a recursion specifically for a **non-doubling extension immediately after a doubling step**. Here `x_{r-1}` itself has complementary halves over its minimal period, while the lower coordinate `x_{r-2}` has period `N/2`. Those two facts should impose a tractable half-block formula on

\[
f_r=x_{r-1}\lor x_{r-2}
\]

and hence on `X_r`. The immediate benchmark remains deriving `L_8(32)\le26` structurally (and finding a state attaining 26), rather than by exhaustive enumeration.