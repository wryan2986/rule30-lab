# Astra automation handoff — run 90 — 2026-09-17

## Starting state

No intervening repository work was present after run 89. Starting branch tip: `069829618c31f0536f242b3430ab069f53e3a218`.

## New result

Added `proofs/informal/problem1_full_period_vertices_branch_unless_terminal.md`.

Run 89 asked whether a new full-period portal subtree might remain a path. This is false in general. If an exact-period-`n` zero target `w` has even parity, its integrations are `x` and `complement(x)`. If those integrations were the same necklace, `S^k x = complement(x)` for some `k`. Applying the cyclic derivative gives `S^k w=w`, contradicting exact period `n` (except `k=0`, which would require `x=complement(x)`). Hence the integrations are distinct necklaces. Rotation equivariance plus injectivity of `rho_n` makes their zero-return endpoints distinct necklaces too.

Therefore every even-parity full-period vertex has exactly two child necklaces; every odd-parity vertex is terminal. Run 89's single portal edge is the exceptional birth edge from the proper-period doubled odd parent. After portal birth, the genuinely new full-period component is a full binary tree (unique parent, two children at every nonterminal vertex), not a path.

## Problem 1 status

OPEN.

## Next target

Exploit the now-rigid binary-tree structure. The remaining question is whether every full-period branch reaches odd parity in finite depth / whether every newly attached dyadic portal tree is finite. Search for a well-founded statistic or counting argument on full-period parent-map ancestry; do not pursue the path hypothesis further.

Research commit: `6855e883177f771753c48d3b6156fd69a6f88758`.
