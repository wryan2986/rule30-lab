# Round 304 lead adversarial disposition

Status: `partial-proof` / scoped `refuted` / `finite-exhaustive` as assigned
in the reviewed note. This is a LEAD review, not an external independent
review. Problem 1 remains OPEN.

Reviewed first unit: `problem1_finite_cycle_phase_fork.md` and its fixed checker.
The review objective was to find a fatal flaw, particularly an unjustified
finite-support inference, confusion of phase with preperiod, or replacement
of the actual right boundary by free lift choices.

## 1. Quantifiers and mathematical checks

1. The proposal being refuted is explicit: EVERY positive finite cyclic y
   with zero low temporal bit has odd high-bit weight in its LEAST period.
   It is not the stronger FULL-conditioned statement. A single verified
   finite y with even weight suffices for this scoped refutation.
2. For z_e=2y+e, sigma A^t z_e=A^t y and the one-bit equation is
   v_(t+1)=bit_1(A^t y) XOR v_t because bit_0(A^t y)=0. This is a
   permutation at every time. Both lifts are cyclic from time zero;
   no unobserved transient is inferred away.
3. The p-step parity return fixes both lifts in the even case. Their
   periods divide p and are divisible by p by projection. If the two
   cycles met, an A-time shift joining their initial states would project
   to a return of y and be divisible by p, hence fix the starting lift.
   Thus the cycles are disjoint. Equal period does not mean equal cycle.
4. The fixed word has six 2s; its half-period test at indices 1 and 9
   excludes every proper divisor of 16. Word length alone is not used as
   its least period certificate.
5. The three displayed Phi transitions were rechecked against g's literal
   table, including the last-to-first edge. In particular g(1,0)=3;
   the lookalike inverse-scan h table would give an incorrect chain.
6. The deletion chain reaches zero with every earlier row nonzero.
   Conjugacy gives a genuinely FINITE spatial row; neither dyadic period
   nor eventual temporal periodicity alone would justify that conclusion.
   Reading first symbols recovers the complete integer. Explicit cell
   evolution then checks the whole row for sixteen steps and a return.
7. The two lift traces have weights 4 and 12, providing an independent
   obstruction to a rotation identification. This separation is redundant
   with projection and is used as a falsification check, not a replacement
   for the general argument.
8. For the physical consequence, sigma^t Y^e_t=A^t z_e retains each
   actual boundary separately. The projected rows differ only at bit zero;
   hence bit t is the highest actual difference, not just an upper bound.
   Both rows have the same arbitrary complete right fringe. Physical sites
   further left agree by cones, and the common neighbor on the propagation
   characteristic is zero. This is a moving characteristic, not a pair of
   fixed spatial columns; the width-two nonperiodicity theorem is not
   contradicted.
9. The persistent difference is BETWEEN TWO initial cyclic rows. It is
   not either row's internal cycle defect, and it counts no R_t on ONE
   survivor. Neither initial pair is silently relabeled a FULL cyclic source.
   The result supplies neither an infinite FULL orbit nor infinitely many
   births, even with a finite common fringe.

Disposition: accepted by the lead at the stated scope. No `rigorous-proof`
status is assigned. The nilpotence/parity reduction is refuted; full-history
compatibility with the original boundary remains the research bottleneck.

## 2. Computation and provenance audit

The new run has exactly one scientific input, the literal word selected from
Rowland's author PDF. The PDF's last page was visually inspected for the bit
order; its hash and URL are in the atomic record. No assertion about the
first occurrence among columns is imported. The fixed word is not a new
member of the rejected one-hole family, a completion of the round303 suffix
construction, or a larger FULL-prefix test.

The two deletion loops have separate representations (tuple/Boolean formula
and string/literal table). Full trajectory hashes and all reconstruction
digits agree. The Boolean cell evolution has an independent local rule and
checks all 851328 bits, with zero upper boundaries retained. The lifted
cycles are separately checked with packed A and the scalar XOR recurrence.
The checker stops on zero or a fixed 100000-step cap; a cap without zero
has status `inconclusive`, not a no-zero claim. The 60-second/128-MiB limits
passed. There is no optimized backend, sanitizer requirement for a new native
kernel, benchmark, seed search or long physical orbit run in this unit.

The initial `python` invocation failed before execution because only
`python3` is installed. The subsequent Python 3 child run succeeded. This
failure did not generate or supersede a scientific record.

## 3. Missing external review

The authorized Muse review of the incoming round303 note was attempted in
thread `01a07af9-afb9-7e03-833c-cbe7da1826b8`. It returned no review text,
failing with `MissingSessionID` (missing `x-opencode-session`). The thread
was closed. This was not a 429 and the rate-limit fallback was not triggered.
MiMo was not an advertised model override. No alternate native or other
provider reviewer was substituted, and no provider configuration was changed.

Fresh external review therefore remains missing for the incoming round-ten
and round303 notes and for this new round304 proof unit. The lead's separate
algebraic derivations and independent programs do not satisfy that external
review requirement. Rollover is a maintenance checkpoint, not research
success, blockage or exhaustion.

## 4. Second unit: reset anchoring geometry (lead review)

Reviewed `problem1_reset_anchoring_geometry.md` as a separate derivation.
No numerical experiment is used. Its statuses remain `partial-proof` and
the scoped `refuted` same-cell assignment; no FULL orbit is constructed.

* The reset driver is A^(T+1+rho)Y_t, so with lambda=T+rho+1 it is
  A^lambda Y_t, not A^(lambda-1)Y_t. The wrong lift at scan time
  lambda-1 is updated by this driver. The physical reset cell is
  (-lambda,t+lambda), and erasure happens one physical time later at
  the same site on the adjacent characteristic. This checks the offset
  independently of the renewal's shorthand H_t.
* The characteristic coordinate of the reset is t. Original activity
  cells have characteristic -2n or -2n-1, with n>=1. This establishes
  disjointness even before checking the shorter anchored horizon.
* For the sharp L1 distance, the two bounds d>=t+j and
  d>=t+2lambda-2j+2 use only the two linear coordinate functionals
  of L1 norm one and s<n. Twice the first bound plus the second, divided
  by three, gives d>=t+2(lambda+1)/3. The three residue classes of lambda
  cover ALL lambda>=1; k>=1 in the 3k case prevents n=0. Each displayed
  attainment point has nonnegative time and a valid anchored horizon.
  Equality is only for the sampling domain; its nearest point need not
  be active in the particular initial row.
* The 55 control is nonvacuous. Its odd row100 has closed cycle
  A(100)=25 XOR118=111, A(111)=27 XOR127=100. Together with the imported
  55 and223 cycles, this gives R_1=1, lambda=1. The erasing point(-1,2)
  is three spacetime steps from the active point(-2,0). No additional
  physical prefix is used.
* A purported uniform-radius charge under an unknown FULL/finite-entry
  premise cannot simply be called refuted: the premise may be empty.
  The note correctly states the conditional geometric obstruction and
  leaves global transport open. This is an essential quantifier fence.
* Q(-1)=1 and sum_n J_n(-1)=infinity follow from A(-1)=0, with no
  periodic-center premise. This refutes only identifying a supremum of
  per-ray counts with total count across all rays.
* The rebase H=2ceil(h_J(K)/2) is chosen ONCE and has the correct
  phase. The bound for A^H Y_0 uses preservation of finite width after
  time h, not the false assertion that Q is A-invariant. Restoring H
  low bits gives width<=H+2(K+h+1), whence Q(Y_H)<=K+h+H/2. The zero
  projected-row case still satisfies this bound. The rebased right
  half is the actual finite fringe, retained in full.
* The finite capacity is for PAIR samples. Mapping to individual cells
  can double that capacity. A multiplicity bound must be independent
  of the later time horizon. Neither such a bound nor a charge has
  been proved, so the final implication remains a reduction.

Disposition: accepted by the lead in scope. This narrows the anchored
route to global transport with controlled reuse, after a justified actual
rebase; it does not settle its existence or the FULL incompatibility.
