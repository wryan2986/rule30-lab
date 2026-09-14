# Exact zero-extension / physical-time renormalization

Status: `partial-proof`. This note gives an exact identity connecting the zero-extension tower `tau(2^n v)` to the preperiod of the actual unnormalized Rule-30 iterates `T^t(v)`. It does not solve Problem 1, but it replaces part of the abstract lift bookkeeping by a direct spacetime quantity on the original finite row.

## 0. Setup

Use the reviewed integer maps

    T(q) = q XOR ((q<<1) OR (q<<2)),
    A = sigma^2 T,

where `sigma(q)=q>>1`, and let

    h_v(n) = tau(2^n v).

For every integer `m>=0`, multiplication by `2^m` commutes with `T` exactly:

    T(2^m q) = 2^m T(q).                            (1)

This is immediate from the packed formula for `T`.

## 1. Exact spacetime renormalization

Fix integers `n,t>=0`. During the first `t` applications of `A` to

    2^(n+2t) v,

there are always at least two trailing zero bits available at each step. Using (1), one application gives

    A(2^(n+2t) v)
      = sigma^2 T(2^(n+2t) v)
      = 2^(n+2t-2) T(v).

Iterating gives the exact identity

    A^t(2^(n+2t) v) = 2^n T^t(v).                   (2)

For any eventually periodic state `x` and any `t>=0`, least preperiod obeys the elementary deterministic identity

    tau(A^t x) = max(tau(x)-t, 0).                  (3)

Apply (3) to (2). This yields

    tau(2^n T^t(v))
      = max(tau(2^(n+2t) v)-t, 0)
      = max(h_v(n+2t)-t, 0).                        (4)

Equation (4) is exact for all `n,t>=0`; no asymptotic assumption or FULL hypothesis is used.

Equivalently, in tower notation,

    h_(T^t v)(n) = max(h_v(n+2t)-t, 0).             (5)

## 2. The `n=0` bridge to the actual physical orbit

Setting `n=0` in (4) gives

    tau(T^t(v)) = max(h_v(2t)-t, 0).                (6)

Thus the even zero-extension subsequence has an exact dichotomy:

- if `h_v(2t)<=t`, then the actual physical Rule-30 row `T^t(v)` is already A-periodic;
- if `h_v(2t)>t`, then

      h_v(2t) = t + tau(T^t(v)).                    (7)

In the second branch the shift-tail excess is therefore

    e_v(2t) = h_v(2t)-2t
            = tau(T^t(v))-t.                        (8)

So positive excursions of the even tower excess are exactly positive excursions of the normalized physical-orbit preperiod `tau(T^t(v))-t`, whenever the latter is nonzero. The zero branch is not to be silently discarded: it is precisely the event that `T^t(v)` itself lies on an A-cycle.

## 3. General offset form

For fixed `n`, whenever `h_v(n+2t)>t`, equation (4) can be rewritten as

    e_(T^t v)(n) = e_v(n+2t) + t,                   (9)

or

    e_v(n+2t) = e_(T^t v)(n) - t.                  (10)

This is a genuine renormalization relation: advancing `t` physical Rule-30 steps and removing `2t` zero-extension bits changes the excess by exactly `t`, except when the target has collapsed all the way to preperiod zero, which is already isolated by the `max` in (4).

## 4. Why this matters for the current bottleneck

The previous automation notes reduced a finite physical delay strip to boundedness above of

    e_v(n)=h_v(n)-n,

then expressed its increments by the skip/residence ledger. Equation (6) gives an independent exact representation of the even subsequence directly on the original Rule-30 spacetime.

A future contradiction can therefore attack either of two sharply separated alternatives along large `t`:

1. `T^t(v)` is A-periodic often enough that `h_v(2t)<=t`; or
2. `T^t(v)` is nonperiodic under A, in which case the desired even-subsequence growth is exactly growth of

       tau(T^t(v))-t.

This is potentially more useful than treating the post-transient lift phase as arbitrary, because `T^t(v)` is the actual physical row descended from the fixed finite initial state.

No claim is made here that either alternative is already impossible. In particular, (6) by itself does not imply `limsup e_v(n)=infinity`.

## 5. Next target

Look for an existing FULL/front/finite-entry lemma that constrains the two branches in Section 4 for the actual row `T^t(v)`. A sufficient new theorem would be either:

- rule out `T^t(v)` being A-periodic for all sufficiently large `t` and prove `limsup_t [tau(T^t(v))-t]=infinity`; or
- derive a compensating front/birth event whenever `T^t(v)` enters an A-cycle.

This route should be compared against the maximal-skip-block ledger rather than replacing it: equation (4) may provide the missing common-origin constraint that arbitrary nested periodic lifts lack.

Dependencies: reviewed packed identities for `T` and `A`; `problem1_shift_tail_excess_reduction.md`; `problem1_shift_tail_residence_ledger.md`.

No claim of a Problem 1 solution is made here.
