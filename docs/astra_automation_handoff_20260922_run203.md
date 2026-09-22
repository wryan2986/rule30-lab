# Astra automation handoff — 2026-09-22 run 203

Problem 1 remains OPEN.

## New result

Continue only the corrected run-193--203 chain.

Run 202 reduced the finite-fringe tail to `a_n=tau(2^n x)` and showed that positive late renewals require

    a_n > max(a_(n-1), b+n)

infinitely often for an alleged finite FULL seed.

Run 203 combines the standard deterministic preperiod identity

    tau(A^H y)=max(tau(y)-H,0)

with the already-reviewed exact formula

    A^H(2^n x)=2^(n-2H) T^H(x)   (n>=2H)

to obtain

    max(a_n-H,0)=tau(2^(n-2H) T^H x).

At half depth this becomes

    max(a_(2m)-m,0)=tau(T^m x),
    max(a_(2m+1)-m,0)=tau(2 T^m x).

Therefore the physical diagonal conditions renormalize exactly:

    a_(2m)>b+2m       iff tau(T^m x)>b+m,
    a_(2m+1)>b+2m+1   iff tau(2 T^m x)>b+m+1.

This is not yet the missing contradiction, but it turns the zero-extension rate question into a scale-halved preperiod question along the explicit `T` orbit. A sufficient next theorem is that both renormalized inequalities fail eventually for every fixed finite `x` (with the fixed original-fringe constant `b`).

Do not sample shift towers and do not return to local driver-bit propagation. Target structural control of `tau(T^m x)` and `tau(2T^m x)` relative to `m`, using the explicit triangular/linear form of `T` plus the existing erasing-history/cycle-completion machinery. Also remember that eliminating above-diagonal events is stronger than necessary: FULL additionally needs the strict increase `a_n>a_(n-1)`.

Proof note: `proofs/informal/problem1_run203_shift_tower_renormalization.md`.