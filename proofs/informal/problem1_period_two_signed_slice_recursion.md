# Exact signed-slice lift and scalar-recurrence obstructions

## Purpose

The signed defect mass

```text
S(k,L,x) = sum_{y in B(k,L,x)} (-1)^c(y)
```

is an additive invariant of the full concrete adjacent-shadow belief. Its
nonvanishing certifies that the belief is nonempty. The remaining problem is to
understand how this signed mass changes when a common low base-four digit is
adjoined.

A scalar recurrence would be ideal, but the scalar mass forgets how the signed
parent belief is distributed among the possible next shadow fibers. This note
identifies the exact missing state and gives concrete counterexamples to scalar
and sign-only induction.

## 1. Cylinders and their parent

Let

```text
N = (k,L,x),   L >= 2,
```

be a current cylinder. Write

```text
x = 4q + d
```

and remove the common low digit to obtain the parent cylinder

```text
parent(N) = (k-1,L-1,q).
```

A concrete parent shadow endpoint is a state

```text
p in O_(u,k-2)
```

with the required high-cylinder residue and dominance conditions. Its signed
weight is

```text
w(p) = (-1)^c(p).
```

Let

```text
m = M_(u,k-1)(q)
```

be the new low current fiber introduced when the common digit is restored.

## 2. Five-component signed slice vector

Split the signed parent belief by the exact next shadow fiber:

```text
V_n(parent(N))
  = sum_{p in B(parent(N)), M_(u,k-2)(p)=n} w(p),
```

for

```text
n in {0000,0011,1011,1100,1111}.
```

The scalar parent mass is only the sum of the five components:

```text
S(parent(N)) = sum_n V_n(parent(N)).
```

Define the local signed dominance factor

```text
epsilon_m(n) = 0    if m is not contained in n,
                 1    if n = 1111,
                -1    otherwise.
```

## 3. Exact signed-slice lift theorem

For every cylinder `N=(k,L,x)` with `L>=2`,

```text
S(N) = sum_n epsilon_m(n) V_n(parent(N)).
```

### Proof

Every child shadow endpoint in the same low-digit cylinder has the unique form

```text
4p+d
```

for a parent shadow endpoint `p`. The endpoint `4p+d` exists exactly when the
shadow fiber `n=M_(u,k-2)(p)` contains digit `d`. Because the current endpoint
`4q+d` exists, digit `d` belongs to the current fiber `m`; therefore the
containment test `m subset n` already implies child existence.

The higher `L-1` dominance tests and their signed weight are exactly those of
the parent endpoint `p`. The one new low test rejects the endpoint when
`m` is not contained in `n`; contributes no new defect when `n=1111`; and
contributes one new defect, hence a sign reversal, when `n` is a nonfull
dominant fiber. Its multiplier is therefore exactly `epsilon_m(n)`.
Summing by the five possible values of `n` proves the identity.

This is an equality of concrete endpoint sums. It introduces no quotient edge
and no realization splicing.

## 4. Scalar parent mass does not determine child magnitude

At complexity 17, consider the two depth-two cylinders

```text
A: x = 0x190b9fdfb
B: x = 0x1bcd3a7b3
```

Both have new low current mask `1011`. Their depth-one parents have equal signed
mass:

```text
S(parent(A)) = S(parent(B)) = 1650.
```

However, their signed slice vectors, ordered as

```text
0000, 0011, 1011, 1100, 1111,
```

are

```text
V(parent(A)) = (695, 0, 421,  9, 525)
V(parent(B)) = (721, 0, 138, 48, 743).
```

For current mask `1011`, only shadow masks `1011` and `1111` survive, with
factors `-1` and `+1`. Thus

```text
S(A) = 525 - 421 = 104,
S(B) = 743 - 138 = 605.
```

The same complexity, local current mask, and scalar parent mass therefore do
not determine the child magnitude.

## 5. Parent sign does not determine child sign

At complexity 18, consider

```text
A: x = 0x642e4d2f1, depth 3
B: x = 0x6473d46ab, depth 5.
```

Both introduce low current mask `1011`, and both parent masses are positive:

```text
S(parent(A)) = 606,
S(parent(B)) = 15.
```

Their slice vectors are

```text
V(parent(A)) = (262, 0, 200, 27, 117)
V(parent(B)) = (  3, 0,   5,  0,   7).
```

Consequently,

```text
S(A) = 117 - 200 = -83,
S(B) =   7 -   5 =   2.
```

Even the parent sign, complexity, and local current mask do not determine the
child sign.

## 6. Controlled Python verification

Through complexity 16:

```text
phase-u outputs:                    43,970
gap-222 cylinders:                     10
unique stripped ancestor cylinders:    16
signed-zero ancestors:                   0
minimum absolute ancestor mass:          6
signed-slice disagreements:              0
certificate:
459ad0505c55ef7c7622c203ad3d8df8a1dfaf454c00de168be28ead355f1e39
```

Through complexity 18:

```text
phase-u outputs:                   144,173
gap-222 cylinders:                     26
unique stripped ancestor cylinders:    43
signed-zero ancestors:                   0
minimum absolute ancestor mass:          2
signed-slice disagreements:              0
certificate:
6153f7a60f7ea8c2a2d4f28950e8e19d8a9e51b43e673fc8b58af86d073268d8
```

Seven focused Python tests pass.

## 7. Independent complexity-28 ancestor census

The independent C++ analyzer builds the phase-`u` frontier through complexity
28, gathers every gap-`222` cylinder, strips every possible number of common
low digits, and evaluates the signed mass of every resulting ancestor
cylinder.

```text
phase-u outputs:                    40,122,287
gap-222 cylinders:                      5,162
unique stripped ancestor cylinders:     7,363
ancestor lift transitions:               2,222
signed-zero ancestor cylinders:              0
negative ancestor cylinders:                94
minimum absolute ancestor mass:               1
```

The scalar transition census contains

```text
exact-parent-mass collision classes:          28
classes with mixed child signs:                0
parent-sign collision classes:                43
parent-sign classes with mixed child signs:   20
```

The absence of zero ancestor masses is finite evidence through complexity 28.
The explicit scalar obstructions and the signed-slice theorem are exact.

Validation used

```text
-O3 -std=c++20 -Wall -Wextra -Werror -pedantic
```

with output SHA256

```text
5d181d36ac88a9887e9e7a29f287a1455b13c27a320937115f66dc2bb334369f
```

runtime about 31.9 seconds, and peak RSS about 549,488 KiB.

## 8. Scientific boundary

The following are exact at every depth:

1. the five-component signed-slice definition;
2. the signed-slice dot-product lift theorem;
3. the two scalar-recurrence counterexamples.

The complexity-28 nonvanishing and collision counts are finite observations.
They do not prove that ancestor signed masses remain nonzero at arbitrary
complexity, that a three-defect shadow always exists, the all-depth adjacent
shadow inclusion, exclusion of eventual period two, or Rule 30 center
nonperiodicity.

## 9. Next target

The scalar route is closed. An all-depth induction must retain enough of the
five-component vector to show that it never lies in the local cancellation
hyperplane

```text
sum_n epsilon_m(n) V_n = 0.
```

For the three nonfull current masks this reduces to a difference of selected
slice components. The next useful target is therefore a cone, ordering, parity,
or boundary invariant on the signed slice vector that is preserved by the
forced `t/u` return schedule and excludes those cancellation hyperplanes.
