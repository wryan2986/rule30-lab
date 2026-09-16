# Astra automation handoff — run 77

## New result

Recast zero-column first return as a diagonal-hit problem for the deterministic inverse pair map.

For the unique predecessor equation

`b = S y xor (a or y)`, `(a,b) -> (y,a)`,

substitution shows exactly

`y=0 iff b=a`

when `a != 0` (the reverse implication uses the existing uniqueness theorem). Hence a deterministic connector reaches its next zero column exactly when its current pair first hits `(a,a)`. At that hit the next state is forced to `(0,a)`, and only the following singular integration creates unary phase collapse or genuine branching.

Also, for `a != 0`, `b=0 iff y=1^p`.

Full note: `proofs/informal/problem1_zero_return_diagonal_hit_criterion.md`.

## Why useful

The p=32 >10^7-step connector is now a first-return-to-the-diagonal problem for a deterministic map on ordered word pairs. This cleanly separates long connector dynamics from the already-classified singular branching step and gives a simpler exact stopping predicate (`a == b`) before predecessor evaluation.

## Remaining blocker

This is a structural reduction, not yet a jump algorithm. The next target is a quotient/statistic that predicts first diagonal return, or a multi-step transducer for `T^k` that certifies no intermediate diagonal hit.

Problem 1 remains open.
