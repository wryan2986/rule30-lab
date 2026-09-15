# Problem 1: forced doubling fiber causal-cone audit

## Status

This note resolves the cone-width question left by run 49 for the existing nonresetting/reset scan construction. It is a route audit, not a proof of Problem 1.

## Direction of causal influence

For

\[
(Ax)_i=x_{i+2}\oplus(x_{i+1}\lor x_i),
\]

coordinate `i` at the next A-time depends only on coordinates `i,i+1,i+2` at the current time. Hence a perturbation supported in coordinates `<k` can never affect coordinates `>=k` at any later time. Low-bit forcing propagates only toward still lower output indices, not upward into the high projection.

Thus the upper projection is actually protected forever. This is exactly the factor identity

\[
A^t(x)\gg k=A^t(x\gg k).
\]

The finite-duration cone language of run 49 is therefore unnecessarily weak for coordinates strictly above the forcing support.

## But the doubling fiber is not above the forcing

The relevant one-bit lift has the form

\[
w_s=2z_s+a_s,
\]

where `z_s` is the periodic parent/core state and `a_s` is the newly introduced low bit. The lift recurrence is

\[
a_{s+1}=c_s\oplus(b_s\lor a_s),
\]

with `b_s=bit_0(z_s)` and `c_s=bit_1(z_s)`.

Therefore the coordinate carrying the period-doubling certificate is precisely the newly introduced LOW fiber bit `a_s`. It is not a high coordinate separated from the reset/boundary prescription. The reset/phase choice acts at the same fiber level that distinguishes the two lifts.

The concrete nonresetting-source classification makes this visible. For the two-bit t-source, the actual state `x=Y_t` and periodic shadow `z=Z_t` have low bits

    x: (1,1,0,1)
    z: (0,0,0,1)

with all bits >=2 agreeing. Direct evolution gives

    (Ax mod 4, Az mod 4)=(1,2),
    A^2 x=A^2 z.

So the disagreement is entirely in the low forced/fiber region. The upper state is protected, but the low history needed for the antiperiodic certificate is exactly where actual and periodic comparison histories differ.

## Consequence for the run-49 criterion

The proposed sufficient condition

\[
\text{distance(fiber, forcing support)}\ge\text{2p-step causal width}
\]

cannot hold for the existing one-bit doubling certificate: the relevant fiber is itself at the forcing boundary, so its separation is zero.

This is not merely failure to prove a large enough margin. It is a structural mismatch between the protected coordinates and the certificate coordinate.

Accordingly, the projection/cone route does not transfer the forced scan's antiperiodic fiber history verbatim into the original common-origin realization.

## What remains usable

The exact projection theorem remains valuable for the parent/high coordinates: every high-coordinate history outside the low modification is genuine for all future times. A successful bridge would therefore have to encode the low-fiber complement relation into some property of the protected parent/high history, or use the already established gate/source/return identities to charge the low discrepancy to genuine activity.

In particular, a viable next target is an elimination identity: use

\[
a_{s+1}=c_s\oplus(b_s\lor a_s)
\]

and the antiperiodicity `a_{s+p}=1\oplus a_s` to derive a nontrivial constraint involving only the protected parent traces `b,c` over one parent period. Such a constraint would survive exact projection and avoid transporting the forced fiber itself.

## Dead ends fenced off

1. Do not seek a large spatial separation between the reset support and the one-bit doubling fiber in this construction; they occupy the same low boundary layer.
2. Do not infer that the high projection's perfect causal protection also protects the new low lift bit.
3. Do not spend further effort estimating a `2p` cone width for this certificate. The relevant distance is already zero.
4. If the antiperiodic route continues, eliminate the fiber in favor of parent/high traces or charge its forced discrepancy through genuine gate/source events.
