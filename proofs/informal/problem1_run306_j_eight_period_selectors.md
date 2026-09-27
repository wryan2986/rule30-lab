# Problem 1 run 306: j eight-period closure and parity selectors

Problem 1 remains open. Continue from run 305.

Run 305 proved the exact four-step cocycle

    j_(t+4)+j_t=x_3(t),

where j_t=x_6(t+2)+x_6(t). Run 268 gives

    x_3(t+2)=x_3(t)+1,

and hence x_3(t+4)=x_3(t).

Applying the j cocycle twice therefore gives

    j_(t+8)+j_t
      = x_3(t+4)+x_3(t)
      = 0.

Thus

    j_(t+8)=j_t.

So the run-304 skew is exactly 8-periodic on the restricted branch; it has no further high-coordinate drift.

There is also a useful four-sample parity selector. Apply the four-step cocycle at t and t+2:

    j_(t+4)+j_t=x_3(t),
    j_(t+6)+j_(t+2)=x_3(t+2)=x_3(t)+1.

Adding them gives

    j_t+j_(t+2)+j_(t+4)+j_(t+6)=1.

Shifting by one yields the odd-phase companion

    j_(t+1)+j_(t+3)+j_(t+5)+j_(t+7)=1.

Hence each parity class of the eight-phase j word has odd parity, while the full eight-phase parity is zero.

These identities are formal consequences of runs 268 and 305; no finite-state enumeration is needed.

For the current target

    S_(t+4)+S_t = 1+x_5(t)(1+p_t),

the j-driven terms can therefore be reduced modulo an 8-periodic scalar with known even/odd parity. In particular, any four-step transport calculation that produces a full same-parity orbit sum of j can replace it immediately by 1 rather than expanding j through k and ell or through x_6.

This sharpens the remaining blocker. The low j sector is now closed under both four- and eight-step transport and has exact parity selectors. The unresolved part is to rewrite the r-driven sector of the compact run-302 S expression so that its interaction with j exposes one of these selector sums (or cancels before expansion).

Do not expand the 25-monomial common ANF core merely to use this result; preserve the compact S formula and group by r and j first.
