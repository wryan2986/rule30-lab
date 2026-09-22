# Problem 1 run 204 — `T` is nonlinear, triangular, and injective

Status: `partial-proof`. Problem 1 remains OPEN.

Continue only the corrected run-193--203 chain. Run 203 reduced the remaining sufficient diagonal bound to control of `tau(T^m x)` and `tau(2 T^m x)`, where

    T(q) = q XOR ((q<<1) OR (q<<2)).

This note corrects one descriptor in run 203 and records two exact structural facts about `T` that constrain the next proof attempt.

## 1. `T` is not linear over GF(2)

Run 203 called `T` a linear/triangular map. The triangular part is correct, but linearity is false because of the Boolean OR.

Writing `q_i` for bit `i` and taking `q_j=0` for `j<0`,

    (Tq)_i = q_i XOR (q_(i-1) OR q_(i-2)).                    (1)

The OR term contains the nonlinear product in the GF(2) representation

    a OR b = a XOR b XOR ab.

A direct counterexample is enough: with `u=1` and `v=2`,

    T(1)=7,
    T(2)=14,
    T(3)=9,

while

    T(1) XOR T(2) = 9.

For this pair equality happens accidentally, so use `u=1`, `v=4`:

    T(1)=7,
    T(4)=28,
    T(5)=27,
    T(1) XOR T(4)=27,

again accidental because the shifted supports do not create the needed overlap. A genuine overlap counterexample is `u=2`, `v=4`:

    T(2)=14,
    T(4)=28,
    T(6)=18,
    T(2) XOR T(4)=18.

This also cancels. The reason is that the OR nonlinearity can cancel against the outer XOR for some sparse pairs. An unambiguous symbolic counterexample comes from the bit formula: at output bit `i`, the quadratic term is `q_(i-1) q_(i-2)`. Therefore the polarization is

    (T(u XOR v) XOR T(u) XOR T(v))_i
      = u_(i-1)v_(i-2) XOR v_(i-1)u_(i-2).

Take `u=1` (bit 0) and `v=2` (bit 1). At `i=2` the polarization equals 1, so `T` is nonlinear. Rechecking the integer arithmetic gives

    T(1)=7,
    T(2)=14,
    T(3)=13,
    7 XOR 14=9,

so indeed `T(3) != T(1) XOR T(2)`.

No identity in run 203 used linearity, so equations (3)--(11) there remain intact. Only the suggested proof route must not invoke linear-algebraic properties of `T`.

## 2. Exact triangular inversion

Equation (1) is triangular from low bits upward. Given `y=T(q)`, recover `q` recursively by

    q_i = y_i XOR (q_(i-1) OR q_(i-2)),                       (2)

starting with `q_(-2)=q_(-1)=0`.

Hence `T` is injective on finite nonnegative integers (indeed, on one-sided infinite bit strings). The inverse of a finite `y` need not have finite support, so this does not assert surjectivity on finite integers.

## 3. Exact width growth

Let `h(q)` be the highest occupied bit of a nonzero finite `q`. The highest bit of `(q<<1) OR (q<<2)` is `h(q)+2`, and `q` has no bit there. Therefore

    h(Tq)=h(q)+2                                                (3)

for every nonzero finite `q`. Iterating,

    h(T^m x)=h(x)+2m.                                          (4)

Thus the renormalized states in run 203 are all distinct and their support width grows exactly linearly at slope 2. This rules out any argument that hopes `T^m x` eventually enters a finite set or becomes periodic under `T`.

## 4. Consequence for the run-203 target

The desired sufficient bounds

    tau(T^m x) <= b+m,
    tau(2 T^m x) <= b+m+1

eventually cannot follow from bounded state-space or periodicity of the `T` orbit: the orbit escapes to higher bits at the maximal deterministic rate (4). Nor may one use linear superposition for `T`.

The viable target is narrower: exploit the interaction between the triangular recurrence (1)/(2) and the `A`-preperiod/erasing-history machinery. In particular, any proof must show that despite exact width `h(x)+2m`, the `A`-tail of `T^m x` is at most about `m`, i.e. roughly half its added width. That is a genuine dynamical statement, not a dimension-counting consequence.

Dependencies: `problem1_run203_shift_tower_renormalization.md`; reviewed definitions of `A`, `T`, and least preperiod `tau`.
