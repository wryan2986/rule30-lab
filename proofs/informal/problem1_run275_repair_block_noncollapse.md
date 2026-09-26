# Problem 1 run 275: the moving-window repair block does not collapse alone

## Status

Problem 1 remains open. The branch entered at `c90a1ae762ec0983eda0e851e7b98cf94b85a47d`; no intervening work was present.

Run 274 repaired the false constant-16-window assumption by adding, for each quarter-pair phase,
[
K_t:=x_3(t)left[1+(x_7(t)+e_t)(1+x_8(t)+f_t+d_t+p_t)ight],
]
where
[
e_t=x_7(t+8)+x_7(t),quad
f_t=x_8(t+8)+x_8(t),quad
d_t=x_8(t+16)+x_8(t).
]

The immediate question was whether the selected repair
[
K_{m sel}=K_0+K_1+K_4+K_5
]
itself collapses to the low coordinates, so that it could be disposed of before returning to the run-271 quarter-pair expression.

## Exact exhaustive result

I evaluated the triangular Rule-30 recurrence
[
x_0'=x_0,quad x_1'=x_1+x_0,quad
x_j'=x_j+(x_{j-1}lor x_{j-2})quad(jge2)
]
on all (2^7=128) restricted initial states
[
x_0=1,qquad x_1=x_2=:p,
]
with free variables ordered
[
(p,x_3,x_4,x_5,x_6,x_7,x_8).
]

The selected correction does **not** collapse to a function of
((p,x_3,x_4,x_5)).  In fact each of (x_6,x_7,x_8) is essential.

Single-bit witnesses:

- (x_6): states ((1,0,0,0,0,0,0)) and ((1,0,0,0,1,0,0)) give (K_{m sel}=0,1).
- (x_7): states ((0,1,0,0,0,0,0)) and ((0,1,0,0,0,1,0)) give (K_{m sel}=0,1).
- (x_8): states ((0,1,0,0,0,0,0)) and ((0,1,0,0,0,0,1)) give (K_{m sel}=0,1).

The exact Möbius transform has 30 monomials (bit masks in the variable order above):
[
3,7,13,14,17,18,21,22,25,26,27,34,38,42,43,45,46,49,51,57,61,63,66,70,73,74,75,78,79,85.
]
This is recorded as a finite certificate/dead-end diagnostic, not as the desired proof.

Pairing four phases apart does not rescue the correction block in isolation: (K_0+K_4) has 28 ANF monomials and (K_1+K_5) has 36.

## Consequence

The new run-274 correction must **not** be simplified separately.  Its high-coordinate dependence is real and can disappear only by cancellation against the corresponding terms of the corrected run-271 quarter-pair expression.

This rules out the most obvious continuation suggested at the end of run 274: applying the run-267/run-270 low-coordinate selector identities to the repair block before recombining it with (Q_t^{(271)}).

The structurally correct next move is instead to combine
[
Q_t^{(271)}+K_t
]
at the summand level, substitute
[
d_{t+8}=d_t+p_t,qquad c_{t+8}=c_t+x_3(t),
]
and only then pair (t) with (t+4) (or (t+1)).  Any useful telescoping must cancel the (x_6,x_7,x_8) dependence across the old and repair pieces together.

## Blocker

The target remains
[
W=1+x_5(0)(1+p_0).
]
The immediate algebraic blocker is now precise: find a selector-preserving factorization of the **combined corrected quarter-pair summand**, not of the repair block or the run-267 residual separately.
