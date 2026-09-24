# Problem 1 — run 238: the Pascal-mask separation conjecture is false

Problem 1 remains open.

## Entry point

Run 237 proved the exact periodic folding threshold for `w=A^k 1_N`,

\[
P_*(k)=2^{\lceil\log_2(N-k)\rceil},
\]

and conjectured that once `O_{r-1}>=P_*(k)`, the Rule-30 forcing family `f_r=x_{r-1} OR x_{r-2}` separates the nonzero folded mask, i.e. some initial state has `S_w[f_r]=1`.

That conjecture is false. The failure is not a numerical accident: at least the first family of counterexamples is exactly the existing non-doubling phenomenon in the edge-order sequence.

## Exact counterexample mechanism at k=0

Take `N=O_{r-1}` and `w=1_N=A^0 1_N`. By the triangular recurrence,

\[
x_r(N)=x_r(0)\oplus \bigoplus_{t=0}^{N-1} f_r(t).
\]

Hence

\[
S_{1_N}[f_r]\equiv0
\]

if and only if the `r`th coordinate returns after `N`, equivalently

\[
O_r=O_{r-1}=N.
\]

But run 237 gives `P_*(0)=N`. Therefore every non-doubling step `O_r=O_{r-1}` is a direct counterexample to

\[
O_{r-1}\ge P_*(k)\Longrightarrow S_{A^k1_N}[f_r]\not\equiv0.
\]

The first interior example in the computed order sequence is

\[
O_4=O_5=8.
\]

Thus with `(r,N,k)=(5,8,0)`, we have `O_4=P_*(0)=8` but

\[
S_{1_8}[f_5]\equiv0.
\]

So nonzero folding is only a necessary condition for possible detection, not sufficient for the actual Rule-30 forcing family.

## Exhaustive checks beyond k=0

I independently enumerated all initial states of the lower prefix for feasible widths using the exact triangular map

- `x'_0=x_0`,
- `x'_1=x_1 XOR x_0`,
- `x'_r=x_r XOR (x_{r-1} OR x_{r-2})` for `r>=2`.

The prefix orders through width 9 were

\[
O_0,\ldots,O_9=1,2,2,4,8,8,16,32,32,64.
\]

Searching Pascal masks at and above their folding threshold found further counterexamples with `k>0`:

- `(r,N,k,P_*)=(5,16,8,8)`;
- `(5,32,24,8)`;
- `(5,64,56,8)`;
- `(8,32,1,32)`;
- `(8,64,32,32)`;
- `(8,128,96,32)`.

The larger-`N` examples at fixed `r` are folding/lifting variants of the same lower-period cancellation, so they should not be counted as independent structure. The important new example is

\[
(r,N,k)=(8,32,1),
\]

where `P_*(1)=32=O_7` yet exhaustive enumeration gives

\[
S_{A1_{32}}[f_8]\equiv0.
\]

This shows that the failure of separation is not confined to the trivial `k=0` order-definition identity.

## Interpretation

Run 237 cleanly separated *automatic periodic cancellation* (`O_{r-1}<P_*(k)`) from the regime where a mask can in principle detect the forcing sequence. This run shows that equality with or passage above the threshold still permits genuinely dynamical cancellation.

So the hoped-for exact classification

\[
S_{A^k1_N}[f_r]\equiv0 \iff O_{r-1}<P_*(k)
\]

is false. The residual cancellations are precisely the interesting objects, not noise to be removed.

The `k=0` identity identifies the first residual cancellation with an order plateau. The `(8,32,1)` example suggests higher Pascal-mask cancellations may encode a hierarchy of stronger plateau/parity phenomena of the type already seen in runs 231–235.

## Corrected next target

Do not attempt to prove the run-237 separation conjecture.

Instead define the **excess annihilation condition**

\[
E(r,N,k):\quad P_*(k)\le O_{r-1}\ \text{and}\ S_{A^k1_N}[f_r]\equiv0.
\]

The next useful task is to classify `E` modulo period folding, beginning with `N=O_{r-1}`. In particular:

1. prove the exact `k=0` equivalence `E(r,N,0) iff O_r=O_{r-1}` (already immediate above);
2. identify what `k=1` means in orbit-parity/order language and determine whether the observed `(r,N)=(8,32)` cancellation follows from a short plateau pattern or is independent;
3. compute a census of minimal excess-annihilation triples `(r,N,k)` for larger feasible widths, recording only masks at their minimal effective period to avoid lifted duplicates.

A structural characterization of these excess cancellations is more relevant to Problem 1 than generic mask separation, because they are exactly the places where Rule 30 has more cancellation than periodicity alone forces.
