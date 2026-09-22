# Astra automation handoff — 2026-09-22 run 207

Problem 1 remains OPEN.

Continue only the corrected run-193--207 chain.

## New exact result

Run 206's first-defect identity extends to all depths. For q fixed, let

    r_k=A^k(q), s_k=A^k(2q).

Then exactly

    s_k = 2 r_k XOR d_k

for one bit d_k, with d_0=0 and driver recurrence

    low(r_k)=00: d'=d
    low(r_k)=01: d'=1 XOR d
    low(r_k)=10: d'=1
    low(r_k)=11: d'=0.

So the discrepancy between adjacent shift-tower A-orbits never spreads beyond bit zero. The entire post-defect problem is a one-bit automaton driven by the lower orbit's low-two-bit trace.

Proof notes:

    proofs/informal/problem1_run207_exact_adjacent_tower_defect_automaton.md
    proofs/informal/problem1_run207_cycle_reset_criterion.md

## Eventual-cycle consequence

Let a=tau(q). From time a the driver is periodic.

- If its eventual cycle never has low bit r_0=1, all defect maps are identity/toggle, so d is periodic immediately from a and tau(2q)<=a. Therefore a strict adjacent-tower increment is impossible.
- If the eventual cycle has r_0=1, symbols 10/11 are resets (constant maps). There is a unique periodic defect phase. A strict increment beyond a can occur only if d_a mismatches that phase; the mismatch survives through preceding 00/01 symbols and is erased exactly by the first reset, at most one lower-orbit period later.

Thus positive increments a_n>a_(n-1) are now tied to a concrete cycle-entry phase mismatch, not merely to a first epsilon defect.

## Next target

For q=2^(n-1)x, relate d_{tau(q)} to the repository's complete cycle code/phase. The global goal remains the true renewal condition

    a_n > max(a_(n-1), b+n).

Need to show (or refute) that the reset-phase mismatch producing such above-diagonal increments can occur only finitely often for fixed finite x. Do not return to absolute diagonal bounds, width arguments, or mechanical local front propagation.
