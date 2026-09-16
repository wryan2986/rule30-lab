# Problem 1: phase equivariance of deterministic reverse connectors

## Status

Problem 1 remains open. This note resolves the main ambiguity posed in run 65 for every zero-column event whose two derivative lifts are already phase-equivalent. In particular, it applies to every known dyadic scale-transition lift from run 63.

The reconstruction recurrence is

    q_(i+2) = S q_i xor (q_(i+1) OR q_i),

and a reverse predecessor `x` of a pair `(u,w)` solves

    w = Sx xor (u OR x).

Run 65 proved that when `u != 0` this predecessor exists uniquely.

## Lemma 1: the unique reverse map is shift-equivariant

Let `R(u,w)=x` denote the unique predecessor when `u != 0`. For every temporal shift `S^k`,

    R(S^k u, S^k w) = S^k R(u,w).

Proof: if `x=R(u,w)`, then

    w = Sx xor (u OR x).

Apply `S^k`. Cyclic shift commutes with `S`, XOR, and OR, so

    S^k w = S(S^k x) xor ((S^k u) OR (S^k x)).

Thus `S^k x` is a predecessor of `(S^k u,S^k w)`. Since `S^k u != 0`, run 65 gives uniqueness, proving the identity.

## Lemma 2: phase-equivalent lifts have phase-equivalent entire connectors

Suppose a zero-column state `(0,w)` has even parity, and let its two derivative lifts be `x` and `x xor 1`. Assume they are phase-equivalent:

    x xor 1 = S^k x

for some `k`.

Immediately after choosing the lift, the two reverse states are `(x,0)` and `(S^k x,0)=S^k(x,0)`. As long as the middle column is nonzero, Lemma 1 applies at every reverse step. Inductively, the two reverse trajectories remain exact `S^k` shifts of one another.

Consequently:

1. they reach a zero middle column at exactly the same reverse depth;
2. their return targets are related by the same shift `S^k`;
3. if one reaches a legal initial boundary `(0,c)`, the other reaches `(0,S^k c)`;
4. modulo temporal necklaces, the two connectors are identical.

So no new branch comparison is needed inside a deterministic connector. Once the two lifts at a singularity are one necklace, the entire first-return segment is automatically one necklace.

## Corollary: all known dyadic scale-transition branches collapse globally

Run 63 proved that at the scale transition from period `p` to `2p`, where

    Sx xor x = E(c_p) = c_p c_p

and `c_p` has odd parity, every lift satisfies

    S^p x = x xor 1.

Hence the two complementary lifts differ by the half-period shift `S^p`. Lemma 2 now shows that **their complete post-lift reverse connectors, including the next zero-column return data, differ by that same half-period shift**.

This is stronger than the earlier statement that the two immediate lift words form one necklace: they can never split into inequivalent necklaces later during deterministic reverse propagation.

## Exact criterion at a general zero-column event

For an arbitrary even-parity `w`, let `Dx = Sx xor x = w`. The two lifts `x` and `x xor 1` are phase-equivalent iff there exists `k` such that

    S^k x = x xor 1.

Necessarily `S^k w=w`, because `D` commutes with shifts. Conversely, if `S^k w=w`, then `S^k x` is one of the two integrations of `w`, hence is either `x` or `x xor 1`. Which case occurs is determined by the XOR of any length-`k` arc of `w`:

    x_(j+k) xor x_j = w_j xor w_(j+1) xor ... xor w_(j+k-1).

Thus the complementary lifts are phase-equivalent exactly when `w` has a rotational period `k` whose length-`k` block has odd XOR parity. The dyadic transition `w=c_p c_p` is the special case `k=p`, with odd block parity supplied by eligibility of `c_p`.

## Consequence for the zero-column first-return program

The run-65 question splits cleanly into two parts:

- **Connector problem:** solved. Deterministic reverse propagation cannot turn phase-equivalent lift choices into inequivalent return necklaces.
- **Singularity problem:** still open. One must show that every surviving zero-column target encountered in the terminating basin has an odd-parity rotational block (so its two integrations are phase-equivalent), or otherwise classify any target that fails this criterion.

Therefore future work should inspect only the zero-column target words themselves. There is no need to compare the interiors of paired connector trajectories.
