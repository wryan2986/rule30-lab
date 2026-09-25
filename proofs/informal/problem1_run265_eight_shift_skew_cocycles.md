# Problem 1 run 265: structural 8-shift skew recurrences

## Status

Problem 1 remains open. This note continues runs 262--264.  The branch entered this run at `88e305bfb6f5744e256a641b2ea96da561673f2c`; no intervening pushed research was present.

Work on the restricted branch
[
x_0=1,qquad x_1=x_2=:p.
]
Run 264 observed the exact 8-step map
[
x_j(t+8)=x_j(t)quad(0le jle5),qquad x_6(t+8)=x_6(t)oplus1.
]

The purpose of this note is to avoid the large explicit ANFs for the coordinate-7 and coordinate-8 8-step skews.

## Define the 8-shift skews

Let
[
e_t:=x_7(t+8)oplus x_7(t),qquad
f_t:=x_8(t+8)oplus x_8(t).
]

Using the triangular Rule-30 recurrence
[
x_i(t+1)=x_i(t)oplusigl(x_{i-1}(t)lor x_{i-2}(t)igr),
]
the lower 8-step identities imply compact first-order recurrences for these skews.

### Coordinate 7

The forcing of (x_7) is (x_6lor x_5).  Under an 8-shift, (x_6) is complemented and (x_5) is unchanged.  For Boolean (a,b),
[
((aoplus1)lor b)oplus(alor b)=1oplus b.
]
Therefore
[
oxed{e_{t+1}=e_toplus1oplus x_5(t).}
]

This replaces the direct 11-monomial ANF for (e_t) by a one-dimensional cocycle driven only by (x_5).

### Coordinate 8

The forcing of (x_8) is (x_7lor x_6).  Under an 8-shift these become (x_7oplus e_t) and (x_6oplus1).  Direct Boolean-ring simplification gives
[
((aoplus e)lor(boplus1))oplus(alor b)
=1oplus aoplus eb.
]
Hence
[
oxed{f_{t+1}=f_toplus1oplus x_7(t)oplus e_t x_6(t).}
]

This replaces the direct 22-monomial ANF for the coordinate-8 8-step skew.

These two scalar recurrences are the natural 8-step analogue of run 263's 16-shift recurrence
[
d_{t+1}=d_toplus1oplus x_6(t).
]

## New exact parity consequence

Run 263 established
[
x_7(t+16)=x_7(t)oplus1.
]
Therefore, by the definition of (e_t),
[
e_{t+8}oplus e_t=1.
]
Iterating the boxed recurrence for (e) over eight steps gives
[
e_{t+8}oplus e_t
=igoplus_{j=0}^{7}(1oplus x_5(t+j))
=igoplus_{j=0}^{7}x_5(t+j),
]
because eight copies of 1 cancel.  Consequently
[
oxed{igoplus_{j=0}^{7}x_5(t+j)=1}
]
for every phase (t) on the restricted branch.

This was also independently checked by exact Boolean-ANF propagation: the XOR of the eight (x_5) polynomials is literally the constant polynomial 1.

Thus the complement of (x_7) after 16 steps is not an isolated high-coordinate phenomenon; it is exactly the odd 8-step temporal parity of coordinate 5.

## Why this is useful

Run 264 found that the remaining target
[
W=1oplus x_5(0)(1oplus p)
]
is an 8-step finite difference, but direct substitution was a dead end because the explicit (e_0) and (f_0) ANFs contain 11 and 22 monomials.

The boxed skew recurrences remove that expansion.  The remaining proof should express the selected-block difference in terms of (e_t,f_t), then telescope:
[
e_{t+1}oplus e_t=1oplus x_5(t),
]
[
f_{t+1}oplus f_t=1oplus x_7(t)oplus e_t x_6(t).
]
The already-proved odd parity of the 8-step (x_5) word should dispose of the constant/(e) boundary contribution.  The only genuinely nonlinear residual is (e_t x_6(t)).

## Next target

Rewrite the run-264 quarter-pair functional (H_1oplus H_0) directly using (e_t,f_t), before expanding any coordinate orbit.  Seek a 1-, 2-, or 4-step primitive whose finite difference reduces the nonlinear residual (e_t x_6(t)).  Do not return to the 11/22-monomial explicit skew ANFs unless needed only as a finite verification certificate.
