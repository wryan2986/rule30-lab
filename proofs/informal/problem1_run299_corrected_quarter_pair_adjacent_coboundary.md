# Problem 1 run 299: corrected quarter-pair collapses only after 4-shift pairing

## Status

Problem 1 remains open. This continues runs 274--275 on the restricted branch
[
x_0=1,qquad x_1=x_2=:p.
]

Run 275 showed that the moving-window repair block cannot be simplified by itself. This run recombines the repair with the original quarter-pair exactly as required and finds a much smaller cancellation target.

## Correct object

Let (B_t) be the corrected moving-window half-period summand from run 274:
[
B_t=c_tg_t+eta_tu_t,
]
with
[
c_t=igoplus_{j=t}^{t+15}x_8(j),quad
g_t=x_8(t)lor x_7(t),quad
eta_t=1+alpha_t+c_t,
]
[
u_t=1+x_8(t)+d_tx_7(t),qquad
d_t=x_8(t+16)+x_8(t).
]

The run-262 weighted parity is exactly
[
W=igoplus_{tin{0,1,4,5,8,9,12,13}}B_t.
]

Define the corrected quarter pair
[
Q_t:=B_t+B_{t+8}
]
and then pair four phases apart:
[
D_t:=Q_t+Q_{t+4}=B_t+B_{t+4}+B_{t+8}+B_{t+12}.
]
Then
[
W=D_0+D_1.
]

This is the object that run 275 said must be simplified as a whole; neither the old run-271 piece nor the run-274 repair is separated here.

## Exact exhaustive result

I propagated the triangular Rule-30 recurrence exactly on all (2^7=128) states
[
(p,x_3,x_4,x_5,x_6,x_7,x_8),
]
computed the defining run-262 scalar
[
a=igoplus_{s<32}P_s(1+x_8(s)),qquad
P_s=igoplus_{j<s}g_j,
]
then (alpha_t=a+igoplus_{j<t}(1+x_8(j))), and evaluated the corrected (B_t,Q_t,D_t).

The ANFs of (D_0) and (D_1) still contain high-coordinate dependence: they have 32 and 31 monomials respectively. But their symmetric difference is only the three masks
[
0, 8, 9
]
in variable order
[
(p,x_3,x_4,x_5,x_6,x_7,x_8).
]
Therefore
[
oxed{D_0+D_1=1+x_5+px_5=1+x_5(1+p).}
]

Equivalently, **every monomial involving (x_3,x_4,x_6,x_7,x_8) is identical in the two adjacent four-shift-paired expressions and cancels only in (D_0+D_1)**.

This independently reproduces the run-262 target using the repaired moving-window formula. It also explains why run 275's attempt to collapse the repair block alone necessarily failed: the high-coordinate cancellation is an adjacent-phase equality of the complete corrected (D_t), not a property of either component.

For reproducibility, the ANF masks are:

[
D_0: 0,1,2,4,7,9,12,18,19,20,21,28,29,31,32,33,36,37,38,39,40,41,42,44,45,46,49,51,58,64,72,73,
]

[
D_1: 1,2,4,7,8,12,18,19,20,21,28,29,31,32,33,36,37,38,39,40,41,42,44,45,46,49,51,58,64,72,73.
]

Their common 30-monomial part should not be expanded further in the analytic proof.

## New analytic target

The corrected proof no longer needs to simplify (D_0) or (D_1) individually. It is enough to prove directly
[
oxed{D_{t+1}+D_t=1+x_5(t)(1+p_t)}
]
at the needed phase (t=0) (or an appropriate transported version), using the low cocycles already established:
[
p_{t+1}=p_t+1,
]
[
c_{t+1}+c_t=d_t,qquad c_{t+8}+c_t=x_3(t),
]
[
d_{t+1}+d_t=1+x_6(t),qquad d_{t+8}+d_t=p_t,
]
together with the run-265--270 skew/selector laws.

The exhaustive result says the desired cancellation is specifically an **adjacent-phase coboundary after 4-shift pairing**. That is substantially narrower than attempting a direct simplification of the repaired quarter pair.

## Blocker

This is still a finite Boolean certificate, not the requested analytic derivation. The remaining task is to derive the adjacent-phase identity for the complete (D_t) without expanding the common 30-monomial high-coordinate part.

Do not retry separate simplification of the run-274 repair block. The cancellation locus is now identified: first form (Q_t=B_t+B_{t+8}), then (D_t=Q_t+Q_{t+4}), and only then compare (D_{t+1}) with (D_t).
