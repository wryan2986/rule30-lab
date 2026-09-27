# Problem 1 run 308: four-phase parity of the r-skew driver

## Status

Problem 1 remains open. Continue from run 307 at commit `f5db23d32b4f05ea7996ffb3f57472a0a836e8ef`.

Run 307 defined

    r_t := 1 + x_7(t) + e_t x_6(t),
    u_t := r_(t+4) + r_t,

and proved

    u_(t+4)+u_t = 1+x_6(t),
    u_(t+8)+u_t = j_t+j_(t+2),
    u_(t+16)=u_t.

There is a stronger block identity that follows by reconnecting this driver chain to the original coordinate-8 skew.

## Eight consecutive r terms equal the 16-shift x8 skew

Run 265 defines

    f_t := x_8(t+8)+x_8(t)

and proves

    f_(t+1)+f_t = r_t.

Therefore telescoping over eight adjacent phases gives

    r_t+r_(t+1)+...+r_(t+7)
      = f_(t+8)+f_t.

But directly from the definition of f,

    f_(t+8)+f_t
      = [x_8(t+16)+x_8(t+8)]
        +[x_8(t+8)+x_8(t)]
      = x_8(t+16)+x_8(t).

Run 263 defines exactly this 16-shift skew as d_t. Hence

    BOX:  r_t+r_(t+1)+...+r_(t+7) = d_t.

This is formal and uses no finite-state enumeration.

## Four consecutive u terms equal d_t

By definition,

    u_(t+i)=r_(t+i+4)+r_(t+i).

Adding for i=0,1,2,3 gives every r phase from t through t+7 exactly once. Therefore

    BOX:  u_t+u_(t+1)+u_(t+2)+u_(t+3) = d_t.

This is the useful new selector. The four-step high-driver differences do not merely have bounded transport: their complete four-phase block collapses to the already-present scalar d_t.

Shifting by four gives

    u_(t+4)+u_(t+5)+u_(t+6)+u_(t+7)=d_(t+4).

Adding the two block identities and using run 304,

    d_(t+4)+d_t=j_t+j_(t+1),

recovers

    sum_(i=0)^7 u_(t+i)=j_t+j_(t+1).

This is also consistent with run 307's pointwise relation
u_(s+4)+u_s=1+x_6(s), since XOR over s=t,...,t+3 gives
XOR_{i=0}^3 x_6(t+i)=j_t+j_(t+1).

## Consequence for the run-302 target

The remaining target is

    S_(t+4)+S_t = 1+x_5(t)(1+p_t).

Run 307 proposed collecting four-step r differences into u before expanding products. The new identity shows what to do next: whenever the transported expression produces a complete block

    u_t+u_(t+1)+u_(t+2)+u_(t+3),

replace it immediately by d_t. This returns the high r-sector to the same scalar d already present in K and L, so cancellation can occur before any coordinate-7/8 ANF is introduced.

The preferred order is now:

1. substitute the run-303/304 transport dictionary into S_(t+4)+S_t;
2. rewrite r_(s+4)+r_s as u_s;
3. collect complete four-phase u blocks and replace them by d_t;
4. reduce leftover u pairs using u_(s+4)+u_s=1+x_6(s);
5. only then use the run-305/306 j identities.

This is strictly smaller than treating the u phases independently.

## Blocker

The final product-level cancellation has not yet been completed. The remaining question is whether the coefficients of the u phases in the transported run-302 expression assemble into complete four-phase blocks (or block plus reducible pairs). If they do, the high-driver sector collapses back to d_t without explicit high-coordinate expansion.
