# Problem 1 run 323: the m/f coboundary test fails, with a low residual

Problem 1 remains open. Continue from run 322.

Run 322 reduced the remaining pre-r high block to

    Rm_t m_t + D_t f_t,

where

    Rm=(1+p)(1+x5)+p(x3 OR x4)(x5 OR x6),
    D=Q*j_t+E(1+c+x3+j_t),

and f_t=m_(t+1)+m_t. It showed that this block is a one-step coboundary of the form Delta_1(T m) exactly if

    Rm_t = D_t + D_(t-1).

I evaluated this identity exactly on all 128 restricted initial states
(p,x3,x4,x5,x6,x7,x8), using the triangular Rule-30 recurrence and the
definitions of c,Q,j,E. It FAILS on 52 of 128 states. Thus the proposed
single T*m coboundary is a dead end.

More usefully, the residual

    F := Rm_t + D_t + D_(t-1)

again loses all x7 and x8 dependence. Its phase-zero ANF is the following
16-monomial polynomial:

    F =
      p + x3 + p*x3 + x4
      + p*x5 + x3*x5 + x4*x5 + x3*x4*x5
      + p*x6 + x3*x6 + p*x3*x6
      + p*x5*x6 + x3*x5*x6 + p*x3*x5*x6
      + p*x4*x5*x6 + p*x3*x4*x5*x6.

This ANF was obtained from the exact 128-state truth table by the Boolean
Mobius transform. F=1 on 52 states, matching the failed-identity count.

Consequences:

1. The failure of the simple m/f coboundary is not caused by unresolved
   coordinate-7/8 transport. Those coordinates cancel completely.
2. The remaining obstruction is confined to (p,x3,x4,x5,x6), i.e. the same
   low period-doubling layer already controlled by runs 266--268.
3. Do not spend another run trying to prove Rm=D_t+D_(t-1); it is false.

The next useful target is to reduce F using the two-shift cocycles from run
268,

    k_0 = 1+p+x3,
    ell_0 = p(1+x3+x4),

and the known four-step x5/x6 skews. In particular, search for a 1-, 2-, or
4-step low-coordinate primitive for F before returning to the r/u layer.
The obstruction has now been pushed completely below coordinate 7.
