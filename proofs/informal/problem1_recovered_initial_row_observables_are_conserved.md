# Problem 1: observables of the recovered initial row are conserved

## Status

All-depth structural lemma / stopping fence. Problem 1 remains open.

## Context

Run 124 proved that Rule 30 is injective on finite-support configurations. The handoff suggested looking for an order or filtration on recoverable original-row information whose index advances across resetting and nonresetting passages.

There is an immediate obstruction to the literal version of that proposal: if the proposed quantity is a function only of the recovered time-zero row, it is exactly conserved.

## Setup

Let `T` denote the global Rule-30 map restricted to finite-support configurations. Run 124 proved that `T` is injective on this class. Hence, for every `t >= 0`, `T^t` is injective and has a well-defined inverse on its image.

Fix a finite-support initial row `x`. Write

`x_t = T^t(x)`.

Define the time-zero reconstruction map on the time-`t` image by

`R_t(x_t) = (T^t|_{Fin})^{-1}(x_t)`.

Then by definition

`R_t(x_t) = x`

for every `t`.

## Lemma

Let `Phi` be any function whatsoever on finite-support initial rows (no continuity, locality, computability, or finiteness assumption is needed). Define the recovered-initial-row observable along the orbit by

`V_t = Phi(R_t(x_t))`.

Then

`V_t = Phi(x)`

for every `t >= 0`. In particular `V_t` cannot strictly increase or decrease at a resetting passage, a nonresetting passage, or a forced birth.

### Proof

Since `x_t=T^t(x)` and `T^t` is injective on finite-support rows, its inverse on the image sends `x_t` uniquely back to `x`. Therefore `R_t(x_t)=x`, so `V_t=Phi(x)` for all `t`. QED.

## Consequence for the birth-budget route

The run-124 phrase "order or filtration on recoverable original-row information" needs an extra ingredient. A filtration that is merely recomputed from the uniquely recovered original row cannot advance: the recovered object is the same object at every time.

Thus a viable finite budget must be **episode-relative** or **time/source-relative**. For example it could pair the fixed original row with a changing source coordinate, a moving cut, a selected subset/interval determined by the current episode, or a map from the current source into labels of the original support. The hard theorem is then not recoverability but monotonicity/bounded reuse of that changing selector.

Formally, a candidate has to look like

`V_t = Psi(x, episode_t)`

(or an equivalent current-row definition), not merely `Phi(x)`. To obtain a finite birth bound one still needs to prove that the episode-dependent selector crosses/consumes only finitely many labels, or charges each original-support label only boundedly many times.

## Relation to earlier stopping fences

This is distinct from the run-122 ancestry obstruction. Run 122 showed that one original actual 1 can have descendants forever, so ancestry does not imply consumption. The present lemma says something even more basic about the run-124 reconstruction idea: exact recovery of the initial row supplies information, but **no dynamics at all** to any observable that depends only on that recovered row.

It is also compatible with global injectivity: the full current row retains all original information, while a useful proof resource would have to be a deliberately coarse, episode-dependent projection whose transition law is one-way.

## Next target

Do not search for a monotone quantity of the recovered time-zero row alone. Search for a canonical episode-dependent selector on the fixed finite original support and prove a transition law across the exact resetting/nonresetting passages. A minimal useful theorem would be: every forced two-bit nonreset birth advances a selected original-support index, while resetting passages never decrease it. Since the original support index set is finite, that would yield the missing birth budget.
