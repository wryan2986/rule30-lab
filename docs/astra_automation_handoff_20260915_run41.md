# Astra automation handoff — 2026-09-15 run 41

## Branch state entering run

`research/astra-next` was still at run 40 (`ae8e5cc1a4b748c55f8d810641a5f5d2bf024402`).  Run 40 proved that in a finite exact-period-`p` no-reset cylinder the seed `a=c_1` has minimal temporal period `p`.  The primitive terminating-seed odd-parity lemma remained open.

## New theorem this run

A separate induction through the one-bit factor map proves that **every finite periodic orbit of `A` has power-of-two exact period**.

The key identity is

`A(x) >> 1 = A(x >> 1)`.

If an `n`-bit orbit has exact period `p` and its `(n-1)`-bit projection has exact period `q`, then `q|p`.  Over one parent period the omitted low bit experiences a deterministic return map `F:{0,1}->{0,1}`.  Any periodic orbit of a self-map of two points has length only 1 or 2, so

`p/q in {1,2}`.

Starting from period 1 at one bit, induction gives `p=2^k` for every finite periodic point.

Full proof:

`proofs/informal/problem1_all_finite_cycle_periods_are_powers_of_two.md`

Research commit:

`9eefc9d2aeeea1e74d407b217583ae9603d6c0e5`

## Why this matters

The period-spectrum observation from run 36 is now rigorous globally.  Exact periods 3,5,6,7 (and every other non-power-of-two period) are impossible for finite `A`-cycles.

The run-38--40 primitive-cylinder parity obstruction is therefore **not required** to prove dyadic periods.  It remains relevant to the stronger conjecture that each bitlength contains exactly one periodic orbit: in the no-reset case, even return parity would give the identity fiber return map and split one parent orbit into two children of unchanged period.

## Problem 1 status

Still open.

The local collision/repair work has already shown that indefinite residence at one fixed period is impossible.  This run now restricts any exact-period changes to a dyadic hierarchy: a genuine increase can only be a doubling.

The most globally relevant next target is to combine this with the older FULL/common-origin/finite-entry accounting.  A useful theorem would show that a hypothetical finite survivor cannot undergo infinitely many period doublings, or that each doubling consumes a quantitatively identifiable amount of the finite common-origin structure.

A secondary clean target remains the primitive terminating-cylinder parity theorem from runs 39--40; proving it would establish uniqueness of the periodic orbit at each bitlength and identify exactly when the dyadic period doubles.
