# Astra automation handoff — 2026-09-22 run 200

Problem 1 remains OPEN.

## New result

Continue only the corrected run-193--200 chain.

Run 199 left `p=1,w3=1` unresolved at `t+10`. It is now exact.

For `p=1`, the complete-driver/light-cone block at `t+4` forces

    r_-2(t+8)=0.

Together with run 197's `r_-1(t+8)=0` and `r_0(t+8)=0`, this gives

    r_-1(t+9)=0.

In the remaining `w3=1` branch, run 199 has common `r_-2(t+9)=1`, while run 197 has `d_-1(t+9)=d_0(t+9)=1`. Thus the actual local triple at `(-2,-1,0)` is `100` and the shadow triple is `111`, so Rule 30 gives

    d_-1(t+10)=1.

Since run 199 already gives `d_-2(t+10)=0` for `w3=1`, the exact front is

    p=1,w3=1 => m(t+10)=-1, J(t+10)=t+9.

Complete corrected classification:

    p=0:
      J(t+9)=t+9, J(t+10)=t+9.

    p=1,w3=0:
      J(t+9)=t+8, J(t+10)=t+8.

    p=1,w3=1:
      J(t+9)=t+8, J(t+10)=t+9.

So all branches through `t+10` are now closed. Successive residence decisions are selected by successive low bits of the same complete driver `w=A^4z`, not arbitrary local cells.

## Next target

Do not merely propagate another row unless it exposes a genuinely new invariant. Compare the three now-complete residence patterns against the established original-cut threshold/residence identities and the finite-entry/birth-budget machinery. Try to formulate a charge from a residence/persistence event to a distinct low driver bit or original-support event. The unresolved global step remains proving that repeated nonresetting returns cannot consume such driver-controlled persistence indefinitely with finite initial support.

Do not reuse run-184--192 trajectory claims.

Proof note: `proofs/informal/problem1_run200_complete_tplus10_front_classification.md`.