# Problem 1 run 325: the F*m obstruction cancels when the full r-boundary is restored

Problem 1 remains open. Continue from runs 321--324.

Run 324 correctly proves that the five-variable scalar F has no pure-low temporal primitive. However, F was obtained only after separating the r-boundary from the m/f block. Restoring that boundary makes the apparent obstruction cancel algebraically.

Use the notation of run 321:

    M = Q(1+d+p),
    N = Q(1+c+x3),
    D = Delta4 N,
    Rm = C + Delta4 M,

with C=(1+x5)(1+d)+pQ and Delta4 C=0. The complete m/f/r contribution produced in run 321 is

    B =
      Rm*m + D*f
      + M_(t+4) Delta4 m
      + N_(t+4) Delta4 f.

(The two r sums in run 321 are exactly Delta4 m and Delta4 f.)

Apply the Boolean product rule

    Delta4(XY) = (Delta4 X)Y + X_(t+4) Delta4 Y.

Therefore

    M_(t+4) Delta4 m = Delta4(Mm) + (Delta4 M)m,
    N_(t+4) Delta4 f = Delta4(Nf) + D f.

Substitution into B gives

    B
      = [Rm + Delta4 M]m
        + [D+D]f
        + Delta4(Mm)+Delta4(Nf)
      = C*m + Delta4(Mm)+Delta4(Nf).

Run 320/321 gives s_(t+4)+s_t=m and Delta4 C=0, hence

    C*m = Delta4(C*s).

Consequently the ENTIRE block satisfies the exact identity

    BOX:
    B = Delta4(C*s + M*m + N*f).

This is not a new periodicity proof by itself: it reconstructs the four-step difference of the pre-difference high block. Its value is diagnostic. The odd-orbit class of the run-323 scalar F is an artifact of discarding the attached r-boundary before taking the primitive. It is not an obstruction of the full post-four-step expression. In particular, do not enlarge the state or descend to u merely to cancel F*m.

This also corrects the immediate target suggested at the end of run 324. Recombining only F*m with the r terms cannot yield a new independent obstruction; the full m/f/r sector collapses exactly as above. The next useful target must return to the complete run-302 Delta4 S calculation and collect what remains OUTSIDE this reconstructed high block (especially the low scalar terms and the other K/L coefficient contributions), then test cancellation against the known certificate

    Delta4 S = 1+x5+p*x5.

If an analytic proof is desired, the still-certificate-backed input Delta4 C=0 should also eventually be replaced by the explicit low identity in run 320.

Dead end closed: further primitive searches for F, or u-transport introduced solely to repair F, are unnecessary.
