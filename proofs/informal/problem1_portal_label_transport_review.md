# Problem 1: portal layer and hidden-label transport review

Date: 2026-10-02. Problem 1 remains **OPEN**.

## 1. Dispositions and exact scope

| Statement | Disposition | Scope |
|---|---|---|
| Four-matrix one-layer return formula | LEMMA WITH PROOF — INDEPENDENTLY CHECKED | Every odd driver period p>=1, arbitrary p-periodic upper pair histories |
| Nonzero-parent unique cyclic extension and synchronization | LEMMA WITH PROOF — INDEPENDENTLY CHECKED | One added layer, at most two aligned p-step returns; not a whole-stack transient bound |
| Zero-parent fixed-point alternatives | LEMMA WITH PROOF — INDEPENDENTLY CHECKED | No extension if b_Y=1; two if b_Y=0, with the explicit higher-track parity formula |
| H_ext and H_Y at r=1,2,3 | LEMMA WITH PROOF — INDEPENDENTLY CHECKED | Every even p>=2 and odd driver; full aligned odd-label fibers |
| H_Y implies H_ext and exact rank loss | LEMMA WITH PROOF — INDEPENDENTLY CHECKED | Every r>=1, conditional on invariant newest Y history and nonzero parent |
| General H_ext and H_Y | FINITE EVIDENCE ONLY | p=2,4,6,8,10,12,14 and r=1..6 |
| Endpoint parity affine on an upper fiber | FINITE EVIDENCE ONLY | p=8, r=1, using the previously recorded endpoint classifier |

Proofs are in `problem1_portal_layer_monodromy.md` and
`problem1_shallow_blind_label_affinity.md`. The conditional all-depth
lemma does not prove its hypothesis H_Y. None of these statements gives
an original-support budget across period changes.

## 2. Independent logical review

The parent derived the transfer formula from two raw scalar Rule-30
recurrences, including the half swap at odd driver parity. A separately
pinned `gpt-6-luna` reviewer checked the coordinate change, the four
matrices, nilpotence, unique fixed point, and both zero-parent cases.
The parent then rechecked the forcing formula from the two raw XOR sums.
The parity obstruction belongs to the higher track, not the zero parent.

A fresh scoped Luna review accepted Sections 3–6 of the shallow proof
for even p>=2 and odd weight. It checked the five-state decoding, the
nonzero-track existence arguments, cyclic latest-reset reasoning, and
the exact fiber dimension used in rank-nullity. A separate response
accepted Section 7's conditional reduction: a phase with M=1 anchors X
independently of the labels; if M is everywhere zero, nonzero parent
supplies L=1 and an affine reset. Propagation with fixed Y then proves
affineness. The reviewer explicitly did not accept a general-depth H_Y
theorem or an endpoint-parity theorem.

These model reviews are adversarial checks of the written arguments,
not proof authorities. The parent performed the final mathematical
review. All delegation used explicitly pinned Luna or Space Bunny.
No Astra model, fallback, escalation, or final check was used.

## 3. Reproducible finite monodromy checks

Reproduce:

    python3 experiments/problem1_nonperiodicity/check_portal_layer_monodromy.py

Record: `results/problem1/20261002_portal_layer_monodromy.json`.

The checker compares explicit GF(2) matrix composition with independently
updated raw half bits and all four pair seeds. Exact counts:

* 25,104 matrix compositions and 100,416 seed returns;
* 987,808 raw scalar updates;
* all odd drivers and all higher/parent pair arrays for p=1,2,3;
* all odd drivers and all parent arrays for p=4, with the four constant
  higher-pair histories;
* 24,780 nonzero-parent cases, 324 zero-parent cases;
* among zero parents, 146 have no cyclic extension and 178 have two;
* 256 local coordinate-change controls, plus the actual named even-driver
  p=1 counterexample to dropping the oddness hypothesis.

The parent inspected and independently reran the completed checker.
The theorem is proved symbolically; these finite checks test its formulas
and implementation rather than justify an extrapolation.

## 4. Reproducible finite label-fiber checks

Reproduce:

    python3 experiments/problem1_nonperiodicity/check_blind_fiber_endpoint_affinity.py

Record: `results/problem1/20261002_blind_fiber_endpoint_affinity.json`.

The 42 declared extension scopes enumerate every odd p-bit word for
p=2,4,6,8,10,12,14 and r=1..6. Together they contain 65,532 driver/scope
instances and 42,196 full eligible upper fibers. Every tested fiber
equals its complete parity-constrained blind-label cube; there are no
earlier-zero, zero-parent, or incomplete-fiber exclusions in this run.
The test predicts every member's full aligned extension from an anchor
and an explicit GF(2) basis. No non-affine extension or nonconstant
newest Y history occurs in these declared scopes. The largest tested
affine domain has dimension six. This is **FINITE EVIDENCE ONLY** beyond
the proved r<=3 scope.

At r=4,5,6 the largest tested domain has dimension only one. Every map
on an affine singleton or line is affine automatically, so those scopes
do not test a nontrivial higher-depth affine square. Their H_Y checks
are still informative: equal Y on the two endpoints is an additional
restriction. A genuine higher-depth H_ext falsification test needs a
fiber of dimension at least two.

Separate controls build scalar cyclic children by trying both seeds and
check the original two-row temporal update. For all 128 odd p=8 words
at depths 1..7, there are 896 scalar child solves, 7,168 full phase-state
comparisons and 7,168 temporal updates, with no early zero. Algebra
controls cover a parity-cube anchor whose pivot bit is zero and an
explicit nonlinear function on a two-dimensional cube.

The p=8, r=1 endpoint check groups all 128 words into 46 aligned fibers,
with sizes 1:8, 2:20, 4:16, 8:2. The historical degree-seven classifier
gives 56 odd and 72 even endpoints; no affine-fiber violation is found.
These endpoints were not recomputed by long first-return traversals in
this run. This scope supplies no evidence at p=16 or at other observer
depths for endpoint affineness.

Both atomic records include exact parameters, source/input hashes, base
commit, hardware/software, timings and resource caps. Streaming hashes
identify compact per-scope cube ledgers; regenerating the deterministic
enumeration reproduces them. Execution metadata can differ between runs.

## 5. Rejected claims and implementation corrections

The free critic initially proposed three objections that the parent
rejected and the critic withdrew:

1. A zero-dimensional odd fiber need not be empty. With no blind phases,
   forced labels of odd parity give a singleton.
2. A shorter-period unlabeled state orbit does not force the driver to
   share that period. Blind phases can carry different labels at repeated
   states. Even a p=4 state presentation can have two different odd
   labelings with the same repeated state orbit.
3. Endpoint parity is defined for every odd driver: integrating ww gives
   a nonzero antiperiodic x, and the canonical boundary (x,0) has a finite
   return by the existing boundary-return theorem. Finite-core ancestry
   is not a necessary definition hypothesis.

The critic's further statement that the entire extension is bilinear in
driver and seed was not accepted. A single update is separately affine,
but composition can have higher driver degree. No unproved additional
"blind-flat" hypothesis is promoted into the theorem.

Draft checker mistakes were corrected before accepting their records.
For monodromy, these included confusing a raw second-half bit with Y,
using a whole driver word instead of its current phase bit, and comparing
one return with a two-return fixed point. For the fiber checker, the
original anchor-dependent basis rule could produce a zero basis vector.
The correct rule always pivots at the first sorted blind phase and uses
e_s+e_pivot for every other phase. Rank and coordinate reconstruction are
now checked on every cube. Independent controls caught the distinction
between temporal same-depth updates and growing the observer stack.
The unused witness paths were also audited for the fourth square vertex
and the canonical endpoint boundary. These are implementation failures,
not counterexamples to mathematical hypotheses.

The corrected finite computations survive. Failed objections and draft
bugs are retained here so later work does not mistake them for unresolved
bridges or reuse the rejected implementation.

## 6. Research consequence

The smallest unproved extension depth for this transport strategy is
r=4. H_Y is a sufficient all-depth target, now expressible as a two-driver
counterexample search: equal complete aligned upper orbits but different
new Y histories. Proving it would give an exact linear layer transport
law with rank u_r-u_(r+1). It would still leave the separate task of
transport through a zero return/period doubling and bounded reuse against
the same original finite support. Problem 1 remains open.
