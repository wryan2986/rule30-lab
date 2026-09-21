# Astra automation handoff — run 176

Problem 1 remains OPEN.

Run 176 found and corrected an important domain error in the continuation proposed by runs 174–175.

The terminal `beta` in the surviving one-bit gate-u nonresetting passage is NOT an arbitrary nonnegative delay. In `problem1_nonreset_return_birth_spacing.md` it is explicitly the Boolean cyclic-source birth indicator

    beta = 1 XOR eta,

so `beta in {0,1}`. The same theorem identifies `tau(Y_(t+6))=beta`.

Run 175's exact original-cut result remains valid, but specializes to only two itineraries:

    beta=0: (0,1,1,0,2,1), charge -1;
    beta=1: (0,1,1,0,2,2), charge  0.

Therefore the prior proposed target of forcing `beta>=2` is impossible. Do not pursue terminal-beta magnitude escalation.

This makes the telescope obstruction sharper: every surviving one-bit nonresetting passage has nonpositive six-step signed residence charge. Any all-depth contradiction must instead control hidden zero-delay slack, build a genuinely non-telescoping charge, or constrain the pattern/transport of the Boolean beta values across successive separated episodes and their resetting/cyclic interludes.

New proof/correction note: `proofs/informal/problem1_run176_terminal_beta_is_boolean_and_cannot_escalate.md`.

Next target: revisit the complete-core/global-shadow state at the end of the two beta cases and ask whether either case can feed another sufficiently late one-bit nonresetting source after the proven >=8 spacing. Seek a conserved/monotone driver property across that gap; do not extend a bounded gate prefix without an all-depth invariant.
