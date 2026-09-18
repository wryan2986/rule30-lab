# Birth budget requires a reuse theorem, not an ancestry map

Status: stopping-fence / blocker refinement. Problem 1 remains OPEN.

## Context

The current eventual-K=3 route requires infinitely many cyclic births under FULL, while the established two-bit nonreset passage forces a fresh lag-one row at t+6. Recent attempts tried to charge such births backward to the finite original actual support.

Run122 already observed that Rule 30 is left-permutive and that an original actual 1 can have descendants at arbitrarily late times. The present audit asks whether the stronger local information in the forced two-bit passage supplies the missing bounded-reuse statement.

## Audit of the forced passage

For a two-bit nonreset source at t, the established passage proves:

- the global-shadow centers at t,t+1,t+2 are 0,0,1;
- the return shadow pair at q=t+2 is exactly 10;
- the next cyclic source at t+4 has gate u;
- the vanished shadow zero-pair flag forces beta=1;
- hence a new lag-one even row is created at t+6;
- that t+6 one-bit t source is resetting;
- no nonresetting source occurs at t+1,...,t+7.

These facts determine the *local mechanism* of one forced regeneration, but they do not identify a finite original-support label whose availability changes after the birth.

In particular, neither of the two natural labels currently available is consumptive:

1. A causal ancestor in the original actual row is not consumptive, because left-permutivity allows the same original site to retain descendants at arbitrarily late times.
2. A causal ancestor in the global shadow is not finite, because the initial actual/shadow disagreement supply is infinite to the right.

The additional fact that the forced t+6 source is resetting also does not by itself repair this gap. "Resetting" is a statement about the source/core passage; no proved identity in the pushed branch maps that reset to deletion, exhaustion, or monotone advancement of an original-support label.

## Exact missing lemma

A finite-support contradiction from the present birth mechanism now requires a theorem of the following form (or a genuine substitute).

There is a finite label set S determined by the original actual row and a charge map C from sufficiently late forced births to S such that each s in S is charged at most B times, where B is uniform along the survivor.

Equivalently, an injection (B=1), a monotone label that cannot return, or an irreversible resource decrement would suffice.

What is *not* sufficient is any theorem asserting only that each birth has some original actual ancestor, some shadow-disagreement ancestor, or some resetting source in its recent past.

## Why the next step cannot be completed from the pushed identities

The pushed nonreset-return theorem gives the exact local birth flag and an eight-step exclusion window, but it contains no transition law for an original-support label across successive repair/birth episodes. The older handoff likewise states that bounded reuse/global-front transport remains open without an eventual strip bound. Thus deriving bounded multiplicity now would require a new cross-episode invariant, not another expansion of the already-collapsed local forcing cone.

This is the precise blocker. Future work should target a cross-episode quantity tied to the finite actual row and explicitly prove its update across both resetting and nonresetting passages. Local ancestry or additional fixed-window phase enumeration should not be repeated unless it produces that update law.
