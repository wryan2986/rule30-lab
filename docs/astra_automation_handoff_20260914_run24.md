# Astra automation handoff — 2026-09-14 run 24

Branch: `research/astra-next`

## Repository state reviewed

Run started from `6b8b154c5875e79db56fa54a0b67a2d1cecd785a` (run 23 handoff). No newer branch work was present.

Run 23 proved that genuine first return-fringe collisions never end in source `0 mod 8`, and classified the final source as `{3,7}` for odd corridor length and `{1,2,5,6}` for even corridor length.

The active target was to derive one or two earlier collision-source symbols from return-fringe geometry and test whether the collision-specific suffix synchronizes the three-state commutator automaton.

## New results

### 1. Odd corridors `G>=3` have a forced penultimate source and synchronize in two symbols

Added:

`proofs/informal/problem1_odd_corridor_two_symbol_synchronization_and_reentry.md`

commit `78e4090330e214e3edc1f2154bc289b7b2e2d1d2`.

Let

\[
T^p(z)=2^{2p}z+R,
\qquad m=2p,
\qquad G=m-bitlength(R)=2D+1,
\qquad D\ge1.
\]

For the genuine first collision

\[
x=T^{D+1}(z)
\]

and normalized orbit `u_j=A^j(x)`, corridor separation one step earlier gives

\[
\boxed{
 u_{p-2}=16T^{D-1}(z)+1.
}
\]

Hence

\[
\boxed{u_{p-2}\equiv1\pmod8},
\qquad
\boxed{s_{p-2}\equiv7\pmod8}.
\]

Run 23 already gave `s_(p-1) in {3,7}` for odd `G`, so every genuine odd collision with `G>=3` ends in

\[
\boxed{(7,3)\text{ or }(7,7)}.
\]

These two source suffixes synchronize the three-state commutator automaton completely:

\[
\boxed{
 d_p=3\quad\text{if }s_{p-1}=3,
 \qquad
 d_p=1\quad\text{if }s_{p-1}=7.
}
\]

The terminal-state formula simplifies further to

\[
\boxed{
 d_p=1+2\,(T^D(z)\bmod2).
}
\]

Thus the entire length-`p` commutator history collapses to one parity bit of the physical pre-collision row.

For odd `G`, the boundary defect is `E_p(x)=1`. Combining the synchronized `d_p` with the existing exact re-entry classifier and `T(y) == -y (mod 4)` gives

\[
\boxed{
E_p(Tx)=0
\iff
T^D(z)\equiv1\pmod4.
}
\]

So immediate re-entry after every odd corridor `G>=3` is decided exactly by two low bits of the pre-collision physical row.

### 2. Even-corridor final source set shrinks from four symbols to two

Added:

`proofs/informal/problem1_even_corridor_terminal_source_sharpening.md`

commit `fcf956d14f9f55e50e0c7845bd855a4b1c00ef84`.

A universal finite-word fact was used:

> Every nonzero finite Rule-30 image has leading binary bits `11`.

If `G=2D>0`, put `W=T^(D-1)(R)`. Then `bitlength(W)=m-2`, so

\[
\left\lfloor\frac{T(W)}{2^{m-2}}\right\rfloor=3.
\]

Therefore the exact terminal normalized state is

\[
\boxed{
 u_{p-1}=4T^D(z)+3.
}
\]

and hence

\[
\boxed{
 s_{p-1}\equiv
 \begin{cases}
 5\pmod8,&T^D(z)\text{ even},\\
 1\pmod8,&T^D(z)\text{ odd}.
 \end{cases}
}
\]

Thus genuine even collisions terminate only in

\[
\boxed{s_{p-1}\in\{1,5\}\pmod8}.
\]

The previous possibilities `2` and `6` are impossible. In particular, source `6`, although a one-symbol synchronizer of the abstract automaton, is never the final source symbol of any genuine collision.

For longer even corridors `G>=4` (`D>=2`), the same leading-bit argument one step earlier gives

\[
\boxed{s_{p-2}\in\{1,2\}\pmod8}.
\]

So the only possible terminal two-symbol pairs are

\[
\boxed{(1,1),(1,5),(2,1),(2,5)}.
\]

These do not automatically synchronize the abstract three-state automaton, so the odd-corridor proof does not immediately extend.

## Research significance

The bounded-memory question is now resolved positively on the entire odd-corridor side except the short case `G=1`: return-fringe geometry forces a synchronizing two-symbol suffix.

The remaining commutator-memory obstruction has been isolated to:

1. even corridors, especially `G>=4`, with terminal pairs in `{1,2} x {1,5}`;
2. the short odd case `G=1`;
3. global accumulation across successive plateau/collision events after the local commutator state is known.

## Best next target

For even corridors `G=2D>=4`, derive `s_(p-3)` from the top bits of `T^(D-2)(R)` and propagate the exact Rule-30 leading-bit constraints forward. Determine which terminal triples are genuinely realizable, rather than treating `{1,2} x {1,5}` as a free Cartesian product.

A useful success criterion is either:

- show every genuine even-corridor terminal triple synchronizes the commutator; or
- obtain an exact formula for `d_p` in terms of a bounded number of top-fringe bits and low bits of `T^D(z)`.

If even-corridor suffixes remain nonsynchronizing, construct an actual pair of genuine collision states with the same bounded collision suffix but distinct `d_p`; do not use arbitrary automaton words.

## Status

Problem 1 remains open. Run 24 proves exact two-symbol synchronization for all odd corridors `G>=3`, gives a complete immediate-reentry criterion there, and sharply reduces the even-corridor terminal alphabet.
