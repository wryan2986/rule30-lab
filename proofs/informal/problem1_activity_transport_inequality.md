# Transporting characteristic-pair events into original activity

Status: `partial-proof`, fresh independent derivation accepted in scope.
Problem1 remains open. This extends the staircase local lemma to arbitrary
2-adic inputs. It is an ordered-spacetime inequality, not a finite-support
assumption or a new numerical campaign.

Review: `problem1_activity_transport_review.md`; the exact reviewed
source and lead disposition are retained in
`results/problem1/20260906_activity_staircase_verification.json`.

## Purpose and decision

The staircase proof gives a harmonic lower bound when a finite row's top
pair is nonzero forever. Its local zero-propagation implication does not
need finiteness. The new candidate is a counting inequality: each nonzero
event on a high characteristic pair must be accounted for by an event in
each of several disjoint pairs of staggered original activity terms, with
an explicit bound on how many high events a single term can account for.

A failed implication or indexing seam invalidates this route. A successful
proof supplies a growth criterion WITHOUT the finite-input premise; one
must still derive its characteristic-activity hypothesis from the FULL
actual fringe. No activity census, ray sampling, first-witness search, or
additional local cone verification is admitted. The already admitted
8/16/64 local cones cover the only new proof's imported Boolean seams.

## 1. Local transport on arbitrary inputs (`partial-proof`)

For x in Z_2 and i,t>=0 put

    u_i(t)=bit_i(A^t(x)),
    P_j(t)=u_(2j)(t) OR u_(2j+1)(t), j>=1.

Here A=pi T and pi deletes two low bits, as in the staircase note.
For s>=j define

    w_j(s)=u_(2j)(s-j).

Unlike the finite-row convention there is NO last j and no artificial
zero w_(n+1). The exact diagonal identity is

    V_s(x)=sum_(j=1..s) w_j(s), s>=1.                 (1)

Every term remains an original input term. No appended forced-history
position is substituted for it. The cell rule is

    u_i(t+1)=u_(i+2)(t) XOR (u_(i+1)(t) OR u_i(t)).

It immediately gives the Boolean implication

    P_j(t) <= w_j(t+j+1) OR w_(j+1)(t+j+1),           (2)

where <= denotes the order on bits. Indeed if the two terms on the
right are zero, the cell equation at 2j forces the OR defining P_j
to be zero. Both staggered terms exist at age t+j+1.

The two-time rectangle lemma also gives

    P_(j+1)(t) <= P_j(t) OR P_j(t+1).                 (3)

If the right side is zero, the adjacent pair at positions 2j,2j+1
is zero at t,t+1. Two cell equations make the next pair zero at t.
Both (2) and (3) hold for arbitrary higher bits and arbitrary inputs.

Iterating (3), then using (2), proves for 1<=j<=n

    P_n(t) <= OR_(ell=0..n-j)
      (w_j(t+j+1+ell) OR w_(j+1)(t+j+1+ell)).         (4)

The successive time windows overlap; their union is exactly the whole
integer interval 0,...,n-j. Thus (4) has NO binomial multiplicities.
It is a Boolean covering assertion, not a signed or additive identity.

## 2. The finite event-count inequality (`partial-proof`)

Fix n>=1, a>=n-1 and W>=1, all integers. Let

    C_n(a,W)=sum_(t=a..a+W-1) P_n(t),
    r_max=floor((n-1)/2),
    H_n=sum_(r=0..r_max)1/(2r+1).

Then

    sum_(s=a+2..a+W+n) V_s(x)
      >= sum_(r=0..r_max) ceil(C_n(a,W)/(2r+1))
      >= C_n(a,W) H_n.                               (5)

There are W+n-1 ages in the sum on the left.

Proof. Select j=n,n-2,... down to the last positive j. Fix one
such j and set L=n-j+1. For every time t counted by C_n, (4)
forces a nonzero staggered term in the selected pair at some age

    t+j+1 <= s <= t+n+1.

Assign the event t to any one such nonzero occurrence (j or j+1,s).
For a fixed occurrence at age s, possible assigned t satisfy

    s-n-1 <= t <= s-j-1,

an interval of exactly L integer times. Hence no occurrence receives
more than L assignments. All required occurrences lie in
[a+j+1,a+W+n], so the number of ones in this selected pair over that
interval is at least ceil(C_n/L).

The selected pairs of indices are disjoint and their L values are
1,3,5,...,2r_max+1. Enlarge each age interval to the common interval
[a+2,a+W+n]. Its minimum age is at least n+1 because a>=n-1.
Thus EVERY selected index, including n+1, appears in (1) throughout
the common interval. Summing pair counts can only decrease the full
sum of V. This proves the first inequality in (5); ceiling(z)>=z
proves the second. The argument counts a finite set of events and
uses no limit, distribution, independence, or finite-support premise.

If C_n=0 all right-hand terms are zero and the statement remains valid.
If n=1, the common interval has W ages and (5) is just the sum of
the local inequality (2) for j=1. The extra w_2 term is retained;
setting it to zero on arbitrary inputs would be an error.

## 3. A density criterion for one fixed survivor (`partial-proof`)

Define, explicitly using a limsup so that no existence theorem for a
Banach-density limit is needed,

    d_n^*(x)=limsup_(W->infinity)
                  sup_(a>=n-1) C_n(a,W)/W.

Always 0<=d_n^*<=1. If R(x)<infinity, (5) and V_s<=R give

    R(x)(W+n-1) >= C_n(a,W) H_n

for all a,W in scope. Take the supremum in a, divide by W, and
then let W tend to infinity. For every fixed n,

    R(x) >= d_n^*(x) H_n.                            (6)

The same inequality is trivially valid with R=infinity in the
extended nonnegative reals. As H_n tends to infinity with n, either
of the following conditions on ONE FIXED input x is sufficient for
unbounded activity:

    sup_n d_n^*(x) H_n = infinity;                    (7)

or the stronger, simpler condition that some epsilon>0 satisfies

    d_n^*(x)>=epsilon for infinitely many n.          (8)

These are proved sufficient conditions, NOT proved properties of the
actual survivor. Conversely bounded R<=K forces the explicit bound
d_n^*<=K/H_n for every n. This is a necessary restriction; its converse
is not asserted. There is also a finite witness version of (5):

    R_(a+W+n)(x)
       >= [sum_(r=0..r_max)ceil(C_n(a,W)/(2r+1))]
                                                    / (W+n-1). (9)

No parameter search or ray sampling is admitted by these formulas.

## 4. Geometry and the unresolved coupling (`partial-proof` / `inconclusive`)

The identity A^t=pi^t T^t gives

    P_n(t)=bit_(2n+2t)(T^t(x))
                      OR bit_(2n+2t+1)(T^t(x)).       (10)

In physical coordinates with the supplied tail x to the left of a
cut at coordinate0, these are the two cells at coordinates
-2n-t and -2n-t-1 at time t. They lie on two neighboring LEFT-moving
characteristic rays. They are not the fixed spatial column sampled by
V_s, nor the fixed neighboring column that gives the actual u/t branch.

Equation (10) also reads the true full spacetime when an actual right
fringe is attached to the cut. The radius-one backward cone of the
rightmost sampled cell -2n-t has right endpoint -2n at time0, and
that of its neighbor ends at -2n-1. Thus neither cone touches the
attached cells to the right of the cut. This is a precise connection
to the actual original row, without replacing the supplied right
fringe by an unconstrained driver.

What remains unproved (`inconclusive`) is that actual alternating-center
coupling forces (7), (8), or another useful lower bound in (5). Bounded
gaps in the u/t schedule concern a different line and give no such
conclusion by themselves. Positive activity on one fixed ray is also
insufficient: the condition requires unbounded ray offsets n for the
same x. The original finite-support obstruction has not disappeared.

An essential hand scope control is x=1: R(x)=0 and all P_n, n>=1,
are zero, so (5) is vacuous as required. Another is x=-1: T(-1)=1,
R(-1)=1, and A(-1)=0. Thus every P_n is one at t=0 and zero for
all t>=1, so d_n^*=0. Infinitely many initially active high pairs
DO NOT give the persistent or recurrent density required in (7).
No numerical rerun of these established rational controls is performed.
