# Period-two return-gap rigidity reduction

## 1. Purpose

The period-two zero-tail problem has been reduced to exact nonnegative witness
penalties at successive `u` returns of the zero-initialized moving-fringe
schedule. This note asks whether the return **gap alone**, together with the
three proved finite fringe-language exclusions, already forces a positive
penalty.

The answer is mixed:

- gap `2` genuinely permits both zero and positive penalties;
- every locally admissible gap `3`, `4`, or `5` candidate whose final depth is
  at most twelve has positive penalty in both phases;
- an all-depth proof of that non-two-gap positivity would exclude a finite
  period-two survivor immediately.

The last statement is an exact conditional theorem. The bounded campaign is
not promoted to that theorem.

## 2. Schedule cylinders and phase distance

For a finite branch word

```text
w=q_0 q_1 ... q_(L-1),  q_i in {t,u},
```

let `Phi_L(w)` be the unique zero-survivor cylinder residue modulo `4^L`.
Using the inverse zero branches,

```text
B_q(y)=4 p(q(y))+3,
```

it is computed exactly by

```text
Phi_L(w)=B_(q_0) B_(q_1) ... B_(q_(L-1))(0) mod 4^L.
```

For phase `a in {p,u}`, let

```text
kappa_a(w)
```

be the shortest normalized phase-`a` positive-generator word whose ordinary
arithmetic state equals `Phi_L(w)` modulo `4^L`.

Equivalently, if `d_L` is directed distance in the arithmetic quotient graph

```text
x -> t(x), p(x), u(x) mod 4^L,
```

then

```text
kappa_p(w)=1+d_L(3,Phi_L(w)),
kappa_u(w)=1+d_L(1,Phi_L(w)).
```

## 3. Return extensions

Assume `w` ends in `u`. A next `u` return at gap `r` appends

```text
e_r = t^(r-1) u.
```

The exact fringe-language theorem confines actual gaps to

```text
r in {2,3,4,5}.
```

Define the phase penalty

```text
delta_a(w,r)=kappa_a(w e_r)-kappa_a(w).
```

Projection from modulus `4^(L+r)` to modulus `4^L` proves

```text
delta_a(w,r) >= 0.
```

No computation is needed for this monotonicity.

## 4. The conditional gap-two collapse theorem

Suppose the following statement were proved for one phase `a`:

> Every actual return of gap `3`, `4`, or `5` has positive phase-`a` penalty.

If phase-`a` witness complexity were bounded, the return-block penalty theorem
would force all sufficiently late penalties to vanish. Therefore all
sufficiently late return gaps would have to equal `2`.

A gap-two return word is

```text
u t u.
```

Consecutive gap-two returns therefore make the auxiliary branch schedule
repeat

```text
u t u t u t ...
```

after some finite prefix. The schedule is eventually periodic.

The exact schedule-coding theorem already proves that no eventually periodic
branch schedule can code an ordinary finite-support zero survivor: survivor-tail
uniqueness would repeat a state, while every ordinary continuing zero step
raises its highest set-bit degree by two.

Consequently:

```text
all-depth positivity on non-two returns
    => bounded phase complexity is impossible
    => no finite survivor exists in that phase.
```

Proving the lemma in both phases would close the remaining period-two path.

## 5. Why gap two cannot be discarded

The exhaustive quotient calculation finds both outcomes at gap two while all
three known fringe exclusions are enforced.

Examples include:

```text
phase p, zero penalty: prefix utu, extension tu
phase p, positive penalty: prefix u, extension tu
phase u, zero penalty: prefix u, extension tu
phase u, positive penalty: prefix tu, extension tu
```

Thus a theorem saying merely that *every* return costs a letter is false.
Any successful argument must retain enough witness-side information to
separate zero-cost and positive-cost gap-two returns.

## 6. Complete controlled campaign through final depth twelve

The independent C++ analyzer computes every arithmetic quotient exactly for
all final depths through twelve. It enumerates every prefix ending in `u`
whose full return extension avoids

```text
uu
ttttt
ututtu
```

and classifies the exact phase penalty.

### Gap 2

```text
phase p: 93 candidates, 4 zero, 89 positive
phase u: 93 candidates, 10 zero, 83 positive
```

### Gap 3

```text
phase p: 35 candidates, all positive, minimum penalty 1
phase u: 35 candidates, all positive, minimum penalty 3
```

### Gap 4

```text
phase p: 42 candidates, all positive, minimum penalty 4
phase u: 42 candidates, all positive, minimum penalty 5
```

### Gap 5

```text
phase p: 28 candidates, all positive, minimum penalty 6
phase u: 28 candidates, all positive, minimum penalty 7
```

These are complete finite statements for the declared depth bound. They do
not imply the corresponding all-depth lemma.

## 7. Actual return evidence

The exact actual phase-distance table through depth 22 resolves the first six
complete `u`-return intervals, ending at depth 21:

```text
return  depths   gap   p penalty   u penalty
0       1 -> 5    4        7          10
1       5 -> 7    2        5           2
2       7 -> 12   5       15          13
3      12 -> 14   2        5           3
4      14 -> 19   5        9          12
5      19 -> 21   2        7          10
```

All twelve phase penalties are positive. Again, this is finite exact evidence,
not a recurrence theorem.

## 8. What the calculation rules out

The campaign rules out the simplest finite-horizon counterexamples to the
non-two-gap lemma and shows that the gap-two exception is real. It also shows
that the three known forbidden factors are strong enough to remove every
zero-cost gap-three example found in the unrestricted depth-twelve search.

It does **not** show that the forbidden factors alone determine penalty. The
penalty is a geodesic property of the arithmetic quotient and depends on the
witness-side state, not only on the schedule suffix.

## 9. Next admitted target

The next proof target is now sharply stated:

1. Define a depth-independent state carried by a shortest phase witness at a
   `u` return.
2. Derive its exact update under the four return words of lengths `2..5`.
3. Prove that the gap-`3`, gap-`4`, and gap-`5` updates cannot preserve the
   minimizing stratum.
4. Leave gap `2` as the only possible zero-cost transition.
5. Invoke the conditional gap-two collapse theorem and the existing
   eventually-periodic schedule obstruction.

A finite prefix extension without such a state recurrence would not establish
the missing lemma.

## 10. Scientific boundary

This note does not prove all-depth positivity for gaps `3`, `4`, or `5`. It
does not prove either phase complexity diverges, does not prove the alternating
inverse lift has infinite support, does not exclude eventual center period two,
and does not solve Rule 30 center nonperiodicity.
