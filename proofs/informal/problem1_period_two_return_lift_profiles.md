# Period-two return-block witness lift profiles

## Scope

This note groups the one-pair witness-lift theorem along the exact successive
`u` returns of the zero-initialized moving-fringe schedule.

The result is an all-depth reduction of phase witness divergence to a sequence
of nonnegative integer **return penalties**. It does not prove that those
penalties are positive infinitely often, does not exclude eventual center
period two, and does not solve Rule 30 center nonperiodicity.

## 1. Background and notation

Let

```text
q_0,q_1,q_2,... in {t,u}
```

be the actual period-two moving-fringe driver. The exact fringe-language
theorem proves the all-time exclusions

```text
uu,
ttttt.
```

Consequently `u` occurs infinitely often. Write its positions as

```text
0=n_0<n_1<n_2<...
```

and its return gaps as

```text
r_j=n_(j+1)-n_j in {2,3,4,5}.
```

Let `X` be the actual zero-survivor and

```text
X_L = X mod 4^L.
```

For a fixed normalized phase `a in {p,u}`, let `kappa_a(L)` be the minimum
normalized word length reaching `X_L` in the positive arithmetic generator
graph modulo `4^L`.

The driver letter `q_n` controls pair position `n+1`, because pair zero is the
universal low pair `3`. It is therefore natural to set

```text
L_j=n_j+1.
```

Then

```text
L_(j+1)=L_j+r_j.
```

## 2. Return-block lift profile

For a return interval `j`, phase `a`, and block code

```text
0 <= c < 4^r_j,
```

define

```text
Gamma_a(j,c)
```

as the minimum normalized phase-`a` word length reaching

```text
X_(L_j) + c 4^L_j  mod 4^L_(j+1).
```

The code is written in low-to-high base-four order: its `r_j` digits are the
candidate pair block between depths `L_j` and `L_(j+1)-1`.

The actual block code is

```text
c_j = (X_(L_(j+1))-X_(L_j))/4^L_j.
```

## 3. Projection theorem

For every return interval, phase, and block code,

```text
Gamma_a(j,c) >= kappa_a(L_j).
```

Indeed, reduction modulo `4^L_j` sends every block-lift target to `X_(L_j)`.
Any word reaching a lift therefore reaches the base target after projection.

Conversely, let `W` be a shortest phase-`a` word reaching `X_(L_j)`. Applying
the same word modulo `4^L_(j+1)` produces one and only one block code `c` above
that base residue. Hence

```text
min_c Gamma_a(j,c) <= |W| = kappa_a(L_j).
```

Combining the two inequalities gives the exact identity

```text
min_c Gamma_a(j,c) = kappa_a(L_j).              (1)
```

The actual code `c_j` selects `X_(L_(j+1))`, so by definition

```text
Gamma_a(j,c_j) = kappa_a(L_(j+1)).              (2)
```

No finite computation is used in this proof.

## 4. Return penalties and telescoping

Define the phase-`a` return penalty

```text
delta_(a,j) = Gamma_a(j,c_j)-min_c Gamma_a(j,c).
```

Equations (1) and (2) give

```text
delta_(a,j)
  = kappa_a(L_(j+1))-kappa_a(L_j)
  >= 0.                                             (3)
```

Therefore, for every `J>=1`,

```text
kappa_a(L_J)
  = kappa_a(L_0) + sum_(j=0)^(J-1) delta_(a,j).    (4)
```

This is the exact return-block telescoping law.

Because the penalties are nonnegative integers, the following statements are
equivalent for either fixed phase:

1. `kappa_a(L)` is bounded;
2. the sum of the return penalties is finite;
3. `delta_(a,j)=0` for every sufficiently large return `j`;
4. the actual block code is eventually a minimizing return lift at every `u`
   return.

The earlier boundedness criterion then identifies these conditions with the
existence of one ordinary finite phase-`a` zero survivor.

Thus eventual center period two is excluded once one proves, for both phases,
that positive return penalties occur infinitely often. Since every block span
is only `2`, `3`, `4`, or `5`, this replaces arbitrary-depth increments by a
bounded-span but moving-base problem.

## 5. Exact initial return profiles

The controlled campaign exhausts every block-lift target for the first three
actual `u` returns.

### Return 0

```text
driver positions: 0 -> 4
base depths:      1 -> 5
gap:              4
actual block:     [1,0,3,2] low-to-high
actual code:      177
```

```text
phase p: minimum 1, actual 8, penalty 7,  one minimizer
phase u: minimum 2, actual 12, penalty 10, one minimizer
```

### Return 1

```text
driver positions: 4 -> 6
base depths:      5 -> 7
gap:              2
actual block:     [1,0]
actual code:      1
```

```text
phase p: minimum 8,  actual 13, penalty 5, one minimizer
phase u: minimum 12, actual 14, penalty 2, two minimizers
```

### Return 2

```text
driver positions: 6 -> 11
base depths:      7 -> 12
gap:              5
actual block:     [1,1,0,0,3]
actual code:      773
```

```text
phase p: minimum 13, actual 28, penalty 15, one minimizer
phase u: minimum 14, actual 27, penalty 13, two minimizers
```

The cumulative penalties through depth twelve are therefore

```text
p: 7+5+15 = 27 = kappa_p(12)-kappa_p(1),
u: 10+2+13 = 25 = kappa_u(12)-kappa_u(1).
```

All six initial phase-return penalties are strictly positive. This is exact
finite evidence for the proposed infinite route, not an all-return theorem.

## 6. Independent certificates

The Python analyzer computes the first two return profiles by default and may
be run through all three controlled returns:

```bash
python3 experiments/problem1_nonperiodicity/\
analyze_period_two_return_lift_profiles.py --maximum-returns 3
```

The C++ analyzer independently exhausts all three profiles:

```bash
g++ -O3 -std=c++20 \
  experiments/problem1_nonperiodicity/analyze_period_two_return_lift_profiles.cpp \
  -o /tmp/rule30-return-lifts
/tmp/rule30-return-lifts 3
```

The complete profile arrays are represented by deterministic digests and exact
distance histograms. The controlled C++ output hash is recorded in the result
file.

## 7. Remaining target

The exact unresolved statement is now:

> For each phase `a in {p,u}`, the actual return block `c_j` is a
> non-minimizing coordinate of `Gamma_a(j,.)` for infinitely many `j`.

A stronger uniform statement—positive penalty at every return—would immediately
prove divergence, but the current work establishes it only for the first three
returns. A viable continuation should transport the minimizing block set
through the exact four-bit fringe return selector or through the whole-word
section recurrence, rather than extending the finite table without a closure
argument.
