# Exact recursive base-four lifts of ordinary phase frontiers

Status: complete proof of an exact recursive membership criterion for the
ordinary phase frontiers. This is a structural partial result. It does not prove
that the actual zero-initialized moving-fringe orbit has recurring positive
return penalties, exclude eventual center period two, or solve Rule 30 center
nonperiodicity.

## 1. Phase frontiers

For phase `a in {p,u}`, let `O_(a,k)` be the set of distinct ordinary outputs at
complexity `k`. The generators are

```text
t(x) = x xor ((x<<1) or (x<<2)),
u(x) = t(x) xor 1,
p(x) = t(x) xor 1 xor (2 if x is even else 0).
```

The initial frontiers are `O_(p,1)={3}` and `O_(u,1)={1}`. Every positive
generator application raises bit length by exactly two, so complexity levels
are disjoint.

The preceding projection theorem proved

```text
x in O_(a,k)  =>  x>>2 in O_(a,k-1).
```

That condition was necessary but did not determine which of the four lifts
`4h,4h+1,4h+2,4h+3` occur above an ancestor `h`. The rule below is exact.

## 2. Parent-digit table

Write a level-`k` parent as `x=4r+d`, where `d in {0,1,2,3}`. For every final
generator `g in {t,u,p}`, the quotient of the child is independent of `g`:

```text
d=0: G_g(4r+0)>>2 = t(r),
d=1: G_g(4r+1)>>2 = u(r),
d=2: G_g(4r+2)>>2 = p(r),
d=3: G_g(4r+3)>>2 = p(r).
```

The possible low base-four digits of the child are also fixed by `d`:

```text
C_0={0,1,3},
C_1={2,3},
C_2={1,2,3},
C_3={0,1}.
```

As four-bit masks these are `1011`, `1100`, `1110`, and `0011`, with bit `e`
recording the presence of child digit `e`. These identities follow by direct
expansion of the two low bits of the three generators.

## 3. Exact partial inverses

The map `t` is triangular from low bits to high bits:

```text
t(x)_j = x_j xor (x_(j-1) or x_(j-2)).
```

A proposed exact preimage is therefore reconstructed uniquely from low to high
and accepted only when forward replay reproduces the target. This defines the
partial inverse `t^(-1)`.

The other partial inverses reduce to it:

```text
u^(-1)(y) = t^(-1)(y xor 1),
```

while `p^(-1)` first recovers source parity from the output low bit, removes the
parity-dependent correction, and then applies `t^(-1)`. Thus a quotient has at
most one residual preimage under each generator.

## 4. Four candidate parents

For a quotient `h`, define

```text
Q_0(h)=4*t^(-1)(h),
Q_1(h)=4*u^(-1)(h)+1,
Q_2(h)=4*p^(-1)(h)+2,
Q_3(h)=4*p^(-1)(h)+3,
```

with a candidate absent when the corresponding partial inverse is undefined.
Define the predecessor mask and next lift fiber by

```text
P_(a,k)(h)={d : Q_d(h) is in O_(a,k)},
D_(a,k+1)(h)={e : 4h+e is in O_(a,k+1)}.
```

The parent-digit table gives the exact identity

```text
D_(a,k+1)(h) = union over d in P_(a,k)(h) of C_d.
```

Every child in the fiber has one of the four parent digits, and each valid
candidate parent contributes exactly its corresponding set `C_d`.

## 5. Recursive membership theorem

Let a target at complexity `k+1` be `y=4h+e`.

> **Recursive lift theorem.** `y` lies in `O_(a,k+1)` if and only if at least one
> `d in {0,1,2,3}` satisfies both `e in C_d` and
> `Q_d(h) in O_(a,k)`.

This is a complete recursion from the singleton initial frontiers. A memoized
implementation decides one target without constructing every intermediate
frontier. Once a valid parent is found, direct replay identifies a final
generator and recursively reconstructs a complete generator witness.

## 6. Five-mask theorem

Every phase frontier has the pairing property

```text
4r+2 in O_(a,k)  =>  4r+3 in O_(a,k).
```

An output ending in digit `2` is accompanied by the digit-`3` output from the
same generator parent: `t` and `u` differ in the low bit; for an odd source
`p=u`; and an even-source `p` output cannot end in digit `2`.

The candidates `Q_2(h)` and `Q_3(h)` share the same residual `p` preimage.
Therefore

```text
2 in P_(a,k)(h)  =>  3 in P_(a,k)(h).
```

Combining this implication with the four contribution masks leaves exactly five
possible lift fibers:

```text
0000 = empty,
0011 = {0,1},
1011 = {0,1,3},
1100 = {2,3},
1111 = {0,1,2,3}.
```

The tempting mask `1110={1,2,3}` would be contributed by `C_2` alone, but a
digit-`2` predecessor forces the digit-`3` predecessor, and
`C_3={0,1}` supplies the missing zero digit. All five allowed masks occur in
both phase towers after the initial levels.

## 7. Strict lift examples

For phase `p`, quotient `12` at complexity two has

```text
D_(p,3)(12)={2,3},
```

so `50,51` occur while `48,49` do not.

For phase `u`, quotient `26` at complexity three has

```text
D_(u,4)(26)={0,1,3},
```

so `104,105,107` occur while `106` does not. The high ancestor is necessary;
the exact predecessor mask determines the valid low lifts.

## 8. Complexity-25 recursive certificate

The known phase-`u` output

```text
x=0x1bcd3a7b3fdfb
```

is accepted by the recursive theorem at complexity 25. Memoization visits only
767 distinct `(phase,complexity,target)` states instead of enumerating the full
frontier. One recovered generator witness is

```text
uuuuttttutuptuputtputtpuu
```

of length 25. Forward replay reproduces the displayed state exactly. This word
need not equal an earlier representation because distinct generator words can
collide at the same ordinary output.

## 9. Independent exhaustive campaign

The C++ implementation exhausts both phase towers through complexity 25:

```text
phase-p outputs checked:  9,118,715
phase-u outputs checked:  7,745,997
total outputs checked:   16,864,712
quotients checked:        9,678,827
candidate-parent checks: 38,715,308
recursion errors:                 0
```

The aggregate fiber counts are

```text
0000: 4,611,229
0011:   236,587
1011: 1,314,110
1100:   809,199
1111: 2,707,702
```

Their sum is the exact number of checked quotients. No other mask occurs. The
Python implementation independently verifies the identities through complexity
20 and checks the recursion against complete small frontiers. Seven focused
regression tests pass.

## 10. Consequence for minimizers

Suppose a depth-`L` survivor cylinder has residue `X(w)` and a proposed
complexity-`k` representative is

```text
x=X(w)+4^L h.
```

The projection theorem requires `h in O_(a,k-L)`. Repeating the new one-level
recursion now decides whether the complete sequence of `L` low base-four digits
can be lifted above that residual ancestor. This replaces an informal
compatibility condition by an exact finite membership certificate.

What remains difficult is minimization: proving that no lower-complexity
residual ancestor and lift path represents the same actual survivor cylinder.

## 11. Scientific boundary

The theorem completely characterizes membership in every finite ordinary phase
frontier and supplies exact certificates for individual candidates. It does not
prove that actual return cylinders force increasing minimum complexity, recurring
positive return penalties, exclusion of eventual center period two, or Rule 30
center nonperiodicity.
