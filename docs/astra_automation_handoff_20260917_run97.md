# Astra automation handoff — run 97 — 2026-09-17

## Starting state

No intervening repository work was present after run 96. Starting branch tip: `7c60f96fadbc02e9df211f98574aaacec270628a`.

## New result / strategy fence

Added `proofs/informal/problem1_restart_excess_offset_is_covariant.md`.

For a finite row with right endpoint `R` and tail seed `v=L_R(r)`, the established physical-time tail conjugacy gives, for each fixed restart time `t` and eventually in tower index `n`,

    e_(T^t v)(n)=e_v(n+2t)+t.

The finite Rule-30 right edge advances exactly one site per physical step (`100 -> 1`), so the restarted endpoint is `R_t=R+t`. Hence

    e_(T^t v)(n)-R_t = e_v(n+2t)-R.

Thus the offset that actually controls physical delay is restart-covariant. The apparent `+t` gain in restarted excess is cancelled exactly by the `+t` motion of the right support edge. Hidden slack is transported the same way.

## Strategic consequence

Do not try to amplify bounded excess into a contradiction merely by restarting at large physical time. Restart deletes/reindexes a finite prefix but cannot improve the physical strip bound or create overshoot. A successful theorem must use genuinely non-covariant survivor-specific information from the complete finite fringe: bounded reuse, ordered erasure, or a mechanism forcing new maxima of `e_v(n)-R`.

## Problem 1 status

OPEN.

Research commit: `d085ee97175aff4c4bb1d82e711f16a966b33f09`.
