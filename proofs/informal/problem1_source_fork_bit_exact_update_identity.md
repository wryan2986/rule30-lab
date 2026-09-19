# Exact update identity for the source-relative 001/011 fork bit

Status: `partial-proof` / structural refinement. Problem 1 remains OPEN.

## Setup

Continue `problem1_forced_birth_sensitive_route_previous_source_dichotomy.md`. Let `q=t+2` be the cyclic `t` source arising from a two-bit nonreset source. FULL gives

    r_0(q)=1, r_0(q+1)=0, r_0(q+2)=1,

and the previous argument proved

    r_-2(q)=0,

while the sensitive provenance fork is controlled by

    a := r_-1(q).

Thus the three actual cells at positions `-2,-1,0` at the source are exactly

    0 a 1.

## Exact one-step image of the fork bit

The cell immediately to the left of the center one step later is

    r_-1(q+1)
      = f(r_-2(q), r_-1(q), r_0(q))
      = f(0,a,1)
      = 1

for both `a=0` and `a=1`, as already used in the dichotomy proof.

But the cell one step farther left has a useful exact expression. Put

    p := r_-3(q).

Then

    r_-2(q+1)
      = f(r_-3(q), r_-2(q), r_-1(q))
      = f(p,0,a)
      = p XOR a.

Therefore the local source block

    p 0 a 1

maps on its two relevant left outputs to

    (p XOR a) 1.

Equivalently,

    a = p XOR r_-2(q+1).

So the 001/011 fork bit is not an independent event label: it is exactly the parity discrepancy between the next farther-left source bit and its one-step descendant.

## Consequence for the provenance/budget strategy

This gives a sharper interpretation of the obstruction found in run130.

- `a=0` (the `001` branch) means `r_-2(q+1)=r_-3(q)`: the farther-left bit is transported unchanged across this local step.
- `a=1` (the `011` branch) means `r_-2(q+1)=1-r_-3(q)`: the farther-left bit flips across the step.

Thus repeated `011` obstructions can be viewed as local flip events along a left-moving staircase, rather than as generic creation events with no algebraic structure.

However, this identity alone does **not** provide a finite birth budget. The staircase coordinates move left as time increases, so a parity/flip count can in principle draw on arbitrarily many cells outside the original finite support. A successful telescoping argument would need an additional boundary condition or cross-episode alignment proving that the relevant staircase eventually lies in a fixed zero region at both ends, or otherwise tying its net flip count to finitely many original actual cells.

This is a more concrete next target than arbitrary monotonicity of `r_-1(q)`: determine whether the successive cyclic-source fork bits can be assembled into a telescoping XOR along a single spacetime staircase. If yes, finite support could turn the number/parity of `011` branches into a boundary quantity; if the source-to-source geometry does not align, record that as the next no-go result.

Dependencies: `problem1_forced_birth_sensitive_route_previous_source_dichotomy.md`, Rule 30 local rule `f(l,c,r)=l XOR (c OR r)`.
