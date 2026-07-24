# Period-two pre-branch cylinders and the first consecutive-free return counterexample

Status: complete proof of the pre-branch cylinder rule and an exact bounded
counterexample to the proposed universal isolated-zero return lemma. This is a
partial structural and no-go result. It does not construct a finite survivor for
the actual moving-fringe schedule, exclude eventual center period two, or solve
Rule 30 center nonperiodicity.

## 1. Why the return branch is invisible at its own depth

Let `Phi(q)` be the unique 2-adic zero survivor for a branch schedule

```text
q=q_0 q_1 q_2 ... ,  q_i in {t,u}.
```

The established first-difference theorem says that schedules first differing at
branch `n` have survivors whose difference has exact valuation

```text
v_2(Phi(q)-Phi(r))=2n+2.
```

Consequently the residue modulo `4^L=2^(2L)` is determined by

```text
q_0,...,q_(L-2),
```

but not by `q_(L-1)`. Equivalently, two length-`L` words that differ only in
their final branch define the same survivor residue modulo `4^L`.

This is the **pre-branch cylinder rule**: depth `L=n+1` is the cylinder just
before branch `q_n` becomes visible. At a `u` return position `n_j`, the depth
used in the return-penalty analysis is

```text
L_j=n_j+1,
```

so the current return branch `q_(n_j)=u` is not yet fixed by the base residue.

## 2. Ordinary phase frontiers

For phase `a in {p,u}`, let `O_(a,k)` be the set of distinct ordinary integers
obtained by a positive generator word of total length `k` whose first letter is
`a`. Thus

```text
O_(p,1)={3},
O_(u,1)={1},
```

and

```text
O_(a,k+1)={t(x),p(x),u(x): x in O_(a,k)}.
```

For every positive integer `x`, each generator raises bit length by exactly two.
Therefore

```text
bitlen(x)=2k     for x in O_(p,k),
bitlen(x)=2k-1   for x in O_(u,k).
```

Different complexity levels are disjoint. Enumerating the ordinary frontier in
increasing `k` is therefore an exact complexity enumeration, not a heuristic
word search.

An ordinary state can continue a terminal-zero block exactly when it is `7` or
`11 mod 16`. Its next forced branch and successor are

```text
7 mod 16  -> u,
11 mod 16 -> t,

x' = q(p((x-3)/4)).
```

Iterating this rule gives the complete finite forced zero schedule `sigma(x)`.

Combining this with the first-difference theorem gives:

> **Frontier-cylinder theorem.** An ordinary phase-`a` output `x` represents the
> depth-`L` survivor cylinder of a length-`L` branch word `w` exactly when
>
> ```text
> x = 3 mod 4
> ```
>
> and `sigma(x)` begins with `w` with its final branch deleted.

Hence `kappa_a(w)` is the first frontier level containing such an output.

## 3. Correct translation of two return penalties

Suppose a base return is at depth `L_j=n_j+1`, and the next two return gaps are
`r` and `s`. The complete branch word through the third return is

```text
base_prefix + u t^(r-1) u t^(s-1) u.
```

The final `u` is invisible modulo `4^(L_(j+2))`. Thus a base-minimal ordinary
output has zero total two-return penalty exactly when its forced schedule,
starting at the pre-branch cut, contains

```text
u t^(r-1) u t^(s-1),
```

while the full word obtained by appending the final `u` is an allowed branch
word.

This corrects a tempting but wrong translation requiring three visible future
`u` events. Only the first two return branches are visible in the deeper target
residue.

## 4. Exact counterexample

The complexity-25 phase-`u` frontier contains

```text
x = 489092214423035
  = 0x1bcd3a7b3fdfb.
```

It has bit length 49, exactly `2*25-1`, and forced zero schedule

```text
tutututttutututt.
```

Consider the locally admissible words

```text
w_12 = tutututttutu,
w_14 = tutututttututu,
w_16 = tutututttutututu.
```

They differ by two successive gap-two return blocks. Direct exact computation
gives

```text
x mod 4^12 = 0x00b3fdfb = X(w_12),
x mod 4^14 = 0x07b3fdfb = X(w_14),
x mod 4^16 = 0xa7b3fdfb = X(w_16).
```

The independent ordinary-frontier campaign exhausts every phase-`u` output at
complexities 1 through 24 and finds none in even the base cylinder. At
complexity 25 the displayed `x` is the first base representative and also lies
in both deeper cylinders. Projection monotonicity then gives

```text
kappa_u(w_12)=kappa_u(w_14)=kappa_u(w_16)=25.
```

Both consecutive single-return penalties vanish, and so does their two-return
sum.

The word `w_16` avoids all three established local exclusions:

```text
uu,
ttttt,
ututtu.
```

Therefore those local exclusions alone cannot prove that zero return penalties
are isolated.

## 5. Controlled frontier campaign

The C++ analyzer exhausts both ordinary phase frontiers through complexity 25:

```text
phase p outputs:  9,118,715
phase u outputs:  7,745,997
total:           16,864,712
```

Among them, 4,831,012 outputs are congruent to `3 mod 4` and therefore eligible
for a survivor cylinder. Every forced zero schedule terminates before the
48-step safety cap; the maximum observed complete schedule length is 19.

The campaign finds exactly one locally admissible zero two-return candidate:

the phase-`u`, complexity-25 state above, with pre-branch prefix
`tutututttut` and gap pair `(2,2)`.

The result is independent of the earlier depth-14 quotient campaign. The two
campaigns are consistent: the first counterexample has final depth 16, beyond
the earlier cutoff.

## 6. Research consequence

The generic isolated-zero conjecture is false. A successful continuation must
use information specific to the actual zero-initialized fringe orbit, not only:

- the return gaps `2..5`;
- the factors `uu`, `ttttt`, and `ututtu`;
- or generic phase-minimality.

Possible next states to couple are the exact fringe return coordinate, a
higher-order return residue, or a joint state combining the actual fringe with
the minimizer frontier. The counterexample does not show that the actual orbit
has a zero two-return penalty and does not weaken any exact actual-distance
value already proved.
