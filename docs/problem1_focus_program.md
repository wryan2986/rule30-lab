# Problem 1 focused research program

Status date: 2026-07-22

All three prize problems remain open. This document freezes broad platform
expansion and makes one Problem 1 implication the repository's critical path.

## Target

Let `C=(c_t)` be a proposed center trace with `c_0=1`. Force the initial right
half-line to zero and use Rule 30 left-permutivity to reconstruct the initial
left half `L(C)=(x_{-d}(0))_{d>=1}`.

The focused conjecture is:

> If `C` is eventually periodic, then `L(C)` is not eventually zero.

The true single-cell evolution has an identically zero initial left half, so a
proof would exclude an eventually periodic true center and solve Problem 1.
A counterexample would refute this proof route, though not necessarily Rule 30
center nonperiodicity.

## What the existing finite search does not establish

The finite prefix-equivalence theorem proves that the first reconstructed one
occurs exactly at the first mismatch from the appropriate zero-left reference
trace. Therefore searching larger preperiod/period boxes for a *first* one is
only an expensive prefix comparison. It cannot distinguish a reconstructed
tail with one exceptional bit from a tail with infinitely many ones.

The four-forbidden-block image subshift is depth-independent, but its
time-zero constraint is vacuous on an all-zero adjacent left pair. The exact
cyclic-pair theorem assumes both the center and right-neighbor columns are
cyclic; eventual center periodicity alone does not justify that assumption.

The whole-tail formulation also has an exact limitation. An eventually-zero
reconstructed tail is equivalent to a finite-support initial configuration
whose rightmost one is at coordinate zero. In right-edge coordinates its
center trace is the growing diagonal
`bit_t(T^t(S))`, where
`T(S) = S XOR ((S << 1) OR (S << 2))` and `S` is any odd positive integer.
Thus the focused conjecture uniformly strengthens the single-seed prize
instance; it does not reduce it to a fixed finite-state system. See
[`problem1_whole_tail_equivalence.md`](../proofs/informal/problem1_whole_tail_equivalence.md).

The growing-diagonal map is now known to be a unit-triangular isometric
bijection of the 2-adic integers. Eventual temporal periodicity is equivalent
to a rational 2-adic output. The exact infinite-support cycle
`-1/3 <-> 1/3` maps to the period-one traces `-1` and `1`, so nested
fixed-coordinate periods alone cannot yield a contradiction. Finite spatial
support is the essential missing property. See
[`problem1_two_adic_diagonal_map.md`](../proofs/informal/problem1_two_adic_diagonal_map.md).

The published width-two theorem plus local Rule 30 identities now excludes
both eventual constant tails for every finite seed. Therefore period one is
closed, while every period at least two remains open. See
[`problem1_period_one_exclusion.md`](../proofs/informal/problem1_period_one_exclusion.md).

The first exact period-two pass is also complete. Its two phase equations
leave the right pair unrestricted, the two-step right-boundary recurrence is
a NOR of three spatial cells rather than a closed temporal map, and three
specific local/rapid-settling mechanisms failed their finite controls. This is
a stopping barrier, not an exclusion of period two. See
[`problem1_period_two_barrier.md`](../proofs/informal/problem1_period_two_barrier.md).

The inverse lift now has an exact low-to-high branch recurrence. Its dynamics
sections close on three maps, but the diagonal map does not: the section of
`Delta` along `j` zero input bits is `Delta circ T^j`, and these sections are
pairwise distinct. Thus neither `Delta` nor its inverse is a universal
finite-state tree automorphism. On the alternating period-two control, the
induced schedule already reaches period 256 by depth 16. This is a proved
universal finite-state obstruction plus a finite period-specific diagnostic,
not an exclusion of period two. See
[`problem1_inverse_lift_sections.md`](../proofs/informal/problem1_inverse_lift_sections.md).

The first period-specific quotient pass is also complete. The schedule head
is exactly a two-cell autonomous moving fringe, but its local four-state
relation is strongly connected. The apparent seven-block driver fails at
block 153, equal head-plus-depth-two portraits at blocks 11 and 55 have
different next-block zero status, and the proposed dyadic endpoint parity law
fails at `k=11`. A surviving all-width identity gives the sharper target: if
`ell_m` is the leading `t` run in the accumulated inverse word `H_m`, then the
pure alternating lift has infinite support exactly when `m-ell_m` tends to
infinity. This is a reduction, not yet the growth proof. See
[`problem1_period_two_quotient_obstruction.md`](../proofs/informal/problem1_period_two_quotient_obstruction.md).

The leading-run target now has an exact renewal form. A zero emitted base-4
block extends the leading `t` run by one, while every nonzero block resets it;
therefore infinite support is equivalent to infinitely many nonzero blocks.
During any hypothetical final zero streak, a normalized ordinary integer
`x=K^(-1)(0)` obeys `x'=Q(P(x>>2))`. Zero continuation is possible only at
`x=7 mod 16` with `Q=U` or `x=11 mod 16` with `Q=T`, and each continuing step
raises bit length by two. See
[`problem1_period_two_renewal_reduction.md`](../proofs/informal/problem1_period_two_renewal_reduction.md).

The partial map itself cannot supply a termination theorem on the full 2-adic
space. It has exact fixed points `x=5/3` on the constant-`u` branch and `x=1/3`
on the constant-`t` branch. Finite truncations shadow either fixed point for at
least `floor((N-4)/2)+1` zero blocks, so there is no uniform finite zero-run
bound based only on low-bit dynamics. See
[`problem1_period_two_2adic_zero_countermodels.md`](../proofs/informal/problem1_period_two_2adic_zero_countermodels.md).

The actual future schedule now has a unique 2-adic zero-survivor `X_m`, obtained
by composing the exact inverse zero branches. If `x_m` is the ordinary
normalized state, the number of consecutive zero blocks beginning at `m` is
exactly `floor(v_2(x_m-X_m)/2)` unless the states are equal, in which case the
zero tail is infinite. The shift-zero survivor is exactly
`Delta^(-1)(-1/3)`, the alternating inverse lift, and later survivors are its
moving tails. Its low-to-high bit pairs are generated by the coupled recurrence
`G -> G|_11 p q` with output `G(11)`. Therefore period-two support is reduced
to proving that this output-pair stream is not eventually `00`. See
[`problem1_period_two_schedule_survivor.md`](../proofs/informal/problem1_period_two_schedule_survivor.md).

The survivor construction now has an exact global schedule coding. If two
branch schedules first differ at index `n`, their survivor states differ with
exact valuation `2n+2`. Thus the complete zero-survivor set is a compact
perfect 2-adic Cantor set of Haar measure zero and Hausdorff dimension one
half. Moreover, an eventually periodic branch schedule cannot code an
ordinary finite integer: schedule-tail repetition would force survivor-state
repetition, while every ordinary zero step raises the highest set-bit degree
by exactly two. The actual schedule remains unclassified; starting at block
two it shadows `(ttututt)^infinity` for exactly 151 branches, explaining an
exact 304-bit survivor shadow. See
[`problem1_period_two_schedule_coding.md`](../proofs/informal/problem1_period_two_schedule_coding.md).

The actual moving fringe now has exact all-time local language constraints. Its
`u` indicator is the even-time trace of cell `-2`, so the published width-two
theorem forces this branch schedule to be non-eventually-periodic under a
finite-seed alternating-center hypothesis. The autonomous two-step fringe map
forbids `uu`, `ttttt`, and `ututtu` at every position; successive `u` events
are separated by two through five blocks. Combining these constraints with the
schedule similarity coding places every compatible survivor in a
graph-directed 2-adic set of dimension at most about `0.275732`. This still
does not exclude isolated ordinary integers. See
[`problem1_period_two_fringe_language.md`](../proofs/informal/problem1_period_two_fringe_language.md).

## Admitted work

A proposed task is on the critical path only if both possible outcomes inform
the whole-tail conjecture. Current admitted directions are:

1. Search for eventually periodic traces whose reconstructed left prefixes
   have a long terminal zero run after their last one. Such candidates are
   counterexample leads; absence is finite evidence only.
2. Derive exact recurrence, diagonal, or front constraints on the complete
   reconstructed tail under an eventually periodic temporal boundary.
3. Formulate the simultaneous conditions “temporal tail periodic” and
   “initial spatial tail zero” as a symbolic-dynamics, SAT, de Bruijn, or
   transducer problem, proving any claimed state bound before using a finite
   graph as an infinite argument.
4. Search for monotone quantities or forbidden cycles that survive the
   transient seam and distinguish an eventually-zero spatial tail.
5. Formalize only stable local or finite-tail lemmas needed by a candidate
   proof, then connect them to the existing width-two literature result when
   the hypotheses genuinely match.

## Frozen work

Until a new theorem or algorithm changes the situation, do not spend research
time on:

- larger center-prefix statistics or discrepancy checkpoints;
- larger first-witness period/preperiod boxes;
- generic automaton, recurrence, or 2-kernel sweeps for Problem 3;
- wider polynomial-conservation sweeps for Problem 2;
- CUDA optimization of one sequential Rule 30 history;
- ports of established experiments to additional backends;
- repeated benchmarks without a changed algorithm;
- fixed-width graphs offered without a depth-independent state theorem;
- universal finite-state section searches for `Delta` or `Delta^(-1)`, which
  are ruled out by the infinite-section theorem;
- wider fixed-depth portraits, longer schedule-head prefixes, or new endpoint
  patterns without a proved closure mechanism;
- CLI, runner, dashboard, or documentation features beyond maintenance; or
- broad Lean formalization of implementation details.

Problems 2 and 3 retain their verified code, vectors, and records. Their tests
remain regression gates, but their research campaigns are paused.

## Decision gates

Each new experiment must state in advance:

- the exact quantified finite or infinite claim;
- what would count as a counterexample lead;
- what finite absence can and cannot establish;
- how the result changes the next proof step; and
- a resource cap and stopping condition.

After each campaign, continue only if it produces a new invariant, a stable
recurrence, an exact certificate, a counterexample candidate, or a sharper
mathematical obstruction. Merely increasing a bound is not continuation.

## Immediate sequence

1. Derive an all-scale first-return map between successive `u` events, whose
   exact return times are now known to lie in `{2,3,4,5}`.
2. Seek a renormalization or cocycle coupling that return map to nonzero output
   pairs of the schedule survivor; a longer fixed word list is not continuation.
3. Prove any proposed return-state quotient is depth-independent before using
   cycle classification as an infinite argument.
4. If the return map does not close, transfer the self-trace and mismatch
   valuation identities to an original-spacetime finite-support obstruction.
5. Formalize the autonomous fringe, self-trace, and return identities only when
   they enter a genuine infinite argument.
