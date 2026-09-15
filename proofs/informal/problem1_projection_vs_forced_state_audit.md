# Problem 1: exact projection versus forced/reset state audit

## Status

This note follows the exact projection identity

\[
A^t(x)\gg k=A^t(x\gg k)
\]

and audits where it can legitimately be applied in the reset/scan argument.

## Exact projections need no transport lemma

For the accelerated Rule 30 map

\[
(Ax)_i=x_{i+2}\oplus(x_{i+1}\lor x_i),
\]

right shift is an exact factor map:

\[
A(x)\gg k=A(x\gg k),
\]

hence by induction

\[
A^t(x)\gg k=A^t(x\gg k).
\]

Thus if a finite periodic state used at a doubling passage is literally a high-bit projection of the original realization at some time,

\[
y=A^\tau(x)\gg k,
\]

then every temporal coordinate history of `y` is already a literal spacetime column of the original realization. In particular an antiperiodic doubling fiber

\[
b(t+p)=1\oplus b(t)
\]

requires no separate causal pullback.

## The reset/forced construction is different

The existing reset-bit scan does not in general identify its periodic comparison state with an exact projection of the original orbit. The scan introduces a boundary/reset prescription in order to obtain a finite autonomous state/cycle. That modification is precisely what makes the local finite-state period analysis possible.

Therefore the implication

\[
\text{doubling in the forced/reset scan}
\Longrightarrow
\text{literal antiperiodic column in the original realization}
\]

is not justified merely by shift-equivariance of `A`.

The projection identity only removes the transport problem for portions of the state lying outside the support/influence of the forcing. The remaining issue is to prove that the coordinate carrying the doubling fiber is unaffected by the reset prescription for the entire time interval needed to certify

\[
b(t+p)=1\oplus b(t).
\]

## Finite-speed criterion

Because one step of `A` at coordinate `i` depends only on coordinates `i,i+1,i+2`, a perturbation of a low/boundary coordinate can influence only coordinates moving toward lower indices under forward iteration; equivalently, for a coordinate at distance `d` from the forcing boundary, agreement with the unforced projection is guaranteed only for a finite cone whose duration is controlled by `d`.

Hence a sufficient bridge for a doubling of parent period `p` is:

> the doubling-fiber coordinate is separated from the reset/forcing support by enough spatial margin that the forced and unforced evolutions agree at that coordinate for at least `2p` consecutive times.

Under that condition the full antiperiodic certificate is inherited verbatim by the original realization.

This criterion is stronger than agreement at the source time. A one-time equality of forced and unforced states does not preserve a period certificate, because the reset can enter the coordinate's causal cone before time `2p`.

## Consequence for the current route

The live quantitative question is now a cone-width comparison:

\[
\boxed{\text{distance from doubling fiber to reset support}\ \stackrel{?}{\ge}\ 2p\text{-step influence width}.}
\]

If the existing gate/source formulas imply such a margin for infinitely many late doublings, run 47's density budget can be applied directly to genuine columns of the original spacetime diagram.

If they do not, then the projection-history route stalls for a precise reason: the reset boundary can contaminate the fiber before one complete doubled cycle has been observed.

## Dead ends to avoid

1. Do not treat a reset/forced scan cycle as automatically equal to `A^tau(x) >> k`.
2. Do not infer an original antiperiodic history from equality at a single time slice.
3. Do not use the exact projection identity across a boundary operation; first isolate the forcing support and its forward causal cone.
4. The next useful computation is not another period census. It is the exact spatial location of the doubling fiber relative to the reset bit/source and the corresponding cone width over `2p` steps.
