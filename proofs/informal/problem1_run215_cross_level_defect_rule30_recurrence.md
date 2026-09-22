# Problem 1 run 215 — cross-level defect hierarchy obeys the same local rule

Problem 1 remains OPEN.

## Setup

Use

    A(q) = (q >> 2) XOR ((q >> 1) OR q).

Fix a finite origin `x` and write

    y_j(k) = A^k(2^j x),   j >= 0.

Run 207 gives, for every adjacent pair of tower levels, a unique defect bit

    y_j(k) = 2 y_{j-1}(k) XOR d_j(k),   d_j(k) in {0,1},   j >= 1.

Initially

    d_j(0)=0

for every j>=1.

Run 207 also gives the one-step defect update. If the low two bits of the lower state `y_{j-1}(k)` are `(r0,r1)`, then

    d_j(k+1)
      = r0 XOR r1 XOR (d_j(k) AND NOT r0)
      = r1 XOR (r0 OR d_j(k)).

The second form is the useful one.

## Exact cross-level recurrence

The adjacent decompositions identify the low bits of every non-base tower level:

    bit_0(y_{j-1}(k)) = d_{j-1}(k),

and, for j>=3,

    bit_1(y_{j-1}(k)) = bit_0(y_{j-2}(k)) = d_{j-2}(k).

Therefore for every j>=3,

    d_j(k+1)
      = d_{j-2}(k) XOR (d_{j-1}(k) OR d_j(k)).

For j=2 the same formula holds if the left boundary is defined by

    d_0(k) := bit_0(y_0(k)) = bit_0(A^k(x)).

Namely

    d_2(k+1)
      = d_0(k) XOR (d_1(k) OR d_2(k)).

The first defect layer is driven by the two actual low bits of the base orbit:

    d_1(k+1)
      = bit_1(y_0(k)) XOR (bit_0(y_0(k)) OR d_1(k)).

Hence, away from the single base boundary, the entire infinite defect triangle satisfies the autonomous local rule

    boxed:  d_j' = d_{j-2} XOR (d_{j-1} OR d_j),   j>=2.

This is exactly the same Boolean local form as the scan map itself,

    (Aq)_i = q_{i+2} XOR (q_{i+1} OR q_i),

with the spatial index reversed: the tower-level direction plays the role of the scan's bit-position direction.

## Interpretation

This is the requested cross-level recurrence retaining the information that period data discarded in run 214.

The mismatch phase at level j is not an independent one-bit automaton. All defect layers are coupled by a deterministic Rule-30-form triangular evolution. Once the base orbit `A^k(x)` is fixed, the entire common-origin shift tower is generated from the all-zero initial defect half-line by this boundary-driven recurrence.

In particular, for j>=2 the update of layer j depends only on layers j,j-1,j-2 at the previous time. Thus cycle-entry mismatch phases and reset gaps at successive levels are constrained by one common spacetime diagram; they cannot be assigned independently even when all eventual periods have stabilized.

## Direct check

The recurrence was checked against direct exact integer iteration for sample finite origins and tower levels by comparing

    d_j(k) = A^k(2^j x) XOR 2 A^k(2^{j-1}x)

with the recurrence above. The adjacent difference is always a single bit by run 207, and the cross-level recurrence agrees step by step.

## What this does not yet prove

This identity alone does not bound the residence surplus `a_n-n`, and it does not prove that the above-diagonal renewals are finite. Indeed the recurrence has exactly the same nonlinear local form as the original scan, so assuming it is automatically contracting would be circular.

What it does accomplish is to replace the vague run-214 target ('find a cross-level phase recurrence') by an exact autonomous bulk law.

## Next target

Analyze the defect spacetime along the stopping/cycle-entry curve

    k = a_j = tau(2^j x).

Runs 208--210 say that `a_j-a_{j-1}>0` precisely when the new layer is out of its periodic phase at lower-level cycle entry, with the gain equal to the first-reset distance. The new recurrence shows that those mismatch bits are boundary traces of one Rule-30-form defect diagram.

A genuinely new theorem should therefore target the geometry of the curve `k=a_j` through this diagram: for example, derive a relation between the mismatch at level j and the neighboring defect layers near `(j,a_{j-1})`, or prove an ancestry/non-reuse statement for long zero/reset gaps in this defect spacetime. Do not fall back to period-growth amortization; run 214 ruled that out.