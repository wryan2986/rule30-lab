# Period-two multi-time bulk and bounded-lag obstruction

Status: complete informal proof of an exact all-width bulk theorem, together
with bounded exhaustive checks. This is a partial structural result. It does
not exclude eventual period two and does not solve Rule 30 center
nonperiodicity.

## 1. Context

During a hypothetical final zero tail, the normalized ordinary state obeys

```text
x_(m+1) = R_(q_m)(x_m) = q_m(p(x_m >> 2)),
```

where `q_m` is `t` or `u` and the lowercase notation denotes the forward maps
inverse to the inverse-tree letters. In integer form, with

```text
T(x) = x XOR ((x << 1) OR (x << 2)),
```

the three forward generators are

```text
t(x) = T(x),
u(x) = T(x) XOR 1,
p(x) = T(x) XOR 1 XOR (2 if x is even else 0).
```

Earlier work studied one seam at a time or compared fixed-width views of the
two ends. The proposed continuation was to compare two moving seams `m<n` and
use the complete intervening schedule block. The theorem below identifies the
exact information carried by such a comparison when the lag `k=n-m` is fixed.

## 2. The branch-independent bulk rule

Write the binary digits of `x` as `x_i`, indexed from low to high. Fix an
output index `i>=4` and abbreviate

```text
(a,b,c,d,e) = (x_(i-2), x_(i-1), x_i, x_(i+1), x_(i+2)).
```

Let `z=x>>2`. The correction distinguishing `p(z)` from `T(z)` is supported
only in bits zero and one. Applying the outer generator `q` adds only another
bit-zero correction. A bit below position two can influence at most positions
zero through three under one further application of `T`. Therefore, for every
`q in {t,u}` and every `i>=4`,

```text
R_q(x)_i = T^2(z)_i.
```

Expanding the two Rule 30 right-edge steps gives the exact radius-two Boolean
rule

```text
Phi(a,b,c,d,e)
  = [e XOR (d OR c)]
      XOR
    ([d XOR (c OR b)] OR [c XOR (b OR a)]).
```

Its algebraic normal form over `GF(2)` is

```text
a + b + ab + ac + bc + abc + ad + bd + abd + e.
```

In particular, `e` occurs exactly once and in no product term. Hence

```text
Phi(a,b,c,d,0) != Phi(a,b,c,d,1)
```

for every fixed `(a,b,c,d)`: the bulk rule is **right permutive**.

This proves that the actual `t/u` branch enters one normalized step only
through a four-bit low boundary layer. Every higher bit follows the same
radius-two cellular rule `Phi`.

## 3. Exact k-block causal cone

Let

```text
R_w = R_(q_(k-1)) ... R_(q_1) R_(q_0)
```

for any branch word `w=q_0...q_(k-1)` of length `k`.

### Theorem 1: branch-independent interior

For every `k>=1` and every output index

```text
i >= 2k+2,
```

the bit `R_w(x)_i` is independent of the complete branch word `w`. It is the
`i`th bit obtained by applying `Phi` exactly `k` times, and it depends only on

```text
x_(i-2k), ..., x_(i+2k).
```

### Proof

For one step this is the preceding calculation. For `k` steps, trace the
radius-two dependency cone backward. At the first normalized update the
smallest intermediate index that can influence final bit `i` is

```text
i-2(k-1).
```

The inequality `i>=2k+2` makes this index at least four, so the entire first
layer of the cone lies outside the branch-dependent boundary. The same
argument applies recursively to every earlier layer. Each layer expands the
initial dependency interval by two cells on each side, giving the stated
interval of width `4k+1`. QED.

This is the exact two-seam identity in the interior: a fixed lag does not carry
the intervening actual schedule through the full state. It carries it only in
a lower cone of width linear in the lag.

## 4. Right permutivity survives every scale

Let `Phi^k_i` denote output position `i` after `k` bulk steps.

### Theorem 2: extreme-input permutivity

For every `k>=1`, `Phi^k_i` is permutive in the extreme-right input bit

```text
x_(i+2k).
```

### Proof

The claim for `k=1` is right permutivity of `Phi`. Assume it for `k`. At the
next step,

```text
Phi^(k+1)_i = Phi(
  Phi^k_(i-2),
  Phi^k_(i-1),
  Phi^k_i,
  Phi^k_(i+1),
  Phi^k_(i+2)).
```

The extreme bit `x_(i+2k+2)` occurs only in `Phi^k_(i+2)`. By induction that
argument is permutive in the extreme bit, and the outer `Phi` is permutive in
its rightmost argument. Their composition is permutive. QED.

## 5. Constructive block surjectivity

Fix a later target interval

```text
I = [a, a+r-1]
```

inside the safe bulk. Its complete earlier dependency rectangle is

```text
[a-2k, a+r-1+2k].
```

Fix every bit in that rectangle except

```text
x_(a+2k), x_(a+1+2k), ..., x_(a+r-1+2k).
```

Then every target word of length `r` on `I` has a unique assignment to those
`r` free bits.

To construct it, process target positions from left to right. At position
`a+j`, Theorem 2 makes the new bit `x_(a+j+2k)` toggle that output. Bits chosen
later lie strictly to the right of the dependency cone of all earlier target
positions, so they cannot change outputs already fixed.

Thus even after all other earlier bits in the dependency rectangle are fixed,
an arbitrary later interior word remains realizable.

## 6. Consequence for the moving-seam strategy

Suppose a proposed contradiction compares seams `m` and `m+k` using:

- a fixed-width low schedule cylinder;
- a fixed-width high frontier or finite-support boundary;
- and local relations across the `k` intervening blocks.

When `k` is bounded and the state width grows, the two causal boundary cones
leave an arbitrarily wide middle. Theorem 2 and the constructive solver show
that this middle is not merely unknown: every finite target word remains
compatible with the fixed surrounding context.

Therefore:

> No bounded-lag local multi-time seam identity can bridge the free middle or
> distinguish an ordinary finite survivor from a 2-adic survivor.

This extends the earlier single-time frontier-gluing obstruction to exact
multi-time dynamics. A successful continuation must use at least one of:

1. a lag growing with the seam or state width;
2. a genuinely nonlocal quantity spanning the whole spacetime strip;
3. an identity special to the unique zero-initialized fringe orbit; or
4. an external theorem controlling long directional traces.

## 7. Finite verification

The accompanying analyzer independently checks:

- every residue below `2^14`, both branches, and all safe one-step bits;
- the complete 32-entry truth table and all 16 right-permutivity contexts;
- every branch word and every local input cone through lag three, totaling
  67,648 exact cone comparisons;
- constructive realization of every target word through width five in three
  fixed contexts at every lag through three, totaling 558 solver checks.

These checks validate the implementation. The all-width claims are the
Boolean dependency and permutivity proofs above.

## 8. Scientific boundary

This result does **not** analyze lags that grow proportionally to the complete
state width. It does not provide a nonlocal invariant, prove that the actual
survivor has infinite support, exclude eventual center period two, or solve
Rule 30 center nonperiodicity.
