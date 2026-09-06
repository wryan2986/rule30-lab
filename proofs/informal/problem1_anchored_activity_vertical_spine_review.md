# Independent review: vertical-spine obstruction + independent implementation

Reviewed source: `proofs/informal/problem1_anchored_activity_vertical_spine_obstruction.md`
SHA256 (computed locally before reading):
`e7e44fcb19b358ff3191a9e8fdde80ae85e8af8de644ad389906d2c835141ee7`
Owned outputs of this review only: this file,
`experiments/problem1_nonperiodicity/check_anchored_spine_independent.py`,
`results/problem1/20260906_anchored_spine_independent.json` (atomic write by
the script). Lead source untouched; nothing committed. No search, no sweep,
no census: one fixed 6-cell input, 6 updates.

## Verdict (corrected: provenance repair v2)

ACCEPT the hand certificate and its exact scope; INDEPENDENT RUN AGREES
on repaired provenance v2. The original v1 acceptance overstated the
record: lead correctly REJECTED v1 provenance (no top-level payload,
non-canonical hash spacing, missing source/admission snapshots and sha
keys, unenforced wall cap, tolerated cap exceptions, unvalidated git).
The mathematics was and is accepted; the execution record was not. This
v2 corrects all six defects, reruns the SAME single input/6 updates once
(repair, not expansion), and retains the full superseded v1 record plus
the v1 source snapshot inside the new record. Originals also preserved at
/tmp/astra-round6-spine-{independent-initial.json,independent-source-initial.py,review-initial.md}.
All 18 `g` evaluations re-derived by hand (Sec. A); cyclic-to-infinite
lifting, exact `Q = 5`, and first finite-entry time 6 verified (Sec. B);
the independent physical-rule implementation reproduces
`50,23,10,45,36,63,0` bit-for-bit (Sec. C). Scope stays narrow: this
refutes only the coefficient-one vertical-alignment claim (and its anchored
`A^K` variant at `K = 5`); no `cK`-general no-go, no growth claim, and no
actual-survivor relevance is established or claimed. The harmonic theorem
is numerically consistent (`H_6 = 49/20 <= 5`). Aim-to-break probing found
no flaw; details in Sec. D.

## A. All 18 `g` evaluations, by hand

Symbols low-to-high bits; `r = b0 XOR (a0 OR a1)`, `s = b1 XOR (a1 OR r)`.
Identity 1 (`Phi v_0 = v_1`): `g(2,3)`: `r = 1 XOR 1 = 0`,
`s = 1 XOR 1 = 0` -> 0; `g(3,2)`: `r = 0 XOR 1 = 1`, `s = 1 XOR 1 = 0` -> 1;
`g(2,1)`: `r = 1 XOR 1 = 0`, `s = 0 XOR 1 = 1` -> 2; `g(1,0)`:
`r = 0 XOR 1 = 1`, `s = 0 XOR 1 = 1` -> 3; `g(0,3)`: `r = 1`,
`s = 1 XOR 1 = 0` -> 1; `g(3,0)`: `r = 0 XOR 1 = 1`, `s = 0 XOR 1 = 1`
-> 3. Gives `(0,1,2,3,1,3) = v_1`. Verified.
Identity 2 (`Phi v_1 = v_2`): `g(0,1)`: `r = 1`, `s = 0 XOR 1 = 1` -> 3;
`g(1,2)`: `r = 0 XOR 1 = 1`, `s = 1 XOR 1 = 0` -> 1; `g(2,3) = 0` (above);
`g(3,1)`: `r = 1 XOR 1 = 0`, `s = 0 XOR 1 = 1` -> 2; `g(1,3)`:
`r = 1 XOR 1 = 0`, `s = 1 XOR 0 = 1` -> 2; `g(3,0) = 3`. Gives
`(3,1,0,2,2,3) = v_2`. Verified.
Identity 3 (`Phi v_2 = v_0`): `g(3,1) = 2`, `g(1,0) = 3` (above);
`g(0,2)`: `r = 0`, `s = 1` -> 2; `g(2,2)`: `r = 0 XOR 1 = 1`,
`s = 1 XOR 1 = 0` -> 1; `g(2,3) = 0`; `g(3,0) = 3`. Gives
`(2,3,2,1,0,3) = v_0`. Verified.
Junction and tail: each identity's 6th evaluation is `g(3,0) = 3`
(`v_6` would-be vs `v_5`), and `g(0,0) = 0` keeps the zero extension
fixed, so the finite words extend correctly to all `t >= 6`. Nonzero
counts: `v_0` misses only `t = 4`; `v_1` only `t = 0`; `v_2` only `t = 2`;
5 each; final symbol 3 at `t = 5` throughout. Bit packing rechecked:
`(2,0,3)` -> `0,1,0,0,1,1` = 50; `(3,1,1)` -> 23; `(2,2,0)` -> 10;
`(1,3,2)` -> 45; `(0,1,2)` -> 36; `(3,3,3)` -> 63. All match the table.

## B. Lifting, exact `Q`, exact entry time: ACCEPT

Cyclic-to-`Z` lift: the `A` stencil reads only current/higher bits, so a
period-6 row's every length-3 window recurs mod 6; verifying (1) at the
six cells verifies the local `A` equations at every integer index.
Time lift: row 6 is exactly 0 and `A(0) = 0`, covering all later times
with no tail sampling. One-sided lift for `x = -50/63`: same stencil
reads only `>= i`, so the cyclic rows are the full one-sided orbit.
`A^6 x = 0` with rows 0..5 all nonzero (each has a nonzero pair in the
period) gives first finite entry exactly 6 for `A`; for `T`, `A^6 x = 0`
forces `T^6 x` finite via `A^h = pi^h T^h`, while finite `T^5 x` would
make `A^5 x` finite against the nonzero 63-periodic row. Exact `Q = 5`:
for `n >= 6` the horizon covers all of `t = 0..5` (later times zero) and
each word contributes exactly its 5 nonzero times; for `n < 6`,
`J_n <= n <= 5`. Hence `Q(x) = 5` while `A^5 x` is infinite: the anchored
`Q <= K => A^K` finite variant is refuted at `K = 5`, exactly as scoped.
Harmonic check: `H_6 = 49/20 = 2.45 <= 5`, unaffected. Low pair of `x` is
2, not 3: correctly noted as outside permitted actual survivors.

## C. Independent implementation and run: AGREES

Implementation: plain cell lists, physical rule
`r_i' = r_{i-1} XOR (r_i OR r_{i+1})` mod 6, initial `r_i = u_{-i}` with
`u = bits(50)`, conversion `u_i(t) = r_{(-i-t) mod 6}(t)`; no packed-`A`,
no `g`/`Phi` reuse; stdlib only; reference file hash-checked, never
imported. Hand spot-check of the conversion at `t = 1` (physical row
`[0,1,0,1,1,1]`, re-cut gives `[1,1,1,0,1,0] = 23`) matched before running.
Run: exit 0, words `[50, 23, 10, 45, 36, 63, 0]`, elapsed ~0.0000 s against
the explicit 120 s wall / 120 s CPU / 1 GiB budgets. Payload in
`result_summary` has exactly the lead-specified structure
(`period_bits`, `initial_word`, `a_rows` t0..6, `temporal_pairs` with
trailing 0, `pair_activity_counts [5,5,5]`, `first_zero_time 6`); protocol
fields (full git commit `a38580...`, snapshots of lead-source and
reference SHAs, hardware/software, timings, hashes, limitations, admission
basis) surround it; atomic same-directory tmp + fsync + replace.
Execution ledger (corrected): v1 ran at git `a3858002719830ec8e54227ade7b5d81fe5de089`
(provenance rejected as written); v2 repair rerun at git
`94f28fcc57151ea0819467539049bde980447cd7` (provenance accepted); v3
wrapper repair rerun at the same `94f28fc` commit (this execution).
Total: 3 executions, 2 repair reruns, all on the identical fixed input
and 6 updates; scientific formula never changed.
Provenance v2/v3 checks: top-level payload with exactly the six assigned
keys; canonical hash `json.dumps(sort_keys=True, separators=(',',':'))`,
whose digest `b58afe36...` matches the lead primary payload hash
byte-for-byte on every execution; exact source/admission snapshots
`{path,sha256,text}` with matching
`source_sha256`/`admission_sha256`/`immutable_reference_sha256` keys;
`signal.alarm(120)` wall enforcement with fail-closed rlimits (no silent
tolerance); 40-hex validated git commit; superseded v1 record and v1
source snapshot embedded, plus full v1+v2 execution archive from v3 on.
v3 wrapper (replayability): admission resolves live-note-bytes first, then
the primary record's admission snapshot with content-SHA re-verification
(this run used the fallback: note had moved to `f1b37c...` on a harmless
status edit, `recovered_from` recorded); history resolves `/tmp` retention
first (container-SHA verified) unless `SPINE_REPLAY_NO_TMP=1`, then the
working v2 record with container SHA verified before reading any mutable
byte and all embedded content SHAs re-verified (this run proved that path:
`history_via = repo-fallback`, `/tmp` untouched). No mutable prior output
is trusted without hash checks.
Status `finite-exhaustive` is explicitly confined to the singleton fixed
trajectory in `proof_scope` + `limitations`; no infinite inference is
drawn anywhere. Lead's packed cyclic-`A` counterpart and final archive are
out of scope here by assignment.

## D. Adversarial probes (all closed)

(i) Sign/direction errors in `g`: recomputed every evaluation twice from
the bit pairs; the easy slip (`g(3,2)` first bit) resolves to the claimed
1. (ii) Junction `t = 5/6`: covered by the 6th evaluations plus `g(0,0)`.
(iii) Cyclic-boundary smuggling: the `A` stencil never reads below `i`,
and the one-sided lift needs nothing below; the cyclic identification only
reuses verified windows. (iv) `Q` upper side for `n >= 6`: times `>= 6`
contribute zero only because `A^6 x = 0` exactly, verified. (v) Scope
overreach: the note claims no `cK` bound, no classification, no survivor
relevance; the `refuted` label attaches solely to the alignment claim and
its anchored `K = 5` instance. Nothing to trim.

## E. Acceptance scope

Accept: 18/18 `g` evaluations; word counts and miss-times; row table;
both lifts; exact `Q = 5`; exact entry 6 for `A` and `T`; `H_6`
consistency; scope boundaries. The independent run agrees bit-for-bit on
the single admitted trajectory. Open (correctly so): everything about
larger constants, other heights, and full-fringe growth. No solution
claimed.

## F. Overwrite-robust loader repair (post-v3 catch, no new execution)

Caught before final acceptance: the v3 fallback pinned working-record
bytes to the v2 digest, so any replay after v3's own overwrite would fail
closed spuriously. Fixed in the script (v4, loader only; formula and
inputs untouched): one shared history loader locates the authenticated v2
either as raw v2 bytes (pre-overwrite) or via the working record's
`archived_executions` entry labelled `v2-provenance-repair` (post-
overwrite), authenticated by the FIXED canonical-JSON digest
`350b38f38af7cd1a1a9db07228eeea23dd8bef27f6bf9ae459238f5f807f13ec`
plus content source/admission SHA checks in both cases; OUT_REL is never
assumed to still be v2. Post-write load-only verification on the
already-written v3 artifact (`--check-load-only`, zero science recomputed,
zero writes, `/tmp` forced inaccessible): admission via primary-fallback
(note live at `f1b37c...`, exact original admission SHA re-verified),
history via `repo-fallback/archived-entry`, payload digest lead-equal
(`b58afe36...`), exit 0. Execution ledger unchanged: 3 executions, 2
repair reruns; this loader fix added no sixth-row rerun by design.

## G. Wrapper vs executed provenance (separate; no fourth execution)

The v3 record's `source_snapshot` pins the EXACT executed v3 wrapper and
is preserved untouched -- no science was rerun to attach anything newer.
The current wrapper file differs ONLY outside the science block, verified
by normalized diff of the computation span (identical formula, inputs,
loop, conversion, word/count assertions, canonical payload digest;
residual diffs: `return fail` vs raising-`fail` plumbing and the loader
refactor with `canonical()` helper). Explicit: current wrapper !=
executed wrapper; science block unchanged.
Metadata-only verification via `--verify-replay-inputs` (`--check-load-only`
alias) on the already-written v3 artifact, `/tmp` forced inaccessible,
exiting before any six-row computation: reference ok; admission via
primary-fallback with exact original SHA re-verified; history via
repo-fallback/archived-entry with v2 canonical digest authenticated;
artifact payload digest lead-equal; exit 0; zero writes. Ledger final: 3
scientific independent executions total (initial + 2 repair reruns), no
fourth. Both source versions (executed v3 snapshot in-record, current
wrapper file) are retained for the final audit to archive as distinct.
