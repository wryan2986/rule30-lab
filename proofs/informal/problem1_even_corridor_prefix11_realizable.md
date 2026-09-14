# Problem 1: `11`-leading long even return fringes are realizable

Status: exact counterexamples plus finite-state computational classification. Problem 1 remains open.

## 1. Question left by run 25

For a pure `A`-periodic state `z`, write

\[
T^p(z)=2^{2p}z+R,
\qquad
G=2p-\operatorname{bitlength}(R).
\]

Run 25 proved that when `G=2D>=4`, the first return-fringe collision has a forced commutator-source suffix

\[
(6\text{ or }5),\;5^{D-1},\;(1\text{ or }5),
\]

where the first symbol is `6` if `R` begins in binary `10` and `5` if `R` begins `11`.

The `10` case synchronizes the three-state commutator automaton. The remaining question was whether a genuine long even return fringe can begin `11` at all.

It can.

## 2. First small long-even witness: the `10` class is nonempty

A direct scan of all

\[
1\le z<300,000,000
\]

for exact `A`-period `p<=20` found one genuine state with even corridor `G>=4`:

\[
\boxed{z=3,650,443}.
\]

It has exact period

\[
\boxed{p=4}
\]

and

\[
T^4(z)=2^8z+11.
\]

Hence

\[
R=11=1011_2,
\qquad
\operatorname{bitlength}(R)=4,
\qquad
\boxed{G=8-4=4}.
\]

Thus genuine long even corridors are not vacuous. This first witness lies in the synchronizing `10`-prefix class.

Its `A`-cycle is

\[
3,650,443\to3,282,733\to3,644,020\to3,291,619\to3,650,443.
\]

The four phase return fringes are respectively

\[
11,\ 77,\ 244,\ 195,
\]

so the length-four corridor occurs only at the first phase.

## 3. Exact `11`-prefix counterexamples at period 8

The exceptional geometry from run 25 is genuinely realizable already at exact period eight.

### Witness A

Take

\[
\boxed{z_A=7,476,107,372}.
\]

Direct iteration gives exact `A`-period

\[
\boxed{p=8}
\]

and

\[
T^8(z_A)=2^{16}z_A+3180.
\]

The fringe is

\[
R_A=3180=110001101100_2.
\]

Therefore

\[
\operatorname{bitlength}(R_A)=12,
\qquad
\boxed{G=16-12=4},
\]

and `R_A` begins `11`.

### Witness B

Take

\[
\boxed{z_B=6,723,037,797}.
\]

Again the exact `A`-period is

\[
\boxed{p=8},
\]

with

\[
T^8(z_B)=2^{16}z_B+3429.
\]

Here

\[
R_B=3429=110101100101_2,
\]

so again

\[
\boxed{G=4}
\]

and the return fringe begins `11`.

Thus the proposed route "prove every genuine long even fringe begins `10`" is false.

## 4. Both surviving commutator-history branches occur

The counterexample is stronger than mere realizability of the `11` prefix.

For `G=4` we have `D=2`, and the first collision is

\[
x=T^{D+1}(z)=T^3(z).
\]

Put

\[
u_j=A^j(x),
\qquad
s_j=T(u_j)\bmod8,
\]

and

\[
d_j=A^j(Tx)\oplus T(A^j x).
\]

Run 25 showed that when `R` begins `11`, exactly one binary distinction survives into the forced terminal `5` suffix: whether

\[
d_{p-D-1}=1
\]

or not.

Both possibilities actually occur among genuine exact-period-eight collisions.

### Witness A: non-`1` branch

For `z_A=7,476,107,372`, the source residues are

\[
\boxed{(4,5,7,1,4,5,5,5)}
\]

and the commutator states are

\[
\boxed{(0,0,1,1,0,0,1,0,1)}.
\]

Since `p-D-1=5`,

\[
\boxed{d_5=0},
\qquad
\boxed{d_8=1}.
\]

The boundary defect is

\[
E_8(x)=A^8(x)\oplus x=3.
\]

### Witness B: `1` branch

For `z_B=6,723,037,797`, the source residues are

\[
\boxed{(5,7,1,4,5,5,5,1)}
\]

and the commutator states are

\[
\boxed{(0,1,1,0,0,1,0,1,0)}.
\]

Thus

\[
\boxed{d_5=1},
\qquad
\boxed{d_8=0}.
\]

The boundary defect is

\[
E_8(x)=1.
\]

Hence the single history bit left unresolved by run 25 is not an artifact of an overlarge abstract state space: both values occur on genuine return-fringe collision states with the same `(p,G)=(8,4)` and the same leading fringe prefix `11`.

Consequently neither

1. the fact that the fringe begins `11`, nor
2. the pair `(p,G)` together with that prefix

is sufficient to determine the terminal commutator state.

## 5. Finite-state extension computation

The period-eight examples were found by exploiting the one-sided locality of `A`.

The bit rule for normalized Rule 30 is

\[
(Ax)_i=x_{i+2}\oplus(x_{i+1}\lor x_i).
\]

Therefore bit `i` of `A^p(x)` depends only on bits

\[
x_i,\ldots,x_{i+2p}.
\]

For fixed `p`, the equation

\[
A^p(x)=x
\]

is therefore a finite-type constraint on overlapping windows of length `2p+1`.

For `p=8`, use a 16-bit state consisting of bits

\[
(x_i,\ldots,x_{i+15}).
\]

Append a candidate bit `b=x_{i+16}`. The transition is legal exactly when bit zero of `A^8` applied to that 17-bit block equals `x_i`. Shift right by one bit to obtain the next 16-bit state. A finite `A^8`-fixed word exists with a prescribed low 16-bit state exactly when that state has a directed path to the all-zero state.

Among the reachable low states, the `p=8` finite-state computation finds `70` states whose associated return fringe has

- positive even corridor `G>=4`, and
- leading fringe bits `11`.

Of these, `69` have exact period eight rather than a proper divisor.

The exact-period-eight cases include corridor lengths

\[
G\in\{4,6,8,10\}.
\]

For `G=4` alone, both unresolved history branches occur repeatedly. In the shortest-extension sample used in this run, the classifications were

\[
36\text{ cases with }d_{p-D-1}=1,\ d_p=0,
\]

and

\[
14\text{ cases with }d_{p-D-1}=0,\ d_p=1.
\]

So the two explicit witnesses above reflect a broad period-eight phenomenon, not isolated arithmetic accidents.

## 6. A period-four contrast

The same finite-state calculation gives a useful contrast at `p=4`.

There are four low-byte residues whose four-step return fringe would have bitlength four and begin `11`:

\[
109,\ 110,\ 140,\ 159\pmod{256}.
\]

None can extend to a finite `A^4`-fixed word.

The only low-byte states extendable to finite `A^4`-fixed words with `G=4` give return fringes

\[
R=9\quad\text{or}\quad R=11,
\]

both beginning `10`.

Thus `11` is genuinely forbidden at period four but becomes realizable at period eight. Any structural proof must therefore explain a period-dependent transition; a period-independent leading-bit prohibition cannot work.

## 7. Research consequence

Run 25's remaining dichotomy is now resolved negatively:

\[
\boxed{\text{genuine long even return fringes can begin }11.}
\]

Moreover, the one-bit commutator-memory obstruction in that branch is genuine:

\[
\boxed{d_{p-D-1}=0\text{ and }1\text{ both occur.}}
\]

This closes off two tempting routes:

1. proving all long even fringes begin `10`;
2. hoping the `11` prefix itself nevertheless forces the surviving commutator bit.

The next viable target is more refined. One must either

- identify additional collision geometry, beyond `(p,G)` and the top two fringe bits, that controls the surviving bit; or
- bypass local commutator synchronization and connect these realizable `11` collisions directly to the existing FULL/common-origin or residence-growth machinery.

A useful computational subtarget is to classify the surviving bit against longer prefixes of `R` and against the physical common-origin data, while treating any apparent short-prefix rule only as experimental evidence until it is derived from the collision geometry.
