# Problem 1 run 197 — corrected t+9 front

Problem 1 remains OPEN.

## Purpose

Continue the active corrected chain from runs 193--196. Run 196 fixed the complete-driver bit

`q=r_-4(t+4)=0`

and therefore the corrected front at `t+8`:

`m(t+8)=0`, `J(t+8)=t+8`.

This note propagates one more row without importing any invalidated run-184--192 source/delay claims.

## Next complete-driver bit

Put

`p := r_-5(t+4)`.

From

`Y_(t+4)=16 A^4 z+7`,

bit 5 of `Y_(t+4)` is bit 1 of `A^4 z`, so

`p = bit_1(A^4 z)`.

The defining zero low A-trace fixes bit 0 of every `A^n z`, but by itself does not numerically fix this bit-1 datum; therefore retain `p` rather than silently treating it as zero.

Using the complete low block from run 196,

`(r_-4,r_-3,r_-2,r_-1,r_0)(t+4)=(0,0,1,1,1)`,

three/four literal Rule-30 updates give

`r_-1(t+8)=1 xor p`.

Because `m(t+8)=0`, actual and shadow agree at positions `-2,-1` on row `t+8`, while run 195 gives

`r_0(t+8)=0`, `hat r_0(t+8)=1`.

## Discrepancy at -1 on row t+9

At position `-1`, actual and shadow have the same left and center inputs and differ only in their right input (position 0). For Rule 30,

`F(l,c,r)=l xor (c or r)`.

Changing `r` from 0 to 1 changes the output exactly when `c=0`. Here

`c=r_-1(t+8)=1 xor p`,

so

`d_-1(t+9)=p`.

## Discrepancy at 0 on row t+9

The corrected row `t+7` has actual/shadow `(r_0,r_1)=(1,1)/(0,0)` and common `r_-1=1` (because `q=0`). Hence on row `t+8`,

`(r_0,hat r_0)=(0,1)`.

Also the actual position-1 update is

`r_1(t+8)=F(1,1,r_2(t+7))=0`

independently of the unknown farther-right actual cell. The shadow position-1 value may depend on its farther-right neighbor, but since `hat r_0(t+8)=1`, that dependence is erased in the next update at position 0:

`r_0(t+9)=F(c,0,0)=c`,

`hat r_0(t+9)=F(c,1,hat r_1)=c xor 1`,

where the common left input is `c=r_-1(t+8)`.

Therefore

`d_0(t+9)=1`

for both values of `p` and for every farther-right continuation.

## Exact corrected front

Thus

`d_-1(t+9)=p`, `d_0(t+9)=1`,

and the global front is exactly

- `p=1 => m(t+9)=-1, J(t+9)=t+8`;
- `p=0 => m(t+9)=0, J(t+9)=t+9`.

Equivalently,

`m(t+9)=-r_-5(t+4)`.

So characteristic `t+8` either has a second-row residence (when bit 1 of `A^4 z` is 1) or the front advances immediately to characteristic `t+9` (when it is 0). No farther-right physical or shadow cells affect this decision.

## Status / next target

Runs 193--197 are the active corrected continuation. The next useful question is whether the retained complete-driver/global-threshold structure constrains

`p=bit_1(A^4 z)`.

The zero low A-trace alone only supplies `bit_0(A^n z)=0`, so a claim that `p` is fixed requires an additional identity linking bit 1 of `A^4 z` to a later low-trace bit or to the original-cut thresholds. If no such identity exists, this is the first genuine corrected branch after run 196 and both cases should be propagated rather than guessed.
