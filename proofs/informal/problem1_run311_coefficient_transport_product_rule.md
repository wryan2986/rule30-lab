# Problem 1 run 311: coefficient transport product rule

Problem 1 remains open. Continue from run 310 at commit 883887aea938e9d18bf48792da5fafcfcda22fa1.

All sums below are in the Boolean ring.

Run 307 gives

    u_(t+4)+u_t = 1+x_6(t).

For any Boolean coefficient A_t,

    A_(t+4)u_(t+4)+A_t u_t
      = [A_(t+4)+A_t]u_t + A_(t+4)[1+x_6(t)].

Therefore

    BOX: Delta_4(Au)_t
       = (Delta_4 A_t)u_t + A_(t+4)[1+x_6(t)].

This is the exact product rule for the coefficient-transport issue left by run 310. If A_(t+4)=A_t, the u term disappears completely. A surviving u term is possible only through the four-step skew of its coefficient.

One level higher, because u_t=r_(t+4)+r_t,

    BOX: Delta_4(Ar)_t
       = (Delta_4 A_t)r_t + A_(t+4)u_t.

Thus a four-invariant coefficient descends from r to u and then to x_6 without any coordinate-7/8 expansion.

There is also an exact weighted version of the run-310 selector. Put

    A_k=A_(t+4k),
    u_k=u_(t+4k),
    g_k=1+x_6(t+4k).

Since u_(k+1)=u_k+g_k,

    sum_(k=0)^3 A_k u_k
      = (A_0+A_1+A_2+A_3)u_0
        + A_1 g_0
        + A_2(g_0+g_1)
        + A_3(g_0+g_1+g_2).

Hence a weighted four-step orbit has only one possible surviving u term, and its coefficient is exactly

    A_t+A_(t+4)+A_(t+8)+A_(t+12).

If that coefficient parity is zero, the whole weighted orbit reduces to x_6-level data. Constant A recovers run 310.

For the run-302 target

    S_(t+4)+S_t = 1+x_5(t)(1+p_t),

the next calculation should not seek another transport identity for u. Instead, collect the actual r/u coefficients in the compact S formula and compute their four-step skews. Coefficients with zero four-step skew eliminate u immediately. For the rest, test the four-sample coefficient parity above before any high-coordinate expansion.

Blocker: the remaining task is now finite and algebraic: compute the four-step skews of the small coefficient functions multiplying the r/u sector in run 302. This note gives the exact criterion and residual; it does not assume those skews vanish.
