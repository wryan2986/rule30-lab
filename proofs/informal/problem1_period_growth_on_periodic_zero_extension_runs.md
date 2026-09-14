# Problem 1: period growth along periodic zero-extension runs

## Status

Problem 1 remains open. This note gives a new exact structural invariant for the post-threshold periodic prefix discussed in the run-10/run-11 notes.

The run-11 example showed that an individual plateau can have negative signed excess change, so a useful inter-plateau quantity must retain information not present in the scalar pair `(Q_H,d_H)`. The exact cycle period of the stripped periodic states is one such quantity.

## Setup

Let

    T(x) = x XOR ((x << 1) OR (x << 2)),
    A(x) = T(x) >> 2.

Suppose `z` is periodic under `A` with exact period `p`. Write a one-bit lift as

    w = 2 z + a_0,

and along the base orbit put

    z_s = A^s(z),
    b_s = bit_0(z_s),
    c_s = bit_1(z_s).

The previously proved one-bit lift recurrence is

    a_(s+1) = c_s XOR (b_s OR a_s).

The projection of the lifted orbit is the base orbit, so any period of a periodic lift must be a multiple of `p`.

## Lemma 1: a periodic one-bit lift has period p or 2p

Consider the return map on the lift bit after one complete base period,

    F : {0,1} -> {0,1},
    a_0 |-> a_p.

A periodic lifted state requires `a_0` to lie on a periodic orbit of `F`. Since `F` acts on two points, its recurrent orbit has length one or two. Because projection to the base requires the lifted period to be a multiple of the exact base period `p`, the exact lifted period is therefore

    p  or  2p.

More precisely:

1. If `b_s=1` for some `0<=s<p`, then that step is an eraser: the update no longer depends on the incoming lift bit. Hence `F` is constant. There is a unique recurrent lift bit, and the corresponding periodic lift has exact period `p`.

2. If `b_s=0` for every `0<=s<p`, then every step is affine without erasure,

       a_(s+1)=a_s XOR c_s.

   Thus

       F(a)=a XOR C,
       C = XOR_(s=0..p-1) c_s.

   If `C=0`, both lifts have exact period `p`; if `C=1`, both lifts have exact period `2p`.

Therefore period doubling is possible only when the entire base cycle has low bit zero.

## Lemma 2: a deep literal zero extension cannot have too short a period

Let `u>0`, and suppose

    z_q = 2^q u

is periodic under `A` with exact period `p`.

If `q>=2p`, then the exact renormalization identity can be iterated for all `p` steps without exposing the low boundary:

    A^p(2^q u) = 2^(q-2p) T^p(u).

Periodicity would force

    2^(q-2p) T^p(u) = 2^q u,

hence

    T^p(u) = 2^(2p) u.

But `T` preserves the 2-adic valuation of every nonzero integer. Indeed, if `nu_2(u)=r`, then the lowest nonzero bit of `u` is at position `r`, while both shifted terms in

    (u << 1) OR (u << 2)

vanish below position `r+1`, so the bit at position `r` survives in `T(u)`. Thus

    nu_2(T^p(u)) = nu_2(u),

whereas

    nu_2(2^(2p)u)=nu_2(u)+2p,

an impossibility.

Therefore every nonzero periodic literal zero extension obeys the strict bound

    q < 2p.

Equivalently,

    p > q/2.

## Corollary: periodic skip runs force period doublings

Consider a literal post-threshold chain

    z_q = 2^q u,

and suppose `z_q` is periodic for `0<=q<Q`. Let `p_q` be its exact `A`-period.

By Lemma 1,

    p_(q+1) in {p_q, 2 p_q}

for every `q+1<Q`.

Hence

    p_q = p_0 * 2^(D_q),

where `D_q` is the number of period-doubling steps among the first `q` lifts.

Lemma 2 gives

    q < 2 p_0 2^(D_q).

So a periodic zero-extension run cannot continue arbitrarily deeply while keeping its cycle period fixed. Once `q>=2p_0`, at least one doubling must already have occurred; more generally, increasingly deep periodic runs require repeated powers-of-two growth of the cycle period.

This is a genuinely non-telescoping state variable: the signed residence ledger can lose value across a plateau, but the cycle period cannot decrease along the periodic part of a literal zero-extension chain.

## Exit bound from the terminal period

Let `Q` be the first index for which `z_Q=2^Q u` is nonperiodic, while `z_(Q-1)` is periodic of exact period `p`.

The terminal periodic core cannot have low trace identically zero: in that case Lemma 1 shows that both one-bit lifts are periodic (with period `p` or `2p`), contradicting nonperiodicity of `z_Q`.

Therefore the terminal core has an eraser. Let

    r = min{s>=0 : bit_0(A^s(z_(Q-1)))=1}.

Then `0<=r<=p-1`, and the one-bit lift classifier gives

    tau(z_Q)=r+1.

Consequently

    1 <= tau(z_Q) <= p.

Combining this with the run-10 causal exit estimate

    tau(z_Q) >= ceil((Q+1)/2)

shows

    p >= ceil((Q+1)/2).

Thus a long negative plateau segment necessarily exits from a periodic core whose cycle period has already grown to at least half the periodic-prefix depth.

## Canonical v=1 example revisited

For the run-11 example,

    u = T^2(1) = 25,

and the periodic prefix is

    25, 50, 100, 200, 400.

Their exact periods are

    2, 2, 2, 2, 4.

The final state `400` must have doubled period: if its period had remained `2`, Lemma 2 would forbid periodicity at depth `q=4`, because the strict condition would read `4<4`.

So the same example that disproves local full repayment also exhibits the new mechanism exactly: its five-deep periodic prefix is sustained only by a forced cycle-period doubling before the nonperiodic exit.

The exit state `800` has preperiod `3`, while its parent `400` has period `4`, consistent with

    tau(800) <= 4.

## Research consequence

This does not yet prove inter-plateau compensation. Period growth can, in principle, support long periodic prefixes by repeated doubling, and the current argument gives only logarithmic lower bounds on the number of doublings as a function of depth.

However, it rules out treating successive negative plateaus as scalar copies with no memory. A long post-threshold deficit necessarily transports increasing cycle-period complexity into its terminal periodic core.

A useful next theorem would couple this period potential to the next plateau. Two concrete targets are:

1. show that period doublings accumulated during one negative plateau force extra preperiod growth at a later rise, with bounded reuse; or
2. prove that the physical/common-origin structure bounds how often the cycle period can double without creating positive excess `h_n-n`.

Any future inter-plateau argument should track `(h_n, period of the stripped periodic core)` rather than only `(Q_H,d_H)`.
