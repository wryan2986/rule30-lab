# Period-two zero-survivor schedule coding

Status: complete informal proof of the exact schedule coding, its 2-adic
similarity and dimension, and the exclusion of eventually periodic auxiliary
schedules from ordinary finite support. These are partial structural results.
They do not prove that the actual moving-fringe schedule survivor has infinite
support and do not solve Rule 30 center nonperiodicity.

## 1. Setup

For a future period-two zero-branch schedule

```text
q=(q_0,q_1,q_2,...),  q_j in {t,u},
```

the preceding schedule-survivor theorem defines inverse zero branches

```text
B_q(y)=4 p(q(y))+3
```

and a unique survivor

```text
Phi(q)=lim_(n->infinity) B_(q_0)...B_(q_(n-1))(z).
```

The limit is independent of the terminal 2-adic value `z`. Every branch adds
exactly two digits of 2-adic agreement:

```text
v_2(B_q(a)-B_q(b))=v_2(a-b)+2.                 (1)
```

Every survivor is `3 mod 4`. If its current branch is `u`, it is `7 mod 16`;
if its current branch is `t`, it is `11 mod 16`.

Let `K=Phi({t,u}^N)` be the complete set of 2-adic states that emit zero
forever under their uniquely forced branch schedules.

## 2. Exact first-difference law

Take two schedules `q` and `r`, and suppose their first difference is at index
`n`:

```text
q_0=r_0, ..., q_(n-1)=r_(n-1),  q_n != r_n.
```

After removing their common `n` outer contractions, the remaining survivors
lie in opposite branch cylinders. One is `7 mod 16` and the other is `11 mod
16`, so their difference is `4 mod 16`. Therefore its valuation is exactly two.
Applying the common contractions and using (1) gives

```text
v_2(Phi(q)-Phi(r))=2n+2.                         (2)
```

Thus the coding is injective. More strongly, after rescaling the standard
schedule ultrametric so that schedules first differing at `n` have distance
`2^(-2n-2)`, `Phi` is an isometry onto `K`.

Equation (2) also gives the exact finite-prefix statement:

> Two schedules have the same first `n` branches if and only if their survivors
> agree modulo `2^(2n+2)`.

No finite extrapolation is involved.

## 3. Cylinder counts and Haar measure

At schedule depth `n`, there are exactly `2^n` branch words. By (2), they give
exactly `2^n` distinct survivor residues modulo

```text
2^(2n+2).
```

Each corresponding 2-adic cylinder has Haar measure `2^(-2n-2)`. Hence the
depth-`n` cover of `K` has total measure

```text
2^n * 2^(-2n-2)=2^(-n-2).
```

This tends to zero, so

```text
mu(K)=0.                                          (3)
```

The result is a measure statement only. A Haar-null set may still contain
ordinary integers, so (3) does not solve the support problem.

## 4. Compactness, perfection, and dimension

The schedule space `{t,u}^N` is compact. The exact distance law makes `Phi`
continuous, so `K` is compact. Every finite schedule prefix admits both a `t`
and a `u` continuation, producing two distinct survivors arbitrarily close to
any given survivor. Thus `K` has no isolated points and is perfect.

For the Hausdorff dimension, the depth-`n` cylinders have diameter
`2^(-2n-2)`. The cover above gives, for every `s>1/2`,

```text
2^n * (2^(-2n-2))^s -> 0,
```

so `dim_H(K)<=1/2`.

For the reverse inequality, put the fair Bernoulli measure on schedule space
and push it forward through `Phi`. A depth-`n` survivor cylinder has mass
`2^(-n)`. A 2-adic ball of radius between `2^(-2n-2)` and `2^(-2n)` meets at
most a bounded number of depth-`n` cylinders, so its mass is at most a constant
times the square root of its radius. The mass-distribution principle gives
`dim_H(K)>=1/2`. Therefore

```text
dim_H(K)=1/2.                                     (4)
```

Equivalently, `K` is an exact two-branch 2-adic Cantor set with contraction
ratio `1/4`.

## 5. Eventually periodic schedules cannot have finite survivors

Let `X_m` denote the survivor for the schedule tail beginning at block `m`.
Suppose the branch schedule is eventually periodic. Then for some `m` and
`p>=1`,

```text
(q_m,q_(m+1),...)=(q_(m+p),q_(m+p+1),...).
```

The future schedules are identical, so uniqueness gives

```text
X_m=X_(m+p).                                      (5)
```

Assume for contradiction that `X_m` is an ordinary nonnegative integer. Every
zero-emitting forward step is

```text
x_(j+1)=Q_j(P((x_j-3)/4)).
```

For a nonzero finite integer, each forward generator `T`, `P`, or `U` raises
the highest set-bit position by exactly two. Removing the forced low pair
reduces it by two, and the two generators then add four. Thus each complete
zero step raises degree by exactly two:

```text
deg(X_(j+1))=deg(X_j)+2.                          (6)
```

After `p` steps, (6) gives

```text
deg(X_(m+p))=deg(X_m)+2p,
```

contradicting (5). Every survivor is `3 mod 4`, so the zero state is not an
exception.

Therefore:

> **Eventually-periodic schedule theorem.** The zero survivor of every
eventually periodic branch schedule has infinitely many nonzero binary digits.

The same argument says that if two future schedule tails are equal, their
survivors are equal; an ordinary survivor orbit cannot return to the same
state because its degree strictly increases.

This theorem excludes a broad auxiliary class, but the actual moving-fringe
schedule has not been proved eventually periodic. A finite-support
counterexample would necessarily be coded by a genuinely aperiodic branch
schedule.

## 6. Exact explanation of the seven-block shadow

For the actual alternating moving fringe, starting at block two the branch
schedule agrees with repetitions of

```text
ttututt
```

for exactly 151 branches. The first mismatch is at global block 153.

Let `q` be the actual tail at block two and let `r` be the infinite periodic
schedule `(ttututt)^infinity`. Their first schedule difference is at relative
index 151. Equation (2) therefore gives the all-width finite identity

```text
v_2(Phi(q)-Phi(r))=2*151+2=304.                  (7)
```

The actual shift-two survivor and the periodic comparator agree in exactly
their first 304 low binary digits and differ at the next bit. This explains
why a short periodic driver looked convincing for a long time and why finite
endpoint laws built on that shadow eventually failed.

Equation (7) is a finite exact comparison. It does not make the actual schedule
periodic and does not prove anything about survivor digits above the mismatch.

## 7. Research consequence

The support problem is now split cleanly:

1. `K` contains all possible infinite zero-survivors and has exact dimension
   one half.
2. No eventually periodic branch schedule codes an ordinary integer.
3. The actual schedule is a specific aperiodic-looking path in this Cantor set.

The next admitted target is not another finite schedule prefix. It is to find
an exact property of the actual moving-fringe path that excludes its coding
point from the countable subset of ordinary integers. Candidate routes include
an all-scale recurrence for schedule cylinders, a boundary functional on the
packed fringe recurrence, or a theorem that forces recurrent nonzero survivor
pairs from a depth-independent feature of the actual schedule.
