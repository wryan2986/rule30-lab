# Astra automation handoff — run 146 — 2026-09-19

Problem 1 remains OPEN.

## New result

The inverse-center dependency-frontier route now has a decisive stopping fence.

Starting from the distinguished source motif `(r_-5,...,r_2)=10101110`, I exhaustively enumerated right-driver assignments and solved the unique left extension required by the alternating FULL center trace using Rule 30 left-permutivity.

Essential right-driver sets for the first new left offsets are:

- `r_-6`: `r_3,r_4`
- `r_-7`: `r_3,r_4`
- `r_-8`: `r_3,r_4`
- `r_-9`: none
- `r_-10`: `r_3,r_4,r_5,r_6`
- `r_-11`: `r_3`
- `r_-12`: **all of `r_3,...,r_12`**

So at `r_-12` the forced left bit genuinely depends on `r_12`, the farthest right coordinate in its generic time-12 light cone. An explicit witness fixes `(r_3,...,r_11)=101101000` and changes only `r_12`: the required `r_-12` changes from 0 to 1.

Full result: `proofs/informal/problem1_inverse_center_dependency_frontier_reaches_full_cone_at_minus12.md`.

## Interpretation

The delay discovered in runs 144-145 is transient, not a bounded-width compression. The inverse-center frontier reaches the generic cone boundary by offset 12. Do not spend another run merely extending this dependency table; a fixed-width inverse-center transducer cannot reconstruct the FULL-compatible source row uniformly.

## Next target

Return to the cyclic episode/gate quotient route. The useful question is whether the **return/birth observable itself**, rather than the full resetting-source neighborhood, factors through a small quotient of the wider fringe. Search for two FULL-admissible resetting-source configurations with the same candidate quotient state but different next return/birth outcomes; either a counterexample identifies the next required state bit, or failure to find one supports a genuine quotient theorem.
