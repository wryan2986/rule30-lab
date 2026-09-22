# Astra automation handoff — 2026-09-21 run 197

Problem 1 remains OPEN.

## New result

Continue only the corrected run-193--197 chain. Run 196 fixed `q=r_-4(t+4)=0` and hence `m(t+8)=0`, `J(t+8)=t+8`.

Let

`p := r_-5(t+4) = bit_1(A^4 z)`

from the complete driver `Y_(t+4)=16 A^4 z+7`.

Literal Rule-30 propagation gives

`r_-1(t+8)=1 xor p`.

Since actual/shadow agree left of position 0 at `t+8` and differ at position 0, the next discrepancy satisfies

`d_-1(t+9)=p`.

Independently, the corrected `t+7` seed forces actual `r_1(t+8)=0`, while `hat r_0(t+8)=1` erases any farther-right shadow dependence in the next center update. Therefore

`d_0(t+9)=1`

for both values of `p`.

Hence the corrected front is exactly

- `p=1 => m(t+9)=-1`, `J(t+9)=t+8`;
- `p=0 => m(t+9)=0`, `J(t+9)=t+9`.

Equivalently `m(t+9)=-r_-5(t+4)`.

No farther-right continuation affects this classification.

## Important constraint

Do not set `p=0` merely from the zero low A-trace. That trace directly fixes bit 0 of every `A^n z`; here `p` is bit 1 of `A^4 z`. It needs an additional operator/threshold identity if it is to be forced.

## Next target

Audit the retained definition/action of `A` and original-cut threshold identities for a relation between `bit_1(A^4 z)` and a later low-trace bit. If none exists, retain both corrected branches and propagate them to `t+10`; do not revive run-184--192 claims.

Proof: `proofs/informal/problem1_run197_corrected_tplus9_front.md`.
