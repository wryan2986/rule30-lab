# Phase-frontier projection tower and minimizer high ancestors

Status: complete proof of an exact projective structure on the ordinary phase
frontiers, plus a controlled independent exhaustion through complexity 25. This
is a structural coupling theorem. It does not prove positive actual return
penalties, exclude eventual center period two, or solve Rule 30 center
nonperiodicity.

## 1. Ordinary phase frontiers

For phase `a in {p,u}`, let `O_(a,k)` be the set of distinct ordinary outputs at
complexity `k`. The initial levels are

```text
O_(p,1)={3},
O_(u,1)={1},
```

and every later level is obtained by the three generators

```text
t(x)=x xor ((x<<1) or (x<<2)),
u(x)=t(x) xor 1,
p(x)=t(x) xor 1 xor (2 if x is even else 0).
```

When `x` is odd, `p(x)=u(x)`, so the distinct frontier children are still exactly
the values used by the existing phase-frontier enumerators.

The established bit-length law is

```text
bitlen(x)=2k     for x in O_(p,k),
bitlen(x)=2k-1   for x in O_(u,k).
```

Hence the complexity levels are disjoint.

## 2. Generator-blind base-four projection identity

Write a parent state as

```text
x=4r+d,  d in {0,1,2,3}.
```

A direct bitwise expansion gives, for every child generator `g in {t,u,p}`,

```text
g(4r+0)>>2 = t(r),
g(4r+1)>>2 = u(r),
g(4r+2)>>2 = p(r),
g(4r+3)>>2 = p(r).
```

The right-hand side is independent of `g`. The most recent generator changes
only the two low positions that are removed by the projection.

Define

```text
C_0=t,
C_1=u,
C_2=C_3=p.
```

Then the identity is

```text
g(4r+d)>>2=C_d(r).
```

Each `C_d(r)` is an allowed ordinary-frontier child of `r`. For odd `r`, the
symbol `p` merely duplicates `u`; for even `r`, it is the third distinct child.

## 3. Phase-frontier projection theorem

Let

```text
pi(x)=x>>2.
```

> **Projection theorem.** For every phase `a` and every `k>=2`,
>
> ```text
> pi(O_(a,k)) subseteq O_(a,k-1).
> ```

### Proof

The level `k=2` cases are direct:

```text
O_(p,2)={12,13},  pi(O_(p,2))={3},
O_(u,2)={6,7},    pi(O_(u,2))={1}.
```

Assume the theorem through level `k-1`. Take `y in O_(a,k)`. Then

```text
y=g(x)
```

for some `x in O_(a,k-1)` and some generator `g`. Write `x=4r+d`. By the
induction hypothesis,

```text
r=x>>2 in O_(a,k-2).
```

The generator-blind identity gives

```text
y>>2=C_d(r).
```

Since `C_d(r)` is a valid frontier child of `r`, it lies in `O_(a,k-1)`.
This completes the induction.

Iterating immediately yields

```text
x in O_(a,k)
    => x>>(2L) in O_(a,k-L)
```

for every `0<=L<k`.

## 4. Exact one-level fiber bound

For `q in pi(O_(a,k))`, choose a frontier parent `x in O_(a,k-1)` and a
generator `g` with

```text
g(x)>>2=q.
```

Both `t(x)` and `u(x)` belong to `O_(a,k)`, are distinct, and have the same
projection as `g(x)`. Thus every nonempty projection fiber has at least two
members.

A fiber can contain at most the four integers

```text
4q, 4q+1, 4q+2, 4q+3.
```

Therefore

```text
2 <= |{y in O_(a,k): y>>2=q}| <= 4
```

for every nonempty fiber.

The projection is generally neither injective nor surjective.

## 5. Coupling to phase-minimizer witnesses

Let `X(w)` be the depth-`L` survivor residue for a branch word `w`, where
`L=|w|`. Suppose an ordinary phase-`a` output `x in O_(a,k)` represents that
cylinder:

```text
x = X(w) mod 4^L.
```

When `L<k`, write

```text
x=X(w)+4^L h,
h=x>>(2L).
```

The iterated projection theorem gives the exact necessary condition

```text
h in O_(a,k-L).
```

Thus every deep phase-minimizer witness carries a genuine ordinary
phase-frontier ancestor of residual complexity `k-L` in its aligned high
quotient.

This is the first exact bridge from the minimizer frontier to the growing high
part: a candidate is not an arbitrary high lift of the survivor cylinder. Its
high quotient must itself be a valid lower-complexity phase output.

The condition is necessary but not sufficient. For example,

```text
phase p:
12 in O_(p,2)
50,51 in O_(p,3)
48,49 not in O_(p,3)
```

even though all four proposed lifts project to `12`. Similarly,

```text
phase u:
26 in O_(u,3)
104,105,107 in O_(u,4)
106 not in O_(u,4).
```

The residual ancestor therefore narrows a minimizer search but does not
reconstruct the low lift by itself.

## 6. The complexity-25 counterexample ancestry

The known phase-`u` state

```text
x=0x1bcd3a7b3fdfb
```

is generated at complexity 25 by

```text
uuuttttutuptttututututuu
```

from the phase-`u` start state `1`.

Its three nested counterexample cylinders have depths 12, 14, and 16. Their
aligned high quotients are

```text
depth 12: x>>24 = 0x1bcd3a7 in O_(u,13),
depth 14: x>>28 = 0x1bcd3a  in O_(u,11),
depth 16: x>>32 = 0x1bcd3   in O_(u,9).
```

The residual complexities are exactly

```text
25-12=13,
25-14=11,
25-16=9.
```

Hence the same generic zero-penalty counterexample now has an explicit
phase-frontier ancestry at every nested return depth.

## 7. Independent controlled exhaustion

The C++ analyzer exhausts both phase frontiers through complexity 25.

```text
phase-p outputs checked:  9,118,715
phase-u outputs checked:  7,745,997
total outputs checked:   16,864,712

generator-identity checks: 50,594,136
projection violations:     0
```

Across levels 2 through 25, the one-level projection fibers are

```text
size 2: 1,045,786
size 3: 1,314,110
size 4: 2,707,702
```

They account for all `16,864,710` noninitial outputs.

The number of distinct projected parents is

```text
5,067,598,
```

while `4,611,229` preceding-level outputs have no lift into the next level.
This confirms the strict nonconverse on a large exact campaign.

Validation:

```text
focused Python tests:       7 passed
Python default certificate: 8434a652065aea04ab71c196d7406ec0afd4251680dc07f4c773a223396a5e24
Python full certificate:    711c29f1b185c611549e140dc1f7cf0391a5840a40c8c33703c919bbfa900337
C++ output hash:             c3de4b488927b3284626acd5e9e63152d424c55edbc459de02ac336263fc4e0e
C++ runtime:                 about 0.77 seconds
C++ peak RSS:                about 86.7 MiB
```

## 8. Scientific consequence and boundary

The phase-minimizer problem now has an exact high/low decomposition:

```text
low part:
the depth-L survivor cylinder X(w)

high part:
a required phase ancestor h in O_(a,k-L)
```

This supplies a rigorous way to couple the phase-minimizer search to a growing
high state. It also shows why the high ancestor alone cannot decide minimizer
membership: many valid ancestors have only a strict subset of their four
base-four lifts in the next frontier.

The theorem does not prove that actual return penalties are eventually or
recurrently positive. It does not prove phase-witness complexity divergence,
exclude eventual center period two, or solve Rule 30 center nonperiodicity.
