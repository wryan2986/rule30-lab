# Problem 1 — run 218: reset-gap period bound and isolated period doublings

Problem 1 remains OPEN.

## Setup

Write

\[
q_n=2^n x,\qquad a_n=\tau(q_n),\qquad P_n=\pi(q_n).
\]

Runs 208–210 established the exact adjacent preperiod increment law: a positive increment

\[
\delta_n=a_n-a_{n-1}>0
\]

is a phase-mismatched one-bit lift, and then

\[
\delta_n=\rho_n,
\]

where \(\rho_n\) is the distance, measured along the eventual cycle of \(q_{n-1}\) from the relevant cycle-entry phase, to the first reset (the first state with LSB 1).

Run 213 established the adjacent period law

\[
P_n\in\{P_{n-1},2P_{n-1}\},
\]

with doubling possible only when the lower eventual cycle contains no reset at all.

## Lemma 1: every positive increment is bounded by the lower period

If \(\delta_n>0\), a reset exists on the eventual cycle of \(q_{n-1}\). That cycle has minimal period \(P_{n-1}\). Starting from any phase on a periodic orbit containing at least one reset, the first reset is encountered within one traversal of the cycle. Therefore

\[
\boxed{1\le \delta_n=\rho_n\le P_{n-1}.}
\]

This is exact and requires no additional ancestry argument.

Equivalently, the residence variable \(e_n=a_n-n\) satisfies

\[
e_n-e_{n-1}=\delta_n-1\le P_{n-1}-1
\]

on a positive-increment level, while a matched lift gives \(e_n-e_{n-1}=-1\).

This does not by itself solve Problem 1 because the periods may grow with tower level.

## Lemma 2: period doublings cannot occur at consecutive tower levels

Assume

\[
P_n=2P_{n-1}.
\]

By the run-213 criterion, the lower cycle has no reset, so over one lower period the defect monodromy is a toggle (odd parity of the `01` events). Hence the lifted defect bit changes value after one block of length \(P_{n-1}\), and returns after the second block.

The defect bit is exactly the least-significant bit of the lifted state \(q_n\). Therefore the eventual \(2P_{n-1}\)-cycle of \(q_n\) contains both defect values 0 and 1, in particular at least one state with LSB 1.

Thus the next lift, from \(q_n\) to \(q_{n+1}\), has a reset on its lower cycle. By run 213, a lift whose lower cycle has a reset cannot double its period. Hence

\[
\boxed{P_n=2P_{n-1}\implies P_{n+1}=P_n.}
\]

So period-doubling levels are isolated: no two consecutive adjacent lifts can double.

## Combined consequence

The only source of an increment larger than 1 is a reset-containing, therefore period-preserving, level, and its size is bounded by the current lower period. Period growth occurs only on reset-free levels, and those growth events cannot be consecutive.

This gives a clean coarse envelope:

- positive preperiod gains satisfy \(\delta_n\le P_{n-1}\);
- a period-doubling level has \(\delta_n=0\) (indeed no reset exists, so the mismatch-with-reset mechanism is unavailable);
- after every period doubling there is at least one period-preserving level.

However, this still does not yield a sufficient amortized bound. Isolated doublings could in principle occur infinitely often, causing \(P_n\) to grow without bound, and long stretches of period-preserving levels can continue to contribute positive increments bounded only by that current period.

## Computational diagnostic for x=1

As a finite diagnostic only, exact orbit computation for the canonical tower \(q_n=2^n\) through \(n=1000\) gives period doublings at

\[
n=3,8,29,400,
\]

so \(P_{1000}=16\). The largest adjacent preperiod increment observed through \(n=1000\) is 13 (at \(n=660\)), consistent with the proved bound \(\delta_n\le P_{n-1}=16\) there. Also

\[
\tau(2^{1000})=1275,
\]

so the residence surplus \(\tau(2^{1000})-1000=275\) remains substantial despite the very sparse period doublings.

These finite observations are not used in either proof.

## Strategic consequence / next target

The run-217 certificate ancestry remains relevant, but any attempted non-reuse theorem should exploit the new finite-period ceiling: within a fixed-period epoch, every positive reset gap has length at most that period. The remaining issue is therefore not arbitrarily long individual gaps at fixed period; it is whether sufficiently many bounded gaps can accumulate before the next isolated period doubling.

A sharper next target is to bound the cumulative positive residence gain over a maximal constant-period epoch, preferably in terms of the period itself and the defect-cycle phase structure. If such an epoch bound were sublinear in tower-level duration, or if period doublings themselves could be globally bounded for a fixed finite origin, the FULL obstruction would materially tighten.
