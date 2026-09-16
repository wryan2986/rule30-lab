# Astra automation handoff — run 63 (2026-09-16)

Problem 1 remains open.

## New exact progress

The derivative lift at every scale transition is now structurally understood more sharply. If `c` has length `p` and odd XOR parity, and `x` solves

    Sx xor x = E(c)=cc

on the length-`2p` cycle, then necessarily

    x_(j+p) = x_j xor 1.

This follows by XORing `p` consecutive coordinate equations: every length-p window of `cc` is a rotation of `c` and therefore has parity one.

Consequences:

- the two solutions of the derivative equation are complements;
- antiperiodicity shows that complementing is exactly shifting by `p`;
- therefore the apparent two-way derivative branch is only one cyclic necklace modulo phase;
- for dyadic `p`, the lift has exact period `2p`;
- the lift is explicitly the cyclic cumulative-XOR integral of `cc`, unique modulo phase.

Full note: `proofs/informal/problem1_derivative_lift_antiperiodicity.md`.

## Next target

The scale transition is now: embedded lower-period reverse orbit -> one canonical doubled-period derivative-lift necklace modulo phase -> post-lift connector -> legal `(0,c_(2p))`.

Focus on the connector after this canonical lift. Determine whether its reverse predecessor is unique modulo phase at every step until the legal initial pair, and search for a block-level description relating that connector to the forward/reverse orbit of the lift itself. Do not treat the two integration constants as distinct branches; they are half-period shifts of one another.
