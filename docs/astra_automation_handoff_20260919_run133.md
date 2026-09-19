# Astra automation handoff — 2026-09-19 — run 133

Problem 1 remains OPEN.

Starting branch tip was `a627b68aa13d82d4069f6c39659baf040b38157f`; no intervening work was present after run132.

## New result / correction

The run130 `001/011` fork at the preceding cyclic `t` source is not actually free under FULL.

Let `q=t+2`. FULL gives the center transition

    r_0(q)=1,
    r_0(q+1)=0.

Rule 30 at the center is

    r_0(q+1) = r_-1(q) XOR (r_0(q) OR r_1(q))
             = r_-1(q) XOR 1.

Therefore

    r_-1(q)=1.

The earlier provenance calculation already established `r_-2(q)=0`, so the predecessor neighborhood producing `r_-1(q+1)=1` is exactly `011`, never `001`.

Thus every relevant forced-birth sensitive-one lineage terminates at the unique `011` obstruction at the preceding cyclic `t` source. The four-step endpoint question from run132 (`r_-2(q+4)=0?`) is unnecessary for deciding this fork; the run132 lemma remains correct but is weaker for this application.

A local exhaustive sanity check agrees. More strongly, the proof shows the center drop `1 -> 0` alone forces the fork bit; neither the gate nor the `r_-2` condition is needed for that bit.

## Next target

Do not pursue fork-bit parity/telescoping: the fork is constant under FULL. Focus specifically on the distinguished family of `011` events at cyclic `t` sources. Determine whether successive such source-relative `011` events have an ordering, spacing, or bounded-reuse law tied to finite actual initial support. Generic `011` scarcity is already refuted by run128, so any useful theorem must exploit their source-relative/cyclic placement.

New proof note: `proofs/informal/problem1_full_center_drop_forces_011_at_cyclic_t_source.md`.
