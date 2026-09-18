# Problem 1: every fixed moving-right-fringe prefix is purely periodic (no-go)

## Purpose

Run 109 isolated a possible next target: attach a bounded state to the terminal fringe, compute its transition across regenerative passages, and hope that the reachable state graph is acyclic. For the most natural such state — any fixed-width prefix measured behind the maximal right-moving ray — this cannot work. The transition is an autonomous permutation, hence every such prefix is purely periodic from time zero.

## Setup

Let `r` be a nonzero finite Rule-30 row with right support endpoint `R`, so `r_R=1` and `r_x=0` for `x>R`. Write Rule 30 as

    F(l,c,u) = l XOR (c OR u).

For `t,j >= 0`, define the moving-right-edge coordinates

    a_j(t) = (T^t r)_{R+t-j}.

Set `a_{-1}(t)=a_{-2}(t)=0`, corresponding to cells beyond the maximal right ray.

## Exact autonomous recurrence

The three parents of `a_j(t+1)` are, at time `t`,

    a_j(t), a_{j-1}(t), a_{j-2}(t).

Therefore

    a_j(t+1)
      = a_j(t) XOR (a_{j-1}(t) OR a_{j-2}(t)).          (1)

In particular `a_0(t+1)=a_0(t)`, and since `a_0(0)=r_R=1`, the maximal right ray is identically one.

For every fixed `J`, the vector

    A_J(t)=(a_0(t),...,a_J(t))

therefore evolves autonomously: its next state depends only on itself, not on any deeper part of the row.

## The transition is a permutation

Define `Phi_J` on `{0,1}^{J+1}` by the right side of (1). Coordinate `j` has the triangular form

    y_j = x_j XOR f_j(x_0,...,x_{j-1}),

where `f_j=x_{j-1} OR x_{j-2}` (with the negative-index convention above).

Such a triangular Boolean map is bijective. Indeed, recover coordinates successively:

    x_0 = y_0,

and after `x_0,...,x_{j-1}` are known,

    x_j = y_j XOR f_j(x_0,...,x_{j-1}).

Hence `Phi_J` is a permutation of the finite state space `{0,1}^{J+1}`. Restricting to the invariant slice `a_0=1` preserves bijectivity.

Consequently every orbit of every fixed moving-right-fringe prefix is **purely periodic from time zero**. There is no transient tree and no acyclic forward state graph to consume.

## Consequence for the finite-support-budget route

This decisively rejects the simplest version of the run-109 proposal. A budget based only on the instantaneous bits in a fixed-width strip behind the maximal right ray cannot be a strictly decreasing well-founded resource: that state necessarily recurs forever.

This is stronger than merely observing that late events reuse the same original terminal support positions. Even their natural finite moving-edge state is recurrent by exact Rule-30 dynamics.

Therefore any successful original-fringe non-reuse invariant must contain information not present in a fixed instantaneous moving-edge prefix. Possibilities include an unbounded-depth anchored phase/history variable, coupling to the core/global shadow, or a state indexed by a distinguished source/characteristic rather than by fixed distance from the maximal ray.

In particular, checking whether the fixed terminal-prefix state graph is acyclic is unnecessary: it is exactly a permutation graph, a disjoint union of directed cycles.

## Status

This is a stopping-fence result, not a solution of Problem 1. It narrows the missing all-depth mechanism by ruling out fixed-width moving-right-fringe state consumption as the finite-support budget.
