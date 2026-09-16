# Problem 1: second reverse branch forces 8-divisibility

## Status

Problem 1 remains open. This note upgrades run 59's p=8 second-branch experiment to a symbolic divisibility result.

The reconstruction recurrence is

    q_(i+2) = S q_i xor (q_(i+1) OR q_i)

on cyclic binary temporal words of length p. Run 58 proved that reaching sufficiently far backward from a terminal zero pair first requires `4 | p`, and the first branch `q_(N-9)` is one of the two period-four solutions of `S v xor v = alt_p`.

## Reverse equation

Given consecutive words `(q_k,q_(k+1))=(u,w)`, a predecessor `x=q_(k-1)` must satisfy

    w = S x xor (u OR x).                 (R)

Once the first branch has been chosen, all words are 4-periodic. Therefore (R) can be solved on one four-bit block until another singular equation is encountered; repeating that block around the temporal cycle gives the general p solution whenever `4 | p`.

## Exact four-periodic propagation

Choose one phase of the first branch. Direct substitution in (R), block by block, gives a unique predecessor at each of the next twenty reverse equations. One convenient phase convention starts with the repeating block `0110` and passes through the following four-periodic states (cyclic rotations depend on the convention):

    0110 -> 1111 -> 0011 -> 1000 -> 1101 -> 1110 -> 0110 -> 0011
         -> 1011 -> 0001 -> 1100 -> 1001 -> 0110 -> 1110 -> 0011
         -> 1010 -> 0001 -> 0011 -> 1101 -> 1101 -> 0000.

Each arrow here is obtained by solving (R) with the preceding adjacent state retained; uniqueness is checked by the four local Boolean equations, not by an assumption of invertibility. The complementary/shifted first branch gives the corresponding shifted sequence.

At the next predecessor equation the current word is zero and the output-side word is a repetition of a four-bit word of odd Hamming/XOR parity (in this phase, `1101`; another shift convention gives the equivalent `1011`). Thus (R) reduces exactly to

    S x xor x = h,

where `h` is 4-periodic and has odd parity on each four-bit block.

## Divisibility consequence

For a cyclic binary word, the derivative equation

    S x xor x = h

is solvable iff the total XOR parity of `h` is zero. Since `h` consists of `p/4` copies of an odd-parity four-bit block,

    parity(h) = (p/4) mod 2.

Therefore the second reverse branch exists iff `p/4` is even. In particular,

    sufficiently deep termination past this branch => 8 | p.

When solvable, the kernel of `S+I` is exactly the two constant words, so there are exactly two predecessor solutions and they are complements. At p=8 these are the complementary pairs observed in run 59 (`01101001` / `10010110`, up to the phase convention).

## What this establishes

The first two losses of reverse invertibility now have the same mechanism:

1. the first derivative equation has an alternating right-hand side and forces `4 | p`;
2. after a rigid four-periodic reverse segment, the second derivative equation has an odd-parity four-periodic right-hand side and forces `8 | p`.

This is the first proved iteration of the dyadic divisibility mechanism suggested by the terminating-necklace experiments. It is stronger than the p=8 computation: it applies to arbitrary temporal length p once the reverse trajectory is deep enough to reach this second singular equation.

## Remaining gap

This does not yet prove the general induction `2^m | p` at the m-th reverse singularity. The next task is to formulate the rigid segment and singular right-hand side recursively, rather than enumerate a longer period-eight block by hand. A useful target is a renormalized reverse map on block words: show that after a derivative branch at scale `2^m`, the uniquely forced reverse segment reaches another equation `Sx xor x = h_m` where `h_m` is `2^m`-periodic with odd parity per primitive block. That would force one additional factor of two in p at every level.