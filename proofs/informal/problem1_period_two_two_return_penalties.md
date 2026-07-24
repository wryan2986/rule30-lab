# Period-two two-return penalty criterion

Status: complete informal proof of an exact two-return telescoping and divergence
criterion, together with a finite exhaustive classification through final depth
fourteen. This is a partial result. It does not prove the required all-depth
positivity statement, exclude eventual center period two, or solve Rule 30
center nonperiodicity.

## 1. Context

For each phase `a in {p,u}`, let `kappa_a(L)` be the minimum normalized
phase-`a` positive-generator word length reaching the actual schedule-survivor
cylinder modulo `4^L`.

At successive `u` positions of the moving-fringe schedule, write

```text
0=n_0<n_1<n_2<...
L_j=n_j+1,
r_j=n_(j+1)-n_j in {2,3,4,5}.
```

The preceding return-block theorem defined the single-return penalty

```text
delta_(a,j)=kappa_a(L_(j+1))-kappa_a(L_j) >= 0.
```

The inequality is exact quotient projection: every word reaching the deeper
survivor cylinder also reaches its projection at the shallower depth.

A bounded phase complexity would force all sufficiently late single-return
penalties to vanish. The last campaign showed that gap two genuinely admits
zero penalties, so the stronger statement that every return has positive
penalty is false for general locally admissible prefixes.

This note groups two returns at a time.

## 2. Two-return penalty

Define

```text
Delta_(a,j)=kappa_a(L_(j+2))-kappa_a(L_j).
```

Insert the intermediate return depth:

```text
Delta_(a,j)
 = [kappa_a(L_(j+2))-kappa_a(L_(j+1))]
   +[kappa_a(L_(j+1))-kappa_a(L_j)].
```

Therefore

```text
Delta_(a,j)=delta_(a,j)+delta_(a,j+1) >= 0.       (1)
```

This is an all-depth identity. No finite computation enters its proof. Since
both summands are nonnegative integers,

```text
Delta_(a,j)=0
iff delta_(a,j)=delta_(a,j+1)=0.                 (2)
```

Thus a zero two-return penalty is exactly a pair of consecutive zero
single-return penalties.

## 3. Divergence criterion

### Theorem

Suppose there is an index `J_0` such that

```text
Delta_(a,j) >= 1
```

for every `j>=J_0`. Then `kappa_a(L_j)` is unbounded. More precisely,

```text
kappa_a(L_J)
 >= kappa_a(L_(J_0)) + floor((J-J_0)/2).          (3)
```

### Proof

Use the disjoint two-return windows

```text
J_0 -> J_0+2,
J_0+2 -> J_0+4,
...
```

Each contributes at least one by hypothesis. Summing the corresponding
instances of (1) proves (3). QED.

Equivalently, proving that zero single-return penalties cannot occur on two
consecutive actual returns is sufficient for phase-complexity divergence.
This criterion is strictly weaker than proving every non-two return has
positive penalty. It permits isolated zero penalties at any gap, including the
known gap-two exceptions.

If the criterion holds in both phases, neither fixed zero phase can contain a
finite survivor, so the remaining period-two case is excluded.

## 4. Finite gap-pair formulation

For a finite locally admissible branch prefix `w` ending in `u`, let the next
two return gaps be `r,s`. The complete extension is

```text
w t^(r-1) u t^(s-1) u.
```

For phase `a`, define

```text
Delta_a(w;r,s)
 = kappa_a(w t^(r-1) u t^(s-1) u)-kappa_a(w).     (4)
```

Projection through the intermediate prefix gives

```text
Delta_a(w;r,s)
 = delta_a(w;r)
   +delta_a(w t^(r-1)u;s).                        (5)
```

The established fringe language has return gaps in `{2,3,4,5}`. Its exact
return-pair language contains every ordered pair except `(2,3)`. A gap-two
return followed by a gap-three return contains the already proved forbidden
schedule factor `ututtu`.

The finite classifier constructs extensions directly and rejects every word
containing any of the three established factors

```text
uu,
ttttt,
ututtu.
```

It therefore does not assume the return-pair theorem as an implementation
shortcut.

## 5. Exact exhaustive method

At final depth `D`, the arithmetic quotient has `4^D` states. For each phase,
the analyzer performs complete breadth-first search in the directed graph

```text
x -> t(x), p(x), u(x) mod 4^D.
```

Every generator is evaluated exactly with integer bit operations. The reverse
schedule contractions construct the unique survivor residue for each tested
prefix.

For every base depth and every locally admissible prefix ending in `u`, the
analyzer:

1. constructs each possible two-return extension `(r,s)`;
2. computes the exact phase complexity at the base and final cylinders;
3. checks the two intermediate single-return penalties are nonnegative;
4. checks equation (5) exactly;
5. records the complete penalty histogram.

The C++ campaign stores full quotient distances through final depth fourteen.
This is finite exhaustive computation, not sampling.

## 6. Depth-fourteen result

Across all fifteen locally possible return-gap pairs, both phases have strictly
positive two-return penalty through final depth fourteen. The pair `(2,3)` has
no locally admissible instance, as required by `ututtu`.

The minimum penalties observed for the remaining pairs are:

| gaps `(r,s)` | phase `p` | phase `u` |
|---|---:|---:|
| `(2,2)` | 1 | 3 |
| `(2,4)` | 6 | 8 |
| `(2,5)` | 12 | 12 |
| `(3,2)` | 5 | 5 |
| `(3,3)` | 11 | 10 |
| `(3,4)` | 11 | 11 |
| `(3,5)` | 15 | 18 |
| `(4,2)` | 8 | 10 |
| `(4,3)` | 8 | 12 |
| `(4,4)` | 12 | 14 |
| `(4,5)` | 15 | 17 |
| `(5,2)` | 8 | 9 |
| `(5,3)` | 15 | 15 |
| `(5,4)` | 18 | 17 |
| `(5,5)` | 18 | 22 |

The weakest pair is `(2,2)`, exactly where isolated zero-cost single returns
were already known. Nevertheless, its total cost is still positive in both
phases.

The complete campaign contains

```text
414 prefix/gap-pair cases per phase,
828 phase cases total,
0 zero two-return penalties.
```

This includes every locally admissible prefix whose completed pair of returns
ends by depth fourteen.

## 7. Better infinite target

The prior candidate lemma asked for positivity at every return of gap three,
four, or five. That statement may be stronger than necessary and does not
explain the structure of gap-two exceptions.

The new target is the isolated-zero lemma:

```text
for each phase, two consecutive actual return penalties cannot both vanish.
```

An all-depth proof would immediately imply divergence by Section 3. It would
also tolerate arbitrary isolated zero-cost returns of any gap.

The likely proof object is the geodesic lift set. A zero penalty means that a
shortest word for the current survivor cylinder also reaches the entire next
return cylinder at the same length. Two consecutive zero penalties mean one
base shortest word survives both nested lift restrictions. The bounded
campaign says this never occurs through depth fourteen, even though the first
restriction alone can be free.

A successful continuation should therefore track the shortest-word set through
two nested return contractions, rather than classify the gap label alone.

## 8. Validation

The focused Python suite checks exact generator/inverse round trips, the
forbidden `(2,3)` return pair, absence of zero two-return penalties in the
bounded reference campaign, positive `(2,2)` total penalty in both phases,
exact telescoping, and deterministic certificate stability.

The independent C++ campaign through depth fourteen records every pair/phase
histogram and reports a deterministic output hash in the result record.

## 9. Scientific boundary

The depth-fourteen result is finite. It does not prove the isolated-zero lemma
at arbitrary depth. Consequently it does not prove phase-complexity divergence,
prove that the alternating inverse lift has infinite support, exclude eventual
center period two, or solve Rule 30 center nonperiodicity.

The exact progress is the all-depth two-return criterion and the complete
elimination of consecutive zero penalties in the largest direct quotient
campaign currently practical.
