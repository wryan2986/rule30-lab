# Problem 1: every fixed left-front offset is eventually periodic

## Setup

Let a finite-support Rule-30 initial row have leftmost 1 at coordinate `L`, and use the moving coordinates from run 138

`y_j(t) = x_{L-t+j}(t)`.

Then `y_{-1}=y_{-2}=0` and

`y_j(t+1) = F(y_{j-2}(t), y_{j-1}(t), y_j(t))`,

where `F(l,c,r)=l xor (c or r)`.

Run 138 observed that each fixed-width prefix is an autonomous finite system. The stronger point below is that each individual fixed offset is necessarily eventually periodic, inductively from the triangular form.

## Lemma

For every fixed `j >= 0`, the binary sequence `t -> y_j(t)` is eventually periodic.

### Proof

Proceed by induction on `j`.

For `j=0`, the leftmost front bit is identically 1. For `j=1`, the recurrence gives eventual (indeed immediate after the first update) constancy at 1. Thus the base cases are periodic.

Assume `y_0,...,y_{j-1}` are eventually periodic. In particular the pair

`d_t=(y_{j-2}(t),y_{j-1}(t))`

is eventually periodic, say with period `P` after time `T`.

For `t>=T`, the remaining bit obeys a one-bit periodically driven recurrence

`y_j(t+1)=phi_t(y_j(t))`,

where `phi_t(r)=F(d_t[0],d_t[1],r)` and `phi_{t+P}=phi_t`.

Sample only at times `T+nP`. One complete forcing period induces a fixed map

`Phi : {0,1} -> {0,1}`.

Iteration of any map on the two-element set is eventually periodic (with eventual cycle length at most 2). Hence the sampled sequence is eventually periodic. Restoring the `P-1` intermediate phases shows the full sequence `y_j(t)` is eventually periodic (with a period dividing `P` or `2P` after a sufficiently long transient).

This closes the induction.

## Consequence

Every bounded-width strip attached to the deterministic left support front eventually cycles, and this can be proved coordinate-by-coordinate without merely invoking finiteness of the whole prefix state space. If `P_{j-1}` is a common eventual period for offsets below `j`, then offset `j` admits an eventual period dividing `2 P_{j-1}`. Starting from period 1 at the stabilized low offsets, one may therefore choose power-of-two upper bounds on the eventual periods of successive fixed offsets.

For orientation, the first universal low-offset relations from run 138 are

- `y_0 = 1`,
- eventually `y_1 = 1`,
- eventually `y_2 = 0`,
- `y_3` alternates with period 2.

The exact phases farther right can retain dependence on the initial finite row, but no fixed offset can carry aperiodic information forever.

## Relevance and stopping fence

This strengthens the finite-state boundary picture but does **not** solve Problem 1. A distinguished source-relative `011` event near the fixed center at physical time `q` has moving-frame index approximately `q-L`, so the relevant index tends to infinity. The theorem applies to each fixed `j`; it gives no uniform stabilization time or uniform state description along the growing diagonal `j~t`.

Therefore a contradiction cannot follow merely from saying that the left-front boundary is eventually periodic at every fixed depth. A successful use of this structure must establish a **uniform-in-depth transport law** (or a finite automaton propagated down the growing diagonal) connecting the periodic boundary hierarchy to the cyclic-source/gate constraints near the center.

This is a useful stopping fence: further computation of individual fixed offsets or their periods is unlikely to address the birth-budget bottleneck unless it reveals such a uniform law.

Problem 1 remains open.
