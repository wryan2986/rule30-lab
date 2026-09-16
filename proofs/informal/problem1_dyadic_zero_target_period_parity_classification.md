# Problem 1: dyadic zero-target period/parity classification

## Purpose

Runs 66--72 reduced the terminal reverse basin at fixed period to a finite rooted zero-return tree modulo temporal rotation. Two local questions remained:

1. when does an even-parity zero target genuinely branch rather than have its two derivative integrations collapse to one necklace?;
2. when an odd-parity zero target is reached, must it have full period and hence be a legal period-`p` initial word?

For dyadic ambient period, both questions have immediate answers from the primitive rotational period.

## Setup

Let the ambient cyclic word length be

\[
p=2^n.
\]

For a word `w` of length `p`, let `d` be its exact rotational period. Since `d | p`, we have `d=2^m` for some `m <= n`. Write

\[
w=b^{p/d},
\]

where `b` is the primitive block of length `d`. Let `P(z)` denote XOR parity (Hamming weight modulo 2).

Then

\[
P(w)=(p/d)P(b) \pmod 2.
\]

## Theorem 1: odd parity forces full period at dyadic length

If `P(w)=1`, then `d=p`.

### Proof

If `d<p`, then `p/d` is a power of two greater than one and is therefore even. Hence

\[
P(w)=(p/d)P(b)=0 \pmod 2,
\]

contradicting `P(w)=1`. Therefore `d=p`. QED.

### Consequence for the terminal reverse tree

At a zero-column state, an odd-parity target has no derivative predecessor and is therefore a leaf of the reverse zero-return tree. At dyadic ambient period, every such leaf automatically has exact period `p` by Theorem 1.

Thus the separate condition "odd leaf is full-period/legal" is redundant:

\[
\boxed{\text{every odd-parity zero-return leaf at dyadic }p\text{ is automatically full-period}.}
\]

This explains structurally why all 16 leaves found in the complete `p=16` graph had exact period 16; no enumeration was needed to establish their legality once their parity was known.

## Theorem 2: exact branch criterion from primitive-block parity

Assume `P(w)=0`, so the derivative equation

\[
Dx=Sx\oplus x=w
\]

has the two complementary integrations `x` and `x\oplus 1`.

Run 66 proved that these two integrations are phase-equivalent iff `w` has a rotational period `k` for which the XOR parity of a corresponding length-`k` repeating block is odd.

Taking `d` to be the exact rotational period gives a sharper dyadic formulation:

\[
\boxed{\text{the two integrations phase-collapse iff }P(b)=1.}
\]

Equivalently,

\[
\boxed{\text{a nonterminal even zero target genuinely branches iff its primitive block has even parity}.}
\]

### Justification

Any rotational period of `w` is a multiple of the exact period `d`. A block for period `k=rd` is `b^r`, whose parity is `rP(b)`. Therefore some rotational-period block has odd parity iff `P(b)=1` (choose `k=d` in the forward direction; if `P(b)=0`, every multiple-period block also has even parity).

Combining with the run-66 phase-equivalence criterion proves the claim. QED.

## Corollary: every full-period even target genuinely branches

If `d=p`, then the primitive block is `w` itself. Hence an even-parity full-period target has `P(b)=0` and necessarily gives two distinct child necklaces:

\[
\boxed{d=p,\ P(w)=0\quad\Longrightarrow\quad\text{genuine binary branch}.}
\]

So the 15 full-period even internal vertices in `G_16` did not need pairwise branch testing: their exact period and even parity force genuine branching.

## What remains

Together with runs 71--72, the terminal reverse basin at dyadic `p` is a finite rooted tree, every odd leaf is automatically a legal full-period word, and every non-root even vertex is locally classified by one primitive-block parity test.

Therefore the unresolved counting problem can be stated more cleanly:

> Count the reachable even zero-target necklaces whose primitive block has even parity.

Modulo the special treatment of the terminal root/self-loop convention, each such genuine branch contributes one additional leaf, while primitive-odd even targets lie on phase-collapsed unary portions of the tree.

The next `p -> 2p` question should therefore track the primitive-period/parity distribution of reachable even zero targets, rather than separately tracking leaf legality or explicitly comparing complementary integrations.
