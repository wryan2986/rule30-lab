# Astra handoff: supervisor round306 working checkpoint, 2026-09-07

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

Round306 reduces eventual all-physical K=2 to K=1. The K=1 birth/no-exit
constraint from round305 remains open. Ranked next routes (`heuristic`):

1. Retain the whole actual/global-shadow pair and the complete periodic
   driver at each cyclic return. Control the simultaneous infinite birth
   supply and no-exit condition using the original finite support. The new
   reduction means an exclusion of eventual K=1 would also exclude K=2.
2. For a possible structural extension beyond two bits, first identify what
   prevents a third-bit excursion from repairing. The new third-bit result
   ALONE does not iterate to arbitrary K. Do not launch width or gate sweeps.
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
t would give d_1=1 with common bit2=0 and force b_(t+1)>=3. Consequently
all late doublings in this conditional case already have even gate u and
negative-half agreement at the source. This is consistent with the old
K=1 episode law; it supplies no finite birth budget.

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
`check_round306_two_bit_collapse.py` and atomic
`results/problem1/20260907_round306_two_bit_collapse.json` verify sixteen
fixed Boolean assignments with independent physical truth-table and packed
A-cut implementations, after eight hand rule values. Ten-second/128-MiB
caps passed. Six source hashes and the canonical payload hash were audited.
This checks local algebra, not E membership, infinite FULL, or the theorem's
all-depth induction. No new rigorous-proof status is assigned.

Muse incoming-review thread01a07b76-3648-75b1-81f9-796b6893e2c6 and fresh
collapse-review thread01a07b83-13c1-7e31-946c-22d09696f35d both failed before
review text with MissingSessionID (missing x-opencode-session); both CLOSED.
Neither was429. MiMo was not advertised; no native/other provider was
substituted or settings changed. External review is explicitly missing.

Round306 owns only its new proof/review notes, fixed checker and atomic
record, incoming handoff archive, and this handoff. Unrelated supervisor
files, worktrees, and old untracked results remain untouched. Immutable
reference SHA256 remains
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Keep workloads local. No force-push, history rewrite, main merge, reference
edit, cloud workload, or hardware-control changes.
