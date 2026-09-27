# Problem 1 run 309: same-parity selectors for u

Problem 1 remains open. Continue from run 308.

Established identities:

    u_(t+4)+u_t = 1+x_6(t)
    j_t = x_6(t+2)+x_6(t)

Apply the first identity at t and t+2 and add. The constants cancel:

    u_t+u_(t+2)+u_(t+4)+u_(t+6)
      = x_6(t)+x_6(t+2)
      = j_t.

Thus

    BOX: u_t+u_(t+2)+u_(t+4)+u_(t+6)=j_t.

Shifting one phase gives

    BOX: u_(t+1)+u_(t+3)+u_(t+5)+u_(t+7)=j_(t+1).

Adding these recovers the run-308 eight-term identity, but the split is stronger: each parity class collapses separately.

Run 308 also gives

    u_t+u_(t+1)+u_(t+2)+u_(t+3)=d_t.

So the u sector now has two four-term reductions: consecutive blocks collapse to d, while same-parity blocks collapse to j. Together with u_(t+4)+u_t=1+x_6(t), these are three cheap rewrite patterns for the remaining transported expression.

For the target S_(t+4)+S_t, first replace each r_(s+4)+r_s by u_s. Then reduce consecutive four-blocks to d, same-parity four-blocks to j, and four-separated pairs to 1+x_6 before using the closed j identities.

Blocker: the product-level u coefficients in the compact S expression still need to be collected. No explicit coordinate-7/8 expansion is needed yet.
