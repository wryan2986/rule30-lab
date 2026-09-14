# Problem 1: the first return-fringe boundary collision creates only a two-bit normalized defect

## Status

Problem 1 remains open. This note sharpens the end of the consecutive physical `A^p`-persistence block proved in `problem1_return_fringe_physical_periodic_persistence.md`.

Let

    A^p(z)=z,
    T^p(z)=2^(2p) z + R,
    0<R<2^(2p).

Put

    m=2p,
    L=bit_length(R),
    G=m-L,
    D=floor(G/2).

The previous theorem proves

    A^p(T^d z)=T^d z    for 0<=d<=D,

and failure at the next physical row

    w=T^(D+1) z.

The new result is that this first failure is extremely small: `A^p(w)` differs from `w` only in its bottom two bits, with an exact parity-dependent formula.

## 1. Exact boundary-collision quotient

Consider arbitrary integers `u>=0`, `0<=r<2^m`, and write the top two fringe bits

    a=bit_(m-1)(r),
    b=bit_(m-2)(r).

For

    x=2^m u+r,

all output bits of `T(x)` at positions `m+2,m+3,...` depend only on the shifted copy `u`, so after dividing by `2^m` they agree exactly with bits `2,3,...` of `T(u)`.

The only possible discrepancy lies in quotient bits `0,1`.

Using

    bit_k(Tx)=x_k XOR (x_(k-1) OR x_(k-2)),

we get at the copy boundary

    bit_m(Tx)=u_0 XOR (a OR b),

whereas

    bit_0(Tu)=u_0.

Thus quotient bit `0` is flipped iff

    a OR b = 1.

Likewise

    bit_(m+1)(Tx)=u_1 XOR (u_0 OR a),

while

    bit_1(Tu)=u_1 XOR u_0.

Hence quotient bit `1` is flipped iff

    a=1 and u_0=0.

Therefore

> **Boundary quotient formula.** For every `u,r` as above,
>
>     floor(T(2^m u+r)/2^m)
>       = T(u) XOR eps,
>
> where
>
>     eps = (a OR b) + 2*(a AND (1-u_0)).
>
> In particular `eps` is always one of `0,1,3`.

This is exact. No carries occur because the statement is about output bits themselves.

## 2. Apply at the first failed physical return

At physical time `D`, the previous persistence theorem gives

    T^p(T^D z)=2^m T^D z + T^D(R).

Set

    u=T^D z,
    r=T^D(R).

Its remaining zero-corridor length is

    G_D=G-2D,

so

    G_D in {0,1}.

The next physical row is

    w=T(u)=T^(D+1) z,

and

    A^p(w)
      = floor(T(2^m u+r)/2^m).

### Odd `G`

If `G` is odd, then `G_D=1`. Thus

    a=0,
    b=1.

The boundary formula gives

    eps=1,

hence the exact near-return

>     A^p(w)=w XOR 1.                              (1)

So the first failed return differs from the physical row in exactly its least-significant bit.

### Even `G`

If `G` is even, then `G_D=0`. Thus

    a=1.

Therefore quotient bit `0` always flips, while bit `1` flips exactly when `u` is even:

>     A^p(w)=w XOR 1,   if u is odd,               (2)
>
>     A^p(w)=w XOR 3,   if u is even.              (3)

Equivalently, at the first failure the normalized `p`-return defect is always supported in the two-bit set `{0,1}` and is exactly one of the masks `1` or `3`.

## 3. Examples

### `z=25`, `p=2`

Here `R=1`, `G=3`, so `D=1` and `G` is odd. The first failed row is

    w=T^2(25)=401.

Exactly as (1) predicts,

    A^2(401)=400=401 XOR 1.

### `z=50`, `p=2`

Here `R=2`, `G=2`, so `D=1` and `u=T(50)=222` is even. The first failed row is

    w=T(222)=802.

Exactly as (3) predicts,

    A^2(802)=801=802 XOR 3.

### Re-entry example `z=28519`, `p=4`

The earlier example has `R=23`, `G=3`, so the first failure is again odd-corridor type. With

    w=T^2(z)=455503,

we obtain

    A^4(w)=455502=w XOR 1.

This is consistent with the later re-entry of `T^3 z` into the `A^4`-fixed set: the theorem here describes only the exact defect at first collision, not permanent escape.

## 4. Research consequence

A long neutral plateau no longer ends in an uncontrolled loss of periodic return. Its endpoint has a rigid local form:

    long return-fringe corridor
      -> long physical A^p-persistence block
      -> first collision produces only a 1-bit or 2-bit normalized defect.

This interfaces directly with the existing one-bit and two-bit source/lift machinery. In particular, any future attempt to extract compensation at the end of a long corridor need only analyze the two exact defect masks

    1 and 3,

rather than arbitrary states.

The parity split is also exact:

- odd corridor length forces the one-bit mask `1`;
- even corridor length forces mask `1` or `3` according only to the parity of the final persistent physical row `u=T^D z`.

This is a concrete reduction of the remaining boundary event.

## 5. What this does not prove

The near-return alone does not imply positive residence surplus. Earlier repository results show that local one-bit/two-bit events can telescope away in the signed residence ledger. Therefore the masks `1` and `3` must be coupled to the common-origin/full-spacetime structure before claiming compensation.

The next useful target is to transport these exact boundary defects through the existing one-bit/two-bit return classifier and determine whether repeated long corridors force either:

1. period growth that persists globally,
2. a bounded-reuse birth/front event, or
3. a later residence increment whose charge cannot telescope against the same corridor.
