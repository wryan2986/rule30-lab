# Problem 1 run 194 — corrected beta=1 t+7 discrepancy front

Problem 1 remains OPEN.

## Purpose

Run 193 exposed an inconsistency in runs 189–192. This note repairs the first broken front calculation while preserving the complete beta=1 driver.

## Retained facts

From the complete driver

`Y_(t+4)=G(z)=16 A^4 z+7`

and the established cut convention, the low actual cells at `t+4` satisfy

`(r_0,r_-1,r_-2,r_-3)=(1,1,1,0)`.

Together with the already-used right prefix `(r_0,r_1,r_2,r_3)=(1,1,1,0)`, two literal Rule-30 steps give

`x := r_0(t+6)=0`.

The pre-run189 terminal-pair calculation also gives at `t+6`

`r_-1 = hat r_-1 = 1`,
`r_0=0`, `hat r_0=1`,

and the actual/shadow right pairs

`(r_1,r_2)=(0,1)`, `(hat r_1,hat r_2)=(1,1)`.

These data are mutually consistent; the inconsistent datum was the later assertion `d_0(t+7)=0`.

## Direct discrepancy update

For Rule 30 write

`F(l,c,r)=l xor (c or r)`.

At position 0,

`r_0(t+7)=F(1,0,0)=1`,

while

`hat r_0(t+7)=F(1,1,1)=0`.

Therefore

`d_0(t+7)=1`.

At position 1,

`r_1(t+7)=F(0,0,1)=1`,

while

`hat r_1(t+7)=F(1,1,1)=0`,

so

`d_1(t+7)=1`.

At position -1, actual and shadow agree at -2,-1, and differ only at position 0. If their common `r_-2(t+6)` is `c`, then

`F(c,1,0)=c xor 1=F(c,1,1)`.

Hence

`d_-1(t+7)=0`.

The discrepancy front is therefore exactly

`m(t+7)=0`,

not `m(t+7)=1`.

Equivalently the characteristic index is

`J(t+7)=t+7`,

not `t+8`.

## Consequences

1. The run-189 inference `x=1` came from combining the correct local update formula with the incorrect eraser assertion `d_0(t+7)=0`. The complete-driver value `x=0` instead gives `d_0(t+7)=1` exactly.
2. Runs 184–192 that rely on `m(t+7)=1`, the rigid `0000` actual block at `t+7`, or a `t+8` positive-delay crossing are not established for the complete beta=1 trajectory.
3. The actual/shadow prefix at `t+7` begins, at positions 0 and 1,

   actual: `11`, shadow: `00`,

   with agreement at position -1. This is the correct seed for the next front calculation.

## Next target

Recompute `t+8` from this corrected seed while retaining enough cells on both sides to determine `m(t+8)` exactly. Then reconnect the result to the original-cut residence thresholds. Do not import any `t+8` delay/source classification from runs 184–192 without rederiving it from this corrected front.