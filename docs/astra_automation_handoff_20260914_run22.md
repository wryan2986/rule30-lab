# Astra automation handoff — 2026-09-14 run 22

Branch: `research/astra-next`

## Repository state reviewed

Run started from `a84acee9694084de201c9147aad66a0980c6056c` (run 21 handoff). No newer branch work was present.

The active question was whether genuine return-fringe collision histories can have long terminal source-`0 mod 8` runs, which are the exact memory-preserving obstruction for the three-state commutator automaton.

## New result

Added:

`proofs/informal/problem1_terminal_zero_source_valuation_ladder.md`

commit `f1be2542bf0a0884b8d49317f8aba3ae4b56bb21`.

### Exact residue identity

For normalized packed Rule 30,

\[
T(x)\equiv -x\pmod8.
\]

Therefore the commutator source symbol is simply

\[
s_j\equiv-u_j\pmod8,
\]

where `u_j=A^j(x)`.

In particular:

- source `0 mod 8` iff `u_j == 0 mod 8`;
- synchronizing source `6 mod 8` iff `u_j == 2 mod 8`.

### Zero-source runs are valuation ladders

Rule 30 preserves 2-adic valuation. Hence on a zero-source step,

\[
v_2(u_{j+1})=v_2(u_j)-2.
\]

A consecutive block of `k` zero source symbols beginning at `u_m` occurs iff

\[
u_m=4^k r
\]

for an even nonzero finite word `r`; then exactly

\[
u_{m+k}=T^k(r).
\]

Thus a memory-preserving zero suffix is not an arbitrary automaton phenomenon: it is an exact hidden physical Rule-30 evolution beneath `k` factors of four.

The endpoint obeys

\[
2k+2\le bitlength(u_{m+k}).
\]

### Boundary-collision specialization

For a genuine first boundary collision,

\[
A^p(x)=x\oplus\varepsilon,\qquad\varepsilon\in\{1,3\}.
\]

A terminal length-`k` source-zero suffix would force

\[
x\oplus\varepsilon=T^k(r)
\]

for an even finite word `r`, while `x` itself is a positive physical descendant of the periodic return state. This converts long suffix memory into a finite-common-ancestry question for the neighboring rows `x` and `x xor epsilon`.

### Computational evidence

Exhaustively scanned `1 <= z < 2,000,000` for exact pure `A`-period `p <= 20`, positive return fringe and positive corridor. There were 27 genuine first boundary collisions (periods 1, 2, and 4 in the scanned range).

None had even one terminal source-zero symbol:

\[
s_{p-1}\not\equiv0\pmod8
\]

in all 27 cases.

This is not true for arbitrary near-return states, so the observed exclusion appears tied to genuine return-fringe collision geometry rather than merely the equation `A^p(x)=x xor 1/3`.

## Best next target

Prove or disprove the empirical statement:

> A genuine first return-fringe boundary collision never has `A^(p-1)(x) == 0 (mod 8)`.

A promising route is to combine the forced finite ancestry

\[
x\oplus\varepsilon=T(r)
\]

with the explicit fact that `x=T^(D+1)(z)` for the periodic return state `z`. If terminal zero is impossible, the strongest memory obstruction from run 21 disappears for genuine collisions; then classify the remaining terminal source symbols and their transition semigroup for a bounded synchronization result.

## Status

Problem 1 remains open. This run converted terminal zero-source memory into exact 2-adic/physical ancestry and found a strong collision-specific empirical exclusion worth targeting next.
