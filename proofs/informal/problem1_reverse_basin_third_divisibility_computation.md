# Problem 1: third reverse singularity forces 16-divisibility (exact finite block computation)

## Status

Problem 1 remains open. This note extends the proved dyadic reverse-basin pattern by one scale using an exact exhaustive computation on the primitive period-8 block. It is a computer-assisted finite block result, not yet the desired all-scale induction.

The reconstruction recurrence is

    q_(i+2) = S q_i xor (q_(i+1) OR q_i),

and a predecessor `x=q_(k-1)` of a known pair `(q_k,q_(k+1))=(u,w)` satisfies

    w = S x xor (u OR x).                 (R)

For fixed cyclic length p, (R) has at most two solutions: fixing one boundary bit determines every other bit successively around the cycle, and the final closure equation either accepts or rejects each of the two seeds. Thus predecessor enumeration does not require brute force over `2^p` words.

## Exact reverse-tree singularity depths

Starting from the first terminal zero pair and excluding the trivial extension by another zero, exact predecessor propagation gives the following loss-of-invertibility depths (counting predecessor equations backward from the terminal pair):

    depth 4    : two phase choices in the universal terminal suffix
    depth 9    : first derivative singularity
    depth 30   : second derivative singularity
    depth 401  : third derivative singularity

At temporal length p=8, all eight branches present immediately before depth 401 have no predecessor. At p=16, every one of those eight branches has exactly two predecessors, producing sixteen branches. The same depth-401 branching occurs at p=32.

This cleanly isolates the next divisibility obstruction: p=8 dies exactly where p=16 survives.

## Form of the third singular equation

Immediately before the depth-401 predecessor equation, every branch has `u=0`. The other word `w` is a repetition (up to cyclic phase/complement conventions inherited from earlier branches) of a primitive 8-bit block of odd XOR parity. One representative at p=16 is

    w = 11000010 11000010.

The primitive block `11000010` has three ones, hence odd XOR parity. Therefore (R) reduces to

    S x xor x = h,

where `h` is 8-periodic with odd parity on each primitive 8-bit block.

For a cyclic binary word, `Sx xor x=h` is solvable iff total XOR parity of `h` is zero. If the temporal length p is a multiple of 8, then

    parity(h) = (p/8) mod 2.

Consequently the depth-401 predecessor exists iff `p/8` is even, i.e.

    depth-401 survival => 16 | p.

When solvable, the kernel of `S+I` consists of the two constant words, so each incoming branch has exactly two complementary predecessors. At p=16, for the representative above, they are

    0100000110111110
    1011111001000001,

which are complements.

## Why the finite block computation is exact

The computation uses only Boolean recurrence (R) and cyclic closure. Between the depth-30 and depth-401 singularities, the states remain 8-periodic. Therefore checking the forced segment on one primitive 8-bit block is sufficient for every p divisible by 8: the same block repeats around the temporal cycle until the singular derivative equation is reached. No probabilistic search or heuristic trajectory sampling is involved.

The result is nevertheless labelled computer-assisted because the 370 intervening forced predecessor equations were propagated mechanically rather than compressed into a human symbolic recurrence.

## New structural evidence

The first three derivative singularities now have the same exact shape:

1. an odd-parity primitive 2-block obstruction forces `4 | p`;
2. after a forced period-4 segment, an odd-parity primitive 4-block obstruction forces `8 | p`;
3. after a forced period-8 segment, an odd-parity primitive 8-block obstruction forces `16 | p`.

The singularity depths are `9, 30, 401` under the present indexing. Their rapid growth explains why naive forward/reverse enumeration becomes expensive even though each predecessor equation itself has at most two solutions.

## Remaining gap

This is strong evidence for the proposed renormalized induction, but three scales do not prove it. The next task should seek a transformation of the forced block-level reverse orbit that maps the scale-`2^m` segment to the scale-`2^(m+1)` segment and explains both (a) why the next singular right-hand side has odd parity per primitive block and (b) why the singularity depth changes from 9 to 30 to 401. A successful recurrence for the block orbit or singularity depth would replace the 370-step computer-assisted segment with an all-scale theorem.
