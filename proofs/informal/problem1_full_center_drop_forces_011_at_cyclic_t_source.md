# Problem 1: FULL center drop forces the `011` provenance fork

Status: exact all-depth local lemma.

## Setup

Let `q` be the cyclic `t` source considered in the forced-birth passage. The previous provenance notes established that the sensitive route into the later cyclic center passes through `r_-1(q+1)=1`, whose time-`q` neighborhood is either `001` or `011` according to the fork bit `a = r_-1(q)`.

The fork is in fact not free under FULL.

## Lemma

If the actual center satisfies

    r_0(q) = 1,
    r_0(q+1) = 0,

then

    r_-1(q) = 1.

### Proof

Rule 30 is

    f(l,c,r) = l XOR (c OR r).

At the center update from `q` to `q+1`, `c = r_0(q) = 1`, so `c OR r = 1` independently of `r_1(q)`. Hence

    r_0(q+1) = f(r_-1(q), 1, r_1(q))
               = r_-1(q) XOR 1.

Since FULL gives `r_0(q+1)=0`, necessarily `r_-1(q)=1`.

In the cyclic-`t` provenance calculation we also have `r_-2(q)=0` (from the already-established production of `r_-1(q+1)=1` with right input `r_0(q)=1`). Therefore that predecessor neighborhood is not `001`; it is exactly

    (r_-2(q), r_-1(q), r_0(q)) = 011.

So the sensitive-one lineage into the later forced birth terminates at an `011` event at every such cyclic `t` source.

## Consequences

1. The `001/011` dichotomy in run130 was over-permissive because it did not reuse the direct center update `1 -> 0` at time `q`. Under FULL, the fork bit is fixed to 1 before any four-step recurrence is needed.
2. The run132 endpoint question `r_-2(q+4)=0?` is no longer needed to decide this fork. The four-step zero-staircase lemma remains correct but is strictly weaker for this application.
3. The provenance route is now sharper: every relevant forced-birth lineage reaches the unique sensitive-one obstruction `011` at the preceding cyclic `t` source. Any finite birth-budget argument based on this route must therefore control this *source-relative family of `011` events*, not a free fork sequence.

## Computational sanity check

Exhaustive enumeration of the local dependency cone agrees: imposing only the center prefix `r_0(q..q+2)=101`, the cyclic-`t` gate condition `r_1(q) OR r_2(q)=1`, and the established `r_-2(q)=0` yields no assignment with `r_-1(q)=0`. The proof above shows that even the gate and `r_-2` conditions are unnecessary for forcing `r_-1(q)=1`; the center drop `1 -> 0` alone suffices.

## Remaining blocker

This does not yet bound the number of births. Generic `011` events are abundant, as run128 already showed. The next useful target is whether these distinguished `011` events at cyclic `t` sources possess a cross-episode ordering, spacing, or bounded-reuse property tied to the finite actual initial row. Do not return to the fork-bit parity/telescoping route: the fork is constant under FULL.