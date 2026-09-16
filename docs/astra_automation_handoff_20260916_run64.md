# Astra automation handoff — run 64 — 2026-09-16

## Result

Problem 1 remains open, but the reverse-basin induction was narrowed substantially.

New proof note:

- `proofs/informal/problem1_reverse_predecessor_uniqueness_reset_lemma.md`

Research commit before this handoff:

- `618b1ca76ea1ba28e44f24be64a8ae3d118a9fec`

## New lemma

For the reverse predecessor equation

    w = Sx xor (u OR x),

if `u != 0`, there is at most one cyclic predecessor `x`.

Reason: coordinatewise,

    x_(j+1) = w_j xor (u_j OR x_j).

At any coordinate where `u_j=1`, the next bit is independent of the previous bit. Thus the difference between two candidate solutions is reset to zero and can never reappear around the cycle.

If `u=0`, the equation is

    Sx xor x = w,

so it has zero or exactly two complementary solutions, with solvability iff `w` has even XOR parity.

## Why this matters

All reverse branching is now proved to occur only at zero-column events. The derivative singularities at depths 9, 30, and 401 are therefore instances of the only possible branching mechanism, not merely a repeated empirical pattern.

Run 63 already proves that at the scale-transition equation `Sx xor x = E(c_p)`, the two complementary solutions are related by a half-period shift and hence are one temporal necklace. Therefore the connector cannot branch at all while its middle column is nonzero.

## Next target

Do not enumerate arbitrary predecessor trees. Track only zero-column events after the canonical derivative lift. Prove that every such event before the legal initial pair either cannot occur or yields two integrations equivalent modulo temporal phase. This is now the remaining obstruction to reverse-basin uniqueness modulo phase.
