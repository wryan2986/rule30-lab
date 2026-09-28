# Problem 1 run 321: combined alpha/m four-step block

Problem 1 remains open. Continue from run 320.

This note carries out the next calculation proposed there. All sums are in the Boolean ring.

Write

    Q=qplus,
    A=1+d+p,
    M=Q A,
    C=(1+x5)(1+d)+pQ,
    s_t=alpha_(t+4)+alpha_t.

Run 320 certifies

    C_(t+4)=C_t

on every restricted state and gives

    Delta4(C alpha)=C s.

Also

    s_(t+4)+s_t=m_t.

Therefore the four-step difference of the surviving direct-alpha contribution is exactly

    BOX: Delta4(C s)=C m.

Now combine this with the m term already present in qplus*L. Its coefficient is M=Q(1+d+p). Run 304 gives

    m_(t+4)+m_t=r_t+r_(t+2).

For an arbitrary coefficient M,

    Delta4(Mm)
      =(Delta4 M)m + M_(t+4)(r_t+r_(t+2)).

Hence the complete combined alpha/m block obeys

    BOX:
    Delta4(C s + M m)
      =[C+Delta4 M] m
       +M_(t+4)(r_t+r_(t+2)).

Run 312 gives Delta4 A=j_t+j_(t+1), and run 313 gives E=Delta4 Q. The Boolean product rule therefore yields

    Delta4 M
      =Q_t [j_t+j_(t+1)]
       +E_t [A_t+j_t+j_(t+1)].

Thus the only possible surviving m coefficient after the alpha term is correctly combined with the pre-existing m term is the explicit low-layer scalar

    BOX:
    Rm_t
      = C_t
        +Q_t[j_t+j_(t+1)]
        +E_t[A_t+j_t+j_(t+1)],

where

    C=(1+x5)(1+d)+pQ,
    A=1+d+p,

and run 313 closes E without x7/x8:

    E=(j_t+j_(t+2))(1+x5)
      +x6 H+(j_t+j_(t+2))H,
    H=Delta4 x5=p(1+x3).

This is a sharper reduction than run 320. No alpha or s remains after one more four-step comparison of the combined block. The high part is now only

    Rm*m + M_(t+4)(r_t+r_(t+2)).

In particular, any proof that Rm=0 would make the whole alpha/m block descend directly to the r layer. If Rm is nonzero, it must be cancelled using the f sector and the exact adjacent primitive Delta m=f; treating m as an independent Boolean variable would then be invalid.

For reference, the f term in qplus*L has coefficient

    N=Q(1+c+x3).

Run 304 gives

    Delta4 f=r_t+r_(t+1)+r_(t+2)+r_(t+3),

so

    Delta4(Nf)
      =(Delta4 N)f
       +N_(t+4)(r_t+r_(t+1)+r_(t+2)+r_(t+3)),

with run 312/313

    Delta4 N
      =Q_t j_t+E_t(1+c+x3+j_t).

Therefore the next concrete test is not another high-coordinate transport lemma. It is to simplify Rm on the restricted low-coordinate state space and determine whether it vanishes identically. If it does, combine the displayed r residuals from M and N. If it does not, the m/f primitive relation must be used before coefficient collection.

No claim that Rm vanishes is made here.
