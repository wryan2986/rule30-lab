# Astra automation handoff — run 125

Problem 1 remains OPEN.

Starting branch tip: `a87e5727b784278e032011df8e6384eddec1733a` (`research/astra-next`). No intervening work was found after run124.

## New result

Run124's suggested search for a monotone "filtration on recoverable original-row information" has a simple all-depth obstruction in its literal form. Since Rule 30 is injective on finite-support rows, the unique time-zero reconstruction `R_t(T^t x)` equals the same initial row `x` at every time. Therefore for **any** function `Phi` on finite-support initial rows,

`Phi(R_t(T^t x)) = Phi(x)`

for all `t`. No continuity/locality/computability assumption is needed. Thus an observable depending only on the recovered initial row is exactly conserved and cannot advance at resets, nonresets, or births.

This does not kill the finite-support budget route. It sharpens the required form: the resource must pair the fixed original row with a changing episode/source-relative selector (moving cut, source coordinate, selected subset/index, etc.) and prove monotonicity or bounded reuse for that selector. Recoverability alone contributes no one-way dynamics.

Recorded in `proofs/informal/problem1_recovered_initial_row_observables_are_conserved.md`, commit `2e4554242f87d1b2c41c939496ac9d21e2798411`.

## Next target

Construct a canonical episode-dependent selector on the finite original support. The minimal useful transition theorem would say that every forced two-bit nonreset birth strictly advances a selected original-support index while resetting passages never decrease it. Because the original support index set is finite, that would yield the missing global birth budget. Do not spend another run searching for a monotone function of the reconstructed time-zero row alone; this lemma rules that out identically.
