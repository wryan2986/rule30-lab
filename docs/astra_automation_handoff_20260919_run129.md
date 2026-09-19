# Astra automation handoff — run 129

Problem 1 remains OPEN.

Starting branch tip: `aa7314f04c39f9a36f2719db4c488602424c7fa7` (`research/astra-next`). No intervening work was found after run128.

## New result

Run128 left one precise target: apply sensitive-1 routing to the forced `beta=1` born after a two-bit nonreset source and see whether it hits the unique `011` obstruction.

It does not hit `011` locally. Let `s=t+4` be the cyclic `u` source immediately preceding the forced birth. Its actual right pair is `00`, and FULL centers at `s,s+1,s+2` are `1,0,1`. Thus

    r_1(s+1)=f(1,0,0)=1.

Since the next center is one,

    1=f(r_-1(s+1),0,1)

forces `r_-1(s+1)=0`. Therefore the birth center at `s+2=t+6` is produced by exact neighborhood `001`; its sensitive 1-parent is `r_1(s+1)`. That intermediate 1 was itself produced by exact neighborhood `100` at time `s`, so its sensitive 1-parent is the center `r_0(s)=1`.

Hence the forced birth has the exact two-step sensitive-1 route

    center(t+6) <- r_1(t+5) <- center(t+4).

The local birth segment therefore reuses the preceding cyclic center lineage rather than supplying a new provenance label. Any `011` obstruction relevant to this strategy must occur earlier than `t+4`.

Recorded in `proofs/informal/problem1_forced_birth_sensitive_route_reuses_prior_center.md`, commit `208255c7e2cf570c5271f3fc18344ee613d212b7`.

## Next target

Continue sensitive-1 provenance from the cyclic center at `t+4` backward through the cyclic `t` source at `t+2` and the completed nonreset return. Determine whether it is forced into a source-relative `011` or reaches another distinguished source/center. Stop unless this produces a genuine cross-episode ordering or bounded-reuse law; route extension alone is not a finite birth budget.
