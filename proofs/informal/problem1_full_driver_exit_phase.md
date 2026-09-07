# The complete periodic driver decides a one-bit exit

Status: `partial-proof` for the conditional all-depth identities. Fresh
external adversarial review is missing. Fixed algebra checks have only their
declared `finite-exhaustive` scope. No finite FULL survivor, eventual strip
bound, or finite birth budget is established. Problem 1 remains OPEN.

## 0. Admission and route choice

Round306 reduces eventual K=2 to K=1 and describes the K=3 repairs. The
remaining common obligation is to control infinitely many cyclic births on
ONE actual orbit while meeting its no-exit or repair conditions. The two
shadow right bits cannot be freely supplied at each return.

Rankings (`heuristic`): first eliminate the remaining shadow exit bit using
the COMPLETE periodic driver, including the phase of a nonresetting lift;
second transport a nonnegative birth count to the finite original support;
third control repeated K=3 repairs with that same driver. The first route
has an exact algebraic test and can either remove a purported free phase or
show where additional original-boundary data remain necessary. The second
still lacks bounded reuse; the third cannot be settled by more local flags.

This note does not repeat the physical exit table. It identifies the phase
selected by the actual transient, then expresses the resetting alternative
as a backward word condition. There is no new source-word or prefix search.

## 1. One orbit and its entire periodic core

Keep ONE finite nonzero FULL actual spacetime r, its complete ORIGINAL
finite right fringe, and its global shadow hat r=U^t E(r(0)). At an even
time t suppose

    d_i(t)=0 for every i<=-1, d_0(t)=1.              (1)

Put x=Y_t and z=cyc(x). FULL gives the common left neighbor 1, so

    x=z XOR 1=z+1, z mod4=2, A x=A z, tau(x)=1.    (2)

Let b_s=Theta(z)_s, of least period p, extended periodically to all integer
A-times. Thus b_0=2, and for s>=1 it also equals Theta(x)_s. The actual
gate is u exactly when b_1=2; gate t has b_1=1. Write

    h=hat r_1(t), k=hat r_2(t).

The one-bit exit theorem says that (1) exits negative-half agreement at
t+2 exactly when the ACTUAL gate is u and h=0. We now determine h from
this complete b, with no eventual strip assumption.

## 2. A resetting driver gives an exact backward parity

The shadow cut ending at position 1 is 2z+h. If its low A-trace is w_s,
the one-bit scan obeys

    w_(s+1)=b_s[1] XOR (b_s[0] OR w_s).            (3)

Its maps for letters 0,1,2,3 are respectively identity, constant 1, flip,
constant 0. Suppose b contains 1 or 3. Then its recurrent extension is
unique. Define the last reset strictly before phase zero by

    ell=max{s<0:b_s in {1,3}},
    gamma=XOR_(s=ell+1..-1) 1[b_s=2].              (4)

The suffix in (4) contains only 0 and 2; ell lies in [-p,-1]. Equation (3)
sets w_(ell+1)=1[b_ell=1], then flips once for each 2 in that suffix.
Consequently

    h=1[b_ell=1] XOR gamma.                        (5)

This is an exact all-period identity. Negative indices are phases of this
ONE periodic core, not a negative-time prehistory of the actual row. The
lookback is not bounded independently of p.

In particular, at a lag-one u source the exit occurs precisely when

    gamma=1[b_ell=1].                              (6)

The no-exit condition instead reads gamma=1[b_ell=3]. This is a test of
the complete periodic word, not a freely chosen shadow-neighbor bit.

## 3. A nonresetting driver's phase is fixed by the actual transient

Suppose b is contained in {0,2}. Both one-bit extensions of z are cyclic;
that fact alone leaves a phase ambiguity, including the even-parity fork
already certified in round304. Nevertheless the shadow of THIS x selects

    (h,k)=(1,1).                                   (7)

Here is a phase-sensitive proof. Let a=r_1(t), so the ACTUAL cut at
position 1 is q=2x+a. Its first A low bit is

    (A q)[0]=x[1] XOR (x[0] OR a)=1 XOR 1=0.

Thus A q=2 A z. Since the low trace of A z is identically zero, 2 A z
is already cyclic. Therefore A cyc(q)=A q. Projection gives
cyc(q)=2z+h, and its next low bit, by b_0=2, is 1 XOR h. Equating this
with 0 proves h=1. This uses the ACTUAL transient (2); it does not select
one universal lift phase merely from finite support or the clock.

For the next shadow extension, the first extension's low trace w is a
permutation response to b and visits both bits: b_0=2 already flips its
initial value. The high trace of 2z+1 is identically zero. Hence the next
extension's scalar rule is v_(s+1)=w_s OR v_s. Its unique cyclic response
is identically 1, proving k=1. The least first-extension period may be p
or 2p; both cases have the same selected pair (7).

There is an independent paired-scan proof on the FULL u branch. The pair
state order is low-to-high: a state w represents r_2+2r_1. For drive
letters 0 and 2, the set {1,3} is invariant; H_0 fixes its two members
and H_2 interchanges them. Therefore 4z+3 is cyclic. The actual right
pair is 00, and its cut is 4x. At A-time zero its actual input symbol
is 3 while the core symbol is 2. The hand identities

    H_3(0)=1=H_2(3), A x=A z

give A(4x)=A(4z+3). Phase-correct completion therefore gives
cyc(4x)=4z+3, proving (7) again, including its phase. This proof uses
the actual pair 00; it is not a statement about arbitrary resetting scans.

Under FULL this case necessarily has gate u, since b_1 must be 1 or 2
and cannot be 1. The one-bit exit theorem and (7) give a cyclic even
successor at t+2, without a future strip premise. The same is true when
the count of 2s in one least period is EVEN: nonresetting does not mean
clock doubling. The first physical step doubles exactly when that count
is odd. Thus the old finite even-parity fork cannot be used as a freely
chosen no-exit/exit alternative on this fixed lag-one orbit.

## 4. The remaining simultaneous word constraints

At a cyclic even source, round305 already expresses the birth indicator as

    beta=1[b_1=2] XOR
         XOR_(s=j+1..-1)1[b_s=3],
    j=max{s<0:b_s in {1,2}}, b_0=3.                (8)

At a one-bit source, b_0=2. Section 3 shows that a driver in {0,2}
automatically returns, with the phase (7). If the driver contains 1 or 3,
Section 2 supplies (5)-(6). Hence under eventual K=1 the still-required
condition at EVERY sufficiently late lag-one u source is precisely

    b subset {0,2}, OR
    [b has a reset and gamma=1[b_ell=3]].            (9)

Infinitely many cyclic sources must meanwhile satisfy beta=1 by the
existing clock/birth count. These are different backward quotients of
the COMPLETE successive periodic cores: (8) resets on 1/2, whereas
(9) resets on 1/3. They are not two independently supplied word streams.
Both cores are selected by the same original actual fringe through E.

Under eventual K=3, every six-step repair begins instead at a resetting
core with (6). The nonresetting case cannot initiate a repair. No budget
for occurrences of (6), or for births (8), follows from these identities.
Spatial mortality of each finite core still has to be coupled to the
whole sequence of its actual physical returns.

## 5. Fixed validation and stopping fence

Pre-run admission: check the eight letter/bit scan values, the sixteen
compositions of the four scalar maps, the four invariant-pair transitions,
and the single phase certificate from the already known x=7, z=6.
A disagreement invalidates the corresponding algebra or phase selection;
agreement checks only that fixed algebra/certificate, not an infinite FULL
realization or a finite-support birth budget. No new code word is searched.
The maps' last-reset formula is proved by induction above, not inferred
from a period census.

Checker: `experiments/problem1_nonperiodicity/check_round307_exit_phase.py`.
Caps: one local CPU, 10 seconds, 128 MiB, 128 KiB output, and at most eight
A updates for each explicitly named certificate. It checks packed A
against a separate hand-rule cell implementation, after the hand rule and
cycle edges. Atomic record:
`results/problem1/20260907_round307_exit_phase.json`.

Do not enumerate more backward suffixes, core words, forks, or gate prefixes.
The unresolved implication is global: finite original support must prevent
the simultaneous infinite birth supply and the appropriate (9) or repair
conditions on ONE original realization. No such implication is proved here.

Dependencies: `problem1_global_cycle_shadow.md` Sections 1-2;
`problem1_one_bit_shadow_exit.md` Sections 1-2;
`problem1_shadow_gate_birth_phase.md` Section 3;
`problem1_physical_time_cycle_defects.md` Section 4;
`problem1_finite_cycle_phase_fork.md` Section 1;
`problem1_three_bit_exit_repair.md` Sections 1 and 6.
