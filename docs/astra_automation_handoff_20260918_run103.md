# Astra automation handoff — run 103 — 2026-09-18

## Starting state

No intervening repository work was present after run 102. Starting branch tip: `22867ee86d05cc7a7da11419532623b50c84a6a5`.

## New exact refinement

Added `proofs/informal/problem1_extremal_return_blocks_are_one_sided_excursions.md`.

In bounded-slack case B, let

    m = liminf q_n,
    M = limsup q_n.

Since q is eventually integer-valued in a finite interval, m and M both occur infinitely often and eventually m <= q_n <= M. Successive returns to m give exact nonnegative charge excursions:

    sum_[a,j)(delta-1) = q_j-m >= 0

for every internal prefix, with total charge zero at the next return. A nontrivial minimum excursion begins with delta>=2 and necessarily ends with delta=0; the last pre-return level is exactly m+1 because q can decrease by at most one per step.

Dually, successive returns to M give nonpositive charge excursions. A nontrivial maximum excursion begins with delta=0 and ends with delta>=2.

This strengthens run 102's arbitrary recurrent-level zero-charge blocks: extremal blocks constrain the sign of every prefix charge, not merely the total. A future FULL/fringe contradiction can therefore target ordering rather than uncompensated total charge. It suffices to force a skip-before-surplus ordering that makes a minimum-excursion prefix negative, or the dual surplus-before-skip ordering that makes a maximum-excursion prefix positive.

The result remains abstract bounded-discrepancy combinatorics; constant and periodic bounded schedules remain countermodels without Rule-30/FULL coupling. Problem 1 remains OPEN.

Research commit: `487df969f2516a7db9638dc99fd9bc88b53ff270`.
