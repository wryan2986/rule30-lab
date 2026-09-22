# Problem 1 run 203 — exact renormalization of the finite-fringe shift tower

Status: `partial-proof`. Problem 1 remains OPEN.

Continue only the corrected run-193--202 chain. Run 202 reduced the finite-fringe tail to

    a_n := tau(2^n x),

where `x=L_b>0` is fixed, and showed that a positive late renewal at tail index `n` is equivalent to

    a_n > max(a_(n-1), b+n).                                  (1)

This note gives an exact scale-halving identity for `a_n`. It does not prove the needed diagonal bound, but it replaces the zero-extension rate question by a dynamically renormalized one involving the already-established linear map `T`.

## 1. Deterministic preperiod shift

For any eventually periodic state `y` under `A`, with least preperiod `tau(y)`, determinism gives

    tau(A^H y) = max(tau(y)-H, 0)                              (2)

for every `H>=0`.

Proof: if `H<tau(y)`, the point `A^H y` lies exactly `tau(y)-H` edges before the first cyclic point on the same functional-graph tail. If `H>=tau(y)`, it is already cyclic. Minimality is preserved because an earlier cyclic point after shifting back would contradict minimality of `tau(y)`.

## 2. Combine with the exact zero-extension identity

The reviewed identity used in `problem1_highest_wait_nonforcing.md` is, for `n>=2H`,

    A^H(2^n x) = 2^(n-2H) T^H(x),                             (3)

where

    T(q) = q XOR ((q<<1) OR (q<<2)).

Apply (2) to the left side of (3). For every `n>=2H`,

    max(a_n-H,0)
      = tau(2^(n-2H) T^H(x)).                                 (4)

This is exact; no asymptotic or FULL assumption is used.

Taking the largest possible half-depth gives two useful identities. For `m>=0`,

    max(a_(2m)-m,0)   = tau(T^m x),                            (5)
    max(a_(2m+1)-m,0) = tau(2 T^m x).                          (6)

Thus any ABOVE-DIAGONAL event has an equivalent renormalized delay condition. In particular,

    a_(2m) > 2m  iff  tau(T^m x) > m,                          (7)

and

    a_(2m+1) > 2m+1  iff  tau(2 T^m x) > m+1.                 (8)

The implications are safe because either strict inequality forces the relevant left side of (5)/(6) to be positive, so the `max` branch is known.

More generally, the run-202 physical threshold is `b+n`, so

    a_(2m) > b+2m
      iff tau(T^m x) > b+m,                                    (9)

    a_(2m+1) > b+2m+1
      iff tau(2 T^m x) > b+m+1.                                (10)

Again these equivalences hold whenever the displayed strict inequality is tested; a positive right side forces the positive branch of (5)/(6), and conversely substitution recovers the left side.

## 3. Consequence for the FULL obstruction

Run 202 says an alleged finite FULL seed requires infinitely many indices satisfying (1). In particular it requires infinitely many indices above the physical diagonal. Equations (9)--(10) show that these cannot be treated as an opaque growth-rate question for zero extensions alone: after halving physical depth, they are exactly superlinear preperiod events for the orbit family

    T^m x   or   2 T^m x.

So a sufficient all-depth theorem is now equivalently narrowed to either parity:

    tau(T^m x) <= b+m eventually,
    tau(2 T^m x) <= b+m+1 eventually.                          (11)

This would eliminate all sufficiently late above-diagonal events, hence all sufficiently late positive renewals, contradicting FULL.

The strict-increase condition `a_n>a_(n-1)` in (1) is not used here. Therefore (11) is stronger than necessary; failure of (11) would not by itself produce FULL.

## 4. What this does and does not settle

This is genuine reduction, not a proof of (11). It also exposes why the theorem `a_n->infinity` is too weak: (5)--(6) allow `a_n<=floor(n/2)` exactly when the renormalized state is already cyclic, while above-diagonal behavior corresponds to the renormalized state retaining a tail longer than the halved physical depth.

The next useful target is therefore structural control of `tau(T^m x)` and `tau(2T^m x)` relative to `m`, using the explicit linear/triangular form of `T` together with the existing erasing-history or cycle-completion machinery. Do not return to numerical sampling of `a_n`, and do not infer (11) merely from finite width: individual erasing waits can exceed one.

Dependencies: `problem1_run202_finite_fringe_shift_tower_reduction.md`; `problem1_highest_wait_nonforcing.md` Sections 2 and 4; reviewed identities for `A`, `T`, and least preperiod.