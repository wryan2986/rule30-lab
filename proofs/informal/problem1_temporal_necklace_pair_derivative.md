# Problem 1: temporal-necklace period-halving experiment

## Status

Problem 1 remains open. This note continues the run-53 unique-necklace experiment and tests the proposed route from a terminating length-`2p` temporal word to the terminating length-`p` necklace.

## Setup

For a cyclic temporal word `c` of dyadic length `p`, reconstruct columns by

    q_0 = 0,
    q_1 = c,
    q_(i+2) = S q_i xor (q_(i+1) OR q_i).

Run 53 found one terminating rotation orbit for each tested `p=1,2,4,8`, with representatives (up to bit-order convention/rotation)

    p=2:  01
    p=4:  0111
    p=8:  00001011.

The immediate next suggestion was to test whether a terminating length-`2p` necklace simply decimates to the length-`p` necklace.

## Direct decimation fails already at 8 -> 4

I checked every cyclic phase of the known `p=8` necklace. Neither the even-index subsequence nor the odd-index subsequence is a cyclic rotation of the known `p=4` necklace.

Thus the naive induction

    c_(2p) -> even(c_(2p)) = c_p

or

    c_(2p) -> odd(c_(2p)) = c_p

is false already at the smallest nontrivial available test beyond `p=4`.

This should be treated as a dead end: do not build an induction on raw decimation.

## A different period-halving map survives all currently available scales

A more structured map does work on the known necklaces. Choose a cyclic phase and pair consecutive symbols, then take pairwise XOR:

    Delta_2(c)_j = c_(2j) xor c_(2j+1).

For the known `p=4` necklace, there are cyclic phases for which `Delta_2(c_4)` is a rotation of the unique `p=2` necklace.

For the known `p=8` necklace, there are likewise cyclic phases for which `Delta_2(c_8)` is a rotation of the unique `p=4` necklace.

Equivalently, at both tested nontrivial scales,

    [Delta_2(c_(2p))] = [c_p]

holds at the necklace level for a suitable parity/phase choice, where brackets denote cyclic rotation class.

The phase qualification is essential because pairing a cyclic word requires choosing which edge is the first pair boundary.

## Why XOR is structurally plausible

This is not yet a theorem, but XOR is less ad hoc than raw decimation. The reconstructed early columns already contain temporal differences: with `q_0=0, q_1=c`, one has

    q_2 = c,
    q_3 = S c xor c.

Thus temporal XOR derivatives occur naturally in the exact Rule-30 column recursion. A period-halving pair derivative may therefore interact with the reconstruction more naturally than selecting one parity class of samples.

## Cautions

1. This is only checked on the known unique necklaces through `p=8`; it is not evidence sufficient for a proof.
2. The correct phase/pair-boundary choice has not been characterized intrinsically.
3. It has not been proved that `Delta_2` sends *every terminating* length-`2p` word to a terminating length-`p` word.
4. A direct exhaustive `p=16` classification remains computationally expensive with naive trajectory simulation because the state is a pair of 16-bit columns and terminating trajectories may be long (already termination width is about 400 at `p=8`).

## Next target

Try to prove a semiconjugacy or implication of the form

    terminating(c of length 2p)
        => terminating(Delta_2(c) of length p)

for one of the two possible cyclic pair boundaries. The proof should be sought directly from

    q_(i+2) = S q_i xor (q_(i+1) OR q_i),

possibly by decomposing each length-`2p` temporal column into adjacent time pairs and tracking pair XOR plus one auxiliary pair variable. If exact closure requires an auxiliary bit/word, identify the smallest closed quotient rather than assuming `Delta_2` alone closes.

If such a theorem holds, run 53's observed uniqueness can plausibly be attacked inductively. If it fails, produce the smallest terminating counterexample rather than returning to the forced-fiber transport route.