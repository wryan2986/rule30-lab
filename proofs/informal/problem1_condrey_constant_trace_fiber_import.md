# Problem 1: importing Condrey's constant-trace fiber method

Status: external-method import / new research target. Problem 1 remains OPEN.

External source:

- David L. Condrey, *Finite Configurations Cannot Generate a Constant Trace in Rule 30*, arXiv:2609.09431v1, 8 Sep 2026.
- https://arxiv.org/abs/2609.09431

This note records exactly what the paper contributes to this repository, what
is already covered by our existing stopping fences, and one source-specific
generalization that is worth testing.

## 1. Condrey's exact result

Write Rule 30 as

    F(x)_i = x_(i-1) XOR (x_i OR x_(i+1)).

For the center trace c_t=F^t(x)_0 and initial halves

    R_j=x_j,   L_j=x_(-j),

Condrey proves the following.

### Triangular uniqueness

If two configurations agree on every coordinate i>=0 and have the same
complete center trace, then they are equal. In finite-prefix form, agreement
on the nonnegative half together with trace agreement through time r forces
agreement at initial coordinates -1,...,-r.

This is the same left-permutive extreme-characteristic mechanism already used
in this repository, but Condrey packages it as the basic trace-fiber
uniqueness statement.

### Exact zero-trace fiber

If R_0=0 and the positive half is nonzero, let

    m=min{j>=1:R_j=1}.

The unique left half compatible with c_t=0 for every t>=0 is

    L_j=0 for j<m,
    L_m=1,
    L_j=j mod 2 for j>m.

Equivalently,

    L_(2k+1) = OR_(j=1..2k+1) R_j,

    L_(2k) = R_(2k) AND NOT OR_(j=1..2k-1) R_j.

If the positive half is zero, the unique zero-trace row is the zero row.

The important Rule-30-specific ingredient is the OR latch: once the first
right-side one reaches the relevant position, the forced left tail becomes
permanently nonzero at alternating depths.

### Exact all-one fiber

If R_0=1, the unique left half compatible with c_t=1 for every t is

    L_j=1 iff j is positive and even,

independently of the remainder of the right half.

Thus every nonzero constant-trace fiber has infinitely many ones to the left.

### Finite-support consequence

No column of a nonzero finite Rule-30 configuration is eventually constant.
Condrey obtains this directly from the two fibers, without invoking Kopra's
width-two theorem.

For support contained in [-w,w], the longest constant center prefix has
length at most w+2. The paper also gives the sharp separate zero/one horizons
and extremizer counts.

## 2. What this changes in our repository

problem1_period_one_exclusion.md already excludes eventual period one, but
it does so via Kopra's published width-two nonperiodicity theorem. Condrey
provides a direct Rule-30-specific replacement and a stronger exact fiber
classification.

The exact fiber formulas and the sharp w+2 horizon appear to be new relative
to our current pushed notes.

The triangular-uniqueness component itself is NOT new for us. It overlaps
with, among others:

- problem1_arbitrary_finite_center_trace_by_left_permutivity.md
- problem1_finite_support_realizes_arbitrary_finite_right_driver_and_center_trace.md
- problem1_full_center_prefix_places_no_constraint_on_arbitrary_right_half.md
- problem1_fixed_fringe_finite_horizon_uniqueness_no_go.md

In fact Condrey's conclusion section explicitly identifies the same barrier
we already isolated: arbitrary finite traces can be realized by finite
support through arbitrary finite horizons. The paper makes no claim for
period two or higher.

Therefore DO NOT treat the sharp constant-prefix horizon as a period-two
bound, and do not retry a generic finite-prefix uniqueness argument.

## 3. The useful generalization: a source-restricted alternating trace fiber

The promising import is the fiber-classification viewpoint, not the
period-one conclusion.

At the distinguished FULL source already established in this repository we
have the alternating center phase

    c_t = 1,0,1,0,...

and the rigid local source word

    (r_-5,...,r_2) = 10101110.

Thus the nonnegative initial half starts

    R_0,R_1,R_2 = 1,1,0,

with later right-fringe cells constrained by the complete cyclic-source/gate
structure. Existing inverse-center calculations then force

    L_1,...,L_5 = 1,0,1,0,1,

and for a=R_3, b=R_4,

    L_6 = NOT(a OR b),
    L_7 = a OR b,
    L_8 = a OR (NOT b),
    L_9 = 1.

This is exactly the beginning of a trace-fiber computation.

Define the two alternating trace fibers

    A_1 = {x : Tr(x)=101010...},
    A_0 = {x : Tr(x)=010101...}.

Rule 30 maps A_1 into A_0 and A_0 into A_1. By triangular uniqueness, for
every prescribed complete nonnegative half there is at most one compatible
left half in either fiber.

The exclusionary target is therefore:

> Source-restricted alternating-fiber target:
> For every complete finite right half admitted by the distinguished
> FULL/cyclic-source constraints, the unique alternating-trace left
> completion (if it exists) contains ones at arbitrarily large left depths.

This would be qualitatively stronger than our existing finite-horizon
phase-collapse result. It attacks the SUPPORT of the last unique survivor,
not the multiplicity of finite-horizon candidates, and therefore avoids the
stopping fence in
problem1_fixed_fringe_finite_horizon_uniqueness_no_go.md.

## 4. Why Condrey's OR latch is the right thing to test

For a constant zero trace, the right-neighbor recurrence becomes monotone and
the first right-side one latches permanently; this is what collapses the
entire left fiber to the prefix-OR formulas.

For the alternating trace, the same one-step monotonicity is lost. That is
why the paper does not extend automatically to period two.

However our distinguished source is not an arbitrary alternating-trace row:
its right pair, gates, cyclic returns, and transported source phases are
already heavily constrained. Runs 303--324 encode exactly this extra
structure.

The next useful calculation is therefore NOT a generic search for a
period-two horizon. It is:

1. express the alternating trace-fiber inversion in two-step phase blocks;
2. retain the complete actual right-fringe/gate variables rather than an
   arbitrary right driver;
3. look for a Rule-30-specific latch or finite-state invariant that, after
   each admissible return, forces a new nonzero initial left depth;
4. if such a latch exists, prove that it survives all admissible source
   phases and cannot be reset by the r/u sector.

This is also compatible with run 324's conclusion. A successful invariant
must retain additional transported/high information; a pure five-variable
temporal coboundary cannot remove the residual.

## 5. Concrete next work unit

Start from the complete post-four-step expression retained before the r/u
boundary elimination in runs 321--324, but reinterpret the r/u sector as the
right-driver state of the alternating trace fiber.

At one distinguished source phase, compute the two-step inverse map that
takes

    (finite right-fringe state, forced-left boundary state)

to the next forced-left boundary state.

Admission test for continuing this route:

- PASS if the exact map has a source-restricted absorbing/latching class that
  forces a nonzero bit at an unbounded sequence of new initial left depths;
- FAIL/STOP if the complete admissible state graph contains a reset cycle
  allowing arbitrarily many new depths to be zero while preserving all
  FULL/cyclic-source constraints.

Do not infer success from long finite prefixes. The theorem needed is
all-depth and must exclude the unique infinite continuation, not merely make
it unique.

## 6. Immediate safe import

Independently of whether the new route succeeds, Condrey's result can replace
the external-width-two dependency for the period-one subcase in future
exposition:

> Every nonzero finite Rule-30 configuration has no eventually constant
> column.

For a final proof package we should cite Condrey's Theorems 2 and 3 and
Corollaries 4 and 5, while retaining the existing Kopra-based proof as an
independent cross-check until the new preprint has received broader review.
