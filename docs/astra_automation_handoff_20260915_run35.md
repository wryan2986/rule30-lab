# Astra automation handoff — 2026-09-15 run 35

Branch: `research/astra-next`

## Repository state reviewed

Run started from `4e598989e09d827ee7e3105a7b8154efd57c928f` (run 34 handoff). No newer work was present on the branch.

Problem 1 remains open.

Run 34 disproved a tiny universal bound on same-period repair-chain length: an exact period-8 witness has 13 consecutive `A^8`-fixed nodes separated by one-step collisions.

## New exact result

Added `proofs/informal/problem1_two_step_repair_train_fringe_dynamics.md`.

For fixed `p`, put `m=2p`. If an `A^p`-fixed state `z` with return fringe `R` successfully repairs its immediate collision so that `z_+=T^2(z)` is again `A^p`-fixed, then its new return fringe is exactly

`R_+ = T^2(R) mod 2^(2p)`.

Hence along any alternating same-period repair train,

`R_j = T^(2j)(R_0) mod 2^(2p)`.

The large physical fixed state is therefore unnecessary: the whole train is a segment of the finite permutation orbit of

`F_p(R)=T^2(R) mod 2^(2p)`,

filtered by the already-derived endpoint repair conditions.

Because Rule 30 modulo `2^(2p)` is bijective, `F_p` is a permutation. A complete fringe determines at most one finite `A^p`-fixed state, while a nonzero finite physical Rule-30 orbit strictly increases bitlength. Thus a finite same-period repair train cannot revisit a fringe.

For an alternating short-gap train every fixed node has `G=0` or `G=1`. There are only

`2^(2p-1) + 2^(2p-2) = 3*4^(p-1)`

such nonzero fringes. Therefore

`N_fixed <= 3*4^(p-1)`.

This is crude but unconditional and closes the possibility of an infinite repair train at one fixed period. The remaining global issue is repeated escape into changed/larger periods or phases.

## Next target

Compute maximal admissible path lengths under the exact endpoint repair filter along `F_p` for modest `p`, looking for a substantially smaller period-dependent law. Then connect exit from this finite admissible set to the existing FULL/common-origin period-growth/birth accounting.

Commit this run before handoff: `ec1602e5b6f234befb67e6f6241fe0d05a38bed7`.
