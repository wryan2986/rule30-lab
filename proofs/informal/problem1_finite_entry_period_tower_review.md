# Independent adversarial review: finite-entry period tower

Reviewed source: `proofs/informal/problem1_finite_entry_period_tower.md`
SHA256 (computed locally before reading):
`839113840d7829cd89b792244c43e26193c88f1413ee33c23984d00b97f730e9`
(157 lines, read in full.) Own file only; source untouched; no runs, no
census, no enumeration. Method: find a fatal flaw; re-derive every table,
map, divisibility, and bound by hand.

## Verdict

ACCEPT as `partial-proof` modulo the dependencies in Sec. E. No fatal flaw
found. The rank-drop mechanism, the tower induction (including its
fencing-off of the constant all-ones step), the `A`-to-`T` posture, and all
edge heights `h = 0,1,2` check out. Two exposition nits (non-load-bearing)
in Sec. D. The diagonal incompatibility stays `inconclusive`, as declared.

## A. Inverse recurrence and return map (Sec. 1): ACCEPT

A1. Tables (1) verified all eight entries: state `s = v_i + 2v_{i+1}`;
`v_{i+2} = y_i XOR (v_{i+1} OR v_i)`; low output bit is the old high bit.
`f_0 = [0,2,3,3]`: `s=1 -> 0 XOR 1 = 1`, output `0+2`; `s=2 -> 1`, output
`1+2`; `s=3 -> 1`, output `1+2`. `f_1 = [2,0,1,1]`: `s=0 -> 1`, output 2;
`s=1 -> 0`, output 0; `s=2,3 -> 0`, outputs 1,1. All match.
A2. Cycle confinement: a bi-infinite orbit in a finite functional graph
is recurrent at every position (an infinite backward chain in a finite set
repeats, and the repeat is a cycle containing that position), so it never
uses a transient predecessor; the "intersection of iterated images"
phrase is standard. Period dividing `ell*p`, `ell <= 4`, follows. No
hidden prehistory choice remains. Verified.
A3. Rank drop: nonconstant `y` has least period `p >= 2` and a zero phase;
starting the return map there, `f_0` has image `{0,2,3}`, and the second
transition gives `{0,3}` (if `a_1 = 0`) or `{2,1}` (if `a_1 = 1`), both
size 2, using `f_0(2) = f_0(3)`, `f_1(2) = f_1(3)`; later maps cannot
grow the image. Recurrent set `<= 2` forces cycle length 1 or 2. Verified
for both `a_1` values, including `p = 2` words `(0,1)`/`(1,0)`.
A4. Least-period pin (2): `q | ell*p` from A2-A3; `p | q` because a
translation-commuting local map sends `q`-periodic rows to `q`-periodic
rows and `p` is least for `y`. Hence `q in {p, 2p}`. Uniqueness of the
preimage is correctly never assumed. Verified.
A5. Constants: `y = 0` gives cycles `{0}`, `{3}` only, hence exactly the
two constant preimages. `y = 1` gives the single 3-cycle `0->2->1->0`
with 3 transient (nothing maps to 3), i.e. exactly the rotations of `001`
(rechecked decoding: states `0,2,1` force cells `0,0,1`). Verified.

## B. Mortal-row tower (Sec. 2): ACCEPT

The induction is fenced correctly: `A^{e-1}v` is a nonzero preimage of 0,
hence all-ones (A5); `A^{e-2}v` is a bi-infinite preimage of the CONSTANT
row 1, hence a period-3 rotation (A5, transient state excluded by
bi-infiniteness) -- this step does NOT use (2), properly so. Every still
earlier row maps to a row of period `>= 3`, hence nonconstant, so (2)
applies and periods keep or double. Periodicity is derived at each step
from A2, never assumed of the initial row. Bound `k <= e-2`: one doubling
budget per backward step over `e-2` steps from the period-3 row. Height
edges: `e = 1` gives all-ones period 1; `e = 2` gives period 3. The spine
witness (period 6, height 6) satisfies `6 = 3*2^1`, `1 <= 4`. The
NECESSARY-only disclaimer is accurate. Verified.

## C. Finite-entry consequences (Sec. 3): ACCEPT

C1. Tail-to-`v` transfer: `v` periodic implies `A^h v` periodic; stencil
windows give agreement of `A^h x` and `A^h v` at all sufficiently high
positions, where `A^h x` vanishes; periodic plus tail-zero forces
`A^h v = 0`. (The last half-sentence is compressed in the source; the
mathematics is complete.) `v = 0` forces finite `x`. First extinction
`1 <= e <= h` feeds (3). Verified.
C2. Least eventual period equals least period of `v` (mutual divisibility
between tail periods and full-`v` periods on the overlap). Common period
`P_h = 3*2^{h-2}` (`h >= 2`): `1` and every `3*2^k`, `k <= h-2`, divide
it. `h = 0` (finite `x`) and `h = 1` (`e <= 1`) give period 1 only, so
`P_0 = P_1 = 1`. Verified.
C3. Denominator (6): period-`P_h` tail equals `-B/(2^{P_h}-1)` 2-adically;
preperiod shifts and integer parts touch only numerators and powers of two.
Integers have denominator 1. The no-exclusion-of-finite-seeds disclaimer
is honest. Verified.
C4. Anchored combination (`h = h_J(K)`) is a direct import application;
no list computed. Verified as scoped.

## D. Dyadic A clock (Sec. 4) and nit list: ACCEPT

Bit update `new_j = c XOR (d OR old_j)` with fixed higher neighbors per
phase: constant map if `d = 1`, else identity (`c = 0`) or flip (`c = 1`)
-- exactly the three stated cases. An `L`-fold composite on two points is
eventually fixed or 2-cyclic, so eventual period divides `L` or `2L`;
higher bits are unaffected by lower ones (stencil reads upward only), so
the downward induction yields a 2-power dividing `2^{B-1}`, with `z = 0`
at period 1. The necessary-only and non-finite-state-diagonal caveats are
accurate (scans keep consuming fresh input symbols). Verified.
Nits (exposition, not flaws): (i) C1's periodic-plus-tail-zero half
sentence could be one line longer; (ii) `e >= 1` in Sec. 3 is tacit via
`v != 0`.

## E. Acceptance, dependencies, audits

Accepted outright: A1-A5, B, C1-C4, D. Imports (not re-proved):
inverse-tail rationality/recursion; `A^h = pi^h T^h`; anchored theorem and
`h_J`. Audits requested: bi-infinite prehistory (A2, no hidden choices);
minimal-period divisibility (A4, both directions); `h = 0/1/2` (C2, all
covered); constants (`P_h`, denominator, `2^{B-1}` -- all rechecked);
`A`-entry to `T`-entry (identity import; this note claims no independent
`T`-entry time). No converse or growth step exists to audit; Sec. 5's
stopping fence is clean. No flaw found; nothing needs weakening.

## F. Novelty disposition (post-review source change)

After this review was written, the lead replaced the source's Section 4
duplicate derivation with an explicit import of the dyadic finite-`A`
cycle theorem from `problem1_frontier_head_dynamics.md`, Section 2, and
retitled the note 'Spatial periods of mortal tails' (current source SHA
`a56258a6a55f33ace44a66b4e53c8cbaba0e0b7a461678816216fd4ee4c6ebf3`;
original reviewed source retained at
`/tmp/astra-round6-tower-source-reviewed.md`). Disposition: my Section D
verification stands only as a consistency re-derivation, NOT as a novelty
claim -- the temporal clock is old, and no new temporal result is asserted
here by either party. Accepted novelty narrows to Sections 1-3 (spatial
mortal-period classification `1 or 3*2^k`, common period `P_h`,
denominator restriction). No old-cycle check was rerun. The older
dependency hash is left for the audit builder; this item is flagged for
inclusion in the pending final cross-file audit (`problem1_round6_final_review.md`).

## G. Corollary disposition: at most two preimages + mortal-row count (ACCEPT)

New Section 2 corollary (current source SHA
`4399e9738893cc654784fc26168406844da3021b7cb2a12a7aa4c3add1bee012`;
the `/tmp` archived original predates it): a fixed nonconstant periodic
output has `<= 2` bi-infinite preimages, giving `S_1 = 1`, `S_2 = 3`,
`S_e <= 2S_{e-1}` (`e >= 3`), `S_e <= 3*2^{e-2}`, and
`#{v : A^h v = 0} <= 3*2^{h-1}-1` (`h >= 1`). Adversarially verified:
(i) Backward-branching audit: transitions admit local branching
(`f_0(2) = f_0(3)`, `f_1(2) = f_1(3)`), but no transient predecessor
extends infinitely -- an infinite backward chain in the finite graph
repeats, hence lies in the recurrent set `R` (`|R| <= 2` at the zero
phase), and within `R` the backward walk is forced in all three cases
(single fixed point: all-constant; two fixed points: constant per
choice; 2-cycle: forced alternation per phase). Each recurrent state
determines exactly one bi-infinite row; total `<= 2`. (ii) Nonconstancy
is load-bearing and correctly stated: constant `y = 1` has THREE
preimages, so the bound genuinely needs the hypothesis. (iii) Exact-height
lemma: preimages of height-`e-1` rows land exactly at height `e` for
`e >= 3` (uses `A^{e-2}z != 0`), and preimage sets of distinct rows are
disjoint, so no counting leakage. (iv) Sum: zero row plus
`1 + sum_{e=2..h} 3*2^{e-2} = 3*2^{h-1}-1`; `h = 1` gives exactly two
(zero, all-ones). (v) Phases-as-distinct-rows convention is consistent
(`S_2 = 3` rotations). No period assumed, nothing enumerated. Corollary
accepted as `partial-proof`; no flaw found, nothing to weaken. If the
source moves again, this disposition pins the text as read above.
