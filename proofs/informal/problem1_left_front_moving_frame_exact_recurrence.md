# Problem 1: exact finite-support left-front recurrence

## Status

Useful structural lemma / candidate moving-cut coordinate system. This does **not** solve Problem 1.

## Setup

Let `x_i(t)` be a finite-support Rule-30 orbit, with local rule

`F(l,c,r) = l xor (c or r)`.

Let `L` be the leftmost occupied site at time 0. Rule 30 has exact left-front speed one: the leftmost occupied site at time `t` is

`L_t = L - t`.

Indeed the site `L_t-1` sees `001` and becomes 1, while everything farther left still sees `000`.

Define the moving-frame bits

`y_j(t) = x_{L-t+j}(t)`,  `j >= 0`,

and set `y_{-1}(t)=y_{-2}(t)=0`.

## Exact recurrence

Because the frame itself shifts left by one site each step,

`y_j(t+1) = F(y_{j-2}(t), y_{j-1}(t), y_j(t))`.

This is a one-sided triangular recurrence: the first `m` moving-front bits evolve autonomously from the first `m` moving-front bits. No cells farther to the right can influence them.

In particular:

- `y_0(t)=1` for every `t`;
- after one step, `y_1(t)=1` forever;
- after two steps, `y_2(t)=0` forever;
- once the preceding stabilization has occurred,
  `y_3(t+1)=1 xor y_3(t)`, so the fourth front bit alternates forever.

Thus every finite-support Rule-30 orbit has the universal asymptotic left-front prefix

`110*...`,

with the `*` at offset 3 alternating with period two.

More generally, every fixed-width left-front window is a finite autonomous dynamical system under the displayed triangular map, so its eventual behavior can be studied exactly without simulating the unbounded interior.

## Relation to the current FULL/cyclic-birth bottleneck

Runs 133--137 reduced the sensitive-provenance route to distinguished `011` events near the fixed center and showed that simple initial-support labels fail: sensitive labels escape into the initial zero tail, while ordinary 1-ancestry can reuse the preceding cyclic center.

The recurrence above gives a clean finite-support moving-cut state space that was not explicit in those runs. It is potentially useful because any proposed global finite-support invariant involving the *left boundary* can now be tested in a genuinely finite autonomous system.

However, it does **not** yet bound the distinguished events. Their spatial location remains near the fixed center while the left front is at `L-t`; hence their moving-frame index grows linearly with time. A fixed-width front window therefore does not directly see the cyclic source or its distinguished `011` event.

This is an important stopping fence: merely replacing the time-zero sensitive label by a fixed-width state attached to the left front cannot by itself count the center-side forced births. A successful moving-cut argument must either

1. propagate some bounded state from this triangular front system across an expanding distance to the cyclic source, or
2. choose a cut whose position tracks the cyclic source while retaining a finite-range quantity inherited from finite support.

## Next useful test

Exploit the triangular recurrence computationally/symbolically to ask whether there is any low-width quantity (parity, affine form, finite automaton state) transported from the left front along the right-moving sensitive characteristic that ends at the distinguished `011` event. The target should be a quantity with finite range **and bounded reuse** across cyclic episodes. Fixed front prefixes alone should not be pursued further.