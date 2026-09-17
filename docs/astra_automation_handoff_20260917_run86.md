# Astra automation handoff — run 86

## Main result: compute the relevant root basin of `P_n`, not its full functional graph

No intervening work was present after run 85 (`8ed470e97ace13d3089094a0d1cb07e26176cc7a`).

Using run 84's exact reverse pair map `F(u,v)=(v, S u XOR (v OR u))`, I computed `rho_n^{-1}` and hence run 85's parent map `P_n=D o rho_n^{-1}` on every binary necklace through `n=10`.  The important refinement is to retain only the component whose repeated `P_n` iterates reach the terminal root `0`; other functional components of `P_n` are not part of the reverse zero basin.

Root-basin sizes (including zero) for `n=2..10` are:

`3, 2, 4, 2, 3, 2, 5, 2, 3`.

Every one of these small root basins is a path with one odd-parity terminal leaf.  Leaves are:

- n=2 `01`
- n=3 `111`
- n=4 `0111`
- n=5 `11111`
- n=6 `010101`
- n=7 `1111111`
- n=8 `00001011`
- n=9 `111111111`
- n=10 `0101010101`

For period 8 the parent chain is

`00001011 -> 01110111 -> 01010101 -> 11111111 -> 00000000`,

with root-outward connector lengths `1, 3, 19, 369`.  The inherited edges retain exactly the same connector lengths under repetition, matching the naturality theorem.

This sharpens the search strategy: do not seek a statistic monotone on all of `P_n`; unrelated `P_n` components exist outside the root basin.  Test statistics only on the root basin and especially the genuinely new full-period portal trees.  The small census does not conflict with the known period-16 branching; it shows that the small periods through 10 are still path-like.

Full note:

`proofs/informal/problem1_parent_map_root_basin_census.md`

Research commit: `48aa86a1dd6683d3b7b3cceaf99738946cc75c20`

## Status / next target

Problem 1 remains open.  Next run should reconstruct the already-known period-16 root basin / full-period portal vertices from repository artifacts, rewrite those actual edges in `P_16` language, and test local statistics (run count, derivative weight, transition count, exact period) only on this relevant finite set.  Avoid global `P_16` enumeration because long connectors make it expensive and most components are irrelevant.
