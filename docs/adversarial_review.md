# Final adversarial review

Review date: 2026-07-22 UTC  
Reviewed commit: `7941c5e4` (descendant of required baseline `6a93595`)  
Disposition after closeout: **ready for the initial reproducible handoff with
the accepted limitations below; no prize problem is solved**

## Scope and method

This review challenged the tracked source, tests, documentation, and all 20
structured JSON records. It inspected mathematical quantifiers and status
labels, trusted-vector provenance, cross-backend output contracts, benchmark
comparability and provenance, controlled-runner confinement, Problem 3 model
selection and held-out use, deterministic execution claims, and the canonical
quality-gate script. It did not modify code or results.

Read-only or temporary-build probes established the following:

- all 20 result records satisfy the strict schema, have unique experiment IDs,
  and name commits present in the local Git object database;
- graph checksum manifests and the 4,096-byte benchmark output hash are
  internally consistent with the trusted vector;
- Python: 224 tests passed;
- the reviewer's isolated first C++ pass completed CPU tests but could not open
  the WSL GPU, so four CUDA cases skipped;
- a subsequent canonical-host gate with direct device access passed all seven
  release C++/CUDA CTests and each GPU executable directly;
- C++ ASan/UBSan build in `/tmp`: two tests passed;
- Rust: 22 tests passed, including both engines and shared vectors;
- Lean 4.30.0 accepted `proofs/lean/Rule30.lean` directly;
- the repository has no configured Git remote; and
- retained C++, CUDA, and Rust benchmark executables still match their recorded
  SHA-256 values.

## Verified controls

### Correctness and backend agreement

The trusted 10,000-byte vector is anchored by hand/local-rule checks, an
independently indexed Python implementation, the preserved supplied program,
and compiled C++ and Rust implementations. Boundary, partial-word, streaming,
and CLI tests are substantive rather than checksum-only. The final benchmark
compares complete numeric-byte streams from Python coordinate, C++ scalar,
C++ AVX2, Rust packed, and CUDA direct evolution against the trusted vector
before timing and rechecks every warm-up, measured run, and RSS run. For its
stated `N=4096`, all streams have SHA-256
`c31df0a2310247e6452237d4b780467e31b86340ce2a6dd90b679dd94c8012ff`.

The reviewer's isolated worker could not repeat GPU execution because that
worker lacked device access. This was an execution-context artifact rather
than host unavailability: the lead process then ran the clean consolidated
gate on the reviewed commit with direct RTX 2060 access. All seven release
C++/CUDA CTests and the device probe, batch-period, direct-evolution,
batch-sideways, and generation-CLI GPU contracts passed. The committed CUDA
records additionally contain CPU-oracle comparisons for uneven grids, word
boundaries, and chunk boundaries. This is finite implementation evidence, not
universal correctness.

### Benchmark semantics and nondeterminism

The five-backend matrix performs materially identical generation output work
and describes its timing honestly: subprocess startup, runtime initialization,
computation, and stdout writes are included; parent validation is excluded.
Five measured rotations let each backend start one round. Every sample, median,
minimum, maximum, mean, population standard deviation, output size/hash,
host-RSS profile, compiler version, relevant build metadata, and pre/post
thermal snapshot is recorded. CPU frequency is observed rather than pinned,
and GPU timings include CUDA initialization; therefore the numbers are
workload-specific empirical measurements, not asymptotic claims.

Analysis and predictor workloads use fixed argument maps and byte-identical
JSON checks across verification, warm-up, timing, and RSS executions.
`PYTHONHASHSEED=0` and one-thread cooperative-library settings reduce avoidable
nondeterminism. CUDA benchmark test data use fixed seeds. Scheduler, frequency,
thermal, WSL, and driver variation remains and is correctly disclosed.

### Problem 3 leakage control

The main bounded-search record uses `[0,5000)` for training and
`[5000,10000)` for held-out validation. The benchmark workload independently
uses `[0,2500)` and `[2500,5000)`. DFAO and recurrence candidates are screened
and fixed from training bits before held-out inspection; Berlekamp--Massey is
fit only to training data; Boolean-rule completions are fixed before rollout.
Tests perturb held-out data and verify candidate selection is unchanged. No
random seed affects selection. Earlier observed held-out bits may be used as
history only where the record explicitly calls validation teacher-forced; that
procedure is not presented as an autonomous shortcut.

### Controlled runner

The current runner uses a fixed repository-relative script allowlist, rejects
script and run-root symlink escapes, confines declared read paths, forbids
generic side outputs, rejects abbreviated path-bearing options, launches with
`shell=False`, isolated Python, `/dev/null` stdin, and a small environment, and
checks HEAD/worktree plus runner/child hashes before and after execution.
Output caps are exact and concurrently drained. Wall limits, process-group
termination, bounded post-kill pipe draining, atomic per-file publication,
disk reserve checks, validated restart-only resume, and fail-closed optional
GPU telemetry are covered by tests. The tracked final controlled record was
made with this hardened runner at commit `6a93595` and records stable pre/post
provenance.

## Findings by severity and status

### High — resolved during closeout

1. **The isolated reviewer could not access the WSL GPU.** In that restricted
   worker context, `/usr/lib/wsl/lib/nvidia-smi` returned `GPU access blocked by
   the operating system` and CTest skipped four cases. The canonical host
   process immediately reran `scripts/run_quality_gates.sh` from a clean tree
   with explicit GPU access: all seven CTests and all five direct CUDA commands
   passed. Read-only telemetry showed 40 C before and 41 C after. Therefore the
   repository gate is satisfied; the isolated skip remains useful evidence
   that skip-aware instructions are necessary.

2. **The original standalone documented `RULE30_REQUIRE_CUDA=1 ctest` command
   did not actually require CUDA.** No test reads that variable, and CTest can
   exit zero after return-code-77 skips. Closeout removed that ineffective
   claim from `README.md` and `docs/setup_wsl_cuda.md`, documented the skip
   semantics, and added the same direct probe and four direct GPU contract
   invocations used by the consolidated quality gate.

### Medium — accepted limitation

1. **Native binary provenance is evidence, not attestation.** The benchmark
   records a clean source commit, tree IDs, build directories, retained flags,
   compiler versions, and executable hashes before and after timing. These do
   not cryptographically prove that each binary was produced from exactly that
   commit. Rebuilding from the recorded command and reproducing outputs remains
   necessary.

2. **Runner memory control is per process.** `RLIMIT_AS` is inherited but is not
   an aggregate process-tree RSS/cgroup limit. Cooperative thread variables are
   not a kernel CPU quota. The fixed trusted allowlist materially reduces the
   risk, and documentation states the limitation accurately.

3. **The runner is not a hostile-code or network sandbox.** A child can access
   the local network, and a deliberately hostile descendant could escape its
   process group. Bounded pipe draining prevents the parent from hanging but
   does not prove every escaped process is gone. This is acceptable only while
   the fixed allowlisted scripts remain audited and trusted.

4. **CUDA memcheck is unresolved.** NVIDIA Compute Sanitizer could not
   initialize its WDDM debugger interface. CPU sanitizers pass and finite
   CPU/GPU oracle comparisons are extensive, but they are not a substitute for
   successful CUDA memory checking.

### Low — resolved or accepted

1. The controlled record's `provenance_policy` says the “complete tracked and
   untracked” worktree was clean, whereas `git status` intentionally excludes
   ignored transient/toolchain paths. The historical record remains immutable,
   but closeout changed future runner wording and the resource/benchmark
   documentation to “tracked and non-ignored untracked.”

2. Static record tests validate schema, unique IDs, and commit existence, but
   do not recompute every record-specific cross-field invariant. The benchmark
   driver and its tests enforce those invariants when producing the record;
   adding a committed-record semantic verifier would improve later tamper and
   transcription detection.

## Finite-versus-infinite and quantifier audit

- **Problem 1:** the period/preperiod searches, prefix-then-zero exclusions,
  and fixed-width graphs quantify only over their stated finite descriptions,
  horizons, and widths. They do not supply a depth-independent finite-state
  bound. The only infinite deduction is the narrow theorem that the center
  cannot be eventually all one, conditional on the checked published
  width-two theorem. It excludes neither an all-zero tail nor any period above
  one.
- **Problem 2:** million-bit counts, discrepancies, correlations, spectral
  statistics, entropy estimates, and a fitted scaling exponent are finite or
  heuristic. They do not prove `D(N)=o(N)`, existence of a limit, balance,
  randomness, normality, or mixing. The conservation search is exhaustive only
  for its explicitly bounded rational/GF(2) ansatz.
- **Problem 3:** the repository correctly separates “no exact `o(n)`
  algorithm,” an `Omega(n)` lower bound, and the literal published “no exact
  `O(n)` algorithm” predicate. Bounded DFAO, recurrence, Boolean-window, and
  2-kernel failures exclude only the enumerated finite classes and prefixes.
  They imply neither nonautomaticity nor any universal time lower bound.
- **Formal claims:** the `rigorous-proof` record applies only to the exact local,
  bounded-reconstruction, and tail-implication statements accepted by Lean.
  The external width-two theorem and the final contradiction are not
  formalized there. The status is not a prize-solution claim.

## Conclusion

**No Rule 30 prize problem is solved by this repository.** The computational
evidence is carefully scoped, the partial all-one-tail theorem is genuinely
limited, and the Problem 3 ambiguity is handled correctly. No mathematical
claim inflation or held-out leakage was found.

The repository is technically ready for its initial local handoff. The clean
consolidated quality gate passed after the isolated review, and the misleading
standalone CTest instruction was corrected. CTest success with skipped CUDA
tests remains insufficient; the documented direct GPU contracts are the
canonical device gate. Accepted limitations above—including unattested native
build provenance, per-process memory limits, lack of a hostile-code sandbox,
and unavailable CUDA memcheck—remain explicit.
