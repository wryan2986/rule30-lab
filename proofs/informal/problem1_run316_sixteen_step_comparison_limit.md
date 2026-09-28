# Problem 1 run 316: limit of the sixteen-step comparison

Problem 1 remains open.

Runs 314--315 imply qplus, j, and u are each 16-periodic. Therefore the mixed terms qplus*j*u and qplus*(j+j_(t+1))*u are exactly 16-periodic.

This shows that taking Delta16 of the compact run-302 expression is not, by itself, a useful route to the desired Delta4 identity: it annihilates the isolated high sector by periodicity and loses the phase information needed to determine Delta4 S.

The point can be checked directly. Put C=(1+x5)*j and D=j+j_(t+2). Run 315 gives

    Delta8(qplus*j*u) = C*u + qplus_(t+8)*j*D.

Here C,D,j,x5 are 8-periodic, u_(t+8)+u_t=D, and qplus_(t+16)+qplus_(t+8)=1+x5. Applying Delta8 again gives

    Delta8^2(qplus*j*u)
      = C*D + (1+x5)*j*D
      = 0.

The cancellation is tautological because C=(1+x5)*j; it produces no new low-coordinate constraint.

So the next calculation should preserve Delta4 rather than pass immediately to Delta16. Normalize every shifted u phase in the actual run-302 Delta4 S expression to one representative using the run-308--310 selectors and run-315 transport. The decisive high-coordinate question is whether the full coefficient of that surviving representative u cancels. Only after that cancellation should the remaining low-coordinate polynomial be compared with 1+x5*(1+p).

Precise blocker: extract and simplify the complete product-level coefficient of a normalized u_t in Delta4 S. High-driver transport is closed; coefficient cancellation in the full compact formula is not yet proved.

For completeness, the previously derived but separately unpersisted run-314 fact is qplus_(t+8)+qplus_t=1+x5_t, hence qplus_(t+16)=qplus_t.