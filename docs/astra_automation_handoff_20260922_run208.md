# Astra automation handoff — 2026-09-22 run 208

Problem 1 remains OPEN.

Continue only the corrected run-193--208 chain.

## New exact result

Run 207's one-bit defect automaton gives an exact formula for every positive adjacent shift-tower tau increment.

For q fixed, let a=tau(q), P its eventual period, and let d_a be the defect bit in

    A^k(2q)=2 A^k(q) XOR d_k.

If the eventual q-cycle has no low-bit-1 symbol (no 10/11 reset), then

    tau(2q) <= a.

If it has a reset, there is a unique periodic defect phase d*. If d_a matches that phase, again

    tau(2q) <= a.

If d_a mismatches it, let rho be the forward distance from cycle entry to the first reset transition. Identity/toggle maps preserve the mismatch until that reset; the reset kills it exactly. Therefore

    tau(2q) = a + rho,

with 1 <= rho <= P.

Proof note:

    proofs/informal/problem1_run208_exact_tau_doubling_reset_formula.md

## Shift-tower form

For q_n=2^n x and a_n=tau(q_n), every positive increment is exactly

    a_n-a_(n-1)=rho_n,

where rho_n is the first-reset distance on the lower eventual cycle and the entry defect phase is mismatched.

Thus the true renewal condition becomes

    a_(n-1)+rho_n > b+n

in the mismatch case.

## Dead end found

Do NOT try to prove that reset mismatches / above-diagonal renewals are eventually absent for arbitrary fixed finite x using only this automaton. Exact bounded computation for x=1 through n=119 shows many indices with

    a_n > max(a_(n-1), n),

including many late in the tested range. This is not an infinitude proof, but it strongly refutes the intended proof strategy as a generic shift-tower statement.

## Next target

Find structure supplied specifically by the FULL/global-front hypothesis that constrains the sequence of cycle-entry phases or first-reset distances rho_n. The adjacent-tower automaton alone is too permissive. Compare the exact rho_n formula against the repository's global-front residence/renewal identities and complete cyclic code. Avoid absolute diagonal bounds, width arguments, mechanical local propagation, and generic mismatch-finiteness claims.