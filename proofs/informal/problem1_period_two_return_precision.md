# Period-two first-return precision loss

Status: complete all-time proof of the exact **worst-case** 2-adic precision
needed to propagate a finite return coordinate, plus independent bounded
certificates. The theorem concerns the full first-return map over all compatible
higher-bit lifts. It does not determine the unique zero-initialized orbit,
exclude eventual center period two, or solve Rule 30 center nonperiodicity.

## 1. Return coordinates

At a `u` event, write the packed even-time right fringe as

```text
A = 4z.
```

Let

```text
(rho(z), R(z))
```

be the gap to the next `u` event and the next return coordinate. The established
return selector gives

```text
rho(z) in {2,3,4,5}
```

and depends only on `z mod 16`.

For `k >= 1`, the finite lifted output of interest is

```text
(rho(z), R(z) mod 2^k).
```

## 2. Dependency-cone upper bound

One two-step fringe block has radius two. Consequently, the low `m` bits after
one block depend only on the low `m+2` bits before the block. Iterating `r`
blocks gives:

```text
low m output bits depend only on low m+2r input bits.       (1)
```

To know `R(z) mod 2^k`, one must know the returned packed state `A'=4R(z)`
modulo `2^(k+2)`. If the return gap is `r`, equation (1) shows that this is
determined by `A mod 2^(k+2+2r)`, equivalently by

```text
z mod 2^(k+2r).                                             (2)
```

Since `r <= 5`, the complete lifted outcome is determined by

```text
z mod 2^(k+10).                                             (3)
```

For `k>=4`, this modulus also contains the four selector bits that determine the
return gap.

## 3. Exact lower bound

The ten-bit overhead in (3) is not an artifact of the cone estimate. For every
`k>=4`, there are two return coordinates congruent modulo `2^(k+9)` that stay in
the same gap-five cylinder but whose successors differ modulo `2^k`.

For `4 <= k <= 12`, use the following base coordinates and compare

```text
z_k
z_k + 2^(k+9).
```

| k | z_k | left successor mod 2^k | right successor mod 2^k |
|---:|----:|-----------------------:|------------------------:|
| 4 | 203 | 11 | 3 |
| 5 | 407 | 12 | 28 |
| 6 | 16191 | 19 | 51 |
| 7 | 23 | 24 | 88 |
| 8 | 199 | 139 | 11 |
| 9 | 415 | 44 | 300 |
| 10 | 11 | 555 | 43 |
| 11 | 7 | 1579 | 555 |
| 12 | 15 | 2712 | 664 |

In every row:

```text
rho(left) = rho(right) = 5
successor_left XOR successor_right = 2^(k-1).
```

Thus the two outputs first differ in the top requested bit.

## 4. Uniform sparse witness for all k >= 13

For all `k>=13`, take

```text
z = 7
z* = 7 + 2^(k+9).                                          (4)
```

Both coordinates have the same low sixteen bits, so both have return gap five.
The high perturbation in (4) is isolated from the fixed low prefix.

Away from the boundary, one fringe block is the translation-invariant five-bit
rule

```text
Phi(a,b,c,d,e)
 = Rule30(
     Rule30(a,b,c),
     Rule30(b,c,d),
     Rule30(c,d,e)
   ).
```

Starting from one isolated `1` in a zero background, the support after five
blocks, relative to the original position, is

```text
{-10,-9,-6,-1,1,2,3,4,6,7,10}.                            (5)
```

In particular, the lowest affected bit is exactly ten positions lower. In (4),
the perturbation is at bit `k+9` of `z`, hence at bit `k+11` of `A=4z`.
Equation (5) makes the lowest changed bit of the returned packed state `A'` equal
to `k+1`, and therefore the lowest changed bit of `R(z)=A'/4` equal to

```text
k-1.
```

For `k=13`, the finite boundary cone is checked directly. For larger `k`, the
high perturbation cone is separated from the fixed low prefix and the same
translated local calculation applies unchanged.

Therefore `2^(k+9)` precision fails for every `k>=13` as well.

Combining the dependency upper bound and these lower-bound witnesses gives the
exact all-time theorem:

```text
For every k>=4,
(rho(z), R(z) mod 2^k)
is determined by z mod 2^(k+10),
and no modulus 2^(k+9) suffices.                            (6)
```

## 5. Iterated precision budget

For a fixed sequence of return gaps

```text
r_0, r_1, ..., r_(J-1),
```

repeated use of (2) shows that `k` final coordinate bits are determined by

```text
k + 2 * sum_j r_j
```

initial coordinate bits. Since every gap is at most five, a worst-case
`J`-return prediction needs

```text
k + 10J
```

initial bits.

This is an exact explanation of why the mod-64 campaign cannot be promoted to an
inductive finite automaton by merely choosing another fixed modulus. The full
return map continually consumes higher-bit information. A successful actual-orbit
argument must carry a growing front, exploit a special invariant of the unique
zero-initialized state, or couple the return coordinate to another global
quantity.

## 6. Controlled validation

The Python campaign exhausts every coordinate through target width ten, or
2,080,768 total finite states across levels `k=4,...,10`, validates the explicit
witnesses through `k=12`, and checks the uniform sparse family through `k=32`.

An independent C++ implementation exhausts the same finite levels and checks the
uniform family through `k=40`.

Validation records:

```text
Python tests:                 7 passed
Python small certificate:     8c27ba880121f2b5e2d5190e7c9f2d5bb7e3961594397cfe78127c69d6c72ed5
Python full certificate:      c206fe50ae8924380ce40db2187aa7d73b4e3415ecc16df697d83e1a3022715e
Python full JSON SHA256:       ce92c660c7932b0ff3aa0d0cd92dac079d63f576727e625784d2fb6564f40cf9
C++ output SHA256:             2bc9bdb1fc1692e0a2725d9a30c717fdc1c14c9ca1e3e4815b6f1024f25cc613
```

The dependency proof and uniform-family argument are the all-width components;
the exhaustive runs are reproducible cross-checks rather than substitutes for
those proofs.
