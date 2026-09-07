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
