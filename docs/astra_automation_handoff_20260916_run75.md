# Astra automation handoff — 2026-09-16 run 75

## What changed

Continued from run 74 at branch tip `95cedf350564f3ab289de37d6bd3238933cba7df`; there was no intervening work.

Added:

- `proofs/informal/problem1_dyadic_leaf_count_monotonicity_and_p32_cost.md`

Research commit: `cfa311fe131ef4e35ac1f5e96688f04f448d8109`.

## New structural consequence

From run 74's exact portal decomposition,

`L_{2p} = L_p + sum_l B(l)`

with every portal-tree internal count `B(l) >= 0`. Therefore

`L_{2p} >= L_p`.

Equality holds exactly when every doubled old-leaf portal reaches an odd full-period leaf without encountering a full-period even zero target. Strict growth occurs exactly when at least one portal contains a full-period even zero target.

This reduces the strict-growth question to a local portal property.

## p=32 computational probe

Started the proposed portal-by-portal p=32 computation with the first canonical period-16 leaf

`0000010101000101`.

For its doubled zero target `ll`, an exact packed 32-bit reverse implementation was capped at 10,000,000 unique-predecessor steps and still had not reached the next zero column. A prior Python version also exceeded 5,000,000 steps. Thus the first tested p=32 portal-to-zero connector is rigorously longer than 10 million columns under the established recurrence convention.

This shows that portal decomposition controls branching but not connector length. Building `G_32` one inverse column at a time is computationally unattractive.

## Best next target

Develop an exact accelerated zero-to-zero first-return operator. The most promising structure to exploit is the antiperiodicity of the doubled-leaf integration (`S^16 x = complement(x)`) and/or composable transfer maps for long stretches with nonzero middle column. Any jump method must retain exact detection of intermediate zero columns.
