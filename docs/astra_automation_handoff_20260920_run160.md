# Automation handoff — run160 — 2026-09-20

Problem 1 remains OPEN. Continue on `research/astra-next`.

## New result

The `g_{t+5}=2` hidden-slack branch is now completely excluded.

Run159 translated the two surviving g=2 front itineraries into exact original-global-shadow patterns at `q=t+2`:

- `(1,0,0,4)` requires `hat r_1(q)=0`;
- `(0,1,0,4)` requires `(hat r_1(q),hat r_2(q))=(1,1)`.

The older all-depth nonreset-return theorem (`problem1_nonreset_return_birth_spacing.md`, eq. (3)) already transports the SAME global E-shadow and proves

    (hat r_1(q),hat r_2(q))=(1,u*(a OR b)).

For the TWO-BIT t source, `u=0`, so the pair is exactly `(1,0)`. This contradicts both surviving run159 patterns. The third g=2 itinerary was already excluded in run157. Therefore `g_{t+5} != 2`.

Combined with run154's exclusion of g=3:

    0 <= g_{t+5} <= 1.

By run153's exact repayment identity,

    s_{t+6}-s_{t+5}=g_{t+5}+2 in {2,3}.

Full argument: `proofs/informal/problem1_run160_global_shadow_excludes_g2.md`.

## Next target

Only `g=1` remains between the current result and exact zero terminal hidden slack. Run155 says `g>=1` forces actual driver bit `r_3(q)=1`; the older transported-shadow identity fixes only `(hat r_1,hat r_2)(q)=(1,0)` for this two-bit source. Seek a bridge from the one-unit original-cut residence to a wider original-shadow bit/first-discrepancy condition, or use the earlier global-shadow transport identities to classify the g=1 front itinerary exactly. Do not redo g=2 core/residence cases.
