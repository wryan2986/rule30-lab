# Round306 lead review and verification limits

Status: `partial-proof` for accepted conditional deductions; local tests are
`finite-exhaustive` only on their declared inputs. No new `rigorous-proof`
status is assigned. Problem 1 remains OPEN.

## 1. External review attempts

The incoming shadow-gate/one-bit-exit review was assigned read-only to
`opencode-go/muse-spark-1.3-contributor`, thread
`01a07b76-3648-75b1-81f9-796b6893e2c6`. It failed before review text with
`MissingSessionID`: missing `x-opencode-session`. The thread was closed.

A fresh adversarial review of the NEW two-bit-collapse theorem was assigned
read-only to the same requested model, thread
`01a07b83-13c1-7e31-946c-22d09696f35d`. Its explicit goal was to find a fatal
flaw in the odd-doubling obstruction, exit escalation, or infinite induction.
It failed before review text with the same `MissingSessionID`; it too was
closed. Neither failure was a 429. MiMo was not advertised. No native or
other model was substituted, and no provider settings were changed.

Thus external review is missing for both the incoming notes and the new
theorem. The derivations below are lead checks, not reviews attributed to
either failed worker. There are no worker-authored changes to integrate.

## 2. Two-bit-collapse dispositions

Reviewed source: `problem1_two_bit_strip_collapse.md`.

* The even four-bit identity uses the actual centers through three further
  physical steps and the actual right-pair gate. It imposes no FULL values
  on the shadow.
* At an odd doubling the zero trace is along ONE moving characteristic.
  At the next even row it becomes the identically-zero HIGH A-trace.
  Assuming b<=2 makes bits 2 and 3 common and forces the next high shadow
  bit to be 1, a contradiction. This proves b>=3 there, not tau>=3 at
  the odd source. A row can have spatial discrepancy deeper than its delay.
* The one-bit exit table supplies agreement at every position<=-2 and
  disagreement at -1 at its next even row. Actual no-uu makes that row's
  gate t, hence its shared -2 bit is zero. One physical step then gives
  EXACT b=3; all still-further-left cones agree. No shadow center is needed.
* The invariant-region induction uses the eventual b<=2 premise at that
  additional odd time. Removing this future premise would invalidate the
  induction. Every intervening odd negative half is shielded by the common
  even left neighbor 1.
* The all-depth entry argument chooses a common late cutoff for tau<=2
  and b<=2. Unbounded clocks give a doubling beyond that cutoff; the new
  odd-doubling obstruction makes it even. The imported two-step result
  really assumes tau at that source is at most TWO, ensuring the upper
  row in the second extension is cyclic. Its unique cyclic low bit is 1,
  which matches the actual second even center. This supplies the cyclic
  start for the induction.
* Only after obtaining eventual b<=1 is threshold transport used to get
  eventual tau<=1. No row-wise identity b=tau, bounded period, uniform
  time to the next doubling, finite birth supply, or general induction on
  K has entered. The reverse implication is immediate.

Disposition: accept these deductions at `partial-proof` scope. They reduce
eventual K=2 to eventual K=1 for the single finite FULL orbit, and leave
existence or exclusion of that orbit unresolved.

## 3. Fixed checker audit

`check_round306_two_bit_collapse.py` freezes all eight Rule30 truth-table
values, then compares direct truth-table physical evolution with a separate
packed A-cut calculation on all sixteen declared assignments. Four check
the odd-doubling contradiction and twelve check the post-exit third bit.
The tests do not construct E shadows or infinite FULL sources and do not
search a neighborhood for a pattern.

The initial shell invocation used unavailable `python` and did not run the
checker. The successful invocation was `python3`; its atomic record is
`results/problem1/20260907_round306_two_bit_collapse.json`. All declared
10-second/128-MiB caps passed. The six current source hashes and canonical
payload hash were independently recalculated after execution and matched.
The record names the full pre-change base commit and hashes the new sources,
so their then-uncommitted state is explicit rather than concealed.

The immutable reference hash remains
`358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`.
No optimized backend, new benchmark, broad regression campaign, reference
edit, remote computation, or hardware change was involved.

## 4. Three-bit repair and eventual decomposition

Reviewed source: `problem1_three_bit_exit_repair.md`. This was a new
logical unit after the two-bit checkpoint; the two failed Muse threads
in Section 1 did not review it. A subsequent fresh review of this unit
was assigned to Muse, thread `01a07ba6-4d51-7be3-9f38-ca0d4b6ef219`, with
the explicit objective of finding a fatal flaw in its repair, entry, or
decomposition arguments. That attempt also failed before review text with
MissingSessionID, and the thread was closed. This was not a 429; no
substitute model or provider setting change was made. External review
remains missing. The following is a fresh lead check with explicit dependencies.

* Section 2's next-gate variable is actual input bit4 only under the FULL
  paired bridge. The arbitrary finite test cones therefore call it bit4,
  and do not assert a FULL continuation. The A difference after two steps
  is (low,high)=(0,z); this puts the high difference at PHYSICAL position
  -3, not -2. The lower physical differences also require the shadow's
  own center and right pair, which the direct updates retain.
* A -1 defect at a t source under b<=3 forces the next gate t even when
  that transition repairs the defect. Applying this at each listed source
  really produces the FIVE consecutive t gates v+2 through v+10 if the
  repair flag at v+4 is 1. No-ttttt then forces that flag to be 0. A b bound
  only through v+6 would not justify this argument; the all-late premise
  supplies the required extra two even rows.
* The b profile is 1,1,2,3,2,3,e, not the tau profile. Each exact tau is
  deduced with both a strict and a weak threshold at specified later
  times, or with the common even left-neighbor eraser. The renewal profile
  sums to 5+e, agreeing independently with tau_end-tau_start plus six
  positive-delay source times. This is not an original-support budget.
* The original-cut thresholds are determined even at the repaired e=0
  endpoint: s_(v+5)=v+6 and monotonicity force s_(v+6)=v+6 there. This
  justifies both exact front residence intervals and their erasers at
  (-3,v+3),(-3,v+5). Event ordering still does not supply ancestor reuse
  bounds. This is substitution into the imported identities, not a run.
* Positive R excludes two possible doubling times, and the new odd-source
  spatial obstruction excludes the three odd ones. The only possible
  doubling is at offset4, with source tau=2; the old two-step consumption
  law then forces e=0. Cyclic repair does not conversely prove a doubling.
* The shadow center inputs 0,1,1,1 used to obtain the transported flag are
  deduced from THIS exit. They are not a new imposed FULL boundary on the
  shadow. The flag reads five cells of the same globally selected shadow;
  realizing their assignments on that global domain is not checked locally.
* The new constant-one lemma uses only the shadow low values at A-times
  0,1,2 plus the next-two-step spatial bounds. After forcing d2=u, u=1
  violates the next spatial bound; u=0 with d1=1 instead violates the
  bound two steps later. A finite test of those necessary conditions
  does not claim that its shadow has an all-time constant low trace.
* At an odd doubling successor, the zero HIGH shadow trace and shared
  bit3 force d1=d2=1, then the next strip bound forces gate t. Center
  agreement would produce a -2 defect two steps later and hence delay
  greater than2. Clock consumption gives delay at most2, so the center
  also differs. The resulting three-bit difference is erased by ONE A
  step; the following odd common left1 shields the center. This proves
  entry at t+3 with no claim that b=tau at its intermediate row.
* One late doubling exists by the imported unbounded clocks. Either parity
  gives one even entry. Subsequent two- or six-step passages cover all
  future even rows and have even depths at most2, so all later odd
  doublings are excluded. Odd depths can still be3: the conclusion is NOT
  eventual all-physical b<=2, and the two-bit collapse cannot be reapplied
  without this missing hypothesis.
* The even-time tau equivalence uses the threshold at n=2 in one direction
  and the physical odd-delay bound in the other. If exits were eventually
  absent, the passage induction would imply eventual K=1. Thus a distinct
  K=3 alternative needs infinitely many disjoint exit passages, rather
  than merely a single finite example with delay3.
* Unbounded clocks still apply after entry, and every sufficiently late
  doubling is even and returns to a cyclic even row. Thus those returns
  occur infinitely often; their time gaps have not been uniformly bounded.
* The final birth-count inequality is a finite telescoping count of the
  binary noncyclic indicator. Each late doubling is a positive-to-zero
  switch because its next even row is cyclic; the number of such switches
  is births+I_M-I_N. Exclusion of odd doublings identifies the period-ratio
  logarithm with the counted even doublings. Additional nonclock returns
  can only strengthen the inequality. The round305 flag identity is used
  only at cyclic sources. Repairs are not wrongly counted as new cyclic
  births, and their unbounded possible number supplies no finite budget.

Disposition: accept only these `partial-proof` conditional results. They
identify a possible repair mechanism and its necessary repeated supply;
they neither exhibit that mechanism on an infinite FULL orbit nor refute
a separate proof that K=3 eventually collapses to K=1.

`check_round306_three_bit_repair.py` checks 96 fixed Boolean assignments:
16 paired transitions, 16 transported flags, 32 constant-one implications,
and 32 odd-entry controls. Separate truth-table and packed implementations
agree, after eight hand rule values and one hand four-step cone. The
10-second/128-MiB caps pass. The earlier 32-case working record was replaced
atomically after the additional entry lemmas required new checks; no source
or parameter discovery was run. Final provenance is audited at checkpoint.

The final notation audit corrected `d_1(t)` to physical `d_-1(t)` in the
two-bit note's optional even-doubling observation, and uses
`delta_j=d_(-j)(w)` for bit differences in the three-bit entry proof. The
formulas and verified cases are unchanged. Both atomic records are refreshed
against the final proof sources, and both six-source manifests and payload
hashes are independently recalculated. The incoming handoff archive is
compared byte for byte with the original base commit's handoff.
