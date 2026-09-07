# Astra handoff: round 9 maintenance checkpoint, 2026-09-07

Problem 1 remains OPEN. This is routine time maintenance, not goal
achieved, research blocked, or research exhaustion. Continue on
`research/astra-next`. This was historical research round nine and
unattended supervisor round one. Started 02:41:05 UTC; the user requested
approximately70 minutes, overriding the older50–60 minute goal-file default.
The final atomic audit records checkpoint time and elapsed seconds.
Read ASTRA_GOAL.md first.

Incoming round-eight handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260907_round9.md`. Base commit:
`28f5570d622ceb50bcd5b9e2f78d9c579e2ed419`. Do not redo its varying-input
bounded-lag family or the earlier reset-language, clock tower, anchored
finite-entry equivalence, full diagonal, width count or fixed55 certificate.

## Current bottleneck

FULL must contradict finite entry for ONE FIXED ACTUAL survivor.
This round identifies exactly the spatial disagreement strip corresponding
to bounded A-preperiods, refines it to physical time, and gives the exact
waiting time to erase its highest disagreement. It does NOT exclude an
eventually fixed strip, prove unbounded lag heights, or turn later-row
activity into the original anchored Q budget.

The useful next attack is the actual future of the erasing bits in the
highest-disagreement formula below. The complete right fringe must remain
fixed. A bounded strip has an evolving higher driver with possibly unbounded
period: its finite width is NOT an autonomous finite-state closure.

## Exact transport on one orbit (`partial-proof`)

Read `proofs/informal/problem1_cycle_completion_defect_transport.md`.
For eventually A-periodic y, let cyc(y)=A^k y with k a multiple of its
LEAST eventual period beyond its LEAST preperiod tau(y). This is the
phase-correct cycle representative, not an arbitrary first cycle state.
It commutes with A and spatial deletion pi. For finite-entry y, cyc(y)
is finite; this does NOT make y initially finite.

Let kappa(y)=min{n:pi^n y is A-periodic}, possibly infinity. It equals
the number of low spatial pairs containing any disagreement from cyc(y).
For ONE infinite permitted orbit X_m=F^m x,

    kappa(X_(m+n))>n iff tau(X_m)>2n, all m,n>=0.

Thus tau_m<=K eventually implies kappa_m<=ceil(K/2) after that many more
blocks; kappa_m<=N eventually implies tau_m<=2N. Boundedness of the two
sequences is equivalent in the eventual sense. Early nonfinite finite-entry
rows may have infinite kappa; do not use their finite number as an
unbounded late-strip witness. For all sufficiently large m,

    kappa_m=min{0<=n<=m:tau_(m-n)<=2n} <=m.

Every transport is into a LATER actual row, not into the original x.
Unbounded kappa below m remains consistent with this finite-entry bound.

With Z_m=cyc(X_m), pi Z_(m+1)=A^2 Z_m. Its low pair need not be3.
If d is the highest differing BIT of X_m and Z_m, the next highest
index is d+2 exactly when the common bit d+1 is zero at BOTH A-times0,1;
otherwise it is at most d+1 (or no disagreement remains). A new low-pair
birth must be retained. Bit and pair indices cannot be interchanged.

## Physical time and the exact erasing wait (`partial-proof`)

Read `proofs/informal/problem1_physical_time_cycle_defects.md`.
For the SAME actual spacetime, Y_t is its center-and-left row,
c_t=r_0(t) is a SINGLE BIT, and sigma(y)=y>>1. Then

    Y_(t+1)=2 A Y_t+c_(t+1),
    sigma^n Y_(t+n)=A^n Y_t.

The center boundary is actual, not freely prescribed. If b(y) is the
least number of low BITS deleted to reach an A-cycle, then

    b(Y_(t+n))>n iff tau(Y_t)>n.

A late even-row preperiod boundK bounds late odd-row preperiods byK+1.
At a highest disagreementd from Z_t=cyc(Y_t), the next highest bit is
d+1 exactly when bit_(d+1)(Z_t)=0; a1 erases that top disagreement.
New low-bit births remain possible.

The one-bit inverse scan has driven maps identity, constant1, flip,
constant0 for input symbols0,1,2,3. For A-periodic z:

- code in{0,2}: BOTH 2z and2z+1 are A-periodic, even when period doubles;
- code containing1 or3: exactly ONE extension is periodic; the other
  has least preperiod1+rho, rho the first time its drive contains1 or3.

Apply the latter at the HIGHEST disagreement, not automatically at the
whole row. Since sigma^(d+1)Y_t is cyclic and sigma^d Y_t is its wrong
bit extension,

    tau(sigma^d Y_t)
      =1+min{s>=0:bit_(d+1)(A^s Z_t)=1} <=tau(Y_t).

The minimum exists. Lower disagreements can outlast this one; equality
with the whole-row delay is not asserted. Controlling these waits for
ONE fixed FULL realization is still open.

Every physical clock doubling requires an eventual{0,2} input code.
Under FULL, its SOURCE has tau>=1 at even physical time and tau>=2 at
odd time. For the latter, actual center1 then0 at times t+1,t+2 forces
r_-1(t+1)=bit_0(A Y_t)=1. Thus cyclic doubling sources are impossible
under FULL. Do NOT use the source's cyclicity in the local waiting-time
lemma as an actual FULL mechanism; use the projected highest bit above.
The general-trace cyclic-source formula in Section4 has its stated
scope. Earlier paired type{0,3} lag>=3 remains unchanged and stronger
there. Physical clock growth/counts still give no unbounded delay heights.

## Initially finite local controls and a closed supply route

Read `proofs/informal/problem1_round9_finite_source_sidecar.md`.
For finite z and s=(prefix_h,Theta(z)), put K_z=min{K:pi^K z=0}.
Then x=Theta^-1(s) is initially finite iff Phi^{K_z}s is alreadyzero.
Any nonzero remaining finite temporal word keeps its last nonzero time
under every Phi step. This criterion alone does not supply large periods.

Conditional finite-source construction (`partial-proof`): if a finite
A-cycle code u is contained in{0,2}, has odd2-count per LEAST periodp,
and has a cyclic222 occurrence, rotate there and set x=z+1. Then x is
INITIAL finite, source tau=1, actual time-two successor tau=0, and
its period doublesp->2p. Original zero fringe D0=D1=D2=3. No D beyond2
is claimed. Source casesp=1 (x=7) andp=4 (x=467256711) are exact.
Forp=4, u=2220 repeated, Phi kills it in15 steps; z=467256710 has
width29. The hand chain and digit reconstruction are preserved.

The proposed all-k supply u_k=(2^(2^k-1)0)^infinity is REFUTED at k=3.
Exactly ONE undecided word22222220 was admitted and tested. Its cyclic
Phi orbit repeats nonzero03033003 at818, first seen286 (cycle532).
Both implementations agree on every one of819 states, including the
repeat. The verified deterministic cycle proves all-future nonnilpotence
of this word; it supplies no positive all-k or Problem1 conclusion.
Do not extend k, periods, doubling indices, source words or actual horizons.
Unbounded finite222-cycle supply remains `inconclusive`; the failed
family does not decide other supplies or all its later members.

## Verification and provenance

The corrected new-context adversarial review is accepted after independent
lead derivation and audit at the stated partial-proof/refuted scopes.
Primary contributor Muse thread01a079be-35bd-7fe2-aace-9cddd1379dcb is CLOSED.
It supplied the conditional memo and original fixed test. Lead independently
rederived the mathematics and corrected its provenance. Reviewer Muse threads
01a079d8-8ed3-73e0-9f40-1e0d0a28f591 and
01a079de-dbcd-7db1-9c4c-c4bc1d82838e both ended in provider429, with one
retry after a pause. Both are CLOSED. The first left a partial review of
old files, preserved exactly as problem1_round9_muse_partial_review.md;
it is not the final accepted review.

Mandated fallback MiMo thread01a079e2-2a08-7383-8190-5d48dd183a2a reviews
all three current sources and the corrected certificate. Its initial
proposed c_t in{0,2} correction was rejected: c_t is a physical BIT, and
c_t=0 is correct. Its c_(t+1) shorthand misplaced the recurrent1 by one
physical step; the source correctly says c_(t+2). The sidecar's old
k1/k2 wording had already been corrected. Final disposition is recorded
in problem1_round9_fresh_review.md; all three corrections are explicitly
withdrawn. MiMo read the prior Muse partial draft while inspecting the old
review file, so this is NOT claimed to be a blind review. The corrected
sources were separately re-derived and the code/result inspected; no
additional scientific inputs were run by MiMo. Final corrections were
received and the worker CLOSED by03:44:16UTC. All workers are CLOSED;
no review remains pending. No native Codex model was substituted.

Initial experiment/source/memo bytes were captured BEFORE correction in
`results/problem1/20260907_round9_superseded_run.json`. The original record
omitted its computed reference hash and nonzero trajectory hash, used a
nonnumeric runtime field, and merely reported caps. Corrected same-input
verification has separate tuple/formula and string/table orbit loops,
full trajectory/hash, exact checker bytes, full Git, hardware/software,
measured memory and enforced120-second/256-MiB limits, and atomic output.
It also checks all16 g-pairs and the21 already hand-derived transitions.
The unused sidecar T-inverse arithmetic constant111 was wrong (119);
that bypassed argument was removed, not used as a proof dependency.

Checker: `experiments/problem1_nonperiodicity/check_round9_one_hole_control.py`.
Result: `results/problem1/20260907_round9_one_hole_control.json`.
Round audit: `results/problem1/20260907_round9_audit.json`.
Builder: `experiments/problem1_nonperiodicity/audit_astra_round9.py`.
One new fixed-word computation, one necessary same-input verification
correction, and archival integrity work; no sweep or new scientific backend.

Unrelated supervisor files, ASTRA_GOAL.md, .worktrees and old untracked
results remain untouched. Immutable reference SHA256:
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Never force-push, change that reference, or merge to main.
