# Problem 1: eventual cycle period is a global monotone tower invariant

## Status

Problem 1 remains open. This note globalizes the period information from the post-threshold zero-extension analysis. The exact eventual `A`-cycle period of `2^n v` cannot reset when one plateau exits and another begins: along the whole zero-extension tower it can only stay fixed or double. Moreover, every genuine rise of the preperiod preserves the eventual period exactly; period doubling is possible only at a skip.

This supplies the inter-plateau memory that was missing from the previous run.

## Setup

Let

    T(x) = x XOR ((x << 1) OR (x << 2)),
    A(x) = T(x) >> 2.

Fix nonzero finite `v`, and define

    y_n = 2^n v,
    h_n = tau(y_n).

Let `p_n` denote the exact period of the eventual `A`-cycle reached by `y_n`.

The established monotonicity of the zero-extension preperiod gives

    h_(n+1) >= h_n.

Put

    delta_n = h_(n+1)-h_n >= 0.

At time `H=h_n`, define

    z = A^H(y_n).

Then `z` is periodic of exact period `p_n`.

Because one-bit projection is a factor of `A`, the state

    w = A^H(y_(n+1))

is a one-bit lift of `z`: there is `a_0 in {0,1}` such that

    w = 2z+a_0,

and along the orbit

    A^s(w)=2A^s(z)+a_s.

The lift bit obeys the established recurrence

    a_(s+1)=c_s XOR (b_s OR a_s),

where

    b_s=bit_0(A^s(z)),
    c_s=bit_1(A^s(z)).

## Theorem 1: global eventual periods satisfy p_(n+1) in {p_n,2p_n}

Consider the return map on the lift bit after one exact base period `p_n`.

If the base cycle contains an eraser (`b_s=1` somewhere), the return map is constant. There is one recurrent lift phase, and its lifted cycle has exact period `p_n`. Every other lift phase is transient and eventually joins that recurrent lift. Hence every lift of this base has eventual period exactly `p_n`.

If the base cycle has `b_s=0` everywhere, the return map is

    a |-> a XOR C,

with

    C = XOR_(s=0..p_n-1) c_s.

If `C=0`, both lift phases are periodic of exact period `p_n`. If `C=1`, both lift phases lie on a two-cycle of the return map, so the lifted orbit has exact period `2p_n`.

Therefore in all cases

    p_(n+1) in {p_n, 2p_n}.

In particular, the eventual period never decreases anywhere in the full zero-extension tower.

## Theorem 2: every rise preserves period exactly

Suppose

    delta_n > 0.

Then `w=A^(h_n)(y_(n+1))` is not periodic; otherwise `h_(n+1)<=h_n`, contradicting the strict rise.

A nonperiodic one-bit lift of a periodic base is possible only in the eraser case. In that case the one-bit classifier says the lift has a finite transient and then joins the unique recurrent lift, whose exact period is the base period `p_n`.

Hence

    delta_n>0  implies  p_(n+1)=p_n.

Equivalently,

    p_(n+1)=2p_n  implies  delta_n=0.

Thus every period doubling is attached to a tower skip, never to a positive residence increment.

## Corollary: a persistent power-of-two period potential

Let `D(N)` be the number of indices `0<=n<N` at which

    p_(n+1)=2p_n.

Then exactly

    p_N = p_0 * 2^D(N).

This quantity is global: rises, plateau exits, physical-time restarts, and later plateaus cannot erase earlier doublings.

This is stronger than the previous post-threshold statement, which tracked period only while a literal periodic zero-extension prefix remained periodic.

## Relation to the residence ledger

Recall

    e_v(N)=tau(v)+P_v(N)-Z_v(N),

where a skip `delta_n=0` contributes `-1` to the signed residence ledger.

The new result distinguishes two kinds of skips:

1. **period-neutral skip:** `p_(n+1)=p_n`;
2. **doubling skip:** `p_(n+1)=2p_n`.

Only the second type permanently increases a global state variable. Therefore negative ledger charge caused by doubling skips cannot be regarded as structurally identical to negative charge caused by period-neutral skips.

The period-doubling potential does not itself solve Problem 1: boundedness above of `e_v` could still be compatible, a priori, with infinitely many skips and unbounded `p_n`. What is now ruled out is the possibility that cycle-period complexity accumulated during one negative plateau simply disappears when that plateau exits.

## Relation to the post-threshold forced-exit theorem

The previous note proved a stronger local statement in the literal-zero regime: if periodic `z` has period `p` and its **zero lift** `2z` has period `2p`, then the next zero lift `4z` is nonperiodic.

The global theorem here is complementary:

- before the common-origin threshold, the successive lift bits come from the physical row and need not be zero, so a doubling does not by itself force the next tower state to rise;
- after the common-origin threshold, the lift bits are literal zeros, so a doubling skip is terminal for that periodic zero-extension prefix;
- in either regime, once the doubling has occurred, the doubled eventual period survives every later rise.

Thus period can accumulate only at skips, and in the post-threshold part of a plateau such an accumulating skip forces that plateau to exit on the following zero lift.

## Exact bridge across a plateau exit

Suppose a post-threshold plateau has physical-row origin

    u=T^H(v)

and literal periodic prefix

    u,2u,...,2^(Q-1)u,

while `2^Q u` is the first nonperiodic extension with

    d=tau(2^Q u)>0.

Let

    H'=H+d,
    n'=2H+Q,
    k=2d-Q.

The existing causal exit bound gives

    d >= ceil((Q+1)/2),

so

    k>=1.

At the new transient-stripping time,

    A^d(2^Q u)
      = sigma^(2d-Q) T^d(u)
      = sigma^k T^d(u).

This state is periodic by definition of `d`. Also

    2H'-n' = 2(H+d)-(2H+Q)=k.

So the exit lands exactly `k` tower positions before the next common-origin threshold, and its periodic stripped core is precisely the `k`-bit projection of the next physical row `T^d(u)`.

The eventual period of this core equals the eventual period of the exiting state `2^Q u`; by Theorem 2 that period is exactly the period of its terminal periodic parent `2^(Q-1)u`, because the exit is a rise.

Therefore the terminal cycle period of one plateau is transported without loss into the periodic core at the entry of the next plateau. Any intervening periodic one-bit lifts before the next threshold can only preserve or double it.

This is the desired exact inter-plateau period bridge.

## Research consequence

The strongest next target is no longer to relate two plateau periods from scratch. The relation is now exact and monotone.

A useful all-depth contradiction would follow from either of these stronger statements:

1. show that under an eventual upper bound on `e_v(n)`, doubling skips must occur infinitely often, while FULL/common-origin structure permits only finitely many of them; or
2. show that sufficiently large persistent eventual period `p_n` forces a later residence surplus that dominates the skips needed to create that period.

A weaker but concrete intermediate target is to classify period-neutral skips in the post-threshold literal-zero regime. The previous forced-exit theorem completely controls doubling skips there; the remaining long negative plateaus must therefore be carried mostly by period-neutral zero lifts before their final exit.

Do not treat plateau exit as resetting the period potential. It does not.