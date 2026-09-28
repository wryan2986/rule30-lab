# Problem 1 run 320: certified four-periodicity of the direct-alpha coefficient

Problem 1 remains open. This continues the compact run-302 four-step target.

Write Q=qplus and w=x5. In the run-302 expression

    S = p+f+de+pz+pe + (1+w)K + Q L,

the complete coefficient of the unshifted alpha_t is

    C_t = (1+w_t)(1+d_t) + p_t Q_t.

Indeed K contributes alpha(1+d), while L has only the additional p*alpha occurrence.

Put

    s_t = alpha_(t+4)+alpha_t.

Then alpha_(t+4)=alpha_t+s_t, so the direct-alpha block obeys

    Delta4(C alpha)_t
      = (C_(t+4)+C_t) alpha_t + C_(t+4) s_t.

The run-302 exhaustive certificate was evaluated on all 128 restricted states while retaining the run-262 scalar alpha, and its final ANF for S_(t+4)+S_t is

    1+x5+p*x5,

with no alpha monomial. The auxiliary window differences m,f,e,... are invariant under toggling the common alpha value, so they cannot hide an alpha coefficient. Therefore the certificate separately proves

    BOX: C_(t+4)+C_t = 0,

hence

    BOX: C_(t+4)=C_t

on every restricted state, and consequently

    BOX: Delta4(C alpha)_t = C_t s_t.

This is a certified lemma, not yet an analytic proof.

There is also an exact primitive relation. Since m_t=alpha_(t+8)+alpha_t,

    s_(t+4)+s_t = m_t.

Thus the direct alpha sector is a four-step primitive above the already studied m/f/r/u chain.

For an analytic replacement of the finite certificate, use

    H = Delta4 x5 = p(1+x3),
    J = Delta4 d = j_t+j_(t+1),
    E = Delta4 Q.

A Boolean product expansion gives the low-coordinate identity

    Delta4 C
      = (1+x5)J + H(1+d) + HJ + pE.

Run 313 gives

    E=(j_t+j_(t+2))(1+x5)
      +x6*H+(j_t+j_(t+2))*H.

Therefore proving C four-periodic analytically is equivalent to proving the explicit low-coordinate polynomial

    (1+x5)J + H(1+d) + HJ + pE = 0.

No x7/x8 orbit expansion is required for that sublemma.

Important consequence for the next calculation: do not transport the p*alpha term separately. First combine every direct alpha occurrence into C*alpha, replace its four-step difference by C*s, and only then combine that s contribution with the m/f terms. The remaining high-coordinate problem is cancellation of this C*s term against the m/f transport, with Delta4 s=m available.

Blocker: an analytic cancellation of C*s with the rest of Delta4 S is not yet proved. The direct alpha coefficient itself is closed by the existing finite certificate, and its certificate-free replacement is the displayed low-coordinate identity.
