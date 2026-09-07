# Astra handoff: round 10 maintenance checkpoint, 2026-09-07

Problem 1 remains OPEN. This is historical research round ten and unattended
supervisor round two. Continue on `research/astra-next`. The user requested
approximately 70 minutes, overriding the older goal-file default. Started
03:49:17 UTC. The final audit records elapsed time. This is maintenance,
NOT goal achieved, research blocked, or research exhaustion.

Read ASTRA_GOAL.md first. Incoming round-nine handoff is preserved byte for
byte in `docs/astra_handoff_archive_20260907_round10.md`. Base commit:
`043a768d6624983d7871bc99a8a4ced08f09e51b`. Do not repeat that round's
transport, highest-bit formula, physical doubling-source lateness, finite
222 construction, or failed one-hole k3 test.

## Current bottleneck and immediate verification task

FULL must still contradict finite entry for ONE fixed actual survivor.
This round replaces the vague delay-growth target with an exact injection
budget, refutes control by the current highest wait alone, and narrows the
conditional one-bit strip to bounded episodes with an exact past constraint.
It does NOT exclude any positive uniformly bounded strip, transfer these
later-row events into the original anchored Q budget, or solve period two.

FRESH EXTERNAL ADVERSARIAL REVIEW IS MISSING. The three new main notes
received independent lead derivations and a detailed lead adversarial audit,
but all authorized external-review paths failed. Resume with a fresh Muse
review (MiMo after its prescribed fallback sequence) of the EXACT current
three main notes and the recorded lead disposition. Do not claim such a
review already happened or substitute a native Codex reviewer. All results
retain partial-proof/refuted scopes; none is rigorous-proof.

## Exact delay renewal on one actual spacetime (`partial-proof`)

Read `proofs/informal/problem1_cycle_delay_renewal.md`.
For eventually A-periodic y, put T=tau(y), z=2y+a. Projection gives
 tau(z)>=T. At time T the upper row is cyclic. If its low A-trace is
identically zero, BOTH one-bit lifts are periodic, so tau(z)=T exactly.
Otherwise there is one periodic lift; the wrong bit at time T has
 tau(z)=T+rho+1,
where rho is the first future low 1 of A^T y. The correct lift has tau=T.
This extends the previous periodic-input formula through an inherited
transient without conflating cycle entry and phase-correct completion.

For ONE actual orbit Y_(t+1)=2 A Y_t+c_(t+1), set

    T_t=max(tau_t-1,0), R_t=tau_(t+1)-T_t >=0.
    tau_(t+1)=max(tau_t-1,0)+R_t.

R_t>0 is a wrong resetting lift at inherited A-time T_t, with exact
wait rho_t+1. Its bit is e_t=r_(-T_t)(t+1+T_t), NOT automatically the
current center. Every physical doubling has R_t=0; under FULL its source
is late, so tau_(t+1)=tau_t-1 exactly. At an EVEN doubling source with
tau_t<=2, the next EVEN row is A-periodic and retains the doubled clock:
tau_(t+2)=0. This does not control later births.

With H_t=t+tau_t, H_(t+1)=max(H_t,t+1)+R_t. FULL doublings lie on plateaus
of H. For V_N=#{t<N:tau_t>0}, D_N=log_2(p_N/p_0),

    sum_(t<N) R_t=tau_N-tau_0+V_N >= D_N-tau_0.

Finite entry plus one fixed finite original right fringe forces clock
growth, hence infinitely many distinct R_t>0 as well as infinitely many
doublings. With eventual bound K>=1, at least (D_[M,N)-tau_M)/K later
injections are necessary. An infinite sum of bounded injections is still
allowed. No anchored-budget upper bound has been obtained.

## The current highest wait alone is insufficient (`partial-proof` / `refuted`)

Read `proofs/informal/problem1_highest_wait_nonforcing.md`.
For EVERY positive finite x, tau(2^n x) tends to infinity. Proof: these
onsets are nondecreasing under spatial deletion. A uniform bound H would
make every 2^k T^H(x) cyclic. But an entirely cyclic zero-extension tower
must have unbounded periods by the finite-code count; at a doubling, its
first extension has code (b,0) visiting both bits, and the second zero
extension obeys w'=b OR w from 0 and cannot be cyclic. Contradiction.

For y_n=2^n*7, sigma^n cyc(y_n)=cyc(7)=6, whereas sigma^n y_n=7.
The highest disagreement is exactly bit n, its common next bit is 1,
and its first erasing wait is exactly ONE for every n. Nevertheless
 tau(y_n)->infinity.
This refutes EVERY universal finite-valued bound tau(y)<=f(current highest
wait) on initially finite rows. It is not a FULL counterexample.

Actual seed-7 rows are Y_n=A^n(2^n*7), with onset
max(tau(2^n*7)-n,0). The new divergence gives NO control of that difference.
Do not infer actual lag growth, finite-entry exclusion, or a growth rate.

For one finite row under A alone, the whole delay is the SUM of successive
highest-bit erasing waits, with each new highest index evaluated after the
preceding erasure. Indices strictly decrease. Lower differences may vanish
while waiting; initial per-bit waits cannot replace the evolved history.
No claim all these later waits are bounded in the counterfamily is made.

## Conditional one-bit strip: exact episodes and an actual past constraint

Read `proofs/informal/problem1_one_bit_strip_return_constraint.md`.
Assume tau(Y_t)<=1 for ALL sufficiently late PHYSICAL times. The bit-depth
transport then gives b(Y_t)<=1 at all late times. A single row with tau=1
DOES NOT imply this spatial bound. Under FULL, an even lag-one row has
actual low pair 3 and cycle-completion low pair 2.

For the ACTUAL paired gate q_m and late even rows X_m:

    lag1 + t gate -> lag1,
    lag1 + u gate -> lag0.

The first follows from return-map suffix H_1 H_2 being constant 2.
For the second, no-uu forces the first input b_2=2. A {0,2} tail keeps
start 3 recurrent; a resetting return has its recurrent start in {1,3}.
A wrong start stays distinct after that first H_2 and would give lag>=2,
which is excluded by the hypothesis. Thus the successor is cyclic.

Since u gaps are 2 through 5, each lag-one episode lasts at most five
even rows. Only even physical doublings are possible under this bound.
A doubling cannot be the first lag-one row after a cyclic row. Let u be
its pure completion, contained in {0,2}, and v the previous completion.
Then Phi u=shift^2 v. If the predecessor were cyclic, v_0=3 would force
u_-2,u_-1=2,0, making v_1=2 and hence two adjacent actual u gates.
Therefore the predecessor is lag1 with gate t, and

    (u_-2,u_-1,u_0,u_1,u_2)=(0,2,2,2,2).

These negative indices are phases of a PURE periodic code, not negative
actual physical times. A doubling episode has between two and five
lag-one even rows. This extra past condition is not satisfied by the
old period-one and period-four local controls; their original assertions
remain valid. No larger finite-source supply was searched.

The unclosed step is the actual lag0->lag1 birth. Its periodic return
still depends on the complete temporal driver, so the gate/lag pair is
NOT a proved autonomous quotient. Infinite distinct bounded episodes
remain possible as far as these results establish.

## Verification, failures, provenance, and stopping fence

Lead audit and exact missing-review log:
`proofs/informal/problem1_round10_fresh_review.md`.
Muse sidecar: `problem1_round10_bounded_strip_sidecar.md`.
The sidecar's local strip update reads one higher driver bit for K>=2;
K=1's low bit alone follows the prescribed center. Its two distinct-row
witness does not refute an actual-orbit quotient. Earlier overclaims and
incorrect witness formulas were removed and their bytes archived.

Contributor Muse thread 01a079fc-e3db-7d60-b020-d44d6e2fc3df succeeded on
its corrected fixed controls at 04:14:49 UTC, then ended in provider429.
Its paused retry 01a07a1c-fc5f-7841-8d55-db256cdb0955 failed with
MissingSessionID. Fresh Muse reviewer threads 01a07a0a-1bc7-7d21-8fc3-66773ab511fc
and 01a07a0e-efc3-7d40-aebf-88cba6266fd2 both failed with429, with one
paused retry. Mandated MiMo threads 01a07a11-ebc6-7481-9430-ece38b783ad8
and 01a07a1e-912e-7793-8b8a-e29f34e10976 failed with400 missing session
metadata. All six threads are CLOSED; no worker remains pending.

One isolated request to the same configured MiMo provider with explicit
session metadata failed with403/error1010. No external review text exists.
Exact credential-free request/response and runner bytes:
`results/problem1/20260907_round10_mimo_direct_review.json`;
runner `experiments/problem1_nonperiodicity/review_round10_mimo.py`.
No native model substituted and no provider configuration changed.
A CLI endpoint-inspection command incidentally reported automatic
Codex-launcher backup/shim refresh; no research file was changed by it.

The only scientific inputs were y in {0,2,3,6,7,12}, a in {0,1}:
twelve one-bit lifts. Integer/dictionary and tuple-cell/list orbit loops
agree on complete trajectories, repeats, least onsets, periods, phase-cyc,
and lift choices. All sixteen hand transitions agree. Checker:
`experiments/problem1_nonperiodicity/check_round10_delay_renewal.py`.
Final atomic result: `results/problem1/20260907_round10_delay_renewal.json`.
This is finite-exhaustive ONLY over those controls, not proof of any
infinite result or machine verification of the strip-return theorem.

Exact superseded checker/memo/result bytes, including the initially
unenforced caps and later corrections, are in
`results/problem1/20260907_round10_superseded_run.json` (four snapshots).
One lead run passed all mathematics but failed its cap report because
RUSAGE_SELF inherited a 199.297-MiB launcher peak. Snapshot4 retains it.
The unchanged checker was rerun from a small Python parent; all checks
and the SAME 60-second/128-MiB limits passed. The wrapper is recorded in
the lead audit. Historical archive-capture runtimes were not measured;
metadata completion reports its own runtime instead of inventing theirs.

Round audit/builder:
`results/problem1/20260907_round10_audit.json` and
`experiments/problem1_nonperiodicity/audit_astra_round10.py`.
It checks exact current artifacts, dependencies, canonical payloads,
all four archival versions, and recovery of the incoming handoff from
its base Git tree. It introduces zero scientific inputs.

Do not repeat the new renewal derivation, shifted-row no-go, K1 return
maps, 02222 past constraint, or successful scalar controls. Do not expand
prefixes, periods, lag/width boxes, source words, the failed one-hole
family, or fixed-width graphs. After missing external review, attack the
actual resetting lifts/cycle-to-lag births with the complete original
right fringe, or find a valid transfer to the original anchored budget.
Periods >=3 and the older B_all/signed directions retain prior statuses.

## Checkpoint state

The established logical unit is ready for the scoped commit/push after
its artifact audit. The final maintenance update will record that commit
and remote verification. This checkpoint is not research exhaustion.

Unrelated repository supervisor files and old untracked results remain
untouched. Immutable reference SHA256:
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Never force-push, modify the reference, or merge to main.
