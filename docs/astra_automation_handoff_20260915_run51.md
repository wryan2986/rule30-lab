# Astra automation handoff — 2026-09-15 run 51

## New result

Run 50's preferred target succeeds exactly. Starting from

\[
a_{s+1}=c_s\oplus(b_s\lor a_s),
\]

the one-step fiber map is constant whenever `b_s=1`, and is `a -> a xor c_s` whenever `b_s=0`.

Therefore the return map over one parent period `p` is a transposition (hence the lift genuinely doubles from `p` to `2p`) iff

\[
b_s=0\quad(0\le s<p)
\]

and

\[
\bigoplus_{s=0}^{p-1}c_s=1.
\]

So the forced low fiber has been eliminated completely. A genuine doubling is certified solely by protected parent/high traces: a full-period zero block in `b` and odd parity in `c`.

## File added

- `proofs/informal/problem1_doubling_parent_trace_elimination.md`

## Next target

Identify the exact spatial/common-origin meaning of `b_s,c_s` in the scan construction. Use the parent-only criterion to determine whether infinitely many doubling passages force accumulating genuine activity: either via arbitrarily long protected zero blocks with odd companion parity, or by charging the odd `c` parity witnesses into the existing joint-window/finite-entry budget.

Do not return to transporting the low antiperiodic `a` history; this elimination bypasses that obstruction.

Problem 1 remains open.
