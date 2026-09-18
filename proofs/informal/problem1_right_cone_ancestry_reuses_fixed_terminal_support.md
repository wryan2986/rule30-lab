# Right-cone ancestry reuses a fixed terminal part of the original support

Status: `partial-proof` / stopping fence. Problem 1 remains OPEN.

## Setup

Let the original finite Rule-30 row have right support endpoint `R`, so every initial cell at coordinate `x>R` is zero. Rule 30 has radius one. Consider any later spacetime cell at physical time `t` and bounded offset `j>=0` behind the maximal right-moving light-cone coordinate,

    (x,t) = (R+t-j,t).

This note asks whether repeated late fringe/birth events in a bounded-width strip near that right cone can be injectively charged merely to *different original support cells*.

## Exact backward-cone calculation

For a radius-one cellular automaton, the time-zero backward light cone of `(x,t)` is the interval

    [x-t, x+t].

Substituting `x=R+t-j` gives

    [R-j, R+2t-j].

Intersecting this with the original support half-line `(-infinity,R]` leaves exactly

    [R-j,R]

(up to irrelevant coordinates left of the actual left support endpoint).

Therefore:

> **Terminal-ancestry lemma.** For every fixed offset `j`, every cell on the ray `x=R+t-j`, at every time `t`, can depend on original nonzero data only through the same terminal block of at most `j+1` original cells `R-j,...,R`.

More generally, an event whose entire observed neighborhood stays within width `W` behind the maximal right cone has original-support ancestry contained in the fixed terminal block

    R-W,...,R,

independently of how late the event occurs.

This is purely causal and does not claim that every cell in the block has essential influence on every event.

## Consequence for the missing birth budget

The previous stopping fence (`problem1_birth_spacing_does_not_supply_finite_support_budget.md`) said that finite support plus temporal spacing does not itself make late births finite, because original cells can be reused. The geometry here makes that obstruction sharper near the right fringe: for any bounded-width fringe mechanism, repeated late events do not even acquire new candidate original cells as time grows. Their possible original-support ancestry is trapped in one fixed terminal block.

Hence an injective budget of the form

    late birth -> a distinct original support cell in its backward cone

cannot be justified from causal geometry. If infinitely many candidate events remain in a fixed-width right-fringe strip, all of their ancestry sets are subsets of the same finite terminal block; indeed along a fixed offset ray the candidate block is identical at every time.

The extreme case `j=0` is especially clear: every cell on the maximal right ray `x=R+t` has only the single original support cell `R` available in its time-zero backward cone.

## What a successful original-fringe non-reuse lemma must contain

This does **not** rule out a finite-support budget. It rules out obtaining one merely by assigning distinct births to distinct ancestral cell *positions*. A successful charge must distinguish something that can be consumed or made incompatible across repeated uses of the same terminal cells, for example:

- a finite phase/state attached to the complete terminal fringe together with a proof that a regenerative passage cannot revisit a used state;
- a well-founded potential on the complete terminal fringe that strictly decreases despite the forced `beta=1` regeneration;
- an incompatibility between two separated passages having the same anchored terminal-fringe state.

This also gives a more precise computational target than searching arbitrary larger cores: if eventual `K=3` keeps the decisive passage in a uniformly bounded fringe width, enumerate/derive the *anchored terminal-fringe state transition* across the known nonreset return and test whether it is acyclic or admits recurrence. A recurrent state would kill any budget based only on that state; an acyclic transition graph would supply the sought finite-use bound.

## Scope

No new Rule-30 dynamical restriction is proved here beyond radius-one causal geometry. In particular, this does not show that a bounded-width terminal state exists for every relevant birth, nor that its transition is finite-state. It is a stopping fence against a weaker ancestry-position argument and a reduction of the next useful target to state/phase non-reuse on the fixed terminal ancestry block.

Dependencies: `problem1_birth_spacing_does_not_supply_finite_support_budget.md`; `problem1_nonreset_return_birth_spacing.md`; `ASTRA_HANDOFF.md`.
