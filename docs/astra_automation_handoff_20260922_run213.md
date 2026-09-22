# Astra automation handoff — run 213

Problem 1 remains OPEN.

## New exact result

Let pi(q) be the minimal eventual period of the reviewed scan map A. Runs 207–209 give the adjacent-lift defect system

    A^k(2q)=2 A^k(q) XOR d_k,   d_k in {0,1},

with low-pair maps

    00 identity, 01 toggle, 10 constant-1, 11 constant-0.

If P=pi(q), composing these maps over one lower P-cycle shows exactly

    pi(2q) in {P,2P}.

Projection gives P | pi(2q); the one-bit monodromy gives pi(2q) | 2P.

There is also an exact doubling criterion. If the lower eventual cycle ever has low bit 1, a reset occurs and pi(2q)=P. If its low bit is 0 everywhere, then pi(2q)=2P iff the number of cycle positions with low pair (r0,r1)=01 is odd; otherwise pi(2q)=P.

Thus for q_n=2^n x,

    P_n=P_0*2^{e_n}

with e_n nondecreasing and increments only 0 or 1.

Full proof: `proofs/informal/problem1_run213_exact_period_lift_law.md`.

## Diagnostic

For x=1, exact orbit detection shows period changes at n=3 (2), n=8 (4), n=29 (8), and no further change through n=150. This finite observation is not used in the theorem.

## Next target

Couple the exact period law to the exact preperiod/reset-gap law from runs 208–210. Positive preperiod increments end at the first reset after cycle-entry mismatch, whereas period doubling is possible only when the lower eventual cycle has no reset anywhere. Seek an amortized incompatibility: determine whether long reset-gap gains force period-preserving levels, or whether stretches capable of period growth force enough matched lifts to control the residence surplus. Avoid returning to generic contraction of the full n-bit map; one-bit period monodromy is now completely classified.
