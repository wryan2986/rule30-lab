# Finite right support reduces the late strip question to zero-extension excess

Status: `partial-proof` for the exact reduction below. This is a repackaging of
already established all-depth cut/front identities into a sharper scalar target;
it does **not** prove the required excess is unbounded and does not close Problem 1.
No numerical experiment, source census, gate-prefix extension, or periodic-core
search is used.

## 0. Purpose

The current Problem 1 bottleneck is global: FULL must be incompatible with a
finite original row while retaining its complete finite right fringe. The existing
global-front theorem describes the late orbit by the original cut delays

    s_j = tau(L_j(r(0))).

The existing zero-extension theorem proves `tau(2^n v) -> infinity` for every
positive finite `v`, but explicitly notes that this does not control
`tau(2^n v)-n`. The point of this note is to show that the latter difference is
not merely one possible strengthening: after the right support ends, it is
**exactly** the scalar quantity equivalent to an eventual physical delay strip.

This identifies a single all-depth target and rules out spending further work on
mere divergence of `tau(2^n v)`.

## 1. Exact tail identity

Fix one nonzero finitely supported initial Rule 30 row `r`. Use the original-cut
notation

    L_j(r) = sum_(i<=j) r_i 2^(j-i),
    s_j = tau(L_j(r)).

Let `R` be any right support bound with `r_i=0` for all `i>R`, and assume
`v=L_R(r)>0`. Then for every `n>=0`,

    L_(R+n)(r) = 2^n v.                                  (1)

This is an integer identity: after the last actual right-hand 1, increasing the
cut index only appends zero low bits.

The established global-front identity gives, for every physical time `t`,

    tau(Y_t) = max(s_t-t,0).                             (2)

Putting `t=R+n` and using (1) yields the exact tail formula

    tau(Y_(R+n))
      = max(tau(2^n v) - (R+n), 0).                     (3)

No FULL premise is used in (1)-(3). No reinitialization of the right fringe is
made: `v` is the single original cut at the end of the actual finite support.

## 2. Eventual strip iff the zero-extension excess is bounded above

Define the scalar excess

    e_v(n) = tau(2^n v) - n.                            (4)

Equation (3) becomes

    tau(Y_(R+n)) = max(e_v(n)-R,0).                     (5)

Consequently the following are equivalent for this one finite row:

1. `tau(Y_t)` is eventually bounded in physical time;
2. `tau(Y_(R+n))` is bounded for `n>=0` (discarding finitely many initial
   values is immaterial);
3. `e_v(n)=tau(2^n v)-n` is bounded above.

More quantitatively, an eventual physical bound `tau(Y_t)<=K` implies

    tau(2^n v) - n <= R+K                               (6)

for all sufficiently large `n`. Conversely, if `e_v(n)<=C` eventually, then

    tau(Y_(R+n)) <= max(C-R,0)                          (7)

for all sufficiently large `n`.

Thus a theorem of the form

    for every positive finite v,
    limsup_(n->infinity) [tau(2^n v)-n] = infinity      (8)

would exclude **every** eventual finite physical delay strip for every finite
initial row, independent of the width of that strip. The currently proved
statement

    tau(2^n v) -> infinity                              (9)

is insufficient because a sequence such as `n+O(1)` satisfies (9) while its
excess (4) remains bounded.

## 3. Increment form and why monotone divergence is not enough

Let

    delta_v(n) = tau(2^(n+1)v) - tau(2^n v) >= 0,       (10)

where nonnegativity is the already established monotonicity of zero-extension
preperiods. Then

    e_v(n+1)-e_v(n) = delta_v(n)-1,                    (11)

and hence

    e_v(N) = tau(v) + sum_(n=0..N-1)(delta_v(n)-1).    (12)

Therefore (8) is exactly an assertion that the cumulative excess of residence
increments over unit drift has arbitrarily large positive excursions. Merely
proving infinitely many positive `delta_v(n)`, or `tau(2^n v)->infinity`, does
not imply this. Long stretches of `delta=1`, or compensating zero increments,
can keep (12) bounded above.

This formulation also fits the global-front geometry: `delta_v(n)` is the
length increment between successive original-cut delay thresholds after the
right support has ended. Any future argument using clock doublings, skipped
front characteristics, or forced erasers must control their **net contribution
to (12)**, not only show that such events occur infinitely often.

## 4. Relation to the current K=3 frontier

On the presently studied conditional eventual-`K=3` alternative, (6) specializes
to

    tau(2^n v)-n <= R+3                                (13)

for every sufficiently late `n`.

So a contradiction on that branch can be obtained by proving that the same FULL
orbit forces arbitrarily large positive values of the scalar excess (4). This is
strictly stronger than the current nonreset-return spacing theorem: spacing gives
a lower bound between certain temporal events, whereas (12) requires a signed
cumulative lower bound on zero-extension delay increments.

The existing global shadow has infinitely many right discrepancies, so (8) cannot
be justified by charging each positive increment to a distinct initial shadow
discrepancy. The existing cancellation example also blocks an unsigned path-count
argument. A viable proof has to exploit the finite **actual** support/FULL coupling
inside the zero-extension tower, or an equivalent ordered-erasure invariant.

## 5. Research fence

This note does not justify sampling `tau(2^n v)` for more seeds or larger `n`.
The exact missing statement is already (8), and finite samples cannot establish
it. It also does not claim that (8) follows from clock growth, from
`tau(2^n v)->infinity`, or from infinitely many cyclic births.

The useful next question is structural:

> Can the complete one-bit extension/eraser history force the partial sums in
> (12) to have unbounded positive excursions on the FULL finite-fringe domain?

A negative result should ideally exhibit an all-depth mechanism by which
`delta_v(n)` can compensate to average at most one while preserving the FULL
constraints; a finite prefix would not suffice.

Dependencies: `problem1_global_discrepancy_front.md` Sections 1-3;
`problem1_highest_wait_nonforcing.md` Sections 1-2 and 5; the original-cut
identity `L_(R+n)=2^n L_R` after a finite right support bound.