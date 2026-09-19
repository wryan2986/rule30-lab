# Astra automation handoff — run 143 — 2026-09-19

## Starting point

Started from run 142. Its key exact transport law from a distinguished source `q` was

`r[1](q+4)=a`, `r[2](q+4)=a OR b`,

where `a=r[3](q)`, `b=r[4](q)`.

## New result

The transported pair does **not** close the complete resetting-source state. With the fixed distinguished motif `10101110`, choose `a=b=c=0` for source positions 3,4,5 and vary only `d=r[6](q)`.

Exact four-step Rule-30 evolution gives:

- `d=0`: positions 0..4 at `q+4` are `10011`;
- `d=1`: positions 0..4 at `q+4` are `10000`.

So both have the same transported pair `00` at positions 1,2, while position 3 differs. Farther fringe information re-enters immediately beyond the run-142 pair.

Full note: `proofs/informal/problem1_transported_right_pair_does_not_close_full_resetting_source_state.md`.

## Interpretation

Do not spend the next run trying to iterate `(r1,r2)` as though it determines the whole resetting-source neighborhood. It does not.

However, this is only a stopping fence for **full-state closure**. It remains possible that the next return/birth indicator (the actual observable needed by the gate argument) depends only on the transported pair and ignores the differing farther state.

## Next target

Compute the exact dependency of the next return/birth indicator under the resetting-source phase/gate laws for the three reachable pair classes `00`, `01`, `11`.

The decisive question is:

> Can two admissible resetting-source configurations with the same transported pair but different farther fringe produce different next return/birth outcomes?

If no, we have a genuine quotient finite-state system. If yes, identify the first farther bit required; that gives the minimal obstruction/state enlargement rather than an open-ended fringe expansion.

Problem 1 remains OPEN.
