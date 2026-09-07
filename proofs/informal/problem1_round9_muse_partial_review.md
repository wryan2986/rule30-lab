# Round 9 fresh adversarial review (objective: FIND A FATAL FLAW)

Role: fresh adversarial mathematical reviewer. Did not defer to prior acceptance.
Did not read other new review verdicts (none exist).
Problem 1 remains OPEN. No Problem 1 solution is claimed by the sources or by this review.
I own only this file. No commits, no other edits. No sweeps run. Old checker script not rerun;
in-memory read-only re-derivations only (no files written, final results untouched).

Reviewer: muse-spark-1.3-contributor, single-session review, 2026-09-07 ~03:13 UTC.
Sources reviewed (ORIGINAL pre-fix bytes; hashes to be updated after lead signals ready):

- proofs/informal/problem1_cycle_completion_defect_transport.md
  SHA256 94fadeb992033cb26522b4cf47f391b77748ab609114074d70f50f137f618008
- proofs/informal/problem1_round9_finite_source_sidecar.md
  SHA256 545119601725ab59f3672146cece8c2e734ae159b522837c8c241a569e339e8d
- experiments/problem1_nonperiodicity/check_round9_one_hole_control.py
  SHA256 fb8e40942daaa0e45d96175dda7a7fba4bbdb313dc343b4b60e705e6cbe5d5cb
- results/problem1/20260907_round9_one_hole_control.json
  SHA256 5e16aec1259f1090a8b467ea6e728dc24248f553c6188368a390b0b4a7ddc41f

Targeted dependencies read: gate-bridge Secs 1-3, sparse-codes Secs 1-2,
full-fringe diagonal Secs 2-4, reset-language Secs 1-3, anchored-entry Secs 1-5,
plus round 8 bounded-lag controls for X_1/D scoping. Nothing else new read.

## Verdict

No fatal mathematical flaw found in either source within its stated scope.
Required corrections are presentation/scoping plus lead-confirmed provenance defects
(lead-owned fix pending). One misleading scope sentence must be corrected:
a verified nonzero repeat DOES prove an infinite-horizon negative (never hits zero;
all-k one-hole supply refuted). It proves no positive all-k supply and no Problem 1 result.

## Task 1 — transport note (independently re-derived)

cyc well-defined: any two k1,k2 >= tau multiples of p give the same A^k y because
the later is reached from the earlier by a multiple-of-p advance on the cycle. Checked.
cyc(y)=y iff periodic: forward uses k=0; reverse uses y=A^k y, hence y periodic. Checked.
tau(A^r y)=max(tau-r,0): upper bound direct; reverse uses that periodicity of
A^{s+r} y forces tau(y)<=s+r. The reverse direction is load-bearing and holds. Checked.
cyc(A^r y)=A^r cyc(y): one K multiple of p above tau (hence above tau'<=tau) serves
both sides. Checked, including r>tau and tau=0 boundary.
cyc(pi^n y)=pi^n cyc(y): uses piA=A pi, finiteness of tau(pi^n y) via pi-image of a
finite tail orbit, period-divides-p for the pi-image, and K above BOTH onsets that is a
multiple of p(y) (hence of the divisor period). The note's one-line justification is
terse but the missing finiteness/divisibility steps hold. Not fatal; suggest one sentence.
kappa upward-closed uses pi-preserves-periodicity via commutation. Checked.
(6) both directions checked against periodicity of the finite representative.
(7): pi^n X_{m+n}=A^{2n} X_m from (1), then (4); kappa>n iff tau_m>2n follows by
contrapositive, infinity allowed on the left. Finite-entry preservation under F holds:
pi(A^h X_{m+1})=A^{h+2}X_m is finite, and finite pi-projection implies finite source
(low-pair restore); A maps finite to finite. The note compresses this to one sentence;
it is correct. Early-row kappa=infinity before physical finite entry is correctly
excluded from eventual bounds by the M+N / max(0,M-N) offsets. Constants (10)(11) and
translation (12) re-derived exactly, including N=ceil(K/2) sharpness and (9)'s
nonempty witness n=m under 2m>=tau_0. No uniformity manufactured. Checked.
Strip (13): pi Z_{m+1}=A^2 Z_m via cyc commutation applied to pi X_{m+1}=A^2 X_m;
a_m is the representative's own low pair, correctly NOT identified with fringe 3. Checked.
High-bit agreement from (6) is exact; the note's carry warning (distance bound does not
imply agreement) and explicit non-autonomy statement are correct and required. Checked.
Top-defect rule re-derived from bit_i(AY)=y_{i+2} XOR (y_{i+1} OR y_i): (14) holds,
lower bits never affect position d, erasure is permanent, two-step survival iff the two
common driver bits (15) vanish. (16) disjoint-support sum/XOR is harmless. Highest next
defect exactly d+2 iff (15); else <=d+1; low-pair births retained. d=0 erases under FULL
because D_m=3 forces common bit 1 =1. Pair-depth warning (d=2k+1 -> 2k keeps pair k)
is correct. kappa=floor(d/2)+1 re-derived. Rule scoped to finitely differing pairs;
late rows under (10) satisfy this; kappa=infinity early rows are out of scope. Checked.
FULL-application of (1) to actual even rows relies on imported full-fringe bridge under
the all-D=3 premise; dependency cited, not re-proved here. Acceptable as scoped.

## Task 2 — sidecar finite-source construction

Lemma 1 checked: finite x iff some Phi^N kills Theta(x) (via Theta(pi^N x), pi^N x=0);
nonzero finite-support immortal via g(0,0)=0, g(a,0)=3 for a!=0 (all 16 g pairs
recomputed from the bit definition; match). Lemma 2 checked: K_z-tail kill leaves
length-h word w; w=0 iff finite, else immortal finite-support. Checked.
Scoping correction required (minor): K_z=1 ترك only-z=3 is true only inside the
odd doubling tails (z=1 gives u=1^infty, z=2 gives K=1 but is not periodic; both outside
the doubling types). Demand the explicit qualifier among {0,2}/{0,3}-odd tails.
Not fatal to Sec 3, which bypasses Sec 2.
Prefix arithmetic verified by hand: A(135)=230, A(230)=206, A(206)=220, giving mod-4
head (3,2,2,0) consistent with b_3=0. The T^{-1} decoupling sentence is scope-only and
bypassed; not load-bearing.
Identity A(4k+2)=A(4k+3) proved (identical >>2, >>1; bit-0 masked in the OR). Checked.
Theorem checked end to end: rebase preserves least p and odd-2s count; x=z'+1 finite with
b_0=3; A(x)=A(z') gives Theta(x)=(3,u'_1,...); tau=1 exactly (pure periodicity would force
infinitely many 3s against a {0,2} tail); shift^2 b has least p; I_3 of a {0,2}-odd drive
stays in {1,3} by permutation dynamics, is purely 2p-periodic from t=0 with tau=0, and p
is impossible under the swap, so least period is exactly 2p. x=7 instance verified:
F(7)=27, A(27)=25, A(25)=27, period 2=2p. Checked.
D0-vs-D1 ordering correction required: the actual time-2 code is a priori
shift^2 I_0 b; its rewrite as I_3(shift^2 b) is valid ONLY given D_1=3, proved
independently from the head via I_0 (c: 0,1,3,1; D_1=3; D_2=3 from d_4 with b_2=2).
The sidecar lists the I_3 identification before the D triple, inviting a circular
reading. Logic is recoverable (head implies D_1=3 via I_0, then rewrite follows by
induction on the shared drive), but the order must be fixed: prove D_1=3 via I_0 first.
No circularity after reorder; successor tau/period/D claims stand.
Non-claims correctly scoped: no unbounded-222 claim; (2,0)^infty correctly noted finite
but 222-free (k1 is Lemma-level finite, NOT a Sec-3 rung — see ambiguous ending below).

## Task 3 — k2 chain, k3 certificate, provenance

g-table verified 16/16 from the bit definition; rows match the sidecar; h-vs-g caution
(gate-bridge row-1 differs) is correct. k2 15-step chain re-derived in-memory step by
step from g: all 15 transitions match the listed words exactly (2220 to 0000).
Lead datum re-derived: z=467256710 satisfies A^4(z)=z with least A-period 4, Theta head
(2,2,2,0) repeating, bitlen 29; x=467256711=z+1 has head (3,2,2,0), A(x)=A(z),
bitlen 29. Consistent with width-29 claim and Sec-3 rung at 4->8.
k3 in-memory orbit confirms: first six hand words match
(22222220 to 02120313); wraparound coupling caution (no length-halving induction from
the 0212 suffix) is correct; deterministic cyclic-Phi orbit first repeats word 03033003
at index 818 (first seen 286), never hitting zero. Cap 65536=4^8 is the full period-8
state space, so the nilpotent-vs-repeat disjunction is exhaustive for this fixed word.
Two-implementation agreement reproduced in effect (formula vs literal table agree on all
pairs and the orbit uses the verified g). Scope respected: refutes the one-hole all-k
supply at k=3 only; k1/k2 rungs stand; other-period 222 supply must come from elsewhere.
No all-k positive inference drawn. Checked.
Misleading-sentence correction: no infinite statement must not be read as no
infinite-horizon conclusion. The repeat IS a universal negative over all future steps:
a deterministic orbit that revisits a nonzero state is eventually periodic on a nonzero
cycle (zero is a fixed point of cyclic Phi), hence never reaches 00000000. That refutes
the all-k one-hole universal. It proves no positive all-k supply, no unbounded-222
claim, and nothing toward Problem 1. Preserve this distinction in the corrected record.
Provenance defects (lead audit confirmed by inspection, lead-owned fix pending):
ref_sha computed but never stored; nonzero-orbit chain and chain hash both null;
runtime_seconds is a dict not a numeric; limits reported not measured/enforced;
admission/source-version not archived in JSON. Atomic tmp+fsync+replace present in the
reviewed script bytes. Original run/source bytes to be preserved in the corrected audit
record per lead. Hashes above are ORIGINAL; update after lead signals ready.
Sidecar ending correction: k1/k2 finite rungs is ambiguous — k1 word (2,0)^infty is
Phi-nilpotent (hence finite) but has no cyclic 222, so it is NOT a Sec-3 control rung;
only x=7 (p=1) and the k2 word (p=4) are Sec-3 rungs. State this explicitly.

## Finite-to-infinite audit

Transport: every temporal/spatial transfer checked with quantifiers; no promotion of a
census to a theorem; bounded/unbounded equivalences are exact eventual statements with
offsets; strip non-autonomy explicit. Sidecar: finite-source criterion exact;
conditional 222 theorem all-depth given its hypotheses; k3 verdict finite-exhaustive for
exactly one fixed word with an exhaustive state-space cap; unbounded-222 and all-k
positive claims explicitly withheld. No finite experiment presented as an infinite proof
beyond the exact exhaustive disjunction for the single k3 word (legitimate finite claim).
Both sources state Problem 1 open. No solution claimed. No missing finite-to-infinite
step found beyond the corrections above.

## Status and missing checks

Math: Task 1 identities ACCEPT (scoped partial-proof); Task 2 conditional construction
ACCEPT subject to D1-ordering plus K_z-scope wording; Task 3 k2 chain ACCEPT, k3
repeat certificate ACCEPT as stated finite-exhaustive single-word verdict.
Provenance/code: PENDING lead fix and re-verification (old script not rerun; update
hashes when lead signals ready). Sidecar condensation restore: PENDING lead.
No new scientific inputs or sweeps made or needed from this reviewer.
