# Automation research handoff — 2026-09-13

Problem 1 remains **OPEN**. Continue on `research/astra-next`.

This handoff supplements, and does not replace, `ASTRA_HANDOFF.md` and its
archived predecessors.

## Repository-state warning

The pushed `ASTRA_HANDOFF.md` says that the following round309 drafts were in
the worktree during its intermediate checkpoint:

- `proofs/informal/problem1_three_bit_complete_core_system.md`
- `proofs/informal/problem1_complete_core_phase_transport.md`
- `proofs/informal/problem1_fixed_fringe_phase_collapse.md`

They are **not present in the currently pushed branch tree**. Do not pretend to
audit, extend, or cite their unpushed proofs from the short handoff summaries.
The pushed and inspectable nonreset-return unit
`problem1_nonreset_return_birth_spacing.md` is present.

## New all-depth reduction committed in this run

Read:

`proofs/informal/problem1_shift_tail_excess_reduction.md`

For a fixed nonzero finite original row, let `R` end its right support and put
`v=L_R(r)>0`. Then every later original cut is exactly

    L_(R+n)(r) = 2^n v.

Combining this with the established global-front threshold identity gives

    tau(Y_(R+n)) = max(tau(2^n v) - (R+n), 0).

Therefore an eventual finite physical delay strip is equivalent, for this row,
to boundedness above of

    e_v(n) = tau(2^n v) - n.

The existing theorem `tau(2^n v) -> infinity` is insufficient. A sufficient
scalar theorem excluding every finite strip would be

    limsup_n [tau(2^n v)-n] = infinity

for every positive finite `v` (or the corresponding FULL-domain statement if a
universal theorem is too strong).

Writing

    delta_v(n)=tau(2^(n+1)v)-tau(2^n v),

one has exactly

    e_v(N)=tau(v)+sum_(n<N)(delta_v(n)-1).

Thus future clock/front/eraser work has to force unbounded **positive
excursions of this signed cumulative sum**. Infinitely many births, positive
increments, clock doublings, or mere divergence of `tau(2^n v)` do not suffice.

## Current preferred target

Seek an all-depth mechanism on the FULL finite-fringe domain that constrains the
complete one-bit zero-extension/eraser history strongly enough to make the
partial sums

    sum(delta_v(n)-1)

unbounded above. Do not resume gate-prefix, source-prefix, shifted-row, or
periodic-core sampling merely to estimate this rate; the existing stopping
fences already rule those out as proof routes.

A useful negative result would also be valuable: an exact compensation
mechanism showing why the signed sum can remain bounded above despite the
known forced births/clock growth would close this route cleanly and redirect
the search.

No claim of a Problem 1 solution is made here.