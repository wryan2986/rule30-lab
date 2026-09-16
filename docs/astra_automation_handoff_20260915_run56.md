# Astra automation handoff — run 56

Problem 1 remains open.

## Repository state

Run began at `0d020cf00323ebbc68c713539585eac90b98d033`; no intervening work was present after run 55.

## New result

Tested the run-55 proposal that the pair derivative might admit a corrected variable `e=d xor Phi(r,...)` obeying the ordinary lower-period reconstruction on the special terminating basin.

On the complete known length-8 terminating trajectory (`c=10000110`, 400 spatial transitions before the terminal zero pair), exhaustively tested every translation-equivariant static Boolean correction depending on 1, 2, or 3 consecutive bits of the current even-sample word `r`: 4 + 16 + 256 functions. None makes `e` obey the ordinary length-4 reconstruction throughout the trajectory. The bare derivative itself fails that recurrence at 376/400 testable transitions.

Therefore `Delta_2(c_8) ~ c_4` is an initial-word relation, not a trajectory semiconjugacy visible through a short-range static gauge correction. This rules out a broad natural proof strategy but does not disprove the period-halving or unique-necklace conjectures.

## Research file

`proofs/informal/problem1_pair_derivative_local_correction_no_go.md`

Research commit: `d2725e2b4945c3c78d5d26d7e0d3b9716d394dae`

## Next target

Do not keep enlarging static local `Phi(r_i,...)` blindly. Attack the weaker zero-basin implication directly. Reverse the exact recurrence from terminal `(0,0)` in halved `(r,d)` coordinates and derive predecessor constraints on the initial derivative `d_1=Delta_2(c)`, or implement a memoized reverse-basin classifier to make the length-16 test practical.
