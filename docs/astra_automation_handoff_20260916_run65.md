# Astra automation handoff — run 65 — 2026-09-16

## Result

Problem 1 remains open, but run 64's reverse-predecessor uniqueness lemma has been strengthened to an exact existence/cardinality theorem.

For

    w = Sx xor (u OR x),

if `u != 0`, there is **exactly one** cyclic predecessor `x`, not merely at most one. Pick any `k` with `u_k=1`; then `x_(k+1)=w_k xor 1` is fixed independently of `x_k`, and a single sweep around the cycle determines all remaining bits. The anchor equation is automatically satisfied on return. This is an O(p) constructive inverse.

If `u=0`, the equation is `Sx xor x=w`: odd-parity `w` has no predecessor, while even-parity `w` has exactly two complementary predecessors.

Therefore every reverse compatibility failure and every reverse branch occurs only at zero middle columns. Between zero-column events, reverse propagation is guaranteed to exist and is completely deterministic.

## New note

- `proofs/informal/problem1_reverse_predecessor_exact_classification.md`

## Main conceptual reduction

The reverse basin can now be compressed to a first-return dynamics on zero-middle-column states. At `(0,w)`, parity decides death versus a complementary derivative lift; after a lift, the trajectory is forced until the next zero middle column. Together with run 63's antiperiodicity result, known scale-transition complementary lifts are one temporal necklace modulo phase.

## Next target

Construct/analyze the induced zero-column first-return map: integrate an even-parity `w`, follow the unique inverse until the next zero middle column, and determine whether the two complementary starting lifts always yield phase-equivalent return data in the terminating basin. If this descends to a single-valued map on necklaces, it is a much smaller object on which to attack unique termination.
