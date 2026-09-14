# Astra automation handoff — 2026-09-14 run 28

Branch: `research/astra-next`

## Repository state reviewed

Run started from `6a5698ad710deb547a36bb9d9683029f7ed4c904` (run 27 handoff). No newer branch work was present.

Run 27 reduced the long-even residual commutator state to an intrinsic fringe-core function `C_n(R)` and observed empirically at period 8 that `1100`-leading fringes behaved differently from `1101/1110/1111`.

## New exact result: the commutator is a local moving-boundary defect

Added:

- `proofs/informal/problem1_exact_commutator_boundary_formula_and_four_bit_fringe_core.md`
- `scripts/check_exact_commutator_boundary_formula.py`

Commits:

- `b83c0f58ae11997925ca44de28efb8f9080b5dfd` — exact quotient/commutator theorem and four-bit fringe-core classification;
- `1f052c60b3a95249fdb3d6d5453b1dba1d1269dd` — exhaustive checker.

### 1. One-step quotient commutator

For every `Y>=0` and `h>=2`,

\[
\boxed{
(T(Y)\gg h)\oplus T(Y\gg h)
=c((Y\gg(h-2))\bmod8),
}
\]

where

\[
c(s)=(s_0\lor s_1)+2(s_1\land\neg s_2).
\]

Only the two quotient bits immediately above the cut can differ, so the discrepancy is always in `{0,1,3}`.

### 2. Normalized iterates are physical iterates followed by one final quotient

The quotient error is `<4`, hence disappears after the next normalization shift. Inductively,

\[
\boxed{A^k(x)=T^k(x)\gg2k.}
\]

This is useful independently of the current fringe problem.

### 3. Closed form for the entire `k`-step commutator

For

\[
d_k(x)=A^k(Tx)\oplus T(A^k x),
\]

putting `Y=T^k(x)` in the quotient identity gives

\[
\boxed{
d_k(x)=c((T^k(x)\gg(2k-2))\bmod8).}
\]

Thus the three-state automaton from runs 20-27 is only a streaming representation of three physical bits at the moving normalization boundary. There is no genuine long commutator memory.

### 4. Exact fringe-core theorem

For an even-length fringe

\[
L=\operatorname{bitlength}(R)=2n\ge4,
\]

the run-27 preimage satisfies

\[
T^{n-1}(y_R)\equiv R\pmod{2^{2n}}.
\]

Applying the closed commutator formula at `k=n-1` reads physical bit positions `2n-4,2n-3,2n-2`, which are inside this modulus. Therefore

\[
\boxed{
C_n(R)=c((R\gg(2n-4))\bmod8).
}
\]

So `C_n(R)` depends only on the top four bits of `R`, for every even fringe length and without any admissibility assumption.

Complete table:

- `1000 -> 0`
- `1001 -> 1`
- `1010 -> 3`
- `1011 -> 3`
- `1100 -> 0`
- `1101 -> 1`
- `1110 -> 1`
- `1111 -> 1`

In particular, the period-8 empirical split from run 27 is universal:

\[
\boxed{C_n(R)=0\iff R\text{ begins }1100}
\]

inside the `11`-leading class, and all other `11xx` prefixes give `C_n(R)=1`.

### 5. Long-even collision classification is now bounded

For `G=2D>=4`, previous work gave

\[
d_p=\mathbf1_{C_n(R)\ne1}\oplus(D\bmod2)
\]

in the `11` case, and `d_p=1\oplus(D\bmod2)` in the `10` case.

Substitution yields:

\[
\boxed{
R\text{ begins }10xx\text{ or }1100
\implies d_p=1\oplus(D\bmod2),
}
\]

while

\[
\boxed{
R\text{ begins }1101,1110,1111
\implies d_p=D\bmod2.
}
\]

Therefore the long-even commutator contribution is completely determined by `D mod 2` and the leading four fringe bits. The deeper-fringe-memory route is closed.

## Verification

The checker independently verifies:

1. the quotient identity exhaustively for `Y<2^14` and `2<=h<=12`;
2. `A^k(x)=T^k(x)>>2k` for `x<2^12`, `k<8`;
3. the closed commutator formula over the same range;
4. the four-bit fringe-core formula for every fringe of even bitlength `4,6,...,18`.

These checks are redundant with the proofs but useful for regression/reproducibility.

## Research significance

The local commutator-memory obstruction developed over runs 20-27 is now completely resolved. The residual state never needed unbounded source history: it is exactly a three-bit physical boundary function.

The next useful target should return to the global Problem-1 obstruction. Feed the explicit odd/even collision classes into the existing immediate-reentry, FULL/common-origin, and residence-growth machinery. In particular, determine whether each bounded collision class either:

1. forces immediate re-entry with a classifiable low-bit condition;
2. forces a non-reusable front/residence event; or
3. can recur indefinitely, in which case construct an explicit recurring counterexample family to that proof route.

## Status

Problem 1 remains open. Run 28 completely closes the residual commutator-history subproblem and replaces it by a bounded local classification.