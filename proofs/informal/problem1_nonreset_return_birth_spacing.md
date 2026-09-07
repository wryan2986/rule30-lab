# A nonresetting return has a prescribed next birth window

Status: `partial-proof`. Fresh MiMo review of this unit is recorded in
`problem1_round309_recovered_birth_review.md`; its earlier dependencies
are imported rather than claimed freshly reviewed end-to-end.
The fixed cone check has only its declared `finite-exhaustive` scope.
No infinite FULL realization or finite birth budget is proved. Problem 1
remains OPEN.

## 0. Admission and stopping criterion

The selected nonresetting phases are now known at both types of even
source. Test whether the next cyclic-source birth can actually be treated
as unconstrained immediately after that return. An exact restriction would
couple the continuing birth supply to the just-completed whole-driver
passage; failure would leave that proposed coupling unavailable. This is
one symbolic transport of the newly selected phases, not a search for
longer gate words, local flags, sources, or clock trees.

## 1. One current nonresetting source

Keep the ORIGINAL finite actual FULL row, its complete right fringe, and
its global E shadow. At one even physical time t assume

    N_t: the core Z_t has identically-zero low A-trace,
    b(Y_t)<=2.                                    (1)

The nonresetting-core theorem requires no future strip bound to give the
two possible source types. With u the actual gate-u indicator, both have

    shadow cells(-2,-1,0,1,2)=(u,u,0,u,1),
    source delay d=2-u,
    tau(Y_(t+1))=d-1, tau(Y_(t+2))=0.              (2)

The source u=1 is one-bit, while u=0 is the two-bit t source. Write
(a,b)=(hat r_3(t),hat r_4(t)), and set q=t+2. The shadow's OWN centers
at t,t+1,q are 0,0,1. Its right pair at q is exactly

    (hat r_1(q),hat r_2(q))=(1,u*(a OR b)).          (3)

Indeed the first-step shadow right cells are
(1,1 XOR u,1 XOR(a OR b)). The next center input is 0, giving (3).
The first shadow center is u XOR(0 OR u)=0; its first left neighbor is
also 0, giving the second shadow center 1. No artificial alternating
boundary was imposed on the shadow at the source.

## 2. Two consecutive cyclic even sources, with gates t then u

The cyclic row Y_q has constant-one core low trace. Let c=Theta(Y_q),
which is PURE. FULL gives c_0=3 and c_1,c_2 in {1,2}. Since every low
bit of c is 1, necessarily c_1=c_2=1. The actual gate at q is therefore
t, and the paired scan gives the actual gate at q+2 as u:

    (Theta(Y_(q+2)))_1=H_(c_2)(3)=H_1(3)=2.        (4)

Equation (3) makes the shadow zero-pair flag at q equal to 0, matching
the actual t gate's flag. The cyclic birth law therefore proves

    tau(Y_(q+1))=tau(Y_(q+2))=0.                   (5)

Thus the FIRST cyclic source after this N passage cannot create a birth.
The next even source q+2=t+4 is also cyclic and its actual gate is u.
There is no claimed finite-state update of later driver words.

## 3. The next birth is forced for the two-bit t source

Let rho_i=hat r_i(q). Since Y_q is cyclic, the already proved forward
flag law applies with the justified common centers1,0. It gives

    eta=hat u_(q+2)=rho_1*rho_2*(rho_3 OR rho_4)
                   =u*(a OR b)*(rho_3 OR rho_4).

The actual gate at q+2 is u, so its cyclic-source birth indicator is

    beta=1 XOR eta.                               (6)

All the rho_i are cells of the SAME global shadow. They are not free
choices for a new right fringe. In the TWO-BIT source case u=0,

    beta=1.                                       (7)

Equivalently, its return right pair in (3) is10, which makes the next
shadow zero-pair flag vanish regardless of the wider shadow. Thus this
repair-type N return necessarily creates a new lag-one even row at t+6.
In the one-bit source case u=1, formula (6) retains the wider driver;
neither value of beta is claimed to occur on an infinite FULL orbit.

The complete core can also be retained explicitly through this return.
With z=Z_t, the cyclic u-source at t+4 is exactly

    G(z)=Y_(t+4)=16 A^4 z+7.                       (6a)

Indeed the first paired successor is F x=4A^2x+3. At q its pure code
has c_2=1, so A^2(Fx)=4A^4x+1 and F^2x=16A^4x+7. Since the source
delay is at most2, A^4x=A^4z. This proves (6a), including its phase.
Its complete code is I_3 I_1 shift^4 Theta(z), so the old cyclic birth
quotient applied to THIS code is an alternative full-word expression
for beta. It is not a bounded observation or an arbitrary new driver.
The cyclicity and u gate of G(z) hold on the stated actual FULL domain;
they are not asserted for every finite nonresetting z in isolation.

The complete delay and injection profiles determined so far are

    delays at t,...,t+6: d,d-1,0,0,0,0,beta,
    injections at t,...,t+5: 0,0,0,0,0,beta.        (8)

At t+6 the actual gate is t by no-uu, whether beta is 0 or1. When
beta=1 this is a new one-bit t source; its core is resetting because
its code at A-time1 equals the actual gate symbol1.

In the eventual K=3 decomposition, a two-bit N source t is the offset4
row of a repair beginning at t-4. Its repair ends cyclic at t+2; the
new birth in (7) occurs at t+6, four physical steps after that repair's
endpoint. This is a forced continuation of ONE conditional passage,
not a construction of an infinite repeating repair/birth cycle.

## 4. A spacing consequence without searching a clock tree

No nonresetting source occurs at any time t+1,...,t+7. The even times
t+2,t+4 are cyclic with actual center1, so their core low trace cannot
be identically0. At t+6, beta=0 again means cyclicity; if beta=1, the
one-bit t source has core symbol1 at A-time1 and is resetting.

For the odd times, t+1 has the first nonresetting lift trace, which
visits both values. At each of t+3,t+5,t+7 the preceding even row is
cyclic or one-bit. A one-bit source has b_0=2 and its first-right trace
has consecutive values h,1 XOR h, so it cannot be identically0. At a
cyclic even FULL source, an identically-zero first-right trace would
force its entire core alphabet into {0,3}, contradicting its actual
gate symbol at A-time1 in {1,2}. These arguments cover all seven times.

Since a doubling requires a nonresetting source, the only possible clock
doubling on the EIGHT steps with source times t,...,t+7 is the first
one. Under eventual K=3 every late nonresetting source has the even
current bound (1). Consequently distinct sufficiently late N source
times, including the clock-preserving ones, differ by at least8.

This is a lower bound on spacing, not a positive lower density, a finite
number of returns, or an exclusion. In particular arbitrarily sparse
infinite doublings and births remain possible as far as these identities
show. Do not extend gate prefixes to refine this spacing without a new
all-depth budget mechanism.

## 5. Fixed validation and limits

Pre-run admission: check only the eight choices u,a,b in {0,1} in the
two-step shadow identity (3). A failed identity invalidates the proposed
post-return birth argument; agreement verifies that identity only. These
local rows are not asserted to be E shadows or FULL models. The actual
gate and cyclicity deductions are separate all-period arguments using
the complete core and the imported FULL scan identities.

`check_round307_nonreset_return.py` compares direct hand-rule cell cones
with independent packed physical Rule30 for the justified shadow centers
0,0,1 and the right pair (3). Eight hand rule values and a hand two-step
cone precede the check. Caps: one local CPU, 10 seconds, 128 MiB, two
physical steps, and 128 KiB output. Atomic record:
`results/problem1/20260907_round309_nonreset_return.json`.
The earlier round307 JSON is retained byte for byte as a historical run:
its proof hash became stale after subsequent edits. Round309 reruns the
same eight cones against the recovered current sources, with no new input.

The validated invocation uses a fresh Python child, under the SAME caps:

    python3 -c "import subprocess,sys; subprocess.run([sys.executable, 'experiments/problem1_nonperiodicity/check_round307_nonreset_return.py', '--output', 'results/problem1/20260907_round309_nonreset_return.json'], check=True)"

Three direct invocations reached and passed all algebra but failed the
final peak-memory assertion. The diagnostic run reported ru_maxrss above
161 MB alongside current-image VmHWM about20 MB and VmPeak about35 MB.
The [Linux getrusage manual](https://man7.org/linux/man-pages/man2/getrusage.2.html)
states that resource usage survives execve; a fresh child avoids carrying
the launching process's earlier peak into this checker. No cap was raised
and no failed invocation wrote a success record. The exact failed metrics
and final record audit are retained in the round307 review.

The forward zero-flag identity is an already verified dependency and is
not rerun on a new neighborhood collection. No further source or clock
sample is admitted. A global finite-support birth upper bound still has
to handle the forced regeneration (7), as well as the full-driver flag
left in (6). Neither an infinite compatible model nor a contradiction is
obtained from this finite-duration passage.

Dependencies: `problem1_nonresetting_core_returns.md` Sections 1 and 3;
`problem1_shadow_gate_birth_phase.md` Sections 1 and 4;
`problem1_exit_wait_front_residence.md` Section 4;
`problem1_full_fringe_temporal_diagonal.md` Section 4;
`problem1_period_two_fringe_language.md` (no-uu).
