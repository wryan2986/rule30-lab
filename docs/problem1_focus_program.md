# Problem 1 focused research program

Status date: 2026-07-22

All three prize problems remain open. This document freezes broad platform
expansion and makes one Problem 1 implication the repository's critical path.

## Target

Let `C=(c_t)` be a proposed center trace with `c_0=1`. Force the initial right
half-line to zero and use Rule 30 left-permutivity to reconstruct the initial
left half `L(C)=(x_{-d}(0))_{d>=1}`.

The focused conjecture is:

> If `C` is eventually periodic, then `L(C)` is not eventually zero.

The true single-cell evolution has an identically zero initial left half, so a
proof would exclude an eventually periodic true center and solve Problem 1.
A counterexample would refute this proof route, though not necessarily Rule 30
center nonperiodicity.

## What the existing finite search does not establish

The finite prefix-equivalence theorem proves that the first reconstructed one
occurs exactly at the first mismatch from the appropriate zero-left reference
trace. Therefore searching larger preperiod/period boxes for a *first* one is
only an expensive prefix comparison. It cannot distinguish a reconstructed
tail with one exceptional bit from a tail with infinitely many ones.

The four-forbidden-block image subshift is depth-independent, but its
time-zero constraint is vacuous on an all-zero adjacent left pair. The exact
cyclic-pair theorem assumes both the center and right-neighbor columns are
cyclic; eventual center periodicity alone does not justify that assumption.

## Admitted work

A proposed task is on the critical path only if both possible outcomes inform
the whole-tail conjecture. Current admitted directions are:

1. Search for eventually periodic traces whose reconstructed left prefixes
   have a long terminal zero run after their last one. Such candidates are
   counterexample leads; absence is finite evidence only.
2. Derive exact recurrence, diagonal, or front constraints on the complete
   reconstructed tail under an eventually periodic temporal boundary.
3. Formulate the simultaneous conditions “temporal tail periodic” and
   “initial spatial tail zero” as a symbolic-dynamics, SAT, de Bruijn, or
   transducer problem, proving any claimed state bound before using a finite
   graph as an infinite argument.
4. Search for monotone quantities or forbidden cycles that survive the
   transient seam and distinguish an eventually-zero spatial tail.
5. Formalize only stable local or finite-tail lemmas needed by a candidate
   proof, then connect them to the existing width-two literature result when
   the hypotheses genuinely match.

## Frozen work

Until a new theorem or algorithm changes the situation, do not spend research
time on:

- larger center-prefix statistics or discrepancy checkpoints;
- larger first-witness period/preperiod boxes;
- generic automaton, recurrence, or 2-kernel sweeps for Problem 3;
- wider polynomial-conservation sweeps for Problem 2;
- CUDA optimization of one sequential Rule 30 history;
- ports of established experiments to additional backends;
- repeated benchmarks without a changed algorithm;
- fixed-width graphs offered without a depth-independent state theorem;
- CLI, runner, dashboard, or documentation features beyond maintenance; or
- broad Lean formalization of implementation details.

Problems 2 and 3 retain their verified code, vectors, and records. Their tests
remain regression gates, but their research campaigns are paused.

## Decision gates

Each new experiment must state in advance:

- the exact quantified finite or infinite claim;
- what would count as a counterexample lead;
- what finite absence can and cannot establish;
- how the result changes the next proof step; and
- a resource cap and stopping condition.

After each campaign, continue only if it produces a new invariant, a stable
recurrence, an exact certificate, a counterexample candidate, or a sharper
mathematical obstruction. Merely increasing a bound is not continuation.

## Immediate sequence

1. Measure terminal-zero behavior of reconstructed left prefixes, with exact
   cross-horizon consistency and candidate retention rather than first-witness
   counts.
2. Inspect the surviving long-zero-tail candidates symbolically and attempt to
   extend or refute them exactly.
3. Extract a seam-aware recurrence or finite certificate from those cases.
4. State and prove the smallest stable lemma, informally first and then in
   Lean when useful.
5. Reassess the focused conjecture before authorizing another finite search.
