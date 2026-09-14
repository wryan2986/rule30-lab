# Problem 1: the post-threshold half-depth bound is sharp

## Status

Problem 1 remains open. This note closes two tempting strengthenings of the run-10 common-origin plateau lemma.

The counterexample is not an arbitrary nested periodic-lift chain. It occurs in the literal zero-extension tower of the canonical single-cell packed state `v=1`, so it already has the required common physical origin.

## Packed maps

Use the standard packed Rule-30 update

    T(x) = x XOR ((x << 1) OR (x << 2)),
    A(x) = T(x) >> 2.

Write

    h_n = tau(2^n v).

Take `v=1`.

First,

    A(1)=1,

so `h_0=0`. Also

    2 -> 3 -> 3,

hence `h_1=1`, and

    4 -> 7 -> 6 -> 6,

hence `h_2=2`.

Thus tower index `n=2` is a genuine rise into a plateau of height

    H=2.

Its common-origin threshold is

    2H=4.

## Exact physical row at the threshold

Direct Rule-30 evolution gives

    T(1)=7,
    T^2(1)=25.

The run-10 identity therefore identifies the stripped post-threshold tower with

    25, 50, 100, 200, 400, 800, ...

The first five states are `A`-periodic. Their exact cycles are

    25  -> 27  -> 25,
    50  -> 55  -> 50,
    100 -> 111 -> 100,
    200 -> 222 -> 200,
    400 -> 444 -> 401 -> 445 -> 400.

Therefore

    tau(25 * 2^q)=0                 for 0 <= q <= 4.

At the next zero extension,

    800 -> 888 -> 802 -> 891 -> 801 -> 889 -> 803 -> 891 -> ...

so the first repeated state is `891`, first seen after three transient steps. Hence

    tau(800)=3.

Consequently, for the height-2 plateau,

    Q_H = 5,
    d_H = 3.

Equivalently, the original tower satisfies

    h_2=h_3=...=h_8=2,
    h_9=5.

(The post-threshold part begins at index `2H=4`; the five post-threshold skips are the transitions through indices `4,5,6,7,8` before the rise at `9`.)

## Sharpness of the causal lower bound

Run 10 proved universally at a post-threshold exit that

    d_H >= ceil((Q_H+1)/2).

Here

    ceil((5+1)/2)=3=d_H.

Thus the coefficient-one-half causal estimate is attained exactly, even by a literal physical-row zero-extension tower.

The signed excess change across this post-threshold segment is

    d_H-Q_H = 3-5 = -2.

So a genuine common-origin plateau can lose ledger excess across its complete post-threshold periodic prefix and first exit.

## Two universal strengthenings are false

This one exact example rules out both of the following proposed local theorems:

1. `d_H >= Q_H` for every post-threshold plateau exit;
2. `Q_H <= 2H` for every plateau that reaches its common-origin threshold.

Indeed, here

    d_H=3 < 5=Q_H,

and

    Q_H=5 > 4=2H.

More generally, any universal local inequality that strictly improves

    d_H >= ceil((Q_H+1)/2)

at every such exit is impossible without additional hypotheses that exclude this canonical physical example.

## Research consequence

The run-10 menu should now be narrowed.

A proof cannot solve Problem 1 by showing that each post-threshold plateau individually repays essentially all of its skipped depth. That fails already for `v=1`.

The remaining plausible direction is a coupling theorem across later tower segments: a deficit such as the exact `-2` above must be shown to force compensating surplus later, with bounded reuse, or one must construct a different non-telescoping global charge. The relevant information cannot be only the local pair `(Q_H,d_H)` at a single plateau exit.

This does not disprove the target `limsup_n (h_n-n)=+infinity`; it only shows that one plateau can make a real negative contribution even in the canonical common-origin setting.
