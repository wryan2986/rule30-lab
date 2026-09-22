# Astra automation handoff — 2026-09-21 run 196

Problem 1 remains OPEN.

## New result

Run 195's remaining branch bit is forced by the complete driver. Let

`q=r_-4(t+4)`.

For the original nonresetting source core `z=Z_t`, the retained theorem gives

`Y_(t+4)=16 A^4 z+7`,

while nonresetting means the low `A`-trace of `z` is identically zero. Under the cut convention, bit 4 of `Y_(t+4)` is `r_-4(t+4)`, and from the displayed driver formula that bit is exactly bit 0 of `A^4 z`. Hence

`q=(A^4 z)_0=0`.

Run 195 had proved

`d_-1(t+8)=q`, `d_0(t+8)=1`,

so the corrected trajectory has uniquely

`m(t+8)=0`, `J(t+8)=t+8`.

The alternative `q=1`, `J(t+8)=t+7` branch is impossible on the actual complete nonresetting driver.

The complete low-five actual block at `t+4` is therefore

`(r_-4,r_-3,r_-2,r_-1,r_0)=(0,0,1,1,1)`.

## Correction status

Runs 193--196 are the active corrected continuation. Do not reuse run-184--192 claims depending on the erroneous `m(t+7)=1` premise. This run fixes the corrected front at `t+8`; it does not restore the old `t+8` source/delay classification.

## Next target

Propagate the unique corrected branch to `t+9` using complete-driver bits. The next left driver bit is expected to be bit 5 of `Y_(t+4)`, i.e. bit 1 of `A^4 z`; do not assume it is free or fixed without deriving the relevant complete-driver constraint. Then reconnect the resulting front residence to original-cut thresholds.

Proof: `proofs/informal/problem1_run196_complete_driver_forces_corrected_tplus8_branch.md`.