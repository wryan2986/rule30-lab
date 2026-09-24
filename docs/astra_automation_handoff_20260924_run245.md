# Astra automation handoff — run 245 — 2026-09-24

Problem 1 remains open.

## Entry state

The branch entered at run 244 commit `c0e6cf24a462998325564d745912198daad9285d`; there was no intervening work.

## Main correction

Run 244's exact identities remain valid:

- `Delta D = bar B`;
- `parity(H) = parity(Y0) xor <D,C>` for the final doubling decision in a local `double / plateau / double` pattern.

However, the claimed computational evidence that the final doubling *selects* the high-complexity plateau branch is confounded.

The two cited examples, `4 -> 8 -> 8 -> 16` and `16 -> 32 -> 32 -> 64`, actually sit inside

- `2 -> 4 -> 8 -> 8 -> 16`,
- `8 -> 16 -> 32 -> 32 -> 64`.

Thus their first displayed doubling is the second of two consecutive doublings. Run 243 already forces maximal lower complexity on such witnesses, and run 242 then forces the high-complexity plateau branch before the final-doubling functional is evaluated. The final doubling therefore does not provide independent evidence for a selection theorem.

A direct exhaustive sanity check of the small chain confirms that once the full preceding prefix-period history is imposed, every relevant period-8 plateau word is already in cyclic linear-complexity class 8. Lower-complexity period-8 words arise only when the full consecutive-doubling history is not imposed.

## File added

- `proofs/informal/problem1_run245_double_plateau_double_evidence_is_confounded.md`
- this handoff

## Next target

Keep the run-244 decision functional, but do not assume its proposed complexity-selection interpretation. Search for the first genuine `D/P/D` order pattern whose initial `D` is not preceded by another `D` (especially `P/D/P/D`), and test the functional there. If no such pattern appears, investigate whether `P/D/P/D` is itself forbidden. Symbolically, the open task is to classify `parity(Y0) xor <D,C>` without importing run-243 compatibility from an earlier consecutive doubling.
