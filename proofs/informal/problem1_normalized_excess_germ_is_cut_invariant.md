# Problem 1: normalized excess defines a cut-invariant tail germ

## Status

Exact structural lemma. Problem 1 remains open.

## Setup

Let `r` be one fixed finite Rule-30 row. Choose any right support bound `R` (not necessarily the least one), put

    v_R = L_R(r),
    e_R(n) = tau(2^n v_R) - n,
    q_R(n) = e_R(n) - R.

The previous support-bound covariance lemma proves that if `R'=R+m`, `m>=0`, then

    q_(R')(n) = q_R(n+m)                         (1)

for every `n>=0`.

## Lemma: all admissible cuts represent one tail germ

For any two admissible right support bounds `R1,R2`, the sequences `q_R1` and `q_R2` agree after deleting a finite prefix from the sequence belonging to the smaller cut. More precisely, if `R2>=R1`, then

    q_R2(n) = q_R1(n + R2-R1)                   (2)

for every `n>=0`.

Thus the equivalence class

    Q(r) := [ q_R ]  modulo deletion of finite prefixes

is independent of the arbitrary support bound `R`.

### Proof

Take `m=R2-R1` in (1). This gives (2) exactly. Since every pair of admissible cuts is comparable, all `q_R` lie in the same finite-prefix equivalence class. QED.

## Consequences

Every tail property invariant under deletion of finitely many terms is an intrinsic property of the finite row rather than of the bookkeeping cut. In particular the following statements do not depend on `R`:

- `q_R` is bounded above;
- `q_R` is unbounded above;
- `limsup q_R = +infinity`;
- `q_R` takes positive values infinitely often;
- for every `K`, `q_R(n)>K` for some arbitrarily large `n`.

The physical delay identity is

    tau(Y_(R+n)) = max(q_R(n),0).

Hence eventual confinement to a fixed physical strip is exactly an upper-bound statement about the intrinsic germ `Q(r)`, while the desired contradiction is exactly unboundedness above of that germ.

## Why this is useful

Run 98 showed that moving the cut cannot manufacture overshoot. The present formulation removes the cut altogether: future arguments can and should be stated directly for `Q(r)`. This prevents accidental dependence on absolute `R` or zero padding and identifies the remaining object that a complete-fringe invariant must control.

In particular, any proposed finite resource `F(r,R)` whose only change under `R -> R+m` is the appended zero padding cannot prove the needed theorem unless it descends to the germ `Q(r)` or couples to genuinely intrinsic support/fringe data. The missing theorem can now be formulated cleanly as:

> On the FULL finite-fringe domain of an actual finite survivor, prove that the intrinsic normalized-excess germ `Q(r)` is unbounded above.

This is stronger as a formulation, not a solution: no all-depth mechanism forcing that unboundedness is proved here.

## Relation to restart covariance

The physical-time restart lemma similarly says that restarting deletes/reindexes a finite part of the normalized physical-excess history. Consequently the obstruction sought for Problem 1 should be stable under finite-prefix deletion but must use information not erased by the complete original finite fringe. The natural candidates remain bounded-use fringe events or an ordered-erasure quantity attached to actual support rather than nominal cuts.
