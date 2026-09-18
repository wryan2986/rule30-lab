# Astra automation handoff — run 112 — 2026-09-18

## Starting state

No intervening repository work was present after run 111. Starting branch tip: `f57654de3a12f711eb4608ccf31783b134b49151`.

## New structural refinement

Added `proofs/informal/problem1_infinite_moving_fringe_has_pro2_recurrence.md`.

Run 111 proved that every fixed-width moving-right-fringe prefix evolves by a finite 2-group action, hence has power-of-two period. The new note upgrades this from separate finite-prefix periodicity to a synchronized statement about the entire infinite fringe.

If `F_J` is the update on coordinates `0,...,J` and `ord(F_J)=2^m_J`, compatibility under truncation implies the finite orders form a divisibility chain. Hence `F^(2^m_J)` fixes the first `J+1` coordinates for every fringe state. In the product topology, powers of two therefore return arbitrarily deep finite prefixes simultaneously; equivalently the infinite moving-fringe action is an inverse limit of finite 2-group actions, i.e. a pro-2 action.

Consequently every continuous finite-valued observable of the instantaneous infinite moving fringe factors through some finite prefix and must recur at a dyadic time. This closes a broader version of the proposed anchored-phase route: merely inspecting a larger finite moving-edge window and assigning a finite phase/resource state cannot create a non-reuse budget.

A successful FULL/non-reuse theorem must use information outside continuous finite-prefix fringe state: genuinely unbounded-depth information, source/history identity, or coupling to core/global-shadow/hidden-slack dynamics with a non-dyadic obstruction.

Problem 1 remains OPEN.

Research commit: `bed5a19d1dec077501c10b4d3da34b07adb89631`.
