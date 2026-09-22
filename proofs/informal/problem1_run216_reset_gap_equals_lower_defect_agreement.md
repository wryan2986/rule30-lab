# Problem 1 run 216 — reset gaps are exactly lower-defect agreement runs

Problem 1 remains OPEN.

## Setup

Retain run 215 notation

    y_j(k)=A^k(2^j x),
    y_j(k)=2 y_{j-1}(k) XOR d_j(k),

with the exact bulk recurrence

    d_j(k+1)=d_{j-2}(k) XOR (d_{j-1}(k) OR d_j(k)).

Runs 207--210 show that a positive preperiod increment at level j is the waiting time to the first reset of the new one-bit lift after lower-level cycle entry. A reset occurs exactly when the low bit of y_{j-1} is 1. But

    bit_0(y_{j-1}(k))=d_{j-1}(k).

Thus the reset driver for lift j is exactly defect layer j-1.

## Exact zero-run / agreement identity

Apply the run-215 recurrence one level lower:

    d_{j-1}(k+1)
      = d_{j-3}(k) XOR (d_{j-2}(k) OR d_{j-1}(k)).

Whenever d_{j-1}(k)=0 this simplifies to

    d_{j-1}(k+1)=d_{j-3}(k) XOR d_{j-2}(k).

Therefore

    boxed: if d_{j-1}(k)=0, then
           d_{j-1}(k+1)=0  iff  d_{j-3}(k)=d_{j-2}(k),

and

    boxed: if d_{j-1}(k)=0, then
           d_{j-1}(k+1)=1  iff  d_{j-3}(k) != d_{j-2}(k).

Consequently every long reset-free interval in layer j-1 is exactly an interval of agreement between the two immediately lower defect layers j-3 and j-2, shifted by one time step.

More explicitly, suppose at time t the reset driver is zero,

    d_{j-1}(t)=0,

and its first later 1 occurs at t+r, r>=1. Then

    d_{j-3}(t+s)=d_{j-2}(t+s)   for 0<=s<=r-2,

while at the final preceding time

    d_{j-3}(t+r-1) != d_{j-2}(t+r-1).

Thus, up to the one-step indexing convention used for the reset transition, the positive increment rho_j is not merely an unexplained zero-run length: it is the first-disagreement time of the adjacent lower defect pair (d_{j-3},d_{j-2}) after lower-level cycle entry.

If the reset driver is already 1 at cycle entry, the lift is reset immediately and there is no long agreement interval to analyze.

## Why this is new

Run 210 identified positive residence surplus with low-bit zero-runs on the lower eventual cycle. Run 215 identified those low bits with the cross-level defect hierarchy. The identity above goes one step further: it eliminates the zero-run itself and expresses its continuation/termination locally in terms of equality versus inequality of two still lower defect layers.

So a large positive increment at level j forces a correspondingly long synchronization interval

    d_{j-3}=d_{j-2}

along the same stopping-time window. The endpoint of the gain is exactly where those two layers first disagree.

This is a concrete cross-level constraint on the reset gaps; they are not independent resources.

## Limitation / dead end avoided

The identity does not by itself bound the length of the agreement interval. In particular, one must not assume that two adjacent defect layers cannot agree for arbitrarily long times: the bulk dynamics is Rule-30-form and such a claim would require proof.

It also does not yet show that long agreement intervals at successive tower levels consume disjoint ancestry. The missing theorem is now more specific: control repeated long agreement runs of adjacent defect layers when sampled at the cycle-entry times a_{j-1}.

## Next target

Study the evolution of the equality indicator

    e_j(k)=1[d_{j-2}(k)=d_{j-3}(k)]

or equivalently the XOR

    g_j(k)=d_{j-2}(k) XOR d_{j-3}(k).

A useful next result would be an exact recurrence or causal ancestry law for g_j that shows whether a long zero run of g_j can recur across increasing j without requiring fresh boundary influence. This is now exactly the same object as a long positive reset gap, rather than a proxy for it.
