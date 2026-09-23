# Problem 1 run 222 — sharp outer defect characteristic

Problem 1 remains open.

## Context

Run 221 proved the finite-speed cone for the common-origin adjacent-defect hierarchy:

\[
d_j(k)=0 \qquad (j>2k).
\]

This run asks whether the outer part of that cone is merely a loose support bound or whether information from the common origin actually reaches the extremal characteristic.

Recall the exact defect recurrence (run 215), with the boundary convention used there:

\[
d_j(k+1)=d_{j-2}(k)\oplus\bigl(d_{j-1}(k)\lor d_j(k)\bigr),
\]

for the tower-level defects, where \(d_0(k)=\operatorname{bit}_0(A^k(x))\), and common-origin initialization gives \(d_j(0)=0\) for every \(j\ge 1\).

## New all-depth lemma: the outer characteristic is exact

For every \(k\ge 0\),

\[
\boxed{d_{2k}(k)=d_0(0)=x_0.}
\]

Here \(x_0\) is the least-significant bit of the finite tower origin \(x\).

### Proof

The statement is immediate at \(k=0\). Assume it at time \(k\). Apply the defect recurrence at level \(j=2k+2\):

\[
d_{2k+2}(k+1)
 =d_{2k}(k)\oplus\bigl(d_{2k+1}(k)\lor d_{2k+2}(k)\bigr).
\]

By the run-221 finite-speed lemma, both \(d_{2k+1}(k)\) and \(d_{2k+2}(k)\) vanish because their indices exceed \(2k\). Hence

\[
d_{2k+2}(k+1)=d_{2k}(k)=x_0.
\]

Induction proves the claim. ∎

## Consequences

### 1. The run-221 cone is sharp for odd origin

If \(x\) is odd, then

\[
d_{2k}(k)=1
\]

for every \(k\). Thus the support bound \(j\le 2k\) is attained at every depth. There is no improved universal cone \(j\le 2k-C\) with any fixed positive \(C\), and no sub-speed-2 support theorem can follow from common-origin initialization alone.

### 2. Arbitrarily high defect levels retain an exact origin bit

The transient defect hierarchy does not simply forget the common origin as tower level grows. The extremal characteristic transports the original LSB losslessly to level \(2k\) at time \(k\).

This is useful negatively: any proposed bounded-state closure based on an assertion that sufficiently high transient defect layers become independent of the origin is false for odd \(x\).

### 3. What this does *not* prove

The stopping-curve frontier from runs 220–221 is

\[
F_n=d_{n+1}(a_{n-1}).
\]

The exact outer characteristic concerns \((j,k)=(2k,k)\). It determines \(F_n\) only in the special alignment

\[
n+1=2a_{n-1}.
\]

Therefore this lemma does not yet decide whether \(F_n\) is reconstructible from bounded cycle/entry data, nor does it prove unbounded stopping-state complexity.

## Strategic interpretation

Run 221 left open the possibility that the finite causal triangle might have a uniformly simpler effective interior. The new lemma closes the easiest version of that hope: the outer edge is genuinely populated and carries persistent common-origin information at all depths (for odd \(x\)). Any successful compression must use the stopping geometry or cancellation inside the cone; it cannot come from shrinking the universal causal cone.

## Next target

Study the displacement of the stopping point from the sharp characteristic,

\[
\Delta_n:=2a_{n-1}-(n+1).
\]

When \(\Delta_n=0\), \(F_n=x_0\) exactly. More generally, derive recurrences for the near-edge diagonals

\[
e_r(k):=d_{2k-r}(k)
\]

for fixed \(r\). If these diagonals admit bounded-width formulas in the base orbit, then stopping-frontier reconstruction reduces to understanding whether \(\Delta_n\) stays bounded on relevant constant-period epochs. If \(\Delta_n\) is unbounded, this route precisely identifies how far into the causal interior the stopping curve penetrates.