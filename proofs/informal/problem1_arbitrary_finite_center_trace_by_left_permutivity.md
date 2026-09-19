# Arbitrary finite center traces are realizable by finite support

## Purpose

Run135 isolated the missing finite-resource statement: distinguished source-relative `011` events must be charged to a finite object with bounded reuse. This note records a stopping fence on how such a theorem can be proved. **No bounded-reuse theorem can follow from the FULL center trace alone.** Rule 30 left-permutivity lets an arbitrary finite center word be realized by finite-support initial data.

## Lemma

Fix `T >= 0` and any binary word

    c_0,c_1,...,c_T.

There is a finite-support Rule-30 initial row whose cell at spatial coordinate 0 has exactly this trace through time `T`.

More strongly, after fixing all initial cells at coordinates `x >= 0` with the required value at `x=0`, the cells `-1,-2,...,-T` can be chosen successively so as to prescribe `c_1,...,c_T`.

## Proof

Rule 30 is left-permutive:

    f(l,c,r) = l XOR (c OR r).

For fixed `(c,r)`, either desired output value determines a unique `l`.

At time `t`, the value at spacetime point `(0,t)` depends only on initial coordinates `[-t,t]`. Its dependence on the extreme-left input `x=-t` is bijective. This follows by following the unique leftmost characteristic from `(-t,0)` to `(0,t)`: at each of the `t` local updates the traversed input is the left argument, and Rule 30 is permutive in that argument. All other inputs in the cone are independent of the new extreme-left bit.

Proceed inductively. Suppose initial cells `-1,...,-(t-1)` have already been chosen so that the center trace through time `t-1` is the desired prefix. The new initial bit `-t` lies outside every earlier center cone, so changing it cannot alter times `< t`. By the bijective dependence just noted, exactly one choice of `-t` makes the center value at time `t` equal to `c_t`.

After `T` steps only the finite interval `[-T,T]` matters. Set all not-yet-fixed cells in that interval (for example the positive side) arbitrarily, and all cells outside it to zero. The resulting initial row has finite support and realizes the prescribed finite center word. QED.

## Consequence for FULL

Taking

    c_t = 1 for even t, 0 for odd t

shows that arbitrarily long finite prefixes of the alternating FULL center trace are compatible with finite-support initial data. Therefore no contradiction, finite birth budget, or bounded ancestry-reuse statement can be obtained merely from the alternating center word, regardless of how long a finite prefix is inspected.

This does **not** construct an infinite FULL survivor and does not address the complete cyclic-source/right-fringe constraints. It instead localizes what any successful bounded-reuse theorem must use: information beyond the center trace, such as the complete source state, actual gate/right-fringe compatibility, or a genuinely global finite-support invariant.

## Small exact sanity check

A direct exact Rule-30 enumeration was used as a sanity check for alternating prefixes through length 8 while fixing the nonnegative initial side to zero except for the center. Finite left supports were found in every case. Examples include supports `{-2,-1,0}` through time 5 and `{-7,-6,-2,-1,0}` through time 8. These examples are not part of the proof; the left-permutivity induction proves the statement for every finite length and every binary center word.

## Research implication

Run135's proposed target should be narrowed: do not attempt to prove bounded reuse from FULL's center alternation plus generic ancestry properties. Any such argument must explicitly consume the cyclic-source/fringe hypotheses. A useful next test is whether the complete cyclic-source constraints destroy the left-permutive freedom used above by fixing the successive extreme-left bits, or whether those bits remain free enough to realize arbitrarily many distinguished events.
