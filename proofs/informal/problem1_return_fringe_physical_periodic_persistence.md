# Problem 1: return-fringe corridor exactly controls consecutive physical `A^p` persistence

## Status

Problem 1 remains open. This note strengthens the physical-prefix interpretation of the return fringe.

Let `z>0` satisfy

    A^p(z)=z,

where

    T(x)=x XOR ((2x) OR (4x)),
    A(x)=T(x)>>2.

Write

    T^p(z)=2^(2p) z + R,
    0<R<2^(2p),

and let

    L=bit_length(R),
    G=2p-L.

The previous return-fringe note proved that `G` is exactly the number of period-neutral zero-lift steps over `z`, and the physical-prefix note identified the same `G` as a literal zero corridor in one later physical row.

The new result here is a second exact interpretation:

> `floor(G/2)` is exactly the number of consecutive physical Rule-30 steps after `z` for which the same `p`-step normalized return `A^p(w)=w` continues to hold.

Thus every two cells of return-fringe corridor buy exactly one step of physical-time persistence of the same `A^p` return.

This does not solve Problem 1, but it couples the previously separate zero-extension and physical-time pictures by an exact finite theorem.

## 1. A separated-block identity

Put

    m=2p.

Suppose `u,r>=0` and

    r < 2^(m-2).

Then the binary support of `r` lies below position `m-2`, while the support of `2^m u` begins at position at least `m`. There are therefore two zero cells immediately below the shifted block.

Because one Rule-30 output bit depends only on the current bit and the two lower bits,

    y_k = x_k XOR (x_(k-1) OR x_(k-2)),

those two blocks evolve independently for one step:

    T(2^m u+r)=2^m T(u)+T(r).                         (1)

This is an exact integer identity; no linearity of `T` is being assumed. The two-cell gap is what prevents the nonlinear OR term from coupling the blocks.

Also, for every nonzero finite `r`,

    bit_length(T(r))=bit_length(r)+2,                 (2)

because the top bit of `4r` is strictly above every bit of `r` and `2r` and therefore survives in `T(r)`.

## 2. One-step criterion

Assume

    A^p(z)=z,
    T^p(z)=2^m z+R,
    0<R<2^m.

Then

    T^p(Tz)=T(T^p z)=T(2^m z+R).                     (3)

We claim

    A^p(Tz)=Tz

if and only if the top two bits of the `m`-bit fringe `R` are zero, equivalently

    R<2^(m-2),                                       (4)

or equivalently

    G>=2.                                            (5)

### Sufficiency

If `R<2^(m-2)`, apply (1):

    T(2^m z+R)=2^m T(z)+T(R).

By (2), `T(R)<2^m`. Hence

    T^p(Tz)=2^m Tz+T(R),

so shifting right by `m=2p` gives

    A^p(Tz)=Tz.                                      (6)

The new `p`-return fringe is exactly

    R_p(Tz)=T(R).                                    (7)

### Necessity

Let `r_j=bit_j(R)`. In the concatenated word

    2^m z+R,

bit `m` equals `z_0`, while bits `m-1,m-2` equal `r_(m-1),r_(m-2)`.

Therefore bit `m` of its Rule-30 image is

    z_0 XOR (r_(m-1) OR r_(m-2)).                    (8)

If `A^p(Tz)=Tz`, then the quotient of `T^p(Tz)` above the low `m` bits must be exactly `Tz`. Its bottom quotient bit must therefore equal

    bit_0(Tz)=z_0.                                   (9)

Comparing (8) and (9) forces

    r_(m-1)=r_(m-2)=0.                               (10)

Thus (4) is necessary.

We have proved:

> **One-step physical-persistence criterion.** For an `A^p`-fixed state `z`, the next physical row `Tz` is also `A^p`-fixed iff the `p`-return fringe of `z` has at least two leading zero cells.

When this holds, the fringe advances by one physical step exactly as `R -> T(R)`.

## 3. Exact consecutive persistence length

Return to

    L=bit_length(R),
    G=m-L.

Set

    D=floor(G/2).                                    (11)

For every `0<=d<=D`, we claim

    A^p(T^d z)=T^d z,                                (12)

and its `p`-return fringe is

    R_d=T^d(R).                                      (13)

Moreover

    bit_length(R_d)=L+2d,                            (14)

so its remaining corridor length is exactly

    G_d=G-2d.                                        (15)

Proof is by induction. At `d=0` this is the definition of `R`. If `d<D`, then

    G-2d >= 2,

so the one-step criterion applies to `T^d z`, giving (12)-(13) at `d+1`. Equation (14) follows from repeated use of (2).

At `d=D`, the remaining corridor has length

    G_D in {0,1}.                                    (16)

Therefore the one-step criterion fails, and necessarily

    A^p(T^(D+1) z) != T^(D+1) z.                    (17)

Hence:

> **Exact physical-persistence theorem.** If an `A^p`-fixed state has return-fringe corridor length `G`, then
>
>     z, Tz, ..., T^floor(G/2) z
>
> are all fixed by `A^p`, while
>
>     T^(floor(G/2)+1) z
>
> is not fixed by `A^p`.

Equivalently, the number of consecutive *future physical steps* preserving the same `p`-return is exactly

    floor(G/2).                                      (18)

The theorem concerns fixation by `A^p`; it does not assert that `p` remains the exact least period at every intermediate row, although all checked examples retain the same exact period during this guaranteed block. No least-period claim is needed here.

## 4. Relation to the neutral zero-lift theorem

The preceding return-fringe classification gave

    G=2p-L

as exactly the number of period-neutral **zero-lift** steps after `z`.

The present theorem gives simultaneously

    floor(G/2)

as exactly the number of consecutive **physical-time** steps after `z` preserving the same `A^p` return.

Thus the same finite fringe controls two different directions:

    G neutral tower lifts
      <=> G leading zero cells in the return fringe
      => floor(G/2) consecutive physical `A^p` returns,

and the final implication is exact in the sense that the next physical step necessarily loses the `A^p` fixed-point property.

This is a stronger common-origin constraint than the earlier statement that the fringe is merely a prefix of a physical row.

## 5. Exact examples

### `z=25`, `p=2`

The established example has

    T^2(25)=16*25+1,
    R=1,
    L=1,
    G=3,
    D=1.

Therefore the theorem predicts

    25 and T(25)=111

are fixed by `A^2`, while

    T^2(25)=401

is not fixed by `A^2`. Indeed `401` lies on an `A`-cycle of exact period `4` instead.

### `z=50`, `p=2`

Here

    R=2,
    L=2,
    G=2,
    D=1.

Thus `50` and `222=T(50)` are fixed by `A^2`, while

    802=T^2(50)

is not.

### Re-entry warning

Loss of the `A^p` return at the end of the guaranteed consecutive block is not permanent. For example, exact computation gives a period-four state

    z=28519,
    R_4(z)=23,
    G=3.

The theorem guarantees `z` and `Tz` are fixed by `A^4`, while `T^2 z` is not. Nevertheless `T^3 z` is again fixed by `A^4`.

So the theorem controls the **initial consecutive physical run**, not all later physical returns. Any future argument must not promote (17) to permanent exclusion.

## 6. Research consequence

A long period-neutral plateau is now known to force a long block of actual physical rows carrying the same normalized `p`-return. This rules out a tempting but false style of compensation argument in which a long return-fringe corridor is expected to cause immediate physical nonperiodicity or immediate residence growth.

Instead, long corridor means temporary physical periodic persistence:

    corridor length G
      -> floor(G/2) consecutive physical rows fixed by A^p.

This gives a sharper next target for the FULL/global-front machinery:

> Can one bound the length of a consecutive physical block
>
>     T^H(v), T^(H+1)(v), ..., T^(H+D)(v)
>
> all fixed by the same `A^p`, when they arise from one finite FULL/common-origin Rule-30 spacetime?

Any bound `D=o(G)` is impossible because `D=floor(G/2)` identically. What is needed is either:

1. an all-depth obstruction to arbitrarily long consecutive physical `A^p` blocks;
2. a quantitative event forced when such a block ends; or
3. a coupling theorem showing that repeated long blocks cannot occur without later residence surplus or period growth.

The return fringe now supplies an exact conversion factor between the tower obstruction and this physical-time obstruction: two corridor cells per guaranteed physical periodic step.
