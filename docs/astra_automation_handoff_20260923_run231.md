# Astra automation handoff — run 231

Problem 1 remains open.

## Repository state

Run 231 entered at run 230 commit `0962d91dbcbd40c1d23620cd43e869bd2c9b2fab`; there was no intervening work.

## New all-depth plateau constraint

Runs 226 and 230 can be combined into a useful necessary condition for consecutive non-doublings.

Let `O_s` be the width-`s` edge-automaton order, `G_s` the accumulated forcing controlling the extension from width `s` to `s+1`, and

\[
p_r=\bigoplus_{t=0}^{O_r-1}x_r(t).
\]

For `q_s=O_s/O_{s-1}\in{1,2}`,

\[
D_{e_s}G_s=(q_s\bmod2)p_{s-1}.
\]

Therefore, if

\[
O_{s-1}=O_s=O_{s+1},
\]

then the second equality gives `G_s identically 0`, while the first makes its newest-coordinate derivative equal to `p_{s-1}`. Hence

\[
\boxed{p_{s-1}\equiv0.}
\]

Using run 228, this is equivalently an all-state even-time cancellation of the lower forcing cocycle. Thus consecutive non-doublings are not independent: the second forces a descended parity identity one level lower.

Detailed proof: `proofs/informal/problem1_run231_consecutive_plateau_parity_constraint.md`.

## Next target

Try to iterate this descent across a longer constant-order plateau. Specifically, determine whether `G_{r}\equiv0` together with `p_r\equiv0` forces a derivative/parity identity at width `r-1`, and whether a plateau of length `L` yields a tower of `L-2` descended cancellations. This is preferable to symbolic expansion of `T^(2^q)`.
