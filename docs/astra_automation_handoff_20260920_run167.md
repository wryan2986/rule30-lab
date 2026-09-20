# Astra automation handoff — run 167 — 2026-09-20

Problem 1 remains OPEN. Run165 excluded sufficiently late two-bit nonresetting sources. Run166 fenced the invalid shortcut of reading the one-bit cyclicization delay as an original-cut residence. This run obtains the first exact original-cut residence datum for the surviving one-bit gate-u source by a different argument.

## New result

For a sufficiently late one-bit gate-u nonresetting source at even time `t`, the established delay profile has

    tau(Y_t)=1,
    tau(Y_(t+1))=0,
    tau(Y_(t+2))=0.

Use the original-cut identity

    tau(Y_j)=max(s_j-j,0)

and monotonicity of `s_j`. The positive source delay gives `s_t=t+1`. The next zero delay gives `s_(t+1)<=t+1`, while monotonicity gives `s_(t+1)>=s_t=t+1`. Hence exactly

    s_(t+1)=s_t=t+1.

Therefore

    Delta_t=0,

so characteristic `t+1` is skipped by the global front. At physical time `t+1`,

    J(t+1)>=t+2,
    m(t+1)>=1.

The following zero-delay row gives only

    s_(t+2) in {t+1,t+2},

so

    Delta_(t+1) in {0,1}.

Thus the missing one-bit original-cut itinerary now starts with a forced skip and then has a binary branch: either a second skip or a one-step residence.

See `proofs/informal/problem1_run167_one_bit_source_forces_skipped_next_characteristic.md`.

## Next target

Use the SAME original global E-shadow and the complete one-bit source cells to distinguish `s_(t+2)=t+1` from `s_(t+2)=t+2`. Equivalently test whether the first discrepancy at physical time `t+1` can be at position 1 (`J=t+2`) or must lie farther right (`J>=t+3`). Do not infer this from the healed local `(x,z)` pair; it must come from the original global shadow / finite-cut ancestry.
