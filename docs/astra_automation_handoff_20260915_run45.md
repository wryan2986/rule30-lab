# Astra automation handoff — 2026-09-15 run 45

## Repository state reviewed

Started from run 44 tip `7d5322542c209b065d30f3498c1ca7ecd5d7648c`. No intervening commits were present.

Run 44 showed that a naked late boundary hit is not backward-monotone under the accelerated Rule-30 map, so the run-43 many-to-one-depth pullback cannot operate on scalar hit indicators.

## New result this run

Added `proofs/informal/problem1_doubling_antiperiodic_fiber_certificate.md`.

For a one-bit lift `x(t)=2u(t)+b(t)` where the parent has exact period `p` and the child genuinely doubles to exact period `2p`, the omitted-bit return map is the transposition of the two-point fiber. Therefore

`b(t+p) = 1 XOR b(t)` for every phase `t`.

This is an iff certificate for the doubling branch: the new temporal column is exactly antiperiodic at the parent period.

Along a tower `p,2p,...,2^r p`, successive genuine doublings therefore leave complement-symmetry witnesses at distinct temporal scales.

## Important negative conclusion

Total column parity does not count these doublings: over a doubled cycle the fiber contains exactly `p` ones, so for `p>1` its full-cycle XOR parity is even. The useful information is the half-period complement relation, not occupancy or scalar parity.

## Remaining blocker

The antiperiodic witness is local to the periodic forced state at a doubling passage. To contradict finite entry, multiple such witnesses must be transported simultaneously into a common spacetime window of the *same original realization*. Run 44 prevents reducing this to backward transport of one selected nonzero bit.

## Next target

Revisit the exact common-origin/joint-window transport formulas and ask whether they preserve a two-time relation of the form `(b(t), b(t+p)) = (0,1)` or `(1,0)`. A useful theorem would pull `r` doubling passages into one common-origin joint window while retaining `r` distinct complement scales, then lower-bound that window's activity/complexity as a function of `r`.

Problem 1 remains open.