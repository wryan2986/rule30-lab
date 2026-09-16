# Astra automation handoff — 2026-09-16 run 73

## What changed

Continued directly from run 72 at branch tip `b7032ca639429899c24ae876f91185375e985249`; there was no intervening work.

Added:

- `proofs/informal/problem1_dyadic_zero_target_period_parity_classification.md`

Research commit: `a216033a9156d9a178886b9182adcf6533a67777`.

## New results

For ambient dyadic period `p=2^n`, write a zero-target word as `w=b^(p/d)`, where `d` is its exact rotational period and `b` its primitive block.

1. **Odd parity automatically implies full period.** If `d<p`, then `p/d` is even, so the parity of `w` must be even. Therefore every odd-parity zero-return leaf at dyadic `p` has exact period `p`. The separate leaf-legality/full-period check is unnecessary.

2. **Primitive-block parity exactly classifies genuine branching.** Combining the run-66 phase-collapse criterion with exact rotational period shows that, for even `w`, its two derivative integrations are phase-equivalent iff the primitive block `b` has odd parity. They are distinct necklaces iff `b` has even parity.

3. **Every full-period even target genuinely branches.** Its primitive block is itself and has even parity. Thus the 15 full-period even internal vertices found in `G_16` were structurally forced to be binary branch vertices.

Together with runs 71--72, the dyadic terminal reverse basin is a finite rooted tree; every odd leaf is automatically a legal full-period initial necklace; and every even non-root vertex is locally classified by primitive-block parity.

## Best next target

The counting problem can now be reduced to the primitive-period/parity distribution of reachable even zero targets. Seek a `p -> 2p` recurrence for the number of reachable even zero targets with even-parity primitive block. Primitive-odd targets are phase-collapsed unary vertices; primitive-even targets are genuine binary branch vertices. Treat the terminal root/self-loop convention separately.
