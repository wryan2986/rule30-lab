# Problem 1: derivative lifts are antiperiodic and unique modulo phase

Status: exact lemma.

Let `c` be a cyclic bit word of length `p` with odd XOR parity, and let `E(c)=cc` be its repetition to length `2p`. At the reverse-basin scale transition, a predecessor `x` satisfies

    Sx xor x = E(c).                    (D)

## Antiperiodicity lemma

Every solution of (D) satisfies

    x_(j+p) = x_j xor 1                 (A)

for every index modulo `2p`.

Proof: coordinatewise, (D) says `x_(j+1) xor x_j = E(c)_j`, up to the fixed shift orientation. XOR the next `p` equations. Interior terms cancel, giving

    x_(j+p) xor x_j = XOR_{k=0}^{p-1} E(c)_(j+k).

Every length-p window of `E(c)` is a cyclic rotation of `c`, so the right side is the parity of `c`, namely 1. This proves (A).

## Consequences

The two solutions of (D) differ by the constant-one kernel of `S+I`, so they are complements. But (A) gives

    S^p x = x xor 1.

Hence the two complementary derivative lifts are related by a half-period cyclic shift. After quotienting temporal words by cyclic phase, the apparent two-way reverse branch is actually one necklace.

Also, (A) rules out period `p`. When `p` is a power of two, a word on the `2p` cycle whose period does not divide `p` must have exact period `2p`. Thus the derivative lift automatically has exactly the period growth required by the dyadic scale transition.

There is an explicit construction: fix `x_0=0` and take cumulative XORs of `E(c)` around the cycle. The second integration constant gives the complement, which is already the same cyclic orbit by (A). Therefore an odd lower-period necklace canonically determines one doubled-period derivative-lift necklace modulo phase.

## Relevance

The run-62 embedding lemma left the post-lift connector as the new object at each scale. This result narrows that target: there is only one starting lift necklace modulo phase, not two independent branches. An all-scale uniqueness proof only needs to establish rigidity from that single lift necklace to a legal `(0,c_(2p))` pair, modulo phase.

This does not prove that the connector reaches a legal higher-period initial pair or that later branching cannot occur. It does prove that the first apparent binary branch at every scale is purely phase symmetry and cannot itself create multiple terminating necklaces.
