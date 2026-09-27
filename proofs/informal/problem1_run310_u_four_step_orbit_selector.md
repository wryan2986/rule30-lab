# Problem 1 run 310: four-step orbit selector for u

## Status

Problem 1 remains open. Continue from run 309 at commit `c17e4e61721adae2c5fb8a67b953c2efc1d25546`.

Run 307 proved

    u_(t+4)+u_t = 1+x_6(t),

and run 265/run 302 give the exact eight-shift complement

    x_6(t+8)=x_6(t)+1.

Apply the first identity at t and at t+8:

    u_(t+4)+u_t       = 1+x_6(t),
    u_(t+12)+u_(t+8) = 1+x_6(t+8)=x_6(t).

Adding gives the new exact selector

    BOX: u_t+u_(t+4)+u_(t+8)+u_(t+12)=1.

This holds for every phase t. Thus every residue class modulo 4 in a complete 16-phase u orbit has odd parity. It is stronger for sparse four-step orbit sums than the run-309 same-parity selector

    u_t+u_(t+2)+u_(t+4)+u_(t+6)=j_t.

No explicit x7/x8 expansion is used.

Shifting t by 1,2,3 gives four residue-class identities. Adding all four shows the full 16-phase parity is zero, consistent with u_(t+16)=u_t and the earlier block identities:

    XOR_(i=0)^15 u_(t+i)=0.

## Consequence for the run-302 target

The u sector now has four cheap exact rewrite patterns:

1. four-separated pair:
       u_(s+4)+u_s = 1+x_6(s);
2. consecutive four-block:
       u_s+u_(s+1)+u_(s+2)+u_(s+3)=d_s;
3. same-parity four-block:
       u_s+u_(s+2)+u_(s+4)+u_(s+6)=j_s;
4. four-step orbit across one 16-cycle:
       u_s+u_(s+4)+u_(s+8)+u_(s+12)=1.

The fourth pattern is new and removes both the high driver and the low j/d auxiliaries completely. In the final product-level collection of S_(t+4)+S_t, any coefficient pattern recurring at offsets 0,4,8,12 can therefore be collapsed directly to its coefficient (subject to transporting that coefficient separately when it is phase-dependent).

## Blocker

The remaining work is still the product-level collection in the compact run-302 S formula. The useful refinement is that u terms should now be grouped not only into consecutive and parity blocks but also by their residue class modulo 4 across the 16-phase orbit. A complete such orbit contributes exactly 1.

No claim is made yet that the actual coefficients in S_(t+4)+S_t are invariant under those four-step shifts; that coefficient transport is the precise unresolved point.
