# Problem 1 run 223 — exact near-edge diagonal automaton

Problem 1 remains open.

## Setup

Continue the common-origin adjacent-defect hierarchy from runs 215–222. For the interior levels,

\[
d_j(k+1)=d_{j-2}(k)\oplus(d_{j-1}(k)\lor d_j(k)).
\]

Run 221 proved the finite-speed cone

\[
d_j(k)=0\qquad(j>2k),
\]

and run 222 proved its sharp outer characteristic

\[
d_{2k}(k)=x_0.
\]

Define the depth-\(r\) diagonal behind that characteristic by

\[
E_r(k):=d_{2k-r}(k),
\]

whenever \(0\le r\le 2k\).

## Exact diagonal recurrence

For every fixed \(r\ge2\), once the indicated defect levels are in the interior recurrence range,

\[
\boxed{E_r(k+1)=E_r(k)\oplus(E_{r-1}(k)\lor E_{r-2}(k)).}
\]

Indeed,

\[
\begin{aligned}
E_r(k+1)
 &=d_{2k+2-r}(k+1)\\
 &=d_{2k-r}(k)\oplus
   \bigl(d_{2k+1-r}(k)\lor d_{2k+2-r}(k)\bigr)\\
 &=E_r(k)\oplus(E_{r-1}(k)\lor E_{r-2}(k)).
\end{aligned}
\]

At the outer two diagonals, finite speed supplies the missing outside-cone terms and gives

\[
\boxed{E_0(k+1)=E_0(k)=x_0,}
\]

and

\[
\boxed{E_1(k+1)=E_1(k)\oplus E_0(k).}
\]

Thus, after a finite width \(R\) has been born (take \(k\) large enough that all \(E_0,\dots,E_R\) are defined and the interior formula applies), the vector

\[
V_R(k)=(E_0(k),E_1(k),\dots,E_R(k))
\]

evolves autonomously by the triangular Boolean map

\[
T_R:
\begin{cases}
E'_0=E_0,\\
E'_1=E_1\oplus E_0,\\
E'_r=E_r\oplus(E_{r-1}\lor E_{r-2}),&2\le r\le R.
\end{cases}
\]

## Stronger consequence: every fixed edge band is purely periodic

The map \(T_R\) is a bijection of \(\{0,1\}^{R+1}\).

Proof: recover coordinates successively. First \(E_0=E'_0\). Then

\[
E_1=E'_1\oplus E_0.
\]

Having recovered \(E_0,\dots,E_{r-1}\), recover

\[
E_r=E'_r\oplus(E_{r-1}\lor E_{r-2}).
\]

Therefore \(T_R\) is invertible. Since its state space is finite, every orbit is periodic (there are no nontrivial transient tails once the band is fully present).

In particular, for each fixed depth \(r\), the near-edge bit \(E_r(k)\) is periodic in time after the finite birth time of that band. A crude universal period bound is at most \(2^{R+1}\) for the width-\(R\) vector.

## Connection to the stopping frontier

Run 222 defined

\[
\Delta_n=2a_{n-1}-(n+1).
\]

Since the stopping-frontier bit is

\[
F_n=d_{n+1}(a_{n-1}),
\]

we have the exact identity

\[
\boxed{F_n=E_{\Delta_n}(a_{n-1})}
\]

whenever \(\Delta_n\ge0\). If \(\Delta_n<0\), run 221's cone already forces \(F_n=0\).

Hence the moving transient obstruction from run 220 has now been converted into a precise geometric question: how deep, measured by \(\Delta_n\), does the stopping curve penetrate behind the sharp speed-2 characteristic?

If \(\Delta_n\) is uniformly bounded by \(R\) on a constant-period tower epoch, then every possible \(F_n\) is read from the fixed finite invertible automaton \(T_R\), together with the stopping time modulo the period of that automaton. This removes the need to track an ever-growing transient triangle in that case.

If \(\Delta_n\) is unbounded, no fixed near-edge band suffices, and the stopping curve genuinely samples successively deeper defect ancestry.

## What this does and does not prove

This is an all-depth structural result, not a finite computation. It strengthens run 222: not only is the outer characteristic exact, but every fixed-width strip behind it is an autonomous finite invertible dynamical system.

It does **not** prove that \(\Delta_n\) is bounded, nor does it prove Problem 1. The remaining issue is now concentrated in the displacement sequence \(\Delta_n\), rather than in unspecified transient data.

## Next target

Analyze \(\Delta_n=2a_{n-1}-(n+1)\) on constant-period epochs. In particular:

1. derive its exact increment law from \(\delta_n=a_n-a_{n-1}\);
2. test long tower examples (especially \(x=1\)) against constant-period epochs;
3. determine whether bounded period can coexist with unbounded \(\Delta_n\), and if so whether the edge automata still constrain the sampled depths strongly enough to force a contradiction with infinitely many late renewals.