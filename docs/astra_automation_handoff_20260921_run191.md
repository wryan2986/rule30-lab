# Astra automation handoff — run 191 — 2026-09-21

Problem 1 remains OPEN.

## New exact continuation

There was no intervening work after run 190. Continue the beta=1 trajectory from the forced resetting positive-delay passage at `t+8`.

Run 189 gives actual `0000` at positions `0..3` on row `t+7` and shadow `(hat r_0,hat r_1,hat r_2)=(0,1,0)`. Since `m(t+7)=1`, write the two shared cells immediately left of center as

\[
A=r_{-2}(t+7),\qquad B=r_{-1}(t+7).
\]

Direct Rule-30 propagation gives at `t+8`

\[
r_{-1}=\hat r_{-1}=A\oplus B,
\]
\[
r_0=B,\qquad \hat r_0=1\oplus B,
\]
\[
r_1=0,\qquad \hat r_1=1.
\]

Therefore at `t+9`

\[
d_{-1}=1\oplus A\oplus B,\qquad d_0=1\oplus B,\qquad d_1=0.
\]

This yields an exact front trichotomy:

- `A=B`: `m(t+9)=-1`, `J(t+9)=t+8`, hence `s_(t+8)>=t+10` and `Delta_(t+7)>=3`.
- `(A,B)=(1,0)`: `m(t+9)=0`, `J(t+9)=t+9`, hence the characteristic-`t+8` residence exits exactly with `s_(t+8)=t+9` and `Delta_(t+7)=2`.
- `(A,B)=(0,1)`: `d_-1=d_0=d_1=0`, hence `m(t+9)>=2`, `J(t+9)>=t+11`; the global front skips `t+9` and at least `t+10`, corresponding to zero-length intervening residences.

See `proofs/informal/problem1_run191_tplus9_front_trichotomy.md`.

## Next target

Determine or constrain `(A,B)=(r_-2,r_-1)(t+7)` from the retained complete beta=1 return driver/global threshold structure. Check the exceptional `(0,1)` front-jump branch first against finite-entry and threshold constraints; it may be structurally impossible without requiring wider propagation.
