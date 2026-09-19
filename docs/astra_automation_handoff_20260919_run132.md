# Astra automation handoff — 2026-09-19 — run 132

Problem 1 remains OPEN.

Starting branch tip was `354f5f847bdeae9814e6aca1585d3ad46ddb0f3d`; no intervening work was present after run131.

## New result

Run131 asked whether the source-relative XOR fork identities can align across successive episodes. A sharp four-step local recurrence was found.

At a relevant cyclic source `q`, assume the established source condition `r_-2(q)=0` and FULL center word

    r_0(q..q+4)=10101.

If the same relative cell is zero four steps later,

    r_-2(q+4)=0,

then exact Rule-30 evolution forces

    r_-1(q)=1.

Thus the earlier sensitive-one provenance fork is necessarily the exceptional `011` branch; `001` is impossible.

An exhaustive exact census over the nine-cell dependency cone `r_-6(q)..r_2(q)` checks all 512 assignments. Exactly six satisfy the two zero endpoints plus center `10101`, and every one has `r_-1(q)=1`. The later fork bit `r_-1(q+4)` remains free.

This means a four-step recurrence of the source-relative zero condition does not yield a free telescoping parity chain; it rigidifies the earlier discrepancy to 1.

## Important limitation

Do not yet apply this to every forced-birth episode. In the established passage, `q=t+2` is the cyclic `t` source, `t+4` is the cyclic `u` source, and `t+6=q+4` is the forced new one-bit row. The repository has not yet proved that this new row satisfies the exact endpoint condition `r_-2(t+6)=0`.

## Next target

Use the complete forced-birth identities to determine `r_-2(t+6)`. If it is forced to 0, combine that fact with the new four-step lemma to force every preceding `q=t+2` provenance fork to `011`. If it is not forced, record its exact freedom/counterexamples and stop pursuing this recurrence as a global birth budget.

New proof note: `proofs/informal/problem1_four_step_zero_staircase_forces_011_fork.md`.
