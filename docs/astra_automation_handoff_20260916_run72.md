# Astra automation handoff — 2026-09-16 run 72

## What changed

Continued directly from run 71 at branch tip `82a7317be91116c5674f4dd1dbf603d1b0405b94`; there was no intervening work.

Added:

- `proofs/informal/problem1_zero_return_acyclicity_theorem.md`

Research commit: `41d27eec8ffb5f1230ee27093d8a20bd9b49730b`.

## New result

Proved that the simple zero-column first-return graph reachable from the terminal root `[(0,0)]` is acyclic at every period.

The argument uses run 71's no-merger theorem rather than a new monotone quantity. First, the root cannot have a nontrivial incoming edge: reversing such a connector would give a positive-length forward orbit from `(0,0)` to a distinct zero state, impossible because `(0,0)` is a fixed point. If a directed cycle not containing the root were reachable from the root, the first cycle vertex on a shortest root-to-cycle path would have one incoming edge from outside the cycle and one from its cycle predecessor, contradicting indegree <= 1.

At fixed period the zero-state necklace space is finite. Therefore no infinite reverse zero-return path can exist either: an infinite path would repeat a vertex and hence contain a cycle. Combining this with run 71 gives a general theorem that the terminal reverse zero-return basin at every fixed period is a finite rooted tree modulo rotation.

This removes cycles/nontermination as a research target. No monotone quantity is needed for that purpose.

## Best next target

The remaining problem is local/combinatorial rather than graph-topological: characterize reachable even zero targets whose complementary derivative integrations phase-collapse versus genuinely branch, and characterize legal odd/full-period leaves. Seek a recurrence under `p -> 2p` for genuine branch counts / leaf counts, using the inherited lower-period spine plus new full-period zero targets seen at p=16.
