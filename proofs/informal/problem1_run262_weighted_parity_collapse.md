# Problem 1 run 262 — the final weighted parity collapses on x0=1, x1=x2

Problem 1 remains open. This continues runs 260–261.

Recall the lower-orbit quantities

[
g_s=x_8(s)lor x_7(s),quad
P_s=igoplus_{j<s}g_j,quad
a=igoplus_{s<32}P_s(1oplus x_8(s)),
]
[
A_s=igoplus_{j<s}(1oplus x_8(j)),
]
and
[
W=igoplus_{substack{0le s<30\smod4in{0,1}}}
(1oplus aoplus A_s)g_s.
]

Run 261 proved that the b=1 branch forces
[
x_0=1,qquad x_1=x_2,qquad x_5=x_1(x_3lor x_4).
]

## New exact simplification

Impose only the first two conditions
[
x_0=1,qquad x_1=x_2,
]
leaving (x_1,x_3,x_4,x_5,x_6,x_7,x_8) free.

I evaluated the exact 32-step triangular Rule-30 recurrence on all (2^7=128) states of this restricted Boolean cube and took the Möbius transform of the resulting truth table for W. Its ANF has only three monomials:

[
oxed{W=1oplus x_5oplus x_1x_5
      =1oplus x_5(1oplus x_1).}
]

In particular W is independent of (x_3,x_4,x_6,x_7,x_8) once (x_0=1,x_1=x_2).

This makes the run-260 implication immediate from the run-261 branch factorization. If b=1, then (x_0=1,x_1=x_2). There are two cases.

* If (x_1=x_2=1), then (1oplus x_1=0), hence (W=1), with no condition on (x_5) needed.
* If (x_1=x_2=0), run 261 gives (x_5=0), hence again (W=1).

Therefore
[
oxed{b=1Longrightarrow W=1.}
]

This is strictly sharper than run 260's nine-variable certificate: after the two low-coordinate constraints are imposed, the final 32-step weighted parity forgets five of the seven remaining free bits and reduces to a two-bit expression.

## What remains

This still uses a finite Boolean/Möbius certificate to obtain the three-term formula for W. The next structural target is therefore much smaller than before: derive
[
W=1oplus x_5(1oplus x_1)
]
analytically under (x_0=1,x_1=x_2), preferably by grouping the 32-step orbit into four-step blocks. No x3,x4,x6,x7,x8 dependence should survive.

Once that identity is proved from the recurrence rather than by finite reduction, the b=1 parity implication needed for the triple-64 transport is analytic rather than computational.
