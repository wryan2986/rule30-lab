# Round307 lead review and verification limits

Status: `partial-proof` for accepted conditional deductions; fixed checks are
`finite-exhaustive` only on their declared inputs. External review is missing.
No `rigorous-proof` status is assigned. Problem 1 remains OPEN.

## 1. Delegation and missing external review

The initial complete-driver sidecar was assigned read-only to
`opencode-go/muse-spark-1.3-contributor`, thread
`01a07bb5-26b5-7111-9465-72a109c94737`. It failed before returning work with
`MissingSessionID` (missing `x-opencode-session`) and was closed.

A fresh adversarial review of `problem1_full_driver_exit_phase.md` was
assigned to the same requested model, thread
`01a07bc1-fdfc-75a1-9667-347c9f3adc2e`. Its explicit goal was to find a fatal
phase, parity, quantifier, or bit-order error in the NEW proof. It failed
before review text with the same error and was closed. Neither failure was
429; MiMo was not advertised. No native or other provider was substituted,
no provider settings were changed, and there are no worker edits to integrate.

The following is a lead audit, not review attributed to either worker.

## 2. Complete-driver exit-phase dispositions

* The premise is current negative-half agreement with a center defect at an
  even FULL row. The common left neighbor is 1, so A erases that center
  defect in one step. A bound on tau alone at one row would not justify
  this spatial premise.
* The four scalar maps read the high/low bits of Theta(z) in the stated
  order. Their reset letters are 1 and 3, different from the earlier
  cyclic-birth quotient's reset letters 1 and 2. After the last reset, only
  2 flips the output. At h=0 the two terms in equation (5) are equal;
  at h=1 the parity is instead the indicator of reset letter 3.
* Negative A indices select phases of the same pure periodic core. The
  reset lookback exists only in the resetting case. There is no attempted
  last reset in a word contained in {0,2}.
* In the nonresetting case both spatial lift bits are cyclic. The proof
  selects one using A(2x+a)=2Az, with actual x=z+1 and common bit1=1.
  Because the right side is already cyclic, commutation with phase-correct
  cyc forces its previous lift bit to be 1. Merely taking the first cycle
  entry would have the wrong phase and would invalidate this step.
* The next scalar driver visits both bits: the original core's phase-zero
  symbol 2 already forces a flip. Its second cyclic lift is therefore the
  constant 1 response. This proves the second right bit as well as the
  first, without assuming odd parity or a doubled period.
* The separate pair derivation uses the ACTUAL right pair 00 on the FULL
  u branch. The code state is r2+2r1; cyclic state 3 means physical 11.
  The invariant pair {1,3} is recurrent for every periodic word in {0,2},
  whether its return is identity or swap. Its matching first A image fixes
  the same phase as the scalar derivation.
* The prior physical exit theorem is applied only after identifying h.
  Thus a nonresetting source returns without a future strip hypothesis;
  no resetting source has been shown automatically to return.
* Neither backward quotient is an autonomous update of successive cores.
  The concluding birth/no-exit obligations retain the original fringe and
  global E. In particular this result does not refute the finite even-parity
  fork, bound its number, or establish a finite birth supply.

Disposition: accept at `partial-proof` scope, subject to missing external
review. The previously unresolved phase of the nonresetting exit test is
fixed on the stated actual domain; the resetting global condition remains.

## 3. Fixed checker and provenance audit

`check_round307_exit_phase.py` freezes all eight hand Rule30 values and
eight hand A edges before its checks. It compares eight scalar values,
sixteen scalar-map compositions, four invariant-pair transitions, two
first-step pair values, and four named A-orbit certificates. The latter
are the old 7/6 source and its two zero extensions; no source is searched.
Packed A and a separate cell truth-table implementation agree, including
the finite zero boundaries and each final cycle return.

The local 10-second/128-MiB caps pass. The atomic record is
`results/problem1/20260907_round307_exit_phase.json`; its six source hashes
and canonical payload hash were independently recalculated and matched.
It records the full pre-change base commit and hashes the new sources,
making their then-uncommitted state explicit. The finite checks certify
their exact inputs, not E membership of arbitrary words or an infinite FULL
realization. The all-period last-reset induction remains a mathematical
argument with missing external review.

The immutable reference SHA256 remains
`358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`.
No benchmark, optimized backend, remote workload, reference edit, or hardware
control change is involved.

## 4. Exact exit wait and residence

A separate fresh review of `problem1_exit_wait_front_residence.md` was
assigned to Muse, thread `01a07bcc-8b83-7a02-8e97-cae2a53e2e31`, with an
explicit fatal-flaw objective for least delays, period preservation, front
offsets, and the full one-bit passage table. It failed before review text
with MissingSessionID and was closed. This was not429. External review is
missing; no substitute provider or native worker was used.

Lead dispositions:

* The exit-phase theorem excludes a nonresetting core when h=0. The first
  positive reset L therefore exists, and b0=2 makes L<=p-1. Actual u and
  no-uu give b1=b2=2, hence L>=3. No sampled wait is promoted to this claim.
* At the odd row the wrong lift is driven by Az, so the first reset has
  index L-1 and the least delay is L. At the next even row the two pair
  states start at 3 and1 with drive beginning at b2. They remain distinct
  under0/2 and coalesce under1/3 at update L-1. This independently fixes
  the second LEAST delay; an extra low residual cannot remain because the
  entire two-bit states and their already common upper rows then agree.
* Source reset letters preserve the first clock. Its first right trace
  has consecutive values0,1 and resets the second lift, preserving that
  clock too. More generally at every one-bit source the first right trace
  has consecutive values h,1 XOR h, so the second step never doubles.
* All three source delays are positive, justifying s_j=j+tau_j at each
  index in (7). The residence formula then gives exactly L times, at
  front positions0 through1-L. Its last eraser is at (-L,v+L), one cell
  to the left at the same time, not at the next update time. The A-ray
  derivation gives the identical zero word and eraser independently.
* The formula does not determine the next front jump or prevent later
  injections. The K=3 specialization only fixes this first wait to3;
  the six-step repair still needs its separate future-strip argument.
* At L=3, FULL permits reset symbol1 and excludes reset symbol3 at b3
  by the successor code's second symbol. This is a deduction for the
  fixed exit, not a search or a universal classification of larger waits.

Disposition: accept at `partial-proof` scope. No new computation or generated
record is used for this logical unit.

## 5. Nonresetting cores and clock-preserving returns

Reviewed source: `problem1_nonresetting_core_returns.md`. No external review
was obtained after the three provider failures above. This section is
explicitly a fresh lead-only audit of the third unit.

* The unconditional equivalence N_t iff O_(t+2) REQUIRES a positive
  center-and-left cut. The note now states Y0>0; a nonzero seed entirely
  right of the center would not suffice before its cone arrived. Positive
  width and the bridge preserve this premise thereafter. In the reverse
  direction the pure periodic core makes a constant trace after a shift
  equivalent to a constant trace from phase zero.
* A nonzero nonresetting core cannot have both low/high traces zero by
  Theta injectivity. Its first lift therefore visits both bits, even with
  even flip parity, and the second cyclic lift is uniquely constant1.
* An odd N would force the preceding even core's COMPLETE alphabet into
  {0,3}. FULL fixes the actual code's symbol at A-time2 in {1,2}; the
  eventual even bound tau<=2 makes that very symbol agree with its core.
  The argument does not exclude only odd-weight doublings and does not
  identify A-time1 with an already entered cycle when tau=2.
* The even source classification actually needs only CURRENT b<=2 and
  N, not a future bound. The t case's second A equality uses the shared
  bit4=0 forced by the zero core trace; it is not inferred from four low
  bits alone. The first differences are both low bits, and neither can
  affect any higher bit under A. This proves least delay2 directly.
* The t-source right phase is selected after TWO actual A steps. The
  resulting low bit1 is matched against the cyclic trace starting h,
  whose first two driver letters are0,2. This forces h=0. The recurring
  first-right1 then fixes k=1. The paired derivation uses every nonzero
  actual pair and reaches the same phase-correct lift4z+1.
* The return uses the already cyclic upper row at the second physical
  extension and its correct ACTUAL even center1. This is why no future
  strip assumption is needed for the single-source return. Period
  doubling still depends on the high-bit parity, not on N alone.
* The eventual K=3 decomposition locates t-type N at repair offset4;
  it does not assert that all cyclic repairs are N. Counting even-parity
  N returns alongside the odd-parity doublings gives (4) by binary
  switch balance. Clock-preserving nonresetting returns spend a birth
  supply as well, but that supply still has no finite-support upper bound.

Disposition: accept at `partial-proof` scope. Scalar/paired derivations are
independent algebraic checks, not external review. No new experiment or
source search is used for this unit.
