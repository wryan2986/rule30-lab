# Astra automation handoff — 2026-09-22 run 199

Problem 1 remains OPEN.

## New result

Continue only the corrected run-193--199 chain.

Run 198 left `p=bit_1(A^4 z)` genuinely undecided by the scalar zero low A-trace. Put `w=A^4 z`, so `(w0,w1,w2)=(0,p,p)`.

Propagating the actual complete driver `Y_(t+4)=16w+7` five physical rows gives a useful boundary classification at `t+10`.

For `p=0`, `r_-1(t+9)=0`. Since run 197 has `m(t+9)=0`, the Rule-30 boundary discrepancy necessarily spreads left:

    p=0 => m(t+10)=-1, J(t+10)=t+9.

Thus characteristic `t+9` has at least a two-row residence.

For `p=1`, the common cell immediately left of the `t+9` front is

    r_-2(t+9)=w3.

Hence

    d_-2(t+10)=1 xor w3.

In particular

    p=1,w3=0 => m(t+10)=-2, J(t+10)=t+8.

If `p=1,w3=1`, the front does not spread to `-2`; its exact `t+10` location remains to be computed.

The next zero-trace equation `(A^2w)[0]=0` gives

    p=0 => w4=0,
    p=1 => w4=w3.

So on the p=1 branch the scalar-trace-compatible low prefixes through bit4 are `01100` and `01111`.

## Next target

First finish the `p=1,w3=1` discrepancy update at `t+10` and determine whether the front remains on characteristic `t+8` or advances. Keep all required farther-right cells symbolic unless an established complete-driver/FULL identity fixes them.

Then compare the resulting residence pattern with the existing threshold/residence identities. The emerging useful structure is that successive front persistence decisions are being selected by successive low bits of the same complete cyclic driver; the unresolved global step is still to convert that dependence into a finite-support charge.

Do not reuse run-184--192 trajectory claims.

Proof note: `proofs/informal/problem1_run199_corrected_tplus10_front.md`.