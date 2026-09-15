# Astra automation handoff — 2026-09-14 run 32

Branch: `research/astra-next`

## Repository state reviewed

Run started from `24d59d54582b9af35ab34f40c31c769ff0b1eff4` (run 31 handoff). No newer work was present on `research/astra-next`.

Problem 1 remains open.

Re-read the run-31 handoff and the older global FULL/common-origin notes. The older global blocker remains: spacing of nonresetting sources does not by itself give a finite-support upper bound on infinitely many required births.

## New result: residence consequence of the corridor-collapse theorem

Added:

- `proofs/informal/problem1_long_corridor_reentry_forces_next_step_recollision.md`

Commit:

- `5f06f399817b53784a854e80ce74c4d20bb1595d`

The corridor geometry says that an `A^p`-fixed row with corridor `G` first collides after `floor(G/2)+1` physical Rule-30 steps. Runs 30-31 proved that after immediate same-period re-entry from any long corridor `G>=3`, the re-entered corridor satisfies `G'<=1` (indeed `G'=0` for even `G`, and the exact four-bit formula determines `G'` for odd `G`).

Therefore `floor(G'/2)=0`, so the re-entered fixed row's very next physical successor is already another same-period collision.

Thus a long same-period corridor cannot regenerate into another long same-period residence block by immediate re-entry. Its terminal shape is necessarily

    ... -> collision x -> re-entered fixed row z' -> next-step collision T(z').

Any hypothetical survivor with infinitely many long corridors must therefore change effective period/phase mechanism at those forced next-step recollisions; it cannot indefinitely remain in one repaired `p`-phase.

This is a genuine bridge from the local endpoint calculations to the global residence language, but it is not yet a contradiction. No monotonicity of minimal `A`-period under `T` has been proved, and the remaining task is to control the sequence of period/phase changes forced by these recollisions.

## Next target

Analyze the short-gap (`G=0,1`) collision immediately following a repaired long corridor. The sharp question is whether its special provenance from fringe transport `R'=T^(D+2)(R) mod 2^(2p)` forces period doubling, period loss, or another bounded transition. A theorem restricting that transition would connect the local corridor classification directly to the older FULL/common-origin birth budget.
