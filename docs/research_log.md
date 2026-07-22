# Research log

Times and result filenames use UTC unless stated otherwise. Commit references
identify logical milestones; exact experiment commits and argv are also stored
inside the corresponding JSON records.

## 2026-07-21

- Created the WSL-native repository and imported the supplied reference source
  unchanged in commit `8296a83`; the preserved file SHA-256 is
  `358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`.
- Scaffolded the private MIT-licensed repository (`8dd605e`) and recorded
  Windows 11, WSL 2.7.3, Ubuntu 26.04, Ryzen 5 3600, RAM, disk, and one RTX
  2060 SUPER with 8,192 MiB and compute capability 7.5.
- Installed only the approved local build dependencies. Diagnosed the Ubuntu
  CUDA 13.1/glibc 2.43 header conflict and selected NVIDIA WSL CUDA 13.3
  development components. No Linux display driver or hardware setting was
  installed or changed. Details are in `docs/system_changes.md`.
- Added the independent cell-array oracle and provisional vectors (`a59f31b`,
  `4e5fc47`), then promoted complete rows through step 255 and 10,000 center
  bytes only after C++ and Rust agreement (`c4f3ade`).
- Reproduced the supplied-Python million-bit counts and hash (`3052e80`), then
  implemented packed scalar/runtime-AVX2 C++ (`4a6747c`) and independent safe
  packed Rust (`26ef846`). The compiled C++ million-bit reproduction was
  recorded in `aa1dea8`.
- Implemented deterministic CUDA batched-period search (`2d8cb15`) and later
  direct evolution plus batched sideways reconstruction (`3eb6e51`). CPU/GPU
  consistency covered partial grids, word boundaries, and forced chunks.
- Added finite Problem 2 diagnostics (`dbc6d98`), exact bounded local
  conservation searches (`01656dd`, result `9b7e8c3`), million-bit scaling
  analysis (`a158dd0`), spectral record (`2420997`), and benchmark records
  (`0111968`). These remain empirical or finite-exhaustive as scoped.
- Added the Problem 1 pure/eventual-period sideways searches (`88769b1`, result
  `b7a4ff2`) and the Problem 3 bounded DFAO, 2-kernel, GF(2),
  Berlekamp--Massey, and Boolean-window searches (`953a2ae`, result
  `7fa76ec`). No failed finite search was promoted to a universal claim.
- Formalized stable Rule 30 Boolean and reconstruction lemmas in Lean without
  `sorry` (`9a17910`, `d69202f`, `adc51f9`, record `36413db`). Reviewed the
  exact width-two literature theorem and limited all-one-center-tail deduction.
- Completed the unified finite-scope CLI (`0cf0778`), strict record validators
  (`d26c668`, `a851dbe`), canonical-host direct CUDA gate (`808465e`), tracked
  reproduction commands (`9bb5e75`, `7562921`), and pinned WSL/toolchain setup
  (`eb5593e`, `ba886b9`).

## 2026-07-22

- Extended the Problem 1 finite baseline with nine true-prefix-then-zero
  traces and 14 explicit width-4 functional graphs (`79fc033`, record
  `e127883`). The graph family has 544 deterministic DOT edges but supplies no
  depth-independent state bound.
- Added the allowlisted production controlled runner (`32a71c4`) with bounded
  streaming, interruption/checkpoint handling, and conservative resource
  profiles. Two focused adversarial reviews led to bounded post-kill pipe
  draining (`bc160f5`) and stronger path, environment, JSON, resume, and
  before/after provenance checks (`8c4c1f8`).
- Ran the first controlled width-1-through-3 conservation search and recorded
  it in `9262394`. Repeated the same finite search on the fully hardened runner
  at source commit `6a93595`; the current reviewed record was committed in
  `1e43d4b`. It completed in about 0.064 seconds with exact output hashes and a
  stable clean worktree.
- Added the trusted five-backend same-output benchmark driver (`e95e7ff`). A
  focused adversarial review led to canonical-vector anchoring, exact semantic
  checks, rotated order, bounded detached-pipe handling, compiler/build-tree
  evidence, before/after provenance checks, and explicit limitations
  (`cefb261`).
- Fresh release C++/CUDA and Rust builds passed their native suites; all seven
  CTest cases passed with direct RTX 2060 access and all 22 Rust tests passed.
  The final `N=4,096`, five-repetition matrix was committed as `6a93595`.
  Every backend produced SHA-256
  `c31df0a2310247e6452237d4b780467e31b86340ce2a6dd90b679dd94c8012ff`.
- Updated the claim ledger, reproduction instructions, resource-control
  contract, benchmark protocol, and architecture (`7941c5e`). A clean external
  build then passed 224 Python tests, all seven release C++/CUDA CTests and
  direct GPU contracts, two sanitizer-enabled C++ tests, Rust format/clippy and
  22 tests, strict record validation, and Lean's three build jobs. The RTX 2060
  SUPER measured 40 C before and 41 C after; no hardware setting changed.
- Completed the five follow-up campaigns: checkpointed discrepancy through
  four million bits (`9d013b8`--`8c0ecb9`), bounded affine/2-kernel models
  (`4834532`), polynomial conservation identities (`831b349`), exact sideways
  invariants (`625d4c0`), and the extended CPU/CUDA periodic-trace campaign
  (`1a57514`). Six strict controlled-run records were committed in `85033aa`.
- Proved the finite sideways-prefix equivalence (`5b2fe0a`): the first
  reconstructed one is exactly the first trusted-prefix mismatch. This
  invalidates larger first-witness boxes as an independent research direction.
- Froze broad infrastructure, Problems 2/3 parameter sweeps, and generic
  benchmarking. The active critical path is now the whole-tail Problem 1
  conjecture documented in `docs/problem1_focus_program.md`.
- Added the complete reconstructed-tail campaign (`cf61640`). Its final strict
  run on clean commit `72376d4` exhausted 7,905 descriptions (`q<=4`, `p<=8`)
  through depth 2,048, found no interval-occupancy counterexample lead, and
  reproduced stdout SHA-256
  `899806101fe059e7d358041e21cf61c248f1d38897d4e678315c088e34119647`
  in 16.856332 seconds.
- Proved the exact whole-tail/finite-seed equivalence and right-edge recurrence
  (`72376d4`). Exhaustive checks against a direct cell array, sideways
  inversion, and every finite state through width 10 confirmed the indexing
  and fixed-coordinate power-of-two period bound. The result exposes the
  growing diagonal—not the fixed coordinates—as the unresolved obstruction.
- Ran the canonical clean quality gate on `a89246e`: 279 Python tests, nine
  release C++/CUDA CTests and every direct RTX 2060 contract, two sanitizer
  tests, Rust format/clippy and 22 tests, and the three-job Lean build all
  passed. Post-gate telemetry was 41 C at 12.64 W; no hardware control changed.
- Derived the exact 2-adic diagonal map: it is a unit-triangular isometric
  bijection, and eventually periodic traces are exactly its rational outputs.
  The exact `-1/3 <-> 1/3` right-edge two-cycle maps to the period-one traces
  `-1` and `1`, exposing finite spatial support as the hypothesis absent from
  fixed-coordinate period arguments.
- Audited the exact `p`-step center-period defect as a Boolean function of the
  complete radius-`p` cone. The new two-oracle analyzer found no loss of cone
  variables or linear-degree growth in its bounded range; this is a finite
  barrier to a narrow local-phase shortcut, not an orbit theorem.
- Strengthened the published-width-two deduction: an all-zero center tail
  makes the right neighbor monotone and eventually constant, while an all-one
  tail forces the left neighbor to zero. Thus eventual center period one is
  excluded for every nonzero finite seed. Lean kernel-checks the new local
  right-neighbor persistence lemma without axiom dependencies; the external
  width-two theorem remains outside Lean.
- Committed the 2-adic, period-defect, period-one, tests, and synchronized
  documentation as `8960181`. The full Python suite passed 292 tests and the
  Lean build passed all three jobs before the commit.
- Ran both new analyzers through the controlled runner on clean source commit
  `8960181`. The period-defect run covered 174,760 assignments in 1.279285
  seconds with stdout SHA-256
  `dd93af1f7b193672cc88a1b7e822155095b7ddb6aefdab00502a938eb95ef7c9`.
  The 2-adic run covered 8,190 quotient points in 0.460888 seconds with stdout
  SHA-256
  `7f1211fe815b8a82a56e5964428d24c8b063aeab935011e9051f2ea331a19f4c`.
  Independent immediate reruns reproduced both hashes exactly.
