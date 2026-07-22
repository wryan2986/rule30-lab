# Research status

Last updated: 2026-07-22 UTC.

All three Rule 30 prize problems remain open in this repository. Status labels
below use the definitions in `docs/experiment_protocol.md`.

## Verified implementation facts

- The supplied source is preserved byte-for-byte as
  `src/python/rule30_research_reference.py`; its SHA-256 is
  `358bdc07904e77080eb78b67bdd8da25822d6b51f1a91b58b5313dfe461c1d01`.
- Complete rows through time 255 and the first 10,000 center bits were frozen
  only after agreement among the supplied implementation, an independently
  indexed Python cell array, C++ scalar and AVX2 engines, and independent Rust
  coordinate and packed engines. The 10,000-byte center-vector SHA-256 is
  `61de1c97dc3f80cb24d3a02207920bd442d6f530304497eee70189a039a47860`.
- The maintained C++20 engine uses packed `uint64_t` rows with explicit
  inter-word carries, scalar fallback, runtime-dispatched AVX2, streaming
  output, and checkpoint statistics. Boundary, partial-word, and sanitizer
  tests pass.
- The Rust implementation is independent, safe, packed, deterministic, and
  contains no unsafe code. Its native generator agrees with the shared vectors.
- CUDA direct evolution, batched period evaluation, and batched sideways
  reconstruction agree exactly with independent CPU oracles on the tested
  counts, partial grids, word boundaries, and forced chunk boundaries.
- The extended CPU/CUDA periodic-trace engine agrees exactly on 1,028,096
  distinct finite traces in the box `q<=8`, `p<=12`, `H=64`. CUDA was slower
  end to end for this workload, so this is a consistency result rather than an
  acceleration claim.
- The unified `rule30` CLI selects Python, C++ scalar/AVX2, Rust, and CUDA
  generation backends and exposes finite analysis, bounded-search,
  reproducibility, and controlled-experiment routes.
- The controlled experiment runner uses an immutable script allowlist, a clean
  source-tree precondition, repository-confined paths, child-process
  address-space and wall limits, exact streamed output caps, process-group
  termination, atomic checkpoints/records, and optional read-only GPU
  telemetry. Its limitations (including per-process rather than aggregate RAM
  control) are explicit in `docs/resource_controls.md`.
- A production runner invocation on commit `6a93595` completed the exact
  width-1-through-3 rational/GF(2) conservation search within a 120-second,
  512-MiB-address-space envelope. Before/after Git, source, script, and runner
  checks remained stable; its reviewed strict record is
  `results/runs/controlled-p2-conservation-final-w1-w3-20260722.record.json`.
- WSL sees the local RTX 2060 SUPER (8,192 MiB, compute capability 7.5) through
  the Windows driver. CUDA is compiled as native `sm_75` SASS; no Linux display
  driver or hardware-control setting was installed or changed.
- The final clean-build gate on 2026-07-22 passed 224 Python tests, all seven
  release C++/CUDA CTests plus direct GPU contracts, two sanitizer-enabled C++
  tests, Rust formatting/clippy and 22 tests, strict structured-record checks,
  and the three-job Lean build. GPU temperature was 40 C before and 41 C after.

## Reproduced empirical observations

- For `c_0` through `c_999999`, Python and C++ AVX2 independently produced the
  same 1,000,000-byte file with SHA-256
  `6fc1e4e2abfb382255b94955467f259be88c1044d09ec361c5039970985a1669`:
  500,768 ones, 499,232 zeros, and `D(1,000,000)=1,536`.
- The reported discrepancy checkpoints were reproduced exactly:
  `D(100)=4`, `D(1,000)=-38`, `D(10,000)=64`,
  `D(100,000)=196`, and `D(1,000,000)=1,536`.
- The reported binary linear complexities were reproduced:
  `L(1,000)=500`, `L(2,000)=1,000`, and `L(5,000)=2,500`.
- The reported 64-bit 2-kernel prefixes were all distinct at levels 1 through
  9. The same finite diagnostic was extended through level 13, where all
  8,192 sampled residue-class prefixes were still distinct.
- On the million-bit prefix, the greatest absolute prefix discrepancy was
  1,744, first reached at `N=964,778`; there were 500,571 runs and the longest
  run had length 22. A six-checkpoint log-log slope estimate was approximately
  0.5205. That fit is `heuristic`, not an asymptotic bound.
- The finite spectral, block, run, entropy, dyadic-discrepancy, and selected
  correlation measurements are descriptive only. They do not establish
  randomness, normality, mixing, or limiting balance.
- In the verified same-output matrix at `N=4,096`, all five Python coordinate,
  C++ scalar, C++ AVX2, Rust packed, and CUDA direct streams matched the trusted
  bytes before timing and in every warm-up/measured/profile run. Median
  startup-inclusive subprocess times over five rotated repetitions were
  3.195124 s, 0.005578 s, 0.004832 s, 0.004876 s, and 0.401417 s,
  respectively. This ordering is empirical for one modest workload; it is not
  a universal or asymptotic speed result.

## Finite exhaustive results

- At sideways horizon 500, all 2,046 binary descriptions of pure periods 1
  through 10 were checked. The only trace sequence reconstructing an all-zero
  finite left tail was the constant-zero trace (represented redundantly by ten
  words), and none of the survivors satisfied the seed condition `c_0=1`.
- For preperiods 0 through 3 and periods 1 through 5, all 930 descriptions were
  checked at horizon 500. The 20 zero-left survivors again described only the
  constant-zero trace; none satisfied `c_0=1`.
- For retained true-center prefix lengths
  `1,2,4,8,16,32,64,128,256` followed by a permanent-zero tail, exact
  sideways reconstruction through depth 500 found first nonzero initial-left
  depths `1,3,4,8,16,33,64,128,256`, respectively. This is nine finite
  candidate exclusions, not a statement about all prefix lengths.
- Fourteen fixed-width, zero-outer-boundary functional graphs covering every
  binary word description of lengths 1 through 3 at width 4 were explicitly
  exported as 544 deterministic DOT edges with checksums. These graphs do not
  provide a state bound independent of reconstruction depth.
- All 5,898 labeled complete DFAOs with one through three states under the
  recorded MSB-first binary-input convention were tested; none fit the 5,000
  training bits.
- All 4,096 canonical homogeneous GF(2) recurrences through order 12 were
  tested; none fit the 5,000 training bits. Autonomous Boolean suffix-window
  rules of widths 1 through 12 each have an explicit repeated-context conflict.
- A depth-5 finite 2-kernel fingerprint quotient had 63 sampled classes but
  failed closure at depth 6. This excludes only that finite quotient
  construction.
- All 131,200 affine GF(2) binary-digit matrix models of dimensions one and
  two were tested on the stated 64-bit training prefix; none fit. A short
  eight-bit control admitted 192 fits, all refuted at the first held-out bit.
  A 31-node multiscale finite 2-kernel refinement remained fully distinct at
  128 observations but was not closed under child transitions.
- Exact linear systems over both the rationals and GF(2) found no nontrivial
  member of the tested additive local conservation-law ansatz at widths 1
  through 5. A Rule 204 positive control verified the search machinery.
- Sixteen wider bounded-degree polynomial density/flux systems—one-step
  degrees two and three and two-step degree two—had zero excess after the full
  representable coboundary quotient. All six matching Rule 204 controls had
  excess nullity two.
- The exact sideways image of adjacent temporal columns is the shift of finite
  type forbidding `(2,0)`, `(2,1)`, `(3,2)`, and `(3,3)`. This is
  depth-independent structure, but it does not distinguish an all-zero
  reconstructed time-zero tail.
- The first complete-tail campaign exhausted all 7,905 eventual-period
  descriptions with `q<=4`, `p<=8`, `c_0=1` through reconstruction depth
  2,048, representing 3,776 distinct finite trace classes. Every class had a
  reconstructed one in each adjacent interval from `(64,128]` through
  `(1024,2048]`; the largest internal zero run observed was 22. The exact
  scientific certificate is
  `e957c1c5b919eb115c1f354122b0b1fffb614e665062ee52edb8e30109657c27`.

Every item in this section is exhaustive only for its stated finite set. None
is an infinite nonperiodicity, nonautomaticity, recurrence, balance, or
complexity result.

## Partial mathematical results

- `partial-proof`: the center sequence cannot be eventually constant one. If
  `c_t=c_(t+1)=1`, the Rule 30 identity forces the adjacent-left bit at time
  `t` to be zero. An all-one center tail would therefore make the adjacent
  width-two trace eventually constant, contradicting Kopra's Corollary 3.7
  (equivalently the applicable Jen result). The theorem hypotheses and exact
  deduction are checked in `docs/theory_literature_review.md`.
- Lean 4, without `sorry`, user axioms, or reported axiom dependencies, proves
  the Rule 30 Boolean form, left-permutive inversion, correctness of one
  sideways step, bounded column/pair/triangle reconstruction, and the local
  and infinite-tail implication that consecutive true center values force the
  adjacent-left values false. The external width-two theorem is not formalized.
- `partial-proof` (complete informal finite argument, with its local
  injectivity premise checked in Lean): the first nonzero reconstructed-left
  depth is exactly the
  first center-prefix disagreement from the zero-left reference evolution.
  Exhaustive checks covered all 262,142 traces through horizons zero to 16.
  This shows that larger finite first-witness searches are prefix comparisons,
  not independent evidence for nonperiodicity.
- `partial-proof` (complete informal argument, independently checked on finite
  instances): an eventually-zero reconstructed left tail is equivalent to a
  finite-support initial configuration whose rightmost one is at coordinate
  zero. Encoding that configuration by an odd integer `S`, its moving-frame
  evolution is `T(S)=S XOR ((S<<1) OR (S<<2))`, and its fixed spatial center is
  the growing diagonal `bit_t(T^t(S))`. Every fixed bit `k` is periodic with
  period dividing `2^k`, but this does not control the growing diagonal. The
  proof is in `proofs/informal/problem1_whole_tail_equivalence.md`.

These results do not exclude an all-zero tail, any period greater than one, or
eventual periodicity in general.

## Active conjectures

- Any eventually periodic center trace compatible with the single-cell right
  half reconstructs an initial left half that is not eventually zero.
- The center sequence is not eventually periodic.
- Its limiting one-frequency exists and equals one half.
- There may be a sublinear exact representation of `c_n`, but no model is
  favored; the three published Problem 3 formulations remain separate.

## Failed approaches

- Direct evolution of one history on CUDA was substantially slower than the
  packed CPU at 32,768 bits because 32,767 dependent kernel launches dominate.
- The bounded rational/GF(2) local-observable ansatz at widths 1 through 5
  produced only the identified trivial/coboundary space.
- The bounded DFAO, homogeneous GF(2), Boolean-window, and finite 2-kernel
  searches above found no exact finite-prefix model in their stated classes.
- A Berlekamp--Massey recurrence trained on 5,000 bits had order 2,500 and
  first failed held-out validation at `n=5,003`.
- Small fixed-width sideways state graphs did not justify a state bound
  independent of reconstruction depth, so they cannot yet be promoted to a
  finite-state proof.
- Extending first-nonzero sideways searches cannot advance the proof by itself:
  the first witness is exactly the first trusted-prefix mismatch.
- The complete-tail campaign produced no counterexample lead, but its maximum
  internal zero run increased from 19 to 22 and the extremal description
  changed. The data do not support a uniform bounded-gap claim, so merely
  increasing the reconstruction horizon is not an admitted continuation.
- NVIDIA Compute Sanitizer could not initialize its WDDM debugger interface in
  this WSL configuration. CUDA correctness tests still pass, but this is not a
  successful memcheck result.

## Open questions

- Can eventual periodicity of the growing diagonal `bit_t(T^t(S))` be made
  incompatible with the power-of-two periods of every fixed moving-frame bit?
- Can sideways reconstruction under an eventually periodic boundary be
  summarized by a rigorously depth-independent invariant or finite state?
- Can the width-two nonperiodicity theorem be combined with a new local lemma
  to exclude center periods other than the all-one tail?
- Does a wider or nonlinear spacetime observable yield a telescoping identity
  controlling center discrepancy?
- Which exact Problem 3 formulation would the prize committee accept, and in
  which machine model and input convention?
- Are there exact morphic, algebraic, circuit, transducer, or compressed
  spacetime representations outside the bounded classes already tested?

## Potential next experiments

Research is now focused on Problem 1; Problems 2 and 3 are regression-only.
Admission and stopping criteria are in `docs/problem1_focus_program.md`.

1. Derive exact phase constraints imposed by a hypothetical period on the
   growing diagonal of the right-edge recurrence.
2. Combine those constraints with fixed-coordinate power-of-two periodicity
   and Rowland's local-nestedness theorem.
3. Identify a contradiction or a precise barrier before authorizing another
   finite parameter increase.
4. Encode simultaneous eventual temporal periodicity and eventual spatial
   zero as a symbolic/SAT problem only if a depth-independent state bound is
   first proved.
5. Formalize only the smallest stable diagonal lemma that emerges.
