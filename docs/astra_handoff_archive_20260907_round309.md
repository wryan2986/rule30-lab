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

## Further round307 results (`partial-proof`)

Read `proofs/informal/problem1_exit_wait_front_residence.md`. At a one-bit
exit source v, its resetting core has an exact FORWARD first reset
L=min{n>=1:b_n in{1,3}}, with 3<=L<=p-1. Then

    delays at v,v+1,v+2: 1,L,L-1;
    injections at v,v+1: L,0;
    both physical steps preserve the clock.

The original cut thresholds are s_v=v+1 and s_(v+1)=s_(v+2)=v+L+1.
Thus the front resides on characteristic v+1 over [v+1,v+L+1), with
EXACT b(Y_(v+k))=k for 1<=k<=L, and eraser(-L,v+L). This fixes its
first residence, not the later jump/injections. Every late exit under
boundK requires L<=K. UnderK=3 the exact source core prefix is2221.
No longer wait or source prefix was sampled.

The same note gives all one-bit-source renewal alternatives:

    gate t,h=0: delays1,1,1; injections1,1;
    gate t,h=1: delays1,0,1; injections0,1;
    gate u,h=1: delays1,0,0; injections0,0;
    gate u,h=0: delays1,L,L-1; injectionsL,0.

Only the first step of the u,h=1 passage can double, precisely at a
nonresetting core with odd high-bit weight. The second step never doubles.
These are single-source statements without a future strip bound.

Read `proofs/informal/problem1_nonresetting_core_returns.md`. For a finite
initial row with Y0>0, let N_t mean identically-zero core low A-trace,
and O_t identically-one. WITHOUT FULL or a strip premise, N_t iff O_(t+2).
Positive Y0 is essential; do not use merely a nonzero seed to the right.

Under eventualK=3, all sufficiently late ODD N and O are absent. This
excludes even-parity, clock-preserving odd nonresetting extensions too.
For an EVEN FULL N source, CURRENT spatial b<=2 already suffices for:

    gate u: (d_-1,d_0)=(0,1), delay1, shadow right pair11;
    gate t: (d_-1,d_0)=(1,1), delay2, shadow right pair01.

Each returns in two physical steps to a cyclic even row with constant-one
low core trace and actual gate t; both injections are0. The t source
lies at repair offset4 in the eventual K=3 decomposition. The first step
doubles iff the high-bit weight is odd; even parity still returns.
Thus clock-preserving nonresetting returns require additional cyclic births:

    sum B >= log2(clock ratio) + count(even-parity N returns)
                            - initial I + final I.

No finite-support bound on either count, no converse from cyclic repair
to N, and no infinite FULL realization is supplied. These two new units
use exact scalar/paired derivations and original-cut identities, with NO
new experiment. Lead dispositions and missing review are recorded below.

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
and no settings changed. The second-unit fresh review was assigned to Muse
thread01a07bcc-8b83-7a02-8e97-cae2a53e2e31 and failed with the same
MissingSessionID before review text; it too is CLOSED and was not429.
The third unit received a fresh lead-only audit after those failures.
External review is explicitly missing for all three units.

Round307 owns only its new proof/review notes, fixed checker and record,
incoming archive and this handoff. Unrelated supervisor files, worktrees,
and old untracked results remain untouched. Immutable reference SHA256:
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Keep workloads local. No force-push, history rewrite, main merge, reference
edit, cloud workload, or hardware-control changes.
