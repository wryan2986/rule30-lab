# Astra automation handoff — 2026-09-19 run 141

## Starting state

Started from `research/astra-next` at `459ca96b4f3467c4150ca81ea14f8c7a3a7b6a39`, immediately after run 140. No intervening research work was found.

Problem 1 remains OPEN.

## New episode-specific collapse

Returned to the FULL cyclic-source/right-fringe data as requested by run 140. At the distinguished two-bit-return cyclic source `q=t+2`, previous work gives the global-shadow word `01110` on positions `-2,...,2`.

Using the FULL center trace `1,0,1,0,1,0` for times `q,...,q+5`, exact Rule-30 cone evolution successively forces

- `hat r_-3(q)=1`,
- `hat r_-4(q)=0`,
- `hat r_-5(q)=1`.

Hence the exact source-relative word is

`(hat r_-5,...,hat r_2)(q) = 10101110`.

The five cells immediately left of center are therefore the rigid staircase `10101`.

This is independent of the unknown wider right fringe through position `-5`. It is a genuine episode-specific collapse, unlike the moving-frame reindexing fenced off in run 140.

The same cone also gives, writing `a=hat r_3(q)`,

`hat r_1(q+2)=1 XOR a`, `hat r_2(q+2)=1`.

Full note: `proofs/informal/problem1_distinguished_011_full_trace_forces_five_cell_left_staircase.md`.

Research commit: `4e9c75f32377a83f3714af8e9675f8680831a297`.

## Stopping fence

Do not infer an infinite alternating left tail. The forcing ceases to be uniform beyond this finite staircase: the next new left cell can depend on wider right-fringe data. This agrees with the earlier left-permutivity no-go for center traces.

## Best next target

Exploit the exact `10101110` source motif together with the known `t -> u` cyclic gate passage to test whether the wider right driver `(hat r_3,hat r_4,...)` obeys a repeatable finite-state relation across `q -> q+2 -> q+4`. The useful target is a relation that reduces or bounds driver freedom across episodes; merely propagating the alternating center farther left is not useful.

Problem 1 remains OPEN.
