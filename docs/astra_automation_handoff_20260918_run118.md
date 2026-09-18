# Automation handoff: run118, 2026-09-18

Problem 1 remains OPEN. Continue on `research/astra-next`.

## Repository state

No intervening work was found after run117 at startup; starting branch tip was `303629f54b68f8ab0376b0e52dd81996e141c745`.

Run117 established the exact moving-left-edge recurrence and exhaustively observed, through width 19, a single eventual cycle up to phase with dyadic cycle lengths. Its suggested next target was an unbounded-depth/source-indexed characteristic charge.

## New proved unit

Added `proofs/informal/problem1_left_edge_prefix_cycles_are_dyadic.md`.

For the autonomous prefix recurrence

    b_j' = b_(j-2) XOR (b_(j-1) OR b_j),

all eventual cycles at every finite width have power-of-two period.

Proof: extend an `n`-bit base cycle of period `P=2^m` by one bit `z`. Along one base traversal, each update of `z` is one of the four unary Boolean maps `id`, `flip`, `const0`, `const1`. Their composition is again one of these maps. Therefore the return map after `P` steps makes every recurrent lift have period `P` or `2P`. Induct from the width-1 physical state `b_0=1`.

This promotes the dyadic-period portion of run117's computation to an all-width theorem. It does NOT prove the stronger observed single-attractor-up-to-phase claim or the empirical period thresholds.

## Consequence / stopping fence

No larger fixed moving-left-edge prefix can supply an odd-period dynamical obstruction. Like the right fringe, bounded left-edge state eventually exhibits only dyadic recurrence, although unlike the right fringe it may have a transient because the map is dissipative.

Thus the finite-support birth budget still has to use growing depth, history/source identity, or complete core/global-shadow coupling. The source-indexed characteristic idea should not be reduced to another bounded left-edge automaton.

## Next target

Continue the unbounded-depth characteristic route: identify a mathematically canonical backward characteristic or dependency certificate for the forced `beta=1` birth in `problem1_nonreset_return_birth_spacing.md`, and test whether successive forced births can be assigned strictly ordered time-zero intercept/crossing data with bounded reuse. Avoid new fixed-prefix phase censuses unless they import information not covered by the right/left dyadic stopping fences.
