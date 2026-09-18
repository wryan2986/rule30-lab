# Problem 1: finite-horizon fixed-fringe uniqueness does not exclude the last survivor

## Status

No-go lemma / stopping fence. Problem 1 remains open.

## Context

The authoritative round309 handoff describes a recovered draft `problem1_fixed_fringe_phase_collapse.md` (not present in the current pushed branch) with the following claimed finite-horizon conclusion: for the SAME finite fringe and initial core width at most L, at most one core in the admissible domain can pass H = ceil(L/2)-1 complete paired transitions. The handoff explicitly says exclusion of that one continuing candidate still needs new mathematics.

Recent automation runs independently reached a compatible stopping fence: the normalized scalar residence ledger can realize every integer path with downward steps at most one, so further scalar telescoping cannot supply the missing survivor-specific obstruction.

This note isolates why iterating finite-horizon uniqueness, by itself, cannot remove the final candidate.

## Lemma: nested uniqueness is compatible with one infinite survivor

Let S be any set of candidate initial states. For each horizon h >= 0 let S_h be the candidates satisfying all required FULL/fringe constraints through horizon h. Assume only:

1. S_(h+1) is a subset of S_h (longer validity implies shorter validity), and
2. for all sufficiently large h, |S_h| <= 1.

Then these assumptions do not imply that some S_h is empty.

Indeed, choose any s in S and define S_h = {s} for every h. All nesting and uniqueness statements hold, while s satisfies every finite horizon. More generally, if every S_h is nonempty and eventually has size at most one, nesting forces the same unique element to occur in every sufficiently late S_h; that element is precisely an infinite compatible survivor.

Therefore a proof that merely reapplies a finite-horizon phase-collapse/uniqueness theorem at larger and larger horizons cannot yield a contradiction. Once the candidate set has collapsed to one element, additional applications of the same type can simply keep returning that element.

## Restart does not fix this

Run 100 established that the normalized-excess germ Q is invariant under finite physical restart. Restart freedom is useful for discarding transients, but it does not convert uniqueness into emptiness. At each restart one may again obtain a singleton set of locally compatible core/fringe states; those singletons can be the successive states of one actual infinite orbit.

Thus a pigeonhole argument of the form

    finite candidates -> at most one candidate after H -> restart -> at most one candidate -> ...

contains no contradiction unless an additional quantity is shown to change monotonically, be consumed, or become incompatible with the unique continuation.

## What would be sufficient

The missing strengthening must prove at least one genuinely exclusionary statement, for example:

- **eventual emptiness:** for some survivor-specific horizon, no candidate with the fixed COMPLETE actual fringe can continue;
- **strict resource consumption:** every H-block consumes an element of a finite resource tied to the original fringe, and the resource cannot regenerate under restart;
- **incompatible unique continuations:** the unique core allowed by one externally anchored FULL/fringe phase is inconsistent with the unique core forced by another independently anchored phase;
- **forced scalar escape:** the unique continuation necessarily creates a new maximum of the intrinsic normalized-excess germ Q.

Crucially, the extra condition must be anchored independently of choosing the surviving candidate. Otherwise it is only another reformulation of nested singleton compatibility.

## Consequence

Finite-horizon injectivity/phase collapse can reduce multiplicity, but multiplicity zero and multiplicity one are qualitatively different. The unresolved Problem-1 bridge is exactly the step from uniqueness of a possible continuation to impossibility of that continuation.

This is a stopping fence against spending further runs trying to iterate finite-prefix uniqueness alone. A useful next theorem must attach a nonrenewable original-fringe resource or an independently anchored incompatibility to the last candidate.
