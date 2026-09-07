# Final adversarial review: round-7 scan reset language, cycle entry, doubling lag

Verdict: NO FATAL FLAW. Accept the three sources at their stated `partial-proof` /
`refuted`-shortcut scope. This review rederives every claim below by hand from the
stated H table and the cited imported identities. No numerical run, census, or code
change was used. Prior round-7 review verdicts were NOT read; only ASTRA_HANDOFF.md's
description of them was seen. Problem 1 remains OPEN: no full-fringe/finite-entry
contradiction is proved here or in the sources.

## 1. Exact reset language (reset note Sec 1) -- checked

Recomputed all six image-table rows from H0=[0,1,3,3], H1=[3,2,2,2],
H2=[2,3,1,1], H3=[1,0,0,0]: every entry matches (e.g. {1,2,3} under 0 is
{1,3}; {0,1} under 2 is {2,3}; {2,3} collapses to a singleton under every
letter). The path analysis is exact: {2,3} is a one-step-away-from-reset
state, and the surviving words are exactly {0,2}* UNION {0,3}* UNION
{0,3}*{1,2} with one final 1-or-2. Invariant-pair check confirms sufficiency
(H0,H2 permute {1,3}; H0,H3 permute {0,1}; H1/H2 send {0,1} bijectively onto
{2,3}). Corollaries verified: every H_j H_1 is constant since H_1 lands in
{2,3}; 2 0^k 3 resets; 3 0^k 2 lands in {2,3} so any further letter resets.

## 2. Least-period/onset theorem (reset note Sec 2) -- checked, one subtle step confirmed

The delicate sentence (last row: a {0,3}*-prefix plus final-letter exception
coalesces after one more letter) survives the apparent counterexample w="02":
that word belongs to the {0,2} row, not the last row. In the genuine last-row
exception subcase (prefix contains a 3, hence sits at {0,1} before the final 2,
or final letter 1 landing in {2,3}), the image after w is always {2,3}, so the
first letter of the next period does reset. Words with a non-final 1 reset
immediately ({2,3} image plus a following letter). Parity rows verified: on
{1,3}, 0 is the identity and 2 the swap; on {0,1}, 0 is the identity and 3 the
swap; entry takes at most p+1 (resp. p) tail letters; H_0^2=H_0 gives the
all-zero row. Least (not just available) periods follow from Phi c=b, so p
divides q: a period of c is a period of b, forcing p|q. Sharpness example holds:
constant input 1 from state 0 gives 0,3,2,2,..., attaining onset T+p+1 at p=1.
Every doubling visits symbol 1 on its invariant pair under an odd swap count, so
the next scan synchronizes; p_m=p_0 2^{d_m} with d_m<=ceil(m/2) follows and is
independent of the initial right symbols. The note asserts nothing about diagonal
samples lying in their periodic tails.

## 3. FULL late-cycle-entry necessary condition (reset note Sec 3) -- checked

The exclusion step is valid: a purely periodic C_m starting with 3 whose period
lies in {0,3} would force C_{m+1} eventual symbols into {0,1}, contradicting
(C_{m+1})_0=3. Hence all late periods synchronize to one p, the C_m orbit lives
in the finite set of 4^p purely p-periodic codes, and Theta injectivity (all-time
homeomorphism, sparse-codes note) makes X_m eventually periodic. The bit-length
climb X_{m+1}=4 A^2 X_m+3 is exact, and the reviewer verified the hidden lemma it
needs: A maps positive finite rows to positive finite rows with identical bit
length (top bit survives via (x>>1) OR x against x>>2), so A^2 X_m can never be 0
and the length grows by EXACTLY 2 per block -- repetition is impossible. Same-h
finite entry for all W_m uses pi commuting with A (spatial maps), never pi with
T; tau_A(W_m) finiteness uses finite orbit state space. Scope honesty kept: the
condition also holds for general infinite permitted-F orbits, so it discriminates
nothing about actual fringes, and neither universal entry-by-2m nor any 2m+C bound
is claimed.

## 4. Fixed-55 certificate (obstruction note) -- hand-verified arithmetically

A(55)=13 XOR 63=50 and A(50)=12 XOR 59=55 confirm the 55<->50 two-cycle.
F(55)=223; A(223)=55 XOR 255=200, A(200)=50 XOR 236=222, A(222)=55 XOR 255=200
confirm the 200<->222 cycle with tau_A(F55)=1, refuting permitted-step
periodicity preservation. W_1=220 gives 220->201->223 (A(220)=55 XOR 254=201,
A(201)=50 XOR 237=223), hence tau_A(W_1)=3>2, refuting the universal two-step
entry bound with an ACTUAL valid alternating block (D_0=D_1=3). Temporal
coordinates agree: I_0 on (3,2)^inf gives 0,1,3,0,2,0,2,... (preperiod 3) and
C_1=3,0,2,0,2,... . 223 mod 16=15 outside both gates blocks any survivor reading.
The note correctly retains the FULL-conditioned and asymptotic hypotheses as open.

## 5. Clock growth, width bound, doubling-lag location (lag note) -- checked

p_m->inf: the Y!=0 edge case is airtight (y!=0 via pi^J y=x!=0; T injective with
T(0)=0 gives Y=T^h y!=0; Y finite since low h pairs are always finite-width), the
A^h x=0 case is included, T/4^k commutation is by the XOR/OR formula with an
explicit disclaimer against pi-T commutation, and A^h W_m=4^{m-J-h}Y needs only
m-J>=h. The width bound ceil(L/2)<=4^{p_m}-1 is a clean combinatorial count:
N pre-zero Phi-deletion codes are pairwise distinct (applying Phi^{N-j} to a
repeat would kill a code below depth N), each inherits available period p via
Phi-shift commutation, and only 4^p-1 nonzero purely p-periodic words exist.
Gate symbol (4b), (B_m)_{2m+2} in {1,2}, is correctly derived by applying FULL at
m+1 through (C_{m+1})_1=H_{(C_m)_2}(3) with H_i(3) in {1,2} iff i in {1,2}.
Doubling location: {0,2}-tail doublings are late at m (D_m=3 outside {0,2});
{0,3}-tail doublings satisfy tau_m>2m+2 (TWO outside-alphabet gate symbols) with
lag >= THREE, plus the successor late via its {0,1} eventual alphabet -- every
doubling charges a distinct late source depth, giving
|LATE_N cap {0,..,N-1}|>=d_N=log_2(p_N/p_0)->inf. Local lemma: R({0..3}) sub {2,3}
with R(2)=R(3) (every H_i identifies 2,3 at the first letter) forces a unique
purely p-periodic response z, so c has least preperiod 0 (z=3) or exactly 1
(z=2), the longer-period concealment is excluded by sampling at multiples of p,
and exactly one of 4A^2x+2, 4A^2x+3 is periodic. The fixed-55 case realizes the
transient branch. All nongrowth limitations are stated: depths not heights, no
density, no anchored-activity transfer, permitted-F analogue uses current-row
preperiods rather than the W_m/2m threshold.

## 6. Handoff crosscheck, provenance, and scope

Handoff claims match the sources quoted above (reset table, period formula,
late-entry condition, lag THREE, width bound, 55 certificate, log2 count, open
incompatibility). Audit metadata (results/problem1/20260907_round7_audit.json,
builder experiments/problem1_nonperiodicity/audit_astra_round7.py) is
metadata-only: backend "archival-audit-no-scientific-run", limitations state no
census ran, and this review ran zero scientific computations. Hashes confirmed:
reference 358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01
with empty diff against round base 239bff4; builder
0a4dca6497e4cbe42cdede00c47b49c52e08b84a0f74802f7d324a66f45c0abe and handoff
d045115ab69a32ccf8bd00f92eb9b503be554a32e1e9498c4450c48997d37659 both match the
stored JSON; all three proof SHAs and all dependency SHAs in JSON match disk.
Branch research/astra-next, HEAD 04954ef (one commit past the audit's aa919d6 core
checkpoint); working tree clean on all three proof sources. Dependencies checked:
full_fringe_temporal_diagonal (Theta/I_a definitions, C_{m+1}=I_3 shift^2 C_m),
activity_sparse_temporal_codes (Theta computable homeomorphism),
anchored_activity_finite_entry (A^h=pi^h T^h, not pi-T commutation, A preserves bit
length), activity_temporal_gate_bridge (Phi commutes with shift).

Accepted partial-proof scope: exact reset language; least-period/onset/doubling
table with p_m=p_0 2^{d_m}, d_m<=ceil(m/2); FULL-implied infinite late entry
tau_A(W_m)>2m; per-doubling late source with type-{0,3} lag>=3 and log2 depth
count; local F-step preperiod 0-or-1 with unique periodic low-bit mate; fixed-55
refutation of the two universal shortcuts. Explicitly NOT proved: any Problem 1
solution, any FULL/finite-entry contradiction, entry-by-2m (universal or
FULL-conditioned), unbounded lag heights, or restricted-alphabet exclusion.

Sources: reset 7b6848922bacb79ee8630fb36b98b4e7397992cb5e36ee80c7e18e37538b55f5;
obstruction 5793bd078c48bbed28db85c72ede2ed9d0a119f8cde45ea804c905c00fb259e2;
lag 7b8c6844007d9c45916fda267df3edf5d7274d135810eb6b3f41e26035144a5c.
Review window 2026-09-07T00:26:31Z to 2026-09-07T00:30:00Z (ahead of 00:34Z target).
No commits made; no handoff edits; sole worker; only this file written.

## 7. Closure addendum: final-rollover draft and builder drift (2026-09-07T00:30Z)

Lead issued a final-rollover handoff draft and a builder metadata-only change; both
were re-audited read-only, builder never run. Findings:

- All three primary math source bytes are unchanged from 04954ef (identical SHA256s,
  empty git diff on all three paths). No mathematical content moved.
- Stored audit JSON is stage 'doubling' with fresh_final_reviewer None; its three
  archived proof SHAs match current disk bytes exactly.
- Working-tree builder hash differs from the stored snapshot
  (0a4dca64.. -> 2061989e..); git diff shows the ONLY hunk is the additive
  fresh_final_reviewer metadata block (this thread 01a07942-51c5-7812-8916-5235d1244eea,
  stage-conditional, None unless stage final). Expected drift, not an integrity failure.
- Handoff diff touches only the closing sections (maintenance rollover, final-review
  role split, restart point, admitted-sweep fence); every mathematical claim in it
  matches the sources as crosschecked in Sec 6. Immutable reference hash restated
  correctly; no force-push, merge, or reference change.
- Fresh adversarial re-verification (lead-flagged points): period phase/end-factor
  order in the local lemma rechecked with explicit p=2/p=3 drive words --
  R=H_{b_1} H_3 H_{...} with H_3 then H_{b_1} as the last two applied factors, so
  R({0..3}) sub {2,3} holds regardless of intervening factors; fixed-55 certificate
  spot-rechecked (A(223)=55 XOR 255=200). No flaw found.
- Verdict stands: NO FATAL FLAW at stated partial-proof scope. Problem 1 remains OPEN;
  no FULL/finite-entry contradiction, no entry-by-2m, no unbounded-lag claim.

## 8. Dated metadata followup (2026-09-07T00:33Z)

Typo corrected in Sec 2 ('p draws q' -> 'p divides q'); no mathematical content altered.
Read-only git-diff confirmation: at this review's read time the stored DOUBLING audit
matched builder 0a4dca64.. and handoff d045115a..; lead subsequently changed ONLY the
builder fresh-reviewer metadata fields and the handoff maintenance framing/current
closure, so those old hashes now refer to pre-maintenance versions. All three math
source hashes remain unchanged. No claim is made that a final (stage-final) audit has
run yet -- that finalization is lead's next step after this review closes.
