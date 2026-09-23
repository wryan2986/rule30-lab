# Astra automation handoff — run 218

Problem 1 remains OPEN.

## New exact results

For \(q_n=2^n x\), \(a_n=\tau(q_n)\), and \(P_n=\pi(q_n)\):

1. Every positive adjacent preperiod increment is bounded by the lower eventual period:

\[
\boxed{0<a_n-a_{n-1}=\rho_n\le P_{n-1}.}
\]

Reason: a positive increment is the distance to the first reset along a periodic lower cycle containing at least one reset, so it is reached within one period.

2. Period doublings cannot occur at consecutive levels:

\[
\boxed{P_n=2P_{n-1}\implies P_{n+1}=P_n.}
\]

Reason: a doubling means the one-bit defect toggles after one lower period, so the lifted cycle contains both defect values, hence an LSB-1 reset; the next lift therefore cannot satisfy the reset-free doubling criterion.

3. A period-doubling level cannot simultaneously have a positive preperiod increment. Thus growth of period and positive reset-gap gain are mutually exclusive adjacent-level events.

## Finite diagnostic, x=1 only

Exact orbit computation through n=1000 gives period doublings at n=3,8,29,400; P_1000=16. The largest adjacent preperiod increment through 1000 is 13 (at n=660). tau(2^1000)=1275, so tau(2^1000)-1000=275. This is evidence only, not part of the proof.

## Strategic update

Run 217 sought a non-reusable charge for long reset gaps. The new period bound shows that within a constant-period epoch, individual gaps are already uniformly bounded by that period. The harder issue is cumulative reuse: many bounded positive gaps may occur before the next period doubling.

Next target: analyze a maximal constant-period epoch and bound the cumulative residence gain there using the cross-level defect recurrence / cycle-entry phase. Alternatively, prove that period-doubling levels are globally finite for a fixed finite origin. Do not claim either from the current results.

Detailed proof: `proofs/informal/problem1_run218_reset_gap_period_bound_and_isolated_doublings.md`.
