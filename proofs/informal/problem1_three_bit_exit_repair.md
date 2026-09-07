# Exact repair of a one-bit exit inside an eventual three-bit strip

Status: `partial-proof` for the conditional all-depth return, delay profile,
and clock accounting. External review is missing. Fixed algebra checks are
`finite-exhaustive` only on their listed assignments. No FULL survivor or
eventual strip bound is established. Problem 1 remains OPEN.

## 0. Admission: test the obstruction to extending the collapse

The new K=2-to-K=1 theorem excludes a one-bit exit because it reaches a
third spatial bit. Before trying to iterate that proof, determine whether
the very same exit must continue expanding inside a THREE-bit bound or
can repair. Forced further expansion would extend the exclusion mechanism;
a precise repair branch would identify the additional full-shadow datum
that such an extension has to control. No width sweep, new source, longer
gate-prefix experiment, or freely chosen shadow orbit is admitted.

This is one symbolic continuation of the already identified exit. It uses
the established actual no-uu and no-ttttt theorems; those languages are not
recomputed. The result below is a conditional repair law, not a refutation
of an eventual K=3-to-K=1 implication on the possibly empty FULL domain.

## 1. Fixed orbit and statement (`partial-proof`)

Keep ONE finite nonzero FULL actual row and its complete original finite
right fringe, and the global E shadow, with d_i=r_i XOR hat r_i. Assume
b(Y_s)<=3 for every sufficiently late physical time s. Choose an even v
in that late region with the known exit conditions

    d_i(v)=0 for i<=-1, d_0(v)=1,
    actual gate at v is u, hat r_1(v)=0.              (1)

Write (h,k)=(hat r_1(v+4),hat r_2(v+4)). Then necessarily

    gates at v,v+2,v+4,v+6 are u,t,t,t,
    h=0,
    d_i(v+6)=0 for every i<=-1,
    e:=d_0(v+6)=1 XOR k.                             (2)

The exact spatial depths and least A-delays through this repair are

| offset from v | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| b(Y) | 1 | 1 | 2 | 3 | 2 | 3 | e |
| tau(Y) | 1 | 3 | 2 | 3 | 2 | 1 | e |

In particular there are TWO new positive injections, of sizes 3 and 2,
before repair. Returning to the negative-half agreement region does not
empty the original shadow's infinite right discrepancy supply.

## 2. The two-step calculation at the intervening t rows

At an even FULL time w suppose the only possible center-and-left
disagreements are

    d_-1(w)=1, d_0(w)=ell in {0,1}.

Suppose its actual gate is t. Let z be the next actual gate-u indicator,
and put h=hat r_1(w), k=hat r_2(w), hat u=1[(h,k)=00]. At this source,
actual bits0..3 are (1,1,0,1), while shadow bits1,2,3 are (0,0,1).
FULL also identifies actual bit4 with z: two A updates have low bit
Y_w[4], and the paired physical bridge makes it bit2 at w+2.

One physical update gives

    d_-2(w+1)=1, d_-1(w+1)=ell,
    d_0(w+1)=(1 XOR ell) OR h.                       (3)

The shared cell at -3 at this odd time is 1 XOR z. Therefore the next
even discrepancy at -3 is z. Directly updating the remaining cells gives

| ell | d_-3(w+2) | d_-2(w+2) | d_-1(w+2) | d_0(w+2) |
| --- | --- | --- | --- | --- |
| 0 | z | 0 | 1 | 1 |
| 1 | z | 0 | h | hat u |

All positions<=-4 agree. For an independent low-bit derivation, the A
difference at the source has only bits (delta_0,delta_1)=(ell,1).
The actual A low pair is (1,0), its next bit is 1 XOR z, and its shadow
high bit is 1. A second A update therefore has difference delta_0=0,
delta_1=z, with all higher bits zero. Shifting by two accounts for the
two leftmost columns of the table; direct center updates give its other
two columns. This checks both coordinate offsets.

Under the eventual b<=3 premise, z must be 0: otherwise b(w+2)=4.
Thus a t row with a -1 defect MUST be followed by another actual t row
as long as this table applies, including when that transition repairs it.

## 3. No five t gates forces repair at the first opportunity

The exit table supplies at v+2 the state d_-1=1,d_0=0 and agreement at
every position<=-2. Its gate is t by actual no-uu. Section 2 forces the
next gate t, gives b(v+3)=3, and at v+4 gives d_-1=d_0=1, with every
position<=-2 agreeing. The same table forces the gate at v+6 to be t.

If h=hat r_1(v+4) were 1, the state at v+6 would again be d_-1=1,d_0=0.
The next two uses of Section 2 would force t gates at v+8 and v+10.
Together with v+2,v+4,v+6 these are five consecutive t gates, forbidden
on the actual full fringe. Hence h=0. The table now gives negative-half
agreement at v+6 and center difference hat u=1 XOR k, proving (2).

This is an induction through a fixed number of exact alternatives, not
an enumeration or a state graph whose shadow flags may be chosen freely.
It uses the future b bound through v+10 to exclude the nonrepair branch.
No claim is made that arbitrary flags meeting (2) occur on an E shadow.

At v+1 only the center differs. At v+3 and v+5 the highest discrepancy
is exactly position -2. Equations (3) and the table give all seven b
values in Section 1, including b(v+5)=3 even though its delay is only 1.

## 4. The exact delay and renewal profiles

Use the imported threshold identity

    b(Y_(t+n))>n iff tau(Y_t)>n.

For t=v+1, the b value at v+3 is 3>2 and the value at v+4 is 2<=3;
hence tau(Y_(v+1))=3. For t=v+3, use b(v+5)=3>2 and b(v+6)<=1<=3
to get the same exact delay 3. The adjacent b values similarly give
tau(v+2)=tau(v+4)=2. At v+5 the row is not cyclic, but b(v+6)<=1,
so tau(v+5)=1. At even v and v+6, a center-only defect is erased by
the common left neighbor 1, giving the remaining tau values. This proves
the whole delay table without treating b and tau as equal row by row.

Substitution into R_t=tau_(t+1)-max(tau_t-1,0) gives

    (R_v,R_(v+1),...,R_(v+5))=(3,0,2,0,0,e).        (4)

The total for this six-step passage is 5+e. This is an exact local
account, not a nonnegative bound from original finite support. Repeated
passages have not been bounded.

The original-cut global-front identity gives a coordinate check and a
precise target for a future budget argument. With s_j=tau(L_j) for the
ORIGINAL cuts, the seven thresholds in this passage are

    (s_v,...,s_(v+6))
      =(v+1,v+4,v+4,v+6,v+6,v+6,v+6+e).            (4a)

All but the last follow from positive tau_j=s_j-j. If e=0, monotonicity
and s_(v+5)=v+6 force s_(v+6)=v+6, so the last equality holds too.
Thus the first injection is the residence of characteristic v+1 over
[v+1,v+4), and the second is the residence of v+3 over [v+4,v+6).
Their erasing 1s are at physical cells (-3,v+3) and (-3,v+5), respectively.
The global front is at -2 at both last residence times. At v+6 it is at
0 if e=1 and strictly right of 0 if e=0; the global front still exists.
These are ordered erasers in one spacetime, not distinct
original ancestors or a proof of bounded ancestor reuse. No front sample
or new experiment is used to obtain (4a).

There can be AT MOST ONE physical clock doubling in [v,v+6): if it occurs
it is the even step v+4 -> v+5. Indeed positive R excludes v and v+2.
The round306 odd-doubling obstruction excludes v+1,v+3,v+5 because their
next even rows have b<=2. At v+4 the delay is 2, so the imported even
two-step doubling law says that a doubling would force a CYCLIC repair:

    a doubling in this passage implies e=0,
    p_(v+6) is p_v or 2p_v.                          (5)

The converse e=0 implies doubling is NOT asserted. No existence of the
doubling branch or of an infinite sequence of these passages is claimed.

## 5. What the repair flag reads from the original shadow at this exit

Write the first five right cells of the shadow at v as

    (0,a,b,c,d).

The shadow's OWN center values at v,v+1,v+2,v+3 are 0,1,1,1. The first
three follow from (1) and the exit table; the fourth follows from (3) at
the post-exit ell=0 t row. Thus all four inputs for transporting its right
fringe to v+4 are justified by this same spacetime. Direct four-step
transport yields

    hat r_1(v+4)=(1 XOR a)*(1 XOR b)*(c OR d).         (6)

For a hand derivation, the shadow first-right bits after one, two, and
three steps are a, 1 XOR(a OR b), and a. If a=1, the fourth is 0. If
a=0, its second-right bit at step three is b OR((1 XOR c)*(1 XOR d));
the fourth first-right bit is its complement, giving (6).

Consequently the necessary repair condition is

    (1 XOR a)*(1 XOR b)*(c OR d)=0.                  (7)

These are bits of the globally selected shadow of the ORIGINAL finite row.
They are not independently supplied replacement right bits. Equation (6)
does not license reusing the center inputs 0,1,1,1 at a later source.
Nor does (7) prove that the repair condition is automatic on the admissible
domain. That correlation is precisely what a further all-depth argument
would have to establish or rule out.

## 6. Mandatory entry and an eventual decomposition (`partial-proof`)

The passage law becomes a description of the WHOLE late orbit after one
additional entry argument. Choose a common late cutoff for b<=3 and
tau<=3, using the imported threshold equivalences.

First, an even FULL row w whose shadow LOW A-trace is identically 1 must
be cyclic in this region. Its center agrees. Put delta_j=d_(-j)(w) for
bit indices j=0,1,2; bits>=3 agree. Since both centers
are 1, the lowest A difference is exactly delta_2. Actual (A Y_w)[0]=1 XOR u,
while its shadow value is 1, so delta_2=u. If u=1, delta_2=1 is the highest
disagreement and its common neighbor at bit3 is 0. One physical step
would produce b>=4. Therefore u=delta_2=0. If delta_1=1, Section 2 with ell=0
applies. Its second A difference has low bit zero; the shadow low bit
is 1, so the actual second A low bit, hence z, is 1 too. But Section 2
then forces b(w+2)=4. Thus delta_1=0 and the row is cyclic.

At ANY doubling, the periodic shadow at two physical steps later has low
A-trace identically 1: the first lifted trace visits both bits and the
second lift has its unique recurrent low bit 1. This statement is about
the periodic shadow and does not assume that either actual successor is
already cyclic. Consequently every sufficiently late EVEN doubling has
a cyclic even row at t+2 by the preceding paragraph. The threshold
identity also gives tau_t<=2, sharpening the mere assumed bound 3 at
these sources.

Now suppose a sufficiently late doubling is ODD, and put w=t+1 even.
Its shadow high A-trace is identically zero. Since b_w<=3, its bit1 is
0 and its bit3 agrees with actual bit3=1 XOR u. Requiring its next A
high bit to be zero forces shadow bit2=1 XOR u. Thus delta_1=delta_2=1.
The third bit would move out of the strip at the next physical step if
u=1, so the gate at w is t. Let ell=d_0(w).

Clock consumption gives tau_w<=2. If ell=0, the first physical update
has only a -1 defect on its negative half; its shared -2 bit is 0.
The next update therefore has d_-2(w+2)=1. Threshold transport gives
tau_w>2, a contradiction. Hence ell=1. The actual low four bits are
(1,1,0,1), the shadow low four bits are (0,0,1,1), and all higher bits
agree. One A step identifies the entire rows, so tau_w=1 and tau_t=2.
At w+1 the negative halves agree; its actual left neighbor is 1 because
the gate at w was t. It shields the possible center discrepancy at the
next step. Thus the even row w+2=t+3 has negative-half agreement.

Unbounded clocks supply a doubling after the common cutoff. Either parity
therefore supplies ONE late even entry into negative-half agreement.
Thereafter the one-bit table gives either another one-bit row two steps
later, or the exit (1); Sections 1-3 return that exit to the same region
six steps later. These strictly advancing passages describe the whole
remaining orbit, with no unexamined gaps or independent fringe choices.

In particular every sufficiently late EVEN row has b<=2: outside exits
it has b<=1, and inside them the only intermediate even depths are 2,2.
The odd-doubling obstruction then forbids EVERY sufficiently late odd
doubling. All late even doublings have source delay at most 2 and return
to a cyclic even row two steps later. If such a doubling lies within
one of the exit passages, Section 4 places it precisely at offset 4.
Unbounded clocks therefore give infinitely many cyclic even returns.
No uniform bound on the time between those returns is established.

This is an eventual decomposition under K=3, not a finite-state closure
or a proof of eventual K=1. The one-bit exits may still occur infinitely
often. Their return flags, their frequency, and the original finite
support constraint remain part of the full coupled evolution.

Further corollaries sharpen its scope. First,

    eventual all-physical tau<=3
      iff eventual EVEN-time tau<=2.                (8)

For the forward direction, eventual even b<=2 and the threshold identity
with n=2 give tau<=2 at every sufficiently late even source. Conversely,
the imported physical bridge bounds an odd delay by one plus the next
even delay, giving all-physical tau<=3. The analogous EVEN-time bound 1
implies all-physical tau<=2 and hence eventual K=1 by the collapse theorem.

Second, if eventual K=3 holds but eventual K=1 does not, infinitely many
exit passages (1) must occur after entry. They are disjoint as half-open
intervals [v,v+6); the repaired endpoint belongs to the following passage.
If only finitely many occurred, the last repaired even row would stay in
negative-half agreement forever and threshold transport would give K=1.
Thus the remaining distinct three-bit alternative requires infinitely
many of the exact 3,2 injection pairs in (4). This is a necessary supply,
not a proof that a finite original boundary can or cannot supply it.

Finally, the mandatory supply can still be counted at CYCLIC-source births,
even though the intervening exits inject additional delay. Choose a late
paired cutoff M after entry and the exclusion of odd doublings. Put

    X_m=Y_(2m), I_m=indicator[tau(X_m)>0],
    B_m=indicator[I_m=0 and I_(m+1)=1].

Every late clock doubling has I_m=1 and I_(m+1)=0, by the even cyclic
return just proved. There may also be returns without doubling. Counting
binary 0->1 and 1->0 switches on [M,N) therefore gives

    sum_(m=M..N-1) B_m
      >= log_2(p(X_N)/p(X_M)) - I_M + I_N.           (9)

Indeed the number of 1->0 switches is exactly sum B_m+I_M-I_N and bounds
the number of doublings from above. Odd doublings are absent on this
interval, so the latter number is exactly the logarithm in (9).
Every B_m=1 is a cyclic-to-lag-one transition. The round305 birth identity
identifies it, on these same original spacetimes, as

    B_m=indicator[I_m=0] * (u_(2m) XOR hat u_(2m)).

Thus unbounded clocks require infinitely many of the original cyclic-source
gate disagreements even in the three-bit case. An infinite series of
repairs within a single noncyclic episode cannot substitute for that birth
supply: such an episode can contain at most one doubling, and that doubling
ends it with a cyclic return.
No upper bound on this birth count from finite initial support is supplied.

## 7. Verification and stopping fence

`check_round306_three_bit_repair.py` checks exactly sixteen local assignments
for Section 2: ell in {0,1}, input bit4 in {0,1}, and the four shadow right
pairs. The actual right pair is fixed to (1,0). The bit4 variable is NOT
claimed to be the next actual gate in these arbitrary local controls;
that identification in the proof requires the FULL continuation.
It separately checks all sixteen assignments a,b,c,d in (6), using the
specified shadow center inputs. No local test row is asserted to be an
E shadow or an infinite FULL realization.

The entry argument adds two precisely bounded algebra checks. The first
ranges over u,delta_1,delta_2,bit4,bit5 in {0,1} (32 assignments), with equal
centers 1 and equal bits>=3. It checks that shadow A low bits 1 at the
next two A times and the necessary next-two-step strip restrictions
force delta_1=delta_2=0. The second checks the two odd-doubling successor patterns
ell in {0,1}, the four shared bit4/bit5 choices and four shadow right
pairs (32 assignments): ell=0 has a -2 defect two physical steps later,
whereas ell=1 is identified by one A step and has negative-half agreement
two physical steps later. Actual right pair is (1,0), with gate t.

Admission: a failure rejects the new algebra, while agreement certifies
only these ninety-six assignments. The clock and induction deductions are
mathematical, conditional on the stated imports, not numerical results.
Caps: one local CPU, 10 seconds, 128 MiB, at most four physical steps,
128 KiB output. Atomic provenance:
`results/problem1/20260907_round306_three_bit_repair.json`.

The new obstruction to a simple width induction is an EXACT conditional
repair branch with its own required full-shadow flag and two injections.
It is not a counterexample to eventual K=3 collapse. Do not enumerate more
widths, gates, source codes, or shadow flags. The continuing question is
whether the complete finite actual boundary and uniquely selected shadow
can sustain the required passages and clock doublings indefinitely.

Dependencies: `problem1_one_bit_shadow_exit.md`;
`problem1_shadow_gate_birth_phase.md` for the cyclic birth indicator;
`problem1_two_bit_strip_collapse.md` Sections 2-3;
`problem1_physical_time_cycle_defects.md` Section 2;
`problem1_cycle_delay_renewal.md` Sections 2-3;
`problem1_global_discrepancy_front.md` Sections 1-3 for (4a);
`problem1_period_two_fringe_language.md` (no-uu and no-ttttt).
