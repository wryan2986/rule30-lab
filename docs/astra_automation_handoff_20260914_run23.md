# Astra automation handoff — 2026-09-14 run 23

Branch: `research/astra-next`

## Repository state reviewed

Run started from `cb38782a08c5ef448556b5ebd1f6d920e6352021` (run 22 handoff). No newer branch work was present.

The active target from run 22 was to prove or disprove the empirical statement that a genuine first return-fringe boundary collision cannot have terminal source `0 mod 8`, equivalently

\[
A^{p-1}(x)\equiv0\pmod8.
\]

## New result

Added:

`proofs/informal/problem1_genuine_collision_terminal_source_zero_impossible.md`

commit `f96b20f3c3514bb15be20a186702064a89af401a`.

### Exact penultimate-state formula

Let `z` have pure `A`-period `p` with

\[
T^p(z)=2^{2p}z+R,
\]

and define

\[
m=2p,\quad L=bitlength(R),\quad G=m-L>0,\quad D=floor(G/2).
\]

The genuine first boundary-collision row is

\[
x=T^{D+1}(z).
\]

For `u_j=A^j(x)`, corridor separation through physical time `D` gives

\[
\boxed{
 u_{p-1}
 =4T^D(z)+\left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor.
}
\]

This directly exposes the terminal normalized residue from the evolved return fringe.

### Terminal source zero is impossible

Every nonzero finite Rule-30 word gains exactly two bits per physical step.

If `G=2D+1` is odd, then

\[
bitlength(T^D(R))=m-1,
\]

so

\[
\left\lfloor\frac{T^D(R)}{2^{m-2}}\right\rfloor=1
\]

and therefore

\[
\boxed{u_{p-1}\equiv1\text{ or }5\pmod8.}
\]

If `G=2D` is even, then

\[
bitlength(T^D(R))=m,
\]

so the quotient is the top two bits of an `m`-bit word and lies in `{2,3}`. Hence

\[
\boxed{u_{p-1}\pmod8\in\{2,3,6,7\}.}
\]

Thus in every genuine first return-fringe collision,

\[
\boxed{A^{p-1}(x)\not\equiv0\pmod8.}
\]

Since `T(y) == -y (mod 8)`, equivalently

\[
\boxed{s_{p-1}\not\equiv0\pmod8.}
\]

This proves the run-22 empirical exclusion; the 27-case scan was seeing an exact theorem.

### Stronger final-source classification

The terminal source symbol is restricted to

\[
\boxed{s_{p-1}\in\{3,7\}\pmod8}
\]

when `G` is odd, and

\[
\boxed{s_{p-1}\in\{1,2,5,6\}\pmod8}
\]

when `G` is even.

So the identity symbol `0` of the run-21 commutator automaton is geometrically forbidden at the end of every genuine collision history.

The synchronizing source `6` remains possible only in the even-`G` case; it is not yet shown to be forced.

## Research significance

Run 21 showed that unrestricted commutator histories have no universal bounded-suffix description because arbitrarily long suffixes of source `0` preserve all prior state. Run 22 converted such zero suffixes into valuation ladders. This run proves that a genuine return-fringe collision cannot even end in one source-zero step.

Therefore the strongest abstract memory obstruction disappears completely at the actual collision boundary. Any remaining failure of bounded synchronization must use nonzero terminal symbols and genuine collision-compatible source histories.

## Best next target

Classify the transition semigroup near the end using the collision-compatible terminal sets

\[
\{3,7\}\quad(G\text{ odd}),
\qquad
\{1,2,5,6\}\quad(G\text{ even}),
\]

plus the known boundary defect `epsilon` and parity/top-fringe-bit data.

In particular:

1. Compute the automaton transition maps for each allowed terminal symbol and determine which are synchronizing or reduce the possible state set.
2. Pull one or two earlier source symbols directly from the return-fringe geometry, as was done for `s_(p-1)`, to see whether a bounded collision-specific suffix forces synchronization.
3. If a bounded suffix still fails, construct an actual genuine-collision family realizing distinct commutator states with the same collision suffix; do not rely on unrestricted automaton words.

## Status

Problem 1 remains open. The run-22 empirical target is now an exact theorem, and terminal identity-symbol memory is ruled out for genuine boundary collisions.
