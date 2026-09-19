# Astra automation handoff — run 128

Problem 1 remains OPEN.

Starting branch tip: `8023bc2b1be22f8bfe9a149654ef17d2bf51a607` (`research/astra-next`). No intervening work was found after run127.

## New result

Run127 left state-dependent routed provenance as a surviving birth-budget route. The Boolean-sensitive 1-provenance version now has an exact classification.

For Rule 30, `D_l f=1`, `D_c f=1 XOR r`, and `D_r f=1 XOR c`. Among the four neighborhoods producing output 1 (`001,010,011,100`), `001` has a sensitive right 1-parent, `010` a sensitive center 1-parent, and `100` a sensitive left 1-parent. Exactly `011` has no sensitive 1-parent: both 1 inputs are insensitive and the sensitive left input is 0.

Hence a state-dependent backward path constrained to sensitive 1s continues through every output-1 motif except `011`, where it terminates. This sharpens the earlier no-unique-parent result: adaptive routing repairs all cases except one exact nonlinear creation motif.

A direct exact Rule-30 simulation from a single initial seed counted 5321 `011` creation events over times 0..199, including 3931 over times 100..199. Thus generic `011` events cannot plausibly be treated as a scarce finite-support resource; a proof would need special structure of the forced cyclic-birth family.

Recorded in `proofs/informal/problem1_sensitive_one_provenance_breaks_exactly_at_011.md`, commit `004da48584adb2074c7d599dc60112d222dddcbe`.

## Next target

Apply sensitive-1 routing specifically to the proved two-bit nonreset `001` forcing passage. Determine whether the forced later `beta=1` cell's backward sensitive-1 route structurally avoids `011` (which would connect it to an original actual 1) or necessarily terminates at a source-relative `011`. In the latter case, isolate that special `011` family and test it for ordered/bounded reuse. Do not retry generic cone intersection, the unconditional left-sensitive ray, or generic `011` counting as a finite resource.
