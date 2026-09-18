# Problem 1: finite instantaneous fringe factors have only dyadic cycles

Status: proved structural consequence; Problem 1 remains open.

## Setup

Use the moving-right-fringe coordinates

\[
a_j(t)=(T^t r)_{R+t-j},\qquad j\ge 0,
\]

for a finite initial row with right endpoint `R`. Earlier notes established that each finite prefix

\[
A_J(t)=(a_0(t),\ldots,a_J(t))
\]

evolves autonomously by the triangular Rule-30 map

\[
a_j(t+1)=a_j(t)\oplus(a_{j-1}(t)\lor a_{j-2}(t)),
\]

with `a_{-1}=a_{-2}=0`, and that the finite-prefix update is a permutation of 2-power order. The infinite moving-fringe action is therefore pro-2 recurrent.

## New strengthening: every finite continuous factor has only 2-power cycles

Let

\[
\Phi:\{0,1\}^{\mathbb N}\to S
\]

be any continuous map to a finite discrete set `S`. Suppose it is a genuine dynamical factor of the instantaneous moving fringe: there is a map `G:S->S` such that

\[
\Phi(Fx)=G(\Phi(x))
\]

for every fringe state `x` under the moving-fringe update `F`.

Because the Cantor product space is compact and `S` is finite discrete, continuity implies that `Phi` depends on only finitely many coordinates. Thus for some `J`, `Phi` factors through the prefix projection `pi_J`.

The prefix update `F_J` has order `2^m` for some `m`. Hence

\[
\Phi(F^{2^m}x)=\Phi(x).
\]

Using the factor identity gives

\[
G^{2^m}(\Phi(x))=\Phi(x).
\]

Therefore every cycle of `G` that is actually reached from a fringe state has length dividing `2^m`. In particular:

> **Finite-factor dyadic-cycle theorem.** Every finite-valued continuous dynamical factor of the instantaneous moving-right fringe has only power-of-two cycle lengths on its reachable states.

This is stronger than saying that each finite prefix itself has dyadic period: arbitrary finite deterministic summaries/quotients of the instantaneous fringe inherit the same restriction.

## Odd-period corollary

Suppose a finite-valued continuous fringe observable is both a dynamical factor and, on some orbit, is claimed to have period dividing an odd integer `p`. Its actual period divides both `p` and a power of two, so it must have period one.

Equivalently, a nonconstant finite fringe factor cannot carry a genuine odd-order clock. More generally, any proposed finite phase system with a reachable cycle containing an odd prime factor cannot be realized from the instantaneous moving fringe alone.

## Why this matters for the remaining route

The previous run suggested seeking a non-dyadic obstruction coupling FULL/nonreset phase information to the dyadic fringe recurrence. This note makes that target precise.

It is **not** enough to name a 3-phase/odd-phase bookkeeping convention: to obtain a contradiction one must prove all three of the following.

1. The phase is determined continuously by the instantaneous moving fringe (hence by some finite prefix).
2. The phase transport is deterministic, so it is a dynamical factor of the fringe update.
3. An actual FULL survivor forces a nonconstant reachable cycle with an odd factor in its period.

If those hold, the dyadic-cycle theorem immediately contradicts the odd phase cycle. If the phase instead depends on source identity, elapsed history, hidden slack, or core/global-shadow information, then it is not a finite instantaneous fringe factor and this theorem does not apply—which is exactly where genuinely new information can enter.

## Stopping fence

Any finite-state invariant, automaton, phase label, or resource state computed solely and continuously from the instantaneous moving-right fringe has only dyadic recurrent dynamics. Enlarging the fringe window or quotienting it into a more elaborate finite automaton cannot create an odd-order obstruction.

Thus a productive next check is very concrete: inspect the existing FULL/nonreset source-phase machinery for a rigorously forced nonconstant odd-order cycle, and audit whether that phase is actually determined by the instantaneous fringe. A positive result would give a direct contradiction; a failure identifies precisely which extra history/core datum prevents the argument.
