# Astra automation handoff — 2026-09-22 run 209

Problem 1 remains OPEN.

Continue only the corrected run-193--209 chain.

## New exact result

Run 207's decomposition

    A^k(2q)=2 A^k(q) XOR d_k,  d_k in {0,1}

immediately gives the factor identity

    floor(A^k(2q)/2)=A^k(q).

Therefore periodicity of the doubled orbit from time t forces periodicity of the lower orbit from the same time. Hence universally

    tau(2q) >= tau(q).

Combining this with run 208 upgrades its complete classification:

- no reset on the lower eventual cycle: tau(2q)=tau(q);
- reset exists and entry defect matches the periodic lifted phase: tau(2q)=tau(q);
- entry defect mismatches: tau(2q)=tau(q)+rho, where rho is the distance to first reset.

Thus every adjacent shift-tower increment is exactly either 0 or rho; negative increments are impossible.

Proof note:

    proofs/informal/problem1_run209_tau_doubling_monotonicity_and_exact_increment.md

## Strategic correction

Be careful with run 208's suggestion to seek a restriction supplied merely by FULL on the cycle-entry phases/rho_n. The run-202 finite-fringe reduction identifies the actual far-right front thresholds of a finite seed with the shift tower a_n=tau(2^n x). Arbitrary finite x can itself serve as finite initial data. FULL contributes the requirement of infinitely many above-diagonal positive renewals; it does not automatically provide a second independent phase constraint.

For x=1 in particular, the run-208 bounded renewal observations concern the canonical single-seed tower itself. Do not dismiss them as behavior of an irrelevant generic family.

## Exact remaining condition

For q_n=2^n x and a_n=tau(q_n), a positive increment occurs iff the reset-phase mismatch occurs, and then

    a_n=a_(n-1)+rho_n.

The actual late-renewal/FULL condition is stronger:

    a_(n-1)+rho_n > b+n.

The next useful work must add genuinely new information beyond the adjacent-tower factor map—ideally a proved relation between reset location and finite original ancestry/birth accounting. Rephrasing the same renewal condition in complete-code/global-front language is not progress.