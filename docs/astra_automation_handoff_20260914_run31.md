# Astra automation handoff — 2026-09-14 run 31

Branch: `research/astra-next`

## Repository state reviewed

Run started from `3df6166ecebeeab263d05b2f602bf5c491ac1712` (run 30 handoff). No newer work was present on `research/astra-next`.

Problem 1 remains open.

The run re-read the current run-30 handoff and the older global bottleneck notes, especially `ASTRA_HANDOFF.md`, `problem1_nonreset_return_birth_spacing.md`, and `problem1_exit_wait_front_residence.md`. The global obstruction remains what the older handoff states: local spacing/residence identities do not yet give a finite-support upper bound on infinitely many required births or prevent period/phase changes.

## New result: exact odd immediate-reentry gap

Added:

- `proofs/informal/problem1_exact_odd_reentry_gap_from_four_fringe_bits.md`
- `scripts/check_exact_odd_reentry_gap.py`

Commits:

- `e31296d8259ec0e04abf5a55dcb25e08b4a8b347` — exact odd re-entry gap theorem.
- `7fbf92001cde594e474898a6d5ad4c33834347b3` — exhaustive modest-width checker.

Run 30 proved only `G'<=1` for odd `G=2D+1>=3`. The leading-edge recurrence gives a sharper exact formula.

For a nonzero word `w`, if `a_j^(q)` denotes the relative leading-edge bits, direct two-step evaluation gives

\[
a_3^{(2)}=x\land(y\lor z)
\]

when the leading four bits are `1xyz`. Define `H(w)=1` exactly for prefixes `1101`, `1110`, `1111`, and zero for the other five four-bit prefixes. Then

\[
a_3^{(2)}=H(w).
\]

For `q>=2`, the established recurrence has

\[
a_3^{(q+1)}=1\oplus a_3^{(q)},
\]

hence

\[
a_3^{(D+2)}=H(R)\oplus(D\bmod2).
\]

For an odd corridor, truncation after immediate re-entry discards exactly the first three leading bits of `T^(D+2)(R)`. Therefore `a_3^(D+2)` is the highest retained bit. If it is one, `G'=0`; if zero, the next bit is forced one (`a_4=1` for `D>=2`, and the run-30 `a_3 OR a_4=1` identity covers `D=1`). Thus

\[
\boxed{G'=1\oplus H(R)\oplus(D\bmod2).}
\]

So the post-reentry odd gap is exactly zero or one according only to corridor half-parity and the leading four fringe bits.

The same flag `H(R)` was already present in the exact commutator/fringe-core classification. This identifies a common mechanism: both the terminal commutator branch and the post-reentry corridor size are controlled by the same physical leading-edge bit `a_3^(2)`, rather than by unrelated finite-state coincidences.

The checker exhausts every fringe of the relevant bitlength for `6<=m<=16` and every odd `3<=G<m` with at least four fringe bits. The same computation was independently reproduced during this run for 10,872 fringe transports with no mismatch.

## What remains

This sharpens the local collision output but does not close Problem 1. The next genuinely global target remains to connect the bounded collision/re-entry endpoint data to the original finite-fringe FULL/common-origin accounting. In particular, a proof still needs to exclude indefinite evasion through period/phase changes and short-gap states; the old nonreset-return spacing result explicitly allows arbitrarily sparse infinite births/nonresetting sources.
