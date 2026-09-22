# Astra automation handoff — 2026-09-22 run 210

Problem 1 remains OPEN.

Continue only the corrected run-193--210 chain.

## New exact connection

For `q_n=2^n x`, `a_n=tau(q_n)`, `delta_n=a_n-a_(n-1)`, runs 207--209 imply:

- matched lifted defect phase: `delta_n=0`;
- mismatched phase: `delta_n=rho_n`, where `rho_n` is the distance through the first reset transition on the eventual cycle of `q_(n-1)`.

A reset occurs exactly when the current lower-cycle state has least-significant bit 1. Hence, in the mismatch case, `rho_n-1` is exactly the initial low-bit zero-run length from cycle entry.

Therefore the residence-ledger charge has the exact pointwise form

    delta_n-1 = -1                  matched lift,
    delta_n-1 = rho_n-1             mismatched lift.

So positive residence surplus is exactly a cycle-entry low-bit zero-run; skips contribute exactly `-1`.

Proof note:

    proofs/informal/problem1_run210_reset_gap_residence_ledger.md

## Remaining obstruction

This does not establish bounded reuse. Do not count reset gaps as independent births or disjoint original-support resources. The remaining question is whether, for one fixed finite origin `x`, mismatch zero-runs can provide unbounded cumulative surplus over matched lifts.

Useful next targets are: a common-origin restriction on reuse of long low-bit zero-runs across `2^n x`; a bound linking mismatch frequency to matched lifts; or a genuinely non-telescoping ancestry charge attached to reset gaps.
