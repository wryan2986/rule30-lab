# Astra automation handoff — run 147 (2026-09-19)

## Branch state reviewed

Started from run 146 commit `05b87a9fbbcfa6db327164ef4e34f830363afbf4`; no intervening research commits were present when this run began.

## New result

Proved an all-horizons left-permutivity theorem: for any finite desired center trace and **any arbitrarily fixed right half-row** (compatible at time zero), there is a unique successive choice of the needed finite left extension that realizes that center trace.

For Rule 30, `F(l,c,r)=l XOR (c OR r)`, so each new extreme-left source bit is uniquely solvable from the next desired center output after the previously nearer source cells are fixed.

Applied to FULL: every finite alternating center prefix is compatible with every choice of the untouched right driver tail. Thus the widening seen in runs 144--146 is structural, not a finite-depth accident. FULL continuation alone can never compress the unrestricted right driver to bounded width.

Proof file:
`proofs/informal/problem1_full_center_prefix_places_no_constraint_on_arbitrary_right_half.md`

Research commit creating the proof: `54b91798ecb6e3d5d7612633632598d14a120597`.

## Interpretation / stopping fence

Do not spend further runs extending the inverse-center dependency table under FULL alone. Run 146 already saw the extreme cone bit enter at depth 12; this theorem now explains the phenomenon for every horizon.

A successful finite-state argument must use constraints beyond the center trace: cyclic-source/gate/sensitive-return structure, finite support, or a quotient observable that deliberately forgets most of the state.

## Next target

Return to the question left open by run 146: does the **next return/birth observable** factor through a bounded quotient of the resetting source even though the full source state does not? Test this under all actual cyclic/gate admissibility constraints, not merely FULL compatibility. If two admissible configurations with the same candidate quotient yield different return/birth outcomes, record the minimal extra information required.

Problem 1 remains open.
