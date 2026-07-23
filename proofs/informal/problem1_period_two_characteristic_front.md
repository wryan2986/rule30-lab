# Period-two characteristic frontier and dyadic seam recurrence

Status: complete informal proof of an exact all-width characteristic-front theorem, with bounded exhaustive regression checks. This is a partial structural result. It does not exclude eventual period two and does not solve Rule 30 center nonperiodicity.

## 1. Context

During a hypothetical final zero tail, the normalized ordinary state satisfies

```text
x_(m+1) = q_m(p(x_m >> 2)),   q_m in {t,u}.
```

The preceding multi-time bulk result proves that the branch choice affects only a bounded low-bit boundary layer. The present note studies the opposite characteristic boundary: the highest set bit and the finite word read downward from it.

For a positive ordinary integer `x`, let

```text
d(x) = bit_length(x) - 1
front(x)[j] = bit_(d(x)-j)(x),  j >= 0,
```

with `front(x)[j]=0` once `j>d(x)`. Thus `front(x)` begins with `1` and is the finite binary expansion of `x` read from high to low, followed by an infinite zero tail.

## 2. Exact reversal conjugacy

Let

```text
T(x) = x XOR ((x << 1) OR (x << 2)).
```

If `d=d(x)`, then `d(T(x))=d+2`: output bit `d+2` is the old top bit and no higher bit can be nonzero.

Define the one-sided map `E` by

```text
E(h)[j] = h[j-2] XOR (h[j-1] OR h[j]),
```

where `h[-2]=h[-1]=0`. This is Rule 30 in the high-front moving frame: its local Boolean rule is `a XOR (b OR c)`, with the output coordinate shifted so that the new highest bit remains at index zero.

For every `j>=0`,

```text
front(T(x))[j]
  = bit_(d+2-j)(T(x))
  = bit_(d+2-j)(x)
      XOR (bit_(d+1-j)(x) OR bit_(d-j)(x))
  = front(x)[j-2]
      XOR (front(x)[j-1] OR front(x)[j]).
```

Therefore

```text
front(T(x)) = E(front(x)).                         (1)
```

This is an exact identity on the complete one-sided high-front row, not a bounded approximation.

## 3. Zero-tail block theorem

The forward generators used in the normalized recurrence satisfy

```text
t(y) = T(y),
u(y) = T(y) XOR 1,
p(y) = T(y) XOR 1 XOR epsilon(y),
```

where `epsilon(y)` is either zero or bit one. Hence `p(y)` differs from `T(y)` only at bits zero and one. Applying a second `T` can propagate that difference only through bits zero to three, and the final `t/u` choice can alter only bit zero.

Let `x` be an ordinary zero-continuing state, so `x=7 mod 16` or `x=11 mod 16`, and let

```text
x' = q(p(x >> 2)).
```

Writing `d=d(x)`, the continuing degree law gives `d(x')=d+2`. For every output bit index `i>=4`,

```text
bit_i(x') = bit_i(T^2(x >> 2)).
```

Equivalently, in high-front coordinates,

```text
front(x')[j] = E^2(front(x))[j]    for 0 <= j <= d-2.   (2)
```

Thus the complete high frontier, apart from the final four cells adjacent to the low boundary, is independent of the actual branch `q`. During an infinite zero tail, every fixed high-front window eventually lies permanently inside the safe region and thereafter evolves exactly by `E^2`.

## 4. Dyadic temporal recurrence of fixed frontier windows

Write `c_j(s)=E^s(h)[j]` for the temporal column at high-front coordinate `j`.

The recurrence is

```text
c_j(s+1)
  = c_(j-2)(s) XOR (c_(j-1)(s) OR c_j(s)).          (3)
```

Assume columns `j-2` and `j-1` are eventually periodic with a common power-of-two period `P`. Over one `P`-step block, the map from the starting value of `c_j` to its ending value is a composition of unary Boolean maps. Each one-step map is either constant, the identity, or a flip:

- if `c_(j-1)(s)=1`, the new value is independent of `c_j(s)`;
- if `c_(j-1)(s)=0`, the new value is `c_j(s)` XOR `c_(j-2)(s)`.

Consequently the `P`-step return map on one bit is constant, identity, or flip. After at most one such block, column `j` is periodic with period dividing `2P`.

Starting from the two fixed zero columns to the left, induction gives

```text
column j is eventually periodic with period dividing 2^(j+1).   (4)
```

Therefore a fixed prefix of width `r` is eventually periodic under `E`, and hence under the block map `E^2`, with a power-of-two period dividing `2^r`.

Combining this with (2), a hypothetical ordinary final-zero orbit has the following exact seam property:

> For every fixed frontier width `r`, there are a block time `M_r` and a power of two `P_r <= 2^r` such that
>
> ```text
> front_r(x_(m+P_r)) = front_r(x_m)
> ```
>
> for every `m>=M_r`.

This is the first exact growing-lag recurrence on the opposite characteristic boundary.

The argument is a direct specialization of the positional-bijectivity mechanism studied by Eric Rowland in *Local Nested Structure in Rule 30* (Complex Systems 16 (2006), 239-258), but the conjugacy (1) and its use in the period-two normalized strip are stated here explicitly.

## 5. What the theorem does and does not connect

Earlier work proved that under a finite-seed alternating-center hypothesis, the low `t/u` branch schedule is genuinely non-eventually-periodic: it is the even-time trace of a neighboring Rule 30 cell, and an eventually periodic schedule would make a width-two trace eventually periodic.

The present result gives the opposite boundary behavior:

```text
high characteristic boundary:
    every fixed window is eventually dyadically periodic;

low characteristic boundary:
    the actual branch schedule is genuinely aperiodic;

interior:
    the common multi-time bulk is right permutive and constructively free.
```

There is no contradiction between these statements. The high-front window is fixed in characteristic coordinates, while the low branch sits at a boundary receding from it as the ordinary state grows by two bits per block. Increasing a fixed high-front width only enlarges a finite periodic subsystem; it does not bridge the growing middle.

In fact, (1) shows that the characteristic frontier is not a simpler auxiliary system: it is another exact Rule 30 evolution. A proof based only on this boundary would re-embed Rule 30 rather than reduce it.

## 6. Finite regression campaign

The accompanying analyzer independently checks:

- `front(T(x)) = E(front(x))` for every positive integer through the configured bit width;
- the exact branch-independent safe prefix (2) for every zero-cylinder state through the configured width;
- all finite prefix functional graphs through the configured width, verifying that every observed cycle period is a power of two and respects the inductive bound.

These checks validate the implementation. The all-width claims are the elementary bit-index and unary-return-map arguments above.

## 7. Scientific boundary and next target

This result does not prove that the alternating inverse lift has infinite support, does not exclude eventual center period two, and does not solve Rule 30 center nonperiodicity.

It closes another one-boundary strategy. The next useful quantity must be **cross-characteristic**: it must simultaneously couple the dyadically recurrent high frontier to the aperiodic actual low boundary across a width that grows with time. Candidate forms include:

1. a two-boundary communication or rank lower bound for the complete strip;
2. a nonlocal spacetime parity/determinant whose boundary terms live on both characteristics;
3. a theorem showing that the actual low schedule is incompatible with every finite high-front initial row, rather than with every locally allowed boundary word.

A wider fixed frontier, a longer finite branch prefix, or another independent boundary statistic is not enough.
