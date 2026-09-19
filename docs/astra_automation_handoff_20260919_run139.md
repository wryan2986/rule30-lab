# Astra automation handoff — 2026-09-19 run 139

## Starting state

Started from `research/astra-next` at `b58491aff2a5ea1e2567a9fbe6e0f0270ca7d379`, immediately after run 138. No intervening research work was found.

Problem 1 remains open.

## New result

Strengthened run 138's moving-frame observation to an inductive theorem: **for every fixed offset `j` behind the deterministic left support front, `t -> y_j(t)` is eventually periodic.**

Reason: once the two lower offsets driving `y_j` are periodic with period `P`, one full forcing period induces a fixed self-map of the single bit `y_j`. A self-map of `{0,1}` has eventual cycle length at most 2, so `y_j` has eventual period dividing `P` or `2P`. Thus power-of-two period upper bounds can be chosen recursively.

Full note:

`proofs/informal/problem1_fixed_left_front_offsets_are_eventually_periodic.md`

Research commit: `b75b7ce5ec870a9d6b6489988cd0904f9bb2eca0`.

## Why it matters / stopping fence

Every bounded-depth strip at the left support front eventually cycles; no fixed offset can retain aperiodic information indefinitely. But the distinguished cyclic-source `011` events near the fixed center occur at moving-frame depth `j ~ t`, so pointwise-in-`j` eventual periodicity does not control them.

Do not spend another run tabulating more fixed offsets or larger fixed windows unless that computation exposes a formula uniform in depth.

## Best next target

Seek a **uniform-in-depth transport law** from the triangular moving-front recurrence down the growing diagonal `j~t` to the center/source coordinates. A useful law must compress this growing-depth information into finite range while retaining enough of the cyclic-source gate/right-fringe constraints to force progress or bounded reuse. Equivalently, search for a finite automaton/transducer or affine/parity quantity whose update is uniform in `j`, rather than another fixed-width boundary invariant.

Problem 1 remains open.
