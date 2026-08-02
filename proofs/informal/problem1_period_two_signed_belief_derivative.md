# Signed defect mass as an exact branching derivative

## Purpose

The exact weighted recursion proves how every concrete dominant adjacent shadow lifts, but it does not by itself prove that the belief remains nonempty. Previous finite-state quotients tried to preserve individual shadow paths. Their state alphabets continued to grow.

This note instead studies an additive invariant of the **entire concrete belief**.

For a current endpoint `x` at complexity `k` and cylinder depth `L`, let `B(k,L,x)` be the concrete adjacent-shadow endpoints in the same base-four cylinder whose fiber sequence dominates the current fiber sequence.

For `y in B(k,L,x)`, let `c(y)` be the number of non-`1111` shadow fibers. Define

```text
P_(k,L,x)(z) = sum_{y in B(k,L,x)} z^{c(y)}.
```

The signed belief mass is

```text
S_(k,L,x) = P_(k,L,x)(-1).
```

The implication

```text
S_(k,L,x) != 0  =>  B(k,L,x) != empty
```

is immediate and exact. Signed nonvanishing would therefore prove the concrete adjacent-shadow inclusion without choosing or finitely classifying an individual shadow endpoint.

## Local signed factor

Write `m` for a current fiber and `n` for a shadow fiber. Define

```text
epsilon_m(n) = 0    if m is not contained in n,
               1    if n = 1111,
              -1    otherwise.
```

The product of these factors over a cylinder is exactly `(-1)^c(y)` for a dominant shadow and zero for a rejected shadow.

The Rule 30 frontier fibers lie in

```text
0000, 0011, 1011, 1100, 1111.
```

For every nonzero current mask appearing on the relevant gap-`222` paths, the factor has a simpler exact form.

### Current mask `0011` or `1011`

Let `b_2(n)` indicate whether the shadow endpoint has its digit-2 child. Then

```text
epsilon_m(n) = 1[m subset n] * (2 b_2(n) - 1).
```

For `m=1011`, the only dominant masks are `1011` and `1111`; digit 2 distinguishes them. For `m=0011`, the dominant nonfull masks `0011` and `1011` both lack digit 2, while `1111` has it.

### Current mask `1100`

Let `b_0(n)` indicate whether the shadow endpoint has its digit-0 child. Then

```text
epsilon_1100(n) = 1[1100 subset n] * (2 b_0(n) - 1).
```

The dominant masks are `1100` and `1111`; digit 0 distinguishes them.

### Current mask `1111`

Dominance forces `n=1111`, so

```text
epsilon_1111(n) = 1[n=1111].
```

Thus every nonfull local factor is a Rademacher difference determined by the existence of one missing sibling branch.

## Exact branching-derivative theorem

Let the current mask sequence be `m_0,...,m_(L-1)` from low to high base-four position. For every same-cylinder shadow endpoint `y`, let `n_j(y)` be its mask at position `j`. Then

```text
S_(k,L,x)
  = sum_y product_{j=0}^{L-1} epsilon_(m_j)(n_j(y)).
```

Substituting the identities above expresses `S` as an iterated signed sibling-branch derivative of the concrete frontier cylinder.

This is exact and does not use the finite census. It is compatible with the seed-and-lift recursion: appending one common digit filters concrete endpoints and multiplies each surviving signed weight by the new local derivative factor. No endpoint quotient or existential transition is introduced, so realization-splicing does not occur.

## Controlled Python campaigns

Through complexity 16:

```text
phase-u outputs:                 43,970
gap-222 cylinders:                  10
dominant failures:                    0
signed zero cylinders:                0
minimum absolute signed mass:         6
minimum budget-three shadows:        54
certificate:
636dc347652eadbc123580f37bbd786157a382be385b8d0946149efbb341f5d7
```

Through complexity 18:

```text
phase-u outputs:                144,173
gap-222 cylinders:                  26
dominant failures:                   0
signed zero cylinders:               0
minimum absolute signed mass:        2
minimum budget-three shadows:       20
certificate:
3b58fefb20757d024133ee6094579e812f9b51ef9cb0d091c498d785adfc0598
```

Seven focused Python tests pass.

## Independent C++ census through complexity 28

```text
phase-u outputs:                    40,122,287
gap-222 cylinders through k=27:          2,989
new cylinders at k=28:                   2,173
total cylinders:                         5,162
dominant failures:                           0
synchronized/full failures:                  0
signed zero cylinders:                       0
negative signed cylinders:                  59
majority failures:                         292
minimum defect 0:                        5,159
minimum defect 3:                            3
minimum absolute signed mass:                1
minimum number of cost-at-most-3 shadows:    1
```

The unique minimum-magnitude and minimum-budget witness remains

```text
state: 0x1bcd3a7b3fdfb
complexity: 25
cut: 9
signed mass: -1
cost-at-most-3 shadows: 1
```

C++ output SHA256:

```text
8b282101c04a6cd7c36f77de7a468900107115007a4286a14c4d4a8ab6cb51c0
```

Strict compilation used

```text
-O3 -std=c++20 -Wall -Wextra -Werror -pedantic
```

with runtime about 33.6 seconds and peak RSS about 549,228 KiB.

## Exact boundary examples

### Majority is false

Through complexity 28, 292 relevant cylinders retain fewer than half of their same-cylinder adjacent endpoints. Raw density cannot explain nonemptiness.

### Positivity is false

There are 59 relevant cylinders with negative signed mass. The target is nonvanishing, not positivity.

### Signed nonvanishing is not universal

At phase `u`, complexity 5, state `0x198`, and depth 1, the dominant belief has

```text
cost 0: 1
cost 1: 1
```

and hence `P(-1)=0`. The five-mask alphabet and local derivative identity alone do not prove nonvanishing. An all-depth proof must use the forced schedule and return-word constraints.

## Scientific boundary

The following are exact at every depth:

1. the defect-polynomial definition;
2. the local branching-derivative identities;
3. the path-product formula for signed mass;
4. nonzero signed mass implies a nonempty concrete dominant belief.

The nonvanishing census through complexity 28 is finite evidence. It does not prove signed nonvanishing at arbitrary complexity, the all-depth adjacent-shadow inclusion, exclusion of eventual period two, or Rule 30 center nonperiodicity.

## Next target

The finite-state endpoint route should remain closed. The new target is a direct theorem that the iterated branching derivative cannot vanish on an admissible gap-`222` forced-schedule cylinder.

Promising forms are:

- a sign-reversing involution on even- and odd-defect shadows with a provably unpaired boundary endpoint;
- a recurrence for signed cylinder mass using forced-schedule words rather than endpoint identities;
- a boundary, degree, Euler-characteristic, or Walsh-coefficient argument forced to be nonzero by the three-return pattern.
