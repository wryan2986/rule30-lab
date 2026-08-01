# Exact defect-weighted concrete shadow recursion

Status: exact all-depth recursion for dominant concrete shadow endpoints with
additive defect cost, plus an independent phase-`u` gap-`222` census through
complexity 27.

## 1. Weighted concrete beliefs

For phase `a`, let `O_(a,k)` be the exact ordinary frontier. For

```text
x in O_(a,k),  1 <= L < k,
```

a concrete adjacent shadow is a state

```text
y in O_(a,k-1),  y = x mod 4^L.
```

Write

```text
x_j = x >> (2j),
y_j = y >> (2j).
```

At cylinder step `j`, the current and shadow fibers are

```text
M_(a,k-1-j)(x_(j+1))
M_(a,k-2-j)(y_(j+1)).
```

The shadow is dominant when the current fiber is contained in the shadow fiber
at every step.

Give a dominant endpoint the additive cost

```text
c_L(y) = number of j for which
         M_(a,k-2-j)(y_(j+1)) != 1111.
```

The weighted belief `W_(a,k,L)(x)` retains every concrete dominant endpoint
`y` together with this exact cost. Its minimum cost is the minimum shadow
defect from PR #43.

## 2. Exact recursive theorem

Write

```text
x = 4q + d.
```

For depth one,

```text
W_(a,k,1)(x)
```

contains exactly the states `y in O_(a,k-1)` with the same low digit such that

```text
M_(a,k-1)(q) subset M_(a,k-2)(y >> 2).
```

Their cost is zero when the shadow fiber is `1111`, and one otherwise.

For `L >= 2`, the exact recursion is

```text
W_(a,k,L)(4q+d)
 = {
     (4p+d, c + [M_(a,k-2)(p) != 1111]) :
       (p,c) in W_(a,k-1,L-1)(q),
       4p+d in O_(a,k-1),
       M_(a,k-1)(q) subset M_(a,k-2)(p)
   }.
```

### Proof

A same-cylinder endpoint must have the form `y=4p+d`. Removing the common low
digit gives

```text
p in O_(a,k-2),
p = q mod 4^(L-1).
```

The remaining `L-1` dominance tests are exactly the tests defining
`W_(a,k-1,L-1)(q)`. The one new low-step test is precisely

```text
M_(a,k-1)(q) subset M_(a,k-2)(p).
```

The endpoint exists exactly when `4p+d` belongs to `O_(a,k-1)`. The new shadow
fiber contributes one defect exactly when it is not `1111`. The converse is
immediate by adjoining the common digit. This proves equality.

## 3. Seed-and-lift decomposition

Iterating the recursion `L-1` times decomposes every certificate into:

1. one depth-one dominant seed pair;
2. a word of `L-1` common base-four lifts;
3. one local fiber-containment test per lift.

The total defect is exactly the sum of the local indicators for non-`1111`
shadow fibers. No quotient-edge splicing is possible because every recursive
state is one concrete endpoint.

The direct definition and recursive definition were independently compared on
all states, both phases, all depths, through complexity nine:

```text
weighted recursion checks: 7,958
violations: 0
```

## 4. Controlled Python campaign

The Python reference implementation compares the direct and recursive weighted
belief for every three-return occurrence in the controlled campaign.

Through complexity 16:

```text
phase outputs:                 96,416
three-return occurrences:          19
weighted cylinders checked:        17
dominant failures:                  0
maximum minimum defect:             0
certificate:
cd52b20688d0c57c84e82d7b42da01d281a347464c6265d80f70ddf9dc62fed6
```

Through complexity 18:

```text
phase outputs:                315,033
three-return occurrences:         61
weighted cylinders checked:       58
dominant failures:                 0
maximum minimum defect:            0
certificate:
090d44e2e0e2e0b9f6f994f7fe60ec25a861cad95f2424e385936ae492db982e
```

Seven focused Python tests pass.

## 5. Independent gap-222 census through complexity 27

The independent C++ analyzer specializes to the only gap word that produced
positive defect through complexity 25. It exhausts all phase-`u` frontiers
through complexity 27:

```text
phase-u outputs:              23,270,776
gap-222 occurrences:              2,989
dominant failures:                    0
minimum defect 0:                 2,986
minimum defect 3:                     3
minimum defect 1 or 2:                0
```

Every selected minimum path is **synchronized or full** at every step:

```text
shadow mask = 1111
or
shadow mask = current mask.
```

Each positive-defect path has exactly the same defect multiset:

```text
1011, 1011, 1100.
```

No `0011` defect occurs.

### Complexity 23

```text
state:   0x191cf4384dfb
cut:     7
shadow:  0x6473cb14dfb
```

### Complexity 25

```text
state:   0x1bcd3a7b3fdfb
cut:     9
shadow:  0x6f671193fdfb
```

### New complexity-27 exception

```text
state:   0x190b9769df876b
cut:     8
shadow:  0x6f34fd3b7876b
base schedule: ttutttut
```

Its minimum shadow masks, low to high, are

```text
1011,1111,1100,1011,1111,1111,1111,1111,1111.
```

The new base schedule is not of the form `(tu)^m ttt`. Therefore the first two
exceptions do not constitute the only prefix family; an all-depth argument
must use the endpoint-preserving recursion rather than a guessed single-family
formula.

## 6. Validation

```text
Python tests: 7 passed
C++ flags: -O3 -std=c++20 -Wall -Wextra -Werror -pedantic
C++ output SHA256:
57878dc9e60a26e9c91b3012b04034b9ef6e6077ed8c2bb9f59d84ba5cc74f1c
runtime: about 10.18 seconds
peak RSS: about 318,856 KiB
```

## 7. Scientific boundary

The weighted recursion and seed-and-lift decomposition are exact at every
depth. The complexity-27 counts, synchronized/full property, and three-defect
multiset are finite observations.

This result does not prove that three defects suffice at every complexity, the
all-depth adjacent-shadow inclusion, phase-complexity divergence, exclusion of
eventual center period two, or Rule 30 center nonperiodicity.

The next target is a finite invariant on endpoint-refined lift states that
proves every admissible gap-`222` lift has a synchronized/full path of cost at
most three.
