# New-context adversarial review - Round 9 (all three sources + checker + results)

## Provenance

Reviewer: mimo-v2.5 (MiMo fallback per ASTRA_GOAL.md Muse rate-limit protocol).
Thread: 01a079e2-2a08-7383-8190-5d48dd183a2a.
Fallback request after 03:20:36 UTC. Corrected review received by
03:41:15 UTC. This followup ~03:42 UTC.
Git: 28f5570d622ceb50bcd5b9e2f78d9c579e2ed419 on research/astra-next.

This is the final MiMo review. The prior Muse partial draft (152 lines,
SHA256 90f63d29..., two sources, stale hashes) was read during this
review session when inspecting the old review file. It was a partial
attempt with incomplete provenance; its verdict was not deferred to.
The prior Muse partial bytes are archival exact in their own file and
final audit record.

## Sources audited (exact SHA256 at this audit time)

1. proofs/informal/problem1_cycle_completion_defect_transport.md
   f3beba062dc2a28339bea0ded4528bfd777c9f16413184d1101bb1bba1b7c4a4
2. proofs/informal/problem1_round9_finite_source_sidecar.md
   2505b61220d1d0b926f062bb4290f246dec805277583aed6c64efc90db1136a7
3. proofs/informal/problem1_physical_time_cycle_defects.md
   87eafb58d1d3c9ff8d922eb7a1e569045381a7f01d219d7228e046554a6376a5
4. experiments/problem1_nonperiodicity/check_round9_one_hole_control.py
   fe6a200422b95368ec7bfe1593c9182d0bb1f0be3e09ea5fc5e1f2fb4a3ca95c
5. results/problem1/20260907_round9_one_hole_control.json
   f1dc5b8a33902893cddcd5556950cddb523dc8f1812f7ae73b8a38879d18f9cf

## What was actually executed vs inspected

- All three proof sources: READ via exec_command cat of full file bytes.
  Claims re-derived in-memory. No source files written by reviewer.
  This review file is the only file written by this reviewer.
- Checker script: INSPECTED via exec_command cat. NOT rerun.
  Verified code structure: two implementations, 16/16 g-pair cross-check,
  21 frozen hand transitions, atomic write, resource limits, self-hash,
  reference SHA check, hardcoded asserts. NOT independently executed.
- Results JSON: INSPECTED via exec_command cat. NOT regenerated.
  Verified fields: outcome, repeat word, step indices, impl_agree,
  chain length, cycle length, runtime, script SHA, reference SHA.
- A(4k+2)=A(4k+3) in sidecar: HAND REASONING only. Not executed by
  this reviewer. The identity follows from identical bit formulas for
  positions i,i+1,i+2 under both inputs: same shift-2, shift-1, and
  bit-0 is masked by OR. Pure algebraic verification, no computation
  needed.
- g-table: verified all 16 pairs from bit definition in-memory reasoning.
- Old Muse review file (problem1_round9_fresh_review.md prior bytes):
  READ during this session to understand provenance. Not deferred to.

## Verdict

No fatal mathematical flaw found in any source within its stated scope.
All finite-to-infinite transitions correctly scoped. All statuses accurate.
c_t=0 in the physical-time source is correct: c_t = r_0(t) is a single
physical bit in {0,1} (Sec 0), pure code in {0,2} means r_t=0 identically.

## Withdrawn corrections from prior draft

Three corrections from a prior draft are WITHDRAWN as incorrect:

1. WITHDRAWN: proposed c_t in {0,2} instead of c_t=0.
   TYPE ERROR by reviewer. c_t = r_0(t) is a single physical bit in {0,1},
   defined Sec 0. Pair symbol 0 = (r=0,s=0), pair symbol 2 = (r=0,s=1).
   Both have r_t=0, so c_t = r_0(t) = 0 exactly. Source correct.

2. WITHDRAWN: proposed k1/k2 rungs wording fix.
   STALE READING by reviewer. Current sidecar already states: k1 word
   (2,0)^infty has no cyclic 222, so Sec 3 does not apply. Sec 3 cases
   p=1 and p=4 only. Already explicit. No fix needed.

3. WITHDRAWN: any text saying c_{t+1}=1 as the recurrent bit index.
   The correct statement is c_{t+2}=1 (the second one-bit scan, applied
   to Y_{t+2}, starts at the recurrent bit state 1). The first scan
   produces the code of Y_{t+1}; the second scan produces the code of
   Y_{t+2}. The recurrent bit belongs to Y_{t+2}, not Y_{t+1}.

## Task 1 - defect transport (source 1)

Independently re-derived. All identities checked:
- cyc well-defined, cyc(y)=y iff periodic, tau(A^r y)=max(tau-r,0).
- cyc(A^r y)=A^r cyc(y), cyc(pi^n y)=pi^n cyc(y).
- kappa upward-closed. Identity (7): kappa_(m+n)>n iff tau_m>2n.
- Constants (10)(11): N=ceil(K/2), offsets exact. Translation (12).
- Strip (13): a_m NOT fringe 3. Carry warning correct.
- Top-defect rule (14): bit_d(AY XOR AZ)=1 XOR bit_{d+1}(Z).
  d+2 iff (15), else <=d+1. kappa=floor(d/2)+1.
- FULL to even rows: imported full-fringe bridge. Scoped. No flaw.

## Task 2 - finite source sidecar (source 2)

All claims re-derived:
- Lemma 1-2 correct. g-table 16/16 verified from bit definition.
- A(4k+2)=A(4k+3): hand reasoning, identical bit formulas. No execution.
- Sec 3 theorem end-to-end. x=7 instance correct.
- k2 chain 15 steps all match. Lead datum z=467256710 correct.
- k3 repeat 03033003 at step 818/286, never zero. Cap exhaustive.
- k1 explicitly not a Sec-3 rung. Sec 3 cases p=1, p=4 only. No flaw.

## Task 3 - physical time cycle defects (source 3, final)

Source read at SHA 87eafb58 (Sec 5 + Sec 6 eq 14).

Sec 1: sigma Y_{t+1}=A Y_t, Y_{t+1}=2 A Y_t+c_{t+1}. c_t=r_0(t)
single physical bit in {0,1}. sigma commutes with A. Checked.

Sec 2: b threshold (3) exact. Constants (4). Odd-lag (5). Checked.

Sec 3: Disagreement rule (7). Erasure permanent. Checked.

Sec 4: Driven maps 0=id,1=const1,2=flip,3=const0. No-reset and
reset (8a) correct. c_t=0 re-derived: pair symbols 0=(0,0),2=(0,1)
both have r_t=0, so c_t=0. c_{t+2}=1: the SECOND one-bit scan
(producing Y_{t+2} code) has unique recurrent bit state 1, and Y_{t+2}
A-periodic starts there. Checked.

Sec 5: FULL exclusion. c_{t+1}=1,c_{t+2}=0 forces bit_0(A Y_t)=1
by Rule30 (eq 11). Under FULL c_t=1 even, 0 odd; eventual code in
{0,2} has low bit 0; actual c_t=1 at even t exceptional; (11) makes
odd t exceptional after one A step. tau_t>=1 even, >=2 odd (eq 12).
No A-cyclic doubling source under FULL. Period growth (13) via
finite-code width. Checked.

Sec 6: At highest defect d, z=sigma^{d+1} Y_t is A-periodic (agrees
with cyc Z), sigma^d Y_t = 2z + wrong bit. Apply (8a): tau(sigma^d Y_t)
= 1 + min{s>=0: bit_{d+1}(A^s Z_t)=1} <= tau(Y_t). Minimum exists
because no-reset would make both extensions cyclic, contradicting
highest disagreement. First erasing time of highest bit; lower
disagreements may persist. No tau(Y_t) equality asserted. Checked.

## Task 4 - checker and results audit

Checker: INSPECTED, NOT rerun. Structure verified. NOT executed.
Results: INSPECTED, NOT regenerated. Fields consistent.

## Summary

- defect_transport (f3beba06): partial-proof, no fatal flaw
- finite_source_sidecar (2505b612): partial-proof/finite-exhaustive/
  refuted, no fatal flaw, k1 already not a Sec-3 rung
- physical_time_cycle_defects (87eafb58): partial-proof, no fatal flaw,
  c_t=0 correct, Sec 5 FULL exclusion verified, Sec 6 eq (14) verified
- checker (fe6a2004): finite-exhaustive, inspected not rerun, no flaw
- results (f1dc5b8a): finite-exhaustive, inspected not rerun, no flaw

No Problem 1 solution claimed. No sweeps admitted. All work local.
No commits made. Own only this review file.

## Lead disposition, 2026-09-07 03:44:16 UTC

The lead independently re-derived the three scoped mathematical sources,
audited the checker, and checked stored-certificate integrity. The corrected
review is accepted at the stated partial-proof/refuted/finite-exhaustive
scopes. This was a new-context source-based adversarial review, NOT a blind
review: the reviewer read the prior partial Muse draft. No blind review is
claimed. The final source hashes above match the accepted working bytes;
the transport source's change from94fadeb9 to f3beba06 was header metadata
only. Final corrections were received and this worker closed by03:44:16UTC;
the quoted earlier times are orchestration bounds, not measured model time.
All reviewer workers are closed and no review remains pending. Problem1
remains open. This lead paragraph and the heading/count corrections are
metadata edits after the reviewer finished; no mathematical verdict changed.
