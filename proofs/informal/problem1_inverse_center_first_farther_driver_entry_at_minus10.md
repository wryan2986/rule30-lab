# Problem 1: first farther right-driver entry in the distinguished inverse-center cone

Problem 1 remains OPEN.

## Setup

At the distinguished cyclic source `q`, previous runs establish

`(r_-5,...,r_2)(q) = 10101110`

and define

- `a = r_3(q)`
- `b = r_4(q)`.

Run 144 showed that imposing continuation of the FULL alternating center trace forces

- `r_-6 = NOT(a OR b)`
- `r_-7 = a OR b`
- `r_-8 = a OR (NOT b)`
- `r_-9 = 1`.

The question was whether `(a,b)` continues to determine the inverse-center extension arbitrarily far left.

## New result

It does not.  The first failure is exactly at offset `-10`.

Write additionally

- `c = r_5(q)`
- `d = r_6(q)`.

Exact Rule-30 light-cone evaluation, imposing the alternating FULL center trace at every intermediate time, gives

`r_-10(q) = (NOT a) AND (b OR c OR (NOT d))`.

Equivalently, for `a=1` the required bit is always zero.  For `a=0` it is one except in the single local driver case

`(a,b,c,d) = (0,0,0,1)`,

where it is zero.

Thus `(a,b)` determines every newly forced source bit through `r_-9`, but not `r_-10`.  The first extra information entering from the right is not just one next bit: the Boolean dependency at `-10` uses both `r_5` and `r_6` (although only through `c OR NOT d` once `a=b=0`).

## Exhaustive check

I enumerated all assignments of the source bits `r_3,...,r_12`, solved successively for the unique left bits required to maintain the alternating center trace through time 12, and grouped the resulting `r_-10` values by right-driver prefixes.

- Grouping by `(r_3,r_4)` does not determine `r_-10`.
- Grouping by `(r_3,r_4,r_5)` still does not determine `r_-10`.
- Grouping by `(r_3,r_4,r_5,r_6)` does determine it.

The 16-value truth table simplifies to the formula above.  The computation uses the complete finite dependency cone for each tested center time; exterior cells outside that cone are irrelevant, so no zero-tail assumption is being introduced.

## Consequence

This rules out the strongest version of the run-144 finite-state hope: the distinguished FULL source is not compressed indefinitely by the two-bit driver `(a,b)`.  There is, however, substantial delayed dependence: right-driver information at positions 5 and 6 does not re-enter the forced opposite-side extension until position -10.

A useful next question is whether this delay has a systematic characteristic interpretation.  Track, for successive inverse-center offsets, the largest right-driver index on which the forced left bit genuinely depends.  If that dependency frontier advances sublinearly or through a small recurrent transducer under the cyclic-source constraints, it may still provide a finite-resource obstruction.  If it advances at the generic light-cone rate, record that as a stopping fence and return to the episode/gate quotient route.
