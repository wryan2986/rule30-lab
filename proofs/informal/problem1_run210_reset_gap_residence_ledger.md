# Problem 1 run 210 — reset-gap residence ledger

Problem 1 remains OPEN.

For fixed finite nonzero `x`, put `q_n=2^n x`, `a_n=tau(q_n)`, and `delta_n=a_n-a_(n-1)`.

Run 209 proves `delta_n>=0`. From the run-207 defect automaton, `delta_n=0` when the lifted defect phase is matched. When it is mismatched, `delta_n=rho_n`, the number of transitions from cycle entry of `q_(n-1)` through the first reset transition.

The reset symbols are exactly low-bit pairs `10` and `11`, hence a transition resets exactly when the current lower-cycle state has least-significant bit 1. Therefore, in the mismatch case, `rho_n-1` is exactly the initial run length of least-significant-bit zeros on the eventual cycle, starting at cycle entry.

The residence ledger charge is `delta_n-1`. Thus pointwise:

    delta_n-1 = -1       for a matched lift;
    delta_n-1 = rho_n-1  for a mismatched lift.

So every positive ledger contribution is exactly an initial low-bit zero-run length on the eventual A-cycle one tower level below. Over any tower interval,

    sum(delta_n-1)

is exactly the sum of these zero-run lengths over mismatches minus the number of matched lifts.

Beyond the finite original fringe, run 202 identifies front thresholds with `a_n=tau(2^n x)`. Hence for `e_n=a_n-n`, each matched lift changes `e` by `-1`, while each mismatched lift changes it by `rho_n-1`.

This gives a precise remaining scalar obstruction: can one fixed finite origin `x` have cycle-entry mismatches whose initial low-bit zero-runs supply unbounded cumulative surplus over intervening matched lifts?

This is not yet a bounded-reuse theorem. In particular, reset gaps must not be counted as independent births or disjoint original-support resources. A useful next lemma must control reuse of long low-bit zero-runs across the common-origin tower, mismatch frequency, or a genuinely non-telescoping ancestry charge attached to reset gaps.
