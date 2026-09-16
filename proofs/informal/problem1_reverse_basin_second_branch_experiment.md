# Problem 1: reverse basin after the first period-four branch

## Status

Problem 1 remains open. This note continues the exact reverse-basin calculation after the first branch identified in run 58.

The recurrence is

    q_(i+2) = S q_i xor (q_(i+1) OR q_i)

on cyclic binary words. Run 58 showed that the first reverse branch, at `q_(N-9)`, consists of the two complementary period-four words solving

    S v xor v = A,

where `A=alt_p`.

## Exact predecessors immediately after the first branch

I solved the predecessor equations directly. For either of the two period-four branches `v`, the next predecessor is unique:

    q_(N-10) = 1^p.

Indeed it must solve

    0 = Sx xor (v OR x).

Direct bit propagation around the four-periodic pattern forces `x=1`.

The following predecessor is also unique. Since

    v = Sx xor 1,

we obtain

    q_(N-11) = S^(-1)(not v),

again a period-four word. Continuing the exact finite predecessor equations produces only period-four words for several more layers. For one phase convention the sequence beginning at `q_(N-9)` is

    0110..., 1111..., 1100..., 0001..., 1011..., 0111..., 0110..., ...

where each displayed block repeats with temporal period four. The complementary first branch gives the corresponding shifted/complementary sequence.

Thus the first reverse branching does **not** immediately proliferate into arbitrary temporal words: it enters a rigid period-four subsystem.

## Exact finite computation at p=8

I exhaustively enumerated all predecessor words at temporal length `p=8` (only 256 candidates per reverse equation, so this is exact, not heuristic).

For each of the two `q_(N-9)` branches, every predecessor equation is unique for the next 20 reverse layers. The second reverse branching occurs only on the 21st predecessor equation after `q_(N-9)`. At that point there are exactly two predecessors.

For the phase with first branch

    v = 01100110,

the second branch occurs from the pair whose current word is `00000000` and next/output-side word is `10111011`; its two predecessors are

    01101001
    10010110.

For the complementary first branch

    v = 10011001,

the corresponding second branch has predecessors

    01011010
    10100101.

The two solutions in each case are complements. This is consistent with another discrete-derivative kernel appearing at the next scale.

## Structural implication

This is useful evidence for a hierarchical reverse basin. The first branch creates a period-four choice, after which the reverse orbit is rigid for a long interval; at `p=8`, the next noninvertible predecessor equation again creates exactly a complementary pair. That is qualitatively what a dyadic-scale induction would need.

However, this note does **not** yet prove that the second branch always occurs at a fixed symbolic state, nor that its existence forces `8 | p`. The `p=8` calculation should be treated as an exact finite experiment guiding the next algebraic derivation.

## Next target

Derive symbolically the rigid period-four reverse subsystem after `q_(N-9)` and identify the equation at its next loss of invertibility. The computational `p=8` result suggests that the next branch may again reduce to a cyclic derivative equation whose solvability imposes the next dyadic divisibility condition. If so, iterating that mechanism could explain both the unique-necklace phenomenon and why long terminating trajectories require progressively larger powers of two in the temporal length.
