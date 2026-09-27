# Problem 1 run 307: close the r driver under eight shifts

## Status

Problem 1 remains open. Continue from run 306 at commit `3976fcef8dddaa6003f8bc5cee374f4ab589591d`.

Run 303 reduced the high-coordinate transport to the driver

    r_t := 1 + x_7(t) + e_t x_6(t),

where addition is in the Boolean ring and

    e_t := x_7(t+8)+x_7(t).

Run 265 proves

    x_6(t+8)=x_6(t)+1,
    x_7(t+8)=x_7(t)+e_t,
    e_(t+8)=e_t+1.

The last identity follows there from x_7(t+16)=x_7(t)+1.

## Exact eight-shift closure of r

Put z=x_7(t), y=x_6(t), e=e_t. Then

    r_(t+8)
      = 1 + (z+e) + (e+1)(y+1).

In the Boolean ring,

    (e+1)(y+1)=ey+e+y+1.

Therefore

    r_(t+8)
      = z+ey+y,

and adding

    r_t=1+z+ey

gives the exact formal identity

    r_(t+8)+r_t = 1+x_6(t).

Thus the remaining high driver itself has a very small eight-shift residual.

## Four-step skew of r

Define

    u_t := r_(t+4)+r_t.

Then applying the definition at t and t+4 gives

    u_(t+4)+u_t
      = r_(t+8)+r_t
      = 1+x_6(t).

So u has the same four-step forcing that appeared in the moving-window d tower.

Applying this relation twice,

    u_(t+8)+u_t
      = x_6(t+4)+x_6(t).

Run 304 defines

    j_t=x_6(t+2)+x_6(t).

Hence

    j_t+j_(t+2)
      = x_6(t)+x_6(t+4),

and therefore

    u_(t+8)+u_t = j_t+j_(t+2).

Run 306 proves j_(t+8)=j_t. Shift the preceding identity by eight and add it to itself. The right side cancels, yielding

    u_(t+16)=u_t.

Thus the high and low sectors are linked by the exact chain

    u_t = r_(t+4)+r_t,
    u_(t+4)+u_t = 1+x_6(t),
    u_(t+8)+u_t = j_t+j_(t+2),
    u_(t+16)=u_t.

No explicit coordinate-7/8 ANF is required.

## Consequence for the run-302 target

The remaining target is

    S_(t+4)+S_t = 1+x_5(t)(1+p_t).

Runs 303-306 suggested transporting r_t,r_(t+1),r_(t+2),r_(t+3) separately. This note shows that is unnecessarily expensive. In the four-step comparison, first pair every occurrence of r_(s+4)+r_s into u_s. Any subsequent eight-shift residual of u lands directly in the already-closed j sector.

So the next symbolic calculation should:

1. start from the compact run-302 formula for S_t;
2. substitute the run-303/304 transport dictionary for m,f,c,d;
3. collect all four-step r differences as u_s before expanding products;
4. use u_(s+4)+u_s=1+x_6(s) and u_(s+8)+u_s=j_s+j_(s+2);
5. only then apply the run-306 j parity selectors.

This is a stricter target than expanding the common 25-monomial ANF core and should preserve the cancellations already visible computationally.

## Blocker

The final symbolic cancellation has not yet been completed. The remaining obstruction is no longer independent transport of r or j: it is the product-level interaction of the compact run-302 coefficients with the u/j driver chain above.
