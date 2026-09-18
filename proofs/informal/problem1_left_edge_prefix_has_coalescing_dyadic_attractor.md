# Left-edge prefixes coalesce onto a dyadic attractor (computational stopping fence)

Status: `computational-result` plus exact local recurrence. Not a proof of Problem 1.

## Setup and exact recurrence

Let a nonzero finite Rule-30 row have original left endpoint `L`, and use coordinates moving with the left light-cone edge

    b_j(t) = x_{L-t+j}(t),   j >= 0.

For Rule 30, `f(l,c,r)=l XOR (c OR r)`. Therefore

    b_j(t+1) = b_{j-2}(t) XOR (b_{j-1}(t) OR b_j(t)),

with `b_{-1}=b_{-2}=0`.

In particular `b_0(t)=1` for every physical orbit. Also

    b_1(t+1)=b_0(t) OR b_1(t)=1,

so after one step the first two left-edge bits are permanently `11`. Unlike the moving-right-fringe map, this finite-prefix map is generally noninjective, so it can erase initial information.

## Exhaustive finite-prefix experiment

I exhaustively enumerated every `n`-bit prefix with `b_0=1` for `1 <= n <= 19`, iterated the exact recurrence above until repetition, and canonicalized cycles up to cyclic rotation.

For every tested width:

1. every one of the `2^(n-1)` initial prefixes reached the same eventual cycle (up to phase);
2. every observed cycle length was a power of two;
3. the cycle lengths by width were:

       n = 1,2,3       : 1
       n = 4,...,8     : 2
       n = 9,...,19    : 4

The maximum transient lengths over all initial prefixes were

    n:             1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
    max transient: 0  1  2  2  4  5  6  8  8 11 12 14 14 16 17 19 22 22 26

The enumeration at width 19 covers all `2^18 = 262144` prefixes.

These observations are not promoted to an all-width theorem here. They are, however, a strong negative signal for the run-116 proposal of charging regenerative births to a bounded left-edge state: bounded-depth left-edge information appears to *forget* the original finite row and coalesce onto a universal dyadic attractor rather than retain a nonrenewable label.

## Why this matters for the birth-budget program

Run 116 showed that finite-support nonreturn is stored at depth growing with time. One possible response was to look toward the expanding left boundary for a source-indexed characteristic resource. The exact recurrence here shows that merely replacing a fixed right-edge prefix by a fixed left-edge prefix does not solve the problem: the left prefix is autonomous and dissipative, and exhaustive tests through width 19 show complete coalescence of all initial prefix states onto one small dyadic cycle.

Thus a viable left-boundary charge must again use depth growing with time, or preserve a characteristic/history label not recoverable from a fixed instantaneous left prefix. A proposed bounded left-edge automaton should be treated as suspect unless it explicitly imports such information.

## Reproduction pseudocode

For width `n`, encode `b_j` as bit `j` of integer `x`. The exact prefix update is

    mask = (1 << n) - 1
    x = ((x << 2) XOR ((x << 1) OR x)) AND mask

Enumerate all odd `x` in `[0,2^n)` and detect the first repeated state. Canonicalize each eventual cycle by its lexicographically least rotation before comparing attractors.

## Next target

The source-indexed characteristic idea survives only in an unbounded-depth form. A useful next step is to identify the spacetime characteristic actually carrying a forced `beta=1` birth backward toward time zero and determine whether its time-zero intercept or crossing order is monotone across successive forced births. A finite left-prefix phase by itself is unlikely to provide the missing bounded-reuse theorem.

Problem 1 remains OPEN.
