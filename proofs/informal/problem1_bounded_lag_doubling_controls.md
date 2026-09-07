# Arbitrarily large clocks at bounded-lag actual initial blocks

Status: `partial-proof` for the construction below; `refuted` for the
precise local lower-bound claim in Section 3. Verification records:
`problem1_round8_bounded_lag_review.md` and `problem1_round8_fresh_review.md`;
lead acceptance is recorded in ASTRA_HANDOFF.md. The infinite FULL/finite-entry
incompatibility remains `inconclusive`. Problem 1 is OPEN.

## 0. Admission and choice of route

Round seven forces infinitely many late source diagonals at inverse-scan
clock doublings. It does not force their lag heights to grow. The concrete
question here is whether large source period alone forces large source or
successor preperiod, even with finite entry and actual initial fringe
compatibility. A positive answer would strengthen the required passages
before attempting to exclude them. A negative answer would require a
proof to use more of the full future than one transition and these initial
blocks. Both outcomes concern the current bottleneck directly.

The routes considered were: (i) exact local mismatch/reset propagation;
(ii) the stronger assertion that uniformly bounded preperiods along one
infinite permitted orbit imply bounded periods; and (iii) a universal
eventual-entry estimate at the original zero fringe. Route (i) has the
lowest cost and an exact falsification test, and is settled here. Route
(ii) is still open; the sidecar does not refute it. Route (iii) remains
open and is not tested by extending a transient or prefix census.

No scientific program, period list, candidate sweep, or larger actual
prefix was generated. The family is obtained from the existing all-depth
clock-growth theorem, not from a finite search.

Import A, Theta, I_a, Phi and G(c)=I_3 shift^2(c) from the reviewed
full-fringe and reset-language notes. Let tau(c) be the least temporal
preperiod and p(c) the least eventual period. For eventual-periodic codes,
tau(Theta(x)) is the first A-cycle entry time of x, by full-code
injectivity. Finite entry A^h x finite is a different condition from
cycle entry at h; the construction below happens to satisfy both at h=4.

## 1. Supply of finite cycles with unbounded doubling-source periods (`partial-proof`)

Fix the finite input v=1, with original zero right fringe, and put

    V_m=4^m, E_m=Theta(V_m), r_m=p(E_m).

Section 1 of `problem1_scan_doubling_cycle_lag.md` proves r_m tends to
infinity for this fixed input WITHOUT a FULL assumption. Section 2 of
`problem1_inverse_scan_reset_language.md` proves each next period equals
r_m or 2r_m. Consequently there are doubling indices with source periods
exceeding every prescribed P. This is an existence consequence of the
reviewed theorems; no such index is found numerically.

For one such index, take the phase-correct purely periodic completion
u of E_m. This is Theta(z) for a FINITE A-periodic integer z: choose a
multiple k of r_m beyond E_m's preperiod and set z=A^k V_m. Then
Theta(z)=shift^k E_m is precisely that completion. The finite orbit of
V_m stays finite, and z is on its eventual cycle. Its least period is
p=r_m>P.

The exact doubling classification gives precisely one of:

    u has alphabet {0,2}, with an odd number of 2s per least period;
    u has alphabet {0,3}, with an odd number of 3s per least period. (1)

Here "has alphabet" means contained in the displayed set. The relevant
nonzero symbol must occur. We do NOT assert unbounded p for EACH type
separately, nor need to choose a particular type. Both types are handled
by the same construction. These source periods are dyadic, as expected
for finite A cycles; no arbitrary-period finite-cycle claim is made.

## 2. One uniform construction for both types (`partial-proof`)

Prepend four symbols to u:

    s=(3,2,2,0,u_0,u_1,...), x=Theta^(-1)(s),
    c=G(s)=I_3(2,0,u_0,u_1,...).                    (2)

Because shift^4 s=u=Theta(z), conjugacy and injectivity give

    A^4 x=z finite and A-periodic,
    tau(s)<=4, p(s)=p.                             (3)

This asserts finite entry, not that x is initially a finite integer.
It also gives T^4 x finite by the imported identity A^4=pi^4 T^4.

The scan head is a hand consequence of the reviewed H table:

    c_0=3, c_1=H_2(3)=1, c_2=H_0(1)=1.             (4)

From time 2 the input drive is the periodic word u, and c_2=1 belongs
to BOTH invariant pairs: {1,3} for type {0,2}, and {0,1} for type
{0,3}. On the appropriate pair each 0 acts identically and each
relevant nonzero symbol swaps the pair. The odd count in (1) therefore
gives, for every t>=2,

    c_(t+p)=the other member of the pair from c_t,
    c_(t+2p)=c_t.

Thus tau(c)<=2 and p(c)=2p. To verify LEAST period, Phi c=shift^2 s
forces p to divide p(c), whereas the available 2p period makes p(c)
divide 2p; the swap excludes p. This is an exact infinite continuation.

Both source and successor have the required permitted heads:

    (s_0,s_1,s_2)=(3,2,2), (c_0,c_1,c_2)=(3,1,1).   (5)

There is also actual initial-fringe compatibility, beyond those abstract
heads. Attach the ZERO right half at time zero to this x, and retain
the original scans B_j=I_0^j s, D_j=(B_j)_(2j). The hand calculation
in Section 3 of `problem1_full_fringe_temporal_diagonal.md` gives

    D_0=D_1=D_2=3                                  (6)

exactly from s_0=3,s_1=2,s_2=2. Indeed D_1=3 forces s_1=2 when
s_0=3; under these two symbols, D_2=3 forces s_2=2 by a permutation
of that last input. All these equivalences use I_0 from the original
time-zero boundary. No boundary is reset at a later block.

The local alternating-center identity then gives the actual center
values 1,0,1,0,1,0 at times 0 through 5. In particular c is the actual
time-two center-and-left code, not just a freely chosen forced successor.
No D_j for j>=3 is claimed. The construction does not supply an
infinite permitted orbit or a FULL survivor.

## 3. Exact local claim refuted; global quantifiers retained (`refuted` / `inconclusive`)

For EVERY P there exists x with zero initial right fringe such that

    A^4 x is finite and A-periodic;
    D_0=D_1=D_2=3;
    p(Theta(x))>P, p(Theta(X_1))=2p(Theta(x));
    tau(Theta(x))<=4, tau(Theta(X_1))<=2.             (7)

Here X_1 is the ACTUAL center-and-left row at time two. Therefore no
universal lower bound tending to infinity with the source period can
hold for either of these two preperiods under just the hypotheses in
(7). This includes proposed bounds on their maximum: it never exceeds
four in this family. The source is late as required by round seven:
its least preperiod is positive because s_0=3 is outside a {0,2}
tail, while s_1=s_2=2 lie outside a {0,3} tail.

The x and z here vary with P. There is NO single x shown to realize
infinitely many such transitions. It would be a quantifier error to
infer a counterexample to either of these still-open assertions:

1. An infinite FULL finite-entry orbit must have unbounded lag heights.
2. Uniformly bounded preperiods along an infinite permitted G orbit
   force bounded eventual periods.

Nor does this refute a local bound restricted to initially finite x;
our x is proved finite after four physical steps but may be infinite at
time zero. Rephasing at time four does not preserve the displayed
doubling source or its stated small-preperiod bounds.

## 4. Continuation fence (`inconclusive`)

The useful next target remains control of passages along ONE fixed
actual FULL realization, with all future original-fringe constraints.
Any period-dependent lag bound must use hypotheses beyond (7), such as
the infinite future, a global temporal arrangement, or initially finite
support at the transition being studied. This construction gives no
permission to lengthen the fixed horizon or run a prefix, lag, period,
cycle, denominator, or candidate census.

Dependencies: `problem1_full_fringe_temporal_diagonal.md` Sections 1-4;
`problem1_inverse_scan_reset_language.md` Section 2;
`problem1_scan_doubling_cycle_lag.md` Section 1;
`problem1_anchored_activity_finite_entry.md` for A^h=pi^h T^h.
