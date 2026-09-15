# Astra automation handoff — run 43 — 2026-09-15

## Branch state

Research branch: `research/astra-next`.

Run 42 ended at `477d9991a3edb7566de27ad8c3b418a908263bc8` and identified cross-doubling dependence as the next target. This run added `proofs/informal/problem1_cross_doubling_budget_target.md` in commit `4d78b7d3dc092ea0fdc2290bb48950af11f4585f`.

## New progress

The cross-doubling finite-entry idea has been reduced to the exact multiplicity statement needed by the already reviewed activity machinery.

For bounded activity `R(x)<=K`, the existing joint-window theorem gives a uniform bound

    sup_n J_n(x) <= max(h_V(K),2g(K)),

where `J_n` counts boundary-pair activity at depth n during the anchored times `0,...,n-1`.

This exposes two weak formulations that are insufficient:

1. assigning every late doubling to a distinct new entry/birth event lacks a theorem pulling the late source back before the finite-entry cutoff;
2. even assigning every doubling injectively to one anchored event at a distinct depth only gives `J_n>=1` at many n, which is compatible with bounded activity.

The bridge actually required is multiplicity: a chain of r doublings on the same common-origin realization must force `J_n >= f(r)` for some depth, with `f(r)->infinity`, or force an analogous accumulation in one joint transport window. This would combine immediately with the reviewed finite-entry bound.

## Problem status

Problem 1 remains OPEN.

## Next target

Search the existing exact gate/source/return formulas for a way to pull several *different* late doubling sources back into one anchored depth window of the original realization. The crucial property is non-reuse plus accumulation at a common depth/window, not merely one distinct event per doubling.

Do not spend another run proving only that doubling sources are distinct or occur at unbounded depths; that is too weak for the existing `J_n` criterion.