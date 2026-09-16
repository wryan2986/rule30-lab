# Astra automation handoff — run 62 (2026-09-16)

Problem 1 remains open.

## New structural progress

The reverse singularity depths `9,30,401` are now explained: they are exactly one more than the independently computed lower-period termination columns

    N_2=8, N_4=29, N_8=400.

This follows from a repetition-embedding lemma. Repeating a cyclic p-word twice commutes with shift, XOR, OR, the forward reconstruction, and the reverse predecessor equation. Therefore, whenever the lower-period reverse path from `(0,0)` to `(0,c_p)` is unique, the length-2p reverse path must initially retrace that entire lower-period path embedded by repetition.

Immediately before the embedded initial pair `(0,E(c_p))`, the next predecessor equation is

    Sx xor x = E(c_p).

Since `c_p` has odd parity, the corresponding equation has no solution at period p. Its doubled repetition has even parity, so at period 2p it has exactly two complementary solutions. Thus every scale transition consists of: inherited lower-period reverse orbit -> derivative parity obstruction -> two complementary lifts -> genuinely new connector segment.

This turns the previously mysterious long forced intervals into already-known lower-period trajectories. Full note: `proofs/informal/problem1_reverse_singularity_depth_embedding_lemma.md`.

## Next target

Do not spend a run re-propagating the inherited interval or guessing a recurrence from `9,30,401`. Focus only on the post-lift connector: starting from the two solutions of `Sx xor x=E(c_p)`, characterize why reverse propagation is rigid (up to phase/complement symmetry) until it reaches a legal `(0,c_(2p))` pair. If this connector admits a scale-independent/block-recursive description, it would combine with the embedding lemma into an all-scale induction for the unique-necklace phenomenon.
