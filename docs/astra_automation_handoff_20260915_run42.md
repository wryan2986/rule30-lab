# Astra automation handoff — 2026-09-15 run 42

## Branch state entering run

`research/astra-next` was still at run 41 (`5b1695616eef55056e1f9cfb6c14738dbd3e4a83`). Run 41 proved that every finite `A`-cycle has power-of-two exact period and suggested combining that theorem with the older FULL/common-origin/finite-entry machinery.

## Work this run

I audited that proposed bridge against the older accepted scan results. The key conclusion is negative but important: **the new dyadic-period theorem does not further restrict the period evolution of the actual FULL candidate.**

`problem1_scan_doubling_cycle_lag.md` already proves, for one fixed nonzero finite-entry input with its actual finite fringe, that the eventual scan periods satisfy `p_m -> infinity`. The reset theorem already gives exactly

    p_(m+1) in {p_m, 2 p_m},

hence infinitely many actual doubling indices. Under FULL, every such doubling is already charged to a late source diagonal.

So period arithmetic is exhausted on this route: run 41 globally classifies arbitrary finite cycles, but the relevant common-origin scan orbit was already known to have only preserve/double transitions.

I also checked the existing bounded-lag construction. It shows that arbitrarily large doubling-source periods can coexist with source/successor preperiods bounded by 4/2 under the tested local hypotheses. Thus `large dyadic period => large local lag` cannot be the missing resource theorem without using additional global/common-origin information.

Full audit:

`proofs/informal/problem1_dyadic_period_global_bridge_audit.md`

Research commit:

`f6eb22f1f59815f8e7fe202d0fce4d4958ee25a9`

## Problem 1 status

Still open.

The sharpened blocker is now: on one fixed FULL finite-entry realization, infinitely many actual period doublings are required. Need a finite-budget quantity tied to the same original/common-origin future that incurs a positive **non-reusable** charge at every, or sufficiently many, doubling indices.

Known failed substitutes:

- period arithmetic alone: already only preserve/double;
- large period forcing large local preperiod/lag: refuted by the bounded-lag family;
- spacing/density alone: earlier separation work permits arbitrarily sparse infinite sources.

The next high-value target is therefore cross-doubling dependence: prove that distinct doubling passages on the same original FULL realization cannot reuse the same finite-entry defect/birth resource, or find a monotone common-origin quantity transported between consecutive doubling indices.

Secondary route remains the primitive terminating-cylinder odd-parity lemma, but uniqueness of the periodic orbit at each bitlength would still need an additional common-origin monotonicity argument before it could close Problem 1.
