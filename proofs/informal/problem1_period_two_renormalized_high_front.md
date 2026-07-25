# Period-two lossless renormalized high front

Status: complete all-time proof of the renormalized high-front permutation,
its exact truncation semiconjugacy, and the resulting lossless encoding of every
finite return history. This does not prove phase-witness complexity divergence,
exclude eventual center period two, or solve Rule 30 center nonperiodicity.

## 1. Packed fringe map

Let the exact two-step packed fringe update be

```text
F(s) = (o << 1) xor (o or (o >> 1)),
o    = r xor ((r >> 1) or (r >> 2)),
r    = 1 or (s << 1).
```

Define the renormalized high-front map

```text
H(x) = F(x) >> 2.
```

The shift removes the two new high-front bits created by one fringe block.
For positive finite `x`, both `x` and `H(x)` have the same bit length.

## 2. Exact triangular bit rule

Write `x_j` for bit `j`, with `x_j=0` above the finite support, and set

```text
a_j = x_j xor (x_(j+1) or x_(j+2)).
```

Direct expansion of the packed update gives

```text
H(x)_j = a_j xor (a_(j+1) or a_(j+2)).
```

Equivalently,

```text
H(x)_j = x_j xor psi_j(x_(j+1),x_(j+2),x_(j+3),x_(j+4)).
```

Thus output bit `j` is input bit `j` xor a function of strictly higher bits.
The diagonal coefficient is one.

In particular, if `d=bit_length(x)`, then

```text
H(x)_(d-1) = x_(d-1) = 1,
```

so `H` preserves the `d`-bit shell

```text
S_d = {2^(d-1),...,2^d-1}.
```

## 3. Explicit inverse and shell permutation

Given `y=H(x)`, reconstruct `x` from high bits to low bits. Suppose
`x_(j+1),...,x_(d-1)` are already known. The triangular rule has the form

```text
y_j = x_j xor known_higher_bit_expression.
```

Therefore `x_j` is uniquely determined. Descending from `j=d-1` to `0`
produces one inverse value in the same shell.

Hence:

```text
H : S_d -> S_d
```

is a permutation for every `d>=1`.

The same triangular description places `H|S_d` in the finite unitriangular
Boolean permutation group. This group is a 2-group: restricting a triangular
permutation to the higher `d-1` bits has a 2-group image by induction, and its
kernel consists only of independent lowest-bit flips and is an elementary
abelian 2-group. Consequently every cycle of `H|S_d` has power-of-two length.

## 4. Exact truncation commutation

The triangular formula also gives the one-block identity

```text
F(s) >> (m+2) = H(s >> m)
```

for every `s>=0` and every `m>=0`.

Indeed, bit `j` on either side is the same Boolean expression in source bits

```text
s_(j+m),...,s_(j+m+4).
```

Iterating yields the all-width semiconjugacy

```text
F^B(s) >> (m+2B) = H^B(s >> m)
```

for every `B,m>=0`.

## 5. Return-coordinate bridge

At a `u` return, write the packed fringe as

```text
A_0 = 4z.
```

Suppose a finite word of successive returns has total block span `B`, and let
its final packed fringe and return coordinate be

```text
A_B = F^B(A_0) = 4R.
```

Use the semiconjugacy with `s=4z` and `m=2`:

```text
F^B(4z) >> (2B+2) = H^B(z).
```

Since `F^B(4z)=4R`, this becomes

```text
R >> 2B = H^B(z).
```

This identity is independent of the particular intermediate return gaps. It
uses only their total elapsed block span.

## 6. Lossless high-front theorem

Because `H` is a shell permutation, `H^B` is invertible. Therefore the aligned
high front

```text
R >> 2B
```

recovers the complete earlier coordinate exactly:

```text
z = H^(-B)(R >> 2B).
```

Once `z` is recovered, replaying the exact first-return map recovers every
intermediate return gap and every intermediate coordinate. Thus the growing
high front is a lossless code for the complete finite return history.

This complements the low-suffix precision theorems:

- predicting `k` final low bits costs `k+2B` source bits;
- the information is not destroyed;
- it is transported into the aligned high front by the permutation `H^B`.

No fixed low suffix can replace this growing lossless front.

## 7. Controlled validation

The Python campaign checks:

- the explicit bit formula;
- the two-sided high-to-low inverse;
- bit-length preservation;
- one-block truncation commutation;
- iterated semiconjugacy;
- return-coordinate recovery and return-history replay;
- complete shell cycle decompositions.

The independent C++ campaign exhausts every positive state below `2^20`, all
shell cycles through width twenty, and separate semiconjugacy and return-bridge
ranges. Every observed cycle length is a power of two, as the group theorem
requires.

These computations are regression evidence for the separately proved
all-width identities.

## Scientific boundary

The theorem identifies exactly where finite-coordinate information moves and
provides a genuine cross-boundary bridge from low return history to the later
high front. It does not provide a bounded invariant of the unique infinite
zero-initialized front, prove that actual return penalties are positive
infinitely often, prove phase-witness complexity divergence, exclude eventual
center period two, or solve Rule 30 center nonperiodicity.
