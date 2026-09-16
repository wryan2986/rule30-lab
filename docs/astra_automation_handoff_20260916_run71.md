# Astra automation handoff — 2026-09-16 run 71

## What changed

Continued directly from run 70 at branch tip `3002d3298a3a6465ad911ebc1ac29d8b6504eb9a`; there was no intervening work.

Added:

- `proofs/informal/problem1_zero_return_no_merger_theorem.md`

Research commit: `8f2e774132005a8ebbfc84fa3758760a65cef040`.

## New result

Proved a general **no-merger theorem** for the simple zero-column first-return graph modulo cyclic rotation.

If two zero-target necklaces allegedly had the same next-return child, align representatives of the common child by rotation and reverse both connectors. They become two forward orbit segments starting from exactly the same zero state. Forward Rule-30 column-pair evolution is deterministic, so both are prefixes of one forward orbit. If the lengths are equal, their endpoints are equal; if one is shorter, its zero endpoint lies strictly inside the longer connector, contradicting the definition of a first-return connector. Hence every zero-return vertex has simple indegree at most one.

This removes mergers as a possible all-scale complication. The p=16 no-merger observation from run 70 was not accidental.

For any finite acyclic reachable basin, the simple zero-return graph is therefore a rooted tree. Every genuine binary branch increases the leaf count by one, so `L=B+1`, where `B` counts vertices whose complementary integrations lead to two distinct child necklaces. Phase-collapsed integrations do not increase the leaf count.

## Evidence status

Exact theorem from deterministic forward evolution, shift equivariance, and first-return minimality. No finite computation is required.

## Best next target

The graph-theoretic obstruction left after excluding mergers is **cycles / nontermination**. Look for a monotone quantity or invariant on zero-return states that excludes cycles in the relevant dyadic basin. In parallel, classify when complementary integrations phase-collapse versus genuinely branch; once cycles are excluded, terminating-necklace counts reduce to genuine branch counts.
