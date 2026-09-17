# Astra automation handoff — run 84

## Main result: explicit inverse endpoint dynamics + primitive-necklace census

No intervening work was present after run 83 (`00fd0b448fb8f5fc9d5fa034967ce45ab99741c0`).

For the off-zero pair map `T(a,b)=(y,a)` with `b = S y XOR (a OR y)`, the inverse is explicit:

`F(u,v) = (v, S u XOR (v OR u))`.

Thus `rho_n^{-1}` can be obtained by starting at diagonal `(a,a)` and iterating `F` until the boundary section `(x,0)` is reached. This identifies `rho_n` as a first-hit matching between boundary and diagonal sections of the reversible pair dynamics.

I also exhaustively enumerated the induced permutation on primitive necklaces for n=2..10. Cycle lengths:

- n=2: 1
- n=3: 1,1
- n=4: 1,2
- n=5: 1,5
- n=6: 1,2,2,4
- n=7: 1,2,6,9
- n=8: 1,1,28
- n=9: 1,5,50
- n=10: 2,5,6,8,9,20,49

The large 28/30 and 50/56 cycles strongly constrain any putative invariant on all primitive necklaces. Weight and parity were also checked and fail generally.

Full note:

`proofs/informal/problem1_endpoint_inverse_and_primitive_necklace_cycle_census.md`

Research commit: `c784294c01b6b01252bee3cf3f9f69ad89e93705`

## Status / next target

Problem 1 remains open. Broad searches for a simple invariant of `rho_n` on all primitive necklaces now look poorly targeted. Next useful work: identify the sparse primitive necklaces that are actual terminating zero-return leaves and study how that subset sits inside the large `rho_n` cycles, or exploit `F` starting from the special diagonal endpoints associated with those leaves.
