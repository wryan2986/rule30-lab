# Astra automation handoff — 2026-09-19 run 137

Problem 1 remains OPEN.

## New result

Added `proofs/informal/problem1_distinguished_011_ordinary_ancestry_immediately_reuses_cyclic_center.md`.

At each distinguished source-relative `011` event from the forced-birth passage,

    (r_-2(q),r_-1(q),r_0(q))=(0,1,1),  q=t+2.

The output `r_-1(q+1)=1` has two ordinary 1-parents, and its right 1-parent is exactly the preceding cyclic center `r_0(q)=1`. Hence ordinary 1-ancestry from the later forced birth can immediately reuse the previous cyclic-center lineage:

    center(t+4) <- r_-1(t+3) <- center(t+2).

Thus the special `011` obstruction is only an obstruction to sensitive-1 provenance. It does not itself force consumption of a new ordinary ancestry label or a new initial 1-site.

## Stopping fence

Do not spend another run merely assigning finite-support initial 1-ancestors to distinguished `011` events. The local geometry explicitly permits cyclic-center lineage reuse, so such an assignment has no finite budget without an independent bounded-multiplicity theorem.

Run136 already showed that arbitrary finite FULL center prefixes are realizable by finite-support rows, so center alternation alone also cannot supply the missing obstruction.

## Best next target

Return to invariants that use the *complete* cyclic-source/gate/right-fringe state rather than center trace or ancestry alone. In particular, test whether a moving cut attached to successive cyclic sources has a finite-state crossing datum that must strictly change at each two-bit nonreset forced-birth passage. Any candidate must simultaneously have finite range (from finite initial support) and bounded reuse/strict progress; reject candidates that provide only one of those properties.
