# Independent review: signed mass on the full three-return domain

Status: `finite-exhaustive` sweep through phase complexity 16 with Outcome B
(no cancellation). This is FINITE evidence only, not an infinite proof. The
parent conjecture keeps status `inconclusive` at all depths.

## 1. Assignment and hypothesis

Second-worker falsification replay of the parent-selected conjecture (root
note `problem1_period_two_three_return_signed_mass.md`, read-only at
`/home/ryan/rule30-lab/proofs/informal/`, preserved unmodified):

> For `a in {p,u}`, `k>=2`, `x in O_(a,k)`, cut `c` with `L=c+1<k`, gap
> triple `g in {2,3,4,5}^3`: if the forced zero schedule of `x` begins
> `w E(g)` with `|w|=c` and `w E(g) u` avoids `uu`, `ttttt`, `ututtu`, then
> the dominant adjacent-shadow belief at depth `L` has nonzero signed mass
> `P(-1)`, where `P` sums `z^defects` over DISTINCT concrete dominant
> adjacent-shadow endpoints sharing the low `L` base-four digits, defects
> counting nonfull shadow fibers at every common digit.

Gate (fixed before execution): Outcome A (a zero on an admissible instance)
refutes the certificate (not belief nonemptiness, not Problem 1). Outcome B
(no zero in the sweep) only justifies an all-depth counting target, never a
bigger cap.

## 2. Method (independent oracle)

Derived from the proof notes + read-only reference only. The first worker's
module was never read, imported, or copied. Generators from the lift-recursion
note: `t(x)=x^((x<<1)|(x<<2))`, `u(x)=t(x)^1`,
`p(x)=t(x)^1^(0 if x odd else 2)`; `O_(p,1)={3}`, `O_(u,1)={1}`, levels by
forward generation with integer dedup (disjointness and exact bit lengths
`2k`/`2k-1` asserted). Forced schedule from the renewal/first-return rule
(`u` iff state 7 mod 16, `t` iff 11 mod 16, step through `p((state-3)>>2)`);
fibers by direct membership `M_(a,m)(q)={d:4q+d in O_(a,m+1)}`.

Verification order followed: hand derivations first (`t(1)=7`, `u(1)=6`,
`t(3)=13`, `O_(u,2)={6,7}`, `O_(u,3)={24,25,26,27}`, schedule(7)=`"ut"`,
fiber values including the empty fiber above quotient 7 at level 2 — my first
hand guess there was wrong and the code corrected me), then two independent
traversals (direct residue-grouping vs. the literal `W_(a,k,L)` seed-and-lift
recursion) compared bit-for-bit on every swept instance: 0 mismatches. The
known non-three-return cancellation (`u`, `0x198`, `k=5`, depth 1,
costs {0:1, 1:1}, mass 0) is reproduced exactly as an oracle check.

Search order as assigned: k ascending 2..16, phase p then u, integer x
ascending, cut ascending, lexicographic g ascending, stop at first zero.
Caps honored: 1 CPU, k<=16, schedule cap 64 (never hit; max observed schedule
need unremarkable), 1.04 s wall (limit 120 s), RLIMIT_AS 1 GiB.

## 3. Result: Outcome B (finite evidence only)

19 admissible instances (phase split 8 p / 11 u, 5 positive-cut, max cut 2),
exactly matching the published K=16 adjacent-shadow census counts
(8/11/19/5) — independent agreement on the instance set. No zero signed
mass. All 19 distinct-endpoint masses are positive (sorted): 6, 21, 22, 34,
127, 162, 579 (x3), 580, 1052 (x2), 1079 (x2), 1277, 1650 (x2), 1978 (x2).
Minimum: phase `u`, `k=15`, `x=0x1bd9c36b`, cut 2, depth 3, `g=(2,2,2)`,
schedule prefix `ttututut`, mass +6 over 54 endpoints. Sweep exhausted
(`stop_reason=exhausted`, last position phase u, k=16, cut 3).

Full record (atomic write, exact parameters, hashes, timings):
`results/problem1/20260905_three_return_signed_mass_independent.json`.

## 4. Mathematical seam audit

1. Restricted vs. full domain (`L<k`, level-0 top fiber). The conjecture
   quantifies only over `L<k`, excluding the full adjacent-shadow domain.
   At maximal depth `L=k-1` the deepest shadow quotient is 0, which the
   recursive formulation permits (fiber = seed-digit set: `{3}` for p,
   `{1}` for u) while a naive mask-table lookup would reject it (or return
   0000). I implemented the permitted variant. Boundary hits in sweep: 0 —
   no admissible instance reached `L=k-1` (max cut 2, so `L<=3<<k-1`). The
   Level-0 question is therefore live only for deeper sweeps, and any future
   all-depth argument must state its level-0 convention explicitly; proving
   the restricted claim never silently proves the full domain.
2. Final-u convention. Implemented per the stated convention: `w E(g) u`
   must avoid the forbidden factors (admissibility required), but the final
   `u` need not be an observed branch. Sensitivity: dropping the final-u
   admissibility check admits 2 extra instances (u, k=15 `0x1bd90387` and
   u, k=16 `0x6f670387`, both cut 0, `g=(2,2,3)`), with masses 579 and 1650
   — both nonzero, so the Outcome-B verdict is insensitive to this
   convention inside the swept box, but the instance set itself changes
   (21 vs 19). Any all-depth proof must fix this convention in its
   statement.
3. Endpoint deduplication. Implemented DISTINCT concrete endpoints (frontier
   sets hold each integer once). Sensitivity: representation-weighted masses
   (counting generator words) differ numerically on all 21 checked
   cylinders, and on the minimum instance (u, k=15, `0x1bd9c36b`) the
   weighted mass is -548 versus the distinct mass +6 — a sign flip. So
   dedup is load-bearing for the certificate's value and even its sign
   pattern; it is not a bookkeeping detail. Nonvanishing itself survived
   here (no weighted zero either), but a proof must be about the distinct
   sum exactly as conjectured.
4. Sign versus positivity. The claim is nonvanishing, not positivity. In
   this box all masses happened to be positive, but the derivative note's
   59 negative cylinders through complexity 28 (gap-222 slice) already
   refute any positivity strengthening. Kept distinct throughout.
5. Finite vs. infinite. This sweep covers exactly k<=16, both phases, the
   stated order, 19 instances. It proves nothing about k>=17, where the
   known complexity-23/25/27 positive-defect exceptions live. Outcome B
   triggers the all-depth counting target, not a bigger cap. No cap was
   raised.
6. Derivative identity verdict. Independently reviewed
   `problem1_period_two_signed_belief_derivative.md`: the "exact
   branching-derivative theorem" (`S = sum_y prod epsilon`) is a DEFINITION
   restated — it rewrites the summand `(-1)^c` as a product of local signed
   factors. Exact, but with zero nonvanishing content by itself; the note
   itself exhibits the `0x198` depth-1 cancellation as proof that the
   five-mask alphabet plus the local identity cannot force nonvanishing.
   Verdict: definition/restatement, not a theorem toward nonvanishing. Any
   nonvanishing proof must use the forced schedule + return-word
   constraints, as the note's "next target" section already states.
7. Old no-go constraints. (a) Endpoint-profile no-go: one-step paired
   profiles do not lift two-step paths (exact counterexample inside a
   gap-222 certificate) — constrains finite-state quotient routes, keeps
   the endpoint-concrete formulation necessary; does not decide this
   conjecture. (b) Mask-closure obstruction (six-state dominant-shadow
   transducer fails closure through k=25) and (c) budget-language/affine
   no-go: both close particular finite-state compressions, not the concrete
   signed sum; they neither imply nor forbid nonvanishing. (d) The
   `0x198` cancellation bounds the conjecture's domain: nonvanishing is
   false without the three-return admissibility hypothesis. None of the
   no-gos decides the parent conjecture either way.

## 5. Observations and blockers

- The minimum-mass instance sits on gap `(2,2,2)` at cut 2 — the same gap
  family as all known positive-defect exceptions. A counting proof will
  likely need to explain the `(2,2,2)` family first.
- `L=1` masses equal all-defect-zero counts minus defect-one counts (e.g.
  579 over 1223 endpoints); deeper instances show genuine cancellation
  structure (mass 6 over 54 endpoints), so the certificate is nontrivially
  close to vanishing already at k=15. This cuts both ways: it makes a
  refutation plausible at higher k, and makes a uniform nonvanishing proof
  necessarily delicate.
- No blockers. No commits made; parent owns conclusions and integration.

## 6. Protocol metadata

Base `b54f067210d5d8eeb1af3247c858c97af456497c`, branch
`research/signed-full-domain-review`, worktree
`/home/ryan/rule30-lab/.worktrees/signed-full-domain-review`. Reference
SHA-256 `358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`
(matches recorded value). Python 3.11.16, Linux 7.0.0-30-generic x86_64.
Tests: 9/9 pass via `tests/python/run_independent_signed_mass_tests.py`
(no pytest in this environment; direct runner, no network used). Sweep
1.04 s wall, RLIMIT_AS 1 GiB, 1 CPU, schedule cap 64, k<=16.

Changed files (uncommitted): `scripts/check_three_return_signed_mass_independent.py`
(new), `tests/python/test_three_return_signed_mass_independent.py` (new),
`tests/python/run_independent_signed_mass_tests.py` (new),
`results/problem1/20260905_three_return_signed_mass_independent.json` (new),
this note (new). `src/python/rule30_research_reference.py` untouched; root
`proofs/informal/problem1_period_two_three_return_signed_mass.md` (main repo)
read-only, preserved.

---

# Follow-up (2026-09-05 UTC): scope-audit review + mandatory fixes

## A. Separation lemma: refutation attempt FAILED (lemma stands)

Parent lemma (`problem1_signed_mass_scope_audit.md`, status `partial-proof`):
for every phase `a`, `k>=2`, `x in O_(a,k)`, `y in O_(a,k-1)`:
`x != y (mod 4^(k-1))`, hence no adjacent shadow at any `L>=k-1`.

Attack vectors tried, all closed:

1. Base-case error? Recalculated by hand and asserted in tests, both phases:
   `O_(p,1)={3}`, `O_(p,2)={12,13}` (low digits {0,1}); `O_(u,1)={1}`,
   `O_(u,2)={6,7}` (low digits {2,3}). At `k=2` the claim is exactly
   `{0,1}` vs `3` (phase p) and `{2,3}` vs `1` (phase u). Verified.
2. Projection-theorem failure? Checked finitely: `(s>>2) in O_(a,k-1)` for
   every `s in O_(a,k)`, both phases, `2<=k<=8`
   (`test_projection_theorem_finite_check`, passes).
3. Digit-position off-by-one? Residue equality mod `4^(k-1)` fixes the low
   `k-1` digits, in particular digit `k-2` = low digit of the twice-projected
   quotient. No off-by-one: quotient needs exactly `k-2` projections to land
   in `O_(a,2)` / `O_(a,1)`. Checked the chain counts for `k=2` (zero
   projections, direct) through general `k`.
4. Exhaustive residue collision search (direct sets, lemma NOT assumed):
   both phases, `2<=k<=8`, every `x/y` pair — zero collisions
   (`test_separation_lemma_finite_check_both_phases`, passes). The sweep
   itself repeats this check through `k=16`: `separation_violations=[]`.
5. Boundary emptiness without assuming the lemma: direct residue scans show
   the same-cylinder set is empty at `L=k-1` AND at `L=k` for every state,
   both phases, `2<=k<=6` (`test_empty_same_cylinder_at_boundary_depths`).

Independent derivation (reproduced from the audit, checked line by line):
equal residues mod `4^(k-1)` force equal digit `k-2`; projection puts
`x>>(2(k-2)) in O_(a,2)` with low digit in `{0,1}` (p) / `{2,3}` (u) against
`y>>(2(k-2)) in O_(a,1) = {3}` (p) / `{1}` (u) — contradiction. The step
`L>=k-1 => empty` uses only that mod-`4^L` equality implies mod-`4^(k-1)`
equality. No flaw found; the larger-power implication direction is correct.

Verdict: refutation attempt failed. Lemma keeps `partial-proof` (conditional
on the projection theorem, finitely confirmed through k=8 here, k=16 in the
sweep's internal check). Consequence accepted: the signed domain `L<k`
includes `L=k-1`, where any occurrence would have empty belief and zero mass;
an all-depth proof must bound `c+1<=k-2` or treat the boundary. In this box
no occurrence reaches `L=k-1` (max cut 2 at k>=12), and the all-cuts scan
finds ZERO occurrences with `L>=k` (`outside_domain_count=0`).

## B. Mandatory code fixes applied (all five)

1. Caps validated fail-closed at API (`validate_caps`, ValueError) and CLI
   (exit 2): `2<=max_k<=16`, `0<wall_limit<=120`. Deadline threaded through
   builds and scan; `status_for` maps wall-limit/truncation/separation
   surprises to `inconclusive` (`test_status_mapping_inconclusive`,
   `test_forced_tiny_deadline_reports_inconclusive` with wall=1e-9,
   `test_cap_validation_fail_closed`). RLIMIT failure and missing git commit
   now refuse to run (exit 2) instead of proceeding with a claimed bound.
2. Cuts now span `range(len(sched)+1)` (all cuts); only `L<k` evaluated.
   `L>=k` counted in `outside_domain_rows`, never silent success; capped
   schedules counted in `truncated_schedules` (0 in box), never success.
3. Hardware records actual CPU model (`Intel(R) Xeon(R) CPU E5-2690 0 @
   2.90GHz`), post-run peak RSS (43200 KiB), test+runner+reference hashes,
   full commit (fail-closed if unavailable), and `git_dirty_paths`
   (untracked owned files listed, since the script postdates the base
   commit). Output confined to repo; unique `tempfile.mkstemp` + `os.replace`.
4. Controls fenced: dedup/final-u numbers labeled CONTROL ONLY in code,
   record, and interpretation. Sign-flip witness retained WITH exact record:
   instance (u, k=15, x=0x1bd9c36b, cut 2, depth 3, g=(2,2,2)),
   distinct mass +6 vs representation-weighted -548. Corrected prose
   multiplicities regenerated from the array (test-asserted): 6, 21, 22, 34,
   127, 162, 579(x3), 580, 1052(x2), 1079(x2), 1277, 1650(x2 — corrected,
   was misstated x3), 1978(x2); sum 19 = instances. Instance = (k,a,x,c,g):
   19 instances on 17 cylinders (two cylinders carry two gap triples each:
   p/0x37b38787/cut-0 and u/0x1bd90387/cut-0). Equal mass/count alone does
   not verify identical instance sets — hence full per-occurrence rows
   (phase, k, state, cut, depth, gaps, schedule prefix, mass, belief_size,
   weighted_mass, same_cylinder) are in the JSON for exact parent comparison.
5. No pytest (confirmed absent); direct runner used, no downloads. Tests
   17/17 pass; counts recorded in JSON `verification`. Dead CLI flag
   `--timing-only` removed. `interpretation` field added. Semantic
   observations carry claim statuses below.

## C. First-worker code comparison (read-only, not edited)

Read `/home/ryan/rule30-lab/.worktrees/signed-full-domain-pass/experiments/
problem1_nonperiodicity/analyze_period_two_three_return_signed_mass.py`
(844 lines) in full. Findings:

- Agreement: generators, schedule stepping, E(g)/admissibility predicate
  (theirs restricts patterns to self-admissible complete words = 56, then
  checks `w+E(g)u`; mine iterates all 64 triples requiring `w+E` then
  `w+Eu` — provably the same instance predicate since `E(g)u` is a substring
  of `wE(g)u`), scan order (k, p-then-u, x, cut, lexicographic g),
  depth rule `L=c+1<k`, halt at first zero, wall-budget→inconclusive mapping,
  per-occurrence rows, interpretation field. Their dual frontier oracle
  (packed-shift vs bit-by-bit) is stronger than my shared-frontier base; I
  added a bit-by-bit `t` oracle test (3000+2 values) to narrow that gap —
  my belief-level independence (direct grouping vs literal W-recursion, 0
  mismatches) stands.
- Boundary divergence (no effect in box): at `L=k-1` theirs returns {} via
  the separation-lemma path (five-mask assertion would fire on a level-0
  fiber), while mine evaluates through the permitted level-0 seed-digit
  fiber. Under the lemma both give {} (residue filter empties first); box
  confirms (boundary_hits=0, no `L=k-1` occurrence). If the lemma ever failed
  at higher k, the two oracles would visibly disagree there — a feature, not
  a bug, for cross-checking.
- No off-by-one found in their cut/depth/stop logic. Their `same_cylinder`
  counts all same-residue endpoints (mine matches this definition, enabling
  direct row comparison). One note: their `exhaustive` flag does not require
  `truncated_schedules==0`; mine is stricter (any truncation → inconclusive).
- Machine-readable verdict on THEIR file: {"passed": true,
  "security_concerns": [], "logic_errors": [],
  "suggestions": ["consider requiring truncated_schedules==0 for the "
  "finite-exhaustive label, matching the independent replay"],
  "summary": "844-line analyzer reviewed read-only: instance predicate, "
  "scan order, depth rule, dual-oracle cross-checks, separation-lemma path, "
  "and status mapping all sound; no off-by-one or stop-order defect found; "
  "sole suggestion is stricter truncation gating of the exhaustive label."}

## D. Semantic observations (claim statuses)

- `finite-exhaustive`: 19 instances / 17 cylinders, k<=16, zero signed-mass
  zeros, min |mass| 6, exhausted, 0 truncations, 0 cross-mismatches.
- `empirical`: outside-domain count 0 at all cuts in box; final-u control
  rows (2, masses 579/1650); weighted sign-flip witness above.
- `partial-proof`: separation lemma (refutation failed, premises finitely
  confirmed); S!=0 ⟹ nonempty belief (immediate exact implication).
- `inconclusive`: parent conjecture at all depths; Problem 1.

## E. Machine-readable verdict (OWN work)

{"passed": true, "security_concerns": [],
 "logic_errors": ["earlier draft reported status finite-exhaustive on "
 "wall-limit stop and ranged cuts over range(k-1) without outside-domain "
 "accounting; both fixed and regression-tested in this pass"],
 "suggestions": ["parent replay should compare the 19 occurrence rows "
 "(not just totals) against the primary analyzer via canonical row hashes",
 "an all-depth proof must bound c+1<=k-2 or treat L=k-1, per the accepted "
 "separation consequence"],
 "summary": "Outcome B stands on the full all-cuts box: 19 instances, no "
 "zero, exhausted in ~1.1s; separation-lemma refutation failed on both "
 "phases with base-k2 digits pinned; all five parent code-audit issues "
 "fixed with regression tests (17/17 pass); controls fenced; full rows "
 "returned for exact parent comparison."}

Worktree/branch/base unchanged; no commits. Files changed (all uncommitted,
owned only): scripts/check_three_return_signed_mass_independent.py,
tests/python/test_three_return_signed_mass_independent.py,
tests/python/run_independent_signed_mass_tests.py,
results/problem1/20260905_three_return_signed_mass_independent.json, this note.
Reference file untouched. scratch/ contents pre-existing, untouched.
`src/python/rule30_research_reference.py` hash
358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01.
