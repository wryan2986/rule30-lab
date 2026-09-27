# Problem 1 run 303: eliminate the alpha-window skew

Problem 1 remains open. This continues run 302 at commit 5875ed23928beb5a7f0a1d01128db33daafc4c7d.

Run 302 reduced the analytic target to the four-step comparison
[
S_{t+4}+S_t=1+x_5(t)(1+p_t),
]
where the compact eight-shift expression contains
[
m_t=alpha_{t+8}+alpha_t,qquad f_t=x_8(t+8)+x_8(t).
]

The apparent new skew m is not independent.

By the definition of the run-262 scalar alpha,
[
m_t=igoplus_{j=0}^{7}x_8(t+j).
]
Adjacent eight-windows differ only at their endpoints. Therefore
[
oxed{m_{t+1}+m_t=f_t.}
]

Run 265 already gives
[
f_{t+1}+f_t=r_t,qquad
r_t:=1+x_7(t)+e_t x_6(t),
]
with (e_t=x_7(t+8)+x_7(t)). Thus there is an exact two-level primitive hierarchy
[
oxed{Delta m=f,qquad Delta f=r.}
]

Two-step transport immediately collapses:
[
oxed{m_{t+2}+m_t=r_t
=1+x_7(t)+e_t x_6(t).}
]

For the four-step comparison needed in run 302,
[
m_{t+4}+m_t
=f_t+f_{t+1}+f_{t+2}+f_{t+3}
=r_t+r_{t+2},
]
so
[
oxed{
m_{t+4}+m_t
=x_7(t)+x_7(t+2)
+e_t x_6(t)+e_{t+2}x_6(t+2).
}
]

Likewise
[
oxed{
f_{t+4}+f_t
=r_t+r_{t+1}+r_{t+2}+r_{t+3}.
}
]

Hence the m- and f-parts of run 302's compact
[
L=m(1+d+p)+f(1+c+h)+cdots
]
are driven by the same scalar residual r. There is no separate alpha-window obstruction. Under four-step transport one may substitute
[
m^+=m+r_t+r_{t+2},
]
[
f^+=f+r_t+r_{t+1}+r_{t+2}+r_{t+3}.
]

This is useful because the only nonlinear high-coordinate term in r is exactly the (e_t x_6(t)) residual isolated in run 265. The next analytic step should substitute these formulas into (S_{t+4}+S_t), then use the run-268 two-shift layer on (r_t+r_{t+2}) before expanding any coordinate-7/8 orbit.

This removes m from the list of independent blockers; the remaining target is cancellation of the common r-driven four-step transport down to (1+x_5(t)(1+p_t)).
