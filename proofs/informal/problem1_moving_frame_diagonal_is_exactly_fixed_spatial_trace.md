# Problem 1: the growing moving-frame diagonal is exactly the fixed spatial trace

## Context

Runs 138--139 introduced coordinates attached to the deterministic left support front. If the initial leftmost 1 is at `L`, define

\[
y_j(t)=x_{L-t+j}(t).
\]

Then

\[
y_j(t+1)=F(y_{j-2}(t),y_{j-1}(t),y_j(t)),
\]

and every fixed offset `j` is eventually periodic. The remaining hope was to find a uniform-in-depth finite-state transport law from the stabilized left boundary down the growing diagonal `j ~ t` that reaches the fixed center/cyclic-source coordinates.

This note records an exact reindexing that sharply limits that strategy.

## Exact diagonal identity

For any fixed original spatial coordinate `k`, put

\[
j_k(t)=t+k-L.
\]

Then directly from the definition,

\[
 y_{j_k(t)}(t)
 =x_{L-t+(t+k-L)}(t)
 =x_k(t).
\]

Therefore the growing diagonal of the moving-front array is not merely related to the original fixed-coordinate trace: it **is exactly that trace**.

In particular, for the center,

\[
\boxed{y_{t-L}(t)=x_0(t).}
\]

Likewise neighboring growing diagonals are exactly the original neighboring columns:

\[
y_{t+k-L}(t)=x_k(t).
\]

## Diagonal update recovers ordinary Rule 30

Let `z_k(t)=y_{t+k-L}(t)=x_k(t)`. Using the triangular moving-frame recurrence at index `j=t+1+k-L`,

\[
\begin{aligned}
z_k(t+1)
&=y_{t+1+k-L}(t+1)\\
&=F(y_{t-1+k-L}(t),y_{t+k-L}(t),y_{t+1+k-L}(t))\\
&=F(z_{k-1}(t),z_k(t),z_{k+1}(t)).
\end{aligned}
\]

So restriction to these slope-one diagonals simply reconstructs the original Rule-30 evolution in fixed spatial coordinates.

## Consequence for the proposed finite-state transport route

This explains why fixed-`j` eventual periodicity does not automatically propagate toward the center. Reaching the center at time `t` requires depth `j=t-L`, and following that growing depth is exactly following the original center column. A putative uniform finite-state law that determines this diagonal from only the eventually periodic bounded-depth front would therefore amount to a new finite-state compression theorem for the original growing Rule-30 dependency cone.

There is no gain from the coordinate change alone.

Moreover, run 136 already proved by left-permutivity that arbitrary finite center words can be realized by finite-support initial rows. Hence no argument using only the universal eventual behavior of finitely many fixed front offsets can determine or forbid a finite center prefix. Any useful transport law must carry additional state whose information genuinely grows into the interior, or must exploit the special FULL/cyclic-source/right-fringe constraints rather than the moving-frame boundary by itself.

## Stopping fence

Do **not** spend further runs looking for a consequence of fixed-offset eventual periodicity that reaches `j=t-L` merely by reindexing or by taking larger fixed windows. The target diagonal is exactly the original center trace, so such a step would be circular unless a genuinely new uniform compression/invariant is proved.

A viable moving-cut invariant would need at least one extra ingredient:

1. a finite-range quantity conserved/monotone across the entire growing interior, not merely at each fixed front offset;
2. a relation using the FULL cyclic-source gate/right-fringe constraints that collapses the interior state at the distinguished episodes; or
3. a bounded-reuse charge connecting those episodes to finite initial data.

This is a structural clarification rather than a solution. Problem 1 remains open.
