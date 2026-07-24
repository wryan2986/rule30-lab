# Period-two canonical arithmetic relations

Status: complete informal proof of the three conditional arithmetic identities,
the terminating canonical reduction, the six-state automaton, its growth rate,
and the resulting improved almost-sure witness-complexity bound. These are
partial structural results. They do not prove divergence for the actual
zero-initialized fringe schedule and do not solve Rule 30 center
nonperiodicity.

## 1. Arithmetic witness states

For a normalized inverse word `G`, write

```text
x(G)=G^(-1)(0).
```

The forward arithmetic generators are

```text
T(x)=x XOR ((x<<1) OR (x<<2)),
t(x)=T(x),
u(x)=T(x) XOR 1,
p(x)=T(x) XOR 1 XOR (2 when x is even, else 0).
```

Words act from left to right in this note. Thus `up(x)` means `p(u(x))`.
A normalized word begins with phase `p` or `u`, producing initial arithmetic
state `3` or `1`, respectively.

The previous arithmetic quotient used only the immediate collision

```text
p(x)=u(x) when x is odd.
```

Two more exact relations appear after retaining the state modulo four.

## 2. One-bit perturbation lemma

Suppose the second-lowest bit of `y` is one. Then

```text
T(y XOR 1)=T(y) XOR 3.                           (1)
```

Indeed, toggling input bit zero changes output bit zero directly. It also
changes output bit one, whose formula is

```text
y_1 XOR y_0.
```

Output bit two is unchanged because its nonlinear input contains
`y_1 OR y_0`, and `y_1=1`. Higher output bits do not depend on input bit zero.
Therefore precisely output bits zero and one flip, proving (1).

## 3. Three conditional identities

### 3.1 Odd collision

For odd `x`, the extra bit-one correction in `p` vanishes, so

```text
p(x)=u(x).                                        (2)
```

### 3.2 The residue-one relation

Assume `x=1 mod 4` and put `y=T(x)`. The two low bits of `y` are `11`, so
`y=3 mod 4`. Since `x` is odd,

```text
u(x)=y XOR 1,
```

which is even. Hence

```text
p(u(x))
  = T(y XOR 1) XOR 3
  = T(y)
  = t(t(x)),
```

where the middle equality is (1). Therefore

```text
up(x)=tt(x) when x=1 mod 4.                       (3)
```

### 3.3 The residue-two relation

Assume `x=2 mod 4` and again put `y=T(x)`. Then `y=2 mod 4`, so its bit one is
one and it is even. We have

```text
u(x)=y XOR 1.
```

Using (1),

```text
t(u(x))
  = T(y XOR 1)
  = T(y) XOR 3
  = p(y)
  = p(t(x)).
```

Thus

```text
ut(x)=tp(x) when x=2 mod 4.                       (4)
```

Equations (2)-(4) are identities for every ordinary nonnegative integer in the
stated residue class; they are not bounded computational observations.

## 4. Terminating canonical reduction

Order the alphabet by

```text
t < u < p.
```

Scan a word from left to right while carrying its exact arithmetic prefix
state. Apply any available rewrite:

```text
p  -> u   when the prefix state is odd,
up -> tt  when the prefix state is 1 mod 4,
ut -> tp  when the prefix state is 2 mod 4.        (5)
```

Each rule:

1. preserves word length;
2. preserves the arithmetic state after the replaced segment by (2), (3), or
   (4);
3. therefore preserves the action of the untouched suffix;
4. strictly decreases the full word lexicographically.

There are finitely many words of any fixed length. Repeated reduction therefore
terminates. The final word represents the same arithmetic state and contains
none of the state-conditioned forbidden patterns in (5).

Confluence is unnecessary. We need only the existence of at least one
irreducible representative for every arithmetic state.

## 5. Six-state canonical automaton

To recognize irreducible continuations, retain:

- the current arithmetic residue modulo four;
- whether the preceding letter started one of the forbidden two-letter
  patterns.

Use pending value zero for no restriction, one to forbid `p` next, and two to
forbid `t` next. Starting from either phase, only six states are reachable:

```text
A=(0,0), B=(1,0), C=(2,0), D=(2,1), E=(3,0), F=(3,2).
```

The transitions are

```text
A: t->A, u->B, p->E
B: t->E, u->D
C: t->C, p->B, u->F
D: t->C, u->F
E: t->B, u->A
F: u->A.
```

For example, `B --u--> D` records that a word starting `up` at residue one is
forbidden. Similarly, `C --u--> F` records that `ut` at residue two is
forbidden. At odd residues, `p` is absent because of (2).

In state order `(A,B,C,D,E,F)`, the adjacency matrix is

```text
M = [1 1 0 0 1 0
     0 0 0 1 1 0
     0 1 1 0 0 1
     0 0 1 0 0 1
     1 1 0 0 0 0
     1 0 0 0 0 0].                               (6)
```

Phase `p` starts at `E`; phase `u` starts at `B`.

## 6. Growth root

Direct determinant expansion gives

```text
det(lambda I-M)
  = lambda^3 (lambda^3-2 lambda^2-lambda+1).      (7)
```

Let `lambda_*` be the largest real root of

```text
lambda^3-2 lambda^2-lambda+1=0.
```

Numerically,

```text
lambda_* = 2.246979603717466...
```

It is strictly smaller than the prior Pell root

```text
1+sqrt(2)=2.414213562373095...
```

For a fixed phase, the number of accepted normalized words of length `N` is

```text
e_phase M^(N-1) 1,
```

and is therefore `O(lambda_*^N)`. Every distinct arithmetic state has at least
one accepted representative, so the same expression is an upper bound for the
number of distinct exact-length arithmetic states. Summing over lengths does
not change the exponential rate.

## 7. Improved schedule counting

For a fixed phase and depth, one arithmetic state determines one dual zero
boundary target. The future-driver-to-boundary prefix code is injective.
Consequently, for some phase-dependent constant `C`,

```text
#{driver prefixes with kappa_a(q,L)<=N}
  <= C lambda_*^N.                                (8)
```

This is stronger than both previous bounds:

```text
raw words:      O(3^N),
parity/Pell:    O((1+sqrt(2))^N),
canonical mod4: O(lambda_*^N).
```

## 8. Almost-sure witness-complexity rate

Under fair Bernoulli measure, there are `2^(L-1)` future driver prefixes of the
relevant length. Fix

```text
c < log(2)/log(lambda_*).
```

Applying (8) with `N=floor(cL)` gives an exponentially summable upper bound on

```text
P[kappa_a(q,L)<=cL].
```

Borel-Cantelli therefore yields

```text
liminf_(L->infinity) kappa_a(q,L)/L
  >= log(2)/log(lambda_*)
  = 0.856173891675966...                          (9)
```

for either phase and for Bernoulli-almost every schedule.

This improves the Pell-quotient value

```text
0.786439701357394...
```

and the original raw-word value

```text
0.630929753571457...
```

## 9. Bounded campaign

The accompanying analyzer:

```text
experiments/problem1_nonperiodicity/
    analyze_period_two_canonical_relations.py
```

checks the three identities on 65,536 ordinary states, reduces every normalized
word through length nine, constructs the automaton matrix, and compares exact
arithmetic-image counts with its bound through length eighteen.

The default campaign reduces 19,682 normalized words. At exact length eighteen,
it records:

```text
phase p: 75,905 distinct states <= 928,607 canonical words,
phase u: 64,247 distinct states <= 744,685 canonical words.
```

These counts validate the implementation. The identities, termination, matrix,
and asymptotic counting theorem are all-width arguments.

## 10. Scientific boundary

This result is still generic. It proves that arithmetic witnesses occupy a
smaller regular language than the Pell parity quotient suggests, but it does
not distinguish the one zero-initialized Rule 30 fringe schedule from the
exceptional null set that may have bounded complexity.

The remaining target is unchanged:

```text
kappa_p(q_actual,L) -> infinity,
kappa_u(q_actual,L) -> infinity.
```

A useful continuation must either find more state-conditioned relations whose
canonical growth tends toward the exact arithmetic-image growth, or couple the
actual fringe return orbit to a recurring valuation obstruction. No finite
campaign alone proves the required divergence.
