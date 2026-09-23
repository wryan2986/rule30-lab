# Problem 1 — run 217: exact recurrence inside an adjacent-defect agreement gap

Problem 1 remains OPEN.

## Setup

Run 215 established, for the cross-level defect layers,

\[
d_r(k+1)=d_{r-2}(k)\oplus(d_{r-1}(k)\lor d_r(k)).
\]

Run 216 defined the agreement indicator relevant to a level-\(j\) reset gap,

\[
g_j(k)=d_{j-2}(k)\oplus d_{j-3}(k),
\]

and showed that a reset-free interval for the level-\(j\) lift persists exactly while \(g_j=0\).

## Exact one-step recurrence for g

Applying the defect recurrence separately to \(d_{j-2}\) and \(d_{j-3}\) gives

\[
\begin{aligned}
g_j(k+1)
={}&d_{j-5}(k)\oplus d_{j-4}(k)\\
&\oplus (d_{j-3}(k)\lor d_{j-2}(k))\\
&\oplus (d_{j-4}(k)\lor d_{j-3}(k)).
\end{aligned}
\]

This is an exact recurrence, but its useful form appears after conditioning on being inside the agreement gap.

Suppose

\[
g_j(k)=0,
\]

so

\[
d_{j-2}(k)=d_{j-3}(k)=c\in\{0,1\}.
\]

Write

\[
a=d_{j-5}(k),\qquad b=d_{j-4}(k).
\]

Then

\[
g_j(k+1)=a\oplus b\oplus c\oplus(b\lor c).
\]

Hence there are exactly two cases.

### Common value 0

If

\[
d_{j-3}=d_{j-2}=0,
\]

then

\[
\boxed{g_j(k+1)=d_{j-5}(k).}
\]

Therefore the agreement survives the next step iff

\[
\boxed{d_{j-5}(k)=0.}
\]

Notably, \(d_{j-4}\) cancels completely.

### Common value 1

If

\[
d_{j-3}=d_{j-2}=1,
\]

then

\[
\boxed{g_j(k+1)=d_{j-5}(k)\oplus d_{j-4}(k)=g_{j-2}(k).}
\]

Therefore the agreement survives the next step iff the next lower adjacent pair also agrees:

\[
\boxed{g_{j-2}(k)=0.}
\]

## Consequence for a long reset gap

A long positive preperiod increment at level \(j\) is a long interval with \(g_j=0\). At every time in that interval, continuation is forced by one of two lower-level certificates:

1. if the common pair \((d_{j-3},d_{j-2})\) is `00`, then the more distant layer \(d_{j-5}\) must be zero at that time;
2. if the common pair is `11`, then the lower agreement indicator \(g_{j-2}\) must itself be zero at that time.

Thus a reset gap cannot propagate without leaving a precise lower-level ancestry condition at every step. In particular, stretches of common `11` recursively force agreement gaps two tower levels lower, while common `00` stretches force zeros in layer \(j-5\).

This is stronger than run 216's statement that the two adjacent layers agree: it identifies the exact condition required for that agreement to persist one more time step.

## What this does not prove

The two continuation mechanisms can alternate in time, and the `00` branch only constrains one lower layer rather than an adjacent pair. Therefore it is not yet justified to claim that a length-\(L\) gap consumes \(L\) disjoint lower-level resources, or that repeated gaps at increasing \(j\) have bounded total length. Such a claim still needs a non-reuse/amortization argument.

## Next target

Trace the two continuation certificates backward through a whole stopping-time window beginning at \(a_{j-1}\). A promising concrete question is whether repeated `11` certificates create a descending staircase \(g_j=g_{j-2}=g_{j-4}=\cdots=0\) whose depth can be charged to tower level, while `00` certificates can be charged to forced zero ancestry without telescoping. The alternation between these two certificate types is the remaining obstacle.
