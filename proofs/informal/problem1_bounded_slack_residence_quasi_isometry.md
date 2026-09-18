# Problem 1: bounded-slack residence quasi-isometry

## Status

Exact strengthening of the bounded-slack branch of the run-101 dichotomy. It does not solve Problem 1, but converts the scalar strip assumption into uniform local constraints on the residence schedule, not merely an interval discrepancy bound.

## Setup

Use the notation of `problem1_bounded_counterexample_slack_discrepancy_dichotomy.md`:

    h_n = tau(2^n v),
    q_n = h_n - n - R,
    delta_n = h_(n+1)-h_n >= 0.

Assume the bounded-slack branch of a hypothetical bounded physical strip. After deleting a finite prefix there are constants `G,K >= 0` such that

    -G <= q_n <= K.                              (1)

Then

    n+R-G <= h_n <= n+R+K.                       (2)

Thus the nondecreasing integer map `n -> h_n` is at uniformly bounded distance from the translation `n -> n+R`.

## Exact local consequences

### 1. No arbitrarily long run of zero residence increments

Suppose

    delta_n = delta_(n+1) = ... = delta_(n+s-1) = 0.

Then `q_(n+s)=q_n-s`. By (1),

    s = q_n-q_(n+s) <= K+G.

Hence every late run of consecutive skips has length at most

    K+G.                                          (3)

So nonzero residence increments occur syndetically in characteristic index.

### 2. No arbitrarily large residence jump

From run 101,

    delta_n = 1+q_(n+1)-q_n <= K+G+1.            (4)

Therefore the image set `{h_n}` has no late gap larger than `K+G+1`: whenever `h_n < t < h_(n+1)`,

    min(t-h_n, h_(n+1)-t) <= K+G,

and in particular every sufficiently large physical time lies within `K+G` of some residence time `h_n`.

### 3. Uniform inverse localization

If `h_n <= t < h_(n+1)`, (2) gives

    t-R-K-1 <= n <= t-R+G.                        (5)

Thus any generalized inverse characteristic index differs from `t-R` by a bounded amount depending only on the strip/slack widths. The residence schedule is a coarse bijection (quasi-isometry) between late characteristic index and physical time.

### 4. Return blocks have exactly zero signed charge

Because `q_n` takes values in the finite integer set `{-G,...,K}`, at least one value `c` occurs infinitely often. For successive late return indices `a<b` with `q_a=q_b=c`,

    sum_(n=a..b-1)(delta_n-1) = q_b-q_a = 0,

or equivalently

    P[a,b) = Z[a,b).                              (6)

Hence the tail admits infinitely many exact zero-charge return blocks. This is stronger than the absolute discrepancy bound on arbitrary intervals and is a useful normalization for any future FULL/fringe episode argument.

## Interpretation

In bounded-slack case B, a hypothetical survivor cannot hide problematic dynamics in increasingly long deserts of skipped characteristics or in increasingly large residence jumps. Both are uniformly bounded. Moreover, one may cut the tail into return blocks based at a recurrent normalized-excess level, and every such block has exactly balanced skip/long-residence charge.

This sharply constrains what a future contradiction must prove. It is enough in case B to show that the complete FULL fringe forces, on sufficiently many recurrent return blocks, either:

1. an internal skip desert longer than `K+G`,
2. a residence jump larger than `K+G+1`, or
3. a nonzero one-sided block charge incompatible with (6).

The third formulation may be the cleanest target because it avoids compensation across block boundaries: the boundaries have equal `q`, so compensation cannot be exported to another block.

## Limitation

These conclusions are still consequences of bounded integer discrepancy alone. Abstract schedules such as `h_n=n+C` satisfy all of them. Therefore they are not a contradiction without a Rule-30/FULL-specific theorem linking complete-fringe events to one of the three forbidden block behaviors above.