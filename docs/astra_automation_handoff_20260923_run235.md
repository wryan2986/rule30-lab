# Astra automation handoff — 2026-09-23 run 235

Problem 1 remains OPEN.

## Entry state

Entered from run 234, commit `a876edf1b70164c10c5278544ccd2412a2d1391f`. No intervening repository work was present.

Run 234 solved the temporal mask transform but left the nonlinear OR-to-coordinate conversion as the next obstruction.

## New result

Added:

- `proofs/informal/problem1_run235_masked_or_derivative_descent.md`

For `f_r=x_{r-1} OR x_{r-2}` and arbitrary finite time mask `w`, proved

`D_{e_{r-1}} S_w[f_r] = parity(w) XOR S_w[x_{r-2}]`.

Hence for even `w`, an all-state identity `S_w[f_r]=0` forces `S_w[x_{r-2}]=0`. Combining with the run-234 recurrence transform gives the exact two-coordinate descent

`S_w[f_r]=0  =>  S_{Aw}[f_{r-2}]=0`.

For `N=2^m`, the Pascal masks `A^k 1_N` have parity `C(N,k+1) mod 2`, hence are even for `0 <= k <= N-2`. Therefore

`S_{A^k 1_N}[f_r]=0 => S_{A^{k+j}1_N}[f_{r-2j}]=0`

through every valid lower coordinate (subject to `k+j <= N-2`).

Applying this to run 231: a three-level constant-order plateau already yields `S_{A1_N}[f_{s-1}]=0`, so that *single* plateau condition propagates an entire tower of lower-coordinate Pascal-mask cancellations. No new plateau hypothesis is needed at each level.

## Next target

Do not derive more interior masks individually. Inspect the exact bottom-coordinate/boundary recurrence and push the new descent all the way to the lowest valid forcing `f_r`. Determine whether the resulting boundary masked identity is contradictory, automatic, or depends on the Pascal exponent. This is now the most direct route to converting the descent theorem into a restriction on possible order plateaus.
