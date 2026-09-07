# Astra handoff: supervisor round307 research checkpoint, 2026-09-07

Problem1 remains OPEN. Continue on `research/astra-next`. This is a routine
checkpoint, NOT goal achieved, research blocked, or exhaustion. Round307
base is `0376025e8647918d5bcb62ca83421e62af349542`. The incoming round306
handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260907_round307.md`, which is AUTHORITATIVE for
all earlier statements, dependencies, checks, and stopping fences.

## Current bottleneck

FULL must contradict finite entry for ONE actual survivor with its COMPLETE
original finite right fringe. Under eventual K=3 (including K=1 and K=2),
infinitely many cyclic-source births are mandatory. No finite-support upper
bound on their nonnegative count is proved. Without an eventual strip bound,
the original global-front transport and bounded-reuse obligation remain open.

Round307 now fixes the full-driver phase deciding the one-bit exit. Read
`proofs/informal/problem1_full_driver_exit_phase.md`. Status: `partial-proof`,
with fresh external review missing. At an even one-bit source x=z+1,
z=cyc(x), b=Theta(z), b_0=2:

* If b contains 1 or3, put ell=max{s<0:b_s in{1,3}} and let gamma be
  the parity of 2s strictly between ell and0 in the PURE periodic code.
  The global shadow's right bit is h=1[b_ell=1] XOR gamma. At an actual
  u gate the exit occurs exactly when gamma=1[b_ell=1]. No exit instead
  requires gamma=1[b_ell=3]. Lookback may use the whole period.
* If b is contained in{0,2}, the actual one-bit transient selects the
  shadow right pair11, even when the one-bit lift has an even-parity fork.
  The proof uses A(2x+a)=2Az to fix the phase, then the unique constant-one
  second lift. Independently the paired invariant set{1,3} gives
  cyc(4x)=4z+3 on the actual u branch. Such a source returns to a cyclic
  even row two steps later WITHOUT any future strip premise. Its first
  physical step doubles iff the number of 2s per least period is odd.

Thus every K=3 repair starts from a RESETTING periodic core. A nonresetting
phase fork is not a free choice of exit versus return on this fixed orbit.
The old fork certificate remains valid on its original domain.

The necessary infinite birth test from round305 resets on code letters1/2
and counts trailing3s; the new resetting no-exit test resets on1/3 and counts
trailing2s. They concern the complete successive cores selected by the SAME
actual boundary. They do not form two independently chosen streams or a
finite-state update. No simultaneous infinite compatibility/exclusion is
proved. Do not enumerate more backward suffixes, cores, forks, or prefixes.

## Preserved round306 frontier

The incoming archive contains the full proofs and checks. In particular:

* Eventual all-physical tau<=2 iff eventual tau<=1. Odd physical doubling
  forces the NEXT even spatial depth>=3; a one-bit exit reaches b=3 at
  its extra odd step. This is conditional, not an eventual bound.
* Eventual all-physical tau<=3 iff eventual EVEN-time tau<=2. One late
  entry followed by one-bit passages and exact six-step repairs covers
  the late orbit. Eventually there are no odd doublings and infinitely
  many cyclic even returns.
* A repair from v has gates u,t,t,t at offsets0,2,4,6, shadow first-right
  bit0 at v+4, and endpoint center discrepancy e=1 XOR hat r2(v+4).
  Its spatial profile is1,1,2,3,2,3,e; delays1,3,2,3,2,1,e; injections
  3,0,2,0,0,e. A doubling can occur only at offset4 and forces e=0.
* If K=3 but not eventual K=1, there are infinitely many disjoint repairs.
  They cannot replace the required cyclic births: every doubling ends a
  noncyclic episode, so births>=log2(clock ratio)-initial I+final I.
* For original cuts s_j=tau(L_j), the global front is J(u)-u with
  J(u)=min{j:s_j>u}. Injections are disjoint residence portions after
  crossing the center. Their erasers are outside the original anchored
  set; neither ordering nor path parity bounds reuse of initial ancestors.
* E is one idempotent U-commuting shadow. Every finite actual rebase leaves
  infinitely many right discrepancies. The actual center escapes the
  fixed windows of the valid dyadic SU limit. No FULL shadow center follows.

## Round307 verification and ownership

Lead review: `proofs/informal/problem1_round307_review.md`.
Fixed checker/atomic record: `check_round307_exit_phase.py` /
`results/problem1/20260907_round307_exit_phase.json`. Eight scalar values,
sixteen map compositions, four invariant-pair transitions, two first-step
pair values, and the four named 7/6 orbit certificates pass. Hand values
precede packed/cell comparison. Ten-second/128-MiB caps and six-source and
canonical-payload hashes were audited. No source or FULL prefix was searched.

Muse sidecar thread01a07bb5-26b5-7111-9465-72a109c94737 and fresh review
thread01a07bc1-fdfc-75a1-9667-347c9f3adc2e both failed before work/review text
with MissingSessionID (missing x-opencode-session). Both CLOSED. Neither
was429; MiMo was not advertised. No native/other provider was substituted
and no settings changed. External review is explicitly missing.

Round307 owns only its new proof/review notes, fixed checker and record,
incoming archive and this handoff. Unrelated supervisor files, worktrees,
and old untracked results remain untouched. Immutable reference SHA256:
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Keep workloads local. No force-push, history rewrite, main merge, reference
edit, cloud workload, or hardware-control changes.
