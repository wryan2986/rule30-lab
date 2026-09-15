# Astra automation handoff — 2026-09-15 run 36

Branch: `research/astra-next`

## Repository state reviewed

Run started from `380b3c7f6473c23a4f9a5c8f1a1efb09c9942769` (run 35 handoff). No newer work was present on the branch.

Problem 1 remains open.

Run 35 reduced an alternating same-period repair train to a nonrepeating segment of `F_p(R)=T^2(R) mod 2^(2p)` and bounded its fixed nodes by `3*4^(p-1)`.

## New exact computation

Added `scripts/check_repair_train_maxima.py` and `proofs/informal/problem1_repair_train_exact_census_p8.md`.

The finite-extension graph was used to enumerate every genuine finite `A^p`-fixed word for `p<=8` and measure exact alternating fixed/collision/fixed train lengths.

Exact-period state counts and maximum train lengths are:

- p=1: 3 states, max 1
- p=2: 10 states, max 1
- p=3: 0 states
- p=4: 84 states, max 3
- p=5: 0 states
- p=6: 0 exact-period-6 states
- p=7: 0 states
- p=8: 2968 states, max 15

Thus the exact maxima at nontrivial power-of-two periods are `M_2=1, M_4=3, M_8=15`, fitting `M_p=2^(p/2)-1` for p=2,4,8. This is only a conjectural pattern, not a theorem.

Run 34's 13-node p=8 witness was not maximal. There are exactly two 15-node maximizers. One starts at

`z=36088633440115177043812706397341401`

and has fourteen consecutive G=1 fixed nodes followed by one G=0 node. The other starts at

`z=16255307958207225759917725669098125`.

## Potentially stronger clue

The exact finite-extension period spectra through p=8 are:

- Fix(A): periods {1}
- Fix(A^2): {1,2}
- Fix(A^3): {1}
- Fix(A^4): {1,2,4}
- Fix(A^5): {1}
- Fix(A^6): {1,2}
- Fix(A^7): {1}
- Fix(A^8): {1,2,4,8}

Counts for exact periods 1,2,4,8 are respectively 3,10,84,2968.

No finite exact period 3,5,6,7 occurs. Through this range every nontrivial finite A-cycle period is a power of two. This is computational evidence only, but a theorem of this form would directly constrain the period-change escape mechanism that remains in the global FULL/common-origin argument.

## Next target

Prioritize proving or disproving: every finite periodic point of A has exact period a power of two. In parallel, analyze why the G=1 restriction of `F_p` gives maxima 1,3,15 at p=2,4,8. A naive p=16 extension graph has 2^32 low states and is not practical; any p=16 census needs a transfer/implicit-state method.

Commits this run before handoff: `1a77df7b9db289ae5541b12010257bb4b193625f`, `458bcddf5b79c2ac96c64838ba25313c0a6b30ed`.
