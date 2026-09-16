# Problem 1: p=16 zero-column audit finds genuine necklace branching

## Purpose

Run 67 proposed auditing the known period-16 terminating reconstruction after the complete p=8 audit showed no genuine reverse necklace branching. This note performs that exact finite test.

The result is negative for the hoped-for all-scale invariant: at p=16 there are nonterminal zero-column targets of full primitive period 16 and even XOR parity. Their two derivative integrations are not related by temporal rotation. In fact, following one such alternative reverse branch produces a second, rotation-inequivalent odd-parity period-16 initial word whose forward reconstruction also terminates.

## Convention

Use the same direct recurrence as run 67,

\[
q_{i+2}=S q_i\oplus(q_{i+1}\lor q_i),
\]

with cyclic temporal shift `S`, and initial pair `(q0,q1)=(0,c)`.

Reverse predecessors satisfy

\[
w=Sx\oplus(u\lor x).
\]

By the exact predecessor classification, a reverse predecessor is unique when `u != 0`; when `u=0`, the equation is `Sx xor x=w`, which has two complementary solutions exactly when `w` has even XOR parity.

## A terminating p=16 trajectory

Exact reverse propagation from the terminal pair, quotienting only by cyclic rotation, finds the odd-parity full-period representative

`c16_a = 0000010101000101`

(integer 1349 in the script convention).

Direct forward propagation independently verifies

`(0,c16_a) -> ... -> q87867=q87868=0`,

so its termination width is

\[
N_{16,a}=87867.
\]

The nonterminal zero columns on this trajectory are:

- `q29580=0`, target `q29581=1000101110111101`;
- `q34659=0`, target `q34660=0011000011000101`;
- `q87467=0`, target `q87468=1100001011000010=(11000010)^2`;
- `q87838=0`, target `q87839=1101110111011101=(1101)^4`;
- `q87859=0`, target `q87860=0101010101010101=(01)^8`;
- `q87864=0`, target `q87865=1111111111111111`;
- `q87867=0`, followed by terminal zero.

The last four nonterminal targets satisfy the run-66 phase-equivalence criterion: their primitive repeating blocks have odd XOR parity.

The first two do not.

### First failure

`1000101110111101` has exact rotational period 16 and Hamming weight 10, hence even XOR parity. Its only period-16 repeating block is the full word, whose parity is even. Therefore the two solutions of

\[
Sx\oplus x=1000101110111101
\]

are complementary but **not** cyclic rotations of one another.

Likewise `0011000011000101` has exact rotational period 16 and Hamming weight 6, so it also produces two genuinely different predecessor necklaces.

Thus the proposed invariant from run 67,

> every nonterminal zero-column target on a terminating dyadic trajectory has an odd-parity primitive rotational block,

is false already at p=16.

## Stronger consequence: a second terminating p=16 necklace

The genuine branch at `q29580=0` is not merely a dead algebraic branch.

One derivative integration is the predecessor lying on the `c16_a` trajectory. Following the other integration backward, using the unique predecessor at every nonzero middle column, reaches after 171051 reverse steps another legal zero-boundary state

`(0,c16_b)` with

`c16_b = 1001110010100010`

(integer 40098).

This word has odd XOR parity, exact rotational period 16, and is not a cyclic rotation of `c16_a`.

Direct forward propagation from `(0,c16_b)` independently verifies termination at

\[
N_{16,b}=229338.
\]

Therefore there are at least two rotation-inequivalent odd-parity terminating period-16 initial necklaces under this reconstruction convention:

- `0000010101000101`, terminating at width 87867;
- `1001110010100010`, terminating at width 229338.

This falsifies the stronger working conjecture that the terminating necklace is unique at every dyadic temporal period.

## Reproducibility

All claims above use exact integer bit operations only.

Forward recurrence:

1. set `q0=0`, `q1=c`;
2. compute `q[i+2]=rotl(q[i],16) XOR (q[i+1] OR q[i])`;
3. stop at the first consecutive zero pair.

For `c=1349`, this gives 87867 steps to the terminal zero pair. For `c=40098`, it gives 229338.

To audit a zero target `w`, compute its minimal cyclic period and XOR parity. At a zero middle column, solve `rotl(x,16) XOR x=w`; even parity gives exactly two complementary solutions. Run 66's criterion determines whether those two solutions are rotations. The two full-period even-parity targets above fail that criterion.

## Research consequence

The reverse-basin program should no longer aim to prove global necklace uniqueness: that statement is false at p=16.

The useful surviving structure is:

- reverse propagation is still exactly deterministic away from zero columns;
- zero columns are still the only branching/death locations;
- inherited scale-transition singularities still have the antiperiodic phase collapse proved earlier;
- but additional zero returns can create genuine branches, and at least one such branch reaches a distinct legal terminating initial necklace.

A better next target is to classify the induced zero-column first-return graph rather than trying to collapse it to one path. In particular, enumerate all p=16 legal odd-parity zero-boundary ancestors of the terminal pair (modulo rotation) and determine whether the graph is finite and whether its branching has a recursive relation to the p=8 graph. That could replace the disproved uniqueness induction with a controlled branching/renormalization statement.
