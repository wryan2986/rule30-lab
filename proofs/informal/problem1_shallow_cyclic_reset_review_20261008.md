# Review: shallow cyclic reset proof for S4 and S5

Status: **PARTIAL-PROOF** relative to Problem 1. The local S4/S5 cycle
exclusion is proved rigorously: no directed cycle of either complete
shared-upper product graph contains a bad edge. This does not prove Problem 1
or the transient selector law, which has a finite counterexample.

## 1. Exact depth-two upper dynamics

Use interleaved pair packing

    u = (X_1+2Y_1) + 4(X_2+2Y_2),

with fixed normalized boundary pairs `(1,0),(0,1)`. For a pair
`(X,Y)`, the two raw bits are `(a,b)=(X,X XOR Y)`. The raw Rule 30 local
equation is `F(h,l,x)=h XOR (l OR x)`. Directly applying this equation to
both raw rows gives the following complete table for `T_0,T_1` at depth two.

| `u` | `T_0(u)` | `T_1(u)` | blind? |
|---:|---:|---:|:---:|
| 0 | 11 | 14 | no |
| 1 | 12 | 8 | no |
| 2 | 3 | 2 | no |
| 3 | 4 | 4 | yes |
| 4 | 15 | 10 | no |
| 5 | 12 | 8 | no |
| 6 | 15 | 10 | no |
| 7 | 12 | 8 | no |
| 8 | 3 | 2 | no |
| 9 | 12 | 8 | no |
| 10 | 3 | 2 | no |
| 11 | 12 | 8 | no |
| 12 | 7 | 6 | no |
| 13 | 12 | 8 | no |
| 14 | 15 | 10 | no |
| 15 | 4 | 4 | yes |

The cyclic strongly connected component containing blind states is
`B={2,3,4,10,15}`. The only other cyclic component is `{7,12}`, which has no
blind state. The table shows the blind depth-two states are exactly `3` and
`15`; both lie in `B`. Thus every depth-two projection of a cyclic blind
source is in `B`.

## 2. Cyclic blind sources at depth at least three

Truncating a normalized state and its transition to the first two pairs
commutes with `T_w`. Therefore the first two pairs of any periodic depth-`r`
upper orbit (`r>=3`) form a periodic depth-two orbit. At a blind phase, that
projection is blind, so its value is `3` or `15`.

State `15` cannot be the low-two-pair projection of a cyclic blind state at
depth at least three. Within `B`, its only predecessor is `4` (the edge is
`4 --0--> 15`). For a depth-three state above low-two value `4`, the first
two pairs are `(0,0),(1,0)`. At the third output coordinate the raw rows see
`F(0,1,x)` and `F(0,1,x XOR y)`, both equal to `1`; hence the output pair is
`(1,0)` regardless of the third input pair. A cyclic successor with low-two
value `15` therefore has third pair `(1,0)`. But low-two value `15` has first
two pairs `(1,1),(1,1)`, and its third output has zero `Y` exactly when its
third input pair satisfies `x=y`; `(1,0)` violates that condition. It cannot
be blind at depth three, hence cannot be a cyclic blind source at any larger
depth either.

The remaining case is low-two value `3`, whose first two pairs are
`(1,1),(0,0)`. At the third output coordinate the raw outputs agree exactly
when the third input pair is `(x,1)`, `x in {0,1}`. In ordinary integer
packing the low three pairs are therefore

    3 + 4*0 + 16*(2+x) = 35 or 51,

or, as pair words, `((1,1),(0,0),(x,1))`. These are necessary for every
cyclic blind source at every depth `r>=3`. A direct check of the 64-state
depth-three upper graph finds exactly these cyclic blind states, agreeing with
the derivation.

## 3. The next blind image resets the last parent

At such a blind source, the fixed boundaries and low-three-pair form give the
two raw input prefixes

    a: 1,0,1,0,x,...
    b: 1,1,0,0,1-x,...
       -1 0 1 2 3

The common outputs at positions 1, 2, and 3 are `0,1,1-x`. Blindness at
position 4 forces the common output there to be `1`: if `x=0`, the `b` output
is already `1`, forcing `a_4=1`; if `x=1`, the `a` output is already `1`,
forcing `b_4=1`. For depth five, blindness at position 5 likewise forces
`C_5=1`. When `x=0`, `a`'s position-5 output is `1`; when `x=1`, `b`'s is
`1`. Consequently the first five common output bits are exactly

    01111  (x=0),   or   01011  (x=1).

At depth four the first four are `0111` or `0101`. In either depth, the
postblind normalized upper state has final pair `(C_r,0)=(1,0)`, which means
the two raw parent bits are both `1`. Its low-two state is `4`, whose depth-two
outputs are `T_0(4)=15` and `T_1(4)=10`, so it is not blind. Consecutive blind
upper states are therefore impossible.

## 4. Product-cycle reset and exclusion of bad edges

Let the two added-copy states differ by `delta=(e,f)`. If their labels agree
at an edge and the last upper pair is `(L,M)`, direct subtraction of the two
raw local updates gives

    f' = M*e + (1+L+M)*f,
    e' = (1+L)*e + w*f',

with arithmetic in `GF(2)`. The postblind state has `(L,M)=(1,0)`, so this map
sends every incoming difference to `(e',f')=(0,0)`. The first edge after a
blind state is forced to use a common label because that postblind upper
state is nonblind; thus it applies this reset. Later nonblind common-label
edges preserve zero. A differing-label blind edge may create an `X` impulse,
but the next edge erases it before another blind state can occur.

Now take any directed shared-upper product cycle. If it contains a blind
state, follow the cycle from one blind state: its next upper state is
nonblind, the following common-label edge resets the copy difference, and the
difference remains zero until the next blind state. Hence every blind source
on the cycle is entered with equal child copies. Its equal-label outgoing
edge cannot have differing `Y` outputs. A blind edge with unequal labels is
not a bad edge by definition. If the cycle has no blind state, it has no bad
edge by definition. This excludes all bad edges on every product cycle at
`r=4` and `r=5`, proving S4 and S5. This is stronger than the resulting
affine-extension consequence restricted to complete odd fibers with nonzero
parents.

The argument is periodic, so an arbitrary seed difference cannot survive as
a cycle obstruction: any cycle containing a blind state includes the reset
edge, and every later blind gate is reached with zero difference. The known
finite transient selector counterexample is consistent with this result
because its initial upper state is not on an upper-state cycle.

## 5. Scope

This proves the fixed-depth cyclic exclusion for `r=4,5`; it does not extend
the result to arbitrary observer depth, prove a transient reset law, or settle
the global whole-tail Problem 1 obstruction.
