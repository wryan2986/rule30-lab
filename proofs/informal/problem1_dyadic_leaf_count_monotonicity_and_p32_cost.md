# Problem 1: dyadic leaf-count monotonicity and p=32 portal cost

## Context

Run 74 proved that `G_{2p}` consists of the repeated inherited copy of `G_p`, with one unary portal at each old odd leaf `l`, followed by a finite full-period binary tree. If `B(l)` is the number of full-period even internal vertices in that portal tree, then

`L_{2p} = sum_l (B(l)+1) = L_p + sum_l B(l)`.

This note records two consequences and a computational dead end encountered when beginning the proposed `p=32` portal-by-portal exploration.

## Leaf-count monotonicity

Because every portal tree is finite and nonempty and `B(l) >= 0`, the run-74 decomposition immediately gives

\[
\boxed{L_{2p}\ge L_p}
\]

for every dyadic doubling covered by the decomposition.

More precisely,

\[
L_{2p}-L_p=\sum_{l\in\mathrm{Leaves}(G_p)} B(l).
\]

Hence equality holds iff every old leaf's doubled portal reaches an odd full-period leaf before encountering any full-period even zero target. Strict growth occurs iff at least one portal encounters a full-period even zero target.

This isolates the exact obstruction to strict growth: it is not graph merging, cycling, leaf legality, or lower-period contamination (all already excluded), but simply whether a portal's first/new full-period zero-return component contains an even vertex.

For the known data, `L_8=1` and the unique period-8 portal has `B=15`, so `L_16=16`.

## First p=32 portal probe

The natural next finite computation is to start from each repeated period-16 leaf `ll` and follow its unary derivative lift to the first genuinely period-32 zero target, then explore only that portal component.

I implemented the established exact reverse recurrence directly on 32-bit words:

- at a zero target `(0,w)`, solve `Sx xor x = w`;
- from `(x,0)`, while the first component is nonzero, solve the unique predecessor equation
  `b = S y xor (a or y)` and replace `(a,b)` by `(y,a)`;
- stop at the next zero state.

As a sanity target I used the first canonical period-16 terminating leaf from the complete p=16 census,

`l = 0000010101000101`,

and its period-32 portal target `ll`.

A straightforward optimized C implementation (`gcc -O3`, 32-bit packed states) did **not** reach the next zero column within 10,000,000 exact reverse predecessor steps. The run was explicitly capped at that value and returned the cap, so this is a rigorous lower bound on that connector length for this implementation/convention, not an estimate of the eventual return length.

A Python prototype had already hit a 5,000,000-step cap on the same portal; the C rerun confirms that the issue is connector length rather than Python overhead.

## Consequence for computation

Run 74's portal decomposition reduces branching enormously, but it does **not** by itself make `p=32` cheap: even a single unary portal-to-first-return connector can exceed ten million reverse columns. A monolithic `G_32` traversal with the current one-column-at-a-time inverse is therefore the wrong next implementation strategy.

The useful computational target is now an accelerated first-return operator. Possible exact routes include:

1. derive a block/jump representation for repeated applications of the unique inverse map while `u != 0`;
2. exploit the antiperiodic structure of the initial period-32 lift (`S^16 x = complement(x)`) to compress the first connector;
3. detect repeated affine/Boolean transfer maps on chunks of columns and compose them rather than advancing one column at a time.

Any accelerated method must preserve exact zero-hit detection; skipping over an intermediate zero column would invalidate the first-return graph.

## Research status

The new all-depth consequence is the monotonicity theorem `L_{2p} >= L_p` and the exact equality/strictness criterion above. The attempted p=32 finite extension is presently blocked by very long deterministic connectors, with the first tested portal proven to require more than 10,000,000 one-column inverse steps before its next zero return.
