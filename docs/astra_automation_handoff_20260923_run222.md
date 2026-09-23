# Astra automation handoff — 2026-09-23 run 222

Problem 1 remains open.

## Repository state entering this run

`research/astra-next` was at `49719a6eba08e5d40ee305ca60f965fee52a8162` (run 221). No intervening work was present.

Run 221 proved the common-origin finite-speed cone

\[
d_j(k)=0\quad(j>2k),
\]

and left the stopping frontier \(F_n=d_{n+1}(a_{n-1})\) as the main transient obstruction.

## New proved result

The outer boundary of the run-221 cone is exact:

\[
\boxed{d_{2k}(k)=d_0(0)=x_0\quad\text{for every }k\ge0.}
\]

Proof: at level \(2k+2\), the recurrence is

\[
d_{2k+2}(k+1)=d_{2k}(k)\oplus(d_{2k+1}(k)\lor d_{2k+2}(k)),
\]

and the last two terms vanish by finite speed. Induct.

Thus for odd origin \(x\), the support reaches the extremal level \(j=2k\) at every time. The causal cone cannot be universally narrowed, and arbitrarily high transient defect levels retain the original LSB exactly.

Full proof: `proofs/informal/problem1_run222_sharp_outer_defect_characteristic.md`.

## Dead end closed / limitation

Common-origin initialization does not create an empty margin behind the speed-2 boundary. Any bounded-state compression must exploit stopping geometry or internal cancellation, not a smaller universal propagation cone.

This does not determine the stopping frontier except when \(n+1=2a_{n-1}\), so it does not solve Problem 1.

## Next target

Define the stopping displacement

\[
\Delta_n=2a_{n-1}-(n+1)
\]

and near-edge diagonals \(e_r(k)=d_{2k-r}(k)\). Derive exact fixed-\(r\) recurrences/formulas. Then test whether \(\Delta_n\) is bounded on constant-period epochs. A bounded displacement would make only finitely many near-edge diagonals relevant to \(F_n\); unbounded displacement would show the stopping curve penetrates progressively deeper into the transient cone.