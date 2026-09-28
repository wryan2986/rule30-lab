# Problem 1 run 322: m/f residual and exact coboundary criterion

Problem 1 remains open.

For the residual from run 321, exhaustive restricted-state simplification gives

    Rm=(1+p)(1+x5)+p(x3 OR x4)(x5 OR x6).

It is nonzero on 68 of 128 restricted states, so Rm=0 is a dead end.

Let D=Delta4 N, where N=Q(1+c+x3). The remaining pre-r high part is

    Rm*m + D*f,

and f_t=m_(t+1)+m_t.

There is an exact one-step coboundary criterion. For any T,

    Delta1(T*m)=(T_(t+1)+T_t)m_t + T_(t+1) f_t.

Therefore Rm*m+D*f is exactly Delta1(T*m) with T_(t+1)=D_t iff

    BOX: Rm_t = D_t + D_(t-1).

This is the next finite low-coordinate test. It is sharper than separately collecting m_t and m_(t+1): only the adjacent skew of D must be compared with the compact Rm above.

Here

    D=Q*j_t+E(1+c+x3+j_t),

with E=Delta4 Q already closed in the low layer by run 313.

Thus the next target is the low-coordinate identity Delta1(D_(t-1))=Rm. No coordinate-7/8 expansion is required unless that identity fails and leaves a residual.
