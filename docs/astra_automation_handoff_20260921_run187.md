# Astra automation handoff — run 187 — 2026-09-21

Problem 1 remains OPEN.

## New result

Run 186's remaining bit

\[
\alpha=r_0(t+6)\oplus(r_3(t+6)\lor r_4(t+6))
\]

does **not** actually depend on the wider-right driver.  Starting from the proved cyclic-row prefix at `t+4`,

\[
(r_0,r_1,r_2,r_3)=(1,1,1,0),
\]

write

\[
a=r_{-2}(t+4),\qquad b=r_{-1}(t+4).
\]

Two literal Rule-30 steps give

\[
\boxed{\alpha=1\oplus a\oplus b}.
\]

So `alpha=1` iff the two cells immediately left of the rigid prefix agree.  Exhaustive local checking over `(a,b,r4,r5,r6)` confirms complete cancellation of `r4,r5,r6`.

If `t+8` is nonresetting, run 185 therefore becomes:

* `a=b`: gate `u`, one-bit, `tau=1`, `Delta_(t+7)=2`;
* `a!=b`: gate `t`, two-bit, `tau=2`, `Delta_(t+7)=3`.

See `proofs/informal/problem1_run187_alpha_cancels_wider_right_driver.md`.

## Next target

Do not spend another run transporting arbitrary right cells from `t+4`; they provably cancel from `alpha`.  Instead determine the pair `(r_-2,r_-1)(t+4)` from the complete cyclic driver, cyclicity constraints, and/or the global-front/return structure.  The key question is whether those constraints force equality or inequality of this pair.  Separately, the classification remains conditional: a proof is still needed that the forced positive-delay row at `t+8` is or is not nonresetting.
