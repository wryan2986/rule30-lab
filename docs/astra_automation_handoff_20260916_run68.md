# Astra automation handoff — 2026-09-16 run 68

## What changed

Continued directly from run 67's proposed p=16 zero-column audit. Added:

- `proofs/informal/problem1_p16_zero_column_branching_counterexample.md`

Research commit: `3d8796ef953c485b345663282263f3baa912f3ec`.

## New result

The hoped-for all-scale zero-target phase-collapse invariant fails at p=16.

Exact reverse/forward propagation finds a terminating full-period odd-parity representative

`c16_a = 0000010101000101`

with termination width `87867`. Its full trajectory has nonterminal zero targets at columns 29580, 34659, 87467, 87838, 87859, and 87864. The first two targets are full-period 16 and even parity:

- `1000101110111101` (weight 10),
- `0011000011000101` (weight 6).

Hence their two derivative integrations are not phase-equivalent. This is genuine reverse necklace branching.

More strongly, the alternate branch at the first target can be propagated backward to another legal odd-parity full-period initial word

`c16_b = 1001110010100010`.

It is not a rotation of `c16_a`. Direct forward propagation independently verifies that `c16_b` terminates at width `229338`.

Therefore the working conjecture of a unique terminating necklace at every dyadic period is false at p=16: there are at least two rotation-inequivalent terminating period-16 necklaces.

## Evidence status

Exact finite computation using the established recurrence and exact predecessor classification. No probabilistic search is involved. The two candidate initial words were independently forward-propagated to consecutive zero pairs.

## Best next target

Do not continue trying to prove global reverse-necklace uniqueness. Replace that target with classification of the induced zero-column first-return graph. Enumerate all p=16 odd-parity legal zero-boundary ancestors of the terminal pair modulo rotation, identify which genuine branches die versus reach legal initial states, and compare that finite graph with the p=8 graph. The inherited scale-transition/antiperiodicity lemmas remain valid; what fails is the claim that all additional zero returns phase-collapse.