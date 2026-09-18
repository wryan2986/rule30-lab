# Astra automation handoff — run 124

Problem 1 remains OPEN.

Starting branch tip: `3cdbdc2b4c91ba49cff93503d1cb3b728849927f` (`research/astra-next`). No intervening work was found after run123.

## New result

Proved that the global Rule-30 map is injective on finite-support configurations. Because f(l,c,r)=l XOR(c OR r) is left-permutive, two finite rows with the same image can be reconstructed identically from their common zero right tail, descending right-to-left. Hence every later finite-support row uniquely determines the complete original finite row.

This rules out a tempting interpretation of the current birth-budget route: the forced resetting source after the established two-bit nonreset passage cannot literally erase/consume original-row information. The physical evolution remains globally injective through that reset. Any finite resource exhausted by reset episodes must therefore be a coarse episode-specific observable with its own proved one-way transition law, not information disappearance.

Recorded in `proofs/informal/problem1_resetting_cannot_be_global_information_consumption.md`, commit `a9d1e05740b3c4df9a82c01715743091c5d21127`.

## Next target

Look for an order or filtration on recoverable original-row information: a source-relative boundary/intercept/nested subset of the finite original support whose index advances monotonically across the exact resetting and nonresetting passages. Do not interpret resetting itself as information loss; injectivity disproves that shortcut.
