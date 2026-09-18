# Problem 1: bounded-counterexample slack/discrepancy dichotomy

## Status

Exact reduction for any hypothetical finite survivor whose physical delay remains in a bounded strip. This does not solve Problem 1, but it separates the remaining scalar obstruction into two exhaustive cases and gives a uniform interval-discrepancy law in the bounded-slack case.

## Setup

Fix a nonzero finite row `r`, choose its actual right endpoint `R`, and put

    v = L_R(r),
    h_n = tau(2^n v),
    q_n = h_n - n - R,
    delta_n = h_(n+1)-h_n >= 0.

Then

    q_(n+1)-q_n = delta_n-1.                 (1)

The physical delay at characteristic `R+n` is

    d_n = max(q_n,0),

while at a zero-delay row the hidden slack is

    g_n = max(-q_n,0).

Thus `q_n=d_n-g_n` exactly.

Assume the putative counterexample has an eventual physical strip

    d_n <= K

for all sufficiently large `n`. Equivalently, `q_n<=K` eventually.

## Dichotomy

Exactly one of the following alternatives holds after discarding a finite prefix.

### A. Unbounded hidden slack

`q_n` is unbounded below. Equivalently,

    limsup g_n = +infinity.

Then any proof of Problem 1 may target arbitrarily deep negative excursions directly: a FULL-dependent recovery theorem must show that sufficiently deep slack cannot be absorbed forever without a later overshoot above the fixed strip ceiling `K`.

### B. Bounded hidden slack

There is `G>=0` with

    -G <= q_n <= K                              (2)

for every sufficiently large `n`.

In this case the residence ledger has **uniform bounded discrepancy on every late interval**. For all sufficiently large `a<b`, telescoping (1) gives

    sum_(n=a..b-1) (delta_n-1) = q_b-q_a,

hence

    |sum_(n=a..b-1) (delta_n-1)| <= K+G.        (3)

Equivalently, with

    Z[a,b) = #{a<=n<b : delta_n=0},
    P[a,b) = sum_(a<=n<b, delta_n>=2) (delta_n-1),

one has the exact identity

    P[a,b)-Z[a,b) = q_b-q_a

and therefore

    |P[a,b)-Z[a,b)| <= K+G.                    (4)

This is stronger than a prefix-only balance: **every** late interval has bounded excess of long-residence surplus over skips and vice versa.

There is also an immediate pointwise residence bound. From (1) and (2),

    delta_n = 1+q_(n+1)-q_n <= 1+K+G,          (5)

so every late characteristic residence length belongs to the finite alphabet

    {0,1,...,K+G+1}.

## Consequences

A bounded-strip counterexample cannot have both bounded hidden slack and an accumulating signed residence bias. In case B, any collection of disjoint late episodes whose signed charges all have the same nonzero sign must be compensated outside those episodes within a total discrepancy window of width `K+G`; otherwise (3) is violated on an interval spanning sufficiently many episodes.

This does **not** resurrect the separated-birth summation route. The pushed physical-episode telescope already shows that the known forced-birth passages can have charge `-1` or `0`, and compensation can occur in the gaps. What (3) adds is the correct all-interval formulation of what a successful episode theorem would need: not merely many births, but a one-sided charge that cannot be compensated indefinitely by the complete fringe dynamics.

The two alternatives therefore give two sharply different remaining targets under the hypothetical bounded strip:

1. **Case A:** prove a deep-slack recovery/overshoot theorem: arbitrarily negative `q` forces a later value above `K` under FULL.
2. **Case B:** exploit the finite residence alphabet plus the uniform all-interval discrepancy bound to obtain a survivor-specific finite-state or bounded-reuse contradiction from the complete fringe.

The previous run showed that the normalized-excess germ `Q` is invariant under finite physical restart. The present dichotomy is likewise tail-invariant: deleting any finite prefix does not change whether case A or B holds, and in case B only the existence of some finite `G` matters.

## What is not proved

Neither alternative is currently contradictory by itself. Arbitrary abstract integer walks can satisfy case B forever (for example `q_n` constant, hence `delta_n=1`). The missing mathematics remains Rule-30/FULL-specific coupling to the complete finite fringe. The value of this reduction is that a future proof no longer needs to reason vaguely about hidden slack: every bounded-strip survivor must either produce unbounded hidden slack, or enter a uniformly bounded-discrepancy finite residence regime.