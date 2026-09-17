# Problem 1: portal return existence from the boundary state

## Result

The return-existence gap identified in run 78 is closed for every singular-integration connector that starts from a zero target.

Let

`T(a,b) = (y,a)`

for `a != 0`, where `y` is the unique solution of

`b = S y xor (a or y)`.

Run 77 proved that `y=0` iff `a=b`, so avoiding a zero return is equivalent to staying forever off the diagonal. Run 78 proved that `T` is injective on its off-zero domain.

Now consider any connector immediately after a singular integration from a zero target. Its first deterministic pair has the form

`(x,0)`

with `x != 0` (the nontrivial integration branch). The crucial observation is that no state in the off-zero domain can map to `(x,0)`: every image of `T` has second component equal to the input first component `a`, and by definition that input satisfies `a != 0`. Hence every off-zero image has nonzero second component.

Therefore `(x,0)` has **no predecessor inside the off-zero deterministic domain**.

Assume for contradiction that the connector never returns to zero / never hits the diagonal. Then all forward iterates of `(x,0)` under `T` remain in the finite set of nonzero, off-diagonal word pairs. Some state must repeat. Because `T` is injective throughout this all-off-zero orbit, a repeated state cannot be entered after a transient: cancelling equal predecessors backwards shows that the initial state `(x,0)` itself lies on the resulting periodic orbit. But a periodic orbit gives `(x,0)` an off-zero predecessor, contradicting the boundary observation above.

Thus every nontrivial singular-integration connector must eventually hit the diagonal, and therefore must produce another zero return.

\[
\boxed{\text{Every connector starting at }(x,0),\ x\ne0,\text{ reaches a zero return in finite time.}}
\]

This argument is independent of dyadic period and does not require antiperiodicity. Ambient off-diagonal cycles from run 79 remain real, but they are dynamically inaccessible from the boundary states produced immediately after zero-column integration.

## Consequences for the dyadic portal program

The caveat introduced in run 78 can now be removed for the zero-return graph generated from actual zero targets:

1. every singular integration branch has a finite next zero return;
2. the no-merger theorem applies to those returns;
3. the zero-return component reachable from the terminal root is finite and acyclic at fixed period;
4. the run-74 inherited-subgraph / doubled-leaf portal decomposition is unconditional again;
5. each doubled-leaf portal has a finite full-period tree attached to it.

In particular, the first p=32 portal that survived more than 100,000,000 exact inverse steps in run 78 is now known theoretically to return eventually. Its enormous connector length is a computational-cost issue, not evidence for nonreturn.

## Sharpened dynamical picture

The off-zero pair dynamics has two qualitatively different regions:

- genuine periodic orbits, including the alternating 2-cycle family from run 79; and
- boundary-launched connector orbits beginning at `(x,0)`.

The latter cannot join a periodic orbit because injectivity forbids transient merging and the boundary state has no off-zero predecessor. Therefore every boundary-launched orbit must exit the off-zero domain through the diagonal in finite time.

This is stronger and simpler than seeking a portal-specific invariant based on half-period antiperiodicity.

## Next target

Return existence is no longer the blocker. Resume the p -> 2p counting program. The main remaining practical obstacle at p=32 is computing the very long guaranteed-finite first-return connectors efficiently. A useful next step is either an exact multi-step accelerator or a structural bound/formula for the first diagonal-return time from `(x,0)`.
