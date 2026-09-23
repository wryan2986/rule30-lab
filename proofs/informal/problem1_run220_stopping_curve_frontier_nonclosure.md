# Problem 1 run 220 — stopping-curve state has an exact one-bit moving-frontier obstruction

Problem 1 remains open.

## Setup

Let
\[
q_n=2^n x,\qquad a_n=\tau(q_n),\qquad P_n=\pi(q_n),
\]
and write
\[
A^k(q_n)=2A^k(q_{n-1})+d_n(k),\qquad d_n(k)\in\{0,1\}.
\]
Inside a constant-period epoch, write the common eventual period as P and let D_n be the aligned eventual P-cycle column of d_n, as in run 219.

Define the stopping phase and entry mismatch bit
\[
\theta_n=a_{n-1}\pmod P,\qquad e_n=d_n(a_{n-1}).
\]
Let \(D_n[\theta_n]\) denote the unique periodic defect value at that aligned phase.

## What the obvious finite-state augmentation does determine

The tuple
\[
(D_{n-2},D_{n-1},D_n,\theta_n,e_n)
\]
determines the adjacent preperiod increment \(\delta_n=a_n-a_{n-1}\) exactly.

If \(e_n=D_n[\theta_n]\), the new lift is already phase-matched and \(\delta_n=0\). If the two bits disagree, the one-bit lift theorem says that \(\delta_n\) is the distance from phase \(\theta_n\) to the first reset on the lower periodic driver. That reset pattern is encoded by the aligned lower cycle columns, so \(0<\delta_n\le P\) is determined. Consequently
\[
\theta_{n+1}=\theta_n+\delta_n\pmod P
\]
is also determined.

Thus run 219's missing mismatch decision really can be reduced to one entry bit at the current level.

## Exact transition obstruction

However, this finite tuple does **not** close under \(n\mapsto n+1\).

To decide the next increment we need
\[
e_{n+1}=d_{n+1}(a_n).
\]
Over the interval from \(a_{n-1}\) to \(a_n=a_{n-1}+\delta_n\), the exact defect recurrence
\[
d_{n+1}(k+1)=d_{n-1}(k)\oplus(d_n(k)\lor d_{n+1}(k))
\]
shows that \(e_{n+1}\) is determined by the known lower drivers on that interval **provided one also knows**
\[
\boxed{f_n=d_{n+1}(a_{n-1}).}
\]
But \(f_n\) is a new look-ahead bit one level above the current stopping curve. It is not part of the current entry state \(e_n\), and the eventual cycle column \(D_{n+1}\) does not determine it while level \(n+1\) is still transient.

If we augment the state by \(f_n\), the same issue shifts outward at the next level: advancing again requires \(d_{n+2}(a_n)\). More generally, a fixed-width stopping-curve augmentation leaves a fresh defect bit just beyond its upper frontier.

So the natural candidate
\[
(T_P,\theta_n,e_n)
\]
is not a closed finite-state dynamical system. The precise escaping information is not the cycle phase or the current mismatch bit; it is a **moving one-bit frontier of transient defect ancestry**.

## Consequence

This blocks the simplest completion of the run-219 strategy. Eventual-cycle geometry is finite-state for fixed P, and the current increment is finite-state once one entry bit is supplied, but propagating that entry bit to the next tower level continually exposes one new transient bit.

Any genuine finite-state epoch theorem therefore needs an additional identity that reconstructs the look-ahead frontier bit from bounded lower data, or else a proof that the frontier becomes irrelevant/forced after some bounded depth. Without such an identity, claiming eventual periodicity of the increment sequence from fixed P would be unjustified.

## Next target

Analyze the diagonal/frontier sequence
\[
F_n=d_{n+1}(a_{n-1})
\]
directly. The useful question is whether the Rule-30-form defect recurrence plus the stopping condition forces F_n from bounded cycle data, or whether two realizable common-origin towers can share the same bounded cycle/entry state but have different F_n. A realizable collision of the latter kind would prove that no bounded-state closure of this form can work; a reconstruction law would revive the finite-state epoch strategy.
