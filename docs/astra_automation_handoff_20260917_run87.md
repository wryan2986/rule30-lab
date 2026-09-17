# Astra automation handoff — run 87 — 2026-09-17

## Starting state

No intervening repository work was present after run 86. Starting branch tip: `c65e6211af20f3993826f6798077f24188ad4158`.

## New result

Added `proofs/informal/problem1_parent_map_period_dichotomy.md`.

For the cyclic derivative `D(x)=Sx xor x`, if `x` has exact rotational period `r` and `D(x) != 0`, then

`per(D(x))` is either `r` or `r/2`.

The strict drop occurs exactly when `x` has half-period complement symmetry:

`S^(r/2) x = complement(x)`.

Because run 82 proved that `rho_n^{-1}` preserves exact rotational period, the zero-return parent map

`P_n = D o rho_n^{-1}`

therefore never increases exact rotational period. Every strict period drop is a halving, and it occurs exactly when the boundary word `rho_n^{-1}(a)` is antiperiodic.

This gives a rigorous filtration of dyadic root-basin ancestry by exact period. A new full-period portal branch stays in the full-period sector until its first antiperiodic boundary integration, at which point it drops into the inherited half-period sector. Repetition naturality then identifies the remainder with lower-period ancestry.

## Important correction / dead end

The stronger claim that `D` always preserves exact rotational period is false. Antiperiodic words are exactly the exception. The failed stronger claim was not committed as a theorem; the research note records the correction explicitly.

## Problem 1 status

OPEN.

## Next target

For period 32, focus on the exact-period-32 ancestry sector. The relevant event is

`S^16 rho_32^{-1}(a) = complement(rho_32^{-1}(a))`,

which is exactly when the next `P_32` parent drops to period 16. Seek a structural bound or quotient controlling how long a full-period ancestry chain can avoid this condition. This is sharper than searching for a global invariant of `rho_32` or `P_32`.

Research commit containing the theorem note: `faeaf6de58f69fa19abdddcc44f61c1f2e4f83b3`.
