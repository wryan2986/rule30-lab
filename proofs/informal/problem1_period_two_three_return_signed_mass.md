# Signed mass on the full three-return domain

Status: `inconclusive` pending the bounded falsification test and independent review.

## Admission and the single bottleneck

The starting source is `b54f067210d5d8eeb1af3247c858c97af456497c`.
The latest signed-belief note concerns only phase `u` and return gaps `(2,2,2)`.
The adjacent-shadow reduction, in contrast, quantifies over both phases and
all admissible triples of gaps in `{2,3,4,5}`. The older research-status and
focus-program summaries predate these frontier results; recent Git history
and the linked proof notes determine the current research boundary.

The single question in this pass is whether signed mass provides one
nonvanishing certificate on that full three-return domain. No earlier
complexity bound is increased.

Conjecture (`inconclusive`): for every phase `a in {p,u}`, complexity `k>=2`,
state `x in O_(a,k)`, cut `c>=0`, and gap triple `g`, if the exact forced zero
schedule of `x` begins `w E(g)`, where `|w|=c`, and `w E(g) u` avoids `uu`,
`ttttt`, and `ututtu`, then the dominant adjacent-shadow belief at depth
`L=c+1<k` has nonzero signed mass.
Here `E(g)=u t^(g_0-1) u t^(g_1-1) u t^(g_2-1)`.
The final appended `u` is an admissibility condition, not an extra observed
branch. This is the established three-return reduction's convention.

For a shadow `y`, its weight is `(-1)^d`, where `d` counts nonfull shadow
fibers along all `L` common low base-four digits. The conjecture concerns the
sum over distinct concrete endpoints, not over generator representations.

Outcome gate, stated before execution:

- A cancellation refutes this unified signed-mass certificate, even if the
  concrete belief remains nonempty. A proof would then need additional
  structure or a different certificate for the offending return class.
- No cancellation through the cap supports only the explicitly finite
  extension of the previous census. It would justify examining an all-depth
  counting identity on the full domain, not increasing the bound.

Resources and stopping rule: one local CPU process, complexity at most 16,
forced-schedule cap 64, at most 120 seconds and 1 GiB address space per run.
Order candidates by complexity, phase (`p` then `u`), integer state, cut, and
lexicographic gap triple. Stop at the first zero signed mass, or after the
cap if none exists. Independent verification may replay the same finite
certificate; it is not a new search campaign.

## Scope and existing barriers

The exact local derivative identity remains valid independently of this test.
Signed nonzero implies nonempty, but the converse is false in general.
The previous phase-`u`, complexity-5 cancellation at `0x198`, depth one, is
not itself an admissible three-return occurrence. It does not settle this
conjecture.

The full adjacent-shadow inclusion is only a sufficient condition for the
absence of three-return zero-penalty plateaus. Neither a signed cancellation
nor failure of an adjacent shadow would by itself supply a finite seed with
an eventually periodic center. General eventual period two and the whole-tail
conjecture remain open.

References:

- `problem1_period_two_signed_belief_derivative.md`
- `problem1_period_two_three_return_adjacent_shadows.md`
- `problem1_period_two_weighted_shadow_recursion.md`
- `problem1_period_two_phase_frontier_lift_recursion.md`

## Result and review

Pending. Finite evidence is not an infinite proof.
