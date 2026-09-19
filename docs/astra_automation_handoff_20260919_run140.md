# Astra automation handoff — 2026-09-19 run 140

## Starting state

Started from `research/astra-next` at `bd5b5c0ddfdde1d25e0f9cc1208508e4b5ac8c74`, immediately after run 139. No intervening research work was found.

Problem 1 remains open.

## New structural clarification

The growing diagonal in the left-front moving frame is exactly the original fixed spatial trace. With

\[
y_j(t)=x_{L-t+j}(t),
\]

for every fixed original coordinate `k`,

\[
\boxed{y_{t+k-L}(t)=x_k(t).}
\]

In particular `y_{t-L}(t)=x_0(t)`. Reindexing the triangular recurrence along these diagonals recovers the ordinary Rule-30 update for the fixed-coordinate columns.

Full note:

`proofs/informal/problem1_moving_frame_diagonal_is_exactly_fixed_spatial_trace.md`

Research commit: `c9ccffe9575c1da9a735472f1d06fea412773859`.

## Why it matters / stopping fence

Run 139 suggested searching for a uniform-in-depth transport law from the eventually periodic fixed front offsets down the diagonal `j~t`. The exact identity above shows that this diagonal is simply the original center/source trace in sheared coordinates. Therefore the coordinate change alone supplies no compression: extending fixed-offset periodicity to `j=t-L` would amount to proving a genuinely new finite-state compression theorem for the original growing Rule-30 dependency cone.

Combined with run 136 (arbitrary finite center words realizable from finite-support rows by left-permutivity), bounded-depth front periodicity cannot by itself constrain FULL center prefixes.

Do not spend another run enlarging fixed front windows or merely reindexing their eventual periodicity toward the center.

## Best next target

Return to the special FULL cyclic-source/gate/right-fringe constraints and look for an episode-specific collapse of the growing interior state: a conserved/monotone finite-range quantity across the whole interior, a source-relative relation that collapses the interior at distinguished `011` episodes, or a bounded-reuse charge to finite initial data. Any moving-cut law must contain genuinely new information beyond the shear-coordinate recurrence itself.

Problem 1 remains open.
