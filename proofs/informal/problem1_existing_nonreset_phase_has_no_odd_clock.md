# Problem 1: the established nonreset return does not supply an odd fringe clock

Status: structural audit / no-go; Problem 1 remains open.

## Purpose

Run 113 proved that every finite continuous dynamical factor of the instantaneous moving-right fringe has only power-of-two cycles. The suggested next test was whether the already established FULL/nonreset source-phase machinery forces a nonconstant odd-order phase that could contradict that theorem.

This note audits the strongest currently pushed nonreset-return result, `problem1_nonreset_return_birth_spacing.md`. It does **not** reconstruct the missing round309 core/phase drafts mentioned by `ASTRA_HANDOFF.md`, because those files are absent from the pushed branch.

## What the established passage actually forces

At a late even nonresetting source time `t`, write `u` for the gate-u indicator. The pushed proof establishes:

- the next two even sources `t+2,t+4` are cyclic;
- their actual gates are respectively `t,u`;
- the first cyclic source cannot birth;
- in the two-bit source case `u=0`, the source at `t+4` forces `beta=1`, hence a new lag-one even row at `t+6`;
- the gate at `t+6` is `t` by no-`uu`;
- when `beta=1`, that new one-bit `t` source is resetting;
- no nonresetting source occurs at `t+1,...,t+7`.

The forced finite gate word is therefore built from the two gate symbols `t,u`; the explicitly transported even-source portion is `t,u,t` (with the initial source type encoded separately by `u`). Nothing here forces a three-cycle or any other odd-order recurrent phase.

Likewise, the forced center data used in the shadow calculation are the finite word `0,0,1`; this is a local passage condition, not a deterministic recurrent three-state factor. Treating those three successive values as a period-three clock would confuse a length-three transient word with a cycle.

The birth profile also fails to create an odd clock. In the two-bit case the proved pattern through the passage is a finite sequence ending in the forced `beta=1`; the proof explicitly stops short of an infinite repeating repair/birth cycle. Thus there is no justified finite-state return map whose reachable cycle has odd order.

## Consequence for the dyadic-factor route

The existing pushed nonreset theorem is fully compatible with the dyadic finite-factor theorem. Its genuine recurrent-looking gate information is binary / parity-based, while the only length-three-looking datum (`0,0,1`) is a finite shadow-center word and has not been shown to recur as a 3-cycle.

Therefore run 113's odd-factor contradiction cannot be obtained merely by relabeling the already proved gate, center, or birth phases. A useful odd obstruction would require a new theorem proving an actual deterministic return cycle with an odd factor in its period.

There is also a second obstruction. `ASTRA_HANDOFF.md` says the recovered complete-core phase transport has an explicit parity commutator and that no phase-discarding quotient on its domain exists. Those details indicate that the richer phase may depend on complete core/source information rather than only the instantaneous moving fringe. Since the corresponding pushed draft is absent, this note does not promote that summary into a theorem. But even if recovered, such a phase would first have to pass the run-113 factor test: prove that it is determined by a finite instantaneous fringe prefix before the dyadic-cycle theorem can be applied to it.

## Stopping fence

Do not pursue an odd-period contradiction by interpreting any of the following as a recurrent odd clock without a new return theorem:

- the three shadow centers `0,0,1`;
- the three displayed even-source gates `t,u,t`;
- a repair / cyclic / birth sequence observed only across one finite passage.

A finite word of odd length is not an odd-order dynamical factor.

## Remaining productive target

The dyadic-factor route now has a precise admission test. A candidate phase must come with both:

1. a deterministic recurrent return law forcing a nonconstant cycle with an odd factor; and
2. a proof that the phase is determined by a finite instantaneous moving-fringe prefix.

The currently pushed nonreset-return machinery supplies neither pair simultaneously. Until such a phase is found, the principal unresolved target remains the older one: a nonrenewable original-fringe/core resource or other finite-support upper bound on the infinitely required cyclic births.
