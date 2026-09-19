# Problem 1: a prescribed finite center trace places no constraint on the arbitrary right half

## Statement

For Rule 30, fix any integer horizon `T >= 0`. Fix an arbitrary initial right half-row

`x_0(0), x_1(0), x_2(0), ...`

and any desired center trace

`c_0, c_1, ..., c_T`

with the necessary compatibility `c_0 = x_0(0)`. Then there exist initial cells

`x_{-1}(0), ..., x_{-T}(0)`

such that the Rule-30 orbit satisfies

`x_0(t) = c_t` for every `0 <= t <= T`.

Moreover these left cells are determined uniquely, successively from `x_{-1}` through `x_{-T}`.

Consequently, for every finite prefix of the alternating FULL center trace, **every** choice of the initial right half beginning with the required center bit is compatible with that prefix after choosing the finite left extension appropriately.

## Proof

Write the Rule-30 local rule as

`F(l,c,r) = l XOR (c OR r)`.

Thus the rule is left-permutive: after `c,r` and the desired output `o` are fixed, the unique required left input is

`l = o XOR (c OR r)`.

Proceed inductively in time.

At time 1, the desired value `x_0(1)=c_1` depends on `x_{-1}(0),x_0(0),x_1(0)`. The latter two are already fixed, so left permutivity determines a unique `x_{-1}(0)`.

Suppose `x_{-1}(0),...,x_{-(t-1)}(0)` have been chosen so that the center trace is correct through time `t-1`. In the depth-`t` backward light cone of `(0,t)`, the new extreme-left source cell `x_{-t}(0)` reaches `(0,t)` along the all-right characteristic. Every other source cell in that cone has already been fixed: the entire nonnegative half-row was fixed initially and the nearer negative cells were fixed at earlier induction stages. Because each step along that extreme characteristic uses Rule 30 in its left argument, the composition is again a bijection in the bit `x_{-t}(0)`. Hence exactly one value of `x_{-t}(0)` makes `x_0(t)=c_t`.

Induction gives existence and uniqueness through horizon `T`.

## Consequence for the distinguished-source program

Runs 144--146 found a delayed but eventually full-cone dependence when solving the distinguished FULL source backward: the right pair `(r_3,r_4)` forced several opposite-side cells, but by offset `-12` the extreme right source bit `r_12` was genuinely relevant.

The theorem above explains why this widening is structural rather than an accident of the first twelve steps. A finite FULL center prefix cannot constrain the untouched right driver tail at all. Arbitrarily chosen farther-right bits remain admissible; the necessary compensation is absorbed uniquely by successively farther-left source bits.

Therefore no proof strategy can obtain a bounded-width compression of the unrestricted right driver **from the FULL center trace alone**. Any finite-state quotient that succeeds must use additional hypotheses specific to the cyclic-source/gate/sensitive-return structure (or finite support), not merely longer continuation of the alternating center trace.

This is stronger than the finite computation at run 146: it is an all-horizons stopping fence. It does not rule out a quotient for the return/birth observable, because that observable may use the extra cyclic/gate constraints and may deliberately forget most of the source state.
