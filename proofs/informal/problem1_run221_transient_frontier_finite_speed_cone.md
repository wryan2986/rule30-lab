# Problem 1 run 221 — exact finite-speed cone for the transient defect frontier

Problem 1 remains open.

## Context

Run 220 isolated the moving look-ahead bit
\[
F_n=d_{n+1}(a_{n-1})
\]
as the obstruction to closing the constant-period stopping-curve dynamics with bounded state. The natural next question is whether the transient tail above that frontier is actually bounded or forced by the common-origin initial condition.

Write
\[
A^k(2^j x)=2A^k(2^{j-1}x)+d_j(k),\qquad d_j(k)\in\{0,1\}.
\]
For the common-origin tower, every adjacent defect starts at zero:
\[
d_j(0)=0\qquad(j\ge1).
\]
For the bulk levels the exact run-215 recurrence is
\[
d_j(k+1)=d_{j-2}(k)\oplus\bigl(d_{j-1}(k)\lor d_j(k)\bigr).
\]

## Exact finite-speed cone

**Lemma.** For every finite origin x and every k >= 0,
\[
\boxed{d_j(k)=0\quad\text{for all }j>2k.}
\]

**Proof.** At k=0 all d_j(0)=0 for j>=1, so the claim holds. Assume it holds at time k. If j>2(k+1), then j, j-1, and j-2 are all >2k. Hence all three inputs on the right side of the defect recurrence vanish, and therefore d_j(k+1)=0. Induction proves the claim. \(\square\)

Thus the common-origin defect spacetime has an exact upward propagation speed of at most two tower levels per scan step. No transient information can appear outside this cone.

## Consequence for the stopping frontier

At the stopping time k=a_{n-1}, the complete look-ahead tail
\[
H_n(r)=d_{n+r}(a_{n-1}),\qquad r\ge1,
\]
has finite support. Explicitly,
\[
\boxed{H_n(r)=0\quad\text{whenever }n+r>2a_{n-1}.}
\]
So run 220's moving frontier is not an arbitrary infinite binary tail at any fixed n. The entire transient state that can possibly influence future stopping-curve transitions is contained below level 2a_{n-1}.

Equivalently, the number of potentially nonzero look-ahead bits beginning at level n+1 is at most
\[
\boxed{\max(0,\,2a_{n-1}-n).}
\]

## Why this does not close the finite-state strategy

The bound is finite at each n but is not uniform in n. In the regime relevant to Problem 1, a_{n-1} itself grows with n (indeed the whole residence question concerns the excess of a_n over the diagonal). Therefore the causal cone can contain a linearly growing number of transient frontier bits.

So the simplest hope — that common-origin initialization forces all but O(1) look-ahead bits to zero — is false as a consequence of finite propagation alone. Finite speed converts the run-220 obstruction from an infinite tail to a finite but potentially growing state; it does not produce a bounded-state epoch theorem.

This is still useful structurally: any reconstruction theorem for F_n need only use the finite causal triangle below (n+1,a_{n-1}), and any impossibility/collision search can be restricted to that triangle rather than an unbounded tower.

## Next target

Exploit the triangular causal cone rather than merely its width. Trace the backward ancestry of F_n through
\[
d_j(k+1)=d_{j-2}(k)\oplus(d_{j-1}(k)\lor d_j(k))
\]
and ask whether the stopping conditions along k=a_j eliminate most admissible causal triangles. In particular, test whether two realizable common-origin towers can have identical bounded cycle/entry data at a constant-period epoch but opposite F_n. Such a collision would rule out reconstruction of F_n from that bounded data; failure to find collisions may expose an additional stopping-curve invariant.
