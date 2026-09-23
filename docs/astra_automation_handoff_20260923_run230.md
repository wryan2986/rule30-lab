# Astra automation handoff — run 230

Problem 1 remains open.

## Repository state

Run 230 entered at run 229 commit `e177b722186245d85a16b102ec9fca4c2d10a161`; there was no intervening work.

## New all-depth reduction

Run 229 recommended abandoning explicit repeated-square expansion and using the order filtration. This run makes that route exact.

For any prefix width `s`, let `L=O_s=2^{m_s}`. Then `T_R^L` fixes coordinates `0,...,s` pointwise, while the next coordinate obeys

\[
(T_R^Lx)_{s+1}=x_{s+1}\oplus G_s(x_0,\ldots,x_s),
\]

where

\[
G_s=\bigoplus_{t=0}^{L-1}(x_s(t)\lor x_{s-1}(t)).
\]

Hence `O_{s+1}=O_s` iff `G_s` is identically zero; otherwise `O_{s+1}=2O_s`.

If `m_s=...=m_t=q` is a constant-order plateau, then one iterate `T^(2^q)` fixes the entire prefix through coordinate `t`; the first coordinate beyond the plateau is again just a one-bit skew extension driven by the accumulated forcing `G_t`.

## Interpretation

This validates the filtration route without expanding `T^(2^q)` symbolically: an entire frozen plateau can be collapsed. But it does not yet bound plateau lengths or `m_R`; the obstruction is now exactly the complexity of the accumulated forcing observables `G_t` on growing frozen prefixes.

Detailed proof: `proofs/informal/problem1_run230_order_filtration_skew_normal_form.md`.

## Next target

Analyze coordinate derivatives/projections of `G_t` across constant-order plateaus. Seek a cancellation or recursion showing that plateau structure forces derivative vanishing or otherwise restricts the next doubling event. Do not return to brute symbolic expansion of repeated squares unless it tests a specific conjectured identity.
