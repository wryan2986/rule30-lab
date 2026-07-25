# Exact transport of period-two phase-minimizer plateaus

Status: complete all-depth derivation of the fixed-complexity transport law,
plus finite exhaustive evidence through phase complexity 25 that three
consecutive zero return penalties do not occur. The finite census is not an
all-depth exclusion.

## 1. Phase cylinders and minimizers

For phase `a in {p,u}`, let `O_(a,k)` be the set of ordinary arithmetic outputs
of exact phase complexity `k`. For a depth `L` survivor residue `X`, define

\[
C_{a,k}(X,L)=\{x\in O_{a,k}:x\equiv X\pmod{4^L}\}.
\]

The phase complexity and complete minimizer set are

\[
\kappa_a(X,L)=\min\{k:C_{a,k}(X,L)\ne\varnothing\},
\]

and

\[
M_a(X,L)=C_{a,\kappa_a(X,L)}(X,L).
\]

The earlier residual-frontier theorem computes these finite sets exactly.

## 2. One extension block

Suppose a deeper cylinder extends `X` by `r` base-four digits:

\[
X'=X+4^L c,
\qquad 0\le c<4^r.
\]

Every state in the old cylinder has a unique decomposition

\[
x=X+4^Lh,
\qquad h=x\mathbin{\gg}2L.
\]

The state lies in the deeper cylinder exactly when

\[
h\equiv c\pmod{4^r}.
\]

Therefore the exact same-complexity intersection is

\[
\boxed{
C_{a,k}(X',L+r)
=
\left\{
 x\in C_{a,k}(X,L):
 (x\mathbin{\gg}2L)\bmod4^r=c
\right\}.
}
\]

No phase-frontier search at a new complexity is needed. This is an arithmetic
identity between nested cylinders.

For a surviving state, write `h=c+4^r h'`. Its new residual coordinate is

\[
\boxed{
h'=h\mathbin{\gg}2r=x\mathbin{\gg}2(L+r).}
\]

Thus a block acts on residual minimizers by:

1. test the next `r` base-four digits against `c`;
2. discard every mismatch;
3. shift the consumed block away.

## 3. Exact zero-penalty criterion

Let

\[
k=\kappa_a(X,L).
\]

Monotonicity gives

\[
\kappa_a(X',L+r)\ge k.
\]

The inequality is an equality exactly when the fixed-complexity filtered set is
nonempty:

\[
\boxed{
\kappa_a(X',L+r)=k
\iff
\exists x\in M_a(X,L)
\text{ with }
(x\mathbin{\gg}2L)\bmod4^r=c.
}
\]

When equality holds, the complete new minimizer set is precisely

\[
\boxed{
M_a(X',L+r)
=
\left\{
 x\in M_a(X,L):
 (x\mathbin{\gg}2L)\bmod4^r=c
\right\}.
}
\]

This proves that a zero-penalty plateau is a finite survival process on the
current minimizer set. A positive penalty occurs as soon as the set becomes
empty.

## 4. Several consecutive return blocks

Let successive nested cylinders append blocks

\[
(c_0,r_0),(c_1,r_1),\ldots,(c_{J-1},r_{J-1}).
\]

Starting from a residual minimizer `h`, the complete zero-penalty path exists
exactly when its low base-four digits are the concatenation of those blocks.
After `J` blocks, the residual is

\[
h\mathbin{\gg}2(r_0+\cdots+r_{J-1}).
\]

Consequently, once a minimizer set is known at one return, the maximum length of
its current zero-penalty plateau can be determined by direct digit comparison.
The calculation does not require discovering the next higher-complexity
minimizers.

This statement does not provide a universal plateau bound, because the starting
minimizer set and its residual widths can grow with depth.

## 5. Actual zero-initialized return transitions

The exact actual return depths through fourteen are

```text
1, 5, 7, 12, 14
```

with gaps

```text
4, 2, 5, 2.
```

Using the complete minimizer sets from the residual-cylinder algorithm, both
phases have zero surviving current minimizers across every one of these four
actual return blocks:

```text
transition   phase p survivors   phase u survivors
1 -> 5                0                   0
5 -> 7                0                   0
7 -> 12               0                   0
12 -> 14              0                   0
```

This recovers the known strictly positive penalties without searching the
higher target complexity. It is finite evidence along the actual orbit.

## 6. The complexity-25 counterexample under transport

The known phase-`u` state

```text
x = 0x1bcd3a7b3fdfb
```

is the unique minimum-complexity state in the nested depth-12, depth-14, and
depth-16 cylinders associated with

```text
tutututttutu
tutututttututu
tutututttutututu
```

The transport theorem gives survivor counts

```text
12 -> 14: 1
14 -> 16: 1
```

so the two consecutive return penalties vanish.

Its complete forced zero schedule is instead

```text
tutututttutututt
```

The depth-16 cylinder does not see branch index 15. The required branch at that
index is `u`, but the state forces `t`. Therefore it cannot continue to a third
zero return penalty. This identifies exactly where the finite counterexample
expires.

## 7. Complete complexity-25 census

For a base prefix that first appears at phase complexity `k`, an `n`-return
zero-penalty candidate must force

\[
u t^{r_0-1}u t^{r_1-1}\cdots u t^{r_{n-1}-1}
\]

while the final `u` at the next return remains invisible at the deepest
cylinder. The complete word including that final branch is also required to
avoid the proved factors

```text
uu
ttttt
ututtu
```

The independent C++ analyzer exhausts every ordinary phase output through
complexity 25:

```text
phase-p outputs:              9,118,715
phase-u outputs:              7,745,997
total outputs:               16,864,712
eligible outputs mod 4 = 3:   4,831,012
```

The exact candidate totals are

```text
two-return zero candidates:    1
three-return zero candidates:  0
```

The unique two-return candidate is the state above, at phase `u`, complexity 25,
cut 11, with return gaps `(2,2)`.

The absence of three-return candidates is a finite exhaustive theorem through
complexity 25. It is not promoted to all complexities.

## 8. Validation

The Python reference campaign verifies:

- 4,788 direct nested-cylinder transport identities;
- the four actual return transitions through depth 14;
- both exact surviving transports of the known counterexample;
- the counterexample's failure at the third required return;
- seven focused regression tests.

Certificates:

```text
Python default K=16:
5c4f5cb9aee833a4d698630643466e75fcc6806d258746baa5c4c81eaa7a26c1

Python full K=20:
72f2443243df0a9485ab54a314e33862139786e5a939d694923f4d309550b328

C++ K=25 output SHA256:
6ef14b494ac4435f01ae4243ad16918efd663cd10f1b43e225fbb8e5555a9439
```

The controlled C++ run completed in about 2.5 seconds with peak resident memory
about 289 MiB.

## 9. Scientific boundary

The plateau-transport theorem is all-depth exact. The complexity-25 census and
the actual depth-14 table are finite.

This result does **not** prove that three consecutive zero return penalties are
impossible at every complexity. It therefore does not yet prove phase-complexity
divergence, exclude eventual center period two, or solve Rule 30 center
nonperiodicity.

The next target is to combine the recursive phase-frontier lift rule with the
transport filter and prove that every putative three-return candidate has a
lower-complexity ancestor in its base cylinder. Such an all-depth theorem would
imply that every three consecutive returns contain a positive penalty and would
finish the period-two complexity path.
