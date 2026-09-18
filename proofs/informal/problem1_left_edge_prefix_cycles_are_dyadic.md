# Every finite moving-left-edge prefix has only dyadic eventual cycles

Status: `proved`. Structural stopping-fence result; not a proof of Problem 1.

## Statement

For a finite Rule-30 row with original left endpoint `L`, put

    b_j(t) = x_{L-t+j}(t),  j >= 0.

The exact autonomous prefix recurrence is

    b_j(t+1) = b_{j-2}(t) XOR (b_{j-1}(t) OR b_j(t)),

with negative indices zero and physical `b_0=1`.

For every finite width `n`, every eventual cycle of the `n`-bit prefix map on states with `b_0=1` has period a power of two.

This promotes one part of the run117 exhaustive observation (dyadic cycle lengths through width 19) to an all-width theorem. It does NOT prove the stronger observed claim that all states at a fixed width enter one cycle up to phase.

## Proof by triangular one-bit extension

Let `T_n` be the autonomous map on `(b_0,...,b_{n-1})`. Truncation intertwines `T_(n+1)` with `T_n`, so a cycle upstairs projects to a cycle downstairs. Assume inductively that a projected `T_n` cycle has period

    P = 2^m.

Along one traversal of that fixed base cycle, the new bit `z=b_n` obeys at each step

    z' = p XOR (q OR z),

where `p=b_(n-2)` and `q=b_(n-1)` are fixed by the current base state.

For fixed `(p,q)`, this is one of the four unary Boolean maps on one bit:

* if `q=0,p=0`: `z' = z` (identity);
* if `q=0,p=1`: `z' = 1 XOR z` (flip);
* if `q=1,p=0`: `z' = 1` (constant 1);
* if `q=1,p=1`: `z' = 0` (constant 0).

After the `P` steps of one base period, the return map on `z` is a composition of unary maps from `{id, flip, const0, const1}`. That set is closed under composition. Therefore the return map is again either constant, identity, or flip.

If it is constant, every recurrent lift over this base cycle has period exactly `P`. If it is identity, recurrent lifts again have period `P`. If it is flip, a recurrent lift closes after exactly `2P`. Hence every lifted cycle has period either `P` or `2P`, both powers of two.

The base width `n=1` has the single physical state `b_0=1`, of period 1. Induction proves the claim for every finite width.

## Consequence for the finite-support budget search

Run117 showed computationally that fixed moving-left-edge prefixes through width 19 fall onto small dyadic attractors. The theorem above removes the possibility that a larger fixed left-edge window eventually reveals an odd-period cycle: no finite width can do so.

This is weaker than the right-fringe permutation/pro-2 theorem because the left-prefix map is dissipative and can have transients. Nevertheless, after its transient, every bounded left-edge state is trapped in dyadic recurrence. Thus an odd-clock obstruction cannot be manufactured from a finite instantaneous left-edge prefix either.

A proposed finite-support birth budget based only on a bounded left-edge automaton therefore still needs a genuinely nonperiodic ingredient (growing depth, history/source identity, or coupling to the complete core/global shadow). The run117 source-indexed characteristic proposal remains viable only in such an unbounded-depth form.

## Relation to run117 computation

The exhaustive run117 data observed cycle lengths 1 for widths 1--3, 2 for widths 4--8, and 4 for widths 9--19. Those particular thresholds and the observed single-attractor-up-to-phase property remain computational observations only. The present argument proves exactly the all-width dyadic-period statement and nothing stronger.

Problem 1 remains OPEN.
