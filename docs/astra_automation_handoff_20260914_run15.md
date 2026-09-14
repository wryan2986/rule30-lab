# Astra automation handoff — run 15

Problem 1 remains **OPEN**. Continue on `research/astra-next`.

## New result this run

Read:

- `proofs/informal/problem1_period_neutral_zero_lifts_return_fringe.md`

Let `z>0` be `A`-periodic with exact period `p`. Since

    A^p(z)=sigma^(2p)T^p(z)=z,

there is a unique nonzero return fringe

    R=R_p(z)

with

    T^p(z)=2^(2p)z+R,
    1 <= R < 2^(2p).

Let

    L=bit_length(R).

For every `0<=q<=2p`, exact renormalization gives

    A^p(2^q z)
      = 2^q z + floor(R / 2^(2p-q)).

Therefore `2^q z` has exact period `p` iff

    q <= 2p-L.

So the entire period-neutral zero-lift prefix is classified exactly: its number of neutral lift steps is

    2p-L.

A long neutral run is precisely a large leading-zero gap in the `2p`-cell return fringe discarded during one `A`-cycle.

## First non-neutral phase is exact

Set

    q_* = 2p-L+1.

Because the top bit of `R` is at position `L-1`,

    A^p(2^(q_*)z)=2^(q_*)z+1.

Thus the first failure of period neutrality is an exact adjacent `+1` phase defect, not an arbitrary phase.

By the existing one-bit period theorem, the first non-neutral zero lift is either:

1. nonperiodic immediately; or
2. periodic with exact period `2p`.

In the doubling case, `problem1_period_doubling_forces_next_exit.md` forces the following zero lift to be nonperiodic.

Hence if `Q` is the first nonperiodic zero-extension depth,

    Q in {2p-L+1, 2p-L+2}.

The second value occurs exactly when the first non-neutral lift doubles the period.

This strictly refines the prior bound `Q<=2p+1`.

## Valuation refinement

If `a=v_2(z)`, then `T` preserves valuation while `2^(2p)z` has valuation `a+2p`, so

    v_2(R)=a.

Hence

    L>=a+1,

and therefore

    Q<=2p-a+1,

or `Q<=2p-a` in the no-doubling branch.

For physical origins `z=T^H(v)`, `a=v_2(v)` is invariant across restarts.

## Canonical sharp example

For `z=25`, `p=2`:

    T^2(25)=401=16*25+1,

so `R=1`, `L=1`. Therefore neutral depths are exactly `q=0,1,2,3`, giving

    25,50,100,200

of exact period 2. At `q_*=4`,

    A^2(400)=401=400+1,

and `400` doubles to period 4. The following zero lift `800` is nonperiodic, so

    Q=5=2p-L+2.

## New preferred target

The local classification of period-neutral skips is now complete. Do not spend another run reclassifying neutral zero lifts.

The next useful all-depth target is the return fringe itself. For periodic physical rows

    z=T^H(v),

try to prove one of:

1. a lower bound on `L=bit_length(R_p(z))` strong enough to prevent repeatedly long negative plateaus;
2. a theorem that a small `L` (large leading-zero gap in `R`) forces later residence surplus or period growth that repays the associated skips;
3. a direct FULL/global-front interpretation of the return fringe `R` that lets finite-support causality constrain its leading-zero gap.

The important structural translation is:

    long period-neutral plateau
      <=>
    p-step return fringe has a long leading-zero gap.

This is now the narrowest unresolved obstruction connecting the persistent period potential to the residence ledger.