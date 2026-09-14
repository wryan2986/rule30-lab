# Astra automation handoff — run 16

Problem 1 remains **OPEN**. Continue on `research/astra-next`.

## New result this run

Read:

- `proofs/informal/problem1_return_fringe_physical_prefix_and_triangular_inverse.md`

The return fringe from the previous run now has an exact common-origin interpretation.

For normalized packed Rule 30,

    T(x)=x XOR ((2x) OR (4x)).

Hence output bit `k` is

    y_k=x_k XOR (x_(k-1) OR x_(k-2)).

So for every `m`, the induced map

    T_m(x)=T(x) mod 2^m

is triangular and bijective. The inverse is recovered low-bit first:

    x_0=y_0,
    x_1=y_1 XOR x_0,
    x_k=y_k XOR (x_(k-1) OR x_(k-2)).

Thus low prefixes evolve autonomously and reversibly.

## Physical-prefix theorem

Let a physical row

    z=T^H(v)

be `A`-periodic of exact period `p`, and write

    T^p(z)=2^(2p)z+R,
    0<R<2^(2p).

Then exactly

    R = T^(H+p)(v) mod 2^(2p).

So the return fringe is simply the low `2p`-bit prefix of one later row in the SAME original physical Rule-30 orbit.

If

    L=bit_length(R),
    G=2p-L,

then the period-neutral plateau length `G` from run 15 is literally the zero corridor

    bits L,...,2p-1 = 0

in the physical row `T^(H+p)(v)`, with bit `L-1=1`; the bits from `2p` upward reproduce `T^H(v)`.

Thus the return row has the exact form

    [ regenerated copy of T^H(v) ][ G zeros ][ nonzero fringe ].

## Inverse-prefix constraint

Because `T_(2p)` is a permutation,

    v mod 2^(2p)
      = T_(2p)^(-(H+p))(R).

Therefore `(H,p,R)` uniquely determines the first `2p` bits of the fixed original seed.

If only `R<2^L` is assumed, then the allowed seed prefixes form

    S_(H,p,L)
      = {T_(2p)^(-(H+p))(r): 0<r<2^L},

with exact cardinality

    |S_(H,p,L)|=2^L-1.

For corridor length `G=2p-L`, this is a fraction `<2^(-G)` of all `2p`-bit prefixes. This is only a counting fact; do NOT use it probabilistically.

The significance is that every long negative plateau now imposes an explicit reversible congruence constraint on the SAME seed `v`.

## What this closes / does not close

Do not treat `R` as an auxiliary cycle-only object anymore. It is an actual physical-row prefix.

Do not infer a local lower bound on `L` from triangular invertibility alone. The known exact example

    z=25, p=2, R=1, L=1, G=3

already realizes an almost-maximal corridor.

Problem 1 is still open because a fixed seed could, in principle, lie in many sparse inverse-prefix constraint sets.

## Preferred next target

The best next route is to couple multiple long-corridor constraints arising from successive physical origins. In particular, try one of:

1. pull the zero corridor backward through the explicit triangular inverse and prove that sufficiently long corridors force a deterministic pattern incompatible with FULL/common-origin structure;
2. compare `S_(H,p,L)` for successive plateau origins and show that repeated large `G` is incompatible unless later residence/period growth repays the skipped depth;
3. connect the literal zero corridor in `T^(H+p)(v)` directly to the global discrepancy front and extract a quantitative residence cost.

The main new bridge is:

    long neutral plateau
      <=> long zero corridor in an actual physical row
      <=> sparse exact inverse-prefix constraint on the original seed.