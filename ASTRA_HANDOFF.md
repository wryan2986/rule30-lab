# Astra handoff (2026-09-04, base `a9af399`)

Repo does not solve any prize problem. Finite evidence is never proof of an infinite statement. Claim statuses (`empirical`, `finite-exhaustive`, `partial-proof`, `inconclusive`, ...) per `docs/experiment_protocol.md`.

## The three prize problems (`docs/problem_statements.md`)

Rule 30: `x_j(t+1) = x_{j-1}(t) XOR (x_j(t) OR x_{j+1}(t))`, single-cell seed (`x_0(0)=1`), center `c_t = x_0(t)`, `c_0 = 1`.

1. **Problem 1 (priority):** is `(c_t)` eventually periodic? Expected answer no. Only eventual period one is excluded.
2. **Problem 2:** does `(1/N) sum_{t<N} c_t -> 1/2`? Campaigns paused.
3. **Problem 3:** exact complexity of computing `c_n` (model/encoding/output/uniformity must be fixed per claim). Campaigns paused.

## Priority and critical path (`AGENTS.md`, `docs/problem1_focus_program.md`)

Problem 1 only. Target implication: if a proposed center trace `C` with `c_0=1` is eventually periodic, its left-permutive reconstruction `L(C)` (right half forced zero) is not eventually zero. Frozen: larger prefix stats, first-witness boxes (= prefix comparisons only), Problems 2/3 sweeps, benchmarks, ports, broad Lean work.

## Established exact / all-depth results (all `partial-proof` or conditional; Problem 1 still open)

- Period-one exclusion for every finite seed (all-one tail forces left column zero; all-zero tail forces right neighbor eventually constant; contradicts width-two theorem). Lean covers local steps only; external width-two theorem not formalized.
- Whole-tail equivalence: eventually-zero reconstructed tail iff finite-support initial config with rightmost one at 0; its center is the growing diagonal `bit_t(T^t(S))`, `T(S) = S XOR ((S<<1) OR (S<<2))`, `S` odd. Fixed bit `k` has period dividing `2^k` (no diagonal control).
- `Delta` is a unit-triangular isometric 2-adic bijection; eventual periodicity iff rational output. Cycle `T(-1/3)=1/3`, `T(1/3)=-1/3` maps to period-one traces: fixed-coordinate periods alone can never contradict.
- Inverse-lift even/odd section recurrences exact; `Delta circ T^j` sections pairwise distinct, so universal finite-state routes for `Delta`/`Delta^-1` are closed.
- Prefix equivalence: first nonzero reconstructed-left depth = first center-prefix disagreement (checked horizons 0-16). Larger first-witness searches add nothing.
- Adjacent-shadow reduction (exact, sufficient but stronger than necessary): three-return zero-penalty plateau implies `T_{a,k} NOT SUBSET P_{a,k-1}`. All-depth inclusion `T_{a,k} \subseteq P_{a,k-1}` would prove every three returns carry positive phase penalty.
- Separation lemma (`partial-proof`, conditional on projection theorem): `x in O_(a,k)`, `y in O_(a,k-1)` implies `x != y (mod 4^(k-1))`; no adjacent shadow at any `L >= k-1`.
- Signed-slice lift (exact): `S(N) = sum_n epsilon_m(n) V_n(parent(N))` (proof: `proofs/informal/problem1_period_two_signed_slice_recursion.md` on sibling branch, see below). Scalar parent mass/sign provably insufficient (e.g. mass 1650 -> children 104 vs 605; positive parents -> children -83 vs +2).
- Derivative identity `S = sum_y prod epsilon` is a restated definition: zero nonvanishing content alone. `S != 0` implies nonempty belief (immediate, exact); converse false.

## Finite-only evidence (explicitly not proofs)

- Full-domain sweep k<=16, both phases, 56 gap triples: 19 occurrences / 17 cylinders, zero signed-mass zeros, min |mass| 6 (`u`, k=15, `0x1bd9c36b`, cut 2, `(2,2,2)`, +6 over 54 endpoints). Outcome B. Records: `results/problem1/20260905_three_return_signed_mass*.json`.
- Gap-`222` census thru k=28 (C++): 5,162 cylinders, 0 zeros, 59 negatives, min |mass| 1 (`0x1bcd3a7b3fdfb`, k=25). Slice-ancestor census thru k=28: 7,363 cylinders, 0 zeros.
- Adjacent-shadow census k<=20: 210 occurrences, 0 violations. Older boxes (sideways horizons, conservation widths 1-5, 5,898 DFAOs, recurrences, 2-adic/quotient campaigns) exhaustive only in stated boxes.

## Failed approaches / no-go results (do not retry without a new mechanism)

- Signed nonvanishing is NOT universal: `u`, k=5, `0x198`, depth 1 has costs {0:1, 1:1}, mass 0. Bounds the conjecture to the three-return admissible domain.
- Scalar and sign-only induction dead (counterexamples above); additive single-letter cocycles trivial; quadratic GF(2) range-3 forces constant terminal potential; six-state shadow-mask closure fails; signature simulation too coarse; budget-language/affine no-go; endpoint profiles do not lift paths.
- Period-two quotient mirages, all exact counterexamples: seven-block driver fails block 153; head+depth-2 portraits collide (blocks 11 vs 55) with different successors; endpoint law `s_(2^k-1) = k mod 2` fails at k=11.
- Mask-only or fixed-modular endpoint quotients refuted (realization-splicing); majority/density false (292 cylinders keep < half); positivity false (59 negatives).

## Strongest Problem 1 pathway

Eventual period two -> three consecutive returns must carry positive phase penalty -> adjacent inclusion `T \subseteq P` -> concrete dominant belief nonempty -> signed-mass nonvanishing -> five-component slice induction along the forced `t`/`u` schedule.

## Exact unresolved bottleneck

No all-depth proof that signed mass never vanishes on the full three-return domain (both phases, all 56 triples): prove the slice vector never lands in the cancellation hyperplane `sum_n epsilon_m(n) V_n = 0` along any forced schedule. Separately, the separation lemma empties `L >= k-1`, but the conjectured domain `L < k` still contains the lethal `L = k-1` (and `L >= k` matters for the original inclusion): an all-depth proof must also establish `c+1 <= k-2` for every occurrence or treat the boundary. Next census-cap increase is NOT the step; a counting/invariant argument is.

## Five-component signed-slice formulation (latest route, lives on sibling branch)

For parent cylinder, `V_n = sum_{p : M(p)=n} (-1)^{c(p)}` over `n in {0000,0011,1011,1100,1111}`; `S = sum_n V_n`; child mass `S(N) = sum_n epsilon_m(n) V_n(parent)`. Full note + analyzer + tests only on `origin/research/period-two-signed-slice-recursion` (`git show origin/research/period-two-signed-slice-recursion:proofs/informal/problem1_period_two_signed_slice_recursion.md`); NOT merged into this branch. Next target per that note: cone/ordering/parity/boundary invariant on `V` preserved by the return schedule that excludes the hyperplanes.

## Reasoning traps

- Finite absence (any `k` cap, any box) proves nothing at `k+1`; the k=23/25/27 positive-defect exceptions live above the k<=16 full-domain box.
- Quantifiers: conjecture is over every phase/complexity/state/cut/gap-triple; one uncaptured case kills the certificate (not the belief, not Problem 1).
- Endpoint dedup is load-bearing: min instance is +6 distinct vs -548 representation-weighted (sign flip). Final-`u` admissibility convention changes the instance set (19 vs 21). State conventions explicitly before any proof.
- Negative mass is fine; only exact zero on an admissible instance refutes. Do not splice endpoints across cylinders into abstract paths. Do not return to universal finite-state, mask-only, or scalar routes.

## Read first

1. `proofs/informal/problem1_period_two_three_return_signed_mass.md` (conjecture + gate)
2. `proofs/informal/problem1_signed_mass_scope_audit.md` (separation lemma + boundary)
3. `proofs/informal/problem1_three_return_signed_mass_independent_review.md` (Outcome B, seam audit, fixes)
4. `proofs/informal/problem1_period_two_three_return_adjacent_shadows.md` (reduction + census)
5. `proofs/informal/problem1_period_two_signed_belief_derivative.md` (derivative = definition; k<=28 census; `0x198`)
6. Sibling: `origin/research/period-two-signed-slice-recursion` note/analyzer/tests (five-component route)
7. `docs/problem1_focus_program.md` (admission/stopping; status 2026-07-22, predates frontier)
8. `AGENTS.md` (non-negotiables; never edit `src/python/rule30_research_reference.py`)

## Branch / PR status

- `main` = `b54f067` (merge PR #48, 2026-08-02). No open-PR check possible offline (`gh` absent); PRs #46-48 merged in history.
- Newest work is LOCAL-ONLY: `research/three-return-signed-mass-full-domain` (`a9af399`, 2026-09-04), one commit over `main`, never pushed. This branch `research/astra-next` = that commit + this file.
- Newest REMOTE work: `origin/research/period-two-signed-slice-recursion` (`c79b67a`, 2026-08-02), sibling off `main`, unmerged; its files are absent from this checkout (available via `git show origin/...`). Fetch 2026-09-04 confirmed up to date.
- 4 sister worktrees at `b54f067` (`.worktrees/`, untracked): `signed-full-domain-pass/-review`, `three-return-signed-cancellation/-check`. Note: `tests/python/test_period_two_three_return_signed_mass.py` hardcodes branch `research/signed-full-domain-pass`, so it fails elsewhere by construction (see baseline).

## Highest-value next questions

1. What invariant on the five-component slice vector (cone, ordering, parity, boundary) is preserved by the forced `t`/`u` schedule and excludes `sum_n epsilon_m(n) V_n = 0` on all 56 gap triples?
2. How to prove `c+1 <= k-2` for every three-return occurrence (or separately discharge `L = k-1` and `L >= k`), given the separation lemma?
3. Do the 19 per-occurrence rows of the primary analyzer match the independent replay row-for-row (canonical row hashes), not just in totals?
4. What explains the `(2,2,2)` family (min-mass instance, all known positive-defect exceptions) -- the likely first refutation or first lemma?
5. How to unify the sibling slice line (gap-`222` thru k=28) with the full-domain line (all triples thru k=16) without raising any cap?
