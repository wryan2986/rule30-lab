# Astra automation handoff — 2026-09-14 run 20

Branch: `research/astra-next`

## Repository state reviewed

Run started from handoff commit `38b7a95768ceaff84204da9117bbe4f22254389e` (run 19). No newer branch work was present.

The active target was to augment the scalar p-step return defect

\[
E_p(x)=A^p(x)\oplus x
\]

with enough source/phase information to evolve it under one physical Rule-30 step.

## New result

Added:

`proofs/informal/problem1_two_bit_commutator_automaton_and_reentry_classifier.md`

commit `b8e464180213fbd0e19eba4661aa58c36fe7c276`.

### Exact four-state commutator automaton

Let

\[
u_j=A^j(x),\qquad v_j=A^j(Tx),\qquad d_j=v_j\oplus T(u_j).
\]

Then `d_0=0` and, for every j,

\[
\boxed{d_j<4}.
\]

Writing \(s_j=T(u_j)\),

\[
\boxed{
 d_{j+1}=F(d_j,s_j\bmod16)
}
\]

where

\[
F(d,s)=A(s\oplus d)\oplus A(s)\oplus c(s)
\]

and

\[
c(s)=(s_0\lor s_1)+2(s_1\land\neg s_2).
\]

Thus the entire noncommutation memory is only two bits; the automaton is driven by the low-four-bit source sequence along the normalized p-orbit.

At the end of the p steps,

\[
\boxed{
E_p(Tx)=T(x\oplus E_p(x))\oplus T(x)\oplus d_p.
}
\]

### Exact immediate-reentry classifiers

If \(E_p(x)=1\), then

\[
\boxed{
E_p(Tx)=0
\iff
x_1=1\text{ and }d_p=3.
}
\]

If \(E_p(x)=3\), then

\[
\boxed{
E_p(Tx)=0
\iff
x_2=1,\ x_0\oplus x_1=1,\ d_p=1.
}
\]

These conditions exactly separate the known period-4 immediate-reentry examples from the period-2 non-reentry examples.

## What this resolves

The run-19 proposed augmented-state direction is viable: the commutator correction does not grow spatially. The missing memory can be compressed to a four-state automaton once the source word is supplied.

However, the source driver has length p, so this is not yet a finite state space independent of p.

## Best next target

Specialize the source word

\[
T(A^j x)\bmod16,\qquad 0\le j<p,
\]

to actual return-fringe collision states. Determine whether corridor/common-origin geometry forces or strongly restricts the terminal automaton state \(d_p\). In particular, seek a formula for \(d_p\) from the fringe boundary bits or a short suffix of the p-cycle, rather than the full source word.

If such compression exists, repeated long corridors may finally be coupled through a genuinely bounded augmented state. If not, record a counterexample showing that arbitrarily long source history is necessary.

## Status

Problem 1 remains open. This run produced an exact finite-state commutator transport theorem and exact classifiers for both allowed boundary-defect re-entry cases.
