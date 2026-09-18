# Problem 1: actual ancestry alone cannot bound forced births

## Status

Problem 1 remains open. This note closes a weaker version of the revised characteristic-budget target from automation run 121.

## Claim

For Rule 30, proving only that every forced cyclic birth has an ancestor among the finitely many nonzero cells of the original actual row cannot imply a finite birth count. Even a single original actual 1 can have certified descendants at arbitrarily late times.

Thus an actual-row ancestry bridge is useful only if it also proves a bounded-multiplicity / consumption statement for the particular birth certificates.

## Proof

Write Rule 30 as

\[
f(l,c,r)=l\oplus(c\lor r).
\]

For fixed `c,r`, the map `l -> f(l,c,r)` is a bijection of `{0,1}`: changing the left input always changes the output. Rule 30 is therefore left-permutive.

Fix an initial site `i`. For every `t>=1`, consider the rightmost characteristic from `(i,0)` to `(i+t,t)`. At the last update, `x_{i+t}(t)` uses `x_{i+t-1}(t-1)` as its left input. Inductively, along this edge characteristic, changing only `x_i(0)` while holding all other initial cells fixed changes `x_{i+t}(t)` for every `t`.

Equivalently, `(i,0)` is a genuine Boolean dependency ancestor of `(i+t,t)` for all `t>=0`. Hence one original actual cell has infinitely many distinct spacetime descendants.

For a nonzero finite row with rightmost occupied site `R`, there is an even sharper physical instance. Outside the support the center and right inputs at the moving right edge are zero, so

\[
x_{R+t+1}(t+1)=f(x_{R+t}(t),0,0)=x_{R+t}(t).
\]

Since `x_R(0)=1`, it follows that

\[
x_{R+t}(t)=1
\]

for every `t>=0`. The same single original rightmost 1 therefore propagates to an actual 1 at every later time on the right edge.

## Consequence for the birth-budget route

Run 121 correctly required a bridge from the forced `001` shadow event to a genuinely finite original ACTUAL resource. This note sharpens that requirement: merely assigning each forced birth an original actual 1 ancestor is insufficient, because finite support does not make causal ancestry consumptive.

A successful charge must prove something stronger for the *specific forced-birth mechanism*, for example:

- each original actual 1 can receive only uniformly boundedly many birth charges;
- charges consume a monotone finite label/order attached to original support;
- or all birth certificates inject into a finite set that cannot be reused.

The left-permutive edge characteristic is a permanent counterexample to any argument that tries to infer bounded reuse from finite actual support plus ancestry alone.

## Stopping fence

Do not spend another run proving only `forced birth -> some original actual 1 ancestor`. That statement, even if true, does not close the global birth budget. The missing content is bounded reuse / irreversible consumption.
