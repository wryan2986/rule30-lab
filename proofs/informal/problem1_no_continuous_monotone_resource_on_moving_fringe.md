# No continuous monotone resource exists on the instantaneous moving fringe

Status: `proved` as a topological consequence of the previously proved pro-2 recurrence of the moving-right-fringe dynamics. This is a stopping-fence result, not a proof of Problem 1.

## Statement

Let `X={0,1}^N` be the infinite moving-right-fringe state space and let `F:X->X` be its Rule 30 moving-edge update. Import the established result from `problem1_infinite_moving_fringe_has_pro2_recurrence.md`: there is a sequence of positive powers of two `N_J` tending to infinity such that

    F^(N_J) -> id

uniformly on every fixed finite prefix (equivalently, in the product topology).

Let `V:X->R` be continuous. If

    V(Fx) <= V(x)                                      (1)

for every `x in X`, then in fact

    V(Fx) = V(x)                                       (2)

for every `x in X`.

The same conclusion holds for any continuous map into a finite totally ordered set, or more generally whenever continuity makes `V(F^(N_J)x)->V(x)` and the target order is closed.

## Proof

Fix `x`. From (1), iteration gives the nonincreasing sequence

    V(x) >= V(Fx) >= V(F^2 x) >= ... .                (3)

Pro-2 recurrence gives `F^(N_J)x -> x`. Continuity therefore gives

    V(F^(N_J)x) -> V(x).                               (4)

If there were some `k>=1` with `V(F^k x)<V(x)`, then (3) would imply

    V(F^n x) <= V(F^k x) < V(x)

for every `n>=k`, contradicting (4) along all sufficiently large `N_J`. Hence no strict decrease can ever occur, and in particular `V(Fx)=V(x)`.

This is pointwise and requires no compactness argument beyond the already established recurrence; for real-valued `V`, ordinary continuity suffices.

## Consequence for the finite-support budget program

Runs 108--110 asked whether the repeatedly reused terminal fringe could carry a nonrenewable resource, and run 110 ruled out an acyclic resource living in a fixed finite prefix. Runs 111--113 strengthened the finite-prefix recurrence to a pro-2 recurrence and dyadic finite-factor theorem.

The present lemma closes a broader loophole: enlarging the resource from a finite phase label to a continuous real-valued potential on the *entire instantaneous infinite moving fringe* does not help. There is no continuous Lyapunov function that is globally nonincreasing under the moving-fringe update and strictly decreases at a birth, repair, nonreset passage, or any other event that is recognized solely through the instantaneous fringe dynamics. Global monotonicity plus fringe recurrence forces exact conservation.

Therefore a proposed nonrenewable budget for the infinitely required births must violate at least one of these hypotheses. It must use information not contained continuously in the instantaneous moving fringe (for example source/history identity, core/global-shadow coupling, or an anchored quantity depending on unbounded past), or its monotonicity must hold only on a special FULL-survivor subset whose recurrence properties are separately broken by the additional constraints.

The last caveat matters: this lemma does **not** prove that a survivor-restricted resource is impossible. A FULL-compatible invariant could import core/history information and thereby evade the autonomous fringe recurrence. The result only prevents treating the moving fringe itself as a consumable reservoir, even with an infinite-window continuous potential.

## Admission test for future candidates

For any proposed birth budget `V`, ask:

1. Is `V` determined continuously by the instantaneous moving-right fringe alone?
2. Is `V` nonincreasing under every fringe update in its claimed domain?
3. Is some required regenerative event supposed to make `V` strictly decrease?

If all three are asserted on the full moving-fringe state space, the proposal is impossible by the theorem above. To remain viable, the proof must identify the extra FULL/core/history condition that destroys one of those premises rather than merely choosing a larger fringe window.

Problem 1 remains OPEN.
