# Astra automation handoff — 2026-09-20 run153

Problem 1 remains OPEN.

## New result

Run153 sharpened run152's hidden-slack bookkeeping for the TWO-BIT nonreset passage.

Run152 gives exact original-cut excesses

    e_(t+2)=0, e_(t+6)=1,

hence

    s_(t+2)=t+2, s_(t+6)=t+7.

For

    d_k=s_(t+k+1)-s_(t+k), k=2,3,4,5,

monotonicity gives `d_k>=0` and the endpoints give

    d_2+d_3+d_4+d_5=5.

The three interior zero rows imply

    d_2<=1,
    d_2+d_3<=2,
    d_2+d_3+d_4<=3.

If `g=g_(t+5)` is the hidden slack immediately before the forced birth, then exactly

    g=3-(d_2+d_3+d_4),
    d_5=g+2.

Thus every unit of terminal hidden slack is repaid immediately as one extra unit of original-cut jump at the forced birth. The terminal jump is in `{2,3,4,5}`. Physical `beta=1` does not distinguish these possibilities.

The scalar information is sharp: all `g=0,1,2,3` have ledger-compatible nonnegative increment patterns satisfying the zero-row inequalities. This does NOT claim all occur on FULL Rule-30 orbits; it proves that physical delay profile + endpoint positivity + monotonicity alone cannot improve run152's slack bound.

Full note: `proofs/informal/problem1_run153_zero_plateau_slack_exact_repayment.md`.

## Next target

Use complete cyclic/gate/global-shadow structure at the forced birth to bound the original-cut jump

    s_(t+6)-s_(t+5).

On this passage that is exactly equivalent to bounding terminal hidden slack, via `jump=g+2`. If the complete driver forces jump 2, then `g_(t+5)=0`. If jumps 3--5 remain possible under the full admissibility conditions, record that as a stopping fence and move to a genuinely non-telescoping global charge.
