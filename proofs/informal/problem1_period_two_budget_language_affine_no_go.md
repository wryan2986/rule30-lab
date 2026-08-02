# Defect-budget continuation languages and an affine modular no-go

## Purpose

The preceding residual profiles retained the exact local mask pair at every node. That is stronger than the period-two shadow argument needs. The target only asks whether a concrete synchronized/full shadow can follow the required common base-four digits while spending at most three non-full shadow fibers.

This note makes the remaining defect budget part of the state and quotients concrete endpoint pairs by their exact **budget-feasible continuation language**. It then tests the most natural algebraic compression of that language, based on the affine separation between the current and shadow endpoints.

## Concrete budget state

Let

\[
    n=(k,q,p),\qquad q\in O_{u,k},\quad p\in O_{u,k-1},
\]

be a synchronized/full concrete pair. Define its local cost by

\[
    c(n)=\mathbf 1\{M_{u,k-1}(p)\ne1111\}.
\]

Because the pair is synchronized/full, a non-full shadow mask equals the current mask, so this is exactly the local defect contribution.

A budget state is `(n,b)` with `b` in `{0,1,2,3}`. It is alive when `c(n) <= b`.

For a common digit `d`, let

\[
    n_d=(k+1,4q+d,4p+d).
\]

There is an exact transition

\[
    (n,b)\xrightarrow d(n_d,b-c(n))
\]

precisely when the two lifted endpoints exist, remain synchronized/full, and the target state remains alive. No existential union is taken; every transition retains one concrete shadow endpoint.

## Exact budget-language profile

Let `L_0(n,b)` be live when `(n,b)` is alive and dead otherwise. Recursively, `L_(r+1)` records, for each digit, either dead or `L_r` of the exact budget transition.

Induction on `r` gives:

> Equality of radius-`r` budget-language profiles is exactly equality of the common base-four words of length at most `r` that the two concrete pairs can realize without exceeding the remaining defect budget.

This is weaker than the full typed residual profile and is aligned directly with the desired cost-at-most-three certificate.

## Exact affine separation

Define

\[
    H(k,q,p)=q-4p.
\]

Under a common digit lift,

\[
\begin{aligned}
H(k+1,4q+d,4p+d)
  &=(4q+d)-4(4p+d)\\
  &=4H(k,q,p)-3d.
\end{aligned}
\]

Thus `H mod 2^m` has an exact finite update. The tested algebraic quotient is

```text
(remaining budget, current mask, shadow mask, H mod 2^m)
```

so its failures cannot be attributed merely to forgetting the current defect type.

## Controlled Python campaigns

Through complexity 16, with the frontier built through complexity 22:

```text
outputs built:             1,444,495
gap-222 occurrences:              10
dominant failures:                 0
source pairs:                      16
budget-closure states:             27

radius:    0  1   2   3   4   5
classes:   1  7  12  12  12  12
```

Through complexity 18:

```text
outputs built:             4,443,626
gap-222 occurrences:              26
dominant failures:                 0
source pairs:                      42
budget-closure states:            173

radius:    0   1   2   3   4   5
classes:   1  13  40  41  41  41
```

The stabilization is exact for those finite concrete state sets, but does not imply closure at higher complexity.

## Independent complexity-28 campaign

The C++ campaign builds the phase-`u` frontier through complexity 28 and retains the complete gap-`222` occurrence campaign through complexity 27:

```text
phase-u outputs:          40,122,287
gap-222 occurrences:           2,989
minimum defect 0:              2,986
minimum defect 3:                  3
source endpoint pairs:            744
```

Starting every source pair with budget three and closing legal transitions from the interior source set through pair complexity 22 produces 3,077 concrete budget states.

```text
radius:          0    1    2    3    4    5    6
classes:         1   16  531  866  893  899  899
split next:     15  143   25    6    0    0
nondeterminism: 30  179   26    6    0    0
```

Radius five is exact and deterministic on this finite closed campaign. However, the alphabet continues to grow:

```text
complexity 21 states:          905
complexity 21 classes:         208
new classes at complexity 21:  172

complexity 22 states:        1,039
complexity 22 classes:         308
new classes at complexity 22:  268
```

Budget capping reduces the deep typed-mask residual alphabet from 1,039 classes to 899 budget-language classes, but does not produce a small or visibly closing state set.

## Modular affine quotient

On the same 3,077 budget states:

```text
bits   classes   nondeterministic class/digit pairs
  14     2,979                  119
  16     3,035                   16
  18     3,068                   11
  20     3,074                    0
  22     3,077                    0
```

At 20 bits the quotient becomes deterministic only by assigning 3,074 classes to 3,077 concrete states. It is essentially an injective encoding, not a useful compression.

### Explicit 18-bit obstruction

These budget-three states have the same local mask pair and the same affine separation modulo `2^18`:

```text
A:
  complexity: 21
  current:    0x190b963bf70
  shadow:     0x642e246a30
  H:          13,768,368

B:
  complexity: 21
  current:    0x1bd9c5bbf70
  shadow:     0x642e246a30
  H:          192,800,233,136
```

Their current endpoints differ by `0x2ce2f80000`, which is divisible by `2^19`. Nevertheless, common digit `0` is an in-budget transition for `A` and is not legal for `B`.

Therefore the 18-bit affine quotient is not realization-consistent even after retaining budget and both local masks.

## Consequence

The increasingly goal-directed finite-state constructions now show the same boundary:

1. Exact continuation behavior stabilizes at modest radius on each finite campaign.
2. The number of concrete behavior classes continues to grow strongly with complexity.
3. A natural closed algebraic state becomes deterministic only when it nearly identifies every concrete state separately.

This is evidence against continuing to enlarge local endpoint signatures or fixed modular suffixes. The next useful route should operate on the exact weighted belief as a set, seeking monotonicity, interval structure, or a counting theorem that proves nonemptiness, rather than classifying individual endpoints with a small finite automaton.

## Scientific boundary

The budget transition, budget-language interpretation, affine recurrence, and explicit witness are exact.

The stabilization, state-growth, and modular counts are finite through the stated bounds. They do not prove that every finite or algebraic quotient fails, do not prove a universal three-defect bound, and do not establish the all-depth adjacent-shadow inclusion or Rule 30 center nonperiodicity.
