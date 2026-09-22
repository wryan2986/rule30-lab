# Astra automation handoff — run 215

Problem 1 remains OPEN.

## Repository state entering run

No intervening work after run 214; branch tip was `1e7d81b18b22f95b2df287498551f2a9c067e01a`.

## New exact result

Let

    y_j(k)=A^k(2^j x)

and define the adjacent defect bit by

    y_j(k)=2 y_{j-1}(k) XOR d_j(k),  j>=1.

All `d_j(0)=0`. Using the run-207 one-bit update and the fact that

    bit_0(y_{j-1})=d_{j-1},
    bit_1(y_{j-1})=d_{j-2}

for j>=3 gives the exact bulk recurrence

    d_j(k+1)=d_{j-2}(k) XOR (d_{j-1}(k) OR d_j(k)),  j>=3.

If `d_0(k)=bit_0(A^k(x))`, the same formula holds for j=2. The j=1 boundary is driven by the two low bits of the base orbit.

Thus the entire cross-level defect hierarchy obeys exactly the same Boolean local form as the scan map A, with the tower-level index reversed relative to bit position. The common-origin mismatch phases are therefore traces of one deterministic boundary-driven Rule-30-form spacetime, not independent one-bit phase choices.

Full note:

`proofs/informal/problem1_run215_cross_level_defect_rule30_recurrence.md`

## Why this matters

This directly solves the run-214 target of deriving a cross-level recurrence that retains mismatch phase information. It also explains why period data was too coarse: the relevant information lives in the coupled defect spacetime.

It does NOT yet prove a bound on `a_n-n`; treating the recurrence as automatically contracting would be circular because its bulk rule is the same nonlinear local rule.

## Next target

Study the defect spacetime specifically along the cycle-entry/stopping curve

    k=a_j=tau(2^j x).

Use the exact recurrence to express the level-j mismatch at time `a_{j-1}` in terms of neighboring defect layers / their ancestry. Look for a non-reuse or causal-cone statement for the long zero runs whose lengths are the positive increments `a_j-a_{j-1}`. Avoid period-growth amortization (run 214 dead end).