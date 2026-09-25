# Problem 1 — run 257: eliminate the two upper coordinates from the b=1 parity target

Problem 1 remains open.

Run 256 reduced the r=11,N=32 one-extra-skew case, on b=1, to

    XOR_{even q<32} [x_10(q) XOR alpha_q x_9(q)] = 1,

where

    alpha_q = a XOR A_q,
    A_q = XOR_{j<q}(1 XOR x_8(j)),

and a is the 32-step skew of x_10.

This run removes x_9 and x_10 entirely from that target.

Put

    h_s = x_10(s) XOR alpha_s x_9(s)
    g_s = x_8(s) OR x_7(s).

Since x_9(s+1)=x_9(s) XOR g_s and
alpha_{s+1}=alpha_s XOR 1 XOR x_8(s), direct Boolean expansion gives the exact one-step identity

    h_{s+1} XOR h_s = (1 XOR alpha_s) g_s.          (1)

The cancellation is worth recording: if w=x_9, v=x_8, z=x_7, then the ANF of the left side after substituting the Rule-30 updates is

    v XOR alpha*v XOR z XOR alpha*z XOR v*z XOR alpha*v*z
      = (1 XOR alpha)(v OR z).

Thus the upper coordinates disappear.

For any binary sequence h and 32 samples, writing d_s=h_{s+1} XOR h_s,

    XOR_{even q<32} h_q
      = XOR_{0<=s<30, s mod 4 in {0,1}} d_s.        (2)

Reason: h_0 occurs 16 times and cancels; d_s occurs in h_2,h_4,...,h_30 exactly 15-floor(s/2) times, which is odd exactly for s mod 4 equal to 0 or 1. Substituting (1), the run-256 target is therefore equivalent to the lower-coordinate identity

    XOR_{0<=s<30, s mod 4 in {0,1}}
        (1 XOR alpha_s)(x_8(s) OR x_7(s)) = 1.       (3)

This is a substantial reduction: (3) depends only on x_7,x_8, the lower accumulated phase alpha, and the skew bit a through alpha_0=a. No x_9 or x_10 remains.

I exhaustively rechecked all 4096 initial 12-bit prefixes. On the b=1 branch there are 512 states; (3) equals 1 for all 512, split evenly between a=0 and a=1 (256 each). Hence the remaining identity is independent of the upper skew choice a in the finite census.

A useful reformulation follows from b=1 itself:

    b = XOR_{s<32} g_s = 1.

So the remaining analytic task is to show that, under the actual 32-periodic lower-prefix dynamics through coordinate 8 and b=1, the weighted subset in (3) captures odd total g-parity. This is now a statement entirely about the closed lower orbit and the phase recursion

    alpha_{s+1} XOR alpha_s = 1 XOR x_8(s).

Next target: simplify (3) using 4-step blocks. Because its selector is exactly s mod 4 in {0,1}, a two-step or four-step telescoping identity involving alpha and g is the natural next attack. Also determine analytically why the value is independent of alpha_0=a.
