# Astra automation handoff — run 88 — 2026-09-17

## Starting state

No intervening repository work was present after run 87. Starting branch tip: `192c26a7abc9f5cf7b19f7f64795e73e31cc06cd`.

## New result

Added `proofs/informal/problem1_period_halving_edges_are_odd_block_repetitions.md`.

Run 87 characterized a period-halving parent edge by antiperiodicity of the boundary integration. Run 88 gives the exact target-side equivalent:

If `x` has exact period `2r`, then

`S^r x = complement(x)`

iff

`D(x) = ww`

where `w` has exact period `r` and odd XOR parity.

The key identity is the half-block telescoping parity

`xor_i w_i = x_r xor x_0 = 1`.

Conversely, integrating a repeated odd block `ww` forces `x_r xor x_0 = 1`, hence both complementary integrations are antiperiodic and (for exact-period `w`) have exact period `2r`.

Therefore a full-period `2r` zero-return parent edge drops to period `r` exactly when its parent target is `ww` for an odd exact-period-`r` block `w`.

This algebraically explains the doubled-odd-leaf portal mechanism: an odd target has no cyclic integration at period `r`; after repetition to `ww` at period `2r`, it has exactly two complementary integrations, and both are new antiperiodic exact-period-`2r` words.

## Problem 1 status

OPEN.

## Next target

At period 32, the attachment set from the new full-period sector is now exactly repeated odd period-16 targets `ww`; within the root basin these are repeated odd leaves. Seek a bound/quotient/monotone controlling the number of full-period-32 `P_32` steps before reaching this target-side set. This is preferable to repeatedly evaluating the >100M-step connector or testing antiperiodicity through `rho_32^{-1}`.

Research commit: `09e67f49982e0e24ef896ec81cf449ba56f0d041`.
