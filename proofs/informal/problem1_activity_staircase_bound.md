# A staircase bound on activity in the complete original history

Status: `partial-proof`, independently re-derived and accepted by the lead
in the stated scope. Problem 1 remains open. Base checkpoint:
`f6f062d5f36d6403c8d0de2dce773b60ada4a5d8`.

Review: `problem1_activity_staircase_review.md`. Two independent methods
agree on all88 admitted local cones. Their finite status is separate
from the all-depth proof. Exact reviewed source, current source, full
reviews and source/admission hashes are archived in
`results/problem1/20260906_activity_staircase_verification.json`.

## Decision and scope

Round five prioritizes fixed-actual-survivor age growth. The nearest-column
two-step defect route so far reproduces the known alternating boundary
identities; it has supplied no new propagation inequality. The present
route retains the complete ORIGINAL history rather than the appended
positions of a forced history. Its concrete candidate is:

> For a finite input, paired original activity terms cannot both vanish
> throughout a time interval whose length is their distance from the top
> pair plus one.

If valid, this gives an explicit harmonic lower bound on long averages of
V and an explicit support bound for the bounded-activity alternative. A
counterexample would invalidate this original-history zero-propagation
mechanism. This is a quantitative strengthening of finite/effective activity
levels, not a repetition of their compactness or finite-entry proofs. It
does NOT itself prove activity growth on an actual survivor. No numerical
experiment, activity-level enumeration, graph, return sweep, or first-witness
search is admitted. The proof is local Boolean algebra and finite counting.

## 1. Finite rows and staggered activity terms (`partial-proof`)

Use the established maps

    T(x)=x XOR ((x<<1) OR (x<<2)),
    pi(x)=x>>2,
    A(x)=pi(T(x))=(x>>2) XOR ((x>>1) OR x),
    V_s(x)=sum_(t=0..s-1) bit_(2s)(T^t(x)), V_0=0,
    R(x)=sup_s V_s(x).

Let x be a nonnegative integer of bit length B, taking B=0 at zero,
and put n=max(ceil(B/2)-1,0). When n=0, the established propagation
bound gives V_s(x)=0 at every age; all lower bounds below are empty.
Assume n>=1 from now on. The highest one is at either 2n or 2n+1.

Write u_i(t)=bit_i(A^t(x)) for i,t>=0. Then

    u_i(t+1)=u_(i+2)(t) XOR (u_(i+1)(t) OR u_i(t)).    (1)

A cannot increase the bit length and preserves the highest one, because
the two higher input bits there are zero. Consequently the pair at
positions 2n,2n+1 contains a one at EVERY t>=0, and every position
at least 2n+2 is zero at EVERY t>=0.

For s>=n and 1<=j<=n define

    w_j(s)=u_(2j)(s-j).

The previously proved A-diagonal identity, with d=s-t, gives

    V_s(x)=sum_(j=1..n) w_j(s), s>=n.                 (2)

Terms with d>n vanish because pi^(n+1)(x)=0; pi commutes with A.
Equation (2) also holds at n=0 as an empty sum. For s>=n+1 additionally
set w_(n+1)(s)=u_(2n+2)(s-n-1)=0. Negative times are never used.

For an ordinary history the w_j are exactly the reversed list of the
preceding original-prefix parity terms in the single-column note. Formula
(2) needs no ordinary-history membership, root, or forced gate.

## 2. The staircase zero-propagation lemma (`partial-proof`)

First a local rectangle fact. If u_i and u_(i+1) are zero throughout
times tau,...,tau+L-1, with tau>=0 and L>=2, then u_(i+2) and
u_(i+3) are zero throughout tau,...,tau+L-2. Equation (1) at i
first gives u_(i+2)(t)=0; equation (1) at i+1 then gives
u_(i+3)(t)=0 over that same shorter interval. Thus shifting a
zero pair upward by TWO spatial positions consumes ONE time value.

**Lemma.** Fix 1<=j<=n and S>=n+1. The two sequences w_j and
w_(j+1) cannot both be zero at every age

    S,...,S+(n-j).

Proof. Put L=n-j+1. If both vanish at an age s, write
tau_s=s-j-1>=0. Their vanishing says

    u_(2j)(tau_s+1)=0,   u_(2j+2)(tau_s)=0.

Equation (1) therefore forces

    u_(2j+1)(tau_s) OR u_(2j)(tau_s)=0.

This gives an adjacent zero pair at positions 2j,2j+1 over L
consecutive times, beginning at tau=S-j-1. Iterate the rectangle
fact n-j times. The pair at 2n,2n+1 is then zero at time tau,
contradicting preservation of the highest one. If j=n there are zero
rectangle iterations and the contradiction is immediate. This also
covers odd B: the top need only belong to the top PAIR, not its even
position at time zero.

The staggered ages in (2) are essential. They give an OR equal to zero
directly. Replacing them by simultaneous columns would change the time
seams and is not the statement proved here.

## 3. A lower bound in every sufficiently late window (`partial-proof`)

For n>=1 put r_max=floor((n-1)/2) and

    H_odd(r)=sum_(a=0..r) 1/(2a+1).

For ANY S>=n+1 and W>=1 the lemma gives

    sum_(s=S..S+W-1) V_s(x)
       >= sum_(r=0..r_max) floor(W/(2r+1)).            (3)

Indeed choose j=n,n-2,n-4,... down to the last positive j. The
selected pairs {w_j,w_(j+1)} are disjoint. Their time lengths L
are exactly 1,3,5,...,2r_max+1. The extra top term w_(n+1) is
zero; if the bottom term w_1 is unselected it is nonnegative.
Partition the W-age interval into floor(W/L) disjoint L-age
subintervals. Each contains at least one one in its selected pair.
Sum first over the subintervals and then over the disjoint pairs.
No independence, average-density assumption, or closed temporal cycle
is needed.

Divide (3) by W and let W tend to infinity. The number of summands
is fixed and finite. Thus

    liminf_(W->infinity) (1/W) sum_(s=S..S+W-1) V_s(x)
          >= H_odd(floor((n-1)/2)),
    R(x) >= H_odd(floor((n-1)/2)).                    (4)

This is logarithmic growth with ORIGINAL support size, not growth with
age for a fixed finite row. A finite row still has V_s<=n at all ages.
Equation (3), rather than an appeal to temporal periodicity, proves (4).

## 4. Explicit finite-support and witness bounds (`partial-proof`)

For an integer K>=0 define

    g(K)=min{r>=0:H_odd(r)>K}.

The odd harmonic sums diverge, so g(K) exists and can be computed using
rational arithmetic. If finite x satisfies R(x)<=K, then

    n<=2g(K),   bitlen(x)<=4g(K)+2.                   (5)

For if n>=2g(K)+1, then r_max>=g(K), and (4) contradicts R<=K.
Inputs with n=0 satisfy the same bound directly. In particular g(0)=0
recovers the correct bit-length bound two for the base level.

There is also an explicit short witness interval AFTER the support
scale is known. Set

    delta_K=H_odd(g(K))-K>0,
    W_K=floor((g(K)+1)/delta_K)+1.

If n>=2g(K)+1, every interval of W_K consecutive ages starting at
S>=n+1 contains an age s with V_s(x)>K. Apply (3) using only its
first g(K)+1 disjoint pairs: its lower bound is at least

    W_K H_odd(g(K))-(g(K)+1)>W_K K.

If every V in that interval were <=K this would be impossible.
This is not a fixed horizon for arbitrary 2-adic oracles: the input
must be finite, and the starting age depends on its support scale n.

Scope controls from established hand certificates, with no rerun:
27 has B=5,n=2 and R=1, consistent with the lower bound 1;
111 has B=7,n=3 and R=2, consistent with the lower bound 4/3.
For K=1, g(1)=1, delta_1=1/3 and W_1=7, so every finite input
with n>=3 has some V>1 in every seven-age interval starting at
S>=n+1. The sharpness of these constants is not asserted.

## 5. An explicit bound for the mortal alternative (`partial-proof`)

Import the reviewed finite-entry theorem and decomposition; they are
not re-proved here. If x is ANY 2-adic input in E_K={x:R(x)<=K},
put

    h=h_V(K)=min{r>=0:H_odd(r)>3K/2},
    y=T^h(x) in N,   z=pi^h(y) in N.

The exact decomposition for s>=h is

    V_s(x)=sum_(t=0..h-1)bit_(2s)(T^t(x))+V_(s-h)(z).

The early terms are nonnegative. Taking s=h+r for EVERY r>=0
therefore proves R(z)<=K. In particular one need NOT replace K by
K+h when bounding this shifted finite row. Equation (5) yields

    bitlen(T^h(x)) <= B_explicit(K),
    B_explicit(K)=2h_V(K)+4g(K)+2.                    (6)

To justify the support seam, y consists of its low 2h digits followed
by z. If z=0 then bitlen(y)<=2h; otherwise it equals 2h+bitlen(z).
Both cases satisfy (6).

This is an explicit replacement for the previously nonconstructive
support bound and the subsequently proved terminating cover search.
For example the elementary integral estimate

    H_odd(r) >= integral_(0..r+1) dt/(2t+1)
             = (1/2)log(2r+3)

gives g(K)<=ceil(exp(2K)) and h_V(K)<=ceil(exp(3K)). Consequently
B_explicit(K)<=2ceil(exp(3K))+4ceil(exp(2K))+2. The harmonic formula
(6) is exact as an upper bound; neither displayed bound is claimed
optimal. No bound on the runtime of the earlier cover-search algorithm
is inferred from this new alternative bound.

Unit triangularity of T gives a unique 2-adic preimage of every y,
as proved in `problem1_effective_activity_levels.md`, Section1. One
may therefore list E_K by enumerating the explicit finite set

    {T^(-h_V(K))(y): 0<=y<2^B_explicit(K)}

and applying the already reviewed exact rational membership algorithm.
This is a proved finite candidate bound, NOT an executed or admitted
census. No new implementation of that listing algorithm is needed.

## 6. Remaining actual-survivor obligation (`inconclusive`)

The bounded alternative now has an explicit support scale, and (3)
is a quantitative relation across the complete original history. It
still has the finite-input premise. Applying it to larger finite
truncations of an actual survivor does not remove that premise or
give an age-growing lower bound for the SAME input: the support scale
and starting age move with the truncation.

To exclude actual bounded activity one must show that the full-fringe
survivor is unequal to EVERY candidate in the corresponding explicit
finite set, for every K, or establish a direct fixed-survivor growth
inequality. Exact candidate descriptions and finite prefix mismatches
do not decide the remaining infinite equality. Pure alternating seed
exclusion and exclusion of every eventually alternating trace also
retain their distinct quantifiers. No phase or preperiod is discarded.
