# Problem 1 run 196 — complete driver forces the corrected t+8 branch

Problem 1 remains OPEN.

## Purpose

Run 195 reduced the corrected `t+8` discrepancy front to one bit

`q := r_-4(t+4)`

of the complete beta=1 return driver. This note decodes that bit from the already retained complete-driver formula rather than treating it as an independent physical cell.

## Complete-driver decoding

At the original nonresetting source time `t`, let `z=Z_t`. By definition of a nonresetting source in `problem1_nonreset_return_birth_spacing.md`, the low `A`-trace of `z` is identically zero:

`(A^n z)_0 = 0` for every `n>=0`.

The same proof gives the complete cyclic u-source at `t+4` exactly as

`Y_(t+4) = G(z) = 16 A^4 z + 7`.

Under the established cut convention, bit `k` of `Y` is physical cell `r_-k`. Multiplication by 16 shifts the binary word four places, while `+7` sets only bits 0,1,2. Therefore

`r_-4(t+4) = bit_4(Y_(t+4)) = bit_0(A^4 z)`.

Since the source core `z` has identically-zero low `A`-trace,

`bit_0(A^4 z)=0`.

Hence the run-195 branch bit is not free:

`q = r_-4(t+4) = 0`.

This also makes the already decoded low five bits of the complete driver

`(r_-4,r_-3,r_-2,r_-1,r_0)(t+4)=(0,0,1,1,1)`.

## Corrected t+8 front

Run 195 proved, without importing the invalidated run-184--192 chain,

`d_-1(t+8)=q`,
`d_0(t+8)=1`,

and therefore

- `q=1 => m(t+8)=-1, J(t+8)=t+7`,
- `q=0 => m(t+8)=0, J(t+8)=t+8`.

Substituting the complete-driver value gives the unique actual branch

`m(t+8)=0`,
`J(t+8)=t+8`.

Together with run 194's `J(t+7)=t+7`, the global front advances by one characteristic between these rows; the alternative residence of characteristic `t+7` through row `t+8` is excluded.

## Why this is new information

Run 195 explicitly left `q` for complete-driver decoding. The formula `G(z)=16 A^4 z+7` alone does not make bit 4 a numerical constant for arbitrary `z`; the decisive extra fact is that this `z` is the core of the original nonresetting source, whose entire low `A`-trace is zero. Thus no new local prefix census or independent fringe assumption is being introduced.

## Correction status

Runs 193--196 remain the active corrected continuation. Do not revive the run-184--192 claims that depended on the erroneous `m(t+7)=1` premise. In particular this result determines the corrected global front at `t+8`; it does not by itself restore any old resetting/nonresetting classification for a `t+8` source.

## Next target

Propagate the now unique corrected branch from `t+8` to `t+9`, retaining the complete-driver bits rather than introducing independent left cells. Reconnect any resulting front residence to the original-cut threshold identities only after the discrepancy row is derived. The global unresolved task remains a finite-support bound on the repeated supply of nonresetting returns/births.