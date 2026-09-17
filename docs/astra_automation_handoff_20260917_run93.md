# Astra automation handoff — run 93 — 2026-09-17

## Starting state

No intervening repository work was present after run 92. Starting branch tip: `87644394632e97aca58655f76d897392feed1248`.

## New result

Added `proofs/informal/problem1_portal_tree_kraft_conservation.md`.

For any genuinely new fixed-period portal component, let the terminal odd leaves have depths `d_i` from the portal child. Since the component is a finite full binary tree, splitting unit mass equally at every continuing even vertex gives the exact Kraft identity

`sum_i 2^(-d_i) = 1`.

Equivalently, if `L_d` counts terminal leaves at depth `d`, then `sum_d L_d/2^d=1`.

Consequences include: at most `2^D` leaves can occur by depth `D`; if there are `O` leaves, some leaf has depth at most `floor(log2 O)`; and the terminal leaves form a complete binary prefix code in the portal branch choices.

## Relevance to the actual bottleneck

This does not bound the number of leaves and therefore is not the missing finite-support birth budget. Its possible value is that the required charging argument need not be a literal one-leaf/one-resource injection. If an original-support/fringe event fixes `k` branch choices, it controls a dyadic cylinder of mass `2^-k`; disjoint terminal cylinders then admit weighted accounting. This is a more flexible target than run 92's direct injection proposal.

`ASTRA_HANDOFF.md` remains authoritative: FULL must contradict finite entry for one actual survivor with its complete original finite right fringe.

## Problem 1 status

OPEN.

## Next target

Seek a theorem connecting an original-support event (initial support position, complete-fringe phase, or bounded-use entry resource) to a fixed prefix of portal branch choices. A useful result must control either total terminal cylinder mass per resource or branch depth from original finite data. Do not treat Kraft conservation itself as a cardinality bound.

Research commit: `b8a95d58999cdc31ff614ec118fc5e77fbdab8e5`.
