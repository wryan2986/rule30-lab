# Astra automation handoff — 2026-09-15 run 34

Branch: `research/astra-next`

## Repository state reviewed

Run started from `9a57a87ca8af1d17c486049f16bdd9918317d245` (run 33 handoff). No newer work was present on the branch.

Problem 1 remains open.

Run 33 showed that a repaired long corridor has a forced next-step recollision with defect 1 for original odd `G` and defect 3 for original even `G`.

## New exact result

Added `proofs/informal/problem1_second_same_period_repair_endpoint_classification.md`.

The second same-period repair from that forced recollision is again completely decided by bounded endpoint data of the transported fringe `R'`.

For original odd long `G`, `R'` is odd and the forced recollision has defect 1:

- if `G'=1`, second repair occurs iff `R' mod 4 = 1` for even `p`, or `3` for odd `p`;
- if `G'=0`, the same low-bit condition is required and the leading four bits of `R'` must be `1000` or `1001`.

For original even long `G`, `R'` is even, `G'=0`, and the forced recollision has defect 3. Second repair occurs iff:

- the leading four bits of `R'` lie in `1000,1001,1010,1011,1100`; and
- `R' mod 8 = 2` for even `p`, or `6` for odd `p`.

So transported-fringe provenance does not forbid a second repair.

## Important counterexample / dead end

Added `scripts/check_second_same_period_repair.py` and ran the exact p=4/p=8 finite-extension census.

At exact period 8, second repair after a repaired long corridor is common:

- original `G=3`: 25 second repairs, 22 failures;
- original `G=4`: 5 second repairs, 2 failures;
- original `G=5`: 7 second repairs, 2 failures.

A particularly useful witness is

`z = 32510615916414451519835451338196251`, `G=3`, `R=7707`.

After the first repair it reaches

`z' = 2313743162027786261944999351769153349`.

From `z'`, the physical orbit alternates fixed/collision for 13 consecutive `A^8`-fixed nodes (25 physical transitions) before leaving that repair train.

Therefore a tiny universal bound on same-period repair-chain length is false. This closes the specific run-33 hope that the second repair might simply be impossible or that one or two local steps would terminate every same-period repair train.

## Next target

Study the two-step map on successfully repaired short-gap states:

`z' -> T^2(z')`.

Derive the exact return-fringe transport and endpoint-class transition under repeated successful repairs. Search for a monotone quantity or a bound depending on `p` / fringe width. The p=8 witness shows any useful bound must allow at least 13 fixed nodes. Alternatively connect each successful two-step repair directly to the common-origin/FULL birth accounting.

Commits this run:

- `cc4ba9a0f34d6e336dd9cdbf7d483b650bb17462` — theorem + counterexample note
- `2dee8575c903c454b2f9201f371a87f52fdef3a9` — exact census checker
