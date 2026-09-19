# Astra automation handoff — run 145 — 2026-09-19

Problem 1 remains OPEN.

## New result

Run 144 asked for the first inverse-center offset where the distinguished two-bit right driver `(a,b)=(r_3,r_4)` stops determining the forced left extension under FULL.

The first failure is exactly `r_-10(q)`.

Let `c=r_5(q)` and `d=r_6(q)`. Exact Rule-30 cone evaluation with the alternating FULL center trace gives

`r_-10(q) = (NOT a) AND (b OR c OR (NOT d))`.

So `(a,b)` suffices through `r_-9`, but not through `r_-10`.  In fact `(a,b,c)` is still insufficient; the minimal tested right prefix determining `r_-10` is `(r_3,r_4,r_5,r_6)`.

The only `a=0` driver pattern producing zero is `abcd=0001`; all other `a=0` patterns give one, while every `a=1` pattern gives zero.

Full derivation and exhaustive check: `proofs/informal/problem1_inverse_center_first_farther_driver_entry_at_minus10.md`.

## Next target

Measure the dependency frontier systematically: for each subsequent forced left bit `r_-n`, determine the largest/minimal right-driver prefix needed under the FULL center constraints.  Look for a characteristic delay, recurrence, or small transducer.  If the frontier simply expands at the generic cone rate, record that stopping fence rather than extending a table indefinitely, and return to the cyclic episode/gate quotient route.
