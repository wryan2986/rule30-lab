# Astra automation handoff — run 17

Problem 1 remains **OPEN**. Continue on `research/astra-next`.

## New result this run

Read:

- `proofs/informal/problem1_return_fringe_physical_periodic_persistence.md`

Let `z>0` satisfy

    A^p(z)=z

and write its `p`-return fringe as

    T^p(z)=2^(2p) z+R,
    0<R<2^(2p).

Put

    L=bit_length(R),
    G=2p-L.

Run 15 proved that `G` is exactly the number of period-neutral literal zero-lift steps. Run 16 identified the same `G` as a literal zero corridor in a later physical row.

The new theorem gives a second exact interpretation:

    D=floor(G/2)

is exactly the number of consecutive future physical Rule-30 steps after `z` for which the same `p`-step normalized return remains valid.

More precisely,

    A^p(T^d z)=T^d z    for 0<=d<=D,

while

    A^p(T^(D+1) z) != T^(D+1) z.

So

    z, Tz, ..., T^D z

are all fixed by `A^p`, and the next physical row is not.

## One-step criterion

The key exact criterion is

    A^p(Tz)=Tz
      iff
    the top two bits of R are zero
      iff
    G>=2.

When `G>=2`, the new return fringe is exactly

    R_p(Tz)=T(R),

and because every nonzero finite word gains exactly two bits under `T`, its corridor length becomes

    G-2.

Iteration proves the theorem above.

The mechanism is simple but nonlinear-safe: if `m=2p` and `r<2^(m-2)`, then the two zero cells between `r` and a block shifted by `m` prevent Rule 30 from coupling the blocks for one step, giving the exact identity

    T(2^m u+r)=2^m T(u)+T(r).

Necessity follows from bit `m`: if either of the two top fringe bits is `1`, bit `m` of the next physical row's `p`-return is flipped, so the quotient cannot equal `Tz`.

## Examples

For the canonical state

    z=25, p=2, R=1,

we have

    G=3, D=1.

Thus `25` and `111=T(25)` are fixed by `A^2`, while `401=T^2(25)` is not fixed by `A^2` (it has exact period `4`).

For

    z=50, p=2, R=2,

we have `G=2,D=1`; `50` and `222` are fixed by `A^2`, while `802` is not.

## Important limitation / dead end fenced

Do **not** infer permanent loss of the `A^p` return after the consecutive block ends.

Exact computation gives

    z=28519, p=4, R=23, G=3.

Then `z` and `Tz` are fixed by `A^4`, `T^2 z` is not, but `T^3 z` is fixed by `A^4` again.

So the theorem controls only the initial consecutive physical persistence block.

Also do not argue that a long zero corridor should cause immediate physical nonperiodicity. The exact theorem says the opposite: every two corridor cells force one additional physical step preserving the same `A^p` return.

## Preferred next target

The obstruction is now equivalently a physical-time one:

> Can FULL/common-origin structure forbid arbitrarily long consecutive blocks
>
>     T^H(v), T^(H+1)(v), ..., T^(H+D)(v)
>
> all fixed by one `A^p`?

Since `D=floor(G/2)` exactly, a long neutral tower plateau forces a proportionally long physical periodic-persistence block.

Useful next routes:

1. search the existing FULL/global-front results for a bound on consecutive physical rows satisfying `A^p(T^(H+d)v)=T^(H+d)v`;
2. derive the spacetime geometry of such a block directly from

       T^(H+d+p)(v)=2^(2p)T^(H+d)(v)+T^d(R)

   for `0<=d<=D`;
3. analyze the forced event at `d=D+1`, where the top one or two fringe bits first reach the copy boundary, and determine whether the resulting boundary interaction forces period growth or residence surplus.

The most concrete new bridge is:

    G neutral zero-lift skips
      <=> G-cell return-fringe corridor
      <=> floor(G/2) consecutive physical A^p returns.
