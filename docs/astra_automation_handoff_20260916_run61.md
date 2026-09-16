# Astra automation handoff — run 61 (2026-09-16)

Problem 1 remains open.

## New exact computer-assisted progress

The reverse-basin dyadic mechanism has been extended through a third singular scale. Using the exact predecessor equation

    w = S x xor (u OR x),

and the fact that a boundary seed determines the whole candidate predecessor, the reverse tree was propagated without brute-forcing all binary words.

After the previously proved singularities at reverse depths 9 and 30, the next loss of invertibility occurs at depth 401. Immediately before it, the current word is zero and the target word is 8-periodic with odd parity on each primitive 8-bit block; a representative block is `11000010` (three ones). Hence the predecessor equation is

    S x xor x = h,

with odd parity per 8-block. Cyclic solvability therefore requires an even number of 8-blocks:

    16 | p.

Exact checks agree with the symbolic parity conclusion: at p=8 all eight incoming branches die at depth 401; at p=16 every incoming branch has exactly two complementary predecessors; p=32 behaves likewise at this singularity.

Full note: `proofs/informal/problem1_reverse_basin_third_divisibility_computation.md`.

## Evidence classification

This is exact finite block computation plus a general parity argument once the period-8 forced segment is reached. It is not an all-scale induction. The 370 forced predecessor equations between depths 30 and 401 were propagated mechanically and have not yet been compressed into a human symbolic recurrence.

## Next target

Do not simply push to the next singularity. Find a renormalization/block transformation explaining the scale sequence itself. The first three derivative singularities now force 4-, 8-, and 16-divisibility and occur at depths 9, 30, and 401. Seek a recurrence or conjugacy on the forced primitive block orbit that maps the scale-`2^m` reverse segment to scale `2^(m+1)`, preserves the odd-parity singular right-hand side, and ideally explains the singularity-depth sequence. That would turn the three-scale computer-assisted pattern into the needed induction.