# Astra automation handoff — run 148 (2026-09-19)

## Repository state reviewed

Previous research tip was run 147 at `5a2a0a9d30a84873871e0e852fc81700dd359381`. No intervening research commit was present before this run.

Problem 1 remains open.

## New result

Strengthened run 147's left-permutive stopping fence to finite-support witnesses.

For any horizon `T`, any desired center trace `c_0,...,c_T`, and any arbitrary prescribed initial right word `x_0,...,x_T` with `x_0=c_0`, Rule 30 admits a finite-support initial row realizing both. Set cells `>T` to zero; left permutivity then uniquely solves `x_-1,...,x_-T` successively for the requested center trace; set cells `<-T` to zero.

Applied to FULL: every finite right-driver prefix is compatible with every finite alternating FULL center prefix **even among finite-support initial rows**.

Full proof:
`proofs/informal/problem1_finite_support_realizes_arbitrary_finite_right_driver_and_center_trace.md`

Research commit creating the proof: `d75d6fd2ad69d801b67af78f700bb9ef810db637`.

## Why this matters

Finite support cannot be used as an extra finite-horizon local condition to make the right driver compress. At horizon `T`, all right-driver words through the relevant finite cone remain realizable. Thus any successful finite-state quotient must use genuinely additional cyclic/gate/sensitive-return conditions or an all-time consequence of eventual FULL.

This closes a possible loophole in run 147: its arbitrary-right-half witnesses were not necessarily finite-support, but the same obstruction already holds with finite-support witnesses at every finite horizon.

## Next target

Return to the cyclic episode/gate quotient. Test the return/birth observable under the **full cyclic/gate admissibility conditions**, not merely FULL compatibility or finite support. The useful question is whether those additional episode constraints identify a bounded quotient of the wider driver even though the underlying source state remains unrestricted at every finite FULL horizon.
