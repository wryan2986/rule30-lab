# Problem 1 run 304: collapse the moving-window four-step transport

## Status

Problem 1 remains open. This continues run 303 at commit `af0d6e3f3802792c143a511481a6975ad003c620`.

Run 302 reduced the analytic target to
[
S_{t+4}+S_t=1+x_5(t)(1+p_t).
]
Run 303 removed the alpha-window skew (m) as an independent obstruction by the primitive hierarchy
[
Delta m=f,qquad Delta f=r,
]
where
[
r_t=1+x_7(t)+e_t x_6(t).
]

This note performs the analogous reduction for the moving 16-window variables (c_t,d_t).

## A second exact primitive hierarchy

From run 274,
[
c_{t+1}+c_t=d_t.
]
From run 263/301,
[
d_{t+1}+d_t=1+x_6(t).
]
Thus (c,d) form another exact two-level primitive tower:
[
oxed{Delta c=d,qquad Delta d=1+x_6.}
]

For four-step transport, summing the first differences and eliminating (d) gives
[
c_{t+4}+c_t=x_6(t)+x_6(t+2).
]
Define the coordinate-6 two-shift skew
[
j_t:=x_6(t+2)+x_6(t).
]
Then
[
oxed{c_{t+4}=c_t+j_t.}
]

Similarly,
[
d_{t+4}+d_t
=igoplus_{i=0}^{3}(1+x_6(t+i))
=igoplus_{i=0}^{3}x_6(t+i)
=j_t+j_{t+1},
]
so
[
oxed{d_{t+4}=d_t+j_t+j_{t+1}.}
]

Therefore neither (c) nor (d) requires an explicit four-step orbit ANF in the run-302 comparison.

## The new skew j is driven entirely by the existing two-shift layer

Run 268 already defines
[
k_t=x_4(t+2)+x_4(t),qquad
ell_t=x_5(t+2)+x_5(t),
]
with
[
k_{t+1}+k_t=1+x_2(t),
]
[
ell_{t+1}+ell_t=1+x_4(t)+k_t x_3(t).
]

The coordinate-6 forcing is (x_5lor x_4). Comparing that forcing at phases (t+2) and (t), and using
[
(a+ell)lor(b+k)+(alor b)
=ell(1+b)+k(1+a)+kell
]
in the Boolean ring, gives
[
oxed{
j_{t+1}+j_t
=
ell_t(1+x_4(t))
+k_t(1+x_5(t))
+k_tell_t.
}
]

Hence the complete four-step transport of the moving-window pair ((c,d)) is controlled by the already-established low-coordinate two-shift cocycles (k,ell), plus one new scalar (j) whose first difference is explicitly low-coordinate.

## Consequence for the run-302 target

The apparent high/nonlocal transport variables now split into two parallel primitive towers:

[
Delta m=f,qquad Delta f=r,
]
[
Delta c=d,qquad Delta d=1+x_6.
]

At displacement four, use
[
m_{t+4}=m_t+r_t+r_{t+2},
]
[
f_{t+4}=f_t+r_t+r_{t+1}+r_{t+2}+r_{t+3},
]
from run 303, together with the new formulas
[
c_{t+4}=c_t+j_t,
qquad
d_{t+4}=d_t+j_t+j_{t+1}.
]

This removes explicit four-step propagation of all four scalar window/skew variables (m,f,c,d). The only new object is (j), and its adjacent difference is already expressed through the run-268 (k,ell) layer.

The next analytic calculation should substitute these four transport identities directly into the compact run-302 formula for (S_{t+4}+S_t), group by (r_t,r_{t+1},r_{t+2},r_{t+3}) and (j_t,j_{t+1}), and only then apply the run-267/270 selector identities. Avoid expanding the common 25-monomial ANF core.

## Blocker

The final cancellation to
[
1+x_5(t)(1+p_t)
]
has not yet been derived symbolically. The remaining obstruction is now the interaction between the high driver (r_t=1+x_7+e_tx_6) and the low two-shift driver (j_t); (c,d,m,f) themselves no longer need independent four-step transport formulas.
