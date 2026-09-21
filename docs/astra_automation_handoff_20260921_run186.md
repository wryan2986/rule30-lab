# Astra automation handoff — run 186 — 2026-09-21

Problem 1 remains OPEN.

## New exact reduction

Continue the beta=1 branch from runs 180-185. At t+6 the actual right pair is `(r1,r2)=(0,1)`. Let `x=r0(t+6)` and

    omega := r3(t+6) OR r4(t+6).

Run 185's t+8 control bit `alpha` satisfies the exact Rule-30 identity

    alpha = x XOR omega.

Proof: `p=r3(t+7)=r2(t+6) XOR (r3 OR r4)=1 XOR omega`, while run 185 defines `alpha=(1 XOR x) XOR p`.

Therefore, conditional on `N_(t+8)`:

- `x != omega`: gate u, delay 1, `Delta_(t+7)=2`;
- `x = omega`: gate t, delay 2, `Delta_(t+7)=3`.

## Important obstruction

Determining only the terminal center bit `x` is not enough. The first recurrence also retains one Boolean of wider complete-driver information, `omega`. The resetting label at t+6 does not presently fix it, and neither the nonresetting-core theorem nor cyclic-source birth law applies at that noncyclic resetting endpoint.

## Next target

Start from the same complete cyclic driver already retained at t+4,

    Y_(t+4)=G(z)=16 A^4 z+7,

and transport the forced beta=1 birth far enough to express

    x XOR (r3(t+6) OR r4(t+6))

in terms of `z` or the already-defined original-shadow cells. Do not replace the wider cells by independent fringe choices. The useful outcome is either a simplification deciding alpha, or an exact identification of the first deeper driver symbol that remains.

Primary new note: `proofs/informal/problem1_run186_alpha_reduces_to_terminal_center_and_right_or.md`.
