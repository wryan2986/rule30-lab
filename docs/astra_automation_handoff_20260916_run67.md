# Astra automation handoff — 2026-09-16 run 67

## What changed

Continued directly from run 66's proposed zero-column audit. Added:

- `proofs/informal/problem1_p8_zero_column_return_audit.md`

Research commit: `51eecc2253bc45536151c90a85d61fbfd3e8d65e`.

## New result

For the known terminating period-8 reconstruction (`N_8=400`), direct exact propagation shows that the only nonterminal zero columns occur at indices 371, 392, and 397. Their following singular targets are respectively

- `01110111 = (0111)^2`,
- `01010101 = (01)^4`,
- `11111111 = (1)^8`.

Each target has a rotational period whose primitive repeating block has odd XOR parity. By run 66's criterion, the two derivative integrations at each zero-column event are therefore phase-equivalent.

Combined with the exact uniqueness theorem away from zero middle columns, this proves that the entire known p=8 terminating reverse trajectory has **no genuine necklace branching anywhere**, not merely at the scale-transition singularity.

## Evidence status

Exact finite computation plus previously proved symbolic lemmas. This is not yet an all-p theorem.

## Best next target

Prove a structural statement about zero-column targets on terminating dyadic trajectories: every nonterminal target should have an odd-parity primitive rotational block, or at least satisfy the run-66 phase-equivalence criterion. If p=16 terminating data are already available/tractable, audit its zero-column targets next to test this formulation before attempting the induction.