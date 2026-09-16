# Astra automation handoff — run 66 — 2026-09-16

## Result

Problem 1 remains open, but the connector-comparison part of run 65's zero-column first-return target is now solved.

The unique reverse predecessor map off `u=0` is shift-equivariant. Therefore, if the two complementary derivative lifts at a zero-column event differ by a temporal shift, their entire deterministic reverse connectors remain related by that same shift. They reach the next zero column at the same depth with phase-equivalent return data. A deterministic connector can never split one lift necklace into two necklaces.

This applies immediately to every known dyadic scale transition: run 63 proved `S^p x = x xor 1` for lifts of `E(c_p)=c_p c_p`, so the two apparent branches remain one necklace throughout the whole post-lift connector, not merely at the first lifted word.

## New note

- `proofs/informal/problem1_zero_return_phase_equivariance.md`

## General criterion

For an arbitrary even-parity zero-column target `w`, its two integrations of `Dx=w` are phase-equivalent iff `w` has a rotational period `k` such that a length-`k` period block has odd XOR parity. Indeed `S^k w=w` implies `S^k x` is one of the two integrations; the block parity decides whether it equals `x` or `x xor 1`.

Thus the remaining first-return problem is entirely a singularity problem: classify the zero-column target words encountered in the terminating basin and show each surviving target has such an odd-parity rotational block, or identify the first counterexample. There is no longer any need to compare connector interiors.

## Next target

Compute or derive the sequence of zero-column target necklaces along the known terminating reverse orbit at `p=8` and, if feasible, `p=16`, checking the odd-parity rotational-block criterion at every even-parity singularity. A failure would expose genuine necklace branching; success would sharpen the all-scale conjecture to a statement purely about zero-return targets.
