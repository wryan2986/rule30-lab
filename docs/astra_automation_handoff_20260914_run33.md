# Astra automation handoff — 2026-09-14 run 33

Branch: `research/astra-next`

## Repository state reviewed

Run started from `7c5772b27409a17b18ef13f7ba9cd17dad23b216` (run 32 handoff). No newer work was present on `research/astra-next`.

Problem 1 remains open.

Run 32 showed that every immediately repaired long corridor (`G>=3`) collapses to `G'<=1`, so the re-entered `A^p`-fixed row collides again on its very next physical successor.

## New result: exact mask at the forced recollision

Added:

- `proofs/informal/problem1_repaired_long_corridor_forces_next_collision_mask.md`

Commit:

- `eec8574f61bf678f20927529c4b9f9135f091542`

The exact commutator boundary formula extends the first-collision mask calculation cleanly to zero corridor. If an `A^p`-fixed row has `G=0`, then its next physical row has defect

    3 if the return fringe is even,
    1 if the return fringe is odd.

For `G=1`, the already-proved odd-corridor rule gives defect 1.

The exact transported fringe after long-corridor repair is

    R' = T^(D+2)(R) mod 2^(2p),

and Rule 30 preserves parity, so `R' == R (mod 2)`.

The long-corridor immediate-reentry criteria already imply:

- original odd `G>=3`: `R` must be odd, while `G' in {0,1}`;
- original even `G>=4`: `R` must be even, while `G'=0`.

Therefore the forced next-step recollision mask is completely determined by the parity of the original long corridor:

    odd long G  -> repair -> forced recollision defect 1
    even long G -> repair -> forced recollision defect 3

No distinction between `G'=0` and `G'=1`, no leading-four-bit flag, and no interior fringe information survives into this mask.

## Why this advances the global bridge

The post-repair short-gap collision is no longer an arbitrary collision. Its incoming defect class is known exactly. This lets the existing defect-1 and defect-3 successor classifiers be applied directly to the transported fringe provenance.

The next target is to determine whether a *second* immediate same-period re-entry from this forced recollision is possible. The useful calculation should combine:

1. the known incoming mask (`1` for repaired odd corridors, `3` for repaired even corridors),
2. the defect-1/defect-3 exact successor classifiers,
3. `R'=T^(D+2)(R) mod 2^(2p)`, and
4. the already-known endpoint restrictions on the original `R` required for the first repair.

If a second repair is impossible in one or both parity classes, or if it forces a bounded deterministic transition, then same-period repair-chain length becomes controlled. That is the most direct current route from the completed local corridor analysis into the older FULL/common-origin period/phase accounting.
