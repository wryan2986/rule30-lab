# Astra automation handoff — 2026-09-23 run 228

Problem 1 remains open.

## Repository state entering this run

`research/astra-next` was at `cc691eb36f2f0a718db38e9b6cef32fc6161de06` (run 227). No intervening work was present.

Run 227 proved that the top-coordinate orbit parity `p_R` descends one width and proposed studying coordinate derivatives of the descended observable.

## New all-depth result

For `R>=2`, with

\[
f_R(t)=x_{R-1}(t)\lor x_{R-2}(t),
\]

we have the exact formula

\[
\boxed{p_R(x)=\bigoplus_{j=0}^{O_R/2-1} f_R(T_R^{2j}x).}
\]

Thus `p_R` is specifically the even-time parity of the lower forcing cocycle, not an arbitrary lower-width Boolean observable.

Proof: expand `x_R(t)=x_R(0) XOR XOR_{s<t} f_R(s)` and XOR over one full order. Since `O_R` is even, the initial top bit cancels. The term `f_R(s)` occurs `O_R-1-s` times, which is odd exactly for even `s`.

Full proof: `proofs/informal/problem1_run228_even_time_formula_for_top_orbit_parity.md`.

## Research consequence

This changes the preferred next step. Rather than blindly taking successive coordinate derivatives of truth tables for `p_R` and `g_R`, analyze the square map `T_R^2`. The descended parity is accumulated exactly on a `T_{R-1}^2` orbit. Seek a two-step triangular recurrence or recursive cocycle decomposition under the square map.

The run-227 telescoping dead end remains a dead end: full-period telescoping merges the even- and odd-time cocycle parities. The new formula shows that `p_R` retains one parity class separately, which is information telescoping discarded.

## Next target

Derive an explicit coordinate formula for `T_R^2`, then test whether repeated squaring yields a recursive description of the cocycles. Because every `O_R` is a power of two, repeated squaring is naturally aligned with the entire order hierarchy and may expose a direct route to `m_R=v_2(O_R)`.
