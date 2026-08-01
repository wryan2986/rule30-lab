# Period-two residual profile refinement

## Purpose

The exact weighted shadow recursion retains concrete current and shadow endpoints. A finite proof would become possible if those endpoint pairs admitted a finite, realization-consistent continuation state.

The one-step endpoint profile does not have that property: equal one-step profiles can have different two-digit synchronized/full continuation languages. The present refinement removes endpoint-tree information that is irrelevant to the desired relation and keeps only legal common-digit continuations.

## Concrete pair states

Fix the phase-`u` frontier sets `O_k`. A pair state is

```text
(k, q, p),  q in O_k,  p in O_(k-1).
```

Write

```text
M_k(q) = {d in {0,1,2,3} : 4q+d is in O_(k+1)}.
```

The pair is **synchronized/full** when

```text
M_(k-1)(p) = 1111
```

or

```text
M_(k-1)(p) = M_k(q).
```

A digit `d` is a legal common lift when the concrete children

```text
(k+1, 4q+d, 4p+d)
```

exist and are again synchronized/full.

## Exact residual recursion

Define the radius-zero residual profile by

```text
R_0(k,q,p) = (M_k(q), M_(k-1)(p)).
```

For `r >= 0`, define

```text
R_(r+1)(k,q,p)
```

to contain `R_0(k,q,p)` and four digit entries. The entry for digit `d` is

```text
dead
```

when the common lift is not legal, and otherwise is

```text
R_r(k+1, 4q+d, 4p+d).
```

### Exact theorem

Equality of `R_r` profiles is exactly equality of the typed synchronized/full continuation trees through `r` common lifts.

This follows by induction on `r`.

- At radius zero, the profile is precisely the local current/shadow mask pair.
- At radius `r+1`, equality requires the same local pair, the same live/dead digit set, and equal radius-`r` profiles after every live digit.

Consequently, if a set of concrete pair states is closed under legal lifts and its `R_r` and `R_(r+1)` partitions agree, then the resulting radius-`r` classes form a deterministic finite continuation system on that closed set.

The closure condition is essential.

## Source pairs from gap-222 certificates

For each selected minimum-defect gap-`222` certificate

```text
current x in O_K
shadow  y in O_(K-1)
```

and each cylinder quotient step `j = 1,...,L`, retain the concrete source pair

```text
(K-j, floor(x/4^j), floor(y/4^j)).
```

These are the pair states at which the next common base-four digit is lifted in the exact weighted recursion.

The complexity-27 campaign contains:

```text
gap-222 occurrences:       2,989
minimum defect 0:          2,986
minimum defect 3:              3
dominant failures:              0
unique source pairs:        4,320
```

The radius-five campaign builds the phase-`u` frontier through complexity 28 and examines the 744 source pairs of complexity at most 22.

## Observed refinement

On those 744 source pairs, the unlevelled residual class counts are

```text
radius 0:   6
radius 1: 121
radius 2: 345
radius 3: 405
radius 4: 409
radius 5: 409
```

The level-specific counts are

```text
radius 0:  38
radius 1: 263
radius 2: 413
radius 3: 451
radius 4: 454
radius 5: 454
```

No radius-four class splits at radius five. The radius-four class/digit transitions are deterministic on all observed representatives.

This is the first finite campaign in this pathway where a realization-consistent continuation refinement reaches a fixed partition rather than immediately producing a deeper path-lifting counterexample.

## Closure test

Partition stabilization alone is insufficient. The 409 represented radius-four classes have 1,558 legal representative transitions, but only 493 transition instances land in a radius-four class already represented by the 744 source pairs. Only 59 of the 409 classes have every legal transition represented.

Thus the observed source-state family is not closed.

A one-step expansion from all source pairs of complexity at most 21 gives:

```text
base nodes:                  455
expanded nodes:            1,266
radius-four classes:         603
radius-five classes:         603
radius-four classes split:     0
nondeterministic digits:       0
```

A deeper expansion starts with source pairs through complexity 18 and follows every legal common lift through complexity 22:

```text
expanded nodes:            2,972
radius-four classes:       1,039
radius-five classes:       1,039
radius-four classes split:     0
interior nondeterministic digits: 0
```

The fixed partition survives these expansions.

## Why this is not yet a finite-state proof

The residual alphabet continues to acquire many new states. In the deeper expansion, the numbers of radius-four classes first appearing at successive complexities include

```text
complexity 18:  92
complexity 19: 154
complexity 20: 193
complexity 21: 206
complexity 22: 273
```

The stable radius-four partition is therefore locally deterministic but not finitely closed in the observed range. New behavioral classes still enter rapidly at the advancing frontier.

## Scientific boundary

Exact:

- the concrete synchronized/full lift relation;
- the residual-profile recursion;
- the induction identifying `R_r` with the typed continuation tree through radius `r`;
- the conditional statement that a closed stabilized partition gives a deterministic finite continuation system.

Finite through the stated bounds:

- all occurrence, defect, source-pair, class, closure, and growth counts;
- radius-four/radius-five agreement on 744 source pairs;
- agreement after the one-step and deeper closure expansions;
- deterministic interior transitions in the tested closure.

Not proved:

- stabilization at every complexity;
- a finite global residual alphabet;
- closure of the observed 409 or 1,039 classes;
- a universal three-defect bound;
- all-depth adjacent-shadow inclusion;
- exclusion of eventual period two;
- Rule 30 center nonperiodicity.

## Next target

The next useful question is no longer whether a fixed lookahead distinguishes the observed paths. Radius four already does so through this campaign. The question is whether the rapidly growing radius-four classes admit a smaller algebraic quotient that is closed under legal lifts while preserving the defect budget.

If no such quotient emerges, the finite-state endpoint strategy should be treated as exhausted rather than extended by larger raw lookahead radii.
