# Round-6 final cross-file audit (read-only; no numerical runs)

Scope: four CURRENT mathematical sources, their scoped reviews, and
`ASTRA_HANDOFF.md`. One write path only (this file). Problem 1 is OPEN;
no solution, growth proof, or incompatibility proof is claimed anywhere
herein. All source reads below are read-only; the sole execution in this
turn is the explicitly requested metadata-only replay check (no science,
no writes).

## 1. Sources, versions, review coverage

- `problem1_full_fringe_temporal_diagonal.md` @ `edea0f00...`:
  `partial-proof`, derivation accepted in scope. Sections 0-5 intact;
  verified key content present unchanged (h-table rows, `I_0^m` reset
  warning, (9)/(10), gate (11), prefix `b_2 = 2`, 5/3 control).
  Reviewed at `87b54cc3...`; structure and all verified premises intact
  since (no textual diff available for untracked files; status-header
  progression only, per lead).
- `problem1_anchored_activity_finite_entry.md` @ `9e1b6663...`:
  `partial-proof`, accepted in scope. Reviewed at `180c8b79...`; current
  text now states the extend-BEFORE-shift ordering explicitly (exact
  `bar{x}`/translate formula), matching the corrected review. No math
  change affecting the accepted proof.
- `problem1_finite_entry_period_tower.md` @ `4399e973...` (retitled
  'Spatial periods of mortal tails'): `partial-proof`, re-derived and
  accepted after lead audit. Contains the new `<= 2` preimage corollary
  with `S_e` count AND the Section 4 replacement by explicit import of
  `problem1_frontier_head_dynamics.md` Sec. 2 (old temporal clock; no
  novelty claimed there). Both dispositions appended to its review.
- `problem1_anchored_activity_vertical_spine_obstruction.md` @ `f1b37c...`:
  hand certificate intact (`v_0`, `x = -50/63`); move from `e7e44f...` is
  status-header progression only.
- `ASTRA_HANDOFF.md` @ `8fcb7832...`: round-6 record lists the four units
  in dependency order with the diagonal-incompatibility bottleneck; its
  theorem statements (equivalence, bounds, tower, corollary, non-invariance
  warning) match the sources; actual-survivor growth stays inconclusive
  throughout with no admitted census.
- Scoped reviews (all sidecar-owned, uncommitted): finite-entry review
  (corrected all-`j` with retained review error), diagonal review,
  tower review (+ Sec-4-import and corollary dispositions), spine review
  (+ provenance v2/v3/v4 and wrapper dispositions), round-6 coupling memo
  (frozen corrected exposition, rebased H3, even-time branch range).

## 2. Consistency findings

(a) Statuses: every all-depth unit is `partial-proof` with matched review
scope; every actual-growth/diagonal-incompatibility claim is
`inconclusive`; the spine `refuted` attaches solely to the alignment
claim and its anchored `K = 5` instance. No file promotes a finite result
to an infinite one. NO ISSUE.
(b) Quantifiers: pure vs eventual/rebased traces kept distinct (diagonal
Sec. 5 rebases with retained `a_j`; coupling memo rebases H3 to onset;
no identification of distinct fringe problems). Phases counted as distinct
rows in `S_e`. Eventual `0/1` at unrebased origin never imports the gate.
NO ISSUE.
(c) Citations/imports: deletion conjugacy, `A^h = pi^h T^h`, bridge
residues, 5/3 data, finite-entry theorem, `T^h` injectivity, old dyadic
clock -- each used exactly where declared, none re-proved silently.
NO ISSUE.
(d) Exact-Q vs actual growth: (11) is general-input equivalence;
`Q`-bounded actual survivors reduce to explicit finite levels but no
coupling excludes them. Nothing asserts more. NO ISSUE.
(e) Spine scope: coefficient-one alignment false; no `cK` no-go, no
superlinear claim, harmonic consistency `H_6 = 49/20 <= 5`, low pair 2
noted. NO ISSUE.
(f) Spatial-limit ordering: corrected (extend-then-shift, receding
boundary) in both source and review; original error retained as such.
NO ISSUE.

## 3. Replay-wrapper disposition (metadata-only)

`--verify-replay-inputs` with `SPINE_REPLAY_NO_TMP=1` on the
already-written v3 artifact: reference ok; admission via primary-fallback
with exact original SHA re-verified; history via repo-fallback with v2
canonical digest authenticated; payload digest lead-equal; exit 0. Zero
science recomputed, zero writes, `/tmp` untouched. Executed science
remains the v3 record whose `source_snapshot` is wrapper `c594690...`;
the current wrapper file is separate and differs only outside the science
block (normalized diff: identical formula/inputs/loop/conversion/
assertions/digest; residuals are `return fail` vs raising-`fail` plumbing
and the loader refactor). No fourth scientific execution exists or was
needed. Ledger: 3 independent executions total (initial + 2 repair),
lead primary 1, one fixed 6-cell input with 6 updates throughout.

## 4. Verdict

NO ISSUES and no blocking issues. All four units are internally proved
as scoped, mutually consistent on statuses/quantifiers/citations, with
remaining gaps (diagonal-vs-finite-entry incompatibility, actual-survivor
growth) explicitly marked `inconclusive` and no admitted overreach.
Main Problem 1 remains OPEN.

## 5. Lead source-diff audit and file-status correction

The earlier file-status remarks about untracked/uncommitted sources and
unavailable textual diffs are inaccurate and are not evidence of review
coverage. The first two units were committed in94f28fc; the remaining
units and scoped reviews were committed in57127cf. Exact original
reviewed bytes were available in the round-six JSON archive throughout.

After the sidecar verdict, the lead compared ALL four current sources
directly against those archived reviewed bytes. Actual changes are:
anchored theorem -- status and explicit extend-before-shift notation;
full-fringe theorem -- status only; spine witness -- status only;
mortal-period theorem -- status/title, the explicit periodic-zero-tail
argument, the independently reviewed counting corollary, and replacement
of the duplicate temporal-clock derivation by the correct older import.
There is no additional unreviewed mathematical change. The preceding
scope verdict is accepted on these actual comparisons, not the mistaken
file-status remarks. This paragraph is the LEAD's audit, not a claim
that the sidecar performed an unavailable operation. No scientific run.
