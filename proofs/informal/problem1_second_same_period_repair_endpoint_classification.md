# Second same-period repair: exact endpoint classification and a counterexample to short-chain hopes

Status: exact local theorem plus finite-state counterexample. Problem 1 remains open.

## Setup

Let `z` be a finite `A^p`-fixed state with a long return corridor `G>=3`, and suppose its first collision repairs immediately. Let `z'` denote the repaired `A^p`-fixed state and `R'` its return fringe:

\[
T^p(z')=2^{2p}z'+R'.
\]

Runs 30--33 prove that `G'<=1`, so `y=T(z')` is the forced next same-period collision. Moreover its defect is

- `E_p(y)=1` if the original long `G` was odd;
- `E_p(y)=3` if the original long `G` was even.

This note asks exactly when the next row `T(y)=T^2(z')` repairs again.

## Defect update classifiers

For a collision row `y`, write

\[
d_p(y)=A^p(Ty)\oplus T(A^p y).
\]

The exact defect update is

\[
E_p(Ty)=d_p(y)\oplus T(y\oplus E_p(y))\oplus T(y).
\]

A direct three-bit Rule-30 calculation gives:

- if `E_p(y)=1`, then `E_p(Ty)=0` iff `y_1=1` and `d_p(y)=3`;
- if `E_p(y)=3`, then `E_p(Ty)=0` iff `y_2=1`, `y_0 xor y_1=1`, and `d_p(y)=1`.

These are the previously used defect-1 and defect-3 successor classifiers.

## Boundary commutator for the forced short-gap collision

Put `m=2p`. Since

\[
T^p(y)=T(2^m z'+R'),
\]

the run-28 boundary formula shows that `d_p(y)` depends only on the low bit of `z'` and the leading four bits of `R'`. Evaluating the local Rule-30 boundary gives the following exact table.

### `G'=1`

Here `R'` has bitlength `m-1`. In the repaired-odd provenance class `R'` is odd, hence `z'` is odd. For every possible leading-four-bit prefix of `R'`,

\[
\boxed{d_p(y)=3.}
\]

Thus in this case the commutator condition for a second repair is automatic.

### `G'=0`, `R'` odd

Here

\[
\boxed{d_p(y)=3}
\]

iff `R'` begins `1000` or `1001`. For prefixes `1010`, `1011`, or `1100`, `d_p(y)=1`; for `1101`, `1110`, or `1111`, `d_p(y)=0`.

### `G'=0`, `R'` even

Here

\[
\boxed{d_p(y)=1}
\]

iff `R'` begins one of

`1000, 1001, 1010, 1011, 1100`.

For `1101`, `1110`, or `1111`, `d_p(y)=0`.

## Exact second-repair theorem

Rule 30 obeys

\[
T(w)\equiv-w\pmod 8,
\]

and the return identity gives

\[
z'\equiv(-1)^pR'\pmod8.
\]

### Original long corridor odd

Then `R'` is odd and `E_p(y)=1`. Since `y` is odd, the low-bit condition `y_1=1` is equivalent to `y == 3 (mod 4)`, hence to

\[
R'\equiv
\begin{cases}
1\pmod4,&p\text{ even},\\
3\pmod4,&p\text{ odd}.
\end{cases}
\]

Therefore:

- if `G'=1`, a second repair occurs iff the above bottom-two-bit condition holds;
- if `G'=0`, a second repair occurs iff the same bottom-two-bit condition holds **and** `R'` begins `1000` or `1001`.

### Original long corridor even

Then `R'` is even, `G'=0`, and `E_p(y)=3`. Since `y` is even, the low-bit defect-3 condition reduces to `y == 6 (mod 8)`. Hence

\[
R'\equiv
\begin{cases}
2\pmod8,&p\text{ even},\\
6\pmod8,&p\text{ odd}.
\end{cases}
\]

Together with the boundary commutator condition, a second repair occurs iff:

1. `R'` begins `1000`, `1001`, `1010`, `1011`, or `1100`; and
2. `R' mod 8` is `2` for even `p`, or `6` for odd `p`.

Thus the second repair is again a bounded endpoint test. The transported fringe provenance does **not** make it impossible.

## Exact finite-state counterexample to a short repair-chain bound

The exact period-8 finite-extension graph gives many second repairs. Among immediate repairs originating from long corridors, the counts are:

- original `G=3`: second repair occurs in 25 cases and fails in 22;
- original `G=4`: second repair occurs in 5 cases and fails in 2;
- original `G=5`: second repair occurs in 7 cases and fails in 2.

More strongly, the exact-period-8 state

\[
z=32510615916414451519835451338196251
\]

has original corridor

\[
G=3,\qquad R=7707,
\]

and after its first long-corridor repair reaches

\[
z'=2313743162027786261944999351769153349.
\]

Starting at `z'`, membership in the `A^8`-fixed set along successive physical Rule-30 rows begins

`1010101010101010101010101...`

for 25 physical transitions: there are 13 consecutive same-period fixed rows separated by one-step collisions before the chain finally leaves this alternating repair pattern.

Therefore the hoped-for statement that a repaired long corridor can undergo at most one, two, or another tiny universal number of same-period repairs is false. Any global proof must allow substantial short-gap repair trains.

This is a useful dead end: the local collision theory has compressed each repair to bounded endpoint data, but that alone does not bound the length of a same-period repair train.

## Next target

The natural next object is the **two-step return map on repaired short-gap states**. Since a successful forced recollision sends `z'` to `T^2(z')`, derive the exact transformation of its return fringe and endpoint class under this two-step repair. The period-8 witness shows this map can remain admissible for at least 12 iterations. A useful global result would need either:

- a monotone quantity along this two-step map,
- a bound depending explicitly on `p` or fringe width (rather than a universal constant), or
- a connection between each successful repair and the existing common-origin/FULL birth accounting.
