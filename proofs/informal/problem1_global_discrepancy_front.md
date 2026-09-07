# Global front residence and exact discrepancy transport

Status: `partial-proof` for the all-depth identities and their conditional
FULL consequences. This is a lead derivation; external adversarial review
is missing. The fixed cancellation example is a hand certificate using
already verified rows. No numerical experiment is used. Problem1 is OPEN.

## 0. Admission and what is new

Round304 places every cycle representative inside ONE whole-spacetime
shadow E(r). Its ancestry result gives only existence of some initial
discrepancy in a cone. Determine whether the residual bit of every positive
renewal injection is on one globally ordered boundary, and derive an exact
transport law which retains both complete spacetimes. A positive result
would identify the crossing quantity a whole-tail argument must control;
failure would expose an invalid identification of the local residual with
global discrepancy. This is an all-depth structural test, not a larger
prefix or source computation.

This note imports the old delay thresholds, one-bit renewal, and unbounded
zero-extension delays. It does not rerun or reprove those results. The new
use of the global shadow is that there is always one leftmost discrepancy
in the WHOLE row, including when its center-and-left portion is cyclic.
Every renewal injection is an explicitly identified residence interval of
that same front. The exact path identity below retains cancellations and
the complete drivers; it supplies no autonomous finite-state quotient.

## 1. One front from all original cuts (`partial-proof`)

Fix a nonzero, finitely supported actual initial row r, with leftmost1 at
position a and with its ENTIRE original finite right fringe retained.
Assume L_0(r)>0 for the physical center notation. The whole shadow is
hat r(0)=E(r), and both rows evolve under the physical Rule30 map U.
For every integer j define

    L_j=sum_(i<=j) r_i(0)2^(j-i),
    s_j=tau(L_j), C_j=cyc(L_j).                      (1)

These are INITIAL cuts, not cuts of a later rebased row. Spatial deletion
makes s_j nondecreasing in j. It is0 for j<=a, and every s_j is finite.
Because the original right fringe ends, the old zero-extension theorem
implies s_j tends to infinity as j tends to infinity. Thus, for each
physical time u>=0, the integer

    J(u)=min{j in Z:s_j>u}                          (2)

exists and is finite. It is nondecreasing in u and tends to infinity.

Let d_i(u)=r_i(u) XOR hat r_i(u). Then the EXACT leftmost discrepancy is

    m(u)=min{i in Z:d_i(u)=1}=J(u)-u.               (3)

Proof. At time u, the cut ending at physical position j-u is
A^u L_j. The corresponding shadow cut is A^u C_j=cyc(A^u L_j).
These cuts agree iff A^u L_j is cyclic, equivalently s_j<=u. At the
first failing j=J(u), all positions strictly to the left agree, and the
bit at j-u must differ. This proves (3), including existence of a global
discrepancy, without treating its infinite right tail as finite.

In particular m(u)>0 means only that the center-and-left row is cyclic;
the global front and infinitely many right discrepancies still exist.
The earlier one-bit strip variable is recovered as

    b(Y_u)=max(u-J(u)+1,0),
    tau(Y_t)=max(s_t-t,0).                          (4)

These two equations are consistent with, and do not strengthen by
themselves, the previously proved threshold equivalences.

## 2. Exact residence intervals and erasing cells (`partial-proof`)

For each integer j the complete set of times with J(u)=j is

    {u>=0:J(u)=j}=[s_(j-1),s_j) intersect Z.         (5)

An interval is empty when the two endpoints coincide. Equation(5) follows
directly from s_(j-1)<=u<s_j and monotonicity of all original-cut delays.
Thus each characteristic j is visited at most once; its visit may last
several physical time steps. The nonempty intervals partition all times.

During a nonempty residence, the front follows physical positions j-u.
For every u in that interval, the bit immediately to its LEFT is shared by
the actual and shadow rows. The local Rule30 rule at the next position
j-u-1 gives

    d_(j-u-1)(u+1)=1 XOR r_(j-u-1)(u).              (6)

All further-left input discrepancies are zero. Consequently that shared
left-neighbor trace is EXACTLY

    r_(j-u-1)(u)=0 for s_(j-1)<=u<s_j-1,
    r_(j-s_j)(s_j-1)=1.                            (7)

The first line may be empty. The front moves left by one physical cell
at each step before the last, and the final1 erases that front bit. At
the next time J increases to a strictly larger integer. In physical
coordinates that reset step has m(u+1)>=m(u), possibly with a large jump.
Knowing the erasing1 does not determine the next J; the rest of the
evolved discrepancy tail is still required.

This is the global form of the old highest-disagreement wait. It applies
also when the front lies to the RIGHT of the center, where the old
center-and-left discrepancy variable is zero.

## 3. A renewal injection is a residence AFTER crossing the center

Keep the physical renewal's notation

    tau_t=tau(Y_t), T_t=max(tau_t-1,0),
    R_t=tau_(t+1)-T_t, t>=0.

Substituting(4), and using s_(t+1)>=s_t, gives exactly

    R_t=max(s_(t+1)-max(s_t,t+1),0).                (8)

Therefore

    R_t=#{u>=t+1:J(u)=t+1}.                        (9)

When R_t>0, the times counted are precisely

    I_t=[max(s_t,t+1),s_(t+1)) intersect Z.          (10)

They are the part of residence(5) on which the physical front lies at
or LEFT of the center: m(u)=t+1-u<=0. Distinct injections have disjoint
I_t and strictly ordered final erasing times. This is an ordering of
physical front events, not uniqueness or bounded reuse of initial ancestors.

In particular, at the inherited-horizon residual time

    u_0=t+1+T_t=max(s_t,t+1),

the old residual discrepancy is the GLOBAL LEFTMOST discrepancy:

    m(u_0)=-T_t, d_(-T_t)(u_0)=1.                  (11)

If lambda=tau_(t+1), its last erasing cell from(7) is

    (i,u)=(t+1-s_(t+1),s_(t+1)-1)
         =(-lambda,t+lambda).                      (12)

This recovers both offsets of the earlier anchoring-geometry note.
That erasing1 remains outside the original anchored sampling domain;
being adjacent to this front creates no new anchored charge.

For a finite cutoff N, the disjoint residence interpretation gives

    sum_(t=0..N-1)R_t
      =#{u:s_0<=u<s_N, m(u)<=0}.                   (13)

Indeed 1<=J(u)<=N is equivalent to s_0<=u<s_N, and(9) adds u>=J(u).
If s_N>=N, every extra time N<=u<s_N has m(u)<=0; their number is tau_N.
If s_N<N, no time s_N<=u<N has m(u)<=0. The first s_0 times, when
present in the cutoff, have J(u)<=0. These observations also recover
the known telescoping formula sum R_t=tau_N-tau_0+V_N, with
V_N=#{0<=u<N:m(u)<=0}. Equation(13) itself handles N<s_0 as well;
the counting identity, not a subtraction of infinite sums, is primary.

In particular the total sum of injections is the number of front times
with J(u)>=1 and m(u)<=0, possibly infinite. This is not a finite budget.

## 4. Clock-doubling characteristics are never front residences

Let p_j=p(L_j) be the least eventual A-period of the original cut. If

    p_j=2p_(j-1),                                  (14)

the cyclic low drive of L_(j-1) is identically zero. The old one-bit
extension theorem then gives s_j=s_(j-1), including any inherited transient.
By(5), J(u) is NEVER j at any physical time. This is stronger as a geometric
description than R_(j-1)=0 at one extension: the whole characteristic is
skipped by the global front. It uses no FULL assumption.

At every actually visited characteristic j, the local eventual clock is
preserved, p_j=p_(j-1), and the front's final eraser belongs to that common
cyclic drive. The widths make p_j unbounded and give infinitely many skipped
doubling characteristics; J(u) also tends to infinity. No bound on the
number of skipped characteristics per jump is asserted.

Under FULL, the imported source-lateness result additionally puts the front
at or left of the center at every physical doubling source. These remain
the same fixed original cuts and the same actual fringe. It follows, as
already known from renewal, that infinitely many residences have a nonempty
portion I_t. The new representation does not prove their total duration
finite, a positive density, or a uniform lower bound on m(u).

## 5. Full-driver path parity, not positive path counts (`partial-proof`)

Use characteristic coordinates for BOTH complete spacetimes:

    v_j(u)=r_(j-u)(u), h_j(u)=hat r_(j-u)(u),
    Delta_j(u)=v_j(u) XOR h_j(u).

Their rule is v_j(u+1)=v_(j-2)(u) XOR(v_(j-1)(u) OR v_j(u)),
and the same for h. The Boolean identity

    (a OR b) XOR (c OR d)
      =(1 XOR a)*(b XOR d) XOR (1 XOR d)*(a XOR c)

therefore proves the EXACT homogeneous linear recurrence, with coefficients
evaluated on this ONE FIXED PAIR of complete spacetimes,

    Delta_j(u+1)=Delta_(j-2)(u)
       XOR beta_j(u)*Delta_(j-1)(u)
       XOR alpha_j(u)*Delta_j(u),                  (15)
    alpha_j(u)=1 XOR v_(j-1)(u),
    beta_j(u)=1 XOR h_j(u).

As an independent algebraic derivation, write OR(a,b)=a+b+ab over GF(2),
substitute v=h+Delta and group the Delta_j term with the ACTUAL neighbor
v_(j-1). This gives exactly(15), including the product of the two local
discrepancies absorbed in that coefficient.

Unroll(15) on its finite cone. Paths from(k,0) to(j,u) have one-step spatial
increments0,1,2. An increment0 ending at(l,s+1) has weight alpha_l(s);
increment1 has weight beta_l(s); increment2 has weight1. Let G(j,u;k) be
the XOR of the products of edge weights over these paths. Induction on u
gives

    Delta_j(u)=XOR_(k=j-2u..j) G(j,u;k)*Delta_k(0).  (16)

Every sum is finite even though the initial discrepancy tail is infinite.
For the residual(11), j=t+1 and u=t+1+T_t, so the initial cone is exactly
[-t-1-2T_t,t+1], agreeing with the earlier ancestry inclusion.
If that residual is1, some active initial discrepancy has an odd number
of active paths. Neither uniqueness nor bounded reuse follows.

The word 'linear' in(15) does not authorize changing r, h or their initial
differences while holding the same coefficient field fixed. These fields
depend on the full actual and shadow histories. The formula is not a
linearization of E, a freely driven model, or a finite-state update.

## 6. A fixed original-shadow cancellation and a factorization fence

Take the already checked source r with L_0=112 and the complete original
right half zero. The phase certificates give

    C_0=111, C_1=cyc(224)=222.

Thus initially Delta_-1=Delta_0=1, Delta_1=0,
v_0=0 and h_1=0. The physical center at time1 has characteristic j=1.
Equation(15) has alpha_1=beta_1=1 and gives

    Delta_1(1)=1 XOR1 XOR0=0.                      (17)

Two active unit paths, from initial positions-1 and0, reach this center;
their contributions cancel. Direct cell rules independently give actual
center0 from000 and shadow center0 from110 (left-to-right). In fact the
actual center-and-left row is200 and cyclic. Mere existence, or the
positive number, of reachable initial discrepancies is not a birth test.

Even the path factorization is not unique. Interchanging actual and shadow
roles in the OR splitting gives another valid recurrence(15) with

    alpha'_j=1 XOR h_(j-1), beta'_j=1 XOR v_j.       (18)

The two right-hand sides differ by
Delta_(j-1)*Delta_j XOR Delta_j*Delta_(j-1)=0. Their total output is
identical, but their individual path contributions need not be identical.
For the SAME112 initial row at j=0, u=1 (physical position-1), all three
initial discrepancies at-2,-1,0 are1. Formula(15) uses the two parents
-2 and0; formula(18) uses-2 and-1. Both give0. This is a hand example
of factorization dependence, not two different evolutions.

The exact parity representation is useful for retaining the whole driver.
Turning it into a nonnegative charge would require a new argument controlling
cancellation, the choice of paths, and reuse on the FULL domain. None is
provided by the existence of a causal cone or by this factorization.

## 7. What remains open

The unknown crossing history can now be expressed as the portions I_t of
one nondecreasing-characteristic front after it reaches the physical center.
All its initial cuts, its infinite right discrepancy supply, and both actual
drivers remain fixed. A reset ends one residence but does not determine
the next residence or identify a fresh original discrepancy source.

A surviving whole-tail argument must constrain these center crossings using
FULL and the finite ORIGINAL actual fringe, or construct the separate
global charge into the finite post-rebase anchored set with bounded reuse.
The count(13), the skipped clock labels, and the signed path identity(16)
do not themselves supply such a bound. Do not enumerate more front samples,
source paths, local neighborhoods or periodic drivers to illustrate them.

Dependencies: `problem1_global_cycle_shadow.md` Sections1-4;
`problem1_highest_wait_nonforcing.md` Section2 (unbounded original-cut
delays after the finite fringe); `problem1_physical_time_cycle_defects.md`
Sections1,4-6; `problem1_cycle_delay_renewal.md` Sections1-4;
`problem1_reset_anchoring_geometry.md` Sections1-3. The112 certificates
are already checked in the round305 phase-transport record.
