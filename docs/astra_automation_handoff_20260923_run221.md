# Astra automation handoff — 2026-09-23 run 221

Problem 1 remains open.

## Repository state entering this run

`research/astra-next` was at `bf7583af5ac73e1b7143b677596b1f46a92256c2` (run 220). No intervening work was present.

Run 220 isolated the stopping-curve look-ahead bit
\[
F_n=d_{n+1}(a_{n-1})
\]
as the precise obstruction to the fixed-period finite-state closure.

## New proved result

For the common-origin tower, all adjacent defects satisfy d_j(0)=0. Combining this with the exact cross-level recurrence gives the all-depth finite-speed lemma
\[
\boxed{d_j(k)=0\text{ for every }j>2k.}
\]

Therefore at stopping time a_{n-1}, the complete look-ahead tail is forced to zero above level 2a_{n-1}. The number of potentially nonzero look-ahead bits from level n+1 upward is at most
\[
\max(0,2a_{n-1}-n).
\]

Full proof: `proofs/informal/problem1_run221_transient_frontier_finite_speed_cone.md`.

## Interpretation / dead end closed

The run-220 frontier is not genuinely infinite at any fixed level: common-origin initialization restricts it to a finite causal triangle. However, the triangle width is not uniformly bounded as n grows, so finite propagation by itself does not revive the bounded-state epoch strategy. The missing transient state can still grow with n.

## Next target

Use the stopping conditions to constrain the *contents* of the finite causal triangle. Highest-value test: search for two realizable common-origin towers that share the same bounded constant-period cycle/entry state but have opposite frontier bit F_n. A collision proves bounded reconstruction impossible for that state choice. If collisions systematically fail, extract the invariant responsible and try to prove it.
