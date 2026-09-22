# Problem 1 run 205 — the run-203 sufficient diagonal bound is false

Status: `counterexample` to the sufficient bound proposed in runs 203--204. Problem 1 remains OPEN.

Continue only the corrected run-193--204 chain. Runs 203--204 proposed, as a sufficient route (not as an established theorem), eventual bounds

    tau(T^m x) <= b+m,
    tau(2 T^m x) <= b+m+1,

for fixed finite `x=L_b`. This note records an exact finite counterexample and closes that route.

## Exact counterexample

Use the smallest possible finite core

    x=1,  b=0,

and

    T(q)=q XOR ((q<<1) OR (q<<2)).

Nine exact iterations give

    T^9(1)=456263 = 0b1101111011001000111.

Using the reviewed scan map

    A(q) = (q>>2) XOR ((q>>1) OR q),

the successive states beginning at `456263` are

    456263,
    410358,
    455490,
    411443,
    456311,
    410338,
    455499,
    411453,
    456304,
    410340,
    455503,
    411452,
    456305,
    410341,
    455502,
    411452, ...

The first repeated state is `411452`: it occurs first at time 11 and again at time 15. All states at times 0 through 14 displayed above are distinct. Hence the least preperiod and period are exactly

    tau(T^9(1)) = 11,
    per(T^9(1)) = 4.

But the proposed even-parity sufficient bound at `b=0,m=9` is

    tau(T^9(1)) <= 9,

which fails by two steps.

The odd companion also fails at the same depth: exact iteration gives

    tau(2 T^9(1)) = 11 > 10 = b+m+1.

Therefore neither inequality in the proposed run-203 sufficient theorem is valid universally.

## Stronger bounded diagnostic

A direct exact scan for `x=1` through `m=49` shows that this is not an isolated one-step anomaly: `tau(T^m(1))-m` repeatedly exceeds zero and reaches 39 in that finite range. This is computational evidence only and is not used as an all-depth claim.

Likewise, directly computing `a_n=tau(2^n)` for `1<=n<100` produces many indices satisfying the run-202 late-renewal inequality

    a_n > max(a_(n-1), n).

This is again bounded evidence, not a claim of infinitely many renewals. It shows that the finite-fringe shift-tower reduction does not by itself create an easy diagonal upper bound even for the canonical one-bit seed.

## Consequence

Runs 203--204 remain correct as reductions/structural identities except for the already-corrected description of `T` as linear in run 203. What is now refuted is specifically the suggested sufficient route

    tau(T^m x) <= b+m eventually

if interpreted as a universal theorem that should follow from triangularity/width. The explicit `m=9` counterexample disproves a pointwise version immediately; the bounded continuation strongly warns against trying to repair it by a small additive constant.

The strict-increase part of the true renewal condition remains essential:

    a_n > max(a_(n-1), b+n).

A future proof must exploit more than an absolute diagonal upper bound. In particular, it should study the increments/plateaux of `a_n`, or relate renewal events to complete-code/return structure. Do not spend another run trying to prove the run-203 sufficient inequalities from width or triangularity.

Reproduction pseudocode:

    A(q) = (q>>2) XOR ((q>>1) OR q)
    T(q) = q XOR ((q<<1) OR (q<<2))
    q = 1
    repeat 9 times: q = T(q)
    iterate A from q until first repeated state

Dependencies: `problem1_run202_finite_fringe_shift_tower_reduction.md`, `problem1_run203_shift_tower_renormalization.md`, `problem1_run204_T_is_nonlinear_triangular_injective.md`, and the reviewed definitions of `A`, `T`, and least preperiod.
