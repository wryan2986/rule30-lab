# Period-two complete-return-word precision

Status: complete all-time theorem for every finite realized return-gap word. The
theorem gives the exact eventual 2-adic precision of the composed return map on
that complete cylinder. It does not determine the unique infinite
zero-initialized orbit, prove witness-complexity divergence, exclude eventual
center period two, or solve Rule 30 center nonperiodicity.

## 1. Return words

At a `u` event write the packed even-time fringe as

```text
A = 4z.
```

Let

```text
w = (r_0,...,r_(J-1)),      r_j in {2,3,4,5}
```

be a finite realized word of successive `u`-return gaps, and put

```text
B = r_0 + ... + r_(J-1).
```

Following the complete word advances the packed fringe by exactly `B`
two-step blocks. Denote the final return coordinate by `R_w(z)`, so that

```text
F^B(4z) = 4 R_w(z)
```

for every `z` in the cylinder `C_w` realizing the return word.

The result below conditions on the complete word, including every intermediate
return. It is therefore stronger than conditioning on one gap at a time.

## 2. Finite-word cylinder modulus

One packed fringe block has radius two. The branch letter after `s` blocks
depends only on the two low bits of `F^s(4z)`, hence only on the first
`2s+2` bits of `4z`. These correspond to the first `2s` bits of `z`.

Consequently every branch letter through block `B`, and therefore the complete
return word `w`, depends only on

```text
z mod 2^(2B).
```

If any ordinary coordinate realizes `w`, reducing it modulo `2^(2B)` gives a
finite representative of the same cylinder. Let `c_w` be the least such
representative. Then

```text
0 <= c_w < 2^(2B).
```

This representative bound is used only to obtain one uniform separation
threshold. The exact precision slope below is independent of the choice of
representative.

## 3. Causal-cone upper bound

To determine `R_w(z) mod 2^k`, it is enough to determine packed output bits
`2,...,k+1` of `F^B(4z)`. Their complete radius-`2B` dependency cones reach no
higher than packed input bit

```text
k + 1 + 2B.
```

Because packed input bit `i+2` is coordinate bit `i` of `z`, the required input
range ends at coordinate bit

```text
k + 2B - 1.
```

Thus

```text
R_w(z) mod 2^k
```

is determined by

```text
z mod 2^(k+2B).                                      (1)
```

This upper bound does not use the intermediate return positions except through
the known total span `B`.

## 4. Separated high-bit witness

Fix

```text
k >= 4B + 5
```

and define

```text
h = k + 2B - 1,
z_0 = c_w,
z_1 = c_w + 2^h.
```

The two coordinates agree modulo `2^h`, so a precision of only `h=k+2B-1`
bits cannot distinguish them.

In packed coordinates, the added isolated bit begins at site

```text
h + 2 = k + 2B + 1.
```

The low component `4c_w` has highest possible occupied site `2B+1`. After `s`
blocks:

- the low component reaches no higher than `2B+1+2s`;
- the isolated high component reaches no lower than `k+2B+1-2s`.

Their separation is therefore at least

```text
k - 4s >= k - 4B >= 5.                              (2)
```

A packed block has radius two, so a gap of five cells means that no local input
window meets both components. During all `B` blocks the high perturbation
therefore evolves exactly as an isolated bit in the translation-invariant
interior, independently of the complete low fringe and its forced boundary.

Equation (2) also implies that the perturbation never reaches packed sites zero
or one. Hence it changes none of the branch letters through block `B`:

```text
z_0 and z_1 realize the same complete return word w. (3)
```

## 5. Extreme response bit

Rule 30 sends the left edge of an isolated finite pattern one cell left at each
single time step, with value one. One packed block consists of two Rule 30
steps. After `B` blocks, the isolated bit introduced at packed site `h+2`
therefore has leftmost response bit

```text
h + 2 - 2B = k + 1,
```

and has no occupied sites below `k+1`.

At the final `u` return, dividing the packed state by four converts packed site
`k+1` into return-coordinate site `k-1`. The low and high components remain
disjoint, so addition is XOR and there is no carry. Therefore

```text
R_w(z_0) XOR R_w(z_1) = 2^(k-1) mod 2^k.             (4)
```

The two inputs are congruent modulo `2^(k+2B-1)` but their outputs differ modulo
`2^k`. Hence the conditioned map cannot factor through a source modulus with
only `k+2B-1` bits.

Combining this lower bound with (1) proves the exact theorem:

```text
For every realized finite return word w of total span B,
and every k >= 4B+5,

    z -> R_w(z) mod 2^k

requires exactly k+2B low bits of z.                 (5)
```

Equivalently, conditioning on the entire finite return word still loses exactly
two coordinate bits per fringe block once the target window is beyond the
explicit separation threshold.

## 6. Exact span-ten census

The Python and independent C++ analyzers exhaust every coordinate modulo
`2^20`. Since a return word with total span at most ten depends only on at most
those twenty bits, this is a complete census of all such cylinders.

The campaign finds 41 realized words:

```text
span 2:   1
span 3:   1
span 4:   2
span 5:   2
span 6:   4
span 7:   5
span 8:   7
span 9:   8
span 10: 11
```

By return count:

```text
1 return:  4
2 returns: 15
3 returns: 16
4 returns:  5
5 returns:  1
```

For each word, the analyzers reconstruct its least representative and check the
witness at five consecutive target widths beginning at `4B+5`. All 205
witnesses preserve the complete return word and flip exactly final coordinate
bit `k-1`.

Validation:

```text
Python tests:                 7 passed
coordinates exhausted:       1,048,576
realized return words:        41
high-bit witness checks:      205
Python default certificate:   af27f91cb19657ea5562ede19c72c5d201dbded8a98b60289e77b4d6085d0542
Python span-10 certificate:   728324c02d0fbccf59b618665cd4b374fdcddaca7afcb2af0540a9bd54b1d57d
C++ output hash:              8eadaf91a7b7f3636b7feb709044cf3493241ef332772ede283eaa93a19f4484
```

The C++ span-ten run completed in about `0.06` seconds with peak resident memory
about `3.7 MiB`. The Python span-ten run completed in about `4.76` seconds with
peak resident memory about `108 MiB`.

## 7. Research consequence

A proof cannot compress the actual return coordinate into a fixed-width suffix
by adjoining any finite prefix of exact return gaps. Even the complete finite
return word leaves the eventual precision cost at two fresh source bits per
fringe block.

The remaining route must use the growing information rather than discard it. A
successful continuation needs either:

- a global invariant special to the unique zero-initialized growing front; or
- a direct coupling between that growing front and the phase-witness minimizing
  sets.

## Scientific boundary

Equation (5) is an all-time theorem about every finite realized return word. It
does not assert anything about the limiting distribution of actual return
words, permanent avoidance of the consecutive-gap-two cylinders, divergence of
`kappa_p` or `kappa_u`, infinite support of the alternating inverse lift,
eventual center period two, or Rule 30 center nonperiodicity.
