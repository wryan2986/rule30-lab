# Problem 1 run 271: reconstruct the missing quarter-pair algebra

## Status

Problem 1 remains open. The branch entered at `453a74f85b2b8f37051032dc770c20665073d54e`.
The committed chain has no run-264 note: run 263 is followed directly by run 265, although run 265 refers to a run-264 quarter-pair functional. This note reconstructs the exact algebra needed for that missing step.

Work on
[
x_0=1,qquad x_1=x_2=:p_t.
]

Run 263 writes the selected half-period summand at phase (t) as
[
B_t=c,g_t+eta_t u_t
]
(over the Boolean ring, so (+) is XOR), where
[
g_t=x_8(t)lor x_7(t),qquad
eta_t=1+alpha_t+c,qquad
u_t=1+x_8(t)+d_t x_7(t),
]
and
[
d_t=x_8(t+16)+x_8(t).
]

For the 8-shift put, as in run 265,
[
e_t=x_7(t+8)+x_7(t),qquad
f_t=x_8(t+8)+x_8(t),
]
and define the 8-step alpha increment
[
m_t:=alpha_{t+8}+alpha_t
    =igoplus_{j=t}^{t+7}(1+x_8(j))
    =igoplus_{j=t}^{t+7}x_8(j).
]

Write temporarily
[
v=x_8(t), z=x_7(t), d=d_t, e=e_t, f=f_t, m=m_t,
quad d^+=d_{t+8},quad eta=eta_t.
]
Then
[
v^+=v+f,qquad z^+=z+e,qquad eta^+=eta+m.
]

Direct Boolean-ring expansion of (B_t+B_{t+8}), with no orbit ANF expansion, gives the exact quarter-pair formula
[
oxed{egin{aligned}
B_t+B_{t+8}={}&
 eta dz+eta d^+e+eta d^+z+eta f\
&+c(ef+ev+e+fz+f)\
&+m(d^+e+d^+z+f+v+1).
end{aligned}}
]
This is the missing selector-preserving algebraic skeleton between runs 263 and 265. It isolates all dependence on the 8-shift skews (e,f), the 16-shift skew (d), and the scalar 8-step alpha increment (m), without expanding coordinates 7 or 8.

## Additional 8-shift law for the 16-skew

Run 263 proved
[
d_{t+1}+d_t=1+x_6(t).
]
Therefore
[
d_{t+8}+d_t=igoplus_{j=0}^{7}x_6(t+j).
]
Exact propagation on the restricted branch gives
[
oxed{igoplus_{j=0}^{7}x_6(t+j)=p_t,}
]
hence
[
oxed{d_{t+8}=d_t+p_t.}
]
The parity identity was independently checked on all 128 restricted initial states and all phases through the lower 16-step period. At phase zero its Möbius transform consists of the single monomial (p).

Substituting (d^+=d+p_t) into the boxed quarter-pair formula removes one independent skew variable. The remaining task is to sum it only over the four selected phases (tin{0,1,4,5}), then use the run-265--270 cocycles and selector laws before expanding anything high-coordinate.

## Dead end avoided

The run-270 residual word (R_t=(p_t+x_4(t))(1+x_5(t))) is useful only after this quarter-pair expression has been assembled. The missing non-(e_tq_t) terms cannot be reconstructed from (R_t) alone; this formula restores their source.

## Next target

Insert (d^+=d+p_t), sum over (t=0,1,4,5), and group the resulting terms by (eta,c,m). Use
[
e_{t+1}+e_t=1+x_5(t),qquad
f_{t+1}+f_t=1+x_7(t)+e_tx_6(t)
]
together with the run-267 collapse and run-270 selector split. The goal remains the analytic identity
[
W=1+x_5(0)(1+p_0).
]
