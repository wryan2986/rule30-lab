# Astra automation handoff — run 240 — 2026-09-24

Problem 1 remains open.

## New result

Run 239's Pascal parity depth has an exact algebraic interpretation. For an `N=2^m` periodic coordinate word

\[
X_r(z)=\sum_{t=0}^{N-1}x_r(t)z^t,
\]

we have

\[
S_{A^j1_N}[x_r]=0\quad(0\le j<d)
\iff
(z+1)^d\mid X_r(z).
\]

Proof: reverse the word. The mask coefficient is `C(N-1-t,j)`, so the pairing is the `j`th Hasse derivative at 1 of the reversed polynomial. Vanishing of the first `d` Hasse derivatives is exactly root multiplicity `d`; reversal preserves multiplicity at the nonzero root 1.

Thus Pascal depth is exactly the `(z+1)`-adic valuation of the cyclic orbit-word polynomial.

## Forcing relation

For `F_r(z)=sum f_r(t)z^t`, the recurrence `x_r(t+1)=x_r(t) XOR f_r(t)` gives in the cyclic ring

\[
zF_r=(1+z)X_r.
\]

Since `N=2^m`, `z^N-1=(z+1)^N`, so this cyclic ring is the truncated local ring `F_2[z]/((z+1)^N)`. Therefore, away from the zero word,

\[
nu_{z+1}(F_r)=nu_{z+1}(X_r)+1.
\]

This packages the entire Pascal-mask hierarchy from runs 234–239 into one valuation.

## Width 8

The run-239 depth-six census is exactly

\[
(z+1)^6\mid X_8(z)
\]

for every initial state at `N=32`, with divisibility by `(z+1)^7` failing for some state. Since `(z+1)^6=1+z^2+z^4+z^6`, this is a compact structural condition.

## Next target

Stop manipulating individual Pascal masks unless needed for a check. Study how the Rule-30 OR forcing acts on this local-ring filtration. Over `F_2`, coefficientwise OR is `A+B+A odot B`, where `odot` is Hadamard/coefficientwise multiplication. Derive or experimentally classify `(z+1)`-adic valuations of the adjacent-coordinate forcing words. The benchmark is to explain `nu(X_8)>=6` uniformly at period 32.

Full note: `proofs/informal/problem1_run240_pascal_depth_is_root_multiplicity.md`.
