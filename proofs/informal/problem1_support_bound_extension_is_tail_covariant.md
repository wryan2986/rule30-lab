# Extending the right support bound only reindexes normalized excess

Status: exact structural identity / strategy fence. This does **not** close Problem 1.

## Statement

Fix a nonzero finite Rule-30 row `r`. Let `R` be any right support bound and put

    v = L_R(r) > 0,
    e_v(n) = tau(2^n v) - n.

If the same row is represented using a later right support bound

    R' = R + m,   m >= 0,

then, because all bits after `R` are zero,

    v' = L_(R')(r) = 2^m v.

For every `n>=0`,

    e_(v')(n) - R'
      = tau(2^n v') - n - (R+m)
      = tau(2^(n+m) v) - n - R - m
      = e_v(n+m) - R.

Hence

    boxed:  e_(2^m v)(n) - (R+m) = e_v(n+m) - R.

Equivalently, extending the nominal support bound by `m` zeros deletes the first
`m` entries of the normalized-excess sequence and changes nothing else.

Using the established physical-delay identity

    tau(Y_(R+n)) = max(e_v(n)-R, 0),

this is exactly what it must be geometrically: the later support-bound convention
starts at physical cut `R+m`, so it sees the same physical-delay tail beginning
`m` cuts later.

## Consequences

1. The absolute quantity `e_v(n)` is representation-dependent. The physically
   meaningful scalar is `e_v(n)-R` together with its physical cut index.

2. Any proposed finite-support contradiction that improves merely by choosing a
   later support bound is spurious. Appending nominal zero support increases both
   `e` and `R` by the same amount after reindexing.

3. This is the spatial analogue of the fixed-physical-time restart covariance:
   neither temporal restart nor extension of the nominal right support bound can
   amplify a bounded physical strip into a contradiction. Both operations only
   remove a finite prefix of the same normalized physical excess.

4. Therefore a survivor-specific non-covariant resource cannot be the arbitrary
   numerical value of `R` or the number of trailing zero cuts included in the
   representation. A viable bounded-reuse / ordered-erasure argument must be tied
   to intrinsic data such as the actual finite support (for example its last 1,
   support width relative to a fixed origin, or complete fringe information).

## Relation to the target

The desired contradiction remains unbounded positive excursions of

    e_v(n)-R = tau(2^n v) - (R+n)

for the actual tail seed. The identity above shows that this target is invariant,
up to deletion of a finite prefix, under replacing `(R,v)` by `(R+m,2^m v)`.
Thus no proof can obtain the missing overshoot simply by moving the bookkeeping
cut farther into the zero tail.

Dependencies: `problem1_shift_tail_excess_reduction.md`,
`problem1_restart_excess_offset_is_covariant.md`.
