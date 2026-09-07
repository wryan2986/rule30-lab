# Astra handoff: round 8 maintenance checkpoint, 2026-09-07

Problem 1 remains OPEN. This is routine time maintenance, not goal
achieved, research blocked, or research exhaustion. Continue on
`research/astra-next`. Round eight started at 00:36:14 UTC; the user
requested approximately 20 minutes. The atomic audit records elapsed
time and the checkpoint timestamp. Read ASTRA_GOAL.md first.

Incoming round-seven handoff is preserved byte for byte in
`docs/astra_handoff_archive_20260907_round8.md`. Base commit:
`69dc3a166a33687dd7416849ba44106c55bddb36`. Do not redo its reset-language,
period tower, anchored equivalence, full diagonal, width count,
cycle-mate lemma, or fixed55 certificate.

## Current bottleneck

FULL must contradict finite entry for ONE FIXED ACTUAL survivor.
Round seven proved that infinitely many inverse clock doublings force
late source diagonals. Round eight now rules out one local way to turn
that into unbounded lag heights: arbitrarily large clocks can double
with uniformly short source and successor transients, even under finite
entry and three actual original-zero-fringe diagonal constraints.

The infinite-future incompatibility remains unproved. In particular the
new family varies its input with the requested clock bound; it is NOT
one infinite FULL or permitted-F orbit. No global route is refuted by
that quantifier change.

## New exact local control family (`partial-proof` / `refuted` local bound)

Read `proofs/informal/problem1_bounded_lag_doubling_controls.md`.
For EVERY P there exists x with original zero right fringe such that

    A^4 x is finite AND A-periodic;
    D_0=D_1=D_2=3 (actual center times0..5 are1,0,1,0,1,0);
    p(Theta(x))=p>P, p(Theta(X_1))=2p;
    tau(Theta(x))<=4, tau(Theta(X_1))<=2.

X_1 is the ACTUAL center-and-left row at time two. Tau denotes LEAST
temporal preperiod, equivalently first A-cycle entry. The source x is
finite-entry; it is NOT proved initially finite. It is finite after
four physical steps, by A^4=pi^4 T^4. Rephasing there does not preserve
the displayed doubling source or its stated bounds.

Construction (all hand argument, no scientific run): import unbounded
period growth for the ONE fixed auxiliary input1 with W_m=4^m. Its
periods change only by doubling, so source periods at doubling positions
are unbounded. Choose a phase-correct eventual cycle code u=Theta(z)
there; z is finite and A-periodic. The input alphabet is either{0,2}
with an odd count of2, or{0,3} with an odd count of3. Do NOT claim
unbounded source periods separately for EACH type.

Set s=(3,2,2,0,u), x=Theta^-1(s). Then A^4 x=z. Its actual first
successor is c=G(s)=I3(2,0,u), with head3,1,1. At time2 the scan
state1 belongs to BOTH invariant pairs ({1,3} or{0,1}); the periodic
drive starts there, so the odd swap gives least period2p and onset<=2.
The source head3,2,2 gives D0=D1=D2=3 by the already reviewed original
I0 full-fringe calculation. No D_j for j>=3 is claimed or evaluated.

Precisely refuted: a universal lower bound tending to infinity with p
for the source preperiod, successor preperiod, or their maximum under
JUST the above local hypotheses. This does not refute any established
repo theorem. It does NOT refute initially-finite-only bounds, nor
infinite-F/FULL statements. The construction is a local control on the
current doubling-lag mechanism, not a prefix campaign.

## Routes considered and what remains open

1. Local mismatch/reset propagation was the cheapest falsifiable route.
   The control family closes the proposed period-dependent local lower
   bound at the exact finite-entry/three-diagonal scope above.
2. Whether uniformly bounded preperiods along ONE INFINITE permitted
   G orbit force bounded periods remains `inconclusive`. The sidecar
   does NOT refute this. A proof would turn round-seven clock growth
   into unbounded lag heights, still not itself a FULL contradiction.
3. Universal eventual entry by2m at the original fixed fringe remains
   unproved, as does its FULL-conditioned version. No lag census ran.

The strongest next attack is still control of the required transient
passages along ONE FIXED ACTUAL FULL realization, using its entire
future boundary. The new local construction shows why arbitrary clock
size at a single step is insufficient. Initially finite support at the
transition is another hypothesis not settled by these controls, but
must not be silently inferred from finite entry.

## Verification and review corrections

Primary Muse worker: `opencode-go/muse-spark-1.3-contributor`, thread
`01a0794c-5067-7e52-82c3-5f0904605ecc`, CLOSED. Its corrected exploratory
memo is `proofs/informal/problem1_round8_lag_sidecar.md`, superseded by
the stronger lead source above. Its source-based scoped review is
`proofs/informal/problem1_round8_bounded_lag_review.md`. Lead independently
re-derived the identities and accepted the corrected scoped result.

Rejected and corrected before acceptance: (a) an isolated-step family
does not imply the whole scan/gate recursion cannot prove a global
bounded-lag theorem; (b) the type{0,3} isolated response has available
onset2, not a required3; (c) Phi makes input period DIVIDE output period,
while an available2p makes output least period DIVIDE2p; (d) mismatch
against the DOUBLED period is needed; (e) finite x does NOT imply an
eventually-zero temporal Theta code. The last was a reviewer error,
explicitly withdrawn in its file; finite1 has Theta(1)=1^infinity.
The main source never made that false claim.

A new-context Muse reviewer, same mandated model, thread
`01a07956-ee3d-7431-bd4b-f0ec21cc04bd`, completed a fresh adversarial
review without reading earlier verdicts. Its record is
`proofs/informal/problem1_round8_fresh_review.md`. It independently
checked both invariant pairs, period-one countercase probes, phase,
least periods, actual-fringe identification and all quantifiers. Lead
independently audited and accepted the scoped result. Orchestration
bounds were 00:48:55 through 00:51:14 UTC; the initially guessed review
window was corrected before archival. No provider429 or fallback occurred.
Both workers are CLOSED, and no review remains pending.

## Provenance and restart fence

Atomic record: `results/problem1/20260907_round8_audit.json`.
Builder: `experiments/problem1_nonperiodicity/audit_astra_round8.py`.
These archive exact sources, review hashes, fullGit, elapsed time,
software/hardware, limitations, immutable reference and incoming handoff.
There was NO scientific simulation, finite search, vector generation,
benchmark or numerical period/lag/prefix computation in this round.

Do not repeat the local family or extend its fixed horizon by search.
No prefix, period, inverse-word, denominator, cycle-width or lag sweep
is admitted. Periods>=3 and B_all/signed nonvanishing retain their older
statuses and were not investigated. Refer to the incoming archive for
all earlier exact formulas, actual-fringe restrictions and stopping fences.

Unrelated supervisor files, ASTRA_GOAL.md, .worktrees and old untracked
results remain untouched. Immutable reference SHA256:
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
Never force-push, change that reference, or merge to main.
