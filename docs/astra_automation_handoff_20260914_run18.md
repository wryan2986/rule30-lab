# Astra automation handoff — run 18

Problem 1 remains **OPEN**. Continue on `research/astra-next`.

## New result this run

Read:

- `proofs/informal/problem1_return_fringe_boundary_collision_two_bit_defect.md`

Run 17 proved that if

    A^p(z)=z,
    T^p(z)=2^(2p)z+R,
    G=2p-bit_length(R),
    D=floor(G/2),

then

    z,Tz,...,T^D z

are fixed by `A^p`, while

    w=T^(D+1)z

is not.

The new theorem determines the **exact first defect** at that failure.

Put `m=2p`, `u=T^D z`, and `r=T^D(R)`. At this point the remaining corridor length is `G-2D`, hence either `0` or `1`.

For an arbitrary boundary word

    x=2^m u+r,

with top fringe bits

    a=bit_(m-1)(r),
    b=bit_(m-2)(r),

the normalized quotient after one physical Rule-30 step satisfies

    floor(T(x)/2^m)=T(u) XOR eps,

where

    eps=(a OR b)+2*(a AND (1-u_0)).

All quotient bits `>=2` agree exactly with `T(u)`; only the bottom two bits can change.

Applying this to the first failed return gives:

### Odd corridor length

If `G` is odd, then the final fringe has one leading zero, so

    a=0,b=1,

and therefore

    A^p(w)=w XOR 1.

### Even corridor length

If `G` is even, then the final fringe reaches the copy boundary, so `a=1`. Hence

    A^p(w)=w XOR 1    if u is odd,
    A^p(w)=w XOR 3    if u is even.

Thus the first failure after an arbitrarily long physical `A^p`-persistence block is never arbitrary. It is always exactly a one-bit or two-bit low-end defect with mask `1` or `3`.

## Checked examples

Canonical `z=25,p=2,R=1,G=3`:

    w=T^2(25)=401,
    A^2(401)=400=401 XOR 1.

Canonical `z=50,p=2,R=2,G=2`:

    u=T(50)=222 even,
    w=T(u)=802,
    A^2(802)=801=802 XOR 3.

Run-17 re-entry example `z=28519,p=4,R=23,G=3`:

    w=T^2(z)=455503,
    A^4(w)=455502=w XOR 1.

## Why this matters

The end of a long neutral plateau now reduces to two exact local defect types:

    mask 1
    mask 3

rather than uncontrolled loss of `A^p` periodicity.

This creates a direct interface with the repository's pushed one-bit/two-bit source and return machinery.

## Preferred next target

Take these two exact masks through the existing source classifier / return results.

The useful question is no longer "what happens when the long physical periodic block ends?" but:

> For a common-origin physical row satisfying
>
>     A^p(w)=w XOR 1
>
> or
>
>     A^p(w)=w XOR 3,
>
> what compulsory later event follows, and can it be charged without falling back into the already-fenced residence-ledger telescope?

Promising routes:

1. identify these masks with existing one-bit or two-bit reset/nonreset source phases;
2. determine whether the period monotonicity theorem forces a period change after either mask;
3. track the boundary defect through one full `p`-block to see whether the same defect can recur indefinitely without consuming new physical fringe.

Do not infer positive residence charge from the defect alone; earlier local birth/source episodes can telescope to zero or negative ledger charge.
