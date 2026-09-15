# Astra automation handoff — 2026-09-15 run 50

## New result

Resolved run 49's proposed causal-cone calculation for the existing one-bit doubling construction.

For `A`, low-bit perturbations never propagate upward: coordinate `i` depends only on old coordinates `i,i+1,i+2`. Thus high projections above a low reset are protected forever, consistent with the exact factor identity.

However, the period-doubling certificate belongs to the newly introduced low lift bit in `w=2z+a`. That fiber is itself in the reset/forcing boundary layer. In the concrete two-bit nonresetting source, actual `x` and periodic shadow `z` agree in all bits >=2 but differ in their low bits, and only merge after two A steps.

Therefore the run-49 margin criterion cannot hold for this certificate: distance from the doubling fiber to the forcing support is zero. The projection/cone route cannot transport the forced antiperiodic fiber history verbatim into the original realization.

## File added

- `proofs/informal/problem1_forced_doubling_fiber_cone_audit.md`

## Next target

Do not continue estimating cone widths. Instead eliminate the low fiber from

\[
a_{s+1}=c_s\oplus(b_s\lor a_s)
\]

plus

\[
a_{s+p}=1\oplus a_s
\]

to obtain a constraint involving only protected parent/high traces `b,c`, or derive a bounded-reuse charge of the low forced discrepancy to genuine gate/source activity. The former is preferable because parent/high histories are exact projections of the common-origin realization.

Problem 1 remains open.
