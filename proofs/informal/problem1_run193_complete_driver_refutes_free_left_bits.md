# Problem 1 run 193: the complete beta=1 driver refutes the free-left-bit continuation

Status: exact consistency check and correction; Problem 1 remains open.

## Purpose

Run 192 treated

\[
(q,r,s,a)=(r_{-5},r_{-4},r_{-3},r_{-2})(t+4)
\]

as locally free, subject only to the later-derived relation on `r_-1`. Its handoff explicitly asked whether the retained complete beta=1 driver

\[
Y_{t+4}=G(z)=16A^4z+7
\]

constrains those cells. It does, immediately and strongly enough to expose an inconsistency in the run 188--192 continuation.

## Exact decoding of the complete driver

By the established cut convention

\[
Y_t=L_0(r(t))=\sum_{i\le 0}r_i(t)2^{-i}.
\]

Therefore bit `k` of `Y_t` is exactly `r_-k(t)`. Since

\[
Y_{t+4}=16A^4z+7,
\]

the four low bits are fixed to binary `0111` (least-significant bit first: `1,1,1,0`). Hence

\[
\boxed{r_0(t+4)=1,\quad r_{-1}(t+4)=1,\quad r_{-2}(t+4)=1,\quad r_{-3}(t+4)=0.}
\]

In run-192 notation this gives

\[
\boxed{s=0,\qquad a=1,\qquad b:=r_{-1}(t+4)=1.}
\]

Thus the 16-assignment census in run 192 is not a census of the actual complete beta=1 return domain. In particular its imported relation `b=1 xor a` is incompatible with the retained complete driver: the driver forces `(a,b)=(1,1)`, while that relation would force `(1,0)`.

## Independent two-step physical check

The conflict is visible without any core algebra. Combine the complete-driver left cells with the already-used actual right prefix at `t+4`,

\[
(r_0,r_1,r_2,r_3)=(1,1,1,0).
\]

Around the center the row is therefore

\[
(r_{-2},r_{-1},r_0,r_1,r_2)=(1,1,1,1,1).
\]

One literal Rule-30 step gives

\[
(r_{-1},r_0,r_1)(t+5)=(0,0,0),
\]

and the next gives

\[
\boxed{r_0(t+6)=0.}
\]

This agrees with the run-188 local identity `x=a xor b` when the *actual complete-driver values* `a=b=1` are substituted. It contradicts run 189's later conclusion `x=1`.

Therefore the first definite break in the recent continuation is the step used in run 189 to force `x=1` (ultimately the asserted eraser/front datum `d_0(t+7)=0` imported there), not the direct Rule-30 identity `x=a xor b`. Any downstream result that depends on `x=1` -- including the rigid `0000` block at `t+7`, the run-190 exclusion, and the run-191/192 front trichotomy specialized from that block -- is not currently established and must not be used until the incompatible front/eraser premise is repaired.

## What remains valid

The complete beta=1 driver formula itself was proved in `problem1_nonreset_return_birth_spacing.md` from the same complete nonresetting source and is the stronger all-depth datum that run 192 was supposed to restore. Its low-bit consequence is exact under that theorem's stated domain.

The useful corrected terminal-center fact is therefore

\[
\boxed{x=r_0(t+6)=0}
\]

for this beta=1 two-bit-return trajectory, assuming the established complete-driver formula and the already-used right prefix.

This does **not** by itself resolve Problem 1 or classify the post-terminal global discrepancy front. That front must now be recomputed with `x=0` from the fixed global shadow, rather than inheriting run 189's inconsistent eraser assertion.

## Next target

Return to the last pre-conflict shadow data (runs 181--188), audit the derivation of `m(t+7)=1` / `d_0(t+7)=0` against the complete driver, and recompute the actual/shadow discrepancy at `t+7,t+8` with `x=0`. Do not continue the run-191/192 `(A,B)` branch analysis until that reconciliation is complete.

Dependencies: `problem1_global_cycle_shadow.md` Section 1 (cut convention); `problem1_nonreset_return_birth_spacing.md` Section 3 (complete driver `G(z)`); `problem1_run188_alpha_is_complement_terminal_center.md`; `problem1_run189_terminal_center_is_forced_one.md`.