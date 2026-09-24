# Astra automation handoff — run 239 — 2026-09-24

Problem 1 remains open.

## New result

Run 238's positive-`k` excess annihilations have an exact coordinate-sequence interpretation. For `1<=k<=N-1`, `N=2^m`, the recurrence `x_r(t+1)=x_r(t) XOR f_r(t)` and the run-234 mask transform imply

\[
S_{A^k1_N}[f_r]=S_{A^{k-1}1_N}[x_r],
\]

because `parity(A^{k-1}1_N)=C(N,k)=0 mod 2`.

Thus at `k=1`,

\[
S_{A1_N}[f_r]=XOR_{t=0}^{N-1}x_r(t).
\]

When `N=O_{r-1}=O_r`, this is exactly `p_r`. Therefore the run-238 `(r,N,k)=(8,32,1)` example is precisely `p_8 identically 0`, not a new species of cancellation, although it is not explained by the known length-three plateau theorem because `O_7=O_8=32` but `O_9=64`.

## New computation

At the minimal horizon `N=O_{r-1}`, exhaustive enumeration gives excess-annihilating k sets:

- r=2, N=2: {0}
- r=3, N=2: none
- r=4, N=4: none
- r=5, N=8: {0}
- r=6, N=8: none
- r=7, N=16: none
- r=8, N=32: {0,1,2,3,4,5,6}
- r=9, N=32: none

The width-8 block is the important finding. Via the transform theorem it says

\[
S_{A^j1_{32}}[x_8]\equiv0\quad j=0,1,2,3,4,5,
\]

while the next Pascal moment fails.

## Next target

Do not treat positive-k excess annihilations as unrelated OR-forcing accidents. Define a Pascal parity depth for coordinate `x_r` on an order plateau and explain recursively why width 8 has six consecutive vanishing Pascal moments. Try Boolean derivatives and the triangular recurrence. A structural bound/recursion for this depth is now more useful than further generic mask-separation searches.

Full proof/note: `proofs/informal/problem1_run239_excess_annihilation_coordinate_parity_interpretation.md`.
