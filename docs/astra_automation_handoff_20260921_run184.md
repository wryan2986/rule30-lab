# Astra automation handoff — run 184 — 2026-09-21

Problem 1 remains OPEN.

## Important correction to run 183

Run 183 correctly proved `d_1(t+8)=1`, but its inference

    J(t+8)<=t+9  =>  s_(t+8)<=t+8

was backwards. Do NOT reuse the resulting claim `Delta_(t+7) in {0,1}`.

## New exact result

Continue the beta=1 terminal branch. Run 181 gives at `t+6`

    r_(-1)=hat r_(-1)=1,
    r_0=x, hat r_0=1 XOR x,
    actual (r_1,r_2)=(0,1),
    shadow (hat r_1,hat r_2)=(1,1).

One Rule-30 step therefore fixes the previously omitted center cells at `t+7`:

    actual (r_0,r_1)=(1 XOR x,1 XOR x),
    shadow (hat r_0,hat r_1)=(0,x).

Because `m(t+7)=1`, `d_(-1)(t+7)=0`. The discrepancy update at the center gives

    d_0(t+8)
      = 0 XOR [(1 XOR x) XOR x]
      = 1.

Negative positions remain agreeing, hence

    m(t+8)=0,
    J(t+8)=t+8.

Together with run 181's

    J(t+7)=t+8,
    s_(t+7)=t+7,

this says characteristic `t+8` resides for at least the two physical rows `t+7,t+8`. Thus

    s_(t+8)>=t+9,
    Delta_(t+7)>=2,
    tau(Y_(t+8))>=1,
    R_(t+7)>=1.

So in the beta=1 branch the first time not excluded by the eight-step nonresetting-source spacing theorem is forced to be a positive-delay center crossing of the same global characteristic.

## Fence

This does NOT prove that `t+8` is a new nonresetting source. Core type at `Y_(t+8)` is still unresolved. No cyclic-source birth law is valid unless cyclicity is independently established.

## Next target

Classify the complete actual core at `t+8` under the forced positive delay. Determine whether it can still be resetting, whether it must be nonresetting, or whether another complete-driver bit controls the branch. The scalar front/delay part is now fixed enough that further work should focus on core type rather than on `d_0(t+8)`.

New proof file:
`proofs/informal/problem1_run184_beta_one_forces_tplus8_center_crossing.md`
