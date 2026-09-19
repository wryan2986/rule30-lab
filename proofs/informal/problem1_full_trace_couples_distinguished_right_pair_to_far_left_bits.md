# Problem 1: FULL couples the distinguished right pair to farther-left source bits

Status: exact local lemma; computationally exhaustively checked over the relevant free bits.

At the distinguished cyclic source `q` from runs 141--143 we already have

```text
(r_-5,...,r_2)(q) = 10101110.
```

Write

```text
a = r_3(q),   b = r_4(q),   s = a OR b.
```

The previous run showed that the four-step transported pair at the resetting source is

```text
(r_1,r_2)(q+4) = (a, a OR b).
```

A tempting interpretation was that this pair might be an autonomous episode state.  The full alternating center trace gives a different and useful consequence: it couples this right pair back to source cells *left* of the previously rigid `10101110` block.

## Exact forced extension

Assume FULL continues through times `q+6,q+7,q+8,q+9`.  Exact Rule-30 cone evaluation gives

```text
r_0(q+6) = r_-6(q) XOR (a OR b).
```

Since FULL requires `r_0(q+6)=1`,

```text
r_-6(q) = NOT(a OR b).
```

Continuing the same inverse-center calculation with the required alternating values at `q+7,q+8,q+9` gives

```text
r_-7(q) = a OR b,
r_-8(q) = a OR (NOT b),
r_-9(q) = 1.
```

Thus the distinguished source is not merely rigid on `[-5,2]`: its next four cells to the left are forced by only the two right-driver bits `(a,b)`.

Equivalently, the block `r_-9 ... r_-6` is

```text
(a,b)=00 : 1101
(a,b)=01 : 1010
(a,b)=10 : 1110
(a,b)=11 : 1110
```

followed by the already-forced block `10101110` on `[-5,2]`.

The identities were checked by exhaustive Boolean evaluation of the exact Rule-30 light cone, varying the relevant unconstrained source bits.  In particular, the first identity is independent of farther right bits, and the successive forced-left values are obtained uniquely from left-permutivity once the FULL center value at each next time is imposed.

## Why this matters

Run 143 showed that farther right information re-enters the *full* resetting-source neighborhood, so `(r_1,r_2)(q+4)` does not close that neighborhood by itself.  The present calculation shows that FULL nevertheless turns the same two-bit right driver into a surprisingly long rigid cross-source constraint on the opposite side of the center.

This is a more promising use of the pair than treating it as an autonomous forward state: the pair labels one of only three distinct forced left extensions (`10` and `11` coincide through `r_-9`).  A next useful test is to continue the inverse-center calculation and determine the first left offset at which `a,b` cease to suffice and `r_5(q),r_6(q),...` enter.  If the two-bit dependence persists uniformly, that would be a genuine finite-state compression of the FULL distinguished source; if it fails, the first entering fringe bit gives the exact obstruction.

This lemma does not by itself prove a contradiction or a finite birth budget.
