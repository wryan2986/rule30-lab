# Astra automation handoff — 2026-09-24 run 246

Problem 1 remains open.

## What changed

Run 246 followed the corrected target from run 245 and found the first genuinely unconfounded `P/D/P/D` order pattern.

Exhaustive permutation enumeration through width 20 gives

`O_0..O_19 = 1,2,2,4,8,8,16,32,32,64,64,64,128,256,256,512,512,1024,1024,2048`.

Hence coordinates 13..17 realize

`256 -> 256 -> 512 -> 512 -> 1024`,

a true `P/D/P/D` decision pattern. The local `D/P/D` block is not preceded by another doubling, so run 243 does not explain it. A second instance occurs at coordinates 15..19:

`512 -> 512 -> 1024 -> 1024 -> 2048`.

Random-state tests conditioned on the full relevant prefix-period history found:

- first case: 922 retained states, all with plateau-coordinate complexity `L(X_16)=451`; 457 subsequently doubled and 465 did not;
- second case: 462 retained states, all with `L(X_18)=964`; 221 subsequently doubled and 241 did not.

Thus the following doubling does not empirically select the complexity class: both decision outcomes occur at the same observed plateau complexity.

The values satisfy the run-242 recurrence exactly:

`451 = 256 + 194 + 1`,
`964 = 512 + 451 + 1`.

## New target

Explain the apparent forced value `L(X_14)=194` from the actual order history ending at `O_14=256`. If this can be proved for full-period witnesses, run 242 should propagate the later exact values 451 and 964 automatically.

Do not return to the run-244 “final doubling selects high complexity” interpretation unless new evidence requires it; run 246 shows both final-decision outcomes coexist in the same complexity class in the first genuine unconfounded examples.

See `proofs/informal/problem1_run246_first_genuine_plateau_double_plateau_double.md`.
