# Astra automation handoff — 2026-09-22 run 201

Problem 1 remains OPEN.

## New result

Continue only the corrected run-193--201 chain.

Comparing run 200 with the established global-front residence law shows that the low complete-driver bits exposed in runs 197--200 are exactly the shared-left-neighbor eraser trace of characteristic `t+8`, not a new independent finite resource.

Run 196 has `J(t+8)=t+8`. Run 197 has

    r_-1(t+8)=1 xor p.

Hence `p=0` gives the final erasing 1 at `(-1,t+8)` and exactly

    s_(t+8)=t+9.

For `p=1`, that shared-left-neighbor is 0 and the residence continues. On this branch run 199 gives

    r_-2(t+9)=w3.

Since `J(t+9)=t+8`, this is the next shared-left-neighbor cell. Therefore `w3=1` is exactly the final eraser at `(-2,t+9)`, giving

    s_(t+8)=t+10,

while `w3=0` is another nonfinal zero and

    s_(t+8)>=t+11.

So characteristic `t+8` has residence length exactly 1 for `p=0`, exactly 2 for `p=1,w3=1`, and at least 3 for `p=1,w3=0`. This also corrects the mild understatement in run 200: the `p=1,w3=0` branch persists on rows `t+8,t+9,t+10`, not merely two rows.

The important negative result is that "successive driver bits are consumed, therefore finite support bounds returns" is not a valid charge. These bits simply re-encode the already-known residence eraser word. Distinct spacetime erasers still need an injective/bounded-reuse ancestry map to finite original support; the global-front path identity permits overlapping ancestry and cancellation.

Do not propagate another local row merely to expose the next driver bit: absent a new ancestry restriction, that will reproduce the same residence law. Target the missing bounded-reuse/global-support lemma directly.

Proof note: `proofs/informal/problem1_run201_driver_bits_are_residence_erasers.md`.