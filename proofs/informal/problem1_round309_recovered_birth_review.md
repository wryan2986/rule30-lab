# Round 309 adversarial review: recovered birth spacing

Reviewer: MiMo (mimo-v2.5), external sidecar
Spawn: 01a07c4e-caa2-7aa2-bd16-0c0ef70f6c92
Date: 2026-09-07
Status: Fresh external adversarial review of the birth-spacing unit only.
No new experiment, input, source search, or domain extension. Only one
path is written by this review:
`proofs/informal/problem1_round309_recovered_birth_review.md`.
Problem 1 remains OPEN.

## 0. Files read

This review reads the following files for inspection and hash verification:

- `proofs/informal/problem1_nonreset_return_birth_spacing.md` — primary proof
- `experiments/problem1_nonperiodicity/check_round307_nonreset_return.py` — checker
- `results/problem1/20260907_round307_nonreset_return.json` — experiment record
- `proofs/informal/problem1_round307_review.md` (Section 6) — lead disposition
- `proofs/informal/problem1_nonresetting_core_returns.md` — imported dependency
- `proofs/informal/problem1_shadow_gate_birth_phase.md` — imported dependency
- `experiments/problem1_nonperiodicity/check_round307_exit_phase.py` — RULE source
- `docs/experiment_protocol.md` — status definitions
- `AGENTS.md` — repository rules

All paths relative to `/home/ryan/rule30-lab`.

## 1. Provenance and hash audit

### 1.1 Reference hash

The immutable reference SHA256 of
`src/python/rule30_research_reference.py` is
`358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`.
Verified on disk: MATCH.

### 1.2 Source hashes in the JSON record

The record at `results/problem1/20260907_round307_nonreset_return.json`
lists six source hashes. Current on-disk re-verification:

| Source | JSON hash | Disk hash | Status |
| --- | --- | --- | --- |
| `experiments/.../check_round307_nonreset_return.py` | `5b0552a2...` | `5b0552a2...` | OK |
| `src/python/rule30_research_reference.py` | `358bdc07...` | `358bdc07...` | OK |
| `experiments/.../check_round307_exit_phase.py` | `e4cad497...` | `e4cad497...` | OK |
| `proofs/.../problem1_nonreset_return_birth_spacing.md` | `4aed14b4...` | `2ec25e35...` | **STALE** |
| `proofs/.../problem1_nonresetting_core_returns.md` | `cc784206...` | `cc784206...` | OK |
| `proofs/.../problem1_shadow_gate_birth_phase.md` | `351459a9...` | `351459a9...` | OK |

### 1.3 Canonical payload hash

Computed from `record["payload"]` with sorted keys and compact separators:

    computed: 4e3778a22fb22e5331c9bd90e19d4c90eb99bc102c71736eca1a6c326000e67f
    recorded: 4e3778a22fb22e5331c9bd90e19d4c90eb99bc102c71736eca1a6c326000e67f
    MATCH.

### 1.4 Git commit

The record was written at commit `8265ddc19593af3d2f5334c8004e1ddbd5d0478c`.
Actual current HEAD at review time: `5be12e3712ea9b4259e3e08124e5e795242371d1`
("fix: emergency kill should trigger on HARD_INTERRUPT grace expiry").
The record faithfully captures the commit at write time; drift is expected
from subsequent uncommitted work.

### 1.5 Stale linkage on birth_spacing.md

`problem1_nonreset_return_birth_spacing.md` was modified after the
experiment record was written. The JSON source hash
`4aed14b4d83576c1b7c4c63f7e09d4862b70506fb624b552aaaea4c606c57b05`
does not match the current on-disk hash
`2ec25e3570c041d97f838b19f966b68b27f8fa4e0cd97c6ad10cd3b26d83fbde`.
The record no longer certifies the exact source state it claims. The
mechanical check result for the eight declared cones remains valid on
its own inputs, but the linkage between record and proof document is
stale.

**Required fix: re-run the checker against the current proof document
with a fresh atomic record.** The existing JSON and its hashes are the
historical record of the prior run and must be retained as-is. Do not
rewrite existing JSON source hashes to claim they were observed at a
different run time.

## 2. Exact FULL hypotheses

### 2.1 The checker's hypothesis (finite-exhaustive)

The checker tests equation (3) of the proof: for each of the eight
combinations u,a,b in {0,1} with initial cells at positions -2 through 4
set to (u,u,0,u,1,a,b), two physical Rule30 steps must produce:

- Centers at positions 0, 0, 1.
- First-step right values at positions (1,2,3): (1, 1 XOR u, 1 XOR (a OR b)).
- Second-step right pair at positions (1,2): (1, u * (a OR b)).

Status: `finite-exhaustive` over exactly these 8 inputs. No FULL
membership, no E-shadow claim, no infinite-domain assertion.

### 2.2 The proof's FULL hypotheses (Sections 1-4)

The mathematical argument in Sections 1-4 uses these imported hypotheses:

1. **Source phase theorem** (from `problem1_nonresetting_core_returns.md`
   Sec. 1 and 3): given N_t and b(Y_t)<=2 at an even time, the shadow
   cells at (-2,...,2) are (u,u,0,u,1) and source delay d=2-u. This is
   an all-period algebraic identity, not a finite experiment. Imported,
   not freshly reviewed end-to-end.

2. **Cyclic-source birth law** (from `problem1_shadow_gate_birth_phase.md`
   Sec. 1 and 4): chi_t = u_t XOR hat-u_t, where the shadow flag is
   computed from the GLOBAL shadow at the cyclic source. Conditional on
   FULL + c_t=1 at even t. Imported, not freshly reviewed end-to-end.

3. **Even delay bound** (from `problem1_nonresetting_core_returns.md`):
   under eventual K=3 FULL, tau(Y_{2m}) <= 2 for sufficiently late even
   times. Imported, not freshly reviewed.

4. **No-uu** (from `problem1_period_two_fringe_language.md`): consecutive
   gate-u indicators cannot both equal 1. Imported, not read by this
   sidecar.

5. **N-implies-O theorem** (from `problem1_nonresetting_core_returns.md`
   Sec. 1): N_t iff O_{t+2} for every physical t, independent of FULL.
   Imported, not freshly reviewed.

These are the stated FULL hypotheses. No additional infinite-domain
hypothesis is introduced by this unit. **All five imported results are
inherited from prior work; their correctness is not re-established by
this review.**

## 3. G(z) formula

Equation (6a): G(z) = Y_{t+4} = 16 A^4 z + 7.

The derivation: with z = Z_t (the shadow at a nonresetting source time),
the first paired successor is F x = 4 A^2 x + 3. At the cyclic return
time q = t+2, the pure code has c_2 = 1, so:

    A^2(F x) = 4 A^4 x + 1
    F^2 x = 16 A^4 x + 7

The source delay being at most 2 gives A^4 x = A^4 z. The code is
described as I_3 I_1 shift^4 Theta(z). The cyclicity and u gate of G(z)
hold on the stated actual FULL domain; they are not asserted for every
finite N core.

Review: the formula is a direct computation from F^2 applied to the
two-step bridge with c_2 = 1. I find no arithmetic error. The formula
correctly captures the complete-core return. The domain restriction
(actual FULL source) is explicitly stated and is not overextended.

## 4. Seven spacing times

The proof claims no nonresetting source occurs at times t+1 through t+7
(seven times). My audit of each:

| Time | Argument | Verdict |
| --- | --- | --- |
| t+1 | First nonresetting lift trace visits both values (imported from Sec. 1 of core returns, not freshly reviewed). | Sound conditional on import. |
| t+2 | Cyclic row, constant-one core low trace, not identically zero. | Sound. |
| t+3 | Preceding even row at t+2 is cyclic (or t+6 is one-bit). Cyclic even FULL source with identically-zero first-right trace forces core alphabet subset of {0,3}, contradicting gate symbol at A-time 1 in {1,2}. One-bit source has b_0=2 so its first-right trace flips. | Sound. |
| t+4 | Cyclic, same as t+2. | Sound. |
| t+5 | Same structure as t+3. | Sound. |
| t+6 | If beta=0: row is cyclic with actual center 1; its core low trace cannot be identically 0 (the gate symbol at A-time 1 is in {1,2}). If beta=1: one-bit t source, code at A-time 1 equals 1, so resetting (not N). | Sound. |
| t+7 | Same structure as t+3. | Sound. |

The seven times are correctly enumerated. The exclusion at each time is
an algebraic fact from imported theorems, not a finite experiment. The
conclusion that distinct sufficiently late N source times differ by at
least 8 follows. The proof correctly notes this is a lower bound on
spacing, not a positive density or a finite birth budget.

**No mathematical fatal flaw found in the spacing argument as stated.**

## 5. Finite eight-cone scope

The checker runs exactly 8 cases: u in {0,1}, a in {0,1}, b in {0,1}.
Each initial configuration is 7 cells at positions -2 through 4. Each is
propagated 2 physical steps. The trusted cone shrinks from positions
[-2,4] to [-1,3] to [0,2], matching the backward cone of the final
outputs.

The checker uses two independent implementations: (a) a truth-table
`truth_step` from the imported RULE tuple, and (b) a packed-bit
`packed_step` using the algebraic identity (word << 1) ^ (word | (word >> 1)).
Both agree on all rows for all 8 cases, including a hand-derived 2-step
cone used as reference.

Caps: 1 CPU, 10 seconds, 128 MiB address space, 128 KiB output. All
passed (peak RSS 20,377,600 bytes, runtime 0.000316s).

The scope is correctly bounded: this certifies the 8 shadow cone
identities only. It does not certify that any of these inputs is an
E shadow, a FULL realization, or a member of any larger search.

## 6. Lead review cross-check (Section 6 of round307 review)

The lead review of this unit (Section 6 of
`problem1_round307_review.md`) dispositioned the proof at
`partial-proof` scope and described the checker as `finite-exhaustive`.

Agreement. The lead review states "There is no omitted input at the
tested boundary: the second outputs occupy positions 0 through 2, whose
backward cones fit exactly inside the initial positions -2 through 4."
This is correct: output at position 2 at time 2 has backward range
0..4 at time 0; output at position 0 at time 2 has backward range
-2..2 at time 0. Both fit within the initial window -2..4. The union
of all backward cones covers the full initial range exactly.

The lead review also documents the three failed direct executions (peak
RSS assertions before the fresh-child fix) and the diagnostic that
ru_maxrss carries across execve. This matches the proof document's own
account. The fresh-child invocation passed the same caps.

## 7. External review status

Two Muse provider threads in this round failed429 and were closed:
- 01a07c49-8a14-7590-ab28-5a1f98a2ea86
- 01a07c4c-79a4-7330-90da-d2456b244cf9

This MiMo sidecar (spawn 01a07c4e-caa2-7aa2-bd16-0c0ef70f6c92) is the
successful fresh external adversarial review of the birth-spacing unit.
The proof document's status header "fresh external adversarial review
missing" is now superseded by this review.

## 8. Compact claims

The following conditional mathematical claims are supported at
`partial-proof` scope:

1. **Shadow cone identity**: For u,a,b in {0,1} with shadow cells
   (u,u,0,u,1,a,b), two physical Rule30 steps give centers 0,0,1 and
   second right pair (1, u*(a OR b)). `finite-exhaustive` over 8 inputs.

2. **Cyclic source gate sequence**: Under FULL + constant-one core low
   trace, c_1=c_2=1, so consecutive gates are t then u. `partial-proof`.

3. **Two-bit source forced birth**: When u=0 (two-bit t source), the
   shadow zero-pair flag at q vanishes, giving beta=1. The return creates
   a new lag-one even row at t+6. `partial-proof`.

4. **Complete core return**: G(z) = 16A^4z + 7 with code I_3 I_1
   shift^4 Theta(z). `partial-proof`.

5. **Seven-time spacing**: No nonresetting source at t+1,...,t+7.
   Distinct sufficiently late N source times differ by at least 8.
   Necessary separation, not positive density. `partial-proof`.

Claims 1-5 depend on imported results that were not freshly reviewed
end-to-end by this sidecar. Their correctness is inherited from prior
units.

## 9. Stale linkage summary

The proof document `problem1_nonreset_return_birth_spacing.md` was edited
after the experiment record was written, producing a stale source hash
linkage. The JSON record stores source hash
`4aed14b4d83576c1b7c4c63f7e09d4862b70506fb624b552aaaea4c606c57b05`;
the current file hash is
`2ec25e3570c041d97f838b19f966b68b27f8fa4e0cd97c6ad10cd3b26d83fbde`.
This is stale linkage, not a mathematical flaw. The mechanical check
result for the eight cones remains valid on its own inputs. The lead
will re-run the checker against the current proof document with a fresh
atomic record. The existing JSON and its hashes are retained as the
historical record of the prior run.

**No mathematical fatal flaw found.** The FULL hypotheses, G(z) formula,
seven spacing times, and finite eight-cone scope are accurately stated
and internally consistent. The checker correctly tests its declared
scope. The conditional deductions in Sections 1-4 use imported results
at `partial-proof` scope; those dependencies were not freshly reviewed
end-to-end and their correctness is inherited, not re-established.
