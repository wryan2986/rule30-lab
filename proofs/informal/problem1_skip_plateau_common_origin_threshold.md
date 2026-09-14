# Problem 1: common-origin threshold inside a skip plateau

## Status

Problem 1 remains open. This note sharpens the remaining long-skip-block loophole.

The point is that the transient-stripped states in a tower plateau are not arbitrary nested lifts forever. Once the tower depth catches the inherited transient shift, they become literal zero-extensions of one concrete physical Rule-30 row.

## Setup

Fix a nonzero finite state `v` and write

    h_n = tau(2^n v).

Suppose a constant-height plateau begins at tower index `n` with

    h_n = H.

For `m >= 0`, transient stripping from `y=2^n v` gives

    x_m = A^H(2^m y)
        = A^H(2^(n+m) v)

and

    h_(n+m) = H + tau(x_m).

Using `A^H = sigma^(2H) T^H` together with

    T^H(2^(n+m) v) = 2^(n+m) T^H(v),

put

    w = T^H(v).

Then exactly

    x_m = sigma^(2H)(2^(n+m) w).

Therefore there are two regimes:

    if n+m <= 2H,
        x_m = sigma^(2H-n-m) w;

    if n+m >= 2H,
        x_m = 2^(n+m-2H) w.

At the threshold

    m_* = 2H-n,

we have the exact identity

    x_(m_*) = w = T^H(v).

Past that threshold,

    x_(m_*+q) = 2^q w.                         (1)

So a plateau that survives to depth `2H` has ceased to be a generic nested-lift chain. Its continuation is exactly the ordinary zero-extension tower of the physical row `T^H(v)`.

## The threshold is not behind a genuine plateau entry

Assume `n>0` is a genuine rise index,

    h_n = H > h_(n-1).

The hidden-slack causal bound already proved on the original finite orbit gives

    H >= ceil((n+1)/2).

Hence

    n <= 2H-1,

so

    m_* = 2H-n >= 1.

Thus every noninitial plateau begins at or before its common-origin threshold. There are only two possibilities:

1. the plateau exits before `n+m=2H`; this is the pre-threshold nested-lift regime;
2. it reaches `2H`, after which all further skips are literal zero-extension periodicity of `w=T^H(v)`.

This separates the generic nested-lift counterexamples from the genuinely tower-specific part of a long plateau.

## Exact post-threshold plateau length

Assume the plateau reaches the threshold `2H`. Then `x_(m_*)=w` is `A`-periodic, because the plateau condition says `tau(x_(m_*))=0`.

Define

    Q_H = min { q >= 0 : tau(2^q w) > 0 },

where `w=T^H(v)`.

The established zero-extension divergence theorem (or equivalently the fact that `h_n -> infinity`) makes `Q_H` finite. Since `tau(w)=0` here, `Q_H >= 1`.

By (1), for every `0 <= q < Q_H`,

    h_(2H+q) = H,

while at the first exit

    h_(2H+Q_H) = H + d_H,

with the exact exit increment

    d_H = tau(2^Q_H w) > 0.                    (2)

Thus the part of a height-`H` plateau lying beyond depth `2H` is measured exactly by the initial periodic prefix of the zero-extension tower of the concrete physical row `T^H(v)`.

This is stronger than saying that a long block has a common origin: it identifies the precise state and the precise scalar whose first positive value terminates the block.

## Causal lower bound on the exit increment

The first post-threshold exit occurs at tower index

    p = 2H + Q_H.

It is a genuine rise, so the hidden-slack causal bound applies:

    h_p >= ceil((p+1)/2).

Using (2),

    H + d_H
      >= ceil((2H+Q_H+1)/2)
      = H + ceil((Q_H+1)/2).

Therefore

    d_H >= ceil((Q_H+1)/2).                   (3)

So a long post-threshold run of periodic zero-extensions cannot exit with an arbitrarily small residence. At least half of its depth is recovered in the exit increment.

Equivalently, across the `Q_H` transitions from tower index `2H` through the exit at `2H+Q_H`, the signed excess change is

    e_v(2H+Q_H) - e_v(2H)
      = d_H - Q_H
      >= ceil((Q_H+1)/2) - Q_H.

This can still be negative, by roughly `Q_H/2`.

## What this rules out, and what it does not

The arbitrary periodic nested-lift counterexample from `problem1_maximal_skip_block_ledger.md` cannot model the entire tail of a sufficiently long height-`H` plateau. Once the absolute tower index reaches `2H`, the states are forced into the literal zero-extension tower of `T^H(v)`.

However, the causal bound (3) is not strong enough to solve Problem 1. The desired scalar is

    e_v(n)=h_n-n,

and recovering only about half of a post-threshold skip run still permits `e_v` to drift downward. In particular, the currently proved all-depth inequalities remain compatible with a schematic growth law of order

    h_n ~ n/2,

which has `e_v(n) -> -infinity` and therefore gives no contradiction to an eventual bounded physical-delay strip.

So merely proving that every long skip plateau eventually reaches common-origin zero-extensions is not enough. The missing theorem must improve one of the following:

1. bound `Q_H` for the special physical rows `T^H(v)` by substantially more than the radius-one causal estimate;
2. force `d_H` to be comparable to `Q_H` with coefficient 1 (and with recurrent positive surplus often enough), rather than only coefficient 1/2; or
3. couple successive plateaus so that the apparent half-depth deficit cannot recur indefinitely.

## Preferred next target

Study the initial periodic zero-extension depth

    Q_H = min { q : tau(2^q T^H(v)) > 0 }

for those physical times `H` at which the height-`H` tower plateau reaches index `2H`.

The exact renormalization identity says

    tau(2^q T^H(v))
      = max(h_v(2H+q)-H,0),

so this is not a new independent process. The useful extra input has to come from the FULL/global-front structure of the physical row `T^H(v)`, not from generic eventual-periodicity of zero extensions.

Do not infer positive ledger gain from (3): it only gives half-depth recovery and explicitly leaves the main scalar target open.
