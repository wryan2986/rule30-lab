# Distinguished source: exact four-step transport of the shadow right pair

Status: `partial-proof`. This is an exact finite-cone consequence of the already established distinguished source motif. It does not prove a finite birth budget or solve Problem 1.

## Setup

At the distinguished cyclic source `q=t+2` in the two-bit nonreset return passage, previous work gives

    (hat r_-5,...,hat r_2)(q) = 10101110.

Write the first wider right-driver bits

    a = hat r_3(q),
    b = hat r_4(q),
    c = hat r_5(q),
    d = hat r_6(q).

All cells below are cells of the same global shadow. Apply Rule 30 exactly, with

    F(l,c,r) = l XOR (c OR r).

## Two-step transport

Direct two-step cone reduction gives

    hat r_1(q+2) = 1 XOR a,
    hat r_2(q+2) = 1,

as already noted in the preceding staircase result. Keeping the next cells gives

    hat r_3(q+2) = a OR ((NOT b) AND (NOT c)),

and

    hat r_4(q+2)
      = (a AND b AND c)
        OR (a AND b AND d)
        OR ((NOT a) AND (NOT b) AND c)
        OR ((NOT a) AND (NOT b) AND d).

The important point is that the first two right cells at the intermediate `u` gate source depend only on `a`, and in particular the second one is rigidly 1.

## Four-step collapse

Propagating the same cone two more Rule-30 steps simplifies much more strongly:

    hat r_1(q+4) = a,
    hat r_2(q+4) = a OR b.

Thus the right pair at the forced one-bit `t` source `q+4=t+6` is exactly

    (a, a OR b).

It is independent of every source bit from `hat r_5(q)` rightward.

Equivalently, the pair can only be

    (a,b) = 00 -> 00,
            01 -> 01,
            10 -> 11,
            11 -> 11.

Therefore the zero-pair flag at `q+4` is exactly

    [hat r_1(q+4)=0 and hat r_2(q+4)=0]
      = (NOT a) AND (NOT b).

This is a genuine finite-state transport relation across the complete `t -> u -> t` passage: although the wider driver at `q+2` still depends on farther cells, the two-cell flag relevant to later shadow/gate arguments remembers only the original pair `(hat r_3(q),hat r_4(q))`.

## Verification

The identities were checked by exhaustive truth-table evaluation of the exact Rule-30 cone. For the four-step right pair, all assignments of the needed wider source cells were enumerated; the resulting values always reduced to `(a, a OR b)`. This is finite-exhaustive validation of the displayed local identity, not evidence for an infinite FULL orbit.

## Consequence and next target

The wider-driver search suggested after the staircase lemma does have a nontrivial bounded quotient: the right zero-pair flag after the `t -> u -> t` passage is determined by only two bits of the distinguished source driver.

What is not yet known is whether the resetting one-bit `t` source at `q+4` and its subsequent FULL gate passage constrain or transport this flag in a way that gives bounded reuse or a finite birth budget. The next useful calculation is to combine `(hat r_1,hat r_2)(q+4)=(a,a OR b)` with the already proved resetting-source phase/gate identities, rather than expanding an unrestricted wider driver word.

Problem 1 remains OPEN.
