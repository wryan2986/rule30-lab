# Cycle disagreements at each physical time step

Status: `partial-proof`; review and lead disposition are recorded in
problem1_round9_fresh_review.md and the handoff. This sharpens the
coordinate description of the current bottleneck; it does not exclude a
FULL finite-entry survivor or prove Problem1. No experiment is used.

## 0. Admission and scope

The new pair-depth transport identifies bounded cycle-entry delays with a
fixed spatial disagreement strip along one orbit. The remaining question
is whether grouping physical times in pairs hides where disagreements
are born or erased. An exact one-step identity would isolate those events
and avoid a parity loss; failure would expose a bad change of coordinates.
All rows below belong to ONE original physical spacetime. No right fringe
is reset, and no additional trace or period is searched.

Use physical Rule30

    r_i(t+1)=r_(i-1)(t) XOR (r_i(t) OR r_(i+1)(t)).

Let Y_t=sum_(i>=0) r_(-i)(t) 2^i be its center-and-left row and
c_t=r_0(t). Write sigma(y)=y>>1, so pi=sigma^2. The same A as in the
reviewed notes has bit rule A(y)_i=y_(i+2) XOR (y_(i+1) OR y_i).

## 1. The one-step bridge keeps the actual boundary (`partial-proof`)

At index i of sigma Y_(t+1), the physical output is r_(-i-1)(t+1).
The physical rule reads exactly the three bits i,i+1,i+2 of Y_t in
the A formula. Therefore, WITHOUT a periodic-center premise,

    sigma Y_(t+1)=A Y_t,
    Y_(t+1)=2 A Y_t+c_(t+1).                        (1)

The boundary bit in (1) is the ACTUAL next center. It is not a freely
chosen replacement for the missing right neighbor. Since sigma commutes
with A, iteration gives

    sigma^n Y_(t+n)=A^n Y_t, t,n>=0.                (2)

For an alternating center, Y_(2m)=X_m and Y_(2m+1)=2 A X_m.
The even-row pair3 and its permitted gate recover the earlier
X_(m+1)=4 A^2 X_m+3; (1) does not assume that identity for other traces.

Assume the Y_t are eventually A-periodic. A fixed finite initial right
fringe and finite entry of Y_0 suffice, as before: after one fixed
physical time the whole physical row is finite. Define tau_t=tau(Y_t)
and Z_t=cyc(Y_t), with the SAME phase-correct representative as in the
new pair-depth transport note. Then sigma also commutes with cyc, by
the same period-divisibility/commutation argument.

## 2. Exact bit-depth thresholds (`partial-proof`)

Define b(y)=min{j>=0:sigma^j y is A-periodic}, with infinity if absent.
Equivalently b(y)<=j iff sigma^j y=sigma^j cyc(y). If there are finitely
many disagreements, b(y) is one plus their highest bit index, or zero
when there are none. As in the pair version, b(y)<infinity for a
finite-entry y iff y is initially finite.

Combining (2) with the LEAST preperiod identity gives

    b(Y_(t+n))>n iff tau_t>n, t,n>=0.               (3)

This is an exact one-bit, one-physical-step threshold. In particular,

    tau_t<=K for all t>=T
       implies b(Y_s)<=K for all s>=T+K;
    b(Y_s)<=K for all s>=S
       implies tau_t<=K for all t>=max(0,S-K).     (4)

These statements concern eventual uniform bounds, not finiteness of
the individual quantities. They remain valid if some early b are infinite.
The two-step result is recovered by taking n even in (2)-(3), with
kappa(y)=ceil(b(y)/2) when b(y) is finite, and both infinite otherwise.

There is no uncontrolled odd-time gap under an alternating center.
Since sigma Y_(2m+2)=A Y_(2m+1),

    max(tau(Y_(2m+1))-1,0)
       =tau(sigma X_(m+1))<=tau(X_(m+1)).           (5)

Thus a bound K on all late even-row preperiods bounds the late odd-row
preperiods by K+1. Conversely any all-time bound covers the even rows.
The new description does not presume odd-row A-periodicity from even-row
A-periodicity; the possible extra step in (5) must be retained.

## 3. Disagreement births and the highest-bit rule (`partial-proof`)

Taking cycle representatives in (1), with a_(t+1)=Z_(t+1) mod2, gives

    Z_(t+1)=2 A Z_t+a_(t+1),
    Y_(t+1) XOR Z_(t+1)
      =2(A Y_t XOR A Z_t)+(c_(t+1) XOR a_(t+1)).    (6)

Here a_(t+1) is a cycle phase bit, not a physical fringe datum. If the
current disagreement set is finite and nonempty, with highest index d,
the next disagreement has highest index d+1 exactly when

    bit_(d+1)(Z_t)=0.                              (7)

If this bit is1, all next disagreements have index<=d, or vanish.
Proof: higher inputs agree, so the difference at index d after A is
the XOR of OR with one common neighbor bit, hence 1 XOR that bit.
It can never be recreated at d from lower positions. The new low-bit
term in (6) does not reach d+1. If there is no current disagreement,
only the new low bit can disagree. Disappearance therefore does not
imply that every subsequent row lies on its A-cycle.

Applying (7) twice yields the paired two-zero condition. Neither form
bounds the number of births or forces the highest index to escape a
fixed strip. In particular a finite strip still has an unbounded-period
higher driver; these equations are not an autonomous finite-state closure.

## 4. One-bit scans isolate the special period-two phase obstruction (`partial-proof`)

This section supplies only a local necessary condition, not a new
period-two exclusion. Put b=Theta(y), where b_t=(r_t,s_t) is a low/high
bit pair. For z=2y+a, let v_t=bit_0(A^t z). Since sigma commutes with A,

    Theta(z)_t=(v_t,r_t),
    v_(t+1)=s_t XOR(r_t OR v_t), v_0=a.             (8)

For the four input symbols0,1,2,3 the driven bit maps are respectively
identity, constant1, flip, constant0. If b has least eventual periodp,
a tail containing1 or3 resets this single-bit scan and preservesp.
A tail in{0,2} acts by permutations; its output has periodp or2p
according as the number of2s per least period is even or odd. The
all-zero case has period1. To justify LEAST periods, sigma is recovered
from the full code, so the input period divides the output period;
the indicated availablep or2p supplies the reverse divisibility bound.
Transient entry into a resetting response is not silently discarded.

There is an exact transient formula when y is itself A-periodic. If its
pure code has no1 or3, BOTH spatial extensions 2y and2y+1 are A-periodic:
every driven bit map is a permutation, including in the period-doubling
case. If its pure code contains1 or3, let

    rho=min{s>=0:Theta(y)_s is1 or3}.               (8a)

Exactly ONE choice of initial bit a gives an A-periodic extension2y+a.
The other has LEAST preperiod rho+1, with the same eventual periodp.
Indeed a reset determines a unique pure periodic driven response. The
wrong starting bit stays opposite under each identity/flip before the
first reset, then coalesces at that reset. Its last disagreement is
time rho, proving the least onset rho+1. When y is finite both extensions
are finite; no temporal-prefix-to-finiteness inference is needed.

By (1), a physical step applies (8) to y=A Y_t and a=c_(t+1).
Suppose p(Y_(t+1))=2p(Y_t), and suppose Y_t and Y_(t+2) are A-periodic.
The no-reset part above then makes Y_(t+1) A-periodic automatically.
The first row's pure code is contained in{0,2},
so c_t=0. The next row's pure code is contained in{0,1}, and contains1:
the first scan flips an odd number of times per input period, visiting
both bit states. The second scan, on{0,1} with a recurring1, has its
unique recurrent bit state1. Since Y_(t+2) is itself A-periodic, its
initial low bit is that recurrent1. Therefore

    every such doubling requires c_t=0, c_(t+2)=1. (9)

For an alternating trace c_(t+2)=c_t, (9) is impossible. In a general
periodic trace that equality need not hold. This locates an actual phase
restriction rather than importing the period-two argument unchanged to
other periods. No assertion about the frequency or admissibility of
doubling phases for periods>=3 is made, and no parameter work is opened.

More precisely, if Y_t is A-periodic, the step doubles its clock, and
the ACTUAL c_(t+2)=0, then Y_(t+2) is not A-periodic. Write
v_s=bit_0(A^s Y_(t+1)); its pure code is(v_s,0) and visits both0 and1.
In the second step the periodic drive is Theta(A Y_(t+1)), containing
only0 and1, with low bit v_(s+1). Its unique recurrent bit state is1,
whereas the actual initial bit is0. Formula(8a) therefore gives the exact
delay

    tau(Y_(t+2))=min{r>=1:v_r=1}.                  (10)

This is a waiting time in the SAME periodic response, not a lower bound
in terms of its least period. Large period need not make this particular
waiting time large. Formula(10) is useful for general actual traces.
For a FULL alternating trace the next section gives a stronger restriction:
a cyclic doubling source is impossible, so (10) supplies no actual
cyclic-source mechanism in that special setting.

## 5. Every physical doubling source is late under FULL (`partial-proof`)

An actual center1 followed by0 forces its left neighbor to be1 at the
first of those times, by the physical Rule30 rule. Consequently

    c_(t+1)=1, c_(t+2)=0
       implies bit_0(A Y_t)=r_-1(t+1)=1.           (11)

This uses the ACTUAL center, including its next two values. There is
no assumption on the right-neighbor bit and no cycle premise.

At ANY physical clock doubling, the least-period classification in(8)
forces the eventual code of Y_t to be contained in{0,2}, so its eventual
low-bit trace is identicallyzero. Under FULL with c_t=1 for even t,
c_t=0 for odd t, compare with the actual early bit:

    p(Y_(t+1))=2p(Y_t) implies
       tau_t>=1 if t is even,
       tau_t>=2 if t is odd.                       (12)

For even t its current low bit c_t=1 is exceptional. For odd t (11)
makes its low bit after ONE A step exceptional as well. This proves
the source itself is late at EVERY physical doubling. In particular,
no source of a physical doubling is A-periodic under FULL, even if
no periodicity assumption is made on the following rows.

With finite entry and a fixed finite initial fringe, the finite positive
Y_t have widths growing byone at every sufficiently late physical step,
by (1) and width preservation under A. The finite-code argument already
used in the reviewed clock-growth note therefore makes p(Y_t) tend to
infinity. Since a physical step preserves or doubles its least eventual
period, there are infinitely many such doublings. Their distinct source
times give, for N>=0,

    #{0<=t<N:tau_t>0} >= log_2(p(Y_N)/p(Y_0)).       (13)

This retains the source time at physical resolution. It does not imply
unbounded delay VALUES, or unbounded original anchored activity. The
earlier even-row type-{0,3} bound of at least THREE remains stronger in
its stated paired setting and is not weakened by(12).

## 6. Apply the waiting-time formula at the highest disagreement (`partial-proof`)

For a row Y_t with finitely many disagreements from Z_t and highest indexd,
put z=sigma^(d+1)Y_t. The agreement of all higher bits and commutation
with cyc make z A-periodic, while sigma^d Y_t=2z+a is the NONperiodic
bit extension: its low bit differs from that of sigma^d Z_t.
The reset case of(8a) therefore applies at this projected row, even though
Y_t itself is not A-periodic. It gives

    tau(sigma^d Y_t)
       =1+min{s>=0:bit_(d+1)(A^s Z_t)=1}
       <=tau(Y_t).                                (14)

In particular the displayed minimum exists; an identicallyzero driver
would make both extensions periodic, contradicting the highest
disagreement. Equation(14) is the first erasing time of that highest
bit. Lower disagreements may persist after it is erased, so equality
with tau(Y_t) is NOT asserted. This identifies the precise cyclic-tail
waiting time available at an actual late source, rather than wrongly
assuming the whole source row is cyclic.

## 7. Remaining obligation (`inconclusive`)

The sharper physical-time target is still to rule out every eventually
fixed disagreement strip for the ONE actual FULL realization. The
one-step formulation exposes the boundary births and exact erasing bits;
it does not control their whole future. Even unbounded strip width would
first establish unbounded delays, not by itself infinite original anchored
activity. No later-row threshold here is relabeled as an event of Y_0.

Dependencies: problem1_cycle_completion_defect_transport.md Sections1-5;
problem1_activity_sparse_temporal_codes.md Sections1-2;
problem1_full_fringe_temporal_diagonal.md Sections2-4;
problem1_activity_temporal_gate_bridge.md Sections1-2;
problem1_inverse_scan_reset_language.md Sections1-3;
problem1_scan_doubling_cycle_lag.md Section1 (the finite-code width argument).
