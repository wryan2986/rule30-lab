# Problem 1: finite support realizes arbitrary finite right-driver and center prefixes

## Status

Structural lemma / stopping fence. This strengthens the run-147 left-permutive construction by keeping the initial row finite-support.

## Statement

Let Rule 30 be

\[
F(l,c,r)=l\oplus(c\lor r).
\]

Fix a horizon `T >= 0`, a desired center trace

\[
c_0,c_1,\ldots,c_T,
\]

and any prescribed finite right prefix

\[
x_0,x_1,\ldots,x_T
\]

with `x_0=c_0`. Then there exists a finite-support initial configuration realizing both prescriptions: its initial cells at positions `0,...,T` equal the chosen right prefix and its center cells at times `0,...,T` equal `c_0,...,c_T`.

In fact, after setting all initial cells at positions `>T` to zero, there is a unique successive choice of the left cells

\[
x_{-1},x_{-2},\ldots,x_{-T}
\]

that realizes the center trace through time `T`; setting all cells `<-T` to zero then gives finite support.

## Proof

The value at the center at time `t` depends only on initial positions `[-t,t]`. Hence cells outside `[-T,T]` are irrelevant through time `T` and may be set to zero.

Proceed inductively in `t`. Suppose `x_{-1},...,x_{-(t-1)}` have already been chosen so that the desired center values hold through time `t-1`. At time `t`, the only as-yet-unfixed source cell in the center's depth-`t` cone is the extreme-left cell `x_{-t}`. Along the extreme-left characteristic from `(-t,0)` to `(0,t)`, each local Rule-30 update uses that characteristic value as the left input. Rule 30 is left-permutive: for fixed `(c,r)`,

\[
l\mapsto F(l,c,r)=l\oplus(c\lor r)
\]

is a bijection of `{0,1}`. Composition along the characteristic therefore makes the time-`t` center value a bijective (indeed affine) function of `x_{-t}` once all other source cells in the cone are fixed. Exactly one choice of `x_{-t}` produces the prescribed `c_t`.

Induction gives the unique left block through `-T`. Zero extension outside `[-T,T]` is finite-support and cannot change the requested data through time `T`.

## Consequence for FULL

Take the desired center prefix to be the alternating FULL trace and choose an arbitrary binary word on the right through depth `T`. Every such finite right-driver word occurs in some finite-support initial row while the center follows FULL through time `T`.

Therefore **finite support does not rescue any finite-horizon attempt to constrain the right driver from the FULL center trace alone**. At every finite horizon, all `2^T` right-driver prefixes remain realizable by finite-support rows.

This is stronger than the run-147 formulation with an arbitrary right half: the witnesses can already be chosen finite-support. Any successful bounded-state restriction must use conditions not implied merely by a finite FULL center prefix plus finite support—for example the cyclic source/gate/sensitive-return structure, or a genuinely all-time consequence of eventual FULL.

## Research implication

Do not spend further runs testing whether a long but finite alternating center prefix, together with finite support, eventually narrows the finite right-driver prefix. It cannot. The remaining quotient route must explicitly incorporate the cyclic/gate return-birth conditions (or another all-time invariant), because every finite local driver word survives the weaker constraints.
