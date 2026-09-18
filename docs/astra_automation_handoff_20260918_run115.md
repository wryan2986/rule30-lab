# Astra automation handoff — run 115 — 2026-09-18

Problem 1 remains OPEN. Continue on `research/astra-next`.

Starting tip was `b01f879185b2f3b1c1c40a8d691c5e660b8600d2`; no intervening work was present.

## New result

Added `proofs/informal/problem1_no_continuous_monotone_resource_on_moving_fringe.md`.

Using the already proved pro-2 recurrence `F^(N_J) -> id` of the infinite moving-right-fringe update, any continuous real-valued `V` satisfying `V(Fx)<=V(x)` for every fringe state must actually satisfy `V(Fx)=V(x)` everywhere. Proof: values along an orbit are nonincreasing, while the dyadic return subsequence converges back to the starting state and hence, by continuity, back to the starting value. Any strict decrease would persist along the tail and contradict that return.

This strengthens the finite-prefix no-go results: not only finite phase labels, but even continuous real-valued potentials on the entire instantaneous infinite moving fringe cannot serve as globally consumable birth resources. A viable nonrenewable budget must import non-fringe information (core/global shadow, source/history identity, unbounded past), be discontinuous in the instantaneous fringe topology, or rely on a special FULL-survivor restriction whose additional structure invalidates global fringe recurrence/monotonicity.

## Stopping fence

Do not search for a Lyapunov/resource function determined continuously by the instantaneous moving fringe alone and globally nonincreasing under its autonomous update. Pro-2 recurrence forces every such quantity to be conserved.

The principal unresolved target remains a genuinely survivor-specific finite-support upper bound on the infinitely required cyclic births, likely using core/history/global-shadow coupling rather than the autonomous moving fringe.

Research commit: `194cefb55ddb9d8152a0314a761f47d5eb72e4d5`.
