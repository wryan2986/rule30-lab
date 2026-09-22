# Astra automation handoff — 2026-09-21 run 198

Problem 1 remains OPEN.

## New result

Continue only the corrected run-193--198 chain. Run 197 left

    p := r_-5(t+4) = bit_1(A^4 z)

as the unique branch bit for the corrected `t+9` front.

Auditing the retained definition of the nonresetting core shows that its identically-zero low A-trace does **not** force `p=0`.

Put `w=A^4 z`. The trace gives `w[0]=0` and `(Aw)[0]=0`. Using the established A rule

    (A Q)[0] = Q[2] xor (Q[1] or Q[0])

gives

    w[2]=w[1]=p.

Hence the low prefix of `A^4 z` is exactly

    (0,p,p),

so the two scalar-trace-compatible prefixes are `000` and `011`.

This is a precise obstruction, not an existence claim for both FULL branches. Eliminating either value of `p` requires complete cyclic code/phase information, FULL constraints, or a global threshold/front identity beyond `N_t`.

## Next target

Retain both corrected run-197 branches. Either:

1. inspect the complete code relation `Theta(G(z)) = I_3 I_1 shift^4 Theta(z)` for a constraint distinguishing the `000` and `011` low prefixes of `A^4 z`; or
2. if no such phase constraint exists, propagate both branches to `t+10`, keeping the next required complete-driver bit symbolic.

Do not infer `p=0` from zero low A-trace and do not reuse run-184--192 trajectory claims.

Proof/obstruction note: `proofs/informal/problem1_run198_p_is_not_fixed_by_low_trace.md`.
