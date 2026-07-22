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
