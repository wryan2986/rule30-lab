# Astra automation handoff — 2026-09-22 run 202

Problem 1 remains OPEN.

## New result

Continue only the corrected run-193--202 chain.

Run 201 closed the proposed independent driver-bit charge: those bits are exactly residence erasers. Run 202 gives a different exact reduction using the COMPLETE ORIGINAL FINITE RIGHT FRINGE.

Let `b` be the rightmost occupied site of the original finite row and `x=L_b`. Beyond the fringe,

    L_(b+n)=2^n x,
    s_(b+n)=tau(2^n x)=:a_n.

Hence characteristic `b+n` has exact residence length

    a_n-a_(n-1),

and the established renewal identity becomes

    R_(b+n-1)=max(a_n-max(a_(n-1),b+n),0).

Therefore any alleged FULL finite seed, which requires infinitely many positive late renewals, must satisfy

    tau(2^n x) > max(tau(2^(n-1)x), b+n)

for infinitely many `n`.

This isolates the missing global finite-fringe statement as a diagonal-growth problem for ONE zero-extension tower. The existing theorem `tau(2^n x)->infinity` is insufficient and explicitly did not control `tau(2^n x)-n`; run 202 shows that this fenced-off rate question is now exactly the relevant quantity.

Do not return to local driver-bit propagation or an injective eraser-to-support charge unless a genuinely new restriction appears. Target an all-depth theorem about `e_n=tau(2^n x)-n`: ideally prove that the inequality above occurs only finitely often for every finite `x`, or rigorously show why such a rate bound fails. Do not use numerical sampling as proof.

Proof note: `proofs/informal/problem1_run202_finite_fringe_shift_tower_reduction.md`.