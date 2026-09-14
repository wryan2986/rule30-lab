# Astra automation handoff — run 14

Problem 1 remains **OPEN**. Continue on `research/astra-next`.

## New result this run

Read:

- `proofs/informal/problem1_global_eventual_period_monotonicity.md`

For the full zero-extension tower

    y_n=2^n v,
    h_n=tau(y_n),

let `p_n` be the exact period of the eventual `A`-cycle reached by `y_n`.

The one-bit factor relation gives the global theorem

    p_(n+1) in {p_n,2p_n}.

Moreover, if

    delta_n=h_(n+1)-h_n > 0,

then the same-height one-bit lift is nonperiodic, so the base cycle must contain an eraser and the lift eventually joins the unique recurrent phase of exact base period. Hence

    delta_n>0  =>  p_(n+1)=p_n.

Equivalently,

    p_(n+1)=2p_n  =>  delta_n=0.

Thus eventual cycle period is a persistent global power-of-two potential. It can increase only at skips and can never decrease at a later plateau exit.

If `D(N)` counts period-doubling tower steps before `N`, then exactly

    p_N=p_0*2^D(N).

## Exact inter-plateau bridge

For a post-threshold plateau with origin

    u=T^H(v),

suppose `2^q u` is periodic for `0<=q<Q`, while

    d=tau(2^Q u)>0.

Set

    H'=H+d,
    n'=2H+Q,
    k=2d-Q.

The causal exit bound implies `k>=1`. Exact renormalization gives

    A^d(2^Q u)=sigma^k T^d(u),

and

    2H'-n'=k.

Therefore the plateau exit lands exactly `k` positions before the next common-origin threshold, with periodic stripped core equal to the `k`-bit projection of the next physical row. Since the exit is a rise, its eventual period is exactly the terminal parent's period. Any subsequent periodic lifts before the next threshold can only preserve or double it.

So the terminal period of one plateau is transported without loss into the next plateau's entry core. Do not treat period as a local quantity that resets between plateaus.

## Relation to prior forced-exit theorem

The prior note `problem1_period_doubling_forces_next_exit.md` remains valid and becomes more useful:

- globally, doubling can occur only on a skip and permanently raises `p_n`;
- in a literal post-threshold zero-extension run, a doubling zero lift forces the following zero lift to be nonperiodic;
- the subsequent rise preserves the doubled eventual period.

So a post-threshold doubling is a terminal skip for that plateau, but its period increase survives the exit.

## Next target

The strongest remaining target is to couple the persistent period potential to the residence ledger.

Two concrete routes:

1. Under the contrary hypothesis that `e_v(n)=h_n-n` is eventually bounded above, prove that infinitely many doubling skips are required, then use FULL/common-origin structure to obstruct infinitely many persistent doublings.
2. Prove that sufficiently large `p_n` forces later positive residence surplus large enough to repay the skips needed to create it.

A narrower local subproblem is to classify **period-neutral** skips in the literal post-threshold zero-extension regime. Doubling skips there are already terminal by the previous theorem; any long negative plateau must therefore consist mostly of period-neutral zero lifts.

Do not return to generic nested-lift compensation or additive birth counting; both routes are already fenced by prior notes.