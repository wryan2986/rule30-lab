# Astra automation handoff — 2026-09-14 run 26

Branch: `research/astra-next`

## Repository state reviewed

Run started from `2ef9461a400de3258401dcf3486bfeceb72e1f01` (run 25 handoff). No newer branch work was present.

Run 25 reduced the long-even-corridor commutator problem to the exceptional case in which the return fringe `R` begins `11`. It suggested proving that such fringes are impossible, or else determining the surviving one-bit history state by additional geometry.

## New result: the exceptional `11` case is real

Added:

`proofs/informal/problem1_even_corridor_prefix11_realizable.md`

and reproducibility script:

`scripts/check_even_corridor_prefix11.py`

Commits during this run:

- `5cf28ad7a4777a62c78126c08a742ce63a3bed0f` — exact `11`-prefix counterexamples and finite-state analysis;
- `6ca89d6ba834795302a13d346eb45edaa2847811` — reproducibility checker.

### 1. First genuine `G=4` witness beyond the old scan

A vectorized direct scan through `z<300,000,000`, exact `A`-period `p<=20`, found

\[
z=3,650,443,
\qquad p=4,
\qquad R=11=1011_2,
\qquad G=4.
\]

Thus long even corridors are genuinely realizable. This witness is in the run-25 synchronizing class because `R` begins `10`.

### 2. Genuine `11`-leading long-even fringes exist at exact period 8

Two small exact witnesses are

\[
\boxed{z_A=7,476,107,372}
\]

with

\[
p=8,
\qquad R_A=3180=110001101100_2,
\qquad G=4,
\]

and

\[
\boxed{z_B=6,723,037,797}
\]

with

\[
p=8,
\qquad R_B=3429=110101100101_2,
\qquad G=4.
\]

Therefore the proposed route "all genuine long even fringes begin `10`" is false.

### 3. Both surviving history branches occur on genuine collisions

For `G=4`, `D=2`. Let `x=T^3(z)` and

\[
d_j=A^j(Tx)\oplus T(A^j x).
\]

For witness A:

\[
(s_0,\ldots,s_7)=(4,5,7,1,4,5,5,5),
\]

\[
(d_0,\ldots,d_8)=(0,0,1,1,0,0,1,0,1),
\]

so

\[
d_{p-D-1}=d_5=0,
\qquad d_p=1.
\]

For witness B:

\[
(s_0,\ldots,s_7)=(5,7,1,4,5,5,5,1),
\]

\[
(d_0,\ldots,d_8)=(0,1,1,0,0,1,0,1,0),
\]

so

\[
d_5=1,
\qquad d_p=0.
\]

Thus the one binary distinction left unresolved in run 25 is not merely an abstract automaton possibility. Both branches occur on genuine exact-period-eight return-fringe collisions with the same `(p,G)=(8,4)` and the same top fringe prefix `11`.

### 4. Finite-type calculation

Because

\[
(Ax)_i=x_{i+2}\oplus(x_{i+1}\lor x_i),
\]

bit `i` of `A^p(x)` depends only on `x_i,...,x_(i+2p)`. Hence `A^p(x)=x` is a one-sided finite-type constraint on overlapping windows of length `2p+1`.

For `p=8`, a 16-bit state graph can therefore decide exactly which low 16-bit words extend upward to finite `A^8`-fixed words.

The computation finds:

- `70` reachable low states with a positive even corridor `G>=4` and return fringe beginning `11`;
- `69` of those yield exact-period-eight finite words;
- realized corridor lengths include `G in {4,6,8,10}`;
- for `G=4`, both values of the run-25 surviving history bit occur repeatedly.

In the shortest-extension classification used in this run, the `G=4` exact-period-eight cases split as

\[
36\text{ with }(d_{p-D-1},d_p)=(1,0),
\]

and

\[
14\text{ with }(d_{p-D-1},d_p)=(0,1).
\]

### 5. Period-four contrast

At `p=4`, all low-byte candidates that would produce a `G=4`, `11`-leading fringe fail the finite-extension test. The only extendable `G=4` low states produce `R=9` or `R=11`, both beginning `10`.

So `11` is forbidden at period four but appears at period eight. A period-independent leading-prefix prohibition cannot be true.

## Research significance

Two run-25 routes are now closed:

1. long even fringes are **not** forced to begin `10`;
2. conditional on prefix `11`, the surviving commutator bit is **not** automatically fixed.

The unresolved bit is genuinely realized by both branches.

## Best next target

Do not spend another run trying to forbid prefix `11` globally.

Better directions:

1. classify the surviving bit against longer prefixes of the full fringe `R` and derive, rather than merely fit, any apparent short-prefix rule;
2. use the finite-type `A^p` graph to search for a collision invariant involving both the low return fringe and the finite high-boundary path;
3. connect realizable `11` collisions directly to the existing FULL/common-origin or residence-growth machinery, bypassing local commutator synchronization if the remaining bit cannot be compressed uniformly.

The finite-state graph is especially useful because it separates local low-fringe admissibility from the finite upper-boundary condition exactly, and already produces explicit witnesses rather than bounded-integer scan artifacts.

## Status

Problem 1 remains open. Run 26 decisively answers the run-25 realizability question: `11`-leading long even return fringes exist, and both values of the residual one-bit commutator history occur on genuine exact-period-eight collisions.
