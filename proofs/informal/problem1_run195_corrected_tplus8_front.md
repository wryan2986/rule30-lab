# Problem 1 run 195 — corrected beta=1 t+8 discrepancy front

Problem 1 remains OPEN.

## Purpose

Continue from run 194's repaired seed at `t+7` and determine the global discrepancy front at `t+8` without importing any of the invalidated run-184--192 `t+8` classifications.

## Retained corrected data

Run 194 gives

- `m(t+7)=0`, hence actual and shadow agree at every position `<0`;
- at positions `0,1`, actual/shadow are respectively `11/00`.

Let

`q := r_-4(t+4)`.

The complete beta=1 driver fixes

`(r_-3,r_-2,r_-1,r_0)(t+4)=(0,1,1,1)`.

A direct Rule-30 propagation on the left side gives

`r_-3(t+5)=1 xor q`,
`r_-2(t+5)=1`,
`r_-1(t+5)=0`,

then

`r_-2(t+6)=q`,
`r_-1(t+6)=1`,
`r_0(t+6)=0`,

and therefore

`r_-1(t+7)=1 xor q`.

Because `m(t+7)=0`, the shadow has the same value at `-1`, and actual/shadow also agree at `-2`.

## Exact t+8 front update

Write the common `t+7` value at position `-2` as `L`, and put

`c := r_-1(t+7)=1 xor q`.

At position `-1`, the actual right neighbor is `1` while the shadow right neighbor is `0`. Thus

`r_-1(t+8)=F(L,c,1)`,
`hat r_-1(t+8)=F(L,c,0)`.

For Rule 30, `F(l,c,r)=l xor (c or r)`, so these differ exactly when `c=0`. Hence

`d_-1(t+8)=q`.

At position `0`, the `t+7` triples are

actual: `(c,1,1)`,
shadow: `(c,0,0)`.

Therefore

`r_0(t+8)=F(c,1,1)=c xor 1`,
`hat r_0(t+8)=F(c,0,0)=c`,

and consequently

`d_0(t+8)=1`

for both values of `q`.

This determines the front exactly:

- if `q=1`, then `m(t+8)=-1` and `J(t+8)=t+7`;
- if `q=0`, then `m(t+8)=0` and `J(t+8)=t+8`.

Equivalently,

`m(t+8) = -r_-4(t+4)`.

## Consequences

1. The corrected `t+8` passage is not the forced positive-delay center crossing claimed in the invalidated run-184--192 chain. The global front either remains on characteristic `t+7` or advances only to characteristic `t+8`.
2. No right-side cells beyond the corrected `11/00` seed are needed to decide `m(t+8)`.
3. The entire corrected `t+8` front branch is selected by one previously unexploited bit of the complete cyclic driver, `r_-4(t+4)`.
4. This is consistent with front monotonicity in characteristic coordinates: from `J(t+7)=t+7`, the next value is either `t+7` or `t+8`.

## Next target

Decode `q=r_-4(t+4)` from the retained complete driver formula `Y_(t+4)=16 A^4 z+7`, if possible, rather than treating it as a free physical cell. If the complete-driver formula leaves `q` free, propagate both corrected branches to `t+9` and reconnect them to the residence/threshold identities. Do not reuse the old run-184--192 `t+8` delay/source classification.