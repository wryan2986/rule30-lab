# Testing activity-record nonincrease across genuine returns

Status: `refuted` for universal activity-record nonincrease on admissible
prescribed three-return blocks, with the exact verification record
below. Closed finite vectors are `finite-exhaustive`; their all-age
interpretation uses the stated recurrence (`partial-proof`). Problem 1
remains open. The following admission text preceded execution.

## Mathematical decision and admission, before computation

The finite-level theorem in `problem1_activity_level_finiteness.md`
shows that R(x)=sup_s V_s(x) has finite sublevel sets on Z_2. A
finite ordinary input in an infinite forced orbit has growing bit
length. Consequently, an all-depth theorem that R does not increase
on every admissible three-return block would exclude such an orbit:
the blocks have gaps 2..5, hence bounded lengths, and the intervening
one-step increase is at most one. R would remain uniformly bounded,
contradicting finiteness of its sublevel set and degree growth.

The universal one-step version is already refuted by the hand case
27->111, but that successor has no continuing gate. A genuine
three-return test is therefore a materially different domain, not
an attempt to repair the one-step formula. R is a maximum over all
sampling ages, not an additive current-history cost; the older
additive-reader no-go results do not decide this candidate.

Test ONLY the existing u/k18 state x0=0x6473d46ab, with recorded
from-zero history uutuuttuupupuuupup. Its fixed root is 1, so the
first u creates the root and is excluded from nonroot positions.
Replay exactly the TEN already observed branches ttttututut, and
confirm the unobserved final u gate at time10 without executing it.
The tested three-return block is times4 through10, gap tuple222,
with its two actual prescribed histories retained. No new initial
state, branch, frontier level, return occurrence, or boundary cut is
searched. Compare R(x4) and R(x10).

If R(x10)>R(x4), the proposed nonincrease on all such actual
prescribed return blocks is refuted and cannot supply termination.
If R(x10)<=R(x4), this is one exact named control only; proving the
all-depth inequality would remain necessary. Failure of a formula,
history, or closure check invalidates that certificate. Failure to
close under the limits below is inconclusive and does not admit a
larger computation.

For an ordinary history with n nonroot letters and prefix endpoints
v0=root,...,vn=x, the established identity is

    V_s(x)=sum_(i=0..n-1) bit_0(A^s(v_i)),  s>=n.

Thus an EXACT closed orbit of the vector of these n finite endpoints
under componentwise A certifies every age s>=n. Compute V_s directly
for s=0,...,n-1. For the tail, initialize the vector at age n and
iterate only until its FIRST repeated full vector. Record the full
score sequence, the first repeated vector, entry age and cycle length,
and the earliest maximizing age. This yields R, with no inference
from failure to see larger values at a finite horizon.

Primary: packed Python integers, ordinary generator/scanner histories.
Independent: explicit bit arrays implementing T and A cellwise, and
an independently derived tail state with components

    w_d=A^(n-d)(pi^d(x)), d=1,...,n.

At age n+r its score is sum_d bit_0(A^r(w_d)); this follows directly
from the A-diagonal formula and pi^(n+1)x=0. These components need
not be the primary history components, so compare entire V score
streams through a common verified preperiod and common period; also
compare direct full temporal vectors for s=0,...,n+2. Each method
certifies its own exact closure. No source imports between them.

Bounds per implementation: one local CPU, 120 seconds, 1 GiB, at most
65536 tail-vector transitions PER one of the two endpoints. Stop
inconclusive on any bound, do not extend it. Record exact parameters,
source and executed-admission snapshots, input/history provenance,
full base Git commit, software/hardware, timings, hashes and atomic
JSON. This is a named finite-state certificate, not an activity-level
or frontier census, and no benchmark or optimized backend is involved.

The finite computational status will be `finite-exhaustive` for the
declared closed vectors and histories. Any all-age inference additionally
uses the explicitly proved finite-state recurrence above. Both the
scope of the counterexample and that finite-to-all-age implication
require fresh adversarial review before acceptance.

## Named outcome and all-age certificate

Both independent methods give

| Orbit time | Endpoint | Nonroot length | First max age | Full record R |
| --- | --- | ---: | ---: | ---: |
| 4 | 0x6473c6fc387 | 21 | 21 | 13 |
| 10 | 0x6473c7a1004b27 | 27 | 25 | 16 |

The exact tail vectors enter cycles at ages32 and41, respectively,
both of period8. Their first closures are at ages40 and49. Direct
ages below21 or27, respectively, together with the complete finite
transient and one closed cycle, cover EVERY possible V age. The
second record is attained already at age25, before its tail formula's
starting age27; a tail-only maximizer report would miss that first age.

Hence R(x10)-R(x4)=3>0 on this genuine prescribed gap222 block.
Explicitly, the gates at times4,6,8,10 are u and those at5,7,9 are t,
so the three successive u-return gaps are exactly2,2,2. Time10's
u gate is checked without executing an eleventh branch.
This refutes nonincrease on all such blocks. No further endpoint or
return search is authorized by the result. In particular the admission
is not extended to fit a compensated record, a modified gap family,
or a larger cycle bound after this counterexample.

The two initial tail vectors coincide after REVERSING their component
order, by pi^d(x)=A^d(v_(n-d)). Their independent constructions and
cell-versus-packed updates agree on the full54 direct temporal bit
vectors,41 tail scores,11 orbit states and both exact closures.
Integration independently replays the closed vectors and checks the
earliest maxima across the entire direct-plus-tail age stream.
Sources and atomic records are the two
`check_activity_return_nonincrease_{primary,independent}.py` scripts
and `verify_activity_return_nonincrease.py` in the experiment directory,
with the three corresponding `20260906_activity_return_nonincrease_`
JSON files in `results/problem1/`.

Lead integration corrected the primary's summary length typo for x10,
its tail-preferred tie rule for the first maximum, and a non-reloadable
payload hash caused by numeric history keys becoming JSON string keys.
These corrections do not change any activity score or R value. The
executed source and admission snapshots are retained in the records;
later explanatory prose here is not silently substituted for them.

Fresh Muse adversarial review is retained in
`problem1_activity_return_nonincrease_review.md`, with exact source
hashes and lead disposition in the verification/review archive. Its
scope is this universal prescribed-block candidate. Restricting a
theorem to an infinite actual survivor is not refuted by this finite
return occurrence. Such a restriction would still need a new all-depth
mechanism; neither finite levels nor this computation supplies one.
