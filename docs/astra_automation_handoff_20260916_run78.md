# Astra automation handoff — run 78

## New result / correction

Found an important logical gap in the all-depth zero-return-tree argument.  No-merger and acyclicity prove that the graph of **existing** zero returns is a tree, but do not prove every singular integration has a subsequent zero return.  A deterministic connector may instead cycle forever among nonzero off-diagonal pair states.

Recorded full details in:

`proofs/informal/problem1_zero_return_existence_gap_and_offzero_cycles.md`

## Exact structural observation

For `a != 0`, the inverse pair map `T(a,b)=(y,a)` is injective because its output gives `a`, and then `b = S y xor (a or y)` is recovered exactly.  Therefore failure to hit the diagonal `a=b` is precisely an off-diagonal periodic-orbit obstruction in the finite pair state space.

This corrects the unconditional wording of runs 72 and 74.  Their no-merger/acyclicity/tree conclusions remain valid conditional on return edges existing.

## Computation

Independent packed-32-bit traversal of the first p=32 doubled-leaf portal (`l=0000010101000101`) found no diagonal hit within 100,000,000 exact predecessor iterations, strengthening run 75's 10,000,000 lower bound by 10x.

## Next target

Return existence is now the principal gap.  Prove portal states cannot lie on off-diagonal cycles, find an invariant separating them from such cycles, or accelerate/cycle-detect the first p=32 portal enough to decide it exactly.
