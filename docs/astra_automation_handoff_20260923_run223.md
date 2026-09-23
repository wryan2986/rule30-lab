# Astra automation handoff — 2026-09-23 run 223

Problem 1 remains open.

## Repository state entering this run

`research/astra-next` was at `f693bb5de1b568c3d167f2aecc6df781f36b9d56` (run 222). No intervening work was present.

Run 222 proved the sharp outer characteristic

\[
d_{2k}(k)=x_0
\]

and proposed studying the stopping displacement

\[
\Delta_n=2a_{n-1}-(n+1).
\]

## New proved result

Define fixed-depth near-edge diagonals

\[
E_r(k)=d_{2k-r}(k).
\]

After the width-\(R\) band has been born, it evolves autonomously by

\[
E'_0=E_0,
\qquad
E'_1=E_1\oplus E_0,
\]

and for \(r\ge2\),

\[
\boxed{E'_r=E_r\oplus(E_{r-1}\lor E_{r-2}).}
\]

The width-\(R\) map is triangular and invertible: recover \(E_0\), then \(E_1\), then each \(E_r\) successively from the primed vector. Therefore every fixed-width near-edge band is a finite **purely periodic** dynamical system.

Full proof: `proofs/informal/problem1_run223_near_edge_diagonal_automaton.md`.

## Exact stopping-frontier reformulation

The run-220 frontier bit is exactly

\[
\boxed{F_n=E_{\Delta_n}(a_{n-1})}
\]

when \(\Delta_n\ge0\); if \(\Delta_n<0\), finite speed forces \(F_n=0\).

So the transient obstruction is now sharply localized: it is the depth \(\Delta_n\) at which the stopping curve samples an otherwise finite-periodic family of edge bands.

## Additional exact identity

From \(\delta_n=a_n-a_{n-1}\),

\[
\boxed{\Delta_{n+1}-\Delta_n=2\delta_n-1.}
\]

Thus a matched lift (\(\delta_n=0\)) moves the stopping curve one layer toward the edge, while every positive increment moves it inward by the odd amount \(2\delta_n-1\). This is the displacement version of the residence ledger.

## Computational warning / evidence already in the repo

Run 218's verified `x=1` diagnostic found period doublings only at levels 3, 8, 29, and 400 through level 1000, with `P_1000=16` and `a_1000=1275`. Consequently

\[
\Delta_{1001}=2(1275)-1002=1548.
\]

So even inside the long observed constant-period-16 epoch after level 400, the stopping curve can sit extremely deep inside the transient cone. This does not prove asymptotic unboundedness, but it makes a small uniform displacement bound implausible and shows that constant eventual period alone does not keep the sampled frontier near the edge.

## Next target

The bounded-\(\Delta\) shortcut is therefore not the main bet. Study how the family of triangular edge automata is nested as depth grows. Because every fixed band is invertible and periodic, ask whether the value sampled at the moving depth \(\Delta_n\) can be related to a conserved/transported quantity, 2-adic triangular structure, or a period-divisibility hierarchy. In parallel, reproduce the `x=1` tower data with explicit \(\Delta_n\), \(F_n\), and near-edge states across the long period-16 epoch to identify an exact candidate invariant rather than relying on period alone.