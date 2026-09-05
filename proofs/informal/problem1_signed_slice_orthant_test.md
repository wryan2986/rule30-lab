# Orthant-union candidate for admissible signed slices

Status: `refuted` for the two-orthant restriction, with an exact finite
counterexample on the admissible ancestor domain. Signed nonvanishing remains
`inconclusive`.

The connected-region obstruction does not rule out the disconnected union
of the nonnegative and nonpositive orthants, with the origin removed. If
every admissible ancestor's outgoing five-slice vector lay there and were
nonzero, its total signed mass would be nonzero. These are two separate
claims: sign coherence of the components does not exclude the zero vector.

Candidate under test: for every ancestor of an admissible three-return
cylinder in either phase, its outgoing slice vector has no two components
of opposite strict sign. The all-depth claim is `inconclusive` before this
check. It is a possible first condition in a disconnected-region induction,
not already a nonvanishing proof.

Admission: a mixed-sign vector on one actual ancestor refutes this proposed
orthant restriction, requiring a finer region or arithmetic argument. No
mixed-sign vector in the fixed box only justifies structural work on that
box's surviving candidate, not a larger census or an infinite inference.

Test order and fixed scope: the 25 ancestors of the existing 19 full-domain
three-return occurrences through complexity 16, sorted by complexity, phase
p before u, depth, state; then the two previously verified complexity-18
nodes `(u,0x642e4d2f1,L=3)` and `(u,0x6473d46ab,L=5)`.
The first node has a verified complexity-19 descendant but this check builds
only the phase-u frontier through 18. Stop at the first mixed-sign vector.
Retain exact positive/negative component endpoint subtotals and direct vs
recursive belief agreement. Both outcomes bear on the all-depth signed
certificate; no nonvanishing census cap is enlarged. Limits: one local CPU,
120 seconds, 1 GiB; atomic result with complete provenance.

## Exact result

The second node in the prescribed order is already a counterexample:

```text
phase u, k=13, x=0x190bf7e, L=1,
V=(60,0,72,-9,34), in order (0000,0011,1011,1100,1111).
```

It has 357 distinct endpoints and total signed mass 157. The exact even- and
odd-defect endpoint counts in the five outgoing slices are

```text
0000: (101,41); 0011: (0,0); 1011: (72,0);
1100: (0,9); 1111: (84,50).
```

The negative `1100` component and positive `1011` component put the vector
outside both orthants. This is an actual ancestor of the admissible cylinder

```text
phase u, k=14, state=0x642fdfb, L=2, cut=1, gaps=(2,2,2),
forced schedule tutututu, generator witness uuuuputptutpuu.
```

The witness head `u` denotes the seed 1. Stripping one low digit from that
cylinder gives exactly the displayed ancestor. Thus the counterexample does
not rely on an arbitrary frontier state outside the restricted domain.

`finite-exhaustive` scope: the occurrence/ancestor construction retains the
existing complexity-16 box (19 occurrences, 25 ancestors). The sign-coherence
search evaluated two nodes and stopped at its first failure; the remaining
25 planned checks, including the named complexity-18 nodes, were not run.
No claim of an all-depth smallest example is made.

Reproduce with `python3 scripts/check_signed_slice_orthants.py`. The atomic
record `results/problem1/20260905_signed_slice_orthants.json` contains exact
counts, ancestry, source/output hashes, source commit and run provenance.
Muse independently recalculated the same single belief using the pre-existing
independent signed-mass oracle, including direct/recursive agreement, witness
replay, and final-u admissibility; its review is archived separately.

The refuted proposal is componentwise sign coherence. This result does not
refute a union of more general regions, a valuation invariant, signed
nonvanishing, or belief nonemptiness. In particular, this very belief has
`v_2(357)=0 != v_2(200)=3`, so it satisfies the separate proposed arithmetic
certificate despite the mixed signs.
