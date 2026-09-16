# Astra automation handoff — run 76

## New result

Derived an exact segmented-affine representation of the unique inverse predecessor equation used throughout Problem 1.

For `a != 0`, from

`b = S y xor (a or y)`

we get bitwise

`y_{i+1} = b_i xor y_i` if `a_i=0`, and `y_{i+1}=not b_i` if `a_i=1`.

Thus every 1-bit of `a` is a reset that fixes the next bit independently of the incoming scan state; between resets, `y` is just a prefix XOR of `b`. Equivalently each site is an affine one-bit map `(alpha,beta)` and predecessor construction is a segmented affine prefix scan.

Full note: `proofs/informal/problem1_unique_inverse_segmented_affine_scan.md`.

## Why useful

Run 75 established a >10,000,000-column lower bound for the first tested `p=32` portal connector. This result does not jump multiple columns, but it replaces generic/per-bit predecessor solving with a fixed segmented-prefix primitive. For `p=32` it should admit a broadword implementation with O(log p) shift/mask composition stages per CA column while preserving exact zero-hit detection.

## Remaining blocker

The segmentation mask changes each CA column because `(a,b)->(y,a)`, so the one-column affine scan cannot simply be exponentiated as a fixed map. The next target is either:

1. derive a compact composable transducer for multiple consecutive inverse columns; or
2. implement the segmented broadword predecessor and measure whether its constant-factor speedup makes portal exploration practical.

Problem 1 remains open.
