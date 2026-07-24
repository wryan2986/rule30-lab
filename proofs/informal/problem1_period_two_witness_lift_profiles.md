# Period-two witness lift profiles

## Purpose

The existing witness-complexity theorem defines, for phase
`a in {p,u}`, the minimum normalized positive-word length

```text
kappa_a(L)
```

needed to represent the actual zero-survivor residue through `L` bit pairs.
The directed-distance formulation computes this number exactly modulo `4^L`.
This note refines one depth transition into four exact alternatives.

It does not prove that either phase complexity diverges.

## Arithmetic quotient

Let

```text
T(x) = x XOR ((x << 1) OR (x << 2)),
U(x) = T(x) XOR 1,
P(x) = T(x) XOR 1 XOR (2 if x is even else 0).
```

Modulo every power of two, each generator is a permutation. Let `X_L` be the
actual schedule-survivor residue modulo `4^L`. The two normalized phase starts
are

```text
P(0)=3,
U(0)=1.
```

Writing directed positive-generator distance modulo `4^L` as `d_L`, the prior
result gives

```text
kappa_p(L)=1+d_L(3,X_L),
kappa_u(L)=1+d_L(1,X_L).
```

## Four-way lift profile

Fix a base depth `L`. Every residue above `X_L` at depth `L+1` has the unique
form

```text
X_L + r 4^L,  r in {0,1,2,3}.
```

For phase `a`, define the lift profile

```text
Lambda_a(L,r)
```

as the minimum normalized phase-`a` word length whose arithmetic state is this
residue modulo `4^(L+1)`.

Equivalently,

```text
Lambda_p(L,r)=1+d_(L+1)(3, X_L+r4^L),
Lambda_u(L,r)=1+d_(L+1)(1, X_L+r4^L).
```

This is a four-coordinate finite quantity at every depth.

## Projection theorem

For either phase,

```text
min_r Lambda_a(L,r) = kappa_a(L).
```

### Proof

Any word reaching one of the four lifts modulo `4^(L+1)` projects to `X_L`
modulo `4^L`. Therefore every lift coordinate is at least `kappa_a(L)`.

Conversely, take a shortest phase-`a` word reaching `X_L` modulo `4^L`. Its
same ordinary arithmetic state has one definite next pair digit `r`, so it
reaches `X_L+r4^L` modulo `4^(L+1)` with the same word length. Hence one lift
coordinate is at most `kappa_a(L)`.

The two inequalities give equality.

## Actual-coordinate theorem

Let

```text
d_L = floor(X / 4^L) mod 4
```

be the actual next pair digit. Since

```text
X_(L+1)=X_L+d_L 4^L,
```

we have exactly

```text
kappa_a(L+1)=Lambda_a(L,d_L).
```

Thus the transition from depth `L` to `L+1` is read from one coordinate of the
four-way profile.

## Exact plateau and jump criterion

Combining the two theorems gives

```text
kappa_a(L+1)=kappa_a(L)
```

if and only if the actual digit `d_L` is a minimizing coordinate of
`Lambda_a(L,.)`.

More generally, the exact jump is

```text
kappa_a(L+1)-kappa_a(L)
  = Lambda_a(L,d_L)-min_r Lambda_a(L,r).
```

This separates two effects that were conflated in the raw distance table:

1. the cheapest possible lift of the current residue; and
2. the particular lift selected by the zero-initialized Rule 30 fringe.

An infinite proof can therefore target repeated failure of the actual digit to
remain in the minimizing lift set.

## Exact profiles through base depth twelve

Each row lists

```text
L, actual next digit, p-profile, u-profile.
```

```text
 1  1   [ 1,  3,  4,  4]   [ 5,  2,  3,  4]
 2  0   [ 7,  6,  5,  3]   [ 2,  7,  4,  6]
 3  3   [ 7, 10,  7,  8]   [ 2,  6,  9,  7]
 4  2   [ 9,  9,  8, 10]   [10,  9, 12,  7]
 5  1   [11, 12, 14,  8]   [12, 14, 13, 12]
 6  0   [13, 14, 12, 13]   [14, 15, 17, 16]
 7  1   [18, 17, 15, 13]   [14, 14, 18, 20]
 8  1   [20, 17, 20, 20]   [17, 18, 14, 18]
 9  0   [17, 18, 22, 19]   [19, 21, 21, 18]
10  0   [21, 20, 17, 20]   [26, 24, 21, 19]
11  3   [25, 22, 21, 28]   [26, 27, 26, 27]
12  0   [30, 28, 28, 29]   [30, 30, 30, 27]
```

For example, at base depth eleven the cheapest `p` lift has digit `2` and
length `21`, while the actual digit is `3`, forcing length `28`. The exact
seven-letter jump is therefore not caused by projection alone; it is caused by
the actual fringe choosing the most expensive of the four lifts in that row.

## Compact exact bidirectional search

The finite graph at depth `L` has `4^L` vertices, so a full breadth-first scan
is already impractical at depth 22. The C++ campaign uses two exact devices.

### Explicit inverses

Each generator is inverted low-to-high modulo `2^(2L)`. A complete reverse
ball of radius `R` around the target is therefore available without storing
edges.

### Split minimality certificate

Suppose the best forward/reverse intersection gives total normalized length
`D`. Once complete forward layers through depth

```text
D-1-R
```

have been processed, every hypothetical shorter path would split at a vertex
inside the completed reverse ball and would already have produced a smaller
intersection. Hence `D` is exact.

### Compact tables

Open-addressing tables store one 64-bit key per state, plus one byte for reverse
distance. This removes allocator and node overhead from standard hash tables.
The controlled depth-22 campaign stayed below 1 GiB peak resident memory.

## New exact actual values

The compact search extends both phases by two further depths:

```text
L       20  21  22
kappa_p 47  49  51
kappa_u 49  52  52
kappa   47  49  51
```

Depth 22 is another exact `u`-phase plateau, while the `p` phase rises by two.

The controlled search records are:

```text
L=21: reverse states 13,631,511
      p forward states 5,235,201
      u forward states 23,270,776

L=22: reverse states 40,441,421
      p forward states 5,235,201
      u forward states 7,745,997
```

The state counts are operational evidence for reproducibility, not asymptotic
theorems.

## Research consequence

The next infinite target can now be stated more locally:

> Prove that, in each phase, the actual next-pair digit fails to remain a
> minimizing lift digit infinitely often, with cumulative jump penalties
> unbounded.

This is equivalent to divergence but exposes the one-pair decision responsible
for every plateau or jump. A viable proof may couple the minimizing lift set
to the exact `u`-return selector or to a section recurrence of the actual fringe.

## Scientific boundary

The projection theorem, actual-coordinate theorem, and plateau criterion are
all-depth exact statements. The profile table and depth-22 distances are finite
exhaustive computations.

This work does **not** prove that either phase complexity diverges, prove that
the alternating inverse lift has infinite support, exclude eventual center
period two, or solve Rule 30 center nonperiodicity.
