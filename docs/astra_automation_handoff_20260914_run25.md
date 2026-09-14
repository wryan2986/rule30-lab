# Astra automation handoff — 2026-09-14 run 25

Branch: `research/astra-next`

## Repository state reviewed

Run started from `061db7f28a40352f2982db3f6860f7c3472d5952` (run 24 handoff). No newer branch work was present.

Run 24 correctly solved the odd-corridor `G>=3` commutator suffix, but its even-corridor Section 3 contained an arithmetic error: a word of bitlength `m-2`, divided by `2^(m-4)`, exposes two leading bits, not three. That error made the claimed penultimate source set `{1,2}` incorrect.

## Corrected and new results

Updated:

`proofs/informal/problem1_even_corridor_terminal_source_sharpening.md`

Commits during this run:

- `bc2e82511168f5f85a4fd60b7eed2d7d8381b860` — correct even-corridor suffix arithmetic;
- `1bb986d9c812ce9e9c938b4340018dbcb189e51e` — identify the source immediately before the forced suffix and the resulting reset dichotomy.

### 1. Long even corridors force a run of source `5`

Let

\[
T^p(z)=2^{2p}z+R,
\qquad m=2p,
\qquad G=m-bitlength(R)=2D,
\qquad D\ge2.
\]

For the first collision `x=T^(D+1)(z)`, put `u_j=A^j(x)` and `s_j=T(u_j)`.

For every `2<=r<=D`, separated return geometry gives

\[
 u_{p-r}
 =2^{2r}T^{D+1-r}(z)
 +
 \left\lfloor
 \frac{T^{D+1-r}(R)}{2^{m-2r}}
 \right\rfloor.
\]

The fringe iterate `T^(D+1-r)(R)` is a nonzero Rule-30 image of bitlength `m+2-2r`. The quotient therefore consists of its top two bits, universally `11`, and is exactly `3`.

Hence

\[
\boxed{u_{p-r}\equiv3\pmod8}
\]

and

\[
\boxed{s_{p-r}\equiv5\pmod8}
\qquad(2\le r\le D).
\]

Thus the terminal source suffix is not in the run-24 Cartesian product. It has the rigid form

\[
\boxed{5^{D-1}(1\text{ or }5)}.
\]

The final source remains

\[
 s_{p-1}=5\quad\text{if }T^D(z)\text{ is even},
\qquad
 s_{p-1}=1\quad\text{if }T^D(z)\text{ is odd}.
\]

### 2. Exact automaton compression over the forced suffix

Source `5` maps reachable commutator states as

\[
0\to1,\qquad1\to0,\qquad3\to1.
\]

After the first `5`, only states `{0,1}` remain, and both terminal symbols `1` and `5` act on `{0,1}` as the same swap `0<->1`.

Writing

\[
h=d_{p-D},
\]

the terminal state is

\[
\boxed{
 d_p=
 \mathbf 1_{h\ne1}\oplus((D-1)\bmod2).
}
\]

In particular,

\[
\boxed{d_p\in\{0,1\}}
\]

for every even corridor `G>=4`; terminal state `3` is impossible.

### 3. The source before the forced suffix is determined by the top two bits of the original fringe

Because `L=bitlength(R)=m-2D` is even and positive, `L>=2`. At `r=D+1`,

\[
 u_{p-D-1}
 =2^{2D+2}z
 +
 \left\lfloor\frac{R}{2^{L-2}}\right\rfloor.
\]

The quotient is exactly the top two bits of `R`. Therefore

\[
\boxed{
 s_{p-D-1}\equiv
 \begin{cases}
 6\pmod8,&R\text{ begins }10,\\
 5\pmod8,&R\text{ begins }11.
 \end{cases}
}
\]

This yields a sharp reset dichotomy.

If `R` begins `10`, source `6` synchronizes the three-state automaton:

\[
\boxed{d_{p-D}=1.}
\]

Consequently

\[
\boxed{
 d_p=
 \begin{cases}
 0,&D\text{ odd},\\
 1,&D\text{ even}.
 \end{cases}
}
\]

and all earlier source history is irrelevant.

If `R` begins `11`, the preceding source is another `5`; this does not fully synchronize. Exactly one binary distinction remains: whether `d_(p-D-1)=1` or not.

## Research significance

The run-24 even-corridor target has been substantially simplified and corrected.

For every long even corridor `G>=4`, the collision source word near the end is

\[
\boxed{(6\text{ or }5),\ 5^{D-1},\ (1\text{ or }5).}
\]

All `10`-leading return fringes synchronize completely. The only local commutator-memory obstruction left for long even corridors is the exceptional case

\[
\boxed{R\text{ begins }11.}
\]

No genuine `G>=4` even-corridor example was found in the earlier exhaustive search up to `z<2,000,000`, so there is currently no small computational witness for either leading-prefix case at this corridor length.

## Best next target

Determine whether a genuine long even return fringe can begin `11`.

Useful routes:

1. combine `R=T^(H+p)(v) mod 2^(2p)` with the zero-corridor/common-origin geometry to constrain the two bits immediately below the corridor;
2. search substantially beyond the previous `z<2,000,000`, `p<=20` range for any genuine even corridor `G>=4`, recording the leading bits of `R`;
3. if `11` is realizable, derive one more pre-suffix condition capable of deciding whether `d_(p-D-1)=1`.

A proof that long even fringes must begin `10` would completely settle the local commutator-memory problem for all even corridors `G>=4`.

## Status

Problem 1 remains open. Run 25 corrects a run-24 arithmetic error and replaces the even-corridor terminal-pair analysis with an exact forced-source suffix and reset dichotomy.
