# Residual-frontier factorization of period-two phase cylinders

Status: exact all-depth factorization and exact finite minimization campaign. The
factorization applies to every phase, complexity, depth, and survivor residue.
The numerical phase-complexity table remains finite through depth sixteen.

## 1. Phase frontiers and cylinders

For a phase `a in {p,u}`, let `O_(a,k)` be the set of distinct ordinary
arithmetic outputs at exact normalized complexity `k`. The established
bit-length law is

```text
bitlen(x)=2k     for x in O_(p,k),
bitlen(x)=2k-1   for x in O_(u,k).
```

Fix a depth `L>=1` and a residue

```text
0 <= X < 4^L.
```

Define the exact phase-cylinder intersection

```text
C_(a,k)(X,L)
  = {x in O_(a,k) : x = X mod 4^L}.
```

The phase complexity of the cylinder is the least `k` for which this set is
nonempty.

For an actual schedule prefix of length `L`, `X` is its zero-survivor residue
modulo `4^L`. The same definition also applies to arbitrary schedule cylinders,
including the generic counterexample cylinders from the pre-branch analysis.

## 2. Residual-frontier factorization

Assume first that `k>L`. Every `x` in the cylinder has one unique decomposition

```text
x = X + 4^L h,
h = x >> (2L).
```

The phase-frontier projection theorem can be iterated `L` times:

```text
x in O_(a,k)
  => x >> (2L) in O_(a,k-L).
```

Therefore

```text
C_(a,k)(X,L)
  subseteq {X + 4^L h : h in O_(a,k-L)}.
```

The reverse inclusion is not automatic, because not every high ancestor admits
the prescribed sequence of low base-four lifts. Retaining the exact frontier
membership condition gives equality:

```text
C_(a,k)(X,L)
  = {X + 4^L h :
       h in O_(a,k-L),
       X + 4^L h in O_(a,k)}.
```

The map

```text
x -> x >> (2L)
```

is injective on the cylinder, with inverse `h -> X+4^L h`. Thus the factorization
is a bijection between the cylinder intersection and the accepted subset of the
residual frontier.

When `k<=L`, every phase output is strictly below `4^L`. Congruence to `X`
then forces equality. Hence

```text
C_(a,k)(X,L) = {X} intersect O_(a,k).
```

Together these two cases decide every finite phase cylinder.

## 3. High-to-low digit filter

Write the base-four expansion

```text
X = e_0 + e_1 4 + ... + e_(L-1) 4^(L-1),
e_i in {0,1,2,3}.
```

For `k>L`, set `r=k-L` and begin with

```text
S_0 = O_(a,r).
```

Read the fixed digits from high to low. For `j=1,...,L`, define

```text
S_j = {
  4q + e_(L-j) :
  q in S_(j-1),
  4q + e_(L-j) in O_(a,r+j)
}.
```

Inductively, every element of `S_j` has the form

```text
4^j h + e_(L-j) + 4 e_(L-j+1) + ... + 4^(j-1) e_(L-1)
```

for one residual ancestor `h in O_(a,r)`. Therefore

```text
S_L = C_(a,k)(X,L).
```

Each membership test in the definition of `S_j` is decided by the exact
partial-inverse recursion from the phase-frontier lift theorem. The algorithm
never constructs `O_(a,k)` unless `k-L=k`, as in the trivial depth-zero case.
Its largest explicitly enumerated frontier is the residual frontier
`O_(a,k-L)`.

This is the key computational separation:

```text
old scale: complete complexity-k phase frontier,
new scale: residual complexity-(k-L) frontier plus exact recursive filters.
```

The method returns the complete minimizer set, not only one witness or one
boolean answer.

## 4. Exact actual campaign through depth sixteen

The independent C++ analyzer uses residual frontiers through complexity twenty
and exact recursive membership above that boundary. It reproduces the known
actual phase complexities and additionally records the complete number of
minimum-complexity phase states in each cylinder.

```text
L   X_L         kappa_p  #p minimizers   kappa_u  #u minimizers
1   0x3              1         1              2         1
2   0x7              3         1              2         1
3   0x7              7         2              2         1
4   0xc7             8         1              7         1
5   0x2c7            8         1             12         2
6   0x6c7           12         1             14         2
7   0x6c7           13         1             14         2
8   0x46c7          17         1             14         1
9   0x146c7         17         1             18         1
10  0x146c7         17         1             19         1
11  0x146c7         21         1             26         2
12  0xc146c7        28         3             27         1
13  0xc146c7        30         2             30         2
14  0x8c146c7       33         1             30         1
15  0x8c146c7       34         2             30         1
16  0x88c146c7      36         1             30         1
```

The table agrees with the prior exact quotient-distance values. The proof of
minimality here is independent in form: every lower complexity has an empty
residual filter, and the displayed complexity has a nonempty complete filter.

### Depth-twelve compression example

At actual depth twelve, the phase-`p` minimum is `k=28`, so the residual
complexity is only sixteen. The high-to-low filter sizes are

```text
23751, 12249, 4962, 2391, 1291, 415, 157,
73, 36, 20, 9, 3, 3.
```

Thus the complete complexity-28 cylinder is obtained from 23,751 residual
states and ends with exactly three minimizers.

For phase `u`, the minimum is `k=27`, residual complexity fifteen, and the
filter is

```text
10998, 5779, 2344, 1127, 610, 209, 73,
42, 17, 9, 5, 1, 1.
```

The actual phase-`u` cylinder has one exact minimizer.

## 5. Uniqueness of the generic zero-penalty counterexample

The phase-`u`, complexity-25 state

```text
x = 0x1bcd3a7b3fdfb
```

was previously shown to lie in the three nested schedule cylinders

```text
w_12 = tutututttutu,
w_14 = tutututttututu,
w_16 = tutututttutututu.
```

The residual filter proves a stronger finite statement: this state is the unique
complexity-25 phase-`u` output in each cylinder.

```text
cylinder   initial residual states   final minimizers
w_12                 3266                    1
w_14                  950                    1
w_16                  255                    1
```

The complete funnels are recorded in the result file. This uniqueness removes
any ambiguity about whether the zero two-return penalty was produced by several
unrelated minimum witnesses.

It remains a generic locally admissible schedule, not the actual zero-initialized
moving-fringe schedule.

## 6. Independent validation

The Python and C++ implementations use the same theorem but independent data
structures and campaign scales.

Python:

```text
focused tests:                    7 passed
small exhaustive cylinders:       3,608
actual default depths:             1 through 10
default certificate:
  8fa73099c54206ed68e0e33028d9d2a4a381d7f6425544c539a887c82c23f087
full depths:                       1 through 12
full certificate:
  18a9d05aa5326f972125291c03761f7081b18d5ef8c7d369b09b7683491faa85
```

C++:

```text
small exhaustive cylinders:       19,984
actual depths:                     1 through 16
maximum residual complexity:       20
phase-p residual frontier size:    239,086
phase-u residual frontier size:    202,660
checksum:                          0xb05eebbc00534617
output SHA-256:
  48ff8fa427b2f9cc08bbe90fb0d5237d0b9a40dfa0bd9811c3a21c8662fd28b7
runtime:                           about 5.8 seconds
peak resident memory:              about 253 MiB
```

The exhaustive checks compare the residual factorization with direct complete
frontier grouping for every phase, all configured small complexities and
depths, and every residue modulo `4^L`.

## 7. Research consequence

The phase-minimizer problem now separates into two exact pieces:

1. enumerate the much smaller residual phase frontier;
2. test the prescribed survivor digits with the exact recursive lift criterion.

This supplies a practical route for targeted cylinders and returns the complete
minimum witness set. It also exposes the remaining difficulty sharply: at large
actual depths, the residual complexity itself still grows and must be controlled
by an all-time orbit-specific argument.

The factorization does not prove that actual return penalties are positive
infinitely often, prove either phase complexity diverges, exclude eventual
center period two, or solve Rule 30 center nonperiodicity.
