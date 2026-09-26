# Problem 1 run 274: repair the half-period pairing with the moving 16-window

## Status

Problem 1 remains open. The branch entered at `11cd16ffff4f08eef7beb2e22ef277c49f8da05a`.

This note corrects a defect in run 263 that propagates into run 271 as written. The run-262 32-step identity itself is unaffected.

Work throughout on
[
x_0=1,qquad x_1=x_2=:p_t.
]

## The 16-window is phase-dependent

Run 263 used the phase-zero scalar
[
c=igoplus_{j=0}^{15}x_8(j)
]
as though
[
alpha_{t+16}+alpha_t=c
]
held for every selected phase. The correct quantity is the moving window
[
c_t:=igoplus_{j=t}^{t+15}x_8(j),
qquad
alpha_{t+16}+alpha_t=c_t.
]

Adjacent windows obey the exact cocycle
[
oxed{c_{t+1}+c_t=d_t},
qquad
d_t=x_8(t+16)+x_8(t).
]

Thus the correct run-263 half-period summand is
[
B_t=c_tg_t+eta_tu_t,
]
where
[
eta_t=1+alpha_t+c_t,qquad
u_t=1+x_8(t)+d_tx_7(t).
]

## New exact 8-shift law for the moving window

Pairing the moving windows eight phases apart gives
[
c_{t+8}+c_t=igoplus_{j=0}^{7}d_{t+j}.
]
Using
[
d_{t+1}+d_t=1+x_6(t),
]
the eight copies of (d_t) cancel and the increments with odd multiplicity are exactly those at offsets (0,2,4,6). Hence
[
c_{t+8}+c_t
=x_6(t)+x_6(t+2)+x_6(t+4)+x_6(t+6).
]

Direct simplification of the lower triangular recurrence under (x_0=1,x_1=x_2) gives
[
oxed{x_6(t)+x_6(t+2)+x_6(t+4)+x_6(t+6)=x_3(t)}.
]
Therefore
[
oxed{c_{t+8}=c_t+x_3(t).}
]

The last identity was independently checked by direct Rule-30 propagation on all 128 restricted initial states and every phase (0le t<16).

This is a useful correction: the failure of constant (c) is not an uncontrolled high-coordinate effect. Its 8-shift is exactly the low coordinate (x_3(t)).

## Corrected quarter-pair formula

Retain the run-265 notation
[
e_t=x_7(t+8)+x_7(t),qquad
f_t=x_8(t+8)+x_8(t),
]
and
[
m_t=alpha_{t+8}+alpha_t.
]
Also use the run-271 identity
[
d_{t+8}=d_t+p_t.
]

Write temporarily
[
v=x_8(t), z=x_7(t), d=d_t, e=e_t, f=f_t, m=m_t,
quad d^+=d+p_t,quad c=c_t,quad eta=eta_t,
]
and put (h=x_3(t)). Then
[
v^+=v+f,quad z^+=z+e,quad c^+=c+h,quad
eta^+=eta+m+h.
]

If (Q_t^{(271)}) denotes the boxed run-271 quarter-pair expression, interpreted with (c=c_t), the only omitted contribution is the simultaneous (h)-change in (c^+) and (eta^+). Therefore
[
B_t+B_{t+8}
=
Q_t^{(271)}+h(g^++u^+).
]
Since
[
g^+=v^+lor z^+,qquad
u^+=1+v^++d^+z^+,
]
Boolean simplification gives
[
g^++u^+
=1+z^+(1+v^++d^+).
]
Consequently the exact repaired formula is
[
oxed{
B_t+B_{t+8}
=
Q_t^{(271)}
+x_3(t)left[
1+(x_7(t)+e_t)
left(1+x_8(t)+f_t+d_t+p_tight)
ight].
}
]

Equivalently, run 271 is missing one explicit correction block, and that block is controlled by (x_3), not by a new coordinate-8 quantity.

## Verification and consequence

The moving-window identity (c_{t+8}+c_t=x_3(t)) was checked on all 128 restricted states and all 16 lower phases. The repaired quarter-pair formula also follows as a formal Boolean-ring identity from the definitions above; no orbit ANF is needed for that step.

This explains why the constant-(c) reconstruction could look structurally close while still fail on selected phases. Runs 265--270 remain usable because their skew/cocycle statements do not require constant (c). Run 271 should only be used after adding the boxed correction term above.

## Next target

Sum the repaired quarter-pair over the actual four phases
[
tin{0,1,4,5}.
]
The new correction is already multiplied by (x_3(t)), and runs 267/270 provide selector identities that also collapse to (x_3) and (p). The next calculation should therefore combine the correction block with those selector laws before expanding any coordinate-7/8 ANF.

The target remains
[
W=1+x_5(0)(1+p_0).
]
