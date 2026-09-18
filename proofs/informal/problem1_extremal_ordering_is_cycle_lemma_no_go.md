# Problem 1: extremal ordering is a cycle-lemma normalization

## Status

No-go refinement following the extremal-return-block result. This does not solve Problem 1. It shows that the one-sided ordering inside an extremal return block is a generic property of zero-charge residence words, so that property alone cannot supply the missing FULL/fringe contradiction.

## Setup

Write

    s_i = delta_i - 1.

Since residence increments satisfy delta_i >= 0, every step obeys

    s_i >= -1.

A return block q_a=q_b has

    sum_[a,b) s_i = 0.

Run 103 observed that if a is a recurrent minimum of q, then every partial sum from a is nonnegative until the return to that minimum.

## Cycle-lemma normalization

Take any finite integer word

    s_0,...,s_(ell-1),   s_i >= -1,

with total sum zero. Define prefix sums

    S_0=0,
    S_j=sum_(i=0..j-1) s_i.

Choose k at which S_k is a global minimum, taking the last minimum if a strict convention is desired. Cyclically rotate the word so that it begins at k. For a prefix that does not wrap, its sum is

    S_j-S_k >= 0.

For a prefix that wraps through ell, its sum is

    (S_ell-S_k)+S_j = -S_k+S_j >= 0,

because S_ell=0 and S_k is a global minimum. Therefore every zero-charge residence word has a cyclic rotation whose partial sums are all nonnegative.

Equivalently, every zero-total word in the residence alphabet delta_i>=0 can be rooted at a minimum so that it becomes exactly the kind of nonnegative excursion found in run 103. Rooting at a global maximum gives the dual nonpositive normalization.

## Consequence for the proposed ordering strategy

The sign restriction on minimum-to-minimum or maximum-to-maximum blocks is therefore not additional Rule-30 structure. It is a generic normalization of any zero-charge word. In particular, an argument of the form

    "a minimum excursion must put surplus before the compensating skip"

cannot by itself contradict the bounded-slack alternative: that ordering is precisely what choosing the minimum as the root guarantees.

A useful FULL-specific ordering theorem must instead anchor an event independently of the q-extremum. Examples would be:

* a distinguished complete-fringe phase that must occur before/after a skip or surplus;
* a fixed actual-fringe marker whose temporal order is not chosen by rotating/rooting the residence word;
* a parity/phase class preserved by the actual dynamics that prevents moving the root to the convenient extremum;
* a charge attached to a specific FULL source whose sign is fixed before the extremal decomposition is chosen.

Without such an external anchor, any proposed finite zero-charge residence pattern can simply be rooted at one of its minima and automatically satisfies the run-103 one-sided-prefix condition.

## Relation to physical restart

This is a combinatorial cyclic-word statement, not a claim that arbitrary cyclic rotations are realizable by physical restart. The previously proved restart covariance shifts the normalized-excess tail only by the permitted dynamical reindexing. The point here is narrower: the extremal-block sign property itself carries no Rule-30 information, because the same property exists for every abstract zero-charge word after choosing an extremal root.

Thus the next useful target should not be an unanchored skip-versus-surplus ordering theorem. It should couple skip/surplus order to a distinguished COMPLETE-fringe phase or other survivor-specific marker that cannot be selected after seeing q.

Problem 1 remains OPEN.
