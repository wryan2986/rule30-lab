# Period-two gap-conditioned return precision

Status: complete all-time proof that conditioning on a known first-return gap does
not reduce the exact 2-adic precision budget. For every return gap
`r in {2,3,4,5}` and every target width `k>=5`, computing the successor return
coordinate modulo `2^k` requires exactly `k+2r` source-coordinate bits.

This is a structural theorem about every compatible return coordinate. It does
not determine the unique zero-initialized orbit, prove permanent avoidance of
the consecutive-gap-two cylinders, exclude eventual center period two, or solve
Rule 30 center nonperiodicity.

## 1. Return coordinates

At a `u` return, write the packed even-time fringe as

```text
A = 4z.
```

Let

```text
rho(z) in {2,3,4,5}
```

be the first-return gap and let `R(z)` be the next return coordinate, so that

```text
F^rho(z)(4z) = 4 R(z).
```

Fix a gap `r` and restrict attention to its exact cylinder

```text
C_r = {z : rho(z)=r}.
```

The question is how many low bits of `z` are needed to determine

```text
R(z) mod 2^k
```

on `C_r`.

## 2. Causal-cone upper bound

One two-time fringe block has radius two. Therefore, after exactly `r` blocks,
output bit `i` depends only on source bits `i-2r` through `i+2r`.

The target residue `R(z) mod 2^k` consists of packed-state bits `2` through
`k+1` after the return. Its complete dependency cone lies within source packed
bits through `k+1+2r`, equivalently source-coordinate bits through
`k+2r-1`.

Hence

```text
R(z) mod 2^k is determined by z mod 2^(k+2r)
```

once the return gap is known to be `r`.

This gives the upper bound

```text
source precision <= k+2r bits.                         (1)
```

## 3. Exact lower-bound witnesses

To prove that one fewer bit cannot suffice, it is enough to find two coordinates

```text
z and z* = z + 2^(k+2r-1)
```

such that

```text
rho(z)=rho(z*)=r
```

but

```text
R(z) XOR R(z*) = 2^(k-1) mod 2^k.                     (2)
```

The two sources agree modulo `2^(k+2r-1)`, while their successor residues differ
in the highest requested bit. Equation (2) therefore proves that
`k+2r-1` source bits are insufficient.

Finite witnesses handle the small widths before the response separates cleanly
from the low return-cylinder base:

```text
gap 2: k=5 base 100; k=6 base 12
gap 3: k=5 base 25;  k=6 base 3
gap 4: k=5 base 6
gap 5: k=5..12 bases
       407,16191,23,199,415,11,7,15
```

For all larger widths, four sparse families work:

```text
gap r   start k   base z   lifted coordinate
2          7         4     4 + 2^(k+3)
3          7         1     1 + 2^(k+5)
4          6         0         2^(k+7)
5         13         7     7 + 2^(k+9)
```

The return gap depends only on the low return-cylinder bits, so the isolated high
bit does not change `rho`. Once it is separated from the base, its exact response
support in successor-coordinate indices relative to its source index is

```text
r=2: {-4,-3,0,4}
r=3: {-6,-5,-2,3,6}
r=4: {-8,-7,-4,0,1,2,8}
r=5: {-10,-9,-6,-1,1,2,3,4,6,7,10}
```

In every row, the smallest displacement is exactly `-2r`, and every other
response bit lies strictly to its right. Placing the source impulse at index

```text
n = k+2r-1
```

therefore places the leftmost response at index `k-1`; all other response bits
are at index at least `k` and disappear modulo `2^k`. This proves (2) for every
width in each uniform family.

Combining the finite and uniform witnesses yields, for every `k>=5`,

```text
source precision >= k+2r bits.                         (3)
```

## 4. Exact theorem

From (1) and (3):

```text
Theorem.
For every r in {2,3,4,5} and every k>=5, the map

    z in C_r  ->  R(z) mod 2^k

has exact source precision k+2r bits.
```

Equivalently, knowing the next gap does not save even one bit compared with the
full radius-`2r` causal cone.

The gap-specific losses are therefore

```text
gap 2: 4 bits
gap 3: 6 bits
gap 4: 8 bits
gap 5: 10 bits
```

rather than merely a worst-case ten-bit bound.

## 5. Iterated consequence

Suppose a realized return prefix has gaps

```text
r_0,...,r_(J-1).
```

The causal-cone upper bound propagates `k` final bits from

```text
k + 2 sum_j r_j
```

initial bits. The one-return theorem shows that no step has hidden precision
slack that could be recovered merely by conditioning on its known gap.

Thus a strategy based on carrying a fixed-width suffix cannot become exact by
also carrying the gap sequence. Its required width grows by the actual amount

```text
2r_j
```

at each return.

This sharpens the earlier worst-case statement `k+10J`: along the actual path,
the precise upper budget is the cumulative elapsed block length, and every
individual gap class realizes its full local loss on compatible coordinates.

## 6. Exact finite certificates

The Python and independent C++ implementations exhaust every source residue at
all levels

```text
r in {2,3,4,5},  k=5,...,10.
```

The total number of source states is

```text
2,741,760.
```

At each level they verify the conditioned return count, successor-residue set,
checksum, and an explicit pair proving failure at `k+2r-1` bits.

The uniform families are checked through target width 40. The finite checks are
regression certificates for the separately proved all-width causal-cone and
isolated-response statements.

## 7. Research consequence

The previous result ruled out one fixed-width quotient using the worst gap. This
result rules out a possible escape: the actual gap sequence cannot be used to
compress the suffix update below the exact radius of each realized return.

A continuation must therefore do at least one of the following:

- retain a genuinely growing coordinate front;
- find a global invariant special to the zero-initialized finite row;
- or couple return precision directly to phase-witness complexity so that the
  expanding information budget itself forces positive penalties.

The theorem does not by itself prove that the actual return orbit enters or
avoids any particular low cylinder.