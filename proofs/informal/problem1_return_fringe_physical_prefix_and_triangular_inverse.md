# Problem 1: return fringe is an exact physical-row prefix, with triangular inverse

## Status

Problem 1 remains open. This note gives a common-origin interpretation of the return fringe introduced in `problem1_period_neutral_zero_lifts_return_fringe.md`.

The main point is that for a periodic physical-row origin `z=T^H(v)`, the abstract return fringe

    R_p(z)=T^p(z)-2^(2p)z

is exactly the low `2p` bits of one later row in the ORIGINAL physical orbit:

    R_p(T^H(v)) = T^(H+p)(v) mod 2^(2p).

Thus a long period-neutral zero-lift plateau is literally a long zero corridor in a fixed Rule-30 spacetime row, not merely a property of an auxiliary periodic lift.

A second exact fact is that normalized Rule 30 is triangular and invertible modulo every power of two. Hence the return fringe determines the entire low `2p`-bit prefix of the original seed `v` once `(H,p)` are fixed.

These facts do not yet prove the required lower bound on fringe length, but they sharply localize the remaining obstruction and give a finite-prefix inverse formulation for future FULL/global-front arguments.

## 1. Packed normalized Rule 30 is triangular

For the packed finite-row convention used throughout these notes, the normalized Rule-30 map is

    T(x) = x XOR ((2x) OR (4x)).                       (1)

Equivalently, if `x_k` and `y_k` are bits of `x` and `y=T(x)`, with `x_j=0` for `j<0`, then

    y_k = x_k XOR (x_(k-1) OR x_(k-2)).                (2)

Therefore bit `k` of `T(x)` depends only on bits `0,...,k` of `x`.

For every `m>=1`, define

    T_m(x) = T(x) mod 2^m,

on `m`-bit words. Equation (2) makes `T_m` triangular. It is in fact a permutation: recover the input bits recursively by

    x_0 = y_0,
    x_1 = y_1 XOR x_0,
    x_k = y_k XOR (x_(k-1) OR x_(k-2))    (k>=2).      (3)

Thus:

> **Triangular-prefix lemma.** For every `m`, `T_m` is bijective, and for every `t>=0`,
>
>     T^t(x) mod 2^m = T_m^t(x mod 2^m).               (4)
>
> In particular, every finite low-bit prefix evolves autonomously and reversibly.

This is stronger than the previously used homogeneity `T(2^q x)=2^qT(x)`: it says low prefixes never depend on higher bits and lose no information under physical time.

## 2. Return fringe equals a physical-row prefix

Let

    z = T^H(v)

be a physical Rule-30 row that is periodic under `A=sigma^2 T` with exact period `p`.

By the return-fringe definition,

    T^p(z)=2^(2p) z + R,
    0<R<2^(2p).                                       (5)

But `z=T^H(v)`, so the left side is simply

    T^(H+p)(v).

Reducing (5) modulo `2^(2p)` gives the exact common-origin identity

    R = T^(H+p)(v) mod 2^(2p).                        (6)

Hence:

> **Physical-prefix theorem.** The `p`-step return fringe of a periodic physical origin `T^H(v)` is exactly the first `2p` bits of the later physical row `T^(H+p)(v)`.

No auxiliary lifted orbit remains in (6).

## 3. Long neutral plateau = explicit zero corridor

Let

    L = bit_length(R),
    G = 2p-L.

The preceding return-fringe classification proves that `G` is exactly the number of period-neutral zero-lift steps after `z`.

Equation (6) gives a direct spacetime interpretation. Since `R` has top bit `L-1`, the physical row at time `H+p` satisfies

    bit_(L-1)(T^(H+p)(v)) = 1,

and

    bit_j(T^(H+p)(v)) = 0
    for L <= j <= 2p-1.                               (7)

Meanwhile (5) says the bits from position `2p` upward reproduce `z` exactly:

    floor(T^(H+p)(v)/2^(2p)) = T^H(v).                (8)

Thus the return row has the literal form

    [ regenerated copy of T^H(v) ][ G zero cells ][ nonzero fringe ].

In integer notation this is simply (5), but (7) identifies the previously abstract leading-zero gap with an actual zero corridor of length `G` in one fixed physical row.

If `a=v_2(v)`, then the earlier valuation argument gives `v_2(R)=a`. Thus the nonzero fringe itself begins at bit `a`, while its last `1` is at bit `L-1`.

The narrow unresolved question can therefore be restated without tower terminology:

> Along periodic physical origins `T^H(v)`, can the exact self-return
>
>     T^(H+p)(v)=2^(2p)T^H(v)+R
>
> repeatedly contain zero corridors `L,...,2p-1` whose lengths `G=2p-L` are large enough to keep the residence excess bounded above?

This is the direct target for finite-support causality and FULL/global-front structure.

## 4. Exact inverse-prefix constraint on the fixed seed

Using the triangular-prefix lemma with `m=2p`, equation (6) becomes

    T_(2p)^(H+p)(v mod 2^(2p)) = R.                   (9)

Since `T_(2p)` is a permutation,

    v mod 2^(2p)
      = T_(2p)^(-(H+p))(R).                           (10)

Therefore `(H,p,R)` uniquely determines the first `2p` bits of the original fixed seed.

If only the fringe-length bound `R<2^L` is known, then (10) places the seed prefix in the explicit set

    S_(H,p,L)
      = { T_(2p)^(-(H+p))(r) : 0<r<2^L }.             (11)

Because `T_(2p)` is bijective,

    |S_(H,p,L)| = 2^L-1.                              (12)

Among all `2^(2p)` prefixes, the exact fraction allowed by a corridor of length at least `G=2p-L` is therefore

    (2^L-1)/2^(2p) < 2^(-G).                          (13)

This is only a counting statement, not a proof that the fixed seed cannot lie in infinitely many such sets. It should not be converted into a probabilistic argument. Its value is structural: every unusually long neutral plateau imposes an explicit, reversible congruence constraint on the SAME original seed prefix.

This creates a possible all-depth route that was absent from the local plateau analysis: compare the sets (11) for successive periodic physical origins and prove that the common-origin/FULL constraints make sufficiently strong long-corridor requirements incompatible.

## 5. Why invertibility alone does not solve the problem

Triangular invertibility by itself supplies no lower bound on `L`.

The already established exact example

    z=25, p=2,
    T^2(25)=401=16*25+1

has

    R=1,
    L=1,
    G=3.

So a physical periodic state can realize an almost-maximal zero corridor. The new result is therefore not a disguised local compensation theorem.

Likewise, the cardinality estimate (13) cannot be used as a randomness heuristic. A fixed finite seed may belong to very sparse explicitly defined congruence classes.

The missing theorem must couple multiple `(H,p)` constraints or use additional geometry of the actual Rule-30 spacetime.

## 6. Preferred next step

Do not reclassify literal zero lifts; that part is complete.

The useful next target is now one of the following equivalent common-origin statements:

1. show that the zero corridor (7) forces a FULL/global-front event with a quantitative residence cost;
2. show that two or more long-corridor inverse-prefix constraints (11), arising at successive physical origins of one tower, are incompatible unless the later period/preperiod gains enough to repay the skipped depth;
3. exploit the triangular inverse (3) to pull the corridor backward through `H+p` physical steps and identify a deterministic forbidden pattern in the fixed finite seed or in an earlier FULL row.

The important reduction is that `R` is no longer an abstract fringe variable: it is an exact prefix of `T^(H+p)(v)` and an exact invertible image of `v mod 2^(2p)`.