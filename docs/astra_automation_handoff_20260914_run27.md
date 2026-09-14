# Astra automation handoff — 2026-09-14 run 27

Branch: `research/astra-next`

## Repository state reviewed

Run started from `307eb0e367f3c0fbc5ba23220f1044414e7cc9a4` (run 26 handoff). No newer branch work was present.

Run 26 established that `11`-leading long-even return fringes are genuinely realizable at exact period 8 and that both residual commutator-history branches occur. It proposed classifying the residual bit using a longer portion of `R` and/or a finite upper-boundary path.

## New structural result: the upper-boundary path is not an independent variable

Added:

- `proofs/informal/problem1_return_fringe_determines_periodic_state_and_core_commutator.md`
- `scripts/check_fringe_core_reduction.py`

Commits:

- `c8e0efc60947919fc1e1141fa5a350c8559b2a1e` — exact fringe-determinism/core reduction;
- `356c25b19879cf4b289c03463ecd642d88229072` — reproducibility checker.

### 1. Deterministic extension theorem

Rule 30 is triangular in binary:

\[
(Tx)_i=x_i\oplus(x_{i-1}\lor x_{i-2}).
\]

Hence `T` and every `T^p` are bijections modulo every `2^M`.

Also, iterating preserves the diagonal input bit:

\[
(T^p x)_k=x_k\oplus\Phi_{p,k}(x_0,\ldots,x_{k-1}).
\]

For an `A^p`-fixed configuration, with `m=2p`,

\[
(T^p x)_{i+m}=x_i.
\]

This uniquely solves `x_(i+m)` from lower bits. Therefore the low `2p` bits determine the entire `A^p`-fixed one-sided configuration uniquely.

A low state corresponds to a finite integer iff this deterministic upward extension eventually becomes zero. This explains the run-26 finite-type graph more sharply: every `2p`-bit state has exactly one legal successor; zero-reachability is the only admissibility question.

The checker exhaustively verifies this for every state at `p=1,...,8`.

### 2. The complete return fringe uniquely determines the periodic state

If

\[
T^p(z)=2^{2p}z+R,
\]

then modulo `2^(2p)`,

\[
R\equiv T^p(z).
\]

Since `T^p` is bijective modulo `2^(2p)`, `R` uniquely determines `z mod 2^(2p)`. The deterministic extension theorem then uniquely determines all higher bits.

Thus for fixed `p`, a fringe `R` belongs to at most one `A^p`-fixed configuration.

So the run-26 suggestion to combine the fringe with an independent high-boundary path is unnecessary: that path is already encoded by the full fringe.

### 3. Exact fringe-only reduction of the residual long-even commutator bit

For an even corridor

\[
G=2D\ge4,
\qquad L=\operatorname{bitlength}(R)=2p-G,
\]

put

\[
n=p-D=L/2.
\]

For the collision row `x=T^(D+1)(z)`, reduction modulo `2^L` gives

\[
\boxed{x\equiv T^{1-n}(R)\pmod{2^{2n}}.}
\]

Define

\[
y_R=T^{1-n}(R)\pmod{2^{2n}}.
\]

The commutator state `d_(n-1)` only uses source symbols through index `n-2`; those depend on collision-row bits below position `2n`, so they are determined entirely by `y_R`.

Define the intrinsic fringe-core state

\[
\boxed{C_n(R)=d_{n-1}}
\]

by driving the existing three-state commutator automaton for `n-1` steps from `y_R`.

Then for every genuine collision,

\[
\boxed{d_{p-D-1}=C_n(R).}
\]

For the unresolved `11`-leading case, the run-25 forced source suffix gives the exact final formula

\[
\boxed{d_p=\mathbf 1_{C_n(R)\ne1}\oplus(D\bmod2).}
\]

Thus the entire residual history bit is an intrinsic finite function of the fringe. No reconstruction of the potentially huge periodic word `z` is needed.

For `10`-leading fringes the known synchronizer formula remains

\[
d_p=1\oplus(D\bmod2).
\]

### 4. p=8 finite-state pattern

The checker verifies the fringe-core formula on all 69 exact-period-eight `11`-leading even-corridor states from run 26.

For the 50 cases with `G=4`, there is a particularly simple empirical split:

\[
\boxed{d_8=1\iff R\text{ begins }1100.}
\]

Prefixes `1101`, `1110`, and `1111` all give `d_8=0` in this exact finite-state set.

For the smaller `G=6,8,10` samples, the same `1100` versus other-`11xx` split appears with the parity reversal predicted by the exact formula above. This is evidence only; no universal four-bit-prefix theorem has been proved.

## Research significance

The long-even memory problem is now entirely internal to the return fringe. The finite high-boundary continuation cannot carry an extra independent bit because it is uniquely forced by the low state, and the low state is uniquely recovered from `R`.

This materially narrows the remaining target.

## Best next target

Study the intrinsic fringe-core function `C_n(R)` on admissible return fringes.

Useful directions:

1. test whether the observed `1100`/other-`11xx` split persists at larger exact periods/corridor lengths;
2. derive `C_n(R)` as a finite transducer acting on `T^{1-n}(R)` and determine whether admissibility forces synchronization after bounded fringe depth;
3. if no bounded descriptor exists, connect the fringe-core state directly to FULL/common-origin or residence-growth machinery rather than returning to an independent-boundary-path model.

## Status

Problem 1 remains open. Run 27 removes an unnecessary degree of freedom from the run-26 formulation and gives an exact fringe-only formula for the residual commutator state in every long-even collision.