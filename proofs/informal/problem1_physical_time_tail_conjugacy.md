# Physical-time tail conjugacy of the zero-extension ledger

Status: `partial-proof`. This note strengthens `problem1_zero_extension_time_renormalization.md` by removing its `max` ambiguity on every sufficiently far zero-extension tail. It gives an exact conjugacy between the residence ledger of a finite row and that of any fixed physical Rule-30 iterate.

## 0. Setup

Let

    T(q) = q XOR ((q<<1) OR (q<<2)),
    A = sigma^2 T,
    h_v(n) = tau(2^n v),
    e_v(n) = h_v(n)-n.

For every nonzero finite `v`, the established zero-extension theorem gives

    h_v(n) -> infinity as n -> infinity.                 (1)

Also `T^t(v)` remains nonzero and finite for every fixed `t>=0`.

The preceding renormalization note proved, for all `n,t>=0`,

    h_(T^t v)(n) = max(h_v(n+2t)-t, 0).                 (2)

## 1. The max branch disappears on every fixed physical-time tail

Fix `t>=0`. By (1), there is an index `N_t` such that

    h_v(n+2t) > t

for every `n>=N_t`. Therefore (2) becomes the exact tail identity

    h_(T^t v)(n) = h_v(n+2t)-t                         (3)

for every `n>=N_t`.

Thus the zero-extension preperiod sequence of the physical row `T^t(v)` is, after finitely many entries, exactly the original sequence shifted left by `2t` in tower index and down by `t` in preperiod.

Subtracting `n` gives

    e_(T^t v)(n) = e_v(n+2t)+t,                        (4)

or equivalently

    e_v(n+2t) = e_(T^t v)(n)-t.                        (5)

This is unconditional for all sufficiently large `n`; unlike the pointwise form in the preceding note, no residual periodic/nonperiodic branch remains at infinity for fixed `t`.

## 2. Exact tail transport of residence increments

Write

    delta_v(n) = h_v(n+1)-h_v(n).

Applying (3) at `n` and `n+1` yields, for every sufficiently large `n`,

    delta_(T^t v)(n) = delta_v(n+2t).                  (6)

Hence skips (`delta=0`), one-step residences (`delta=1`), and long residences (`delta>=2`) are transported exactly under fixed physical time, modulo deletion of a finite prefix.

In particular, if

    Z_v([a,b)) = #{a<=n<b : delta_v(n)=0}

and

    P_v([a,b)) = sum_{a<=n<b, delta_v(n)>=2}(delta_v(n)-1),

then for all sufficiently large `a<b`,

    Z_(T^t v)([a,b)) = Z_v([a+2t,b+2t)),              (7)

    P_(T^t v)([a,b)) = P_v([a+2t,b+2t)).              (8)

So the signed skip/residence ledger itself is a physical-time tail invariant up to translation.

## 3. Limsup invariance of the scalar target

From (4), finite index deletion does not affect limsup, and therefore

    limsup_(n->infinity) e_(T^t v)(n)
      = t + limsup_(n->infinity) e_v(n).              (9)

Equivalently,

    limsup e_v = infinity

if and only if

    limsup e_(T^t v) = infinity                       (10)

for any (hence every) fixed physical time `t`.

Likewise, eventual boundedness above of `e_v` is invariant under replacing `v` by any fixed `T^t(v)`; only the numerical upper bound changes by the additive constant `t`.

This matters for the finite-delay-strip contradiction: one may restart the argument at an arbitrarily late but fixed physical row without changing whether the required unbounded-excess conclusion is true.

## 4. Relation to the pointwise A-periodic branch

The earlier identity at `n=0`,

    tau(T^t(v)) = max(h_v(2t)-t,0),

still has a genuine A-periodic branch. The present note does **not** rule out `tau(T^t(v))=0` at isolated or infinitely many physical times.

What it does show is that such a collapse is a finite-index phenomenon from the viewpoint of the restarted zero-extension tower. For each fixed `t`, once enough additional zero bits are appended, the restarted tower rejoins the original residence ledger exactly by (3) and (6).

Therefore a proof strategy that attempts to extract permanent ledger savings merely from `T^t(v)` lying on an A-cycle cannot work without an additional mechanism: those savings cannot alter the asymptotic tail ledger after the physical restart.

## 5. Consequence for the current bottleneck

The common-origin condition missing from arbitrary nested-lift counterexamples can now be expressed very sharply:

> physical evolution does not generate a new asymptotic zero-extension ledger; it only removes a finite prefix and translates the surviving ledger.

Thus the preferred next use of FULL/front machinery is not to compare unrelated restarted ledgers. It should establish a statement that can be applied after an arbitrarily late physical restart and is incompatible with a single tail ledger remaining bounded above.

A potentially useful contradiction template is:

1. assume `e_v` is eventually bounded above;
2. restart at an arbitrarily late physical time `t` where the FULL/front geometry has a desired local form;
3. use (3)-(8) to identify the restarted skip/residence ledger with the original far tail;
4. prove a restart-local front/birth obligation producing a ledger gain whose size is independent of the discarded prefix;
5. iterate such obligations at separated physical restarts to force unbounded positive ledger excursions.

No such gain theorem is proved here. The contribution of this note is the exact all-depth transport needed to make a restart-based argument legitimate.

Dependencies: `problem1_zero_extension_time_renormalization.md`; established divergence `tau(2^n v)->infinity` for every nonzero finite `v`; `problem1_shift_tail_residence_ledger.md`.

Problem 1 remains open.
