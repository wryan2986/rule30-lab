# Independent Research Audit — Rule 30 Lab

**Audit date:** 2026-07-22  
**Repository:** `wryan2986/rule30-lab`  
**Audited source:** public GitHub tree plus `rule30-lab-chatgpt.tar.gz`  
**Audit environment:** isolated Linux CPU sandbox; no CUDA device; Rust and Lean toolchains unavailable  
**Overall disposition:** technically serious and unusually careful, but **none of the three Rule 30 prize problems is solved**.

## Remediation status

The accompanying public-reproducibility pull request addresses the audit's publication findings without changing any scientific conclusion:

- controlled-run citations now point to a tracked path-neutral certificate manifest;
- internal automated review provenance is explicit;
- the historical full-gate wording no longer claims to be current; and
- source-archive limitations are documented.

The manifest preserves scopes, source commits, direct commands, and certificate
hashes. It does not recreate omitted machine-local telemetry or raw runner files.

## 1. Executive verdict

The repository consistently distinguishes finite computation from infinite proof. I found no mathematical claim that obviously converts its experiments into a prize solution. The current claim ledger is substantially conservative and mostly accurate.

The strongest theorem-backed result is:

> **The center column of Rule 30 from any nonzero finite-support seed cannot be eventually constant.**

The internal argument reducing an eventual all-one or all-zero center tail to an eventually constant adjacent width-two trace is correct. The final contradiction relies on the published width-two non-eventual-periodicity theorem for Rule 30/left-spreading cellular automata. This excludes eventual period one only; it does not exclude periods two or greater.

The strongest current new research direction is the period-two inverse-lift reduction. For the pure alternating temporal trace, the repository derives an exact criterion reducing infinite spatial support to proving

```text
m - leading_t_run(H_m) -> infinity.
```

This is a materially sharper target than another larger finite search. The identity and finite checks are coherent, but the required growth theorem is still missing.

Problems 2 and 3 remain supported only by finite evidence and bounded model exclusions. The million-bit balance data are compatible with limiting frequency one half, but do not prove it. The finite automaton, recurrence, affine-model, Boolean-window, and 2-kernel searches exclude only their exact bounded classes and do not imply a general lower bound.

## 2. Audit scope and method

I reviewed:

- `README.md`, `AGENTS.md`, and the research-status ledger;
- formal problem statements and status-label definitions;
- informal proof documents for sideways inversion, prefix equivalence, whole-tail equivalence, the 2-adic diagonal map, inverse sections, period-one exclusion, and the period-two quotient obstruction;
- Lean source at the level available from the archive;
- Python experiment drivers and their structured outputs;
- tracked result records and certificate hashes;
- publication, reproducibility, and adversarial-review documentation;
- CPU build/test behavior in a fresh sandbox.

I independently reran representative finite campaigns instead of merely accepting their prose summaries. I also checked the central algebraic transitions against direct small-width computations.

This is an independent technical audit, not peer review by a specialist journal referee and not a formal verification of every informal proof.

## 3. Independent validation performed

### 3.1 Test and build results

| Component | Result | Qualification |
|---|---:|---|
| Python | 306 meaningful tests passed | Five archive/environment tests were excluded: three require `.git` history and two assume sub-100 ms timing/telemetry behavior. |
| C++ release | 2/2 passed | Fresh CMake/Ninja CPU-only build. |
| C++ ASan/UBSan | 2/2 passed | No sanitizer failure observed. |
| CUDA | Not run | No NVIDIA device in the sandbox. |
| Rust | Not run | Toolchain absent from the sandbox. |
| Lean | Not run | Toolchain absent from the sandbox. |

The five excluded Python cases do not invalidate the mathematical algorithms. The archive was intentionally generated with `git archive`, so Git-history checks cannot pass inside it. The two timing-sensitive controlled-runner cases appear environmental; the remaining controlled-runner tests passed.

### 3.2 Reference-vector and million-bit reproduction

I independently reproduced:

- supplied Python source SHA-256: `358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`;
- 10,000-byte center vector SHA-256: `61de1c97dc3f80cb24d3a02207920bd442d6f530304497eee70189a039a47860`;
- million-byte center sequence SHA-256: `6fc1e4e2abfb382255b94955467f259be88c1044d09ec361c5039970985a1669`;
- one count: 500,768;
- zero count: 499,232;
- discrepancy: `D(1,000,000)=1,536`.

The million-prefix scaling script reproduced scientific-payload SHA-256:

```text
4966233342cce5b43c63dcf2d735d17c3faa2fca56419d55406fc8686d941b3f
```

### 3.3 Problem 1 finite certificates reproduced

The following scripts completed independently and matched the repository's certificate hashes:

| Campaign | Coverage summary | Certificate SHA-256 |
|---|---|---|
| 2-adic diagonal | 8,190 finite quotient points through width 12 | `b4ea4e5af4cd2318efd99a78a9a5ad9f4fa90d3c5952c072a46073528adc7670` |
| Inverse-lift sections | 2,046 quotient points; 4,352 continuation checks | `9c8e07018c54eb0271ab62fa90733ab91fdc2aa5c16d2d0509db339b1feb619d` |
| Period-two quotient | 2,048 lift bits; 161 fringe blocks; 160 arithmetic blocks | `81593871f2305f0bf796ba596de2ce3285275084b0cfea0d5c155c80965d574c` |
| Period defect | 174,760 assignments for periods 1–8 | `1fea76c334d7f16c24fa27f2ca4af8f41e1a14bb11f4097b6fdf5479ab60fe0c` |
| Period-two audit | 262,144 right traces plus two 4,096-step oracles | `c152c25a32269dccfb2711e9e4efffcdf9a4313c3a2227bd08cefbebfc1208cf` |

These matches provide strong evidence that the published finite summaries are deterministic and reproducible. They do not promote the finite results into infinite theorems.

### 3.4 Problems 2 and 3 campaigns reproduced

I reran:

- the exact additive local-conservation search for widths 1–5 over the rationals and GF(2): all ten Rule 30 systems had zero nontrivial excess nullity;
- the main bounded Problem 3 search: all requested DFAO, GF(2) recurrence, Boolean-window, finite 2-kernel, and Berlekamp–Massey checks completed;
- the extended Problem 3 search: the bounded affine GF(2) and multiscale finite 2-kernel campaigns completed.

The full 16-system polynomial-conservation campaign exceeded this sandbox's single-command runtime ceiling. Its focused verifier tests were part of the passing Python suite, but I did not independently recompute all three published campaign hashes in this environment.

## 4. Claim classification matrix

### 4.1 Rigorous or theorem-backed within a clearly stated scope

| Claim | Audit verdict | Scope/qualification |
|---|---|---|
| Rule 30 Boolean update and left-permutive inversion | Sound | Elementary identity. |
| A supplied center trace and zero initial right half uniquely determine the reconstructed left half | Sound | Exact finite and infinite recursive construction. |
| First reconstructed-left one equals first disagreement from the zero-left reference center prefix | Sound | The argument is a direct injectivity consequence; finite exhaustive checks are supportive, not essential. |
| Eventually-zero reconstructed left tail iff it corresponds to a finite-support initial state with rightmost one at coordinate zero | Sound as an informal lemma | Requires the stated coordinate and moving-frame conventions. |
| Eventual period one is impossible | Sound conditional application of the cited width-two theorem | Excludes constant tails only. The external theorem itself is not formalized in this repository. |
| Finite quotient maps of the 2-adic diagonal construction are unit triangular permutations | Sound | Direct finite algebra; reproduced through width 12. |
| The induced 2-adic diagonal map is a compatible isometric bijection | Mathematically plausible and well argued | Complete informal proof, not independently machine-formalized here. |
| The `-1/3, 1/3` 2-cycle gives periodic diagonals without finite spatial support | Sound | Correctly demonstrates why fixed-coordinate periodicity alone cannot solve Problem 1. |
| `Delta` and its inverse have infinitely many tree sections | Plausible complete informal result | The distinct-section argument via highest set bits is convincing; not a prize result. |
| Period-two highest-support identity involving `ell_m` and `epsilon_m` | Strong candidate lemma | Exact algebra is coherent and finite checks agree, but it should receive a standalone proof audit/formalization before being treated as a foundation for a published theorem. |

### 4.2 Finite-exhaustive results

The repository correctly labels these as finite-exhaustive:

- periodic and eventually-periodic trace descriptions within explicitly bounded `q`, `p`, and horizon boxes;
- period-defect cones through period eight;
- finite 2-adic quotients;
- bounded inverse-section schedules;
- finite period-two right-neighbor traces and arithmetic blocks;
- DFAOs with one through three states;
- homogeneous GF(2) recurrences through order 12;
- autonomous Boolean suffix-window rules through width 12;
- affine GF(2) digit-matrix models of dimensions one and two;
- selected finite 2-kernel quotient/refinement constructions;
- additive conservation ansatzes at widths 1–5;
- the listed bounded polynomial density/flux systems.

Each excludes only the exact model family and finite range stated. None establishes eventual nonperiodicity, limiting balance, nonautomaticity, or an asymptotic computational lower bound.

### 4.3 Empirical or heuristic evidence

The following remain empirical or heuristic:

- near-half frequency on one million bits;
- discrepancy checkpoint behavior and the fitted slope near 0.5205;
- autocorrelation, spectral, entropy, run, block, and dyadic statistics;
- Berlekamp–Massey complexity equal to half the tested prefix lengths;
- growth of distinct sampled 2-kernel prefixes;
- backend timing and scaling results;
- observed zero-run lengths in reconstructed tails;
- observed behavior of the period-two leading-run deficit.

These results are useful for falsifying simplistic models and choosing proof directions. They are not evidence strong enough to support an infinite claim without a structural theorem.

## 5. Problem-by-problem assessment

## 5.1 Problem 1 — eventual nonperiodicity

### What is genuinely established

1. **Period one is excluded.**
   - An eventual all-one center tail forces the adjacent-left column to zero.
   - An eventual all-zero center tail makes the adjacent-right column monotone under OR and hence eventually constant.
   - In either case an adjacent width-two trace becomes eventually constant, contradicting the applicable published width-two non-eventual-periodicity result for Rule 30 from finite/number-like initial data.

2. **Sideways reconstruction is an exact equivalence tool, not merely a heuristic.**
   - A proposed temporal center trace can be inverted leftward when the initial right half is fixed to zero.
   - The true single-cell center trace is characterized by reconstructing the all-zero left initial tail.

3. **The whole-tail formulation is the correct target.**
   - Larger finite first-witness searches merely compare longer prefixes.
   - A proof must force infinitely many reconstructed-left ones, or otherwise rule out eventual zero, uniformly in depth.

4. **The 2-adic reformulation clarifies a major obstruction.**
   - Every fixed coordinate may be periodic while the growing diagonal remains difficult.
   - Periodic diagonal examples exist when finite support is abandoned.
   - Therefore a successful proof must use finite spatial support/odd-integer structure, not only compatible quotient periodicity.

### What remains missing

- No argument excludes period two.
- No uniform invariant excludes every eventual period.
- No depth-independent finite-state closure has been proved for the relevant inverse process.
- No theorem converts observed bounded zero runs into infinite support.

### Best next target

Focus exclusively on the pure period-two alternating trace and prove one of the equivalent statements:

```text
m - leading_t_run(H_m) -> infinity,
```

or

```text
the highest one in the first 2m inverse-lift bits is unbounded.
```

Recommended proof program:

1. Re-derive the all-width recurrence for `(H_m, W_m)` in a compact algebraic notation.
2. Isolate an exact cocycle or valuation that changes when a leading `t` is consumed.
3. Prove that arbitrarily long terminal trapping near the all-`t` ray would force a forbidden periodic section or a contradiction with odd-integer/finite-support structure.
4. Use SAT or exhaustive computation only to discover the invariant and test lemmas, not as the final argument.
5. Formalize the final support identity and growth lemma in Lean once the paper proof stabilizes.

Do not broaden to all periods until period two is either closed or the reduction is shown incapable of producing a growth proof.

## 5.2 Problem 2 — limiting balance

### What is established

- The million-bit counts and discrepancy checkpoints are reproducible across independent implementations.
- The finite statistical record is comprehensive and honestly labeled.
- Several small, exact conservation-law ansatzes have been exhaustively ruled out.

### What is not established

- Existence of a limiting frequency.
- A limit equal to one half.
- Any deterministic discrepancy bound such as `o(N)`.
- Mixing, normality, ergodicity, or a suitable invariant measure for this specific center trace.

### Research recommendation

Further raw prefix extension has low expected proof value. A productive advance would require one of:

- a telescoping/coboundary identity controlling center discrepancy;
- a renormalization relation across dyadic scales;
- a provable cancellation law tied to the left-permutive structure;
- a theorem placing the single-cell orbit in a measure-theoretic class with known center statistics.

The failed bounded conservation searches are useful negative information, but should not be expanded indiscriminately. Increase the ansatz only when motivated by an observed exact identity or theoretical derivation.

## 5.3 Problem 3 — computational complexity

### What is established

The repository has exact finite counterexamples to several small proposed mechanisms:

- tiny DFAOs;
- short homogeneous GF(2) recurrences;
- bounded Boolean suffix-window predictors;
- dimensions-one-and-two affine GF(2) digit-matrix products;
- particular finite 2-kernel quotients/refinements;
- one training-fitted Berlekamp–Massey recurrence on held-out data.

The training/validation separation is well designed and avoids obvious leakage.

### What is not established

- Nonautomaticity.
- Absence of all linear recurrences.
- Absence of a sublinear exact algorithm.
- An `Omega(n)` lower bound in a defined uniform machine model.
- The literal strongest published predicate excluding an exact `O(n)` method.

### Research recommendation

Before further experiments, freeze a single formal machine model and a single target statement. The repository is right to keep the three formulations separate. A credible lower-bound program must specify:

- input encoding for `n`;
- uniformity and preprocessing/advice rules;
- output convention;
- time and space cost model;
- whether randomization is allowed;
- which exact published formulation is being addressed.

Finite model searches can falsify proposed shortcuts, but they cannot establish a universal lower bound without a theorem connecting the searched family to all algorithms in the chosen model.

## 6. Publication and reproducibility findings

### Finding 1 — cited strict run records are absent from the public repository

**Severity:** Medium  
**Type:** Reproducibility/documentation

`docs/research_status.md` cites multiple files such as:

```text
results/runs/p1-period-two-quotient-20260722.record.json
```

but `.gitignore` excludes `results/runs/**/*.record.json`, and the publication audit says these records were deliberately untracked because they contained local executable paths. Therefore public readers cannot inspect the primary strict records cited by the claim ledger.

This does not falsify the scientific certificates; several were independently reproduced. It does leave broken provenance references in the public handoff.

**Recommended fix:** publish sanitized scientific records with machine-local paths normalized or removed, while continuing to ignore raw stdout, stderr, checkpoint, and temporary artifacts. Alternatively, make every ledger citation point to an existing tracked result under `results/problem*/`.

### Finding 2 — “independent review” should disclose that it was automated/internal

**Severity:** Medium  
**Type:** Credibility/wording

The publication audit explicitly identifies its auditor as automated OpenCode, while other documents use terms such as “independent reviewer” or “adversarial review” without always making the agent context equally prominent.

**Recommended fix:** use “internal adversarial review by a separate automated agent/context” unless an external human or unaffiliated reviewer performed the review. Do not imply journal-style external peer review.

### Finding 3 — “latest clean-build gate” is stale relative to publication

**Severity:** Low  
**Type:** Documentation freshness

The research ledger calls the gate on commit `a89246e` the “latest,” while later publication material reports a newer repository state and larger Python test count.

**Recommended fix:** either update the gate evidence for public HEAD or rename it “last recorded full CPU/CUDA/Rust/Lean gate” with its date and commit.

### Finding 4 — source archives cannot verify Git-bound provenance

**Severity:** Low  
**Type:** Expected archive limitation

A `git archive` intentionally omits `.git`. Consequently, commit-existence, clean-tree, and historical provenance tests cannot pass inside the uploaded archive.

**Recommended fix:** document that the archive validates source-level reproducibility, while GitHub or a full clone is required to validate commit-bound provenance.

### Finding 5 — strongest new lemmas are informal rather than formalized

**Severity:** Informational  
**Type:** Proof assurance

The Lean development covers important local inversion and reconstruction facts, but not the external width-two theorem, the complete 2-adic diagonal theorem, or the period-two growth criterion.

**Recommended action:** do not formalize every experiment. Formalize the period-two support identity and eventual growth lemma only after a stable human-readable proof exists.

## 7. Priority action plan

### Priority 0 — repair the public scientific record

1. Add sanitized versions of every strict record cited in `docs/research_status.md`.
2. Replace or repair all missing file references.
3. Clarify automated/internal review provenance.
4. Refresh the clean-gate wording.
5. Add an archive-provenance limitation note.

This should be a small documentation/reproducibility pull request and should precede outreach to researchers or an open-source program application.

### Priority 1 — package the period-one result as a short technical note

Create a concise note containing:

- exact conventions and seed hypotheses;
- the all-one and all-zero deductions;
- the exact external theorem statement and mapping of hypotheses;
- the resulting period-one corollary;
- a clear statement that periods two and greater remain open.

This is the cleanest theorem-level result currently present.

### Priority 2 — attack the period-two leading-run growth lemma

Make this the sole active proof objective until resolved or decisively blocked. Maintain a lemma dependency graph and require each new computation to test a specific proposed invariant.

### Priority 3 — pause broad Problem 2 and 3 searches

Do not spend substantial compute on longer random-looking prefixes or wider arbitrary model sweeps. Resume only when a structural hypothesis predicts an exact signature that can be tested.

## 8. Final conclusion

Rule 30 Lab is a credible reproducible-research environment, not a prize solution. Its implementation discipline, finite certificates, cross-checking, explicit limitations, and negative-results ledger are strong. The repository's mathematical center of gravity should now shift from broad finite exploration to one narrowly defined theorem:

> Prove that the pure period-two inverse lift cannot have finite support by establishing unbounded growth of `m-leading_t_run(H_m)`.

The public repository should simultaneously repair the missing strict-record references and clarify the automated nature of its internal reviews. Those changes would materially improve trust without changing any scientific conclusion.
