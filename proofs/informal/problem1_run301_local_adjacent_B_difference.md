# Problem 1 run 301: local adjacent difference of the corrected half-period summand

## Status

Problem 1 remains open. This continues runs 299--300.  The branch entered at
`e5dac980b3dedd0309bb0006bfc7b92f6b58daee`.

Run 300 reduced the current analytic target to
[
D_{t+1}+D_t=1+x_5(t)(1+p_t),
qquad
D_t=B_t+B_{t+4}+B_{t+8}+B_{t+12}.
]
The remaining problem was to derive the adjacent difference structurally rather
than by expanding the large ANFs of (D_t).

This note performs the first useful analytic compression: it gives a compact
one-step formula for the corrected (B_t) itself.  In particular, the moving
window (c_t) can be handled without any 16-step orbit expansion.

## Definitions

Use the corrected run-274 quantities
[
B_t=c_t g_t+eta_t u_t,
]
[
g_t=x_8(t)lor x_7(t),qquad
u_t=1+x_8(t)+d_t x_7(t),
]
[
eta_t=1+alpha_t+c_t,qquad
d_t=x_8(t+16)+x_8(t).
]

For one phase write
[
a=alpha_t, c=c_t, d=d_t, v=x_8(t), z=x_7(t),
 y=x_6(t), w=x_5(t).
]

The exact one-step recurrences needed are
[
a'=a+1+v,qquad c'=c+d,qquad d'=d+1+y,
]
[
z'=z+(ylor w),qquad v'=v+(zlor y).
]
These are just the definitions plus the triangular Rule-30 recurrence.

## Exact local difference

Substitute those recurrences into
[
B_{t+1}+B_t
=
c'g'+cg+eta'u'+eta u.
]
A direct Boolean-ring simplification gives

[
oxed{
egin{aligned}
B_{t+1}+B_t
={}&1+d+v+dz\
&+(ylor w)
igl[
a+d+v+ad+cd+cv+cz+dz
igr].
end{aligned}}
]

Equivalently, with
[
K_t=
alpha_t+d_t+x_8(t)
+alpha_t d_t
+c_t d_t+c_t x_8(t)+c_t x_7(t)
+d_t x_7(t),
]
one has the compact identity
[
oxed{
Delta B_t
=
1+d_t+x_8(t)+d_t x_7(t)
+
igl(x_6(t)lor x_5(t)igr)K_t.
}
]

This is a formal Boolean identity, not a finite-state inference.

### Reproducibility

Expanding the right side in the seven formal Boolean variables
[
(a,c,d,v,z,y,w)
]
gives 28 monomials.  The terms independent of (y,w) are exactly
[
1+d+v+dz,
]
and the coefficients of (y), (w), and (yw) are all the same polynomial
[
K=a+d+v+ad+cd+cv+cz+dz.
]
That equality of all three coefficients is what factors the entire
coordinate-5/6 dependence into the single OR gate (ylor w).

## Consequence for the run-300 target

Because
[
D_t=B_t+B_{t+4}+B_{t+8}+B_{t+12},
]
the desired adjacent coboundary is now exactly
[
oxed{
D_{t+1}+D_t
=
Delta B_t+Delta B_{t+4}
+Delta B_{t+8}+Delta B_{t+12}.
}
]

Thus the analytic problem no longer requires comparing the corrected
quarter-pair expressions from run 274.  It is enough to sum four copies of the
boxed *local* formula at spacing four.

This is useful because all of its nonlocal information is confined to the
three scalar cocycles (alpha_t,c_t,d_t).  Their differences are already
known:
[
alpha_{t+1}+alpha_t=1+x_8(t),qquad
c_{t+1}+c_t=d_t,qquad
d_{t+1}+d_t=1+x_6(t),
]
while runs 265--274 provide their 4/8-shift transport indirectly through the
lower-coordinate period-doubling hierarchy.

The target becomes
[
igoplus_{jin{0,4,8,12}}
left[
1+d_{t+j}+x_8(t+j)+d_{t+j}x_7(t+j)
+(x_6(t+j)lor x_5(t+j))K_{t+j}
ight]
=
1+x_5(t)(1+p_t).
]

The four constant (1)'s cancel immediately.  The next calculation should
pair the (j=0,8) and (j=4,12) terms using
[
d_{t+8}+d_t=p_t,qquad
c_{t+8}+c_t=x_3(t),
]
and the (e_t,f_t) skew recurrences.  This is smaller than expanding either
(D_t): the common 30-monomial high-coordinate invariant from run 299 never
appears.

## Blocker

The four-shift sum of the local formula has not yet been reduced analytically
to (1+x_5(t)(1+p_t)).  The remaining obstruction is now specifically the
8-shift pairing of the factor
[
(x_6lor x_5)K,
]
not the moving-window correction itself and not the large ANF of (D_t).
