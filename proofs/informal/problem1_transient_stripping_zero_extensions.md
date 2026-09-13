# Exact stripping of inherited transients in a zero-extension tower

Status: `partial-proof`. This note gives an exact transient-removal identity for consecutive zero extensions. It does **not** prove the residence ledger has unbounded positive excursions and does not close Problem 1.

## 0. Purpose

The current handoff isolates the missing step as a transient-aware analogue of the purely periodic two-step compensation lemma. The inherited transient is not actually opaque: if its exact length is used as a checkpoint, the first few zero extensions become explicit finite lifts of a periodic core.

This note records that reduction. It also shows precisely what remains after the inherited transient is stripped: the difficulty is the phase/initial bits of those finite lifts, not the old transient history itself.

## 1. Setup

Let `y>0` be finite and eventually A-periodic, and put

    H = tau(y).

Write

    u = T^H(y),
    c = A^H(y) = sigma^(2H) u.

By definition of `H`, `c` is A-periodic. We use only the reviewed identities

    A^H = sigma^(2H) T^H,

and commutation of `T` with multiplication by powers of 2.

For `m>=0`, define the m-bit post-transient lift

    x_m = A^H(2^m y).

Then exactly

    x_m = sigma^(2H) T^H(2^m y)
        = sigma^(2H) (2^m u).                        (1)

When `0<=m<=2H`, this is

    x_m = sigma^(2H-m) u.                            (2)

In particular,

    x_0 = c,
    sigma(x_1)=x_0,
    sigma(x_2)=x_1.                                  (3)

Thus after the inherited transient has elapsed, the next one and two zero extensions are literally a one-bit and two-bit lift of the periodic core.

## 2. Exact preperiod splitting

Claim. For every `m>=0`,

    tau(2^m y) = H + tau(x_m).                       (4)

Proof. Spatial deletion cannot increase least preperiod, so deleting `m` low bits gives

    tau(2^m y) >= tau(y)=H.                          (5)

On the other hand, after exactly `H` A-steps the state is `x_m`. If `tau(x_m)=t`, then after another `t` steps it is periodic, hence

    tau(2^m y) <= H+t.                               (6)

Let `K=tau(2^m y)`. By (5), `K>=H`. Since `A^H(2^m y)=x_m`, periodicity at time `K` implies that `A^(K-H)x_m` is periodic. Therefore

    tau(x_m) <= K-H,                                 (7)

or `K>=H+tau(x_m)`. Combining with (6) proves (4).

This is an exact equality, not a bound.

## 3. Consecutive ledger increments reduce to lift preperiods

Now specialize to a zero-extension tower. Let

    y = 2^n v,
    H = tau(y)=h_n,

and retain `x_m=A^H(2^m y)`. Then (4) gives

    h_(n+m) = H + tau(x_m).                          (8)

For the first increment,

    delta_n = h_(n+1)-h_n
            = tau(x_1).                              (9)

For the next two increments together,

    delta_n + delta_(n+1)
      = h_(n+2)-h_n
      = tau(x_2).                                    (10)

Hence the exact two-step residence-ledger contribution is

    (delta_n-1)+(delta_(n+1)-1)
      = tau(x_2)-2.                                  (11)

This is the transient-aware form of the earlier purely periodic calculation.

A skip at characteristic `n+1` is exactly

    delta_n=0
    iff tau(x_1)=0
    iff x_1 is A-periodic.                           (12)

So at any skipped characteristic, after stripping the inherited transient the problem becomes:

> `x_0` is periodic, `x_1` is a periodic one-bit lift of `x_0`, and `x_2` is the actual one-bit lift of `x_1` selected by the post-transient phase. How small can `tau(x_2)` be?

The original transient before time `H` has disappeared completely from this formulation.

## 4. Why the old periodic-source lemma does not automatically transfer

The earlier local compensation lemma started from a very special lift: literal multiplication by 2 at physical time zero. In that setting the newly inserted low bit is known to be zero, and for the next extension the driven low response starts from

    w_0=0.

After stripping an inherited transient, (2) shows that `x_1` and `x_2` are determined by adjacent bits of

    u=T^H(y).

Their newly exposed low bits are therefore phase data from `u`; they are not automatically zero. Even if `x_1` is a period-doubled periodic lift of `x_0`, the earlier proof cannot be copied unless the required initial low-bit condition is re-established for this post-transient lift.

For a genuine tower `y=2^n v`, commutation gives

    u = T^H(2^n v)=2^n T^H(v).                       (13)

So `u` has `n` trailing zero bits. But the low bit of `x_2` in (2) is bit `2H-2` of `u`. The tower zeros force this bit to vanish only under

    2H-2 < n.                                        (14)

That inequality is not available in the bounded-strip regime one is trying to contradict: there `H=tau(2^n v)` may be approximately `n+O(1)`, making `2H-2` much larger than `n`.

Thus inherited-transient stripping succeeds exactly, but it exposes a genuine phase obstruction rather than removing the whole difficulty.

## 5. Sharpened target

The residence-ledger problem can now be attacked locally at each skip without carrying the old transient history.

At a skip, `x_1` is periodic. The two-step ledger is nonnegative exactly when

    tau(x_2) >= 2,                                   (15)

and strictly positive exactly when `tau(x_2)>=3`.

Therefore a useful next theorem would be one of the following.

1. **All-skip compensation:** prove `tau(x_2)>=2` for every post-transient skip arising from the FULL zero-extension tail.
2. **Doubling-skip compensation with phase control:** for skipped lifts that double the least period, prove the actual post-transient phase cannot select a recurrent low-bit state immediately.
3. **Controlled failure:** classify the skips with `tau(x_2)<2` and show they force enough later surplus to compensate.

The exact reduction (9)-(12) means no further work is needed on how to transport the inherited transient itself. What remains is the finite-lift phase problem over a periodic core.

No claim is made that (15) holds universally; the present note deliberately stops before that unsupported step.

Dependencies: `problem1_shift_tail_residence_ledger.md`; `problem1_highest_wait_nonforcing.md` Section 2; reviewed identities `A^H=sigma^(2H)T^H`, `T(2^m z)=2^m T(z)`, and monotonicity of least preperiod under spatial deletion.
