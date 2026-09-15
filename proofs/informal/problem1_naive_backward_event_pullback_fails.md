# Problem 1: naive backward event pullback fails

## Context

Run 43 sharpened the global FULL obstruction to a multiplicity statement: infinitely many actual period doublings must somehow force an unbounded anchored count `J_n`, or an equivalent common joint-window count. A tempting route is to take each late doubling-source boundary event and pull it backward along the same depth until it enters the anchored interval.

That route is false without additional structure.

## Exact local obstruction

For the accelerated Rule-30 map used throughout the Problem 1 work,

\[
(Ax)_i=x_{i+2}\oplus(x_{i+1}\lor x_i).
\]

Suppose the boundary pair at coordinates `i,i+1` is zero at time `t`:

\[
x_i=x_{i+1}=0.
\]

This does **not** imply that the same boundary pair is zero one step later. Indeed, choose

\[
x_{i+2}=1.
\]

Then

\[
(Ax)_i=1\oplus(0\lor0)=1.
\]

Thus a boundary hit can be born from a `001` local pattern even though the immediately preceding same-coordinate boundary pair contributed no hit.

Equivalently, the indicator

\[
B_i(t)=[x_i(t)\lor x_{i+1}(t)]
\]

has no backward monotonicity of the form

\[
B_i(t+1)=1\Longrightarrow B_i(t)=1.
\]

The failure is intrinsic to the local rule, not an artifact of the global finite-state construction.

## Consequence for the cross-doubling target

A late doubling-source event therefore cannot simply be traced backward at fixed spatial depth and charged to an earlier anchored event. Any successful many-to-one-depth theorem must use more than the fact that the late boundary indicator is nonzero.

In particular, the following proof templates are invalid:

1. `late source at depth n => some earlier hit at the same depth`, by repeated same-coordinate backward implication;
2. `r distinct late sources => r distinct anchored hits`, unless an independent injection/transport theorem is supplied;
3. treating the anchored count `J_n` as if boundary activity persisted backward in time.

The existing joint-window/transport machinery remains the plausible place to obtain the missing extra structure, because it can retain a spacetime neighborhood rather than only a one-bit boundary indicator.

## Sharpened next target

The desired statement must transport a **structured source certificate** (gate/return/birth configuration, or a whole local joint window), not a naked boundary hit. One should look for a property `Q` attached to each doubling passage such that:

- `Q` is forced by the exact doubling-source formulas;
- `Q` has a valid causal transport or pullback law on the same common-origin realization;
- distinct doubling passages yield distinct transported certificates; and
- after transporting `r` passages into one common depth/window, the certificates force at least `f(r) -> infinity` boundary hits there.

This is stronger than run 43's abstract multiplicity target but avoids a now-explicitly-false local monotonicity shortcut.

## Status

This does not solve Problem 1. It removes a natural but invalid route and narrows the next calculation to the full gate/source/return certificate rather than the scalar boundary indicator.