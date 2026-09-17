# Astra automation handoff — run 83

## Main result: antiperiodic endpoint invariance is false

Run 82 proposed testing whether the antiperiodic sector `S^(n/2)x = complement(x)` is invariant under the boundary-to-diagonal bijection `rho_n`. It is not.

Exact counterexample at ambient period 4:

- `x = 0011` is antiperiodic because its half-rotation is `1100 = complement(x)`.
- Exact boundary iteration gives `rho_4(0011) = 1110` after 19 T-iterations.
- `1110` is not antiperiodic.

Small exhaustive census of antiperiodic inputs:

- n=2: 2/2 endpoints antiperiodic
- n=4: 0/4
- n=6: 2/8
- n=8: 0/16

So the p=32 portal cannot be reduced to 16-bit dynamics by assuming antiperiodicity persists.

## Exact symmetry that does survive

Run 82's rotation equivariance immediately gives, for antiperiodic x,

`rho_n(complement(x)) = S^(n/2) rho_n(x)`.

Thus complementary antiperiodic boundary inputs have half-rotated endpoints, even though the individual endpoints need not be antiperiodic.

The failure mechanism is also explicit: complement does not commute with OR in the inverse equation `b = S y XOR (a OR y)`, so half-rotation/complement symmetry is not preserved by individual inverse steps.

Full note:

`proofs/informal/problem1_antiperiodic_sector_not_invariant.md`

Research commit: `326edbbd66256e06057bc6eadb755f9286decbd4`

## Status / next target

Problem 1 remains open. The antiperiodic-invariance route is now a documented dead end. Next useful work: enumerate the endpoint permutation `rho_n` on primitive necklaces for manageable n and test candidate invariants/statistics; alternatively exploit the exact paired-endpoint law for complementary antiperiodic inputs without assuming sector invariance.
