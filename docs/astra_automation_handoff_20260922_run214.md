# Astra automation handoff — run 214

Problem 1 remains OPEN.

## Repository state entering run

No intervening work after run 213; branch tip was `54611369da947334f91397ea9b21bf408319cb0b`.

## New result / dead end

The run-213 proposal to amortize preperiod gains against period behavior is too coarse.

Combining the exact laws gives the valid implication

    delta_n = a_n-a_{n-1} > 0  ==>  P_n=P_{n-1},

because positive delta_n requires a reset on the lower eventual cycle, while period doubling is possible only when that lower cycle has no reset.

But period preservation does not distinguish matched lifts (delta_n=0) from mismatched lifts (delta_n=rho_n>0), so the period sequence supplies no direct budget on positive residence gains.

Exact diagnostic for x=1 through n=300 reinforces this obstruction: the period reaches 8 at n=29 and never changes again in the tested range, while positive preperiod increments continue frequently. At n=300, tau(2^300)=389 and tau(2^300)-300=89; the surplus reaches at least 95 at n=290.

Full note: `proofs/informal/problem1_run214_period_preperiod_coupling_dead_end.md`.

## Next target

Do not try to charge reset-gap gains merely against period doublings. The next useful object must retain cycle-entry phase information. Derive a cross-level recurrence for the mismatch indicator / cycle-entry defect phase using the exact shift-factor tower and n-bit fiber recurrence from runs 211–212. The needed common-origin restriction must distinguish matched from mismatched period-preserving lifts.
