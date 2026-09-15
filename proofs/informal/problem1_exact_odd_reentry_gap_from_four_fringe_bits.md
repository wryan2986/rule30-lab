# Problem 1: exact odd-corridor re-entry gap from four fringe bits

Status: exact local theorem. This sharpens `problem1_immediate_reentry_collapses_return_corridor.md` from `G'<=1` to an exact `G' in {0,1}` formula for every odd long corridor `G>=3`. Problem 1 remains OPEN; this does not control later period changes or prove a global finite-support contradiction.

## Setup

Keep the notation of the corridor-collapse note:

\[
T^p(z)=2^m z+R,\qquad m=2p,
\]

\[
G=m-\operatorname{bitlength}(R)=2D+1\ge3,
\]

and suppose the first collision immediately re-enters the same `A^p`-fixed set. Then the re-entered return fringe is

\[
R'=T^{D+2}(R)\bmod 2^m.
\]

Define a leading-four-bit flag

\[
H(R)=
\begin{cases}
1,&R\text{ begins }1101,1110,\text{ or }1111,\\
0,&R\text{ begins }1000,1001,1010,1011,\text{ or }1100.
\end{cases}
\]

This is the same flag that appeared in the exact commutator/fringe-core classification.

## 1. The fourth leading bit after two physical steps

For a nonzero finite word `w`, write its relative leading-edge bits as

\[
a_j^{(q)}=(T^q w)_{h+2q-j}.
\]

The already established recurrence is

\[
a_j^{(q+1)}=a_{j-2}^{(q)}\oplus(a_{j-1}^{(q)}\lor a_j^{(q)}).
\]

Let the first four bits of `w` be `1xyz`, so

\[
a_0^{(0)}=1,\quad a_1^{(0)}=x,\quad a_2^{(0)}=y,\quad a_3^{(0)}=z.
\]

A direct two-step evaluation gives

\[
a_3^{(2)}=x\land(y\lor z).
\]

Hence

\[
\boxed{a_3^{(2)}=H(w).}
\]

Indeed this is one exactly for prefixes `1101`, `1110`, and `1111`, and zero for the other five leading-four-bit prefixes.

## 2. Exact parity propagation

For every `q>=2`, the universal leading-edge identities give

\[
a_2^{(q)}=0,
\]

and therefore

\[
a_3^{(q+1)}=1\oplus a_3^{(q)}.
\]

Induction from the two-step value yields

\[
\boxed{a_3^{(q)}=H(w)\oplus((q-2)\bmod2).}
\]

For the transported fringe we use `w=R` and `q=D+2`, so

\[
\boxed{a_3^{(D+2)}=H(R)\oplus(D\bmod2).}
\]

## 3. Exact value of the new corridor gap

Because `R` has bitlength `m-(2D+1)`, the word `T^{D+2}(R)` has bitlength

\[
m+3.
\]

Its highest occupied position is `m+2`. Reduction modulo `2^m` discards relative leading positions `j=0,1,2`. Thus the highest retained candidate, position `m-1`, is exactly `a_3^(D+2)`.

If this bit is one, then `R'` has bitlength `m`, so `G'=0`.

If this bit is zero, the next bit is `a_4^(D+2)`. For `D>=2`, hence `q>=4`, the established leading-edge lemma gives `a_4^(q)=1`. For the only remaining case `D=1`, hence `G=3` and `q=3`, the exact identity

\[
a_3^{(3)}\lor a_4^{(3)}=1
\]

shows that `a_3=0` forces `a_4=1`. Therefore in every odd long corridor, when the highest retained bit vanishes the next retained bit is one and `G'=1` exactly.

Consequently

\[
\boxed{
G'=1\oplus H(R)\oplus(D\bmod2)
}
\]

for every odd `G=2D+1>=3` immediate re-entry.

Equivalently,

\[
\boxed{
G'=0\iff H(R)=1\oplus(D\bmod2),
}
\]

and otherwise `G'=1`.

## 4. Relation to the commutator classification

The same four-prefix flag `H(R)` already controls the residual commutator state in the long-even collision calculation. It is not an unrelated census artifact: both quantities are the same leading-edge bit `a_3^(2)` transported to different normalization boundaries.

Thus two pieces that previously looked separate—terminal commutator behavior and post-reentry corridor size—are manifestations of one four-bit leading-edge invariant.

This does not yet solve the global FULL/common-origin problem. It does remove the last ambiguity inside the odd immediate-reentry output: after a long odd corridor, the next same-period corridor is not merely bounded by one; its exact gap is determined by `D mod 2` and the first four bits of the old return fringe.

## Dependencies

- `problem1_immediate_reentry_collapses_return_corridor.md` for fringe transport and the leading-edge recurrence.
- `problem1_exact_commutator_boundary_formula_and_four_bit_fringe_core.md` for the previously identified four-prefix flag/classification.
