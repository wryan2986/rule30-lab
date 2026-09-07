# Astra handoff: supervisor round306 maintenance checkpoint, 2026-09-07

Problem1 remains OPEN. Continue on `research/astra-next`. This is a routine
checkpoint, NOT goal achieved, research blocked, or exhaustion. Read
ASTRA_GOAL.md first; do not repeat settled work. Round306 base was
`1f1818d49ebd3824d98a316c0056d7cf9f50010e`. The incoming round305 handoff is
preserved byte for byte in `docs/astra_handoff_archive_20260907_round306.md`.
That archive links the full round304 and earlier handoffs and remains
AUTHORITATIVE for their exact statements, dependencies, and stopping fences.

## Current bottleneck and next attack

FULL must contradict finite entry for ONE actual survivor with its COMPLETE
original finite right fringe. Renewal forces infinitely many delay injections
and clock doublings; no finite budget or eventual strip bound is proved.

Round306 reduces eventual all-physical K=2 to K=1, and gives a complete
conditional decomposition under K=3 into one-bit passages and exact
six-step exit repairs. The K=1 birth/no-exit constraint from round305
remains open. Ranked next routes (`heuristic`):

1. Retain the whole actual/global-shadow pair and the complete periodic
   driver at each cyclic return. Control the simultaneous infinite birth
   supply and no-exit condition using the original finite support. The new
   collapse means an exclusion of eventual K=1 would also exclude K=2.
   The final birth-count corollary below makes a finite cyclic-birth budget
   sufficient to exclude eventual K=3 as well, without counting every repair.
2. Under eventual K=3, control the FULL-SHADOW repair flag at the six-step
   exits below. A distinct K=3 alternative must sustain infinitely many
   disjoint repairs, each with mandatory injections3 and2. Repair is now
   exactly characterized conditionally; do not redo the local table or
   try to exclude it solely because the third bit is reached.
3. Without an eventual strip bound, use the global front residence identity.
   A charge to the finite anchored set after ONE even rebase still needs
   distance-growing transport AND bounded reuse. Path existence or XOR
   path parity is not a nonnegative budget.

Do not enumerate more source words, clock trees, local neighborhoods,
shift-tower samples, front samples, or longer gate prefixes merely to
illustrate the known obstructions. Keep the original actual finite fringe;
the global shadow's infinite right fringe cannot replace it.

## New K=2-to-K=1 reduction (`partial-proof`)

Read `proofs/informal/problem1_two_bit_strip_collapse.md`.
For one nonzero finite FULL orbit with its global E shadow,

    eventual tau(Y_t)<=2 iff eventual tau(Y_t)<=1,
    eventual b(Y_t)<=2 iff eventual b(Y_t)<=1.

No antecedent is established. The proof is conditional and fresh external
review is missing. The two new local facts are:

* An ODD physical clock doubling at t forces b(Y_(t+1))>=3. At that next
  even row the shadow HIGH A-trace is identically zero. FULL fixes actual
  bits0..3 to (1,1,u,1 XOR u). If b<=2, bits2,3 agree; the shadow's next
  high bit would instead be (1 XOR u) XOR u=1, a contradiction. This is a
  spatial bound, NOT a claim tau(Y_t)>=3.
* The round305 one-bit exit at an even u source v has only a -1 defect on
  the negative half at v+2. Actual no-uu gives gate t there, hence shared
  cell -2=0. The defect reaches -2 at v+3 and b(Y_(v+3))=3 EXACTLY.

Thus under eventual b<=2, entry into negative-half agreement at any late
EVEN row is permanent: the one-bit table's only exit would violate b<=2
at that extra odd step. A late doubling exists by unbounded clocks and must
be even by the first fact. With tau<=2, the imported two-step consumption
law gives a CYCLIC even successor at t+2. This provides entry; threshold
transport then yields eventual tau<=1. No finite-to-infinite census, bounded
clock, row-wise equality b=tau, or general induction on K is used.

Additionally, under b_t,b_(t+1)<=2 an even doubling source cannot have gate
t: its shadow center and next A low bit are0, forcing shadow bit1=u. Gate
t would give d_-1=1 with common bit2=0 and force b_(t+1)>=3. Consequently
all late doublings in this conditional case already have even gate u and
negative-half agreement at the source. This is consistent with the old
K=1 episode law; it supplies no finite birth budget.

## New K=3 repair and eventual decomposition (`partial-proof`)

Read `proofs/informal/problem1_three_bit_exit_repair.md`.
Assume eventual b(Y_s)<=3 (equivalently eventual all-physical tau<=3).
At a late even one-bit exit source v, the actual gate is u, center
discrepancy is1, and shadow r_1(v)=0. Put

    (h,k)=(hat r_1(v+4),hat r_2(v+4)).

Necessarily h=0; the actual gates at v,v+2,v+4,v+6 are u,t,t,t.
At v+6 every negative position agrees and the center discrepancy is
e=1 XOR k. The exact profiles at offsets0 through6 are

    spatial b: 1,1,2,3,2,3,e,
    A delay:   1,3,2,3,2,1,e,
    R at offsets0 through5: 3,0,2,0,0,e.

The proof uses a t-source with a -1 defect and center discrepancy ell.
Under b<=3 its next gate MUST also be t. Its next even negative half
agrees at every position<=-2, and the pair (d_-1,d_0) becomes

    ell=0: (1,1),
    ell=1: (h,hat u), with hat u=indicator[(h,k)=00].

If h at v+4 were1, this repeats and forces FIVE consecutive actual t
gates at v+2,...,v+10, impossible. The future strip premise through those
extra times is essential. This gives the repair, not an infinite model.

At most one clock doubling occurs in [v,v+6), and it can only be the
even step v+4 -> v+5. If it occurs, the repair is cyclic (e=0). Cyclic
repair does not conversely imply doubling. Repeated repairs are not bounded.

For ORIGINAL cuts, the same profile fixes

    (s_v,...,s_(v+6))=(v+1,v+4,v+4,v+6,v+6,v+6,v+6+e).

Its two mandatory front residences are characteristic v+1 over [v+1,v+4)
and characteristic v+3 over [v+4,v+6). Their erasing 1s occur at
(-3,v+3) and (-3,v+5). This exact translation uses no new front sample
and supplies no claim of distinct original ancestors or bounded reuse.

The new flag also has an exact initial-shadow expression: if the shadow
right bits at v are (0,a,b,c,d), then

    h=(1 XOR a)*(1 XOR b)*(c OR d), hence this product must be0.

The shadow's own center inputs0,1,1,1 for these four steps are derived
from THIS exit. Do not impose them at unrelated times or treat a,b,c,d
as freely chosen; they belong to the original globally selected E shadow.

The same note proves ONE late entry, not merely a conditional passage:

* An even FULL row with identically-one shadow LOW A-trace is cyclic
  under the future b<=3 premise. A center-agreeing bit2 defect would leave
  the strip next step; a remaining bit1 defect would leave two steps later.
* Every doubling has that constant-one shadow low trace two physical
  steps later. Thus every late EVEN doubling returns to a cyclic even row
  at t+2 and has source delay<=2.
* A late ODD doubling must have delay2. Its next even row has all three
  low discrepancies1 but delay1; two steps later the negative halves agree.
  The alternative center-agreeing successor would have delay>2, violating
  clock consumption and the eventual bound3.

Unbounded clocks supply an entry of either parity. Thereafter the one-bit
table and six-step repairs cover the entire late orbit. In particular all
late EVEN depths are<=2, and there are NO late odd doublings. This does
NOT give all-physical depth<=2: the repair's odd depths remain3.
Infinitely many remaining even doublings give infinitely many cyclic even
returns, with no proved uniform gap bound between those returns.

Consequently

    eventual all-physical tau<=3 iff eventual EVEN-time tau<=2.

An eventual even-time delay bound1 instead implies eventual K=1 via the
two-bit-collapse theorem. If K=3 holds but eventual K=1 does not, there
must be infinitely many disjoint six-step repair passages. No finite bound
on those passages or their mandatory3,2 injection pairs is proved.

The cyclic birth supply remains mandatory even with repairs. For late paired
rows X_m=Y_(2m), put I_m=indicator[tau(X_m)>0] and
B_m=indicator[I_m=0,I_(m+1)=1]. Every doubling is a 1->0 switch, so

    sum_(m=M..N-1) B_m
      >= log_2(p(X_N)/p(X_M)) - I_M + I_N.

Here B_m=indicator[I_m=0]*(u_(2m) XOR hat u_(2m)), the SAME cyclic-source
birth observable from round305. Hence infinitely many such births are
necessary also under K=3; repeated internal repairs cannot replace them.
No finite-support upper bound on this nonnegative count is proved.

## Preserved round305 birth, exit, and global-front facts

The incoming archive supplies full details. In particular:

* At an even CYCLIC FULL row, actual/shadow right-pair zero flags u,hat u
  give tau at the next odd row0 and the next even row u XOR hat u. The
  shadow flag is the parity of 3s after the last1/2 in the negative PURE
  periodic code. That lookback can use the whole period.
* At a current one-bit source with center discrepancy ell=1, a t gate
  preserves the center defect; a u gate returns iff shadow r_1=1 and exits
  iff shadow r_1=0. The exit has center agreement but a -1 defect, and its
  intervening odd delay is at least2. The future one-bit strip assumption
  was essential to exclude that branch. Round306 now locates the third bit.
* For ORIGINAL cuts, s_j=tau(L_j), J(u)=min{j:s_j>u}, global leftmost
  discrepancy m(u)=J(u)-u. Residence at j is [s_(j-1),s_j); positive
  physical injection R_t counts its portion u>=t+1. Those intervals are
  disjoint but do not give bounded reuse of original ancestors. Clock
  doubling characteristics have s_j=s_(j-1) and are skipped entirely.
* The exact full-driver discrepancy recurrence unrolls to weighted path
  PARITY. The fixed112 control has cancelling active paths. Swapping the
  OR factorization changes individual paths, so reachability is not a
  positive event count and coefficients cannot be frozen across row changes.
* E is an idempotent, U-commuting whole-row shadow assembled from ORIGINAL
  phase-correct cuts. Its initial right discrepancy supply is infinite at
  every finite actual rebase. The dyadic SU limit is valid on fixed windows;
  the actual center escapes those windows. No FULL shadow center follows.
* The general summary (complete core, exact delay, complete one-bit phase
  map) does not update: sources110/112, same zero child, yield distinct
  next phase maps. This is a same-cycle phase counterexample, not FULL.
* tau(y)<=bitlen(y)-1 is refuted by144 (width8, delay8). Seed9 at physical
  time4 gives delay4>L-1=3, with the same zero right fringe, but is not FULL.
  No width-plus-constant or eventual bound was refuted; no intercept fitted.

The earlier sharp reset distance, finite anchored capacity after one even
rebase, finite-observation no-go, cycle fork, and K=1 episodes of at most
five even rows remain unchanged. Do not reopen their settled searches.

## Verification and review

Lead dispositions: `proofs/informal/problem1_round306_review.md`.
Two fixed checker/atomic record pairs have prefix `check_round306_` /
`results/problem1/20260907_round306_`:

* two_bit_collapse: sixteen Boolean assignments after eight hand rule values.
* three_bit_repair: sixteen t-source transitions, sixteen four-step flags,
  thirty-two constant-one implications, thirty-two odd-entry controls;
  eight hand rule values and one hand four-step cone precede them.

Separate truth-table and packed implementations agree. Both ten-second/
128-MiB caps passed. Both six-source manifests and canonical payload hashes
were audited. The final notation audit uses d_-1 for the physical left
neighbor and delta_j=d_(-j) for bit-index differences; records are refreshed
against the final proof sources.
This checks local algebra, not E membership, infinite FULL, or the theorem's
all-depth induction. No new rigorous-proof status is assigned.

Muse incoming-review thread01a07b76-3648-75b1-81f9-796b6893e2c6 and fresh
collapse-review thread01a07b83-13c1-7e31-946c-22d09696f35d both failed before
review text with MissingSessionID (missing x-opencode-session); both CLOSED.
Neither was429. MiMo was not advertised; no native/other provider was
substituted or settings changed. External review is explicitly missing.
The later three-bit unit received its own fresh Muse review assignment,
thread01a07ba6-4d51-7be3-9f38-ca0d4b6ef219. It failed with the same
MissingSessionID before review text and is CLOSED. Thus all three attempts
failed, and Section4 of the round306 review remains explicitly lead-only.

Round306 owns only its new proof/review notes, two fixed checkers and atomic
records, incoming handoff archive, and this handoff. Unrelated supervisor
files, worktrees, and old untracked results remain untouched. Immutable
reference SHA256 remains
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Keep workloads local. No force-push, history rewrite, main merge, reference
edit, cloud workload, or hardware-control changes.
