# Astra automation handoff — 2026-09-24 run 236

Problem 1 remains OPEN.

## Entry state

Entered from run 235, commit `fa5deff2fcebbf745e1be2d83c43978113b7aa02`. No intervening repository work was present.

Run 235 established the iterated Pascal-mask descent from a three-level constant-order plateau and asked to push it to the exact bottom recurrence.

## New result

Added:

- `proofs/informal/problem1_run236_plateau_position_bound_from_terminal_pascal_mask.md`

For `N=2^m`, the last even Pascal mask is exactly

`A^(N-2) 1_N = (1,1,0,...,0)`.

For every interior forcing `f_r=x_{r-1} OR x_{r-2}` with `r>=3`, this mask cannot annihilate `f_r` identically: choose the state with only `x_{r-3}=1` among coordinates through `r-1`; then `f_r(0)=0` and `f_r(1)=1`.

Therefore a three-level plateau

`O_{s-1}=O_s=O_{s+1}=N`, with `N>=4`,

cannot satisfy `s>=2N-2`. The exact bound is

`boxed: s <= 2N-3`.

This follows by descending `N-3` times from the run-235 starting identity `S_{A 1_N}[f_{s-1}]=0`, reaching exponent `N-2` at coordinate `r=s-2N+5`; if `s>=2N-2`, then `r>=3`, contradicting the explicit witness above.

The exact bottom `f_2` is different: under `x_0'=x_0`, `x_1'=x_1 XOR x_0`, the sequence `f_2=x_1 OR x_0` is constant for every initial state. Hence every even mask annihilates `f_2`; bottom descent itself is automatic.

## Why this matters

This is the first quantitative position/order restriction extracted from the Pascal descent, rather than another equivalent cancellation identity. It is not yet strong enough to solve Problem 1 because `N=O_s` may be exponentially larger than `s`.

## Next target

Classify earlier Pascal masks. For each `k`, determine the smallest forcing coordinate `r` for which `S_{A^k1_N}[f_r]` can vanish identically. A computational census for modest powers of two should be done first. If non-annihilation persists at much lower `k` than `N-2`, the resulting plateau bound could improve substantially beyond `s<=2N-3`.
