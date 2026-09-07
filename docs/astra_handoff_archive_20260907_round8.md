# Astra handoff: round 7 maintenance checkpoint, 2026-09-07

Problem 1 remains OPEN. This is time-maintenance rollover, not goal
achieved, research blocked, or research exhaustion. Research continues on
`research/astra-next` across the next supervisor round.
Round seven began 2026-09-06 at 23:32:42 UTC. The user requested about
70 minutes, overriding the goal file's earlier 50–60 minute default.
The final atomic audit records checkpoint time and total elapsed seconds.
Read ASTRA_GOAL.md first. Incoming round-six handoff preserved byte for
byte in `docs/astra_handoff_archive_20260907_round7.md`.

## Current bottleneck

FULL must contradict finite entry for ONE FIXED ACTUAL survivor. Round six
put both conditions in the same code; round seven now classifies exactly
when an inverse scan resets and doubles its eventual temporal period.
The incompatibility itself is still unproved. Do not repeat the incoming
round-six anchored equivalence, mortality period tower, or full diagonal.

Read new notes in proofs/informal:

1. `problem1_inverse_scan_reset_language.md`.
2. `problem1_scan_cycle_entry_obstruction.md`.
3. `problem1_scan_doubling_cycle_lag.md` and its scoped review.
4. `problem1_inverse_scan_reset_language_review.md`, with Sec8 withdrawing
   the reviewer's false generic-shadow objection.

The original full-fringe/anchored formulas and all older stopping fences
remain in the incoming handoff archive. In particular full scans adjoin
initial spatial pairs, not free gate choices; never replace their original
fixed boundary by repeated resets at each actual block.

## New exact all-word reset and period theorem (`partial-proof`)

H_i(a)=h(a,i), maps in state order0,1,2,3:

    H0=[0,1,3,3], H1=[3,2,2,2],
    H2=[2,3,1,1], H3=[1,0,0,0].

For chronological input word w, H_w is NONCONSTANT exactly for

    {0,2}* UNION {0,3}* UNION {0,3}*{1,2}.

The last factor means one final 1 OR2. A six-image-set induction proves
this at every length; no enumeration ran. For b with LEAST eventual
period p and onset T, I_a b has available onset <=T+p+1 and exact period:

- zero tail:1;
- tail in {0,2}, with2: p or2p according to even/odd count of2;
- tail in {0,3}, with3: p or2p according to even/odd count of3;
- tail contains1 or both2,3: synchronized, period exactlyp.

In both doubling cases the output period contains1. Thus no two successive
inverse scans double, and for ANY initial right symbols,

    p_m=p_0*2^(d_m), d_m<=ceil(m/2).

No assertion that a diagonal sample lies in its periodic tail is made.

## A necessary late-cycle-entry condition (`partial-proof`)

With the original B_m=Theta(W_m), C_m=shift^(2m)B_m=Theta(X_m), FULL
means C_m(0)=3. FULL plus finite entry and a finite right fringe implies

    tau_A(W_m)>2m for infinitely many m,

where tau_A is the first entry onto an A-cycle. Equivalently C_m fails
pure temporal periodicity infinitely often. Every W_m is finite-entry
at the SAME h because pi^m A^h W_m=A^h x; every tau is finite.

If all late C_m were pure-periodic, their recurrent3 would exclude the
{0,3} scan case (next recurrent alphabet {0,1} cannot start3). All steps
then synchronize and preserve one period p. The deterministic bridge
C_(m+1)=I3 shift^2 C_m stays in a finite set of p-periodic codes, making
X_m eventually repeat. But after finite entry,
X_(m+1)=4 A^2 X_m+3 increases finite positive bit length by EXACTLY2.
Contradiction. NO Kopra/literature dependency is needed for this proof.
This condition also applies to every infinite PERMITTED F orbit with
finite entry; it is not an actual-fringe-only discriminator.

## Clock doublings force specific late source diagonals (`partial-proof`)

For a FIXED nonzero finite-entry x and finite initial fringe ending at J,
write y=W_J, Y=T^h y. Then Y is finite positive, including when A^h x=0,
and for m>=J+h,

    A^h W_m=4^(m-J-h)Y.

Its positive finite width grows by2 per scan. Finite A-cycle states of
period<=P form a finite union of finite Theta-code sets, so p_m tends to
infinity. Explicitly a finite cycle of widthL and periodp obeys
ceil(L/2)<=4^p-1: its nonzero Phi-deletion words before the first zero
are all distinct. No code/cycle list was computed.

Under FULL, original B_m symbols at2m,2m+1,2m+2 are respectively3,
1/2,1/2. The last statement uses the NEXT permitted gate and
C_(m+1)=I3 shift^2 C_m. At a doubling source m:

- tail{0,2}: tau_A(W_m)>2m;
- tail{0,3}: tau_A(W_m)>2m+2 (lag at leastTHREE), and the successor
  is late as well because its tail lies in{0,1}.

Thus EVERY doubling has its own late SOURCE diagonal, and

    #{0<=m<N:tau_A(W_m)>2m} >= log_2(p_N/p_0) -> infinity.

This is a count of late depths, NOT unbounded lag heights, positive
frequency, or original anchored activity. The same mechanism applies to
the larger infinite-permitted-F class (count positive current-row
preperiods there; do not use the original W_m/2m threshold on F states).

Further exact local lemma: ifx is A-periodic and permitted, F(x) keeps
its period and has least A-preperiod0 or1. Exactly ONE of
4 A^2 x+2 and4 A^2 x+3 is periodic; the other has preperiod1. The
period return map has image contained in{2,3} and identifies2/3 at its first letter.
The fixed55 example below realizes the one-step defect, not core invariance.

## Two tempting local cycle-entry shortcuts are refuted

Hand certificate (no machine run): x55 is on the A-cycle55<->50 and
lies in the u gate. F55=223 has A orbit223->200<->222, so its entry
height is1 rather than0. For the actual zero right fringe, W1=220 has
orbit220->201->223->200<->222, entryheight3>2. D0=D1=3: this includes
one actual valid alternating block. Temporal check:

    Theta55=(3,2)^infinity,
    I0 Theta55=0,1,3,0,2,0,2,... .

But223 mod16=15 fails BOTH gates, so this is no infinite survivor. It
refutes preservation of the A-periodic core under permitted F and a
universal two-step cycle-entry bound for a zero appended pair. It does
NOT refute eventual entry by2m for one fixed x or the FULL-conditioned
version of such a hypothesis.

## Verification and continuation

One Muse worker, `opencode-go/muse-spark-1.3-contributor`, thread
01a07911-f233-7760-b1a3-fefa4d2ff2d9, reviewed the exact table, language,
least periods, onset, full-fringe implication and fixed certificate.
Lead independently audited and accepted the corrected review. Its initial
claim that periodic Theta(X) need not make X periodic ignored Theta's
full all-time injectivity; withdrawn after an independent rederivation.
The equivalences were NOT weakened. The first sidecar's comparison of
2m with an UPPER transient bound was also rejected, and its missing entry
height and W=0 edge case corrected. No provider429 or fallback occurred.

Atomic round provenance: `results/problem1/20260907_round7_audit.json`,
builder `experiments/problem1_nonperiodicity/audit_astra_round7.py`.
It authenticates current reviewed sources, exact rejected initial review,
dependencies, fullGit, timings, software/hardware, immutable reference and
incoming handoff. No new scientific program, search, vector set or run.

Established core checkpoint aa919d6 is pushed. The next missing step is
an ACTUAL full-boundary obstruction to the infinitely required transient
passages at {0,2}/{0,3} clock doublings. The generic permitted gates allow
the local one-step cycle defect, so their mere existence supplies no
contradiction. Neither universal eventual entry by2m, unbounded lag
heights, nor exclusion of eventual restricted temporal alphabets is proved.
No count/prefix census is admitted. Second established checkpoint04954ef
is pushed; the later maintenance commit is in Git history.

## Final review and restart point

The primary Muse worker was closed after its corrected scoped reviews.
A SECOND Muse worker started in a fresh context for final adversarial
review: thread01a07942-51c5-7812-8916-5235d1244eea, same mandated model.
Fresh review: `proofs/informal/problem1_round7_final_review.md`; all
three sources accepted at their stated partial-proof/refuted scopes after
independent hand derivation, with no prior review verdicts consulted.
The lead independently rechecked the full claims and accepted the review.
Both workers are CLOSED; no pending review or worker remains. The final
handoff audit also corrected the return-image shorthand to CONTAINED in
{2,3}, consistent with the source's subset claim (not equality).
The audit builder distinguishes the two review roles and retains the
fresh review's exact window, 00:26:31–00:30:00 UTC, plus dated metadata
followups. All computation this round is archival integrity work;
mathematical tables, the fixed55 certificate, and infinite continuations
were derived by hand and independently reviewed. No numerical search
or scientific simulation ran. Repository-only recovery of the rejected
initial review is tested with /tmp history disabled before the final push.

Restart from the actual compatibility gap, using the exact necessary
doubling passages. The first route in this round (generic eventual-period
bounds) alone was insufficient; its overclaimed no-go was rejected. The
second route (exact reset words) gave the source-gate delay mechanism. A
local cycle-entry induction was falsified by55. All-depth control of the
required transient passages at the ORIGINAL fixed fringe remains the
strongest next attack. The wider permitted-F setting is a necessary
control, not evidence that its conditions isolate the actual survivor.

Do not repeat any round-six activity/mortality proof or the round-seven
reset classification, width count, cycle-mate lemma, or55 certificate.
No prefix, period, inverse word, denominator, cycle width or lag sweep is
admitted by this checkpoint. Problem1 periods>=3 and B_all/signed
nonvanishing retain their prior status and are not investigated here.

Unrelated supervisor files, ASTRA_GOAL.md, .worktrees and old untracked
results remain untouched. Immutable reference SHA256:
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Never force-push, change that reference, or merge this branch to main.
